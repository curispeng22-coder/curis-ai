"""内容工作流运行时（Wave 2 · W1 串联真实闭环）。

把 C1 的真实 Connector 与 ContentPublishPackage 契约串联成端到端链路：

    生成(AiToEarn connector) → 发布包(ContentPublishPackage) → 发布(social-auto-upload connector)

- mock 模式（默认，无 docker）：先验证 schema 串联，返回模拟发布回执。
- real 模式（D1/D2 端点就绪后，改 env 即可，不改本文件）：调真实内网端点。
- 自有 AI key 与平台 cookie 均来自 Vault，由编排层在调用 connector 前解析，
  **不写入代码/DB**。

本运行时复用既有 ``Database`` / ``EvolutionEventLog``，并把生成的发布包持久化到
``content_publish_packages`` 表（供 F2 成果展示中心消费）。
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from html import escape
from typing import Any, Callable

from .connectors import ConnectorError, get_connector
from .content_publish_package import ContentArtifact, ContentPublishPackage
from .credential_vault import CredentialVaultService, is_resolver_managed_ref
from .database import Database
from .tenant_context import TenantContext
# B 层运行时治理边界（T07 接线点）：G1 真实发布 + G2 对外发。
from .runtime_governance import (
    ActionContext,
    evaluate,
    load_config,
    outcome_for_letter,
)
# 真实 DecisionSink 后端机制（T-DS1 接线信号；仅类型依赖，零新依赖）。
from .decision_sink import PendingDecisionRaised


# 平台 → Vault 凭证 provider 映射（用于按平台解析创始人 cookie）。
PLATFORM_PROVIDER = {
    "douyin": "social_platform_douyin",
    "xhs": "social_platform_xhs",
    "xiaohongshu": "social_platform_xhs",
    "video_account": "social_platform_video_account",
    "bilibili": "social_platform_bilibili",
    "kuaishou": "social_platform_kuaishou",
    "tiktok": "social_platform_tiktok",
    "youtube": "social_platform_youtube",
}


def platform_provider(platform: str) -> str:
    return PLATFORM_PROVIDER.get(platform, f"social_platform_{platform}")


class ContentWorkflowRuntime:
    """内容生产→发布端到端运行时。"""

    def __init__(
        self,
        database: Database,
        event_log: Any,
        credential_vault: CredentialVaultService | None = None,
    ) -> None:
        self.database = database
        self.event_log = event_log
        self.credential_vault = credential_vault

    def run_model_preview(
        self,
        *,
        task_prompt: str,
        trend_source: str,
        trend_summary: str,
        platforms: list[str],
        model_fn: Callable[[str], dict[str, Any]],
        brand_voice_ref: str = "",
        department_id: str = "",
    ) -> dict[str, Any]:
        """用已选模型生成内容发布包；只产出预览，不执行外部发布。"""
        tenant_id = TenantContext.current_tenant_id()
        run_id = f"cwr-{uuid.uuid4()}"
        workflow_id = "wl_ai_content_content_production_sop"
        self._insert_run(
            run_id,
            tenant_id,
            department_id,
            workflow_id,
            platforms,
            status="running",
            steps_total=5,
        )
        try:
            model_result = model_fn(self._model_prompt(
                task_prompt,
                trend_source,
                trend_summary,
                platforms,
            ))
            package = self._package_from_model(
                model_result,
                trend_source=trend_source,
                trend_summary=trend_summary,
                platforms=platforms,
                brand_voice_ref=brand_voice_ref,
                source_workflow=workflow_id,
            )
        except Exception:
            self._fail_run(run_id, "content_generation_failed")
            raise

        self._persist_package(tenant_id, package, status="generated")
        summary = (
            f"# 内容生产报告\n\n热点来源：{trend_source}\n"
            f"发布包：{package.package_id}\n目标平台：{', '.join(platforms)}\n"
            "外部发布：未执行"
        )
        self._complete_run(run_id, 5, 5, summary, status="completed")
        self.event_log.record(
            correlation_id=run_id,
            event_type="content_workflow.executed",
            tenant_id=tenant_id,
            payload={
                "source_workflow": workflow_id,
                "platforms": platforms,
                "published": [],
                "failed": [],
                "status": "completed",
                "mode": "model_preview",
            },
        )
        return {
            "run_id": run_id,
            "status": "completed",
            "package": package.to_dict(),
            "steps": [
                {"name": "热点依据", "status": "completed"},
                {"name": "选题", "status": "completed"},
                {"name": "文案与脚本", "status": "completed"},
                {"name": "图片资产", "status": "completed"},
                {"name": "复盘计划", "status": "completed"},
            ],
            "model_usage": {
                key: model_result.get(key)
                for key in (
                    "model_gateway_id",
                    "model_name",
                    "prompt_tokens",
                    "completion_tokens",
                    "total_tokens",
                    "estimated_cost",
                    "currency",
                    "fallback_used",
                    "fallback_from_model",
                    "fallback_reason",
                )
                if model_result.get(key) is not None
            },
            "summary": summary,
        }

    # ── 端到端：生成 → 发布包 → 发布 ─────────────────────────────
    def run(
        self,
        *,
        prompt: str,
        platforms: list[str],
        brand_voice_ref: str = "",
        language: str = "zh-CN",
        source_workflow: str = "wl_ai_content_content_production_sop",
        department_id: str = "",
        company_id: str | None = None,
        ai_key_credential_ref: str | None = None,
        model: str | None = None,
        decision_sink: Any = None,
        pending_sink: Any = None,
    ) -> dict[str, Any]:
        """跑通一条内容闭环，回写 content_workflow_runs + content_publish_packages。

        返回运行摘要（含发布包、各平台发布回执）。
        """
        tenant_id = TenantContext.current_tenant_id()
        run_id = f"cwr-{uuid.uuid4()}"
        self._insert_run(run_id, tenant_id, department_id, source_workflow, platforms, status="running")
        # B 层运行时治理 · 配置加载（tenant-scoped，单租户 selfuse）。
        self._gov_config = load_config()

        # 1) 生成（AiToEarn connector）
        aitoearn = get_connector("aitoearn")
        api_key = self._resolve_secret(ai_key_credential_ref) if ai_key_credential_ref else None
        try:
            package = aitoearn.generate(
                prompt,
                platforms=platforms,
                brand_voice_ref=brand_voice_ref,
                language=language,
                api_key=api_key,
                model=model,
                source_workflow=source_workflow,
            )
        except ConnectorError as error:
            self._fail_run(run_id, str(error))
            raise

        self._persist_package(tenant_id, package, status="generated")

        # 2) 发布（social-auto-upload connector，逐平台）
        sau = get_connector("social_auto_upload")
        receipts: list[dict[str, Any]] = []
        published_platforms: list[str] = []
        failed_platforms: list[str] = []

        # B 层运行时治理 · G1 真实发布 + G2 对外发（发布循环前评估）。
        # 用户选 A 才执行 sau.publish；B 先内部预览；C 取消（不发布）。
        gate_result = self._governance_gate_before_publish(
            decision_sink, run_id, tenant_id, pending_sink=pending_sink,
        )
        # 顶层无 resume 编排：pending 信号 → fail-closed 取消（不静默误用）。
        if isinstance(gate_result, PendingDecisionRaised):
            self._fail_run(
                run_id, "B 层治理闸等待外部决策，本期未启用 resume，按取消处理"
            )
            return {
                "run_id": run_id,
                "status": "cancelled",
                "package": package.to_dict(),
                "published_platforms": [],
                "failed_platforms": [],
                "receipts": [],
                "summary": "B 层治理闸等待外部决策（本期未启用 resume 编排）",
            }
        if not gate_result:
            # 落库状态受 content_workflow_runs 约束（running/completed/failed）；治理闸取消属
            # "未发布"，以 failed + 摘要说明。返回态保留 cancelled 供调用方识别治理结果。
            self._fail_run(run_id, "用户经 B 层治理闸取消发布")
            return {
                "run_id": run_id,
                "status": "cancelled",
                "package": package.to_dict(),
                "published_platforms": [],
                "failed_platforms": [],
                "receipts": [],
                "summary": "用户取消发布（B 层运行时治理闸）",
            }

        for platform in platforms:
            cookie = self._resolve_platform_cookie(platform)
            try:
                receipt = sau.publish(package, platform=platform, cookie=cookie)
                receipts.append(receipt)
                if receipt.get("status") == "published":
                    published_platforms.append(platform)
                else:
                    failed_platforms.append(platform)
            except ConnectorError as error:
                failed_platforms.append(platform)
                receipts.append({
                    "connector": "social_auto_upload",
                    "mode": sau.mode.value,
                    "status": "failed",
                    "platform": platform,
                    "package_id": package.package_id,
                    "message": str(error),
                })

        # 3) 收尾 + 持久化
        overall = "completed" if not failed_platforms else ("failed" if not published_platforms else "completed")
        summary = self._build_summary(prompt, package, receipts, published_platforms, failed_platforms)
        self._update_package_status(package.package_id, tenant_id,
                                     "published" if published_platforms else "failed",
                                     published_platforms)
        self._complete_run(run_id, len(platforms), len(published_platforms) + len(failed_platforms),
                           summary, status=overall)
        self.event_log.record(
            correlation_id=run_id,
            event_type="content_workflow.executed",
            tenant_id=tenant_id,
            payload={
                "source_workflow": source_workflow,
                "platforms": platforms,
                "published": published_platforms,
                "failed": failed_platforms,
                "status": overall,
            },
        )
        return {
            "run_id": run_id,
            "status": overall,
            "package": package.to_dict(),
            "published_platforms": published_platforms,
            "failed_platforms": failed_platforms,
            "receipts": receipts,
            "summary": summary,
        }

    # ── Vault 解析助手 ───────────────────────────────────────────
    def _resolve_secret(self, credential_ref: str) -> str | None:
        """解析 Vault 引用（local-dev / vault）为明文 secret；非引用返回原值。"""
        if not credential_ref:
            return None
        if is_resolver_managed_ref(credential_ref) and self.credential_vault is not None:
            try:
                return self.credential_vault.resolve(credential_ref)["secret"]
            except Exception:  # noqa: BLE001 - 解析失败视为无 key（降级 mock）
                return None
        return credential_ref

    def _resolve_platform_cookie(self, platform: str) -> str | None:
        """按平台从 Vault 找创始人 cookie 凭证。

        仅当配置了 CredentialVaultService 时尝试；未配置或缺失则返 None
        （mock 模式可降级，real 模式由 connector 抛错）。
        """
        if self.credential_vault is None:
            return None
        provider = platform_provider(platform)
        try:
            creds = self.credential_vault.list()["credentials"]
        except Exception:  # noqa: BLE001
            return None
        for cred in creds:
            if cred.get("provider") == provider and cred.get("status") == "active":
                ref = cred.get("credential_ref", "")
                if is_resolver_managed_ref(ref):
                    try:
                        return self.credential_vault.resolve(ref)["secret"]
                    except Exception:  # noqa: BLE001
                        return None
        return None

    # ── B 层运行时治理 · 决策评估与事件落点 ──────────────────────
    def _governance_gate_before_publish(
        self, decision_sink: Any, run_id: str, tenant_id: str, *, pending_sink: Any = None
    ) -> "bool | PendingDecisionRaised":
        """发布前评估 G1（真实发布）+ G2（对外发）。

        返回 ``True``=继续，``False``=用户取消；``pending_sink`` 注入且需弹闸时返回
        ``PendingDecisionRaised`` 信号（动作未执行，等 resolver 回填后 resume）。
        """
        g1 = evaluate(
            ActionContext(action_type="deploy", external=True, irreversible=True),
            self._gov_config,
        )
        if g1.needs_gate:
            return self._resolve_gate(g1, decision_sink, run_id, tenant_id, "G1-deploy", pending_sink=pending_sink)
        g2 = evaluate(
            ActionContext(action_type="external_send", external=True),
            self._gov_config,
        )
        if g2.needs_gate:
            return self._resolve_gate(g2, decision_sink, run_id, tenant_id, "G2-external", pending_sink=pending_sink)
        return True

    def _resolve_gate(
        self, decision: Any, decision_sink: Any, run_id: str, tenant_id: str, label: str,
        *, pending_sink: Any = None,
    ) -> "bool | PendingDecisionRaised":
        """经 DecisionSink 取决策；无 sink → fail-closed 取消。

        派发优先级（默认 ``pending_sink=None``、``decision_sink=None`` → fail-closed C）：
        ② ``pending_sink`` 注入且需弹闸 → 持久化 + 记录 ``pending`` + 返
           ``PendingDecisionRaised``；
        ③ 既有 ``decision_sink`` 注入 → 取字母并按中心映射落 outcome；
        ④ 默认（无 sink）→ fail-closed 默认取消。返回 ``True``=继续。
        """
        if pending_sink is not None:
            # 真实等用户拍板（非阻塞）：写入存储即返回 pending_id 信号。
            pending_id = pending_sink.ask(
                decision.gate,
                correlation_id=run_id,
                gate_label=label,
            )
            self._record_governance_gate(decision, "pending", run_id, tenant_id, label)
            return PendingDecisionRaised(
                pending_id=pending_id,
                gate_label=label,
                gate_id=getattr(decision.gate, "gate_id", ""),
            )
        if decision_sink is None:
            self._record_governance_gate(decision, "cancelled", run_id, tenant_id, label)
            return False
        letter = decision_sink.ask(decision.gate)
        # 统一经中心映射（③）：B→simulated，A→allowed，C→cancelled，D→alternative。
        outcome = outcome_for_letter(letter)
        self._record_governance_gate(decision, outcome, run_id, tenant_id, label)
        return letter in ("A", "B")

    def _record_governance_gate(
        self, decision: Any, outcome: str, run_id: str, tenant_id: str, label: str
    ) -> None:
        """落 ``b.governance.gate`` 事件（脱敏：无路径 / Key / 参数）。"""
        try:
            self.event_log.record(
                correlation_id=run_id,
                event_type="b.governance.gate",
                payload={
                    "gate_label": label,
                    "category": getattr(decision, "category", None),
                    "outcome": outcome,
                    "needs_gate": bool(getattr(decision, "needs_gate", True)),
                },
                tenant_id=tenant_id,
                idempotency_key=f"{run_id}:b-gov:{label}:{outcome}",
            )
        except Exception:  # noqa: BLE001 - 治理事件为尽力而为
            pass

    # ── 持久化助手 ───────────────────────────────────────────────
    def _insert_run(
        self, run_id: str, tenant_id: str, department_id: str,
        workflow_content_id: str, platforms: list[str], *, status: str,
        steps_total: int = 1,
    ) -> None:
        with self.database.connect() as connection:
            connection.execute(
                """
                insert into content_workflow_runs (
                  run_id, tenant_id, department_id, workflow_content_id,
                  status, steps_total, steps_done, summary, created_at, updated_at
                ) values (?, ?, ?, ?, ?, ?, 0, '', current_timestamp, current_timestamp)
                """,
                (run_id, tenant_id, department_id, workflow_content_id, status, steps_total),
            )

    def _complete_run(
        self, run_id: str, steps_total: int, steps_done: int, summary: str, *, status: str,
    ) -> None:
        with self.database.connect() as connection:
            connection.execute(
                """
                update content_workflow_runs set status = ?, steps_total = ?, steps_done = ?,
                  summary = ?, updated_at = current_timestamp where run_id = ?
                """,
                (status, steps_total, steps_done, summary, run_id),
            )

    def _fail_run(self, run_id: str, reason: str) -> None:
        with self.database.connect() as connection:
            connection.execute(
                "update content_workflow_runs set status = 'failed', summary = ?, "
                "updated_at = current_timestamp where run_id = ?",
                (reason[:500], run_id),
            )

    def _persist_package(
        self, tenant_id: str, package: ContentPublishPackage, *, status: str,
    ) -> None:
        self.database.save_content_publish_package(
            tenant_id=tenant_id,
            package_id=package.package_id,
            source_workflow=package.source_workflow,
            version=package.version,
            language=package.language,
            brand_voice_ref=package.brand_voice_ref,
            platforms_targeted=package.platforms_targeted,
            artifacts=package.artifacts,
            status=status,
            published_platforms=[],
        )

    def _update_package_status(
        self, package_id: str, tenant_id: str, status: str, published_platforms: list[str],
    ) -> None:
        self.database.update_content_publish_package_status(
            package_id=package_id,
            tenant_id=tenant_id,
            status=status,
            published_platforms=published_platforms,
        )

    @staticmethod
    def _build_summary(
        prompt: str, package: ContentPublishPackage,
        receipts: list[dict[str, Any]], published: list[str], failed: list[str],
    ) -> str:
        lines = [
            f"# 内容闭环执行报告",
            "",
            f"选题：{prompt}",
            f"发布包：{package.package_id} · v{package.version} · 工件 {len(package.artifacts)}",
            f"目标平台：{', '.join(package.platforms_targeted)}",
            f"已发布：{', '.join(published) or '无'}",
            f"失败：{', '.join(failed) or '无'}",
            "",
            "## 发布回执",
        ]
        for r in receipts:
            lines.append(f"- {r.get('platform')}: {r.get('status')} · {r.get('message')}")
        return "\n".join(lines)

    @staticmethod
    def _model_prompt(
        task_prompt: str,
        trend_source: str,
        trend_summary: str,
        platforms: list[str],
    ) -> str:
        return (
            "你是 Curis 内容生产员工。仅返回 JSON，不要 Markdown。"
            f"\n任务：{task_prompt}\n热点来源：{trend_source}\n热点摘要：{trend_summary}"
            f"\n目标平台：{json.dumps(platforms, ensure_ascii=False)}"
            "\nJSON 必须包含：trend_analysis 字符串；topic 对象(title, angle)；"
            "platforms 对象，每个平台含 title, body, image_headline, image_subtitle；"
            "retrospective 对象(hypothesis, metrics 字符串数组, next_review)。"
            "不得声称已发布或取得真实表现数据。"
        )

    @classmethod
    def _package_from_model(
        cls,
        model_result: dict[str, Any],
        *,
        trend_source: str,
        trend_summary: str,
        platforms: list[str],
        brand_voice_ref: str,
        source_workflow: str,
    ) -> ContentPublishPackage:
        raw = model_result.get("output") or model_result.get("content")
        if not isinstance(raw, str):
            raise ValueError("content model returned no structured output")
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as error:
            raise ValueError("content model returned invalid JSON") from error
        topic = data.get("topic")
        platform_data = data.get("platforms")
        retrospective = data.get("retrospective")
        trend_analysis = data.get("trend_analysis")
        if (
            not isinstance(trend_analysis, str)
            or not trend_analysis.strip()
            or not isinstance(topic, dict)
            or not all(isinstance(topic.get(key), str) and topic[key].strip() for key in ("title", "angle"))
            or not isinstance(platform_data, dict)
            or not isinstance(retrospective, dict)
            or not isinstance(retrospective.get("metrics"), list)
            or not retrospective.get("metrics")
            or not all(isinstance(item, str) and item.strip() for item in retrospective["metrics"])
            or not all(
                isinstance(retrospective.get(key), str) and retrospective[key].strip()
                for key in ("hypothesis", "next_review")
            )
        ):
            raise ValueError("content model output is incomplete")

        artifacts = [
            ContentArtifact(
                type="editorial_calendar",
                title=topic["title"].strip(),
                body=json.dumps(
                    {
                        "trend_source": trend_source,
                        "trend_summary": trend_summary,
                        "trend_analysis": trend_analysis.strip(),
                        "topic": topic,
                    },
                    ensure_ascii=False,
                ),
                metadata={"stage": "topic"},
            )
        ]
        for platform in platforms:
            item = platform_data.get(platform)
            if not isinstance(item, dict) or not all(
                isinstance(item.get(key), str) and item[key].strip()
                for key in ("title", "body", "image_headline", "image_subtitle")
            ):
                raise ValueError(f"content model output for {platform} is incomplete")
            artifacts.extend([
                ContentArtifact(
                    type="script" if platform == "douyin" else "copywriting",
                    platform=platform,
                    title=item["title"].strip(),
                    body=item["body"].strip(),
                    metadata={"stage": "copy"},
                ),
                ContentArtifact(
                    type="media_asset",
                    platform=platform,
                    title=f"{item['title'].strip()} · 封面",
                    body=cls._cover_svg(
                        platform,
                        item["image_headline"].strip(),
                        item["image_subtitle"].strip(),
                    ),
                    metadata={
                        "stage": "image",
                        "mime_type": "image/svg+xml",
                        "width": 1080,
                        "height": 1440,
                    },
                ),
            ])
        artifacts.append(ContentArtifact(
            type="multichannel_draft",
            title="发布后复盘计划",
            body=json.dumps(retrospective, ensure_ascii=False),
            metadata={"stage": "retrospective", "published": False},
        ))
        return ContentPublishPackage.create(
            source_workflow=source_workflow,
            brand_voice_ref=brand_voice_ref,
            platforms_targeted=platforms,
            artifacts=artifacts,
        )

    @staticmethod
    def _cover_svg(platform: str, headline: str, subtitle: str) -> str:
        colors = {
            "xhs": ("#ff2e4d", "#fff4f6"),
            "douyin": ("#111111", "#25f4ee"),
            "toutiao": ("#e5483f", "#fff5eb"),
        }
        background, accent = colors[platform]
        return (
            '<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1440" '
            'viewBox="0 0 1080 1440">'
            f'<rect width="1080" height="1440" fill="{background}"/>'
            f'<rect x="72" y="72" width="936" height="1296" rx="48" fill="{accent}"/>'
            f'<text x="120" y="170" font-size="42" font-family="sans-serif" fill="{background}">'
            f'{escape(platform.upper())}</text>'
            f'<text x="120" y="570" font-size="92" font-weight="700" font-family="sans-serif" '
            f'fill="{background}">{escape(headline[:16])}</text>'
            f'<text x="120" y="700" font-size="46" font-family="sans-serif" fill="{background}">'
            f'{escape(subtitle[:28])}</text>'
            f'<circle cx="850" cy="1130" r="110" fill="{background}" opacity=".16"/>'
            "</svg>"
        )
