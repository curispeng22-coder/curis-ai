"""Wave 2 验证项 3（T14 研发真实引擎）。

覆盖：
- RdWorkflowRuntime.run() 注入 model_fn 路径可走通：6 步（需求理解/任务拆解/
  架构设计/编码/测试/交付）全部 completed，且最终报告含注入模型的产物标记。
- 不注入（或 model_fn 抛错）时降级 scaffold 不中断，闭环仍为 completed。

注意：研发部需先实例化（本测试在 seeded_db 上独立完成实例化）。
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

os.environ.setdefault("CURIS_CONNECTOR_MODE", "mock")

from app.company_instantiation import CompanyInstantiationService  # noqa: E402
from app.database import Database  # noqa: E402
from app.evolution_event_log import EvolutionEventLog  # noqa: E402
from app.rd_workflow_runtime import RdWorkflowRuntime  # noqa: E402
from app.tenant_context import DEFAULT_TENANT, TenantContext  # noqa: E402

import pytest  # noqa: E402


def _rd_department_id(db):
    with Database(db).connect() as conn:
        row = conn.execute(
            "select id from department_instances where department_type='tech.rd' limit 1"
        ).fetchone()
    return dict(row)["id"]


def test_rd_engine_model_fn_injection(seeded_db):
    """注入 model_fn：6 步 completed，报告含真实模型产物。"""
    db = Database(seeded_db)
    db.initialize()
    event_log = EvolutionEventLog(db)
    svc = CompanyInstantiationService(db, event_log)
    svc.instantiate("ccp_ai_software_company", DEFAULT_TENANT)
    rd_dept = _rd_department_id(seeded_db)

    MARKER = "[MODEL_INJECTED]"

    def fake_model(prompt: str) -> str:
        return f"{MARKER} 针对「{prompt[:12]}」的架构建议：采用分层服务。"

    rt = RdWorkflowRuntime(db, event_log, model_fn=fake_model)
    run = rt.run(rd_dept, "wl_ai_rd_software_dev_sop", "实现内容发布包导出能力")

    assert run["status"] == "completed", run
    # 6 个研发步骤全部 completed
    assert run["steps"] == 6, run["steps"]
    # 注入模型路径生效：最终报告包含模型产物标记
    assert MARKER in run["final_report"], "注入的 model_fn 未进入产物"


def test_rd_engine_scaffold_fallback_when_model_fails(seeded_db):
    """model_fn 抛错（无 key）→ 降级 scaffold，闭环不中断。"""
    db = Database(seeded_db)
    db.initialize()
    event_log = EvolutionEventLog(db)
    svc = CompanyInstantiationService(db, event_log)
    svc.instantiate("ccp_ai_software_company", DEFAULT_TENANT)
    rd_dept = _rd_department_id(seeded_db)

    def boom(_: str) -> str:
        raise RuntimeError("no api key configured")

    rt = RdWorkflowRuntime(db, event_log, model_fn=boom)
    run = rt.run(rd_dept, "wl_ai_rd_software_dev_sop", "降级验证")

    assert run["status"] == "completed", "降级路径不应中断闭环"
    assert run["steps"] == 6
    # 降级产物仍回写（scaffold 文案）
    assert "由" in run["final_report"]


def test_rd_engine_no_model_fn_scaffold(seeded_db):
    """完全不注入 model_fn：纯 scaffold 闭环可跑通。"""
    db = Database(seeded_db)
    db.initialize()
    event_log = EvolutionEventLog(db)
    svc = CompanyInstantiationService(db, event_log)
    svc.instantiate("ccp_ai_software_company", DEFAULT_TENANT)
    rd_dept = _rd_department_id(seeded_db)

    rt = RdWorkflowRuntime(db, event_log)  # model_fn=None
    run = rt.run(rd_dept, "wl_ai_rd_software_dev_sop", "纯 scaffold 验收")
    assert run["status"] == "completed"
    assert run["steps"] == 6
