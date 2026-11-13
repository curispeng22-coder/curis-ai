"""Workspace Quickstart — 一步到位创建 AI 公司并启动运行的组合 API。

在系统启动时自动 seed 必要的部门类型（tech.rd / content.growth / design.ux）
以及 dt_rd_department / et_devops_engineer 等基础设施模板（若尚未存在）。

支持分步可选参数：
- 指定 company_id → 跳过创建公司直接复用
- 指定 department_id → 跳过创建部门直接复用
- skip_skills → 跳过自动分配所有技能
- skip_tools → 跳过自动分配所有工具
- employee_skills / employee_tools → 自定义技能/工具列表
"""

from __future__ import annotations

import json
import logging
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .database import Database
from .employee_templates import EmployeeTemplateContract

logger = logging.getLogger(__name__)


# ── 请求 / 响应模型 ──────────────────────────────────────────────


class QuickstartIn(BaseModel):
    """快速启动向导的输入。支持分步可选参数。"""
    company_name: str = "我的 AI 公司"
    company_id: str | None = None            # 非 None → 跳过创建公司
    department_name: str = "研发部"
    department_type: str = "tech.rd"
    department_id: str | None = None          # 非 None → 跳过创建部门
    employee_name: str = "AI 工程师 1 号"
    employee_template_id: str | None = "et_devops_engineer"  # None → 纯自定义
    employee_skills: list[str] | None = None  # 自定义技能 skill_template_id 列表
    employee_tools: list[str] | None = None   # 自定义工具名列表
    employee_model_preference: str | None = None  # 模型偏好
    project_name: str = "第一个项目"
    project_description: str = "测试项目"
    skip_skills: bool = False                 # True → 跳过分配所有技能
    skip_tools: bool = False                  # True → 跳过分配所有工具


class QuickstartOut(BaseModel):
    company_id: str
    department_id: str
    employee_id: str
    project_id: str
    status: str = "ok"


# ── 依赖注入占位（由 create_app 在注册路由时注入） ────────────────

_database: Database | None = None
_employee_contract: EmployeeTemplateContract | None = None


def _inject_deps(database: Database, employee_contract: EmployeeTemplateContract) -> None:
    global _database, _employee_contract
    _database = database
    _employee_contract = employee_contract


# ── 启动时 seed ──────────────────────────────────────────────────

def ensure_quickstart_seeds(database: Database) -> None:
    """如果缺失必要的部门类型/模板，在启动时自动 seed。

    幂等：INSERT OR IGNORE 确保重复调用安全。
    """
    _seed_department_types(database)
    _seed_department_template(database)
    _seed_employee_template(database)


def _seed_department_types(database: Database) -> None:
    """Seeds tech.rd, content.growth, design.ux department_types if absent."""
    desired = [
        ("tech.rd", "product", "研发部", "技术研发型部门，覆盖后端/前端/QA/DevOps 等工程角色。"),
        ("content.growth", "product", "内容增长部", "内容增长型部门，覆盖内容生产/运营/数据分析等角色。"),
        ("design.ux", "product", "设计体验部", "设计与用户体验部门，覆盖 UI/UX/品牌设计等角色。"),
    ]
    with database.connect() as connection:
        existing = {
            row["type_key"]
            for row in connection.execute(
                "select type_key from department_types"
            ).fetchall()
        }
        for type_key, category, display_name, description in desired:
            if type_key not in existing:
                connection.execute(
                    "insert or ignore into department_types "
                    "(type_key, category, display_name, description, "
                    "manifest_json, manifest_schema_version, is_system) "
                    "values (?, ?, ?, ?, '{}', '1.0', 1)",
                    (type_key, category, display_name, description),
                )
                logger.info("seeded department_type '%s'", type_key)


def _seed_department_template(database: Database) -> None:
    """Seeds dt_rd_department if absent."""
    with database.connect() as connection:
        row = connection.execute(
            "select id from department_templates where id = ?",
            ("dt_rd_department",),
        ).fetchone()
        if row is None:
            employee_ids = [
                "et_tech_lead", "et_backend_engineer", "et_qa_engineer", "et_devops_engineer",
            ]
            connection.execute(
                "insert or ignore into department_templates "
                "(id, slug, name, department_type, description, default_employee_templates_json, "
                "default_workflow_template_id, default_capability_types_json, version, status, "
                "source, tenant_id, enabled) "
                "values (?, 'rd-department', 'R&D 研发部门', 'software_rnd', "
                "'研发部：技术负责人 + 后端工程师 + QA + DevOps。', "
                "?, 'wt_rd_pipeline', '[\"model\",\"tool\"]', "
                "'1.0.0', 'active', 'official', 'platform', 1)",
                ("dt_rd_department", json.dumps(employee_ids, ensure_ascii=False)),
            )
            logger.info("seeded department_template 'dt_rd_department'")


def _seed_employee_template(database: Database) -> None:
    """Seeds et_devops_engineer if absent."""
    with database.connect() as connection:
        row = connection.execute(
            "select id from employee_templates where id = ?",
            ("et_devops_engineer",),
        ).fetchone()
        if row is None:
            connection.execute(
                "insert or ignore into employee_templates "
                "(id, slug, name, role, responsibility, department_type, "
                "default_instructions, default_capability_types_json, default_model_policy_json, "
                "default_workflow_step_types_json, guardrails_json, persona_ref, "
                "default_skill, default_tool, "
                "version, status, source, tenant_id, enabled) "
                "values (?, ?, ?, ?, ?, 'software_rnd', ?, '[\"model\",\"tool\"]', '{}', '[]', '[]', "
                "?, ?, ?, "
                "'1.0.0', 'active', 'official', 'platform', 1)",
                (
                    "et_devops_engineer", "devops-engineer", "DevOps Engineer", "devops_engineer",
                    "维护 CI/CD 管道、部署环境和基础设施上下线。",
                    "et_devops_engineer：确保 CI 门禁不退化、部署环境凭据不泄露；\n"
                    "对外汇报一律遵守《CEO 汇报标准》：先结论、再原因、后建议，用中文白话，"
                    "不堆技术术语与 Contract 引用，风险直说，需决策时给明确下一步。",
                    "pt_direct_executor", "skl_ai_rd_cicd_pipeline", "tl_ai_rd_ci_runner",
                ),
            )
            logger.info("seeded employee_template 'et_devops_engineer'")


# ── API Router ───────────────────────────────────────────────────

router = APIRouter()


@router.post("/api/workspace/quickstart")
def workspace_quickstart(payload: QuickstartIn) -> QuickstartOut:
    """组合创建 API：一步创建 Company → Department → Project → Employee。

    支持分步可选参数：
    - company_id：跳过创建公司直接复用已有公司
    - department_id：跳过创建部门直接复用已有部门
    - employee_skills / employee_tools：自定义技能/工具列表
    - skip_skills / skip_tools：跳过自动分配

    内部顺序：
    1. Company（如果 company_id 为空则新建）
    2. Department（如果 department_id 为空则新建）
    3. Project（始终新建，挂到 department_id）
    4. Employee（如果 employee_template_id 非空则按模板创建）
    5. 分配 skills / tools（按自定义列表或全部，受 skip 控制）
    """
    db = _database
    if db is None:
        raise HTTPException(status_code=500, detail="database not initialized")
    emp = _employee_contract
    if emp is None:
        raise HTTPException(status_code=500, detail="employee contract not initialized")

    from .company_project_runtime import CompanyProjectRuntime

    try:
        company_runtime = CompanyProjectRuntime(db)

        # ── 1. Company ──
        if payload.company_id:
            # 验证公司存在
            try:
                company = company_runtime.get_company(payload.company_id)
            except KeyError as error:
                raise HTTPException(status_code=404, detail="指定公司不存在") from error
            company_id = company["company_id"]
        else:
            companies = company_runtime.list_companies()["companies"]
            if companies:
                company = companies[0]
                company_id = company["company_id"]
            else:
                company = company_runtime.create_company(name=payload.company_name.strip())
                company_id = company["company_id"]

        # ── 2. Department ──
        if payload.department_id:
            # 验证部门存在
            department = emp.get_department_instance(payload.department_id)
            if department is None:
                raise HTTPException(status_code=404, detail="指定部门不存在")
            department_id = department["id"]
        else:
            dept = emp.create_department_instance(
                template_id="dt_rd_department",
                name=payload.department_name.strip() or "研发部",
                company_id=company_id,
            )
            department_id = dept["id"]

        # ── 3. Project（组织结构：公司→部门→项目→员工）──
        project = company_runtime.create_project(
            company_id=company_id,
            name=payload.project_name.strip(),
            goal=payload.project_description.strip() or "快速启动项目",
            description=payload.project_description.strip(),
            department_id=department_id,
        )
        project_id = project["project_id"]

        # ── 4. Employee ──
        employee_template_id = payload.employee_template_id or "et_devops_engineer"
        employee = emp.create_employee_instance(
            department_id=department_id,
            template_id=employee_template_id,
            name=payload.employee_name.strip(),
            company_id=company_id,
        )
        employee_id = employee["id"]

        # ── 5. Assign skills ──
        if not payload.skip_skills:
            if payload.employee_skills is not None:
                _assign_selected_skills(db, emp, employee_id, payload.employee_skills)
                logger.info(
                    "assigned %d selected skills to employee %s",
                    len(payload.employee_skills),
                    employee_id,
                )
            else:
                _assign_all_skills(db, emp, employee_id)

        # ── 6. Assign tools ──
        if not payload.skip_tools:
            if payload.employee_tools is not None:
                _assign_selected_tools(emp, employee_id, payload.employee_tools)
                logger.info(
                    "assigned %d selected tools to employee %s",
                    len(payload.employee_tools),
                    employee_id,
                )
            else:
                _assign_all_tools(emp, employee_id)

        return QuickstartOut(
            company_id=company_id,
            department_id=department_id,
            employee_id=employee_id,
            project_id=project_id,
            status="ok",
        )
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    except KeyError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


def _assign_all_skills(
    db: Database,
    emp: EmployeeTemplateContract,
    employee_id: str,
) -> None:
    """为员工绑定所有可用的官方 skill_templates。"""
    from .skill_runtime import SkillRuntime

    skill_runtime = SkillRuntime(db)

    # 获取所有可用的技能模板
    skill_templates = skill_runtime.list_templates()["skills"]
    if not skill_templates:
        logger.warning("no skill templates available to assign to employee")
        return

    bindings = [
        {
            "skill_template_id": sk["skill_template_id"],
            "capability_binding_ids": [],
            "priority": 100,
            "enabled": True,
        }
        for sk in skill_templates
    ]
    skill_runtime.set_employee_bindings(employee_id, bindings)
    logger.info(
        "assigned %d skills to employee %s", len(bindings), employee_id
    )


def _assign_selected_skills(
    db: Database,
    emp: EmployeeTemplateContract,
    employee_id: str,
    selected_skill_ids: list[str],
) -> None:
    """为员工绑定指定的 skill_templates。"""
    from .skill_runtime import SkillRuntime

    skill_runtime = SkillRuntime(db)

    bindings = [
        {
            "skill_template_id": skill_id,
            "capability_binding_ids": [],
            "priority": 100,
            "enabled": True,
        }
        for skill_id in selected_skill_ids
    ]
    if bindings:
        skill_runtime.set_employee_bindings(employee_id, bindings)
    else:
        logger.info("no selected skills to assign to employee %s", employee_id)


def _assign_all_tools(emp: EmployeeTemplateContract, employee_id: str) -> None:
    """为员工绑定所有可用的 tools。

    仅使用 ``tools`` 运行时表中的工具名（它们是经过 validation 认证的 official 能力）。
    ``tool_templates`` 表中的 tl_* ID 暂未注册为 official capability，跳过以避免
    ``_normalize_binding`` 的 "official capability is not available" 校验失败。
    """
    from .tool_registry import ToolRegistry

    registry = ToolRegistry(emp.database)
    registered_tools = registry.list()
    if not registered_tools:
        logger.warning("no tools available in tools table to assign to employee")
        return

    all_tool_ids = {t["name"] for t in registered_tools}

    # 追加 list_catalog_capabilities 中 type=tool 的条目
    with emp.database.connect() as connection:
        cap_rows = connection.execute(
            "select model_key from official_models where type = 'tool' and status = 'active'"
        ).fetchall()
    for row in cap_rows:
        all_tool_ids.add(row["model_key"])

    bindings = [
        {
            "capability_source": "official",
            "capability_id": tool_id,
            "priority": 100,
            "enabled": True,
        }
        for tool_id in sorted(all_tool_ids)
    ]
    if not bindings:
        logger.warning("no valid tool bindings could be built for employee %s", employee_id)
        return
    emp.set_employee_tool_bindings(employee_id, bindings)
    logger.info(
        "assigned %d tools to employee %s", len(bindings), employee_id
    )


def _assign_selected_tools(
    emp: EmployeeTemplateContract,
    employee_id: str,
    selected_tool_ids: list[str],
) -> None:
    """为员工绑定指定的 tools。"""
    if not selected_tool_ids:
        logger.info("no selected tools to assign to employee %s", employee_id)
        return

    bindings = [
        {
            "capability_source": "official",
            "capability_id": tool_id,
            "priority": 100,
            "enabled": True,
        }
        for tool_id in selected_tool_ids
    ]
    emp.set_employee_tool_bindings(employee_id, bindings)
    logger.info(
        "assigned %d selected tools to employee %s", len(bindings), employee_id
    )
