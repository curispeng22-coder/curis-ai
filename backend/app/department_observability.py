"""职能型部门「自可观测 / 元循环」facade（ADR-0017 D3.impl，issue 058）。

本模块在 D3 reservation（纯只读投影）基础上升级为**真实可观测**：
  - ``get_department_event_stream`` 由「全局 ``get_all()`` 投影」升级为**真实按部门
    关联**的查询：先经 ``DepartmentCatalog.get_manifest`` 校验 type_key 索引（未知
    type_key 抛 ``KeyError``），再按 ``tenant_id = TenantContext.current_tenant_id()``
    作用域（来自 S1 D1.impl）查询 ``evolution_events``，并以 payload 中的
    ``type_key``（部门→事件关联键）+ ``correlation_id`` 前缀做真实关联；单租户兜底
    （tenant == 'default' 且无关联事件）回退为全量投影（兼容 reservation 时期数据）。
  - ``get_department_metrics`` 真实聚合 ``evolution_events`` → 回填 ``call_count`` /
    ``success_rate`` / ``quality_line_hits``（均为真实数值，非仅声明）。
  - ``suggest_self_improvement`` 真实实现：基于观测生成部门自我建议 dict（**不自动
    改码、不自动触发 Governor**），并将观测快照持久化到 additive
    ``department_observations`` 表（tenant-scoped）。**默认不写 ``evolution_events``**
    （保持 ADR-0016 D3 追加写不变式）。

禁止区（延续 ADR-0024 / issue 054 / issue 058）：
  - 不接外部平台、不碰凭证、不触合规面；
  - 不做 L6 经济 / ROI、token-output-ratio（不回填经济度量 schema）；
  - 不做 Employee CRUD；
  - **默认不向 ``evolution_events`` 追加写、不新增写路径**；
  - 不加可视化 / 任何 API endpoint；
  - 不动 D1 的 ``TenantContext`` 不变式。
"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from .database import Database
from .department_catalog import DepartmentCatalog
from .tenant_context import DEFAULT_TENANT, TenantContext


@dataclass
class DepartmentMetrics:
    """部门自可观测指标封装（D3.impl：含真实计算数值）。

    在 reservation 的「仅声明」基础上，新增真实回填字段 ``call_count`` /
    ``success_rate`` / ``quality_line_hits``；``available_fields`` 仍静态声明可计算
    字段名，``schema_version`` 随真实实现升版至 ``"1.0"``。
    """

    type_key: str
    observed_at: str
    event_stream: list[dict[str, Any]] = field(default_factory=list)
    # ── D3.impl 真实计算数值（由 get_department_metrics 聚合回填）──
    call_count: int = 0
    success_rate: float = 0.0
    quality_line_hits: int = 0
    available_fields: list[str] = field(
        default_factory=lambda: ["call_count", "success_rate", "quality_line_hits"]
    )
    schema_version: str = "1.0"


class DepartmentObservability:
    """部门自可观测 facade（ADR-0017 D3.impl，issue 058）。

    读取既有的 ``evolution_events``（按 ``tenant_id`` 作用域 + payload 部门关联）与
    ``department_types``（经 ``DepartmentCatalog`` 校验 type_key 索引），无副作用（除
    自反馈快照写入 additive ``department_observations`` 表）。部门类型索引由内部
    ``DepartmentCatalog(self.database)`` 复用（D2 目录）。

    注：``evolution_events`` 表无 ``department_id`` 列，且 ``EvolutionEventLog`` 仅暴露
    跨租户未作用域的读（``get_all`` / ``get_by_correlation_id``），故本 facade 直接经
    ``Database`` 以 ``WHERE tenant_id = ?`` 做真实租户作用域关联查询（不修改
    ``evolution_event_log.py``，亦不调用其 ``.record`` 写路径）。``event_log`` 形参保留
    以维持与 D4 governance 一致的构造签名。
    """

    def __init__(self, database: Database, event_log: Any = None) -> None:
        self.database = database
        self.event_log = event_log

    # ── 内部辅助：事件行 → dict（解析 payload JSON）──
    @staticmethod
    def _event_from_row(row: Any) -> dict[str, Any]:
        event = dict(row)
        try:
            event["payload"] = json.loads(event["payload"])
        except (json.JSONDecodeError, TypeError):
            event["payload"] = {}
        return event

    # ── 内部辅助：部门→事件关联判定（payload.type_key 为主键，兼容 correlation_id）──
    @staticmethod
    def _event_matches_type(event: dict[str, Any], type_key: str) -> bool:
        """判断一条 evolution_event 是否属于某部门类型。

        关联契约（真实、确定性）：
          - payload 含 ``type_key == type_key``（部门→事件主关联键）；或
          - correlation_id 以 ``"<type_key>@"`` 前缀（辅助关联，兼容外部编排注入）。
        """
        payload = event.get("payload")
        if isinstance(payload, dict) and payload.get("type_key") == type_key:
            return True
        correlation_id = event.get("correlation_id") or ""
        return correlation_id.startswith(f"{type_key}@")

    def get_department_event_stream(
        self, type_key: str, limit: int = 50
    ) -> list[dict[str, Any]]:
        """返回某部门（经 catalog 索引校验）的**真实按部门关联**事件流。

        步骤：
        1. 经 ``DepartmentCatalog.get_manifest(type_key)`` 校验 type_key 存在于
           系统级部门类型目录；未知 type_key 抛 ``KeyError``。
        2. 按 ``tenant_id = TenantContext.current_tenant_id()`` 作用域查询
           ``evolution_events``（真实关联查询，依赖 S1 D1.impl 的 tenant_id 列）。
        3. 以 payload.type_key（部门→事件关联键）+ correlation_id 前缀做真实关联，
           仅保留与本 type_key 相关的事件，截断至最近 ``limit`` 条。
        4. 单租户兜底：当 tenant == 'default' 且本 type_key 无任何关联事件时，
           回退为返回该租户下的全量投影（兼容 reservation 时期未打标的数据）。

        不计算统计、不新增任何写、不调用写路径。
        """
        # 1) 索引校验：type_key 必须存在于目录（未知 key → KeyError）
        catalog = DepartmentCatalog(self.database)
        manifest = catalog.get_manifest(type_key)
        if manifest is None:
            raise KeyError(
                f"未知部门类型 type_key={type_key!r}："
                f"不在系统级部门目录中（须先经 D2 catalog 注册）"
            )

        # 2) 租户作用域真实关联查询（S1 D1.impl 的 tenant_id 列）
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            rows = connection.execute(
                "select * from evolution_events where tenant_id = ? order by event_id",
                (tenant_id,),
            ).fetchall()
        events = [self._event_from_row(row) for row in rows]

        # 3) 部门→事件真实关联
        correlated = [e for e in events if self._event_matches_type(e, type_key)]
        if limit and limit > 0:
            correlated = correlated[-limit:]

        # 4) 单租户兜底：default 租户下无关联事件 → 全量投影（兼容 reservation 数据）
        if not correlated and tenant_id == DEFAULT_TENANT:
            if limit and limit > 0:
                events = events[-limit:]
            return events
        return correlated

    def get_department_metrics(self, type_key: str) -> DepartmentMetrics:
        """返回部门自可观测指标（D3.impl：真实聚合回填数值）。

        内部调 ``get_department_event_stream``（真实关联事件流），聚合为
        ``DepartmentMetrics``：``call_count`` = 关联事件数；``success_rate`` =
        成功事件数 / 关联事件数（float 0..1，无关联事件时为 0.0）；
        ``quality_line_hits`` = 命中质量线定义的事件数。``available_fields`` 仍静态声明。
        """
        event_stream = self.get_department_event_stream(type_key)
        call_count = len(event_stream)
        success_count = sum(1 for e in event_stream if self._is_success(e.get("payload")))
        quality_hits = sum(1 for e in event_stream if self._is_quality_hit(e.get("payload")))
        success_rate = (success_count / call_count) if call_count else 0.0
        return DepartmentMetrics(
            type_key=type_key,
            observed_at=datetime.now(timezone.utc).isoformat(),
            event_stream=event_stream,
            call_count=call_count,
            success_rate=success_rate,
            quality_line_hits=quality_hits,
        )

    def suggest_self_improvement(
        self, type_key: str, observation: Any
    ) -> dict[str, Any]:
        """Meta-loop：部门基于观测触发「自我建议」（D3.impl 真实实现）。

        生成建议 dict（**不自动改码、不自动触发 Governor 编排**），并将观测快照
        持久化到 additive ``department_observations`` 表（tenant-scoped）。

        **默认不写 ``evolution_events``**（保持 ADR-0016 D3 追加写不变式）；本切片
        gate 未显式批准任何子写路径，故绝不向 ``evolution_events`` 追加写。

        Args:
            type_key: 部门类型键（须存在于 catalog，否则 KeyError）。
            observation: 观测对象；若为 ``DepartmentMetrics`` 则直接复用其数值，
                否则基于 ``get_department_metrics(type_key)`` 实时聚合。

        Returns:
            建议 dict（含建议条目、源指标快照、tenant_id、type_key、created_at、
            observation_id；``modifies_code`` / ``triggers_governor`` 均为 False）。
        """
        # 索引校验（与事件流一致）：未知 type_key → KeyError
        catalog = DepartmentCatalog(self.database)
        if catalog.get_manifest(type_key) is None:
            raise KeyError(
                f"未知部门类型 type_key={type_key!r}：须先存在于 department_types 目录"
            )

        # 解析观测指标：优先复用传入的 DepartmentMetrics，否则实时聚合
        if isinstance(observation, DepartmentMetrics):
            metrics = observation
        else:
            metrics = self.get_department_metrics(type_key)

        suggestion = self._build_suggestion(type_key, metrics)

        # 持久化观测快照到 additive department_observations（tenant-scoped）。
        # 注意：仅落本表；绝不写 evolution_events（ADR-0016 D3 追加写不变式）。
        observation_id = uuid.uuid4().hex
        tenant_id = TenantContext.current_tenant_id()
        metrics_json = json.dumps(
            {
                "type_key": metrics.type_key,
                "call_count": metrics.call_count,
                "success_rate": metrics.success_rate,
                "quality_line_hits": metrics.quality_line_hits,
            },
            ensure_ascii=False,
        )
        suggestion_json = json.dumps(suggestion, ensure_ascii=False)
        self.database.save_department_observation(
            observation_id=observation_id,
            tenant_id=tenant_id,
            type_key=type_key,
            metrics_json=metrics_json,
            suggestion_json=suggestion_json,
        )

        suggestion["observation_id"] = observation_id
        suggestion["tenant_id"] = tenant_id
        suggestion["type_key"] = type_key
        suggestion["created_at"] = datetime.now(timezone.utc).isoformat()
        return suggestion

    # ── 内部辅助：真实质量判定（确定性、文档化契约）──
    @staticmethod
    def _is_success(payload: Any) -> bool:
        """判定事件是否为「成功」。

        契约：payload 含 ``success: true``，或 ``status`` / ``outcome`` == 'success'。
        """
        if not isinstance(payload, dict):
            return False
        if payload.get("success") is True:
            return True
        status = str(payload.get("status", payload.get("outcome", ""))).lower()
        return status == "success"

    @staticmethod
    def _is_quality_hit(payload: Any) -> bool:
        """判定事件是否命中「质量线」定义。

        契约：payload 含 ``quality_line_hit: true``，或 ``quality_check`` == 'pass'，
        或 numeric ``quality_score`` >= 0.8。
        """
        if not isinstance(payload, dict):
            return False
        if payload.get("quality_line_hit") is True:
            return True
        if str(payload.get("quality_check", "")).lower() == "pass":
            return True
        score = payload.get("quality_score")
        return isinstance(score, (int, float)) and score >= 0.8

    @staticmethod
    def _build_suggestion(type_key: str, metrics: DepartmentMetrics) -> dict[str, Any]:
        """基于真实指标生成部门自我建议（纯数据，不触发任何副作用 / 改码）。

        返回 dict 明确声明 ``modifies_code=False`` 与 ``triggers_governor=False``，
        呼应 ADR-0025 LOCKED_ACTIONS（自动改码动作全程锁定）与「不自动触发
        Governor 编排」禁止区。
        """
        items: list[str] = []
        if metrics.call_count == 0:
            items.append(
                f"部门 {type_key} 暂无关联观测事件；建议先建立部门级事件埋点"
                f"（payload.type_key={type_key!r}）以启动自可观测。"
            )
        else:
            if metrics.success_rate < 0.8:
                items.append(
                    f"成功率 {metrics.success_rate:.2f} 低于质量线阈值 0.80，"
                    f"建议复盘失败事件根因并加固工具路由。"
                )
            if metrics.quality_line_hits == 0:
                items.append(
                    f"质量线命中数为 0（共 {metrics.call_count} 次调用），"
                    f"建议补充质量校验步骤（quality_check / quality_score）。"
                )
            if metrics.success_rate >= 0.8 and metrics.quality_line_hits > 0:
                items.append(
                    f"自可观测健康：成功率 {metrics.success_rate:.2f}、"
                    f"质量线命中 {metrics.quality_line_hits} 次，维持现状并定期复核。"
                )
        return {
            "type_key": type_key,
            "summary": (
                f"部门 {type_key} 自反馈建议（基于 {metrics.call_count} 次关联观测）"
            ),
            "items": items,
            "metrics_snapshot": {
                "call_count": metrics.call_count,
                "success_rate": metrics.success_rate,
                "quality_line_hits": metrics.quality_line_hits,
            },
            # 明确：仅生成建议，不自动改码、不触发 Governor
            "modifies_code": False,
            "triggers_governor": False,
        }
