"""Wave-1 种子与实例化编排（Curis 自用 v1 · 第一波）。

本模块把 **第一波（Curis 侧轻量路径，零 DevOps 依赖）** 所需的全部
官方资产灌库并实例化为真实运行部门，严格贴合既有
``backend/app/database.py`` 的 seed 风格与 ``catalog_constants.py`` 枚举。

依赖顺序（主理人裁定）：T08 → T04 → T05 → T07 → T06 → T09 → T10 → T16。
本文件覆盖 T04 / T05 / T06 的资产 seed 与 T09 的实例化（T08 的
tenant 归一在 ``_migrate_selfuse_tenant``，T07 见 ``content_publish_package.py``，
T10 / T16 见各自模块）。

设计约束（来自 v1-selfuse-architecture.md）：
- 全局固定 ``tenant_id = 'selfuse'``：先归一既有 ``platform``/``default`` 行，
  新 seed 一律写 ``selfuse``，保留 tenant_id 列但不写多租户隔离逻辑。
- 复用已 seed 的 ``skl_ai_rd_*``(52) / ``tl_ai_rd_*``(30) 与
  ``wl_ai_rd_*``(16) / ``wl_ai_content_*``(12)（已在 workflow_contents / skill_templates /
  tool_templates），**不重建**。
- 新增命名空间严格按架构：研发部 ``tech.rd``、内容增长部 ``content.growth``。
- 所有写入幂等（insert or ignore / insert or replace），可重复运行。
- 不写明文 secret；connector 工具仅定义元数据（真实调用留第二波）。
"""

from __future__ import annotations

import json
from typing import Any

from .database import Database
from .tenant_context import DEFAULT_TENANT

# ── 目录表（需做 tenant 归一；department_types 无 tenant 列，跳过）──
_CATALOG_TENANT_TABLES = [
    "employee_templates",
    "department_templates",
    "skill_templates",
    "tool_templates",
    "workflow_templates",
    "workflow_contents",
    "company_packages",
    "company_templates",
    "persona_templates",
    "dashboard_templates",
    "dashboard_widget_catalog",
]

# ── T04：研发部类型 + 员工模板（绑定已 seed 的 skl_ai_rd_*/tl_ai_rd_*）──
RD_DEPARTMENT_TYPE = ("tech.rd", "tech", "研发部", "Curis 自用研发部：PM/Architect/TechLead/Backend/QA/DevOps 协作的软件研发闭环。")
RD_DEPARTMENT_TEMPLATE = ("dt_ai_rd", "研发部", "tech.rd", "Curis 自用研发部：6 类角色 + 16 条工作流，绑定已 seed 的 skl_ai_rd_*/tl_ai_rd_*。")

# (id, slug, name, role, responsibility, description, default_skill, default_tool)
_RD_EMPLOYEES = [
    ("et_ai_rd_pm", "pm", "Product Manager", "product_manager",
     "理解 CEO 需求，确认范围、验收标准和不做事项。",
     "研发部产品规划员工，把任务转成清晰的产品范围和验收标准。",
     "skl_ai_rd_requirement_analysis", "tl_ai_rd_github_api"),
    ("et_ai_rd_architect", "architect", "Architect", "architect",
     "定义系统边界、数据模型、API 和模块风险。",
     "研发部架构员工，优先复用现有架构，避免未批准的执行链路。",
     "skl_ai_rd_system_design", "tl_ai_rd_code_linter"),
    ("et_ai_rd_tech_lead", "tech-lead", "Tech Lead", "tech_lead",
     "接收研发任务，拆解执行路径，并在任务结束后汇总交付证据。",
     "研发部任务负责人，默认接收未指定员工的研发任务。",
     "skl_ai_rd_api_design", "tl_ai_rd_git_client"),
    ("et_ai_rd_backend", "backend", "Backend Engineer", "backend_engineer",
     "实现 Workspace 后端数据模型、API 和测试。",
     "研发部后端员工，保持租户隔离与模型网关适配器路径不漂移。",
     "skl_ai_rd_backend_development", "tl_ai_rd_code_executor"),
    ("et_ai_rd_qa", "qa", "QA Engineer", "qa_engineer",
     "执行验证、回归测试、范围扫描和验收证据整理。",
     "研发部质量员工，验证现有功能不回退，完成声明须有新鲜证据。",
     "skl_ai_rd_test_design", "tl_ai_rd_test_runner"),
    ("et_ai_rd_devops", "devops", "DevOps Engineer", "devops_engineer",
     "搭建 CI/CD、容器化与可观测性，保障安全可控发布。",
     "研发部运维员工，以灰度与回滚预案控制上线风险。",
     "skl_ai_rd_cicd_pipeline", "tl_ai_rd_ci_runner"),
]

# ── T05：内容部类型 + 技能(33) / 工具(10+) / 员工(12) ──
CONTENT_DEPARTMENT_TYPE = ("content.growth", "content", "内容增长部", "Curis 自用内容增长部：选题→脚本→制作→SEO→分发→度量 的内容生产闭环。")
CONTENT_DEPARTMENT_TEMPLATE = ("dt_ai_content", "内容增长部", "content.growth", "Curis 自用内容增长部：12 类角色 + 12 条工作流，绑定 skl_ai_content_*/tl_ai_content_* + tl_ai_content_social_upload。")

# (id, slug, name, description, skill_type, category)
_CONTENT_SKILLS = [
    ("skl_ai_content_topic_research", "topic-research", "选题研究", "从趋势与受众中识别可内容化的选题并排序。", "research", "research"),
    ("skl_ai_content_data_analysis", "data-analysis", "数据分析", "解读传播/平台数据，提炼可复用的内容洞察。", "analysis", "analysis"),
    ("skl_ai_content_content_planning", "content-planning", "内容策划", "把选题拆为系列主题、节奏与栏目规划。", "planning", "planning"),
    ("skl_ai_content_script_writing", "script-writing", "脚本撰写", "按平台调性撰写口播/分镜脚本，控制钩子与节奏。", "writing", "writing"),
    ("skl_ai_content_copywriting", "copywriting", "文案写作", "产出平台适配的标题、正文与行动号召文案。", "writing", "writing"),
    ("skl_ai_content_storytelling", "storytelling", "故事叙述", "用人物/冲突/转折结构提升内容记忆与共鸣。", "writing", "writing"),
    ("skl_ai_content_video_planning", "video-planning", "视频策划", "规划视频选题、时长、分镜与发布节奏。", "planning", "video"),
    ("skl_ai_content_video_production", "video-production", "视频制作", "组织拍摄/剪辑/配音，输出成片与多版本。", "production", "video"),
    ("skl_ai_content_short_video_editing", "short-video-editing", "短视频剪辑", "按平台规范做短视频剪辑、字幕与节拍对齐。", "production", "video"),
    ("skl_ai_content_cover_design_advice", "cover-design-advice", "封面设计建议", "给出平台化的封面构图、配色与文字排版建议。", "design", "design"),
    ("skl_ai_content_image_generation_prompt", "image-generation-prompt", "图像生成提示词", "为图像/封面生成模型撰写高质量提示词。", "design", "design"),
    ("skl_ai_content_seo_optimization", "seo-optimization", "SEO 优化", "围绕关键词与结构优化内容搜索可见性。", "optimization", "seo"),
    ("skl_ai_content_keyword_research", "keyword-research", "关键词研究", "挖掘高意图关键词并聚类到内容主题。", "research", "seo"),
    ("skl_ai_content_editorial_calendar", "editorial-calendar", "编辑日历", "编排多平台发布日历与栏目节奏。", "planning", "planning"),
    ("skl_ai_content_distribution", "distribution", "多渠道分发", "把成片与文案适配到多平台并跟踪分发。", "release", "distribution"),
    ("skl_ai_content_content_audit", "content-audit", "内容审核", "按平台规则与品牌语气做合规与质量审核。", "qa", "qa"),
    ("skl_ai_content_brand_voice", "brand-voice", "品牌语气", "维护统一品牌语气与表达边界，避免漂移。", "writing", "brand"),
    ("skl_ai_content_community_management", "community-management", "社群运营", "在评论区与社群做互动、答疑与声誉维护。", "operations", "community"),
    ("skl_ai_content_ugc_campaign", "ugc-campaign", "UGC 活动", "设计用户共创活动并组织征集与评选。", "operations", "growth"),
    ("skl_ai_content_livestream_hosting", "livestream-hosting", "直播主持", "主持直播流程、控场与实时互动转化。", "operations", "live"),
    ("skl_ai_content_viral_analysis", "viral-analysis", "传播分析", "分析爆款要素与传播路径，反哺选题。", "analysis", "analysis"),
    ("skl_ai_content_audience_insight", "audience-insight", "受众洞察", "刻画目标受众画像、痛点与内容偏好。", "research", "research"),
    ("skl_ai_content_competitor_monitoring", "competitor-monitoring", "竞品监测", "监测竞品内容策略与声量变化。", "research", "research"),
    ("skl_ai_content_title_hook", "title-hook", "标题钩子", "撰写高点击标题与开场钩子。", "writing", "writing"),
    ("skl_ai_content_transcreation", "transcreation", "跨语言创意本地化", "把内容本地化为多语言版本而不失调性。", "writing", "writing"),
    ("skl_ai_content_fact_checking", "fact-checking", "事实核查", "核查数据与引用，避免误导与合规风险。", "qa", "qa"),
    ("skl_ai_content_content_repurposing", "content-repurposing", "内容再加工", "把长内容拆解为短内容矩阵，提升复用。", "production", "production"),
    ("skl_ai_content_email_newsletter", "email-newsletter", "邮件简报", "策划与撰写邮件简报，沉淀私域读者。", "writing", "writing"),
    ("skl_ai_content_social_listening", "social-listening", "社媒倾听", "监测社媒声量与情绪，发现选题与危机。", "research", "research"),
    ("skl_ai_content_podcast_script", "podcast-script", "播客脚本", "撰写播客大纲与对谈脚本。", "writing", "writing"),
    ("skl_ai_content_infographic_design", "infographic-design", "信息图设计", "把数据/流程设计为可读信息图。", "design", "design"),
    ("skl_ai_content_product_description", "product-description", "产品描述", "撰写平台化的产品卖点与描述文案。", "writing", "writing"),
    ("skl_ai_content_trend_forecast", "trend-forecast", "趋势预测", "结合信号做内容趋势前瞻与提前布局。", "research", "research"),
]

# (id, slug, name, description, tool_type, capability_types_json)
_CONTENT_TOOLS = [
    ("tl_ai_content_web_search", "web-search", "Web 搜索", "发起联网检索并解析结果，支撑选题与事实核查。", "api_integration", '["tool"]'),
    ("tl_ai_content_browser_scraper", "browser-scraper", "浏览器抓取", "按 URL 抓取页面内容与结构化字段。", "web_browser", '["tool"]'),
    ("tl_ai_content_image_generator", "image-generator", "图像生成", "调用图像模型生成封面/配图/海报。", "content_generation", '["tool"]'),
    ("tl_ai_content_video_generator", "video-generator", "视频生成", "调用视频模型生成短片或分镜素材。", "content_generation", '["tool"]'),
    ("tl_ai_content_text_to_speech", "text-to-speech", "语音合成", "把脚本合成为拟人化配音。", "audio", '["tool"]'),
    ("tl_ai_content_speech_to_text", "speech-to-text", "语音识别", "把音视频转录为字幕与文稿。", "audio", '["tool"]'),
    ("tl_ai_content_translation_api", "translation-api", "翻译 API", "调用翻译服务做跨语言本地化。", "api_integration", '["tool"]'),
    ("tl_ai_content_spreadsheet_read", "spreadsheet-read", "表格读取", "读取表格以驱动编辑日历与度量。", "data_processing", '["tool"]'),
    ("tl_ai_content_markdown_renderer", "markdown-renderer", "Markdown 渲染", "把内容渲染为规范 Markdown 草稿。", "document", '["tool"]'),
    ("tl_ai_content_youtube_transcript", "youtube-transcript", "YouTube 转录", "抓取并转录 YouTube 视频文案。", "web_browser", '["tool"]'),
]

# T05 新增：social-auto-upload connector 工具壳（真实调用逻辑留第二波 T11）。
CONTENT_SOCIAL_UPLOAD_TOOL = (
    "tl_ai_content_social_upload", "social-upload", "社交媒体发布",
    "social-auto-upload（MIT，自托管）connector 工具壳：把 ContentPublishPackage "
    "推送到发布执行端，按平台调用 `sau <platform> 发布`；per-platform cookie "
    "取自 Vault（统一引用格式 local-dev://tenant/selfuse/credential/social_<platform>_cookie，"
    "兼容 VAULT_REF_RE 的 /tenant/ 段约定）。第二波 T11 接真实调用。",
    "social_media", '["connector", "tool"]',
)

# (id, slug, name, role, responsibility, description, default_skill, default_tool)
_CONTENT_EMPLOYEES = [
    ("et_ai_content_operator", "operator", "Content Operator", "content_operator",
     "端到端拥有内容产出与发布物质量。",
     "内容部运营员工，默认接收内容生产任务并交付发布包。",
     "skl_ai_content_copywriting", "tl_ai_content_markdown_renderer"),
    ("et_ai_content_researcher", "researcher", "Content Researcher", "content_researcher",
     "研究选题、趋势与受众，供给内容方向。",
     "内容部研究员工，从趋势与数据中产出选题。",
     "skl_ai_content_topic_research", "tl_ai_content_web_search"),
    ("et_ai_content_script_writer", "script-writer", "Script Writer", "script_writer",
     "撰写口播与分镜脚本。",
     "内容部脚本员工，控制钩子与平台调性。",
     "skl_ai_content_script_writing", "tl_ai_content_youtube_transcript"),
    ("et_ai_content_seo", "seo", "SEO Specialist", "seo_specialist",
     "优化内容搜索可见性与关键词布局。",
     "内容部 SEO 员工，围绕关键词做结构优化。",
     "skl_ai_content_seo_optimization", "tl_ai_content_markdown_renderer"),
    ("et_ai_content_distribution", "distribution", "Distribution Operator", "distribution_operator",
     "把内容适配多平台并跟踪分发结果。",
     "内容部分发员工，拥有多渠道发布执行。",
     "skl_ai_content_distribution", "tl_ai_content_social_upload"),
    ("et_ai_content_planner", "planner", "Content Planner", "content_planner",
     "编排选题、日历与栏目节奏。",
     "内容部策划员工，统筹内容节奏。",
     "skl_ai_content_content_planning", "tl_ai_content_spreadsheet_read"),
    ("et_ai_content_auditor", "auditor", "Content Auditor", "content_auditor",
     "按平台规则与品牌语气做审核。",
     "内容部审核员工，把控合规与质量。",
     "skl_ai_content_content_audit", "tl_ai_content_markdown_renderer"),
    ("et_ai_content_video_producer", "video-producer", "Video Producer", "video_producer",
     "组织视频制作与成片输出。",
     "内容部视频员工，拥有视频生产链路。",
     "skl_ai_content_video_production", "tl_ai_content_video_generator"),
    ("et_ai_content_live_host", "live-host", "Live Host", "live_host",
     "主持直播并做实时互动转化。",
     "内容部直播员工，拥有直播流程。",
     "skl_ai_content_livestream_hosting", "tl_ai_content_text_to_speech"),
    ("et_ai_content_community_manager", "community-manager", "Community Manager", "community_manager",
     "运营社群与评论区互动。",
     "内容部社群员工，维护声誉与活跃。",
     "skl_ai_content_community_management", "tl_ai_content_browser_scraper"),
    ("et_ai_content_data_analyst", "data-analyst", "Data Analyst", "data_analyst",
     "分析传播与度量数据，反哺选题。",
     "内容部数据员工，提炼内容洞察。",
     "skl_ai_content_viral_analysis", "tl_ai_content_spreadsheet_read"),
    ("et_ai_content_brand_manager", "brand-manager", "Brand Manager", "brand_manager",
     "维护品牌语气与表达边界。",
     "内容部品牌员工，把控语气一致。",
     "skl_ai_content_brand_voice", "tl_ai_content_markdown_renderer"),
]

# T05：内容工作流容器（wt_*，对应已 seed 的 wl_ai_content_* workflow_template_ref）。
# (id, name, steps_json)
_CONTENT_WT_CONTAINERS = [
    ("wt_content_production_sop", "内容生产 SOP", '["选题", "脚本", "制作", "审核", "发布"]'),
    ("wt_topic_research_sop", "选题研究 SOP", '["趋势扫描", "受众对齐", "选题产出"]'),
    ("wt_script_writing_sop", "脚本撰写 SOP", '["钩子", "结构", "成稿"]'),
    ("wt_video_production_sop", "视频制作 SOP", '["分镜", "拍摄", "剪辑", "配音"]'),
    ("wt_seo_optimization_sop", "SEO 优化 SOP", '["关键词", "结构", "内链"]'),
    ("wt_editorial_calendar_sop", "编辑日历 SOP", '["栏目", "排期", "复盘"]'),
    ("wt_multichannel_distribution_sop", "多渠道分发 SOP", '["适配", "发布", "回收"]'),
    ("wt_content_audit_sop", "内容审核 SOP", '["合规", "语气", "结论"]'),
    ("wt_livestream_sop", "直播 SOP", '["预热", "控场", "转化"]'),
    ("wt_ugc_campaign_sop", "UGC 活动 SOP", '["征集", "评选", "放大"]'),
    ("wt_viral_analysis_sop", "传播分析 SOP", '["度量", "归因", "反哺"]'),
    ("wt_brand_voice_sop", "品牌语气 SOP", '["基调", "边界", "巡检"]'),
]

# T06：两公司包引用集合。
RD_WORKFLOW_REFS = [
    "wl_ai_rd_software_dev_sop", "wl_ai_rd_requirement_to_prd", "wl_ai_rd_system_design_sop",
    "wl_ai_rd_api_dev_sop", "wl_ai_rd_feature_dev_sop", "wl_ai_rd_tdd_sop",
    "wl_ai_rd_code_review_sop", "wl_ai_rd_bugfix_sop", "wl_ai_rd_ci_cd_sop",
    "wl_ai_rd_data_pipeline_sop", "wl_ai_rd_database_migration_sop", "wl_ai_rd_security_review_sop",
    "wl_ai_rd_incident_response_sop", "wl_ai_rd_performance_tuning_sop",
    "wl_ai_rd_microservice_bootstrap_sop", "wl_ai_rd_tech_spike_sop",
]
RD_SKILL_REFS = [
    "skl_ai_rd_python_development", "skl_ai_rd_system_design", "skl_ai_rd_requirement_analysis",
    "skl_ai_rd_test_design", "skl_ai_rd_api_design", "skl_ai_rd_code_review",
]
RD_TOOL_REFS = [
    "tl_ai_rd_code_executor", "tl_ai_rd_test_runner", "tl_ai_rd_code_linter",
    "tl_ai_rd_git_client", "tl_ai_rd_python_repl", "tl_ai_rd_file_reader",
]
CONTENT_WORKFLOW_REFS = [
    "wl_ai_content_content_production_sop", "wl_ai_content_topic_research_sop",
    "wl_ai_content_script_writing_sop", "wl_ai_content_video_production_sop",
    "wl_ai_content_seo_optimization_sop", "wl_ai_content_editorial_calendar_sop",
    "wl_ai_content_multichannel_distribution_sop", "wl_ai_content_content_audit_sop",
    "wl_ai_content_livestream_sop", "wl_ai_content_ugc_campaign_sop",
    "wl_ai_content_viral_analysis_sop", "wl_ai_content_brand_voice_sop",
]
CONTENT_SKILL_REFS = [sid for sid, _, _, _, _, _ in _CONTENT_SKILLS[:8]]
CONTENT_TOOL_REFS = [tid for tid, _, _, _, _, _ in _CONTENT_TOOLS] + [
    "tl_ai_content_social_upload",
]


def _migrate_selfuse_tenant(connection: Any) -> int:
    """T08：把既有 ``platform``/``default`` 目录行归一为固定 ``selfuse``。

    单账号下只保留一个 tenant；不改列、不删字段，仅做值归一
    （非重建——资产内容原样保留）。返回受影响行数（仅用于日志）。
    """
    affected = 0
    for table in _CATALOG_TENANT_TABLES:
        cursor = connection.execute(
            f"update {table} set tenant_id = ? where tenant_id in ('platform', 'default')",
            (DEFAULT_TENANT,),
        )
        affected += cursor.rowcount if cursor.rowcount >= 0 else 0
    # tenants 注册表：把 default 行归一为 selfuse（保留默认公司归属）。
    # 若 selfuse 已存在（如本会话 initialize() 已按 DEFAULT_TENANT 建好），
    # 直接删除遗留 default 行，避免 UNIQUE 冲突（tenant 注册表无目录数据，删除安全）。
    existing = connection.execute(
        "select 1 from tenants where tenant_id = ?", (DEFAULT_TENANT,)
    ).fetchone()
    if existing:
        cursor = connection.execute("delete from tenants where tenant_id = 'default'")
        affected += 1 if cursor.rowcount >= 0 else 0
    else:
        cursor = connection.execute(
            "update tenants set tenant_id = ? where tenant_id = 'default'",
            (DEFAULT_TENANT,),
        )
        affected += cursor.rowcount if cursor.rowcount >= 0 else 0
    return affected


def _seed_department_types(connection: Any) -> None:
    """T04/T06：注册 ``tech.rd`` 与 ``content.growth`` 类型（幂等）。"""
    rows = [RD_DEPARTMENT_TYPE, CONTENT_DEPARTMENT_TYPE]
    connection.executemany(
        "insert or ignore into department_types "
        "(type_key, category, display_name, description, manifest_json, "
        "manifest_schema_version, is_system) values (?, ?, ?, ?, '{}', '0.0', 1)",
        [(rk, cat, name, desc) for (rk, cat, name, desc) in rows],
    )


def _seed_rd_employee_templates(connection: Any) -> None:
    """T04：seed ``et_ai_rd_*``(6)，绑定已 seed 的 skl_ai_rd_*/tl_ai_rd_*。"""
    connection.executemany(
        "insert or ignore into employee_templates "
        "(id, slug, name, role, responsibility, description, department_type, "
        "default_instructions, default_capability_types_json, default_model_policy_json, "
        "default_workflow_step_types_json, guardrails_json, source, tenant_id, enabled, "
        "persona_ref, default_skill, default_tool, version, status) "
        "values (?, ?, ?, ?, ?, ?, 'tech.rd', ?, '[\"model\",\"tool\"]', '{\"mode\":\"tenant_default\"}', "
        "'[]', '[]', 'official', ?, 1, '', ?, ?, '1.0.0', 'active')",
        [
            (
                eid, slug, name, role, responsibility, description, instructions,
                DEFAULT_TENANT, default_skill, default_tool,
            )
            for (eid, slug, name, role, responsibility, description, default_skill, default_tool) in _RD_EMPLOYEES
            for instructions in [f"按 {role} 职责交付；优先复用既有资产，不绕过安全/租户边界。"]
        ],
    )


def _seed_content_skill_templates(connection: Any) -> None:
    """T05：seed ``skl_ai_content_*``(33)。"""
    connection.executemany(
        "insert or ignore into skill_templates "
        "(skill_template_id, slug, name, description, skill_type, "
        "default_capability_types_json, instruction_excerpt, source, tenant_id, status, version, category) "
        "values (?, ?, ?, ?, ?, '[\"model\"]', ?, 'official', ?, 'active', '1.0.0', ?)",
        [
            (sid, slug, name, desc, stype, instruction, DEFAULT_TENANT, category)
            for (sid, slug, name, desc, stype, category) in _CONTENT_SKILLS
            for instruction in [desc]
        ],
    )


def _seed_content_tool_templates(connection: Any) -> None:
    """T05：seed ``tl_ai_content_*``(10) + ``tl_ai_content_social_upload``(connector 壳)。"""
    tools = list(_CONTENT_TOOLS) + [CONTENT_SOCIAL_UPLOAD_TOOL]
    connection.executemany(
        "insert or ignore into tool_templates "
        "(tool_template_id, slug, name, description, tool_type, "
        "default_capability_types_json, instruction_excerpt, source, tenant_id, status, version) "
        "values (?, ?, ?, ?, ?, ?, ?, 'official', ?, 'active', '1.0.0')",
        [
            (tid, slug, name, desc, ttype, caps, desc[:240], DEFAULT_TENANT)
            for (tid, slug, name, desc, ttype, caps) in tools
        ],
    )


def _seed_content_employee_templates(connection: Any) -> None:
    """T05：seed ``et_ai_content_*``(12)。"""
    connection.executemany(
        "insert or ignore into employee_templates "
        "(id, slug, name, role, responsibility, description, department_type, "
        "default_instructions, default_capability_types_json, default_model_policy_json, "
        "default_workflow_step_types_json, guardrails_json, source, tenant_id, enabled, "
        "persona_ref, default_skill, default_tool, version, status) "
        "values (?, ?, ?, ?, ?, ?, 'content.growth', ?, '[\"model\",\"tool\"]', "
        "'{\"mode\":\"tenant_default\"}', '[]', '[]', 'official', ?, 1, '', ?, ?, '1.0.0', 'active')",
        [
            (
                eid, slug, name, role, responsibility, description, instructions,
                DEFAULT_TENANT, default_skill, default_tool,
            )
            for (eid, slug, name, role, responsibility, description, default_skill, default_tool) in _CONTENT_EMPLOYEES
            for instructions in [f"按 {role} 职责交付；平台文案遵守品牌语气与合规边界。"]
        ],
    )


def _seed_content_workflow_template_containers(connection: Any) -> None:
    """T05：补 ``wt_ai_content_*``(12) 容器，使已 seed 的 ``wl_ai_content_*`` 引用可解析。"""
    connection.executemany(
        "insert or ignore into workflow_templates "
        "(id, name, description, source, tenant_id, department_type, process_type, "
        "steps_json, status, updated_at) "
        "values (?, ?, ?, 'official', ?, 'content.growth', 'sequential', ?, 'active', current_timestamp)",
        [
            (wid, name, f"{name}（内容增长部工作流容器）。", DEFAULT_TENANT, steps)
            for (wid, name, steps) in _CONTENT_WT_CONTAINERS
        ],
    )


def _seed_department_templates(database: Database) -> None:
    """T04/T06：创建 ``dt_ai_rd`` / ``dt_ai_content`` 部门模板（幂等）。"""
    rd_emps = [e[0] for e in _RD_EMPLOYEES]
    content_emps = [e[0] for e in _CONTENT_EMPLOYEES]
    database.save_department_template(
        id=RD_DEPARTMENT_TEMPLATE[0],
        slug="ai-rd",
        name=RD_DEPARTMENT_TEMPLATE[1],
        department_type=RD_DEPARTMENT_TEMPLATE[2],
        description=RD_DEPARTMENT_TEMPLATE[3],
        default_employee_templates=rd_emps,
        default_workflow_template_id="wt_software_dev_sop",
        tenant_id=DEFAULT_TENANT,
    )
    database.save_department_template(
        id=CONTENT_DEPARTMENT_TEMPLATE[0],
        slug="ai-content",
        name=CONTENT_DEPARTMENT_TEMPLATE[1],
        department_type=CONTENT_DEPARTMENT_TEMPLATE[2],
        description=CONTENT_DEPARTMENT_TEMPLATE[3],
        default_employee_templates=content_emps,
        default_workflow_template_id="wt_content_production_sop",
        tenant_id=DEFAULT_TENANT,
    )


def _seed_company_packages(database: Database) -> None:
    """T06：补 ``ccp_ai_software_company`` 的 workflow_refs；新增 ``ccp_ai_content_company``。"""
    database.save_company_package(
        company_package_id="ccp_ai_software_company",
        name="AI 软件公司出厂包",
        description="研发部出厂配置：dt_ai_rd + 6 个 et_ai_rd_* + 16 条 wl_ai_rd_*，绑定已 seed 的 skl_ai_rd_*/tl_ai_rd_*。",
        version="1.0.0",
        status="active",
        source="Curis internal",
        pack="ai_rd",
        company_template_ref="ct_ai_software_company",
        department_template_refs=["dt_ai_rd"],
        employee_template_refs=[e[0] for e in _RD_EMPLOYEES],
        persona_refs=[],
        skill_refs=RD_SKILL_REFS,
        tool_refs=RD_TOOL_REFS,
        workflow_refs=RD_WORKFLOW_REFS,
        sub_package_refs=[],
        tenant_id=DEFAULT_TENANT,
    )
    database.save_company_package(
        company_package_id="ccp_ai_content_company",
        name="AI 内容公司出厂包",
        description="内容增长部出厂配置：dt_ai_content + 12 个 et_ai_content_* + 12 条 wl_ai_content_* + tl_ai_content_social_upload connector。",
        version="1.0.0",
        status="active",
        source="Curis internal",
        pack="ai_content",
        company_template_ref="ct_ai_content_company",
        department_template_refs=["dt_ai_content"],
        employee_template_refs=[e[0] for e in _CONTENT_EMPLOYEES],
        persona_refs=[],
        skill_refs=CONTENT_SKILL_REFS,
        tool_refs=CONTENT_TOOL_REFS,
        workflow_refs=CONTENT_WORKFLOW_REFS,
        sub_package_refs=[],
        tenant_id=DEFAULT_TENANT,
    )


def seed_wave1(database: Database) -> dict[str, Any]:
    """T04/T05/T06 资产 seed 总入口（幂等，可重复运行）。

    调用前应已 ``database.initialize()``（确保表与既有 rd 资产就位）。
    返回 seed 统计，供验证使用。
    """
    with database.connect() as connection:
        migrated = _migrate_selfuse_tenant(connection)
        _seed_department_types(connection)
        _seed_rd_employee_templates(connection)
        _seed_content_skill_templates(connection)
        _seed_content_tool_templates(connection)
        _seed_content_employee_templates(connection)
        _seed_content_workflow_template_containers(connection)
    # 使用 Database 写助手（幂等 insert or replace）的模板 / 公司包。
    _seed_department_templates(database)
    _seed_company_packages(database)
    return {
        "tenant_migrated_rows": migrated,
        "rd_employees": len(_RD_EMPLOYEES),
        "content_skills": len(_CONTENT_SKILLS),
        "content_tools": len(_CONTENT_TOOLS) + 1,
        "content_employees": len(_CONTENT_EMPLOYEES),
        "content_wt_containers": len(_CONTENT_WT_CONTAINERS),
        "department_types": ["tech.rd", "content.growth"],
        "company_packages": ["ccp_ai_software_company", "ccp_ai_content_company"],
    }
