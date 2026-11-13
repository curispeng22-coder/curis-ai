"""Shared constants and validation for the New API gateway / official model catalog.

ADR-0028 Phase-2 (issue 064/065). Admin-only metadata definitions:
  * no secrets are ever stored (no api_key / token columns anywhere);
  * ``credential_ref`` is validated as an opaque ``scheme:reference`` string
    only -- Admin never parses or resolves it, and never makes outbound calls;
  * the gateway type / status / auth_type enums are the only allowed shapes.

This module is dependency-free (standard library only).

Phase-1 Asset Factory Consolidation (Gate C/D/E/F): the module is also the
**single source of truth for template-id prefixes, status enums, pack/company
type enums and the Widget Catalog domain taxonomy**. Any prefix/enum check in
the Admin authoring services (Gate D), the catalog fold service (Gate D read)
and the Workspace runtime (Gate E/F) MUST read from the constants here -- no
scattered regex literals anywhere (admin-workspace-template-boundary 铁律).
"""
from __future__ import annotations

import re
from typing import List

# Gateway types（Step 5：单供应商 → N 供应商可注册）。
#
# 边界说明（重要）：这里枚举的是**协议方言**，不是品牌清单。ModelGatewayAdapter
# 只会说 OpenAI 兼容的 ``POST {base_url}/v1/chat/completions`` + ``Bearer`` 认证；
# 因此只允许登记「确实按该协议对外暴露」的网关类型。Anthropic / Gemini 原生协议
# 形状不同，未实现前**不得**加入本表（加了就是撒谎）。
#
# ``newapi`` 保持首位以兼容既有种子数据与 official_models.gateway_ref 缺省值。
GATEWAY_TYPE: List[str] = [
    "newapi",             # New API 聚合网关（R-01，历史缺省）
    "oneapi",             # One API 聚合网关
    "openai",             # OpenAI 官方
    "openai_compatible",  # 通用 OpenAI 兼容端点（自建/未列举厂商）
    "openrouter",         # OpenRouter 聚合
    "deepseek",           # DeepSeek 开放平台
    "moonshot",           # Moonshot 开放平台
    "ollama",             # Ollama 本地（/v1 兼容层）
    "vllm",               # vLLM 自托管（OpenAI 兼容 server）
]

# Model auth_type shapes (placeholder only; no key is persisted).
MODEL_AUTH_TYPE: List[str] = ["none", "oauth", "apikey"]

# Gateway lifecycle status (R-02 / R-05): active <-> inactive.
GATEWAY_STATUS: List[str] = ["active", "inactive"]

# Official model lifecycle status (R-05): active <-> inactive.
MODEL_STATUS: List[str] = ["active", "inactive"]

# Unified capability types: a single official catalog carries model / agent /
# tool / connector / skill / mcp / api / cli / webhook / workflow entries, distinguished
# by the ``type`` column on official_models.
#
# 扩展（Curis 后端核心 P0）：在原 ["model","tool","connector"]（ADR-0028 统一目录）
# 基础上，新增 skill / mcp / api / cli / webhook / workflow 共 6 类，以覆盖能力层
# 全部可替换能力（Agent/模型/Skill/Tool/MCP/CLI/API/Workflow）；具体产品
# （Codex/WorkBuddy 等）不写死，仅作为 catalog 中某一 type 下的条目。
# 注：保留 legacy ``connector`` 以兼容既有统一目录端点（/api/catalog/connectors 等）。
CAPABILITY_TYPE: List[str] = [
    "model",
    "agent",
    "tool",
    "connector",
    "skill",
    "mcp",
    "api",
    "cli",
    "webhook",
    "workflow",
]

# 能力层「运行态/降级链」元数据键（runtime_meta_json 列内使用，见 capability_catalog）。
# 仅为约定说明，不强制；resolver 只读取其中 known 字段。
RUNTIME_META_KEYS: List[str] = [
    "cost_per_unit",     # 单位成本（如每千 token / 每次调用）
    "io_schema",        # {"input": [...], "output": [...]}
    "permissions",      # 所需权限列表，如 ["repo.write","network.egress"]
    "credentials_ref",  # 凭证引用（scheme:reference，如 env:OPENAI_API_KEY），绝不落明文
    "backup_chain",     # 降级链：能力 key 有序列表（首选在前）
    "live_status",      # available | unavailable | unknown（resolver 探活刷新）
]

# credential_ref scheme whitelist (G2 decision (b)): external secret-store
# reference only. The DB NEVER holds the secret value itself.
_CREDENTIAL_REF_PATTERN = re.compile(r"^(env|kms|vault):.+$")

# ── Phase-1 Asset Factory Consolidation (Gate C/D/E/F) ──
# Template-id prefix taxonomy. 9 类目录前缀（Gate C 目录折叠的权威正则来源）；
# ``ccp_*`` 不在此列（Company Package 是聚合包，走独立商业目录，变体 C）。
TEMPLATE_ID_PREFIXES: List[str] = [
    "ct_",   # CompanyTemplate 类型容器
    "dt_",   # DepartmentTemplate 类型容器
    "et_",   # EmployeeTemplate 类型容器
    "wt_",   # WorkflowTemplate 类型容器（Variant A）
    "st_",   # SkillTemplate 类型容器（legacy）
    "tt_",   # ToolTemplate 类型容器（legacy）
    "pt_",   # PersonaTemplate 内容实例（Variant A，Gate E）
    "wl_",   # Workflow 内容实例（Variant B，折叠进 catalog）
    "dtpl_", # DashboardTemplate 内容实例（Variant A，第 8+ 类目录项）
]

# Company Package 前缀（变体 C，出目录）。仅用于 ``company_packages`` 表主键。
COMPANY_PACKAGE_PREFIX: str = "ccp_"

# 模板类生命周期状态（TemplateBase.status）。
TEMPLATE_STATUS: List[str] = ["draft", "active", "disabled", "archived"]

# Company Package 生命周期状态（比模板类少 archived，见 company-package-contract §2）。
COMPANY_PACKAGE_STATUS: List[str] = ["draft", "active", "disabled"]

# Pack 枚举（company_packages.pack）：对齐 skl_/tl_/wl_ 包命名。
PACK_ENUM: List[str] = ["ai_rd", "ai_content", "ai_commercial"]

# Company Type 枚举（dashboard_templates.company_type / company_templates.company_type）。
COMPANY_TYPE_ENUM: List[str] = [
    "ai_rd",
    "ai_content",
    "ai_content_ops",
    "ai_commercial",
    "generic",
]

# Persona 原型（archetype）枚举（employee-persona-system-plan §2.5）。
ARCHETYPE_ENUM: List[str] = [
    "supportive_coach",
    "direct_executor",
    "analytical_advisor",
    "creative_explorer",
    "balanced_facilitator",
    "risk_aware_guardian",
]

# Widget Catalog 域（dashboard_widget_catalog.domain）：单一真相源分桶。
WIDGET_DOMAINS: List[str] = [
    "company",
    "department",
    "project",
    "employee",
    "cost",
    "value",
    "capability",
    "knowledge",
]

# 内容实例来源归因（两层 source 概念之 metadata.source_attribution，仅 Skill/Tool/
# Workflow 内容有；6 值生态，来自各 SOP 参考框架）。
SOURCE_ATTRIBUTION: List[str] = [
    "MetaGPT SOP",
    "ChatDev workflow",
    "CrewAI example",
    "AutoGen pattern",
    "industry SOP",
    "Curis internal",
]

# 目录输出层 source（TemplateCatalogEntry.source）：Admin 写权归属，收窄为二值
# （见 admin-workspace-template-boundary 铁律：谁拥有写权）。
CATALOG_ENTRY_SOURCE: List[str] = ["official", "marketplace"]

# 弃用 Widget 别名 → 规范 widget_id 映射（Gate C §2.2 去重单一真相源）。
# 名称层仅保留规范 id；作者若提交旧别名，由 normalize_widget_id 规范化为规范 id。
DEPRECATED_WIDGET_ALIASES: dict[str, str] = {
    "token_cost": "ai_cost",   # 与运行时 ai_cost / token_usage 同域，非账单
    "tech_risk": "project_risk",  # 同域；如需"技术风险"细分，作为 project_risk 的 data_class='tech'
}

# SemVer 正则（统一 ^\d+\.\d+\.\d+$），由 Admin 控制演进。
_SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")

# 组合型 template_id 正则（前缀 + 稳定后缀）。Gate D 校验统一从此构造。
_TEMPLATE_ID_PATTERN = re.compile(
    r"^(ct_|dt_|et_|wt_|st_|tt_|pt_|wl_|dtpl_)[a-z0-9_-]+$"
)

# Company Package id 正则（变体 C，出目录）。
_COMPANY_PACKAGE_ID_PATTERN = re.compile(r"^ccp_[a-z0-9_-]+$")


def is_valid_credential_ref(value: str) -> bool:
    """Validate a ``credential_ref`` string.

    Empty string is allowed (no reference configured). Otherwise the format MUST
    be ``scheme:reference`` where ``scheme in {env, kms, vault}``. The reference
    is opaque; Admin never parses or resolves it and never makes outbound calls.
    """
    if value is None or value == "":
        return True
    return bool(_CREDENTIAL_REF_PATTERN.match(value))


def is_valid_gateway_type(value: str) -> bool:
    """Return True if ``value`` is an allowed gateway type."""
    return value in GATEWAY_TYPE


def is_valid_gateway_status(value: str) -> bool:
    """Return True if ``value`` is an allowed gateway status."""
    return value in GATEWAY_STATUS


def is_valid_model_status(value: str) -> bool:
    """Return True if ``value`` is an allowed official-model status."""
    return value in MODEL_STATUS


def is_valid_capability_type(value: str) -> bool:
    """Return True if ``value`` is an allowed unified capability type."""
    return value in CAPABILITY_TYPE


def is_valid_auth_type(value: str) -> bool:
    """Return True if ``value`` is an allowed auth_type shape."""
    return value in MODEL_AUTH_TYPE


# ── Phase-1 Asset Factory Consolidation 校验助手 ──
def is_valid_template_id(value: str) -> bool:
    """Return True if ``value`` matches one of the 9 catalog template prefixes."""
    return bool(_TEMPLATE_ID_PATTERN.match(value or ""))


def template_id_prefix(value: str) -> str | None:
    """Return the matched prefix (e.g. ``pt_``) or ``None`` if not a catalog id."""
    if not value:
        return None
    for prefix in TEMPLATE_ID_PREFIXES:
        if value.startswith(prefix):
            return prefix
    return None


def is_valid_company_package_id(value: str) -> bool:
    """Return True if ``value`` matches the ``ccp_`` company package prefix."""
    return bool(_COMPANY_PACKAGE_ID_PATTERN.match(value or ""))


def is_valid_template_status(value: str) -> bool:
    """Return True if ``value`` is an allowed template lifecycle status."""
    return value in TEMPLATE_STATUS


def is_valid_company_package_status(value: str) -> bool:
    """Return True if ``value`` is an allowed company-package status."""
    return value in COMPANY_PACKAGE_STATUS


def is_valid_pack(value: str) -> bool:
    """Return True if ``value`` is an allowed pack enum."""
    return value in PACK_ENUM


def is_valid_company_type(value: str) -> bool:
    """Return True if ``value`` is an allowed company-type enum."""
    return value in COMPANY_TYPE_ENUM


def is_valid_archetype(value: str) -> bool:
    """Return True if ``value`` is an allowed persona archetype."""
    return value in ARCHETYPE_ENUM


def is_valid_widget_domain(value: str) -> bool:
    """Return True if ``value`` is an allowed Widget Catalog domain."""
    return value in WIDGET_DOMAINS


def is_valid_source_attribution(value: str) -> bool:
    """Return True if ``value`` is an allowed content source-attribution enum."""
    return value in SOURCE_ATTRIBUTION


def is_valid_catalog_entry_source(value: str) -> bool:
    """Return True if ``value`` is an allowed catalog-entry source (official/marketplace)."""
    return value in CATALOG_ENTRY_SOURCE


# ── 双轨能力供给（商业化预留）：写权归属 / 可见性 / 来源归因 ──
# owner_type 区分「谁拥有写权」：官方供给（official）vs 租户自助（tenant）vs 系统
# 内置（system）。visibility 区分消费可见范围：private=仅本租户 / tenant=租户内共享
# / public=全租户（仅官方）。source 归因来源：official_curated（官方策划）/ user_registered
#（租户自助登记）/ marketplace（未来市场）。既有 official_models 行的 source 值 'official'
# 为历史别名，按 official_curated 处理；owner_type 为权威判别字段。
CAPABILITY_OWNER_TYPE: List[str] = ["official", "tenant", "system"]
CAPABILITY_VISIBILITY: List[str] = ["private", "tenant", "public"]
CAPABILITY_SOURCE: List[str] = ["official_curated", "user_registered", "marketplace", "official"]


def is_valid_capability_owner_type(value: str) -> bool:
    """Return True if ``value`` is an allowed capability owner_type."""
    return value in CAPABILITY_OWNER_TYPE


def is_valid_capability_visibility(value: str) -> bool:
    """Return True if ``value`` is an allowed capability visibility."""
    return value in CAPABILITY_VISIBILITY


def is_valid_capability_source(value: str) -> bool:
    """Return True if ``value`` is an allowed capability source attribution."""
    return value in CAPABILITY_SOURCE


def is_valid_semver(value: str) -> bool:
    """Return True if ``value`` is a valid SemVer string."""
    return bool(_SEMVER_PATTERN.match(value or ""))


def normalize_widget_id(widget_id: str) -> str:
    """Normalize a (possibly deprecated-alias) widget id to its canonical form.

    Gate C §2.2 去重：若作者提交 ``token_cost`` / ``tech_risk`` 等弃用别名，
    规范化为 ``ai_cost`` / ``project_risk``（目录仅存规范 id，单一真相源）。
    非别名原样返回。
    """
    if not widget_id:
        return widget_id
    return DEPRECATED_WIDGET_ALIASES.get(widget_id, widget_id)


# ---------------------------------------------------------------------------
# 能力副作用面（effect_class）——EvoFlow 复用 A1（只标注，不改变执行语义）
# ---------------------------------------------------------------------------
# read / retrieve / write / exec 四档；planning 相位 deny-by-default（未标注一律拒绝，
# 见 docs/plan/evoflow-reuse-repo-mapping.md §3 与 docs/plan/evoflow-verified-reuse-plan.md A1）。
EFFECT_CLASS_READ = "read"
EFFECT_CLASS_RETRIEVE = "retrieve"
EFFECT_CLASS_WRITE = "write"
EFFECT_CLASS_EXEC = "exec"

# 按能力类型默认（catalog 投影派生，不落库）。
EFFECT_CLASS_BY_TYPE: dict[str, str] = {
    "model": EFFECT_CLASS_READ,      # 纯计算，无副作用
    "agent": EFFECT_CLASS_EXEC,      # 内部可调任意能力，副作用不可知
    "skill": EFFECT_CLASS_READ,      # 提示模板/方法论，无执行
    "workflow": EFFECT_CLASS_EXEC,   # 编排执行，有副作用
    "connector": EFFECT_CLASS_EXEC,  # 远程平台副作用
    "cli": EFFECT_CLASS_EXEC,        # 命令执行（沙箱内）
    "api": EFFECT_CLASS_WRITE,       # 远程调用，默认副作用
    "webhook": EFFECT_CLASS_WRITE,   # 出站推送
    "mcp": EFFECT_CLASS_EXEC,        # 未知权限面，deny-by-default
}

# 工具按名称启发式细分（只读/检索前缀后缀 → read/retrieve；其余默认 exec 安全侧）。
_READ_TOOL_MARKERS = ("reader", "search", "docs", "fetch", "list", "read")
_WRITE_TOOL_MARKERS = ("writer", "git", "upload", "publish", "write", "post")


def effect_class_for_tool(tool_name: str) -> str:
    """按工具名派生 effect_class；无命中回退 exec（planning 拒绝的安全侧）。"""
    name = (tool_name or "").lower()
    if any(marker in name for marker in _READ_TOOL_MARKERS):
        return EFFECT_CLASS_RETRIEVE if "search" in name or "docs" in name else EFFECT_CLASS_READ
    if any(marker in name for marker in _WRITE_TOOL_MARKERS):
        return EFFECT_CLASS_WRITE
    return EFFECT_CLASS_EXEC


def effect_class_for_capability(capability_type: str, name: str = "") -> str:
    """统一派生入口：tool 走名称启发式，其余按类型默认。"""
    if capability_type == "tool":
        return effect_class_for_tool(name)
    return EFFECT_CLASS_BY_TYPE.get(capability_type, EFFECT_CLASS_EXEC)
