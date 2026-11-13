"""Wave 2 验证项 1（W1 内容工作流 mock 端到端闭环）。

覆盖：
- CURIS_CONNECTOR_MODE=mock 下，ContentWorkflowRuntime.run 跑通
  生成(AiToEarn connector) → ContentPublishPackage 持久化 →
  逐平台发布(social-auto-upload connector, xhs/douyin)。
- 断言 published 非空、failed=[]、source_workflow 合规（wl_ai_content_*）。
- 断言发布包已持久化到 content_publish_packages 表。
- 静态断言：ContentWorkflowRuntime 工作流代码**不感知** CURIS_CONNECTOR_MODE
  （环境切换只发生在连接器层，工作流代码无需改动）。
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

os.environ.setdefault("CURIS_CONNECTOR_MODE", "mock")

from app.connectors import get_connector  # noqa: E402
from app.content_workflow_runtime import ContentWorkflowRuntime  # noqa: E402
from app.credential_vault import CredentialVaultService  # noqa: E402
from app.runtime_governance import AutoApproveSink  # noqa: E402
from app.database import Database  # noqa: E402
from app.evolution_event_log import EvolutionEventLog  # noqa: E402
from app.tenant_context import DEFAULT_TENANT, TenantContext  # noqa: E402

import pytest  # noqa: E402

SRC = Path(__file__).resolve().parent.parent / "app" / "content_workflow_runtime.py"


def test_connector_mode_is_mock_by_default():
    """环境切换隔离：默认（及本测试）处于 mock 模式。"""
    assert os.environ.get("CURIS_CONNECTOR_MODE", "mock") == "mock"
    aitoearn = get_connector("aitoearn")
    sau = get_connector("social_auto_upload")
    assert not aitoearn.is_real()
    assert not sau.is_real()


def test_content_workflow_mock_end_to_end(seeded_db):
    """W1 端到端：生成→发布包→发布，两平台均发布，包已持久化。"""
    db = Database(seeded_db)
    db.initialize()
    event_log = EvolutionEventLog(db)
    vault = CredentialVaultService(db, event_log)

    with TenantContext.scope(DEFAULT_TENANT):
        cwr = ContentWorkflowRuntime(db, event_log, vault)
        result = cwr.run(
            prompt="春季护肤：3 个被忽略的误区",
            platforms=["xhs", "douyin"],
            source_workflow="wl_ai_content_content_production_sop",
            decision_sink=AutoApproveSink(),
        )

    # 闭环状态
    assert result["status"] == "completed", result
    # 至少 1 个内容工件
    assert len(result["package"]["artifacts"]) >= 1
    # 两平台均发布，无失败
    assert set(result["published_platforms"]) >= {"xhs", "douyin"}, result["published_platforms"]
    assert result["failed_platforms"] == [], result["failed_platforms"]

    # 持久化核对
    persisted = db.get_content_publish_package(DEFAULT_TENANT, result["package"]["package_id"])
    assert persisted is not None, "发布包未持久化"
    assert persisted["status"] == "published", persisted["status"]
    # source_workflow 合规
    assert persisted["source_workflow"].startswith("wl_ai_content_"), persisted["source_workflow"]
    # 内容工作流运行记录存在
    runs = db.list_content_workflow_runs(DEFAULT_TENANT)
    assert any(r["run_id"] == result["run_id"] for r in runs)


def test_workflow_code_does_not_branch_on_connector_mode():
    """验证项 1 关键红线：工作流代码不感知 CURIS_CONNECTOR_MODE。

    切换 mock↔real 仅由连接器层（base.py / *_client.py）处理，
    ContentWorkflowRuntime 不应 import os.getenv 去读该 env。
    """
    assert SRC.exists()
    text = SRC.read_text(encoding="utf-8")
    assert "CURIS_CONNECTOR_MODE" not in text, "工作流代码不应直接读取连接器环境模式"
    assert "os.getenv" not in text, "工作流代码不应做环境分支"


def test_publish_package_schema_contract():
    """发布包契约：重试真实连接器时契约字段一致（静态一致性核对）。"""
    aitoearn = get_connector("aitoearn")
    sau = get_connector("social_auto_upload")
    # 两连接器 catalog 条目不泄露任何凭证字段
    for c in (aitoearn, sau):
        entry = c.as_catalog_entry()
        assert set(entry.keys()) <= {"name", "kind", "description", "mode"}
