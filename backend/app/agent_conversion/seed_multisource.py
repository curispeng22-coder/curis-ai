"""多源扩展（CrewAI + MCP）权威种子清单 + 行构建器（纯函数，不触 DB）。

本模块持有 **CrewAI** 与 **MCP Registry** 两路受控候选资产的权威快照
（``CREWAI_MANIFEST`` / ``CREWAI_TOOLS`` / ``MCP_MANIFEST``），即把离线
``sources/crewai/*.yaml`` 与 ``sources/mcp/*.json`` 经 adapter 解析 + 人工评审后
落定的快照。``database.py`` 的 opt-in seed 函数消费 ``build_multisource_rows()``
做 ``INSERT OR IGNORE`` / ``UPDATE``；各 Adapter 则证明其可由 ``sources/`` 重新
解析生成等价 spec（见 T9 解析测试）。

设计约束（全部 draft 态、可回滚）：
- 全链路 ``status='draft'``（真实 CHECK 不含 ``'candidate'``，见设计 §0⑤）。
- ``source='official'``、``tenant_id='platform'``、主键幂等 + ``INSERT OR IGNORE``。
- 不接入凭证、不建 marketplace、不 instantiation（ADR-0017 仍锁）。
- CrewAI 复用既有 ``business.general``（**不新增 department_types**）；
  MCP 为纯工具源，仅写 ``tl_mcp_*``，不写 et_*/pt_*/skl_*/wt_*/dt_*。
- 命名空间：CrewAI ``crew_``（``official.employee.crew_<slug>`` /
  ``pt_crew_<slug>`` / ``tl_crew_<name>`` / ``wt_crew_<slug>``）；
  MCP ``mcp_``（``tl_mcp_<name>``）。二者前缀与 pilot_b_ / 基线 6 et / 115 工具 /
  55 技能**全部零冲突**（前缀正交）。

许可闸门（设计 §7.5）：copyleft（GPL/AGPL/CC-BY-SA）拒绝 harvest、无 LICENSE 标记
``skip``；本模块样本统一 ``license_spdx='MIT'``、``commercial_use=True``、
``copyleft=False``、``attribution_required=True``。

安全（设计 §7.4）：所有文本字段在 ``build_multisource_rows()`` 落库前经
``_scrub_text`` 剥离凭证赋值，三段扫描零漏报（``security_scan.scan_all``）。
"""

from __future__ import annotations

import json
import re
from typing import Any

from .sanitize import strip_invisible
from .security_scan import CREDENTIAL_PAT, scan_all
from .seed import SeedMapper  # §7.1 复用 SeedMapper.map_* 纯函数

# ── 许可合规闸门（设计 §7.5）──────────────────────────────────────────────
# copyleft / 强署名共享（CC-BY-SA）一律拒绝 harvest（标记 skip）。
COPYLEFT_SPDX: frozenset[str] = frozenset(
    {
        "GPL-1.0",
        "GPL-2.0",
        "GPL-3.0",
        "AGPL-1.0",
        "AGPL-3.0",
        "LGPL-2.1",
        "LGPL-3.0",
        "CC-BY-SA-1.0",
        "CC-BY-SA-2.0",
        "CC-BY-SA-2.5",
        "CC-BY-SA-3.0",
        "CC-BY-SA-4.0",
    }
)

# 已知宽松许可（允许 harvest，落 draft 候选）。
PERMISSIVE_SPDX: frozenset[str] = frozenset(
    {
        "MIT",
        "MIT-0",
        "Apache-2.0",
        "BSD-2-Clause",
        "BSD-3-Clause",
        "ISC",
        "0BSD",
        "Unlicense",
    }
)


def classify_license(spdx: str | None) -> tuple[bool, str, str]:
    """许可合规闸门（设计 §7.5）。

    Returns:
        (allowed, disposition, reason)
        - copyleft → (False, "skip", "copyleft")：拒绝 harvest。
        - 空 / None → (False, "skip", "no_license")：无 LICENSE 源标记 skip。
        - 宽松 / 未知 → (True, "create", "ok" / "unknown_permissive_assumed")。
    """
    if not spdx or not str(spdx).strip():
        return (False, "skip", "no_license")
    spdx_u = str(spdx).strip()
    if spdx_u in COPYLEFT_SPDX:
        return (False, "skip", "copyleft")
    if spdx_u in PERMISSIVE_SPDX or not spdx_u.startswith(("GPL", "AGPL", "CC-BY-SA")):
        # 已知宽松，或未知但非明确 copyleft 前缀 → 默认允许（create），未知显式标注。
        reason = "ok" if spdx_u in PERMISSIVE_SPDX else "unknown_permissive_assumed"
        return (True, "create", reason)
    return (True, "create", "unknown_permissive_assumed")


# ── 安全：凭证剥离（设计 §7.4）────────────────────────────────────────────
def _scrub_text(text: str) -> str:
    """剥离不可见字符 + 凭证赋值值（key 保留，值置 [REDACTED]），绝不留凭证明文。"""
    if not text:
        return ""
    text = strip_invisible(text)
    text = CREDENTIAL_PAT.sub(
        lambda m: m.group(0).split("=")[0].split(":")[0].strip() + "=[REDACTED]",
        text,
    )
    return text


def _scrub_value(value: Any) -> Any:
    """递归清洗字符串 / 列表 / 字典中的凭证赋值。"""
    if isinstance(value, str):
        return _scrub_text(value)
    if isinstance(value, list):
        return [_scrub_value(v) for v in value]
    if isinstance(value, dict):
        return {k: _scrub_value(v) for k, v in value.items()}
    return value


def _kebab(asset_slug: str) -> str:
    return asset_slug.replace("_", "-")


# ── §T1/T4/T5/T7：CrewAI 候选清单（et_*/pt_*/wt_*/tl_crew_*）─────────────
# asset_slug = crew_<local>；据此：
#   pt_*   = pt_{asset_slug}          = pt_crew_<local>
#   et_*   = official.employee.{asset_slug} = official.employee.crew_<local>
#   wt_*   = wt_{asset_slug}           = wt_crew_<local>
# department_type 统一 business.general（复用既有，不新建 type）。
# 所有文本字段经 _scrub_value 落库前清洗（凭证零持久化）。
CREWAI_MANIFEST: list[dict] = _scrub_value(
    [
        {
            "asset_slug": "crew_research_analyst",
            "slug": "crew-research-analyst",
            "department_type": "business.general",
            "name": "Senior Research Analyst",
            "role": "research_analyst",
            "responsibility": "持续搜集并综合市场与竞品情报，输出可决策的研究简报。",
            "default_instructions": (
                "你是 Curis 平台（多源扩展·CrewAI）的官方员工候选（draft 态，未激活）。\n"
                "背景：你是一名资深研究分析师，擅长从公开渠道检索并交叉验证信息，"
                "将噪声收敛为结构化洞察。\n"
                "职责：围绕目标主题做检索、聚类与综合，输出带来源与不确定性的研究简报；"
                "所有结论必须附可核验来源，不编造未被资料支撑的判断，明确标注不确定性。"
            ),
            "guardrails": [
                "趋势与结论必须附可核验来源。",
                "不编造未被资料支撑的判断。",
                "明确标注不确定性与样本范围。",
            ],
            "persona_archetype": "analytical_advisor",
            "persona_traits": ["严谨", "好奇", "证据优先"],
            "persona_comm": {"tone": "neutral", "format": "data_driven"},
            "persona_report": {"frequency": "per-analysis"},
            "persona_collab": {"style": "deliberative"},
            "persona_decision": "evidence_based",
            "emoji": "",
            "color": "",
            "persona_identity": "研究分析师，把公开信号收敛为可决策的研究简报。",
            "capability_types": ["model", "tool"],
            "default_skill": "",
            "default_tool": "tl_crew_web_search_tool",
            "star_rating": 3,
            "attribution": (
                "Converted from public MIT CrewAI crew example (market research crew). "
                "Original author retains copyright; see source_attribution."
            ),
            "license_spdx": "MIT",
            "commercial_use": True,
            "copyleft": False,
            "attribution_required": True,
            "workflow": [
                {
                    "name": "采集信号",
                    "instruction_excerpt": "按主题检索公开资料并去重。",
                    "expected_output": "去重后的信号条目池。",
                },
                {
                    "name": "综合简报",
                    "instruction_excerpt": "聚类并生成带来源与不确定性的研究简报。",
                    "expected_output": "结构化研究简报。",
                },
            ],
        },
        {
            "asset_slug": "crew_support_specialist",
            "slug": "crew-support-specialist",
            "department_type": "business.general",
            "name": "Customer Support Specialist",
            "role": "support_specialist",
            "responsibility": "在多渠道分诊并高质量应答客户问题，沉淀可复用知识。",
            "default_instructions": (
                "你是 Curis 平台（多源扩展·CrewAI）的官方员工候选（draft 态，未激活）。\n"
                "背景：你是一名客户支持专家，熟悉分诊与知识沉淀流程。\n"
                "职责：接收并分诊工单，基于知识库给出高质量应答；不承诺超出产品能力的方案，"
                "涉及隐私或支付的工单按权限与合规处理，重复问题沉淀为知识条目。"
            ),
            "guardrails": [
                "不承诺超出产品能力的解决方案。",
                "涉及隐私/支付的工单按权限与合规处理。",
                "同一问题反复出现须沉淀为知识条目。",
            ],
            "persona_archetype": "supportive_coach",
            "persona_traits": ["亲和", "耐心", "解决导向"],
            "persona_comm": {"tone": "encouraging", "format": "bullet_points"},
            "persona_report": {"frequency": "per-ticket"},
            "persona_collab": {"style": "collaborative"},
            "persona_decision": "consultative",
            "emoji": "",
            "color": "",
            "persona_identity": "客户支持专家，把每次对话变成信任积累。",
            "capability_types": ["model", "tool"],
            "default_skill": "",
            "default_tool": "tl_crew_ticket_reader_tool",
            "star_rating": 4,
            "attribution": (
                "Converted from public MIT CrewAI crew example (customer support crew). "
                "Original author retains copyright; see source_attribution."
            ),
            "license_spdx": "MIT",
            "commercial_use": True,
            "copyleft": False,
            "attribution_required": True,
            "workflow": [
                {
                    "name": "工单分诊",
                    "instruction_excerpt": "接收工单并做优先级分诊。",
                    "expected_output": "带优先级的工单队列。",
                },
                {
                    "name": "知识沉淀",
                    "instruction_excerpt": "检索知识库答复并沉淀重复问题。",
                    "expected_output": "已闭环工单与知识条目。",
                },
            ],
        },
        {
            "asset_slug": "crew_content_writer",
            "slug": "crew-content-writer",
            "department_type": "business.general",
            "name": "Content Writer",
            "role": "content_writer",
            "responsibility": "产出多形态、强品牌的营销内容，覆盖多渠道。",
            "default_instructions": (
                "你是 Curis 平台（多源扩展·CrewAI）的官方员工候选（draft 态，未激活）。\n"
                "背景：你是一名内容写作者，擅长把产品价值翻译为打动人心的内容。\n"
                "职责：按受众与渠道起草初稿与变体，兼顾品牌调性与合规；不夸大功效或编造用户案例，"
                "尊重版权，敏感行业内容须过合规。"
            ),
            "guardrails": [
                "不夸大功效或编造用户案例。",
                "尊重版权，素材须有合法授权。",
                "敏感行业内容须过合规。",
            ],
            "persona_archetype": "creative_explorer",
            "persona_traits": ["创意", "共情", "品牌敏感"],
            "persona_comm": {"tone": "playful", "format": "narrative"},
            "persona_report": {"frequency": "per-iteration"},
            "persona_collab": {"style": "brainstorming"},
            "persona_decision": "exploratory",
            "emoji": "",
            "color": "",
            "persona_identity": "内容写作者，把产品价值翻译为打动人心的故事。",
            "capability_types": ["model", "tool"],
            "default_skill": "",
            "default_tool": "tl_crew_seo_optimizer_tool",
            "star_rating": 4,
            "attribution": (
                "Converted from public MIT CrewAI crew example (content crew). "
                "Original author retains copyright; see source_attribution."
            ),
            "license_spdx": "MIT",
            "commercial_use": True,
            "copyleft": False,
            "attribution_required": True,
            "workflow": [
                {
                    "name": "起草初稿",
                    "instruction_excerpt": "明确受众与渠道，产出初稿与变体。",
                    "expected_output": "多尺寸内容草稿。",
                },
                {
                    "name": "合规自检",
                    "instruction_excerpt": "品牌与合规自检后定稿。",
                    "expected_output": "发布内容与表现回收。",
                },
            ],
        },
        {
            "asset_slug": "crew_code_reviewer",
            "slug": "crew-code-reviewer",
            "department_type": "business.general",
            "name": "Code Reviewer",
            "role": "code_reviewer",
            "responsibility": "对代码变更做静态分析与测试验证，输出审查结论。",
            "default_instructions": (
                "你是 Curis 平台（多源扩展·CrewAI）的官方员工候选（draft 态，未激活）。\n"
                "背景：你是一名代码审查者，熟悉静态分析与测试验证。\n"
                "职责：对代码变更做静态扫描与测试验证，输出带风险等级的结论；"
                "不擅自修改生产代码，重大风险须升级并留痕。"
            ),
            "guardrails": [
                "不擅自修改生产代码。",
                "重大风险须升级并留痕。",
                "结论须附证据（扫描/测试输出）。",
            ],
            "persona_archetype": "risk_aware_guardian",
            "persona_traits": ["审慎", "严谨", "风险优先"],
            "persona_comm": {"tone": "cautious", "format": "risk_first"},
            "persona_report": {"frequency": "per-change"},
            "persona_collab": {"style": "guarded"},
            "persona_decision": "conservative",
            "emoji": "",
            "color": "",
            "persona_identity": "代码审查者，在质量与风险边界上做守门人。",
            "capability_types": ["model", "tool"],
            "default_skill": "",
            "default_tool": "tl_crew_static_analysis_tool",
            "star_rating": 3,
            "attribution": (
                "Converted from public MIT CrewAI crew example (engineering crew). "
                "Original author retains copyright; see source_attribution."
            ),
            "license_spdx": "MIT",
            "commercial_use": True,
            "copyleft": False,
            "attribution_required": True,
            "workflow": [
                {
                    "name": "静态扫描",
                    "instruction_excerpt": "对变更做静态分析与风格检查。",
                    "expected_output": "问题清单与风险等级。",
                },
                {
                    "name": "测试验证",
                    "instruction_excerpt": "运行测试并复核覆盖率。",
                    "expected_output": "测试结论与遗留风险。",
                },
            ],
        },
        {
            "asset_slug": "crew_growth_strategist",
            "slug": "crew-growth-strategist",
            "department_type": "business.general",
            "name": "Growth Strategist",
            "role": "growth_strategist",
            "responsibility": "设计并复盘数据驱动的增长实验，放大获客与转化。",
            "default_instructions": (
                "你是 Curis 平台（多源扩展·CrewAI）的官方员工候选（draft 态，未激活）。\n"
                "背景：你是一名增长策略师，擅长以实验驱动增长。\n"
                "职责：围绕漏斗各环节设计可证伪增长实验，小流量验证后规模化或止损；"
                "实验优先于口头方案，不购买虚假流量或违规爬取数据。"
            ),
            "guardrails": [
                "实验优先于口头方案，先小流量验证。",
                "不购买虚假流量或违规爬取数据。",
                "对实验结果坦诚，失败也归档复盘。",
            ],
            "persona_archetype": "creative_explorer",
            "persona_traits": ["大胆", "敏捷", "结果导向"],
            "persona_comm": {"tone": "playful", "format": "narrative"},
            "persona_report": {"frequency": "per-experiment"},
            "persona_collab": {"style": "brainstorming"},
            "persona_decision": "exploratory",
            "emoji": "",
            "color": "",
            "persona_identity": "增长策略师，用低成本创意实验撬动增长杠杆。",
            "capability_types": ["model", "tool"],
            "default_skill": "",
            "default_tool": "tl_crew_campaign_analyzer_tool",
            "star_rating": 4,
            "attribution": (
                "Converted from public MIT CrewAI crew example (growth crew). "
                "Original author retains copyright; see source_attribution."
            ),
            "license_spdx": "MIT",
            "commercial_use": True,
            "copyleft": False,
            "attribution_required": True,
            "workflow": [
                {
                    "name": "定位漏点",
                    "instruction_excerpt": "定位漏斗最大漏点并提出可证伪假设。",
                    "expected_output": "增长假设清单。",
                },
                {
                    "name": "实验复盘",
                    "instruction_excerpt": "小流量上线实验，数据分析并规模化或止损。",
                    "expected_output": "实验结论与下一步动作。",
                },
            ],
        },
    ]
)

# ── CrewAI 工具候选（tl_crew_*，结构化具名工具，disposition=create）───────
CREWAI_TOOLS: list[dict] = _scrub_value(
    [
        {
            "id": "tl_crew_web_search_tool",
            "slug": "crew-web-search-tool",
            "name": "Web 检索工具",
            "description": "调用外部检索能力获取公开网页与资料，返回结构化结果。",
            "tool_type": "api_integration",
            "instruction_excerpt": "按查询词检索公开资料并汇总来源。",
            "disposition": "create",
            "source_attribution": "Converted from public MIT CrewAI crew example (market research crew).",
        },
        {
            "id": "tl_crew_data_analyzer_tool",
            "slug": "crew-data-analyzer-tool",
            "name": "数据分析工具",
            "description": "对结构化数据集做统计与可视化分析。",
            "tool_type": "data_processing",
            "instruction_excerpt": "加载数据集并产出统计与图表。",
            "disposition": "create",
            "source_attribution": "Converted from public MIT CrewAI crew example (market research crew).",
        },
        {
            "id": "tl_crew_ticket_reader_tool",
            "slug": "crew-ticket-reader-tool",
            "name": "工单读取工具",
            "description": "读取并解析客服工单内容，辅助分诊。",
            "tool_type": "api_integration",
            "instruction_excerpt": "按工单标识读取内容并提取关键信息。",
            "disposition": "create",
            "source_attribution": "Converted from public MIT CrewAI crew example (customer support crew).",
        },
        {
            "id": "tl_crew_knowledge_base_tool",
            "slug": "crew-knowledge-base-tool",
            "name": "知识库检索工具",
            "description": "检索内部知识库条目以辅助应答。",
            "tool_type": "data_processing",
            "instruction_excerpt": "按问题检索知识库并返回相关条目。",
            "disposition": "create",
            "source_attribution": "Converted from public MIT CrewAI crew example (customer support crew).",
        },
        {
            "id": "tl_crew_seo_optimizer_tool",
            "slug": "crew-seo-optimizer-tool",
            "name": "SEO 优化工具",
            "description": "分析内容关键词与可读性，给出 SEO 建议。",
            "tool_type": "data_processing",
            "instruction_excerpt": "分析文本并产出关键词与可读性建议。",
            "disposition": "create",
            "source_attribution": "Converted from public MIT CrewAI crew example (content crew).",
        },
        {
            "id": "tl_crew_grammar_checker_tool",
            "slug": "crew-grammar-checker-tool",
            "name": "语法检查工具",
            "description": "检查文本语法与拼写，给出修订建议。",
            "tool_type": "data_processing",
            "instruction_excerpt": "扫描文本语法并产出修订建议。",
            "disposition": "create",
            "source_attribution": "Converted from public MIT CrewAI crew example (content crew).",
        },
        {
            "id": "tl_crew_static_analysis_tool",
            "slug": "crew-static-analysis-tool",
            "name": "静态分析工具",
            "description": "对代码做静态分析与风格检查，输出问题清单。",
            "tool_type": "code_execution",
            "instruction_excerpt": "扫描代码并产出问题清单与风险等级。",
            "disposition": "create",
            "source_attribution": "Converted from public MIT CrewAI crew example (engineering crew).",
        },
        {
            "id": "tl_crew_test_runner_tool",
            "slug": "crew-test-runner-tool",
            "name": "测试运行器",
            "description": "运行测试用例并汇总结果。",
            "tool_type": "code_execution",
            "instruction_excerpt": "运行测试用例并汇总通过与失败。",
            "disposition": "create",
            "source_attribution": "Converted from public MIT CrewAI crew example (engineering crew).",
        },
        {
            "id": "tl_crew_campaign_analyzer_tool",
            "slug": "crew-campaign-analyzer-tool",
            "name": "活动分析工具",
            "description": "分析营销活动漏斗与转化指标。",
            "tool_type": "api_integration",
            "instruction_excerpt": "拉取活动指标并定位最大漏点。",
            "disposition": "create",
            "source_attribution": "Converted from public MIT CrewAI crew example (growth crew).",
        },
        {
            "id": "tl_crew_ab_test_tool",
            "slug": "crew-ab-test-tool",
            "name": "A/B 测试工具",
            "description": "设计与分析 A/B 实验，输出统计显著结论。",
            "tool_type": "data_processing",
            "instruction_excerpt": "配置实验并产出带置信区间的结论。",
            "disposition": "create",
            "source_attribution": "Converted from public MIT CrewAI crew example (growth crew).",
        },
    ]
)

# ── §T3：MCP Registry 工具候选（纯工具源，仅 tl_mcp_*）──────────────────
# 全部为净新增（与基线 115 工具零重叠），disposition=create。
# 若未来与已 seed MCP 工具重叠，可标记 enhance_existing + existing_id（见 _seed_mcp）。
MCP_MANIFEST: list[dict] = _scrub_value(
    [
        {
            "id": "tl_mcp_read_file",
            "slug": "mcp-read-file",
            "name": "读取文件",
            "description": "读取本地文件系统中的文件内容。",
            "tool_type": "file_io",
            "instruction_excerpt": "按路径读取文件并返回内容。",
            "disposition": "create",
            "existing_id": "",
            "source_attribution": "filesystem MCP server (MIT).",
            "license_spdx": "MIT",
        },
        {
            "id": "tl_mcp_write_file",
            "slug": "mcp-write-file",
            "name": "写入文件",
            "description": "向本地文件系统写入文件内容。",
            "tool_type": "file_io",
            "instruction_excerpt": "按路径写入内容到文件。",
            "disposition": "create",
            "existing_id": "",
            "source_attribution": "filesystem MCP server (MIT).",
            "license_spdx": "MIT",
        },
        {
            "id": "tl_mcp_list_directory",
            "slug": "mcp-list-directory",
            "name": "列出目录",
            "description": "列出目录下的文件与子目录。",
            "tool_type": "file_io",
            "instruction_excerpt": "列出指定目录内容。",
            "disposition": "create",
            "existing_id": "",
            "source_attribution": "filesystem MCP server (MIT).",
            "license_spdx": "MIT",
        },
        {
            "id": "tl_mcp_fetch_webpage",
            "slug": "mcp-fetch-webpage",
            "name": "抓取网页",
            "description": "抓取指定 URL 的网页内容并转为可读文本。",
            "tool_type": "api_integration",
            "instruction_excerpt": "抓取 URL 并返回清洗后的文本。",
            "disposition": "create",
            "existing_id": "",
            "source_attribution": "fetch MCP server (MIT).",
            "license_spdx": "MIT",
        },
        {
            "id": "tl_mcp_run_sql_query",
            "slug": "mcp-run-sql-query",
            "name": "执行 SQL",
            "description": "在 SQLite 数据库上执行参数化查询。",
            "tool_type": "database",
            "instruction_excerpt": "对 SQLite 执行只读/写查询。",
            "disposition": "create",
            "existing_id": "",
            "source_attribution": "sqlite MCP server (MIT).",
            "license_spdx": "MIT",
        },
        {
            "id": "tl_mcp_list_tables",
            "slug": "mcp-list-tables",
            "name": "列出数据表",
            "description": "列出 SQLite 数据库中的表与 schema。",
            "tool_type": "database",
            "instruction_excerpt": "列出数据库表与字段。",
            "disposition": "create",
            "existing_id": "",
            "source_attribution": "sqlite MCP server (MIT).",
            "license_spdx": "MIT",
        },
        {
            "id": "tl_mcp_git_status",
            "slug": "mcp-git-status",
            "name": "Git 状态",
            "description": "查看仓库工作区与暂存区状态。",
            "tool_type": "api_integration",
            "instruction_excerpt": "查看 git 工作区状态。",
            "disposition": "create",
            "existing_id": "",
            "source_attribution": "git MCP server (MIT).",
            "license_spdx": "MIT",
        },
        {
            "id": "tl_mcp_git_commit",
            "slug": "mcp-git-commit",
            "name": "Git 提交",
            "description": "将暂存改动提交到仓库。",
            "tool_type": "api_integration",
            "instruction_excerpt": "提交暂存改动并附消息。",
            "disposition": "create",
            "existing_id": "",
            "source_attribution": "git MCP server (MIT).",
            "license_spdx": "MIT",
        },
        {
            "id": "tl_mcp_sequential_thinking",
            "slug": "mcp-sequential-thinking",
            "name": "顺序推理",
            "description": "将复杂问题拆解为有序推理步骤。",
            "tool_type": "reasoning",
            "instruction_excerpt": "按步骤拆解并推进推理。",
            "disposition": "create",
            "existing_id": "",
            "source_attribution": "sequentialthinking MCP server (MIT).",
            "license_spdx": "MIT",
        },
    ]
)


# ── §T2：Skill 仓库（curispeng22-coder/skill）候选清单（skl_skill_* + tl_*）──
# 总控已授权 harvest 该无 LICENSE 个人仓库为 draft 候选（不发布、不 instantiation）。
# 许可元数据（§7.5 特批）：license_spdx='NOASSERTION'、commercial_use=False、
# attribution_required=True、attribution 注明来源与授权范围。代码层通用闸门逻辑
# 不变（仍拒绝 copyleft、仍对无 LICENSE 源打 skip）；本仓库因特批不触发 skip。
SKILL_ATTRIBUTION = (
    "来源 curispeng22-coder/skill；总控授权 draft 候选、不发布、不 instantiation。"
)
SKILL_LICENSE = {
    "license_spdx": "NOASSERTION",
    "commercial_use": False,
    "copyleft": False,
    "attribution_required": True,
    "attribution": SKILL_ATTRIBUTION,
}

# skl_skill_* 净新增方法论技能（全部 create；无重叠基线技能）。
SKILL_MANIFEST: list[dict] = _scrub_value(
    [
        {
            "id": "skl_skill_code_review",
            "slug": "skill-code-review",
            "name": "代码审查",
            "description": "对代码变更做静态分析与测试验证，输出风险分级的审查结论。",
            "skill_type": "analysis",
            "instruction_excerpt": "拉取变更并做静态分析，运行测试复核覆盖率，输出带证据的结论。",
            "category": "skill_repo",
            **SKILL_LICENSE,
        },
        {
            "id": "skl_skill_data_analysis",
            "slug": "skill-data-analysis",
            "name": "数据分析",
            "description": "对结构化数据集做统计与可视化分析，输出可解释结论。",
            "skill_type": "analysis",
            "instruction_excerpt": "加载清洗数据，做统计与分组对比，生成图表与结论。",
            "category": "skill_repo",
            **SKILL_LICENSE,
        },
        {
            "id": "skl_skill_doc_writing",
            "slug": "skill-doc-writing",
            "name": "文档写作",
            "description": "产出多形态、强品牌的文档内容，兼顾品牌调性与合规。",
            "skill_type": "creation",
            "instruction_excerpt": "按受众起草初稿，检索知识库补全事实并做合规自检。",
            "category": "skill_repo",
            **SKILL_LICENSE,
        },
        {
            "id": "skl_skill_web_research",
            "slug": "skill-web-research",
            "name": "网络调研",
            "description": "联网检索并综合公开资料，输出带来源与不确定性的研究简报。",
            "skill_type": "research",
            "instruction_excerpt": "按主题检索去重交叉验证，聚类并输出带来源的研究简报。",
            "category": "skill_repo",
            **SKILL_LICENSE,
        },
        {
            "id": "skl_skill_customer_support",
            "slug": "skill-customer-support",
            "name": "客户支持",
            "description": "在多渠道分诊并高质量应答客户问题，沉淀可复用知识。",
            "skill_type": "creation",
            "instruction_excerpt": "接收工单分诊，检索知识库应答，沉淀重复问题为知识。",
            "category": "skill_repo",
            **SKILL_LICENSE,
        },
    ]
)

# tl_* 工具候选（skill 仓库）：净新增 tl_skill_*（create）+ 与 Pack F-J 基线工具
# 重叠者 enhance_existing（seed 时按 slug/name 动态匹配既有 tool_templates，
# UPDATE 富字段，不新建重复行）。enhance_existing 行的 slug/name 故意对齐基线工具
# 以便动态解析命中（tl_github / tl_notion / tl_slack / tl_brave_search /
# tl_ai_rd_pandas_analyzer / tl_ai_rd_chart_plotter / tl_ai_rd_docx_generator）。
SKILL_TOOLS: list[dict] = _scrub_value(
    [
        # ── 净新增（create）──
        {
            "id": "tl_skill_static_analysis",
            "slug": "skill-static-analysis",
            "name": "静态分析",
            "description": "对代码做静态分析与风格检查，输出问题清单与风险等级。",
            "tool_type": "code_execution",
            "instruction_excerpt": "扫描代码并产出问题清单与风险等级。",
            "disposition": "create",
            "existing_id": "",
            "source_attribution": SKILL_ATTRIBUTION,
            **SKILL_LICENSE,
        },
        {
            "id": "tl_skill_web_fetch",
            "slug": "skill-web-fetch",
            "name": "网页抓取",
            "description": "抓取指定 URL 的网页内容并转为可读文本。",
            "tool_type": "api_integration",
            "instruction_excerpt": "抓取 URL 并返回清洗后的文本。",
            "disposition": "create",
            "existing_id": "",
            "source_attribution": SKILL_ATTRIBUTION,
            **SKILL_LICENSE,
        },
        {
            "id": "tl_skill_knowledge_base",
            "slug": "skill-knowledge-base",
            "name": "知识库",
            "description": "检索内部知识库条目以辅助应答与沉淀。",
            "tool_type": "data_processing",
            "instruction_excerpt": "按问题检索知识库并返回相关条目。",
            "disposition": "create",
            "existing_id": "",
            "source_attribution": SKILL_ATTRIBUTION,
            **SKILL_LICENSE,
        },
        # ── 与基线工具重叠（enhance_existing，动态匹配 slug/name）──
        {
            "id": "tl_skill_github_enh",
            "slug": "github",
            "name": "GitHub",
            "description": "GitHub（经 curispeng22 skill 仓库增强）：管理仓库/PR/Issue/Actions 的代码协作。",
            "tool_type": "api_integration",
            "instruction_excerpt": "经 skill 仓库增强：结合代码审查流程管理仓库、PR 与 Issue。",
            "disposition": "enhance_existing",
            "existing_id": "",
            "source_attribution": SKILL_ATTRIBUTION,
            **SKILL_LICENSE,
        },
        {
            "id": "tl_skill_notion_enh",
            "slug": "notion",
            "name": "Notion",
            "description": "Notion（经 curispeng22 skill 仓库增强）：读写页面/数据库/block 的文档协作。",
            "tool_type": "api_integration",
            "instruction_excerpt": "经 skill 仓库增强：结合文档写作流程读写 Notion 页面与数据库。",
            "disposition": "enhance_existing",
            "existing_id": "",
            "source_attribution": SKILL_ATTRIBUTION,
            **SKILL_LICENSE,
        },
        {
            "id": "tl_skill_slack_enh",
            "slug": "slack",
            "name": "Slack",
            "description": "Slack（经 curispeng22 skill 仓库增强）：读取/发送消息与管理频道。",
            "tool_type": "api_integration",
            "instruction_excerpt": "经 skill 仓库增强：结合客户支持流程处理 Slack 工单与通知。",
            "disposition": "enhance_existing",
            "existing_id": "",
            "source_attribution": SKILL_ATTRIBUTION,
            **SKILL_LICENSE,
        },
        {
            "id": "tl_skill_brave_search_enh",
            "slug": "brave_search",
            "name": "Brave Search",
            "description": "Brave Search（经 curispeng22 skill 仓库增强）：对外暴露网络检索能力。",
            "tool_type": "api_integration",
            "instruction_excerpt": "经 skill 仓库增强：结合网络调研流程做去重与交叉验证检索。",
            "disposition": "enhance_existing",
            "existing_id": "",
            "source_attribution": SKILL_ATTRIBUTION,
            **SKILL_LICENSE,
        },
        {
            "id": "tl_skill_pandas_analyzer_enh",
            "slug": "pandas_analyzer",
            "name": "Pandas 分析器",
            "description": "Pandas 分析器（经 curispeng22 skill 仓库增强）：用 Pandas 做数据清洗与分析。",
            "tool_type": "data_processing",
            "instruction_excerpt": "经 skill 仓库增强：结合数据分析流程做统计与分组对比。",
            "disposition": "enhance_existing",
            "existing_id": "",
            "source_attribution": SKILL_ATTRIBUTION,
            **SKILL_LICENSE,
        },
        {
            "id": "tl_skill_chart_plotter_enh",
            "slug": "chart_plotter",
            "name": "图表绘制器",
            "description": "图表绘制器（经 curispeng22 skill 仓库增强）：生成可视化图表。",
            "tool_type": "data_processing",
            "instruction_excerpt": "经 skill 仓库增强：结合数据分析流程生成可视化图表。",
            "disposition": "enhance_existing",
            "existing_id": "",
            "source_attribution": SKILL_ATTRIBUTION,
            **SKILL_LICENSE,
        },
        {
            "id": "tl_skill_docx_generator_enh",
            "slug": "docx_generator",
            "name": "Word 生成器",
            "description": "Word 生成器（经 curispeng22 skill 仓库增强）：生成 .docx 文档。",
            "tool_type": "document",
            "instruction_excerpt": "经 skill 仓库增强：结合文档写作流程生成结构化 .docx。",
            "disposition": "enhance_existing",
            "existing_id": "",
            "source_attribution": SKILL_ATTRIBUTION,
            **SKILL_LICENSE,
        },
    ]
)


# ── workflow_templates（wt_crew_*，draft）────────────────────────────────
# map_workflow 在 seed.py 中硬编码 wt_pilot_b_ 前缀，CrewAI 需独立前缀，故本模块
# 提供复用 SeedMapper 形状但前缀为 wt_crew_ 的映射助手（不修改 seed.py）。
def map_crew_workflow(entry: dict) -> tuple:
    """CrewAI 工作流行（wt_crew_<local>，draft，department_type=business.general）。"""
    steps = [
        {
            "step_order": i + 1,
            "name": s["name"],
            "owner_role": entry["role"],
            "instruction_excerpt": s["instruction_excerpt"],
            "expected_output": s["expected_output"],
        }
        for i, s in enumerate(entry["workflow"])
    ]
    return (
        f"wt_{entry['asset_slug']}",  # id (PK) = wt_crew_<local>
        f"{entry['name']} 工作流",  # name
        entry["responsibility"],  # description
        "official",  # source
        "platform",  # tenant_id
        entry["department_type"],  # department_type = business.general
        "sequential",  # process_type
        json.dumps(steps, ensure_ascii=False),  # steps_json
        "draft",  # status
    )


def build_multisource_rows() -> dict[str, Any]:
    """产出 CrewAI + MCP 全部候选行（供 database.py seed 消费）。

    复用 ``SeedMapper.map_persona/map_employee/map_tool``（形状一致），
    workflow 使用本模块 ``map_crew_workflow``（wt_crew_ 前缀）。

    Returns:
        {
          "crew_personas": [...],   # pt_crew_*
          "crew_employees": [...],  # official.employee.crew_*
          "crew_workflows": [...],  # wt_crew_*
          "crew_tools": [...],      # tl_crew_*
          "mcp_tools": [...],       # tl_mcp_*（含 disposition / existing_id）
        }
    """
    crew_personas = [SeedMapper.map_persona(e) for e in CREWAI_MANIFEST]
    crew_employees = [SeedMapper.map_employee(e) for e in CREWAI_MANIFEST]
    crew_workflows = [map_crew_workflow(e) for e in CREWAI_MANIFEST]
    crew_tools = [SeedMapper.map_tool(t) for t in CREWAI_TOOLS]
    # MCP 行保留为原始 dict（含 disposition / existing_id），由 _seed_mcp 内部
    # 按 disposition 分支做 map_tool / UPDATE，故此处不预映射。
    mcp_tools = MCP_MANIFEST
    # Skill 行：skills 预映射为 tuple（全部 create）；tools 保留原始 dict
    # （含 disposition / existing_id），由 _seed_skill_repo 内部按 disposition 分支。
    skill_skills = [SeedMapper.map_skill(s) for s in SKILL_MANIFEST]
    skill_tools = SKILL_TOOLS
    return {
        "crew_personas": crew_personas,
        "crew_employees": crew_employees,
        "crew_workflows": crew_workflows,
        "crew_tools": crew_tools,
        "mcp_tools": mcp_tools,
        "skill_skills": skill_skills,
        "skill_tools": skill_tools,
    }


# ── 可选 CLI 运行器（镜像 seed_pilot_b.py，支持 --rollback）──────────────
def _counts(db) -> dict:
    with db.connect() as conn:
        def _c(sql: str) -> int:
            return conn.execute(sql).fetchone()[0]

        return {
            "persona_templates(pt_crew_*)": _c(
                "select count(*) from persona_templates where persona_id like 'pt_crew_%'"
            ),
            "employee_templates(official.employee.crew_*)": _c(
                "select count(*) from employee_templates where id like 'official.employee.crew_%'"
            ),
            "tool_templates(tl_crew_*)": _c(
                "select count(*) from tool_templates where tool_template_id like 'tl_crew_%'"
            ),
            "tool_templates(tl_mcp_*)": _c(
                "select count(*) from tool_templates where tool_template_id like 'tl_mcp_%'"
            ),
            "workflow_templates(wt_crew_*)": _c(
                "select count(*) from workflow_templates where id like 'wt_crew_%'"
            ),
            "department_types(business.*)": _c(
                "select count(*) from department_types where type_key like 'business.%'"
            ),
        }


def main(argv: list[str]) -> int:
    import sys

    args = [a for a in argv[1:] if not a.startswith("--")]
    db_path = args[0] if args else "curis_multisource.sqlite"
    rollback = "--rollback" in argv

    from app.database import Database

    db = Database(path=db_path)
    if rollback:
        db.rollback_crewai()
        db.rollback_mcp()
        print(f"[rollback] CrewAI + MCP 资产已回滚：{db_path}")
        for k, v in _counts(db).items():
            print(f"  {k}: {v}")
        return 0

    db.seed_crewai()
    db.seed_mcp()
    print(f"[seed] CrewAI + MCP 候选/草稿已叠加写入：{db_path}")
    for k, v in _counts(db).items():
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    import sys

    raise SystemExit(main(sys.argv))
