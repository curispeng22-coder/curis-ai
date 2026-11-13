#!/usr/bin/env python
"""Wave-1 一键种子 + 实例化 + 验证（Curis 自用 v1 · 第一波）。

执行顺序（主理人裁定）：
    initialize()  → 建表 + 既有官方资产就位
    seed_wave1()  → T04/T05/T06 资产 seed（含 T08 tenant 归一）
    instantiate()  → T09 两部门实例化（tech.rd / content.growth）
    RdWorkflowRuntime.run() → T10 研发部基础闭环验证
    ContentPublishPackage   → T07 发布包导出验证

所有步骤幂等，可重复运行。用法：
    cd backend && python seed_wave1.py [curis.sqlite 路径]
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# 让 backend 目录可导入（app 为包，内部用相对导入，
# 必须以 ``app.xxx`` 形式导入，不能直接 ``database``）。
_BACKEND_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_BACKEND_DIR))

from app.database import Database  # noqa: E402
from app.evolution_event_log import EvolutionEventLog  # noqa: E402
from app.company_instantiation import CompanyInstantiationService  # noqa: E402
from app.wave1_seed import seed_wave1  # noqa: E402
from app.rd_workflow_runtime import RdWorkflowRuntime  # noqa: E402
from app.content_publish_package import ContentPublishPackage, ContentArtifact  # noqa: E402
from app.tenant_context import DEFAULT_TENANT  # noqa: E402


def main() -> int:
    db_path = sys.argv[1] if len(sys.argv) > 1 else str(
        Path(__file__).resolve().parent.parent / "curis.sqlite"
    )
    print(f"[1/5] initialize() → {db_path}  (tenant={DEFAULT_TENANT})")
    database = Database(db_path)
    database.initialize()

    event_log = EvolutionEventLog(database)
    print("[2/5] seed_wave1()  T04/T05/T06 + T08 tenant 归一")
    summary = seed_wave1(database)
    for key, value in summary.items():
        print(f"      - {key}: {value}")

    # v1 selfuse 模式（CURIS_ENV=local / CURIS_IDENTITY_MODE=selfuse）：
    # 只落官方资产（capability / tool / skill catalog），不实例化部门 / 员工 /
    # 工作流，也不导出发布包 —— 避免把开发期测试 fixture 带进部署态。
    # 显式非 selfuse（如演示 / 端到端验证）才跑完整 Wave-1。
    selfuse = os.getenv("CURIS_ENV") == "local" or os.getenv("CURIS_IDENTITY_MODE") == "selfuse"
    if selfuse:
        print("\n✅ selfuse 模式：仅落官方资产，跳过部门实例化 / 工作流 / 发布包（避免测试 fixture）。")
        return 0

    print("[3/5] instantiate()  T09 两部门实例化")
    svc = CompanyInstantiationService(database, event_log)
    rd = svc.instantiate("ccp_ai_software_company", DEFAULT_TENANT)
    content = svc.instantiate("ccp_ai_content_company", DEFAULT_TENANT)
    print(f"      - 研发部 DepartmentInstance: "
          f"{rd['departments'][0]['id']} "
          f"({rd['departments'][0]['department_type']}) · "
          f"员工 {len(rd['employees'])} · 工作流 {len(rd['workflows'])}")
    print(f"      - 内容部 DepartmentInstance: "
          f"{content['departments'][0]['id']} "
          f"({content['departments'][0]['department_type']}) · "
          f"员工 {len(content['employees'])} · 工作流 {len(content['workflows'])}")
    if rd.get("unresolved_refs") or content.get("unresolved_refs"):
        print(f"      - unresolved_refs(RD): {rd.get('unresolved_refs')}")
        print(f"      - unresolved_refs(Content): {content.get('unresolved_refs')}")

    print("[4/5] RdWorkflowRuntime.run()  T10 研发部基础闭环")
    rt = RdWorkflowRuntime(database, event_log)  # 无 model_fn → scaffold 闭环
    rd_dept_id = rd["departments"][0]["id"]
    run = rt.run(
        rd_dept_id,
        "wl_ai_rd_software_dev_sop",
        "实现 Curis 内容发布包 Markdown 导出能力",
    )
    print(f"      - workflow_run: {run['workflow_run_id']} · "
          f"步骤 {run['steps']} · {run['status']}")

    print("[5/5] ContentPublishPackage.export()  T07 发布包导出")
    package = ContentPublishPackage.create(
        source_workflow="wl_ai_content_content_production_sop",
        brand_voice_ref="skl_ai_content_brand_voice",
        platforms_targeted=["xhs", "douyin"],
        artifacts=[
            ContentArtifact(
                type="copywriting", platform="xhs",
                title="春季护肤：3 个被忽略的误区",
                body="误区一：越贵越有效……\n误区二：只在白天防晒……",
                metadata={"word_count": 320, "tone": "亲切科普"},
            ),
            ContentArtifact(
                type="script", platform="douyin",
                title="30 秒口播脚本",
                body="开头钩子：你还在这样护肤吗？\n正文：三个误区一次讲清……",
                metadata={"duration_sec": 30},
            ),
        ],
    )
    markdown = package.export(str(
        Path(__file__).resolve().parent.parent / "data" / "sample_publish_package.md"
    ))
    print(f"      - package_id: {package.package_id} · v{package.version}")
    print(f"      - artifacts: {len(package.artifacts)} · 平台 {package.platforms_targeted}")
    print(f"      - markdown 已导出（{len(markdown)} 字符）：")
    print("──────────────── publish-package markdown ────────────────")
    print(markdown[:1200])
    print("────────────────────────────────────────────────────────────")

    print("\n✅ Wave-1 第一波完成：seed + 实例化 + 闭环 + 导出 全部跑通。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
