"""Wave-1 验收：验证项 5（研发部闭环 RdWorkflowRuntime.run）。

运行方式（在 backend/ 目录下，使用项目 .venv）：
    ../.venv/bin/python -m pytest tests/test_v1_wave1_rd_runtime.py -v

覆盖：scaffold 模式（不注入外部 LLM key）跑通 6 步骤，
workflow_runs / workflow_steps / workflow_results / step_assignments
正确回写、无异常。
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))  # 使 v1_wave1_helpers 可导入

from v1_wave1_helpers import query, scalar, seed_wave1_full


def test_rd_runtime_closed_loop_scaffold(tmp_path):
    """验证项 5：RD 运行时 scaffold 闭环（6 步骤）正确回写。"""
    db = str(tmp_path / "curis.sqlite")
    seed_wave1_full(db)

    # 研发部闭环应写入 1 条 workflow_run、6 条 step、6 条 result。
    assert scalar(db, "select count(*) from workflow_runs") == 1
    assert scalar(db, "select count(*) from workflow_steps") == 6
    assert scalar(db, "select count(*) from step_results") == 6
    assert scalar(db, "select count(*) from step_assignments") == 6

    run = query(db, "select * from workflow_runs limit 1")[0]
    assert run["status"] == "completed"
    assert isinstance(run["final_report"], str) and len(run["final_report"]) > 0
    assert "completed" in run["final_report"]

    steps = query(
        db,
        "select status, output, employee_role, input from workflow_steps "
        "order by step_order",
    )
    assert len(steps) == 6
    for s in steps:
        assert s["status"] == "completed"
        assert isinstance(s["output"], str) and len(s["output"]) > 0
        assert isinstance(s["employee_role"], str) and s["employee_role"]
        assert isinstance(s["input"], str) and len(s["input"]) > 0

    results = query(db, "select status from step_results")
    assert all(r["status"] == "succeeded" for r in results)


def test_rd_runtime_run_return_shape(tmp_path):
    """run() 返回的摘要结构正确（步骤数 / 状态 / 无异常）。"""
    import sqlite3

    from app.company_instantiation import CompanyInstantiationService
    from app.database import Database
    from app.evolution_event_log import EvolutionEventLog
    from app.rd_workflow_runtime import RdWorkflowRuntime
    from app.tenant_context import DEFAULT_TENANT
    from app.wave1_seed import seed_wave1

    db = str(tmp_path / "curis.sqlite")
    database = Database(db)
    database.initialize()
    ev = EvolutionEventLog(database)
    seed_wave1(database)
    svc = CompanyInstantiationService(database, ev)
    svc.instantiate("ccp_ai_software_company", DEFAULT_TENANT)
    svc.instantiate("ccp_ai_content_company", DEFAULT_TENANT)
    conn = sqlite3.connect(db)
    did = conn.execute(
        "select id from department_instances where department_type='tech.rd' limit 1"
    ).fetchone()[0]
    conn.close()

    rt = RdWorkflowRuntime(database, ev)  # 无 model_fn → scaffold
    run = rt.run(did, "wl_ai_rd_software_dev_sop", "研发部闭环验证任务")
    assert run["status"] == "completed"
    assert run["steps"] == 6
    assert run["workflow_run_id"].startswith("wfr-")
    assert run["workflow_instance_id"].startswith("wfi-rd-")
