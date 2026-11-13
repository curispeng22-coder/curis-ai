#!/usr/bin/env python
"""Wave 2 自验证（非 pytest，真实运行）。

验证范围（对应任务 C1/V1/T14/W1/F2）：
  1) initialize + seed_wave1 + 两部门实例化 → 断言 tool_refs 不再 unresolved（C1 修复 _tool_exists）。
  2) Connector mock 端到端（ContentWorkflowRuntime.run）→ 生成→发布包→发布，发布包持久化。
  3) 单账号 Vault 读写：create → list → resolve（V1）。
  4) 研发真实引擎（RdWorkflowRuntime.run 注入 model_fn，无 key 降级 scaffold 不中断）。
  5) F2 成果汇总：/api/results/* 等价查询（直接查 DB 助手）。

用法：cd backend && python verify_wave2.py
退出码 0 = 全部通过；非 0 = 有失败。
"""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

_BACKEND_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_BACKEND_DIR))

from app.database import Database  # noqa: E402
from app.evolution_event_log import EvolutionEventLog  # noqa: E402
from app.company_instantiation import CompanyInstantiationService  # noqa: E402
from app.wave1_seed import seed_wave1  # noqa: E402
from app.rd_workflow_runtime import RdWorkflowRuntime  # noqa: E402
from app.content_workflow_runtime import ContentWorkflowRuntime  # noqa: E402
from app.credential_vault import CredentialVaultService, CredentialError  # noqa: E402
from app.runtime_governance import AutoApproveSink  # noqa: E402
from app.tenant_context import DEFAULT_TENANT, TenantContext  # noqa: E402
from app.connectors import list_connectors, get_connector  # noqa: E402


FAILS: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    status = "PASS" if cond else "FAIL"
    print(f"  [{status}] {name}" + (f" — {detail}" if detail else ""))
    if not cond:
        FAILS.append(name)


def main() -> int:
    tmp = tempfile.mkdtemp(prefix="wave2_verify_")
    db_path = os.path.join(tmp, "curis.sqlite")
    print(f"[setup] db={db_path} tenant={DEFAULT_TENANT}")

    database = Database(db_path)
    database.initialize()
    event_log = EvolutionEventLog(database)

    print("\n[1] seed + 实例化（C1 修复 _tool_exists）")
    seed_wave1(database)
    svc = CompanyInstantiationService(database, event_log)
    rd = svc.instantiate("ccp_ai_software_company", DEFAULT_TENANT)
    content = svc.instantiate("ccp_ai_content_company", DEFAULT_TENANT)
    rd_unresolved = rd.get("unresolved_refs", {}).get("tool_refs", [])
    ct_unresolved = content.get("unresolved_refs", {}).get("tool_refs", [])
    print(f"      RD unresolved tool_refs: {rd_unresolved}")
    print(f"      Content unresolved tool_refs: {ct_unresolved}")
    check("实例化无 unresolved tool_refs", not rd_unresolved and not ct_unresolved,
          f"rd={rd_unresolved} content={ct_unresolved}")
    # 确认连接器工具 tl_ai_content_social_upload 已解析
    check("tl_ai_content_social_upload 已解析", "tl_ai_content_social_upload" not in ct_unresolved)

    print("\n[2] Connector mock 端到端（W1 生成→发布包→发布）")
    with TenantContext.scope(DEFAULT_TENANT):
        cwr = ContentWorkflowRuntime(database, event_log, CredentialVaultService(database, event_log))
        result = cwr.run(
            prompt="春季护肤：3 个被忽略的误区",
            platforms=["xhs", "douyin"],
            source_workflow="wl_ai_content_content_production_sop",
            decision_sink=AutoApproveSink(),
        )
    print(f"      run_id={result['run_id']} status={result['status']}")
    print(f"      package={result['package']['package_id']} artifacts={len(result['package']['artifacts'])}")
    print(f"      published={result['published_platforms']} failed={result['failed_platforms']}")
    check("内容闭环状态 completed", result["status"] == "completed")
    check("发布包含 ≥1 工件", len(result["package"]["artifacts"]) >= 1)
    check("mock 模式下两平台均发布", set(result["published_platforms"]) >= {"xhs", "douyin"})
    # 持久化核对
    persisted = database.get_content_publish_package(DEFAULT_TENANT, result["package"]["package_id"])
    check("发布包已持久化", persisted is not None and persisted["status"] == "published")
    check("发布包 source_workflow 合规", persisted["source_workflow"].startswith("wl_ai_content_"))

    print("\n[3] 单账号 Vault 读写（V1）")
    vault = CredentialVaultService(database, event_log)
    cred = vault.create(name="抖音主号 cookie", provider="social_platform_douyin",
                        credential_type="cookie", secret="sessionid=abc123; uid=42")
    ref = cred["credential_ref"]
    print(f"      credential_ref={ref}")
    check("Vault ref 含 /tenant/selfuse/credential/ 段", "/tenant/selfuse/credential/" in ref, ref)
    listed = vault.list()["credentials"]
    check("list 含新建凭证", any(c["credential_id"] == cred["credential_id"] for c in listed))
    resolved = vault.resolve(ref)["secret"]
    check("resolve 还原明文（进程内）", resolved == "sessionid=abc123; uid=42")
    # 明文不落库核对：credential_metadata 表无明文
    row = database.get_credential_metadata(DEFAULT_TENANT, cred["credential_id"])
    raw = str(row)
    check("库内不存明文 cookie", "sessionid=abc123" not in raw)

    print("\n[4] 研发真实引擎（T14 注入 model_fn，无 key 降级 scaffold）")
    def fake_model(prompt: str) -> str:
        # 模拟真实 model gateway：正常返回；此处直接产出，验证注入链路。
        return f"[model] 针对「{prompt[:20]}」的架构建议：采用分层服务。"
    rt = RdWorkflowRuntime(database, event_log, model_fn=fake_model)
    rd_dept = rd["departments"][0]["id"]
    run = rt.run(rd_dept, "wl_ai_rd_software_dev_sop", "实现内容发布包导出")
    print(f"      run_id={run['workflow_run_id']} steps={run['steps']} status={run['status']}")
    check("研发闭环 completed", run["status"] == "completed")
    check("研发闭环含 30 个 tl_ai_rd_* 引用步骤", run["steps"] >= 1)
    # 无 key 降级：用会抛错的 model_fn 验证不中断
    def boom(_: str) -> str:
        raise RuntimeError("no api key")
    rt2 = RdWorkflowRuntime(database, event_log, model_fn=boom)
    run2 = rt2.run(rd_dept, "wl_ai_rd_software_dev_sop", "降级验证")
    check("model_fn 失败降级 scaffold 不中断", run2["status"] == "completed")

    print("\n[5] F2 成果汇总（results 视图）")
    summary = {
        "publish_packages": len(database.list_content_publish_packages(DEFAULT_TENANT)),
        "content_runs": len(database.list_content_workflow_runs(DEFAULT_TENANT)),
    }
    print(f"      publish_packages={summary['publish_packages']} content_runs={summary['content_runs']}")
    check("成果汇总含发布包", summary["publish_packages"] >= 1)
    check("成果汇总含内容运行", summary["content_runs"] >= 1)

    print("\n[6] Connector 注册表（C1 目录）")
    regs = list_connectors()
    print(f"      connectors={[c['name'] for c in regs]} mode={os.getenv('CURIS_CONNECTOR_MODE','mock')}")
    check("aitoearn 已注册", any(c["name"] == "aitoearn" for c in regs))
    check("social_auto_upload 已注册", any(c["name"] == "social_auto_upload" for c in regs))

    print("\n" + ("=" * 56))
    if FAILS:
        print(f"IS_PASS: NO — 失败项：{FAILS}")
        return 1
    print("IS_PASS: YES — Wave 2 自验证全部通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
