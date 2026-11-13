"""AiToEarn 连接器（Wave 2 · C1 / D1）。

自托管 AiToEarn MIT 作为内容生成地基。Curis 工作流在「生成」步调用本连接器
产出结构化内容，再套用 ``ContentPublishPackage`` 契约。

模式：
- ``mock``：本地合成与真实端点同构的发布包（无需 docker）。
- ``real``：经内网 HTTP POST 到 ``AITOEARN_URL``（默认 http://localhost:8080）
  的 ``/api/create``；自有 AI key 以请求头 ``Authorization: Bearer <key>`` 注入，
  **绝不走 AiToEarn Relay**（禁用 Relay 由部署配置保证，见 deploy/aitoearn）。

设计红线：零第三方 SaaS、零 Relay、自有 AI key 仅经 Vault 解析后注入请求头。
"""

from __future__ import annotations

import os
from typing import Any, Sequence

from .base import ConnectorError, ServiceConnector
from ..content_publish_package import ARTIFACT_TYPES, ContentArtifact, ContentPublishPackage


class AiToEarnClient(ServiceConnector):
    name = "aitoearn"
    kind = "generation"
    description = "自托管 AiToEarn（MIT）内容生成地基：Create / Publish 规划。"

    def __init__(self, *, mode=None, base_url: str | None = None) -> None:
        super().__init__(mode=mode)
        self.base_url = (base_url or os.getenv("AITOEARN_URL", "http://localhost:8080")).rstrip("/")

    # ── 公开领域方法 ──────────────────────────────────────────────
    def generate(
        self,
        prompt: str,
        *,
        platforms: Sequence[str] | None = None,
        brand_voice_ref: str = "",
        language: str = "zh-CN",
        api_key: str | None = None,
        model: str | None = None,
        source_workflow: str = "wl_ai_content_content_production_sop",
    ) -> ContentPublishPackage:
        """生成内容并规范为 ContentPublishPackage。

        返回包对象供下游 social-auto-upload connector 消费（契约唯一对接面）。
        """
        if self.is_real():
            return self._generate_real(
                prompt,
                platforms=platforms,
                brand_voice_ref=brand_voice_ref,
                language=language,
                api_key=api_key,
                model=model,
                source_workflow=source_workflow,
            )
        return self._generate_mock(
            prompt,
            platforms=platforms,
            brand_voice_ref=brand_voice_ref,
            language=language,
            source_workflow=source_workflow,
        )

    # ── mock：本地合成同构发布包 ──────────────────────────────────
    def _generate_mock(
        self,
        prompt: str,
        *,
        platforms: Sequence[str] | None,
        brand_voice_ref: str,
        language: str,
        source_workflow: str,
    ) -> ContentPublishPackage:
        targets = list(platforms or ["xhs", "douyin"])
        title = _slug_title(prompt)
        artifacts = [
            ContentArtifact(
                type="copywriting",
                platform=targets[0],
                title=f"{title}（图文）",
                body=f"[AiToEarn·mock] 围绕「{prompt}」生成的图文文案：\n"
                f"- 钩子：你还在这样理解{prompt}吗？\n"
                f"- 正文：三个角度拆解，贴合{targets[0]}平台调性。",
                metadata={"engine": "aitoearn-mock", "tone": "亲切科普"},
            ),
            ContentArtifact(
                type="script",
                platform=targets[-1] if len(targets) > 1 else targets[0],
                title=f"{title}（口播脚本）",
                body=f"[AiToEarn·mock] 30 秒口播脚本：\n"
                f"开头：{prompt}到底怎么玩？\n正文：一步步讲清。",
                metadata={"duration_sec": 30, "engine": "aitoearn-mock"},
            ),
        ]
        return ContentPublishPackage.create(
            source_workflow=source_workflow,
            brand_voice_ref=brand_voice_ref,
            language=language,
            platforms_targeted=targets,
            artifacts=artifacts,
        )

    # ── real：内网 HTTP 调用自托管 AiToEarn ───────────────────────
    def _generate_real(
        self,
        prompt: str,
        *,
        platforms: Sequence[str] | None,
        brand_voice_ref: str,
        language: str,
        api_key: str | None,
        model: str | None,
        source_workflow: str,
    ) -> ContentPublishPackage:
        try:
            import requests
        except ImportError as error:  # pragma: no cover - requests 为既有依赖
            raise ConnectorError("requests 不可用，无法调用真实 AiToEarn 端点") from error

        url = f"{self.base_url}/api/create"
        headers = {"Content-Type": "application/json"}
        # 自有 AI key 仅经 Vault 解析后注入请求头；不落库、不转发 Relay。
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        payload: dict[str, Any] = {
            "prompt": prompt,
            "platforms": list(platforms or []),
            "language": language,
            "source_workflow": source_workflow,
        }
        if model:
            payload["model"] = model
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=120)
            resp.raise_for_status()
            data = resp.json()
        except Exception as error:  # noqa: BLE001 - 统一转为 ConnectorError
            raise ConnectorError(f"AiToEarn 真实端点调用失败：{error}") from error

        artifacts = _parse_aitoearn_artifacts(data)
        if not artifacts:
            raise ConnectorError("AiToEarn 返回内容为空或契约不匹配")
        return ContentPublishPackage.create(
            source_workflow=source_workflow,
            brand_voice_ref=brand_voice_ref,
            language=language,
            platforms_targeted=list(platforms or []),
            artifacts=artifacts,
        )


def _slug_title(prompt: str) -> str:
    cleaned = "".join(ch for ch in (prompt or "") if ch.isalnum() or ch in "一-鿿 ")
    cleaned = cleaned.strip().replace(" ", "")[:12] or "内容选题"
    return cleaned


def _parse_aitoearn_artifacts(data: dict[str, Any]) -> list[ContentArtifact]:
    """把 AiToEarn 返回的灵活 JSON 解析为 ContentArtifact 列表。

    兼容多种返回形态：``artifacts`` 数组 / ``copywriting``+``script`` 平铺字段。
    """
    artifacts: list[ContentArtifact] = []
    raw_list = data.get("artifacts") or []
    for item in raw_list:
        if not isinstance(item, dict):
            continue
        atype = item.get("type") or "copywriting"
        if atype not in ARTIFACT_TYPES:
            atype = "copywriting"
        artifacts.append(ContentArtifact(
            type=atype,
            platform=item.get("platform", ""),
            title=item.get("title", ""),
            body=item.get("body") or item.get("text") or "",
            metadata=item.get("metadata", {}) or {},
        ))
    if not artifacts and (data.get("copywriting") or data.get("script")):
        if data.get("copywriting"):
            artifacts.append(ContentArtifact(
                type="copywriting", title=data.get("title", "图文"),
                body=str(data["copywriting"]),
            ))
        if data.get("script"):
            artifacts.append(ContentArtifact(
                type="script", title=data.get("title", "脚本"),
                body=str(data["script"]),
            ))
    return artifacts
