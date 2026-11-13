# Agent 拆解转换引擎 V1 — 多源扩展研究与适配评估

> **文档性质**：产品研究 + 适配评估（pre-gate 设计稿，**不实现、不 seed**）
> **作者**：产品经理 许清楚（software-product-manager）
> **上游**：`agent-conversion-engine-v1-report.md`（章节 5 多源章节）/ `agent-conversion-engine-v1-design.md`（4.1 CanonicalAgentSpec、4.2 SourceAdapter ABC、4.3 字段映射）
> **前置裁定（已生效）**：总控已明确**解冻 L2 暂停四项 #4 的解冻范围**——受控试点 B 原为单源（agency-agents），现**授权扩展到多源**（CrewAI / curispeng22-coder/skill / Coze-Dify / MCP Registry / AutoGPT 等范式 2–6）。本文件在试点 B 方法论基础上评估多源扩展。
> **红线**：仅研究 + 评估，不写实现代码、不 seed 真实资产；不接入凭证、不建 marketplace、不 instantiation（ADR-0017 仍锁 Instance/Runtime）。

---

## 0. 评估方法与维度

沿用试点 B 已验证的 `SourceAdapter` 范式：**每个来源实现一套适配器，把异构源归一为 `CanonicalAgentSpec`，再共享同一映射流水线（章节 3 关卡①–⑧）**。本研究的评估维度：

| 维度 | 含义 | 对纳入决策的影响 |
|------|------|------|
| 形态 | 源的物理表达（.md / YAML / JSON / 仓库） | 决定 `discover/fetch/parse` 入口差异 |
| 结构化能力 | 能力是否以显式字段存在（tools/goal/skills） | 高结构化→映射损耗低、无需 NLP 抽取 |
| 保真度 | 对 Curis 资产（et_*/pt_*/skl_*/tl_*/wt_*/dt_*）映射损耗 | 高保真源优先纳入 |
| 适配差异 | 相对 agency-agents（范式 1）的解析差异 | 决定新增 Adapter 的复杂度 |
| 许可风险 | SPDX 是否可商用、是否 copyleft、是否无 LICENSE | 关卡①前置过滤；无 LICENSE=默认保留所有权利 |
| 与 Pack F-J 重叠度 | 与已入库 28 条（source=skill 仓库）的重合 | 重合项判"增强而非新建" |

> 评估范围：规划稿章节 5.2 的 6 种来源 + 1 个可选索引源，共 6 类评估对象（含试点已落地的范式 1 作基线对照）。

---

## 1. 逐源评估

### ① CrewAI YAML（范式 3 → `CrewYamlAdapter`）

| 维度 | 评估 |
|------|------|
| 形态 | YAML 定义 `crew` / `agent` / `task`；单个 agent 含 `role`、`goal`、`backstory`、`tools`（具名列表）、`llm`；task 含 `description`、`expected_output`、`agent`、`context`。 |
| 结构化能力 | **是**。`role/goal/backstory/tools` 均为显式字段，无需自然语言抽取。 |
| 保真度 | **高**。`role→identity.role`、`goal→mission.summary`、`backstory→default_instructions`、`tools`（具名）→`capability_candidates` 直接命中现有 `tl_*` 或生成 `tl_*` candidate、`task→workflow.steps`。映射损耗显著低于 agency-agents（范式 1 需 NLP 抽取）。 |
| 适配差异 | `discover` 遍历 crew/agents YAML；`parse` 直读 YAML 字段（结构化，无需章节切分）；`tools` 已是具名列表→直接进 `tl_*` 命中匹配；**可跳过 `extract_capabilities` 的 NLP 抽取**（结构化源特征）。emoji/color 通常缺失→留空或按 division 派生。 |
| 许可风险 | CrewAI 框架 MIT；社区 crew 示例许可混杂（多为 MIT/Apache-2.0，个别含私有内容）。关卡①须逐仓库扫 SPDX；`Apache-2.0` 须保留 `NOTICE`。 |
| 与 Pack F-J 重叠 | 低。CrewAI 多为研发/通用 agent，与 curispeng22（skill 仓库）无重叠；与 6 官方员工/115 工具低重叠。 |
| **纳入判断** | ✅ **纳入首批**。结构化最高保真、映射损耗最低、与现有资产互补。 |

### ② curispeng22-coder/skill（范式 2 → `SkillRepoAdapter`）

| 维度 | 评估 |
|------|------|
| 形态 | 结构化 skill 仓库：每个 skill 一个目录（含 `SKILL.md` + 描述 + 可执行步骤/工具依赖）。本质是**方法论/手艺型 know-how** 集合。 |
| 结构化能力 | **是**。每个 skill 有 `name` / `description` / `steps`，部分引用具体工具（pptx/xlsx 等）。 |
| 保真度 | **高**（近 `skl_*` 形态）。`skill→skl_*`（`default_capability_types_json=['model']`）；skill 引用的具体工具→命中已有 `tl_*` 或新 `tl_*` candidate。 |
| 适配差异 | `discover` 遍历 skill 目录（`SKILL.md`）；`parse` 读 frontmatter/章节→`skill_candidates`；含工具引用者→`tl_*`。多数已是 `skl_*` 形态，无需 NLP 抽取。 |
| 许可风险 | ⚠️ **关键风险**：curispeng22-coder/skill 是**个人 GitHub 仓库**，多数无明确 `LICENSE` 文件（默认 all rights reserved），不自动授予 harvest 权。虽 catalog 已部分入库 28 条（Pack F-J），但**规模化 harvest 前必须确认许可 / 取得授权**——这是纳入首批的 **blocker 级待确认项**。 |
| 与 Pack F-J 重叠 | **已部分入库（28 条）**。Pack F(4)+G(4)+H(6)+I(8)+J(6)=28 条 `tl_*`（来源标注"skill 仓库"）已在 `tool_templates`。本源 harvest 的处置逻辑见 §3。 |
| **纳入判断** | ✅ **纳入首批**（高保真 + 已验证价值），但**许可确认 + 重叠去重**是前置 gate；首刀以"增强 28 条 `tl_*` + 抽 `skl_*` 方法论"为主，净新增最小化。 |

### ③ Coze / Dify 导出（范式 5 → `PlatformExportAdapter`）

| 维度 | 评估 |
|------|------|
| 形态 | 可视化 bot 导出的 JSON DSL（Coze `bot.json` / Dify `app` DSL）。含 `nodes`（大模型/知识库/代码/工作流节点）、`plugins`（插件=工具）、`prompt`、`variables`、记忆配置。 |
| 结构化能力 | **是**。`nodes/plugins/prompt` 均为结构化字段。 |
| 保真度 | **中高**。`bot prompt→default_instructions/mission`、`workflow nodes→wt_*.steps_json`、`plugins→tl_*` 命中；但平台私有字段（Coze 变量/记忆/UI 配置）须剥离，存在 schema 噪声。 |
| 适配差异 | `discover` 读导出 JSON 文件；`parse` 解析 `nodes/plugins/prompt`；多节点工作流→`wt_*`（owner_role 按节点归属）；须剥离平台私有 schema（metadata/version/ui）。 |
| 许可风险 | ⚠️ **中高**。bot 是用户/第三方创作 IP；从平台"导出再 harvest"可能违反平台 ToS（尤其市场 bot、他人 bot）。仅允许导入**用户自有 bot**且须用户授权；marketplace bot 一律不纳入。 |
| 与 Pack F-J 重叠 | 中。Coze/Dify 的 plugins 与 Curis 115 工具（尤其 Pack A MCP、Pack B HubSpot 等）存在命中→须 `enhance_existing` 去重。 |
| **纳入判断** | ⏸ **暂缓（不纳入首批）**。价值中高，但 ToS/许可模糊 + 平台私有 schema 剥离成本高；建议作 P1 批次（用户自有 bot 导入试点）。 |

### ④ MCP Registry（范式 6 → `MCPManifestAdapter`）

| 维度 | 评估 |
|------|------|
| 形态 | MCP server manifest：每个 server 声明 `tools` / `resources` / `prompts`，tool 带 `input_schema`（JSON Schema 化）。 |
| 结构化能力 | **是（高）**。tool 有结构化 `input_schema`，是最"干净"的工具定义源。 |
| 保真度 | **高（工具侧）**。server→`tl_*`；单个 server 的多 tool 可拆为多个 `tl_*` 或聚合为一个 `tl_*` candidate；`input_schema→description/instruction_excerpt`。**无员工/人格概念**（server 无 role）→`et_*`/`skl_*`/`pt_*` 几乎不产出，是**纯工具源**。 |
| 适配差异 | `discover` 读 registry/manifest JSON；`parse` 把每个 server 的 tools 映射为 `tl_*` candidate；缺失 `mission/persona/workflow`→这些字段留缺省。 |
| 许可风险 | 低-中。官方 MCP 示例多为 MIT；社区 server 许可混杂（Apache/BSD/个别无许可）。与 catalog 已 seed 的 MCP 工具（github/gitlab/postgres 等）高度重叠→须 `enhance_existing`。 |
| 与 Pack F-J 重叠 | 中高（与 Pack A/C 已 seed 的 MCP 工具重叠）。主要处置=补全 + 增强现有 `tl_*`，而非净新建。 |
| **纳入判断** | ✅ **纳入首批**。纯工具源、高保真、天然延续 catalog 的 MCP 线；以"补全 + 增强现有 `tl_*`"为主。 |

### ⑤ AutoGPT / AgentKit（范式 4 → `AgentConfigAdapter`）

| 维度 | 评估 |
|------|------|
| 形态 | JSON/YAML agent 配置（AutoGPT `agent_config`：`name`/`role`/`goals`/`constraints`/`tools`；AgentKit：`agents`/`tools`）。 |
| 结构化能力 | **是**。`tools` 带 schema。 |
| 保真度 | **高**。`role/goals/constraints→et_*`（`goals[]→mission.responsibilities`、`constraints[]→guardrails_json`）；`tools→tl_*`；但 AutoGPT 配置碎片化（`goals` 是字符串数组）需归并。 |
| 适配差异 | `parse` AutoGPT 的 `goals[]`/`constraints[]`→`mission`/`guardrails`；`tools→tl_*`。**与 CrewAI 范式高度重叠**（都是"角色+目标+工具"）。 |
| 许可风险 | AutoGPT 框架 MIT；agent 配置许可混杂。 |
| 与 Pack F-J 重叠 | 低（与 CrewAI 重叠高，与 Curis 资产低重叠）。 |
| **纳入判断** | ⏸ **暂缓（不纳入首批）**。与 CrewAI 范式重叠、边际价值低；建议作 P2，或"若 CrewAI 验证良好则复用 `AgentConfigAdapter` 补刀"。 |

### ⑥ GitHub Trending / Awesome（可选索引源 → 不纳入）

| 维度 | 评估 |
|------|------|
| 形态 | Trending=榜单（仅链接，无内容）；Awesome=README 列表（链接聚合）。 |
| 结构化能力 | **否**（仅索引，无角色定义）。 |
| 保真度 | **低**（无 agent 内容）。 |
| 适配差异 | 无实际 adapter 价值——trending 仅是"去哪里找源"的索引。 |
| 许可风险 | ⚠️ Awesome 列表多为 **CC-BY-SA（copyleft）**→按关卡①直接拒绝 harvest 其文本。 |
| **纳入判断** | ❌ **不纳入 harvest 源**。仅作为"源发现索引"使用（规划稿章节 1 已用 trending 发现 agency-agents 等），不作为转换源。 |

---

## 2. 纳入判断汇总

| # | 源 | 适配器 | 纳入判断 | 主要理由 |
|---|------|------|------|------|
| ① | CrewAI YAML | `CrewYamlAdapter` | ✅ **首批** | 最高保真、结构化、零 NLP 损耗、互补 |
| ② | curispeng22-coder/skill | `SkillRepoAdapter` | ✅ **首批**（许可 gate） | 高保真 + 已验证；须许可确认 + 重叠去重 |
| ③ | Coze / Dify 导出 | `PlatformExportAdapter` | ⏸ **暂缓** | ToS/许可模糊 + 私有 schema 剥离成本高 |
| ④ | MCP Registry | `MCPManifestAdapter` | ✅ **首批** | 纯工具源高保真、延续 catalog MCP 线 |
| ⑤ | AutoGPT / AgentKit | `AgentConfigAdapter` | ⏸ **暂缓** | 与 CrewAI 重叠、边际价值低 |
| ⑥ | GitHub Trending/Awesome | —（仅索引） | ❌ **不纳入** | 无内容、Awesome 为 copyleft |

**首批推荐组合**：① CrewAI + ② curispeng22-coder/skill + ④ MCP Registry（3 源）；③ Coze/Dify 作 P1；⑤ AutoGPT 作 P2；⑥ 仅索引。

---

## 3. 与 Pack F-J 28 条的重叠度分析（curispeng22 已部分入库）

catalog `official-tool-catalog-v1.md` 的 Pack F-J 共 **28 条 `tl_*`**（来源标注"skill 仓库"），已在 `tool_templates` 入册。在 multisource harvest 本源时，它们**不应再被新建**，而是按以下处置：

| Pack | 条目（已入 `tl_*`） | harvest 处置 |
|------|------|------|
| F 办公文档(4) | pptx / xlsx / pdf / docx | `enhance_existing`：用 SKILL.md 更丰富的步骤/证据补全 `description`/`instruction_excerpt`/`source_attribution`；不新建 |
| G 产品+设计(4) | product_manager_toolkit / ai_drawio / frontend_design / nanobanana_ppt | `enhance_existing` 同上 |
| H 内容创作(6) | content_publisher / article_illustrator / url_to_markdown / format_markdown / post_to_x / xhs_images | `enhance_existing` 同上 |
| I 视频语音(8) | video_suite / video_collaborator / video_recreation / video_frame_extractor / viral_video_copy / tts_voice / qwen_asr / infinitetalk | `enhance_existing` 同上 |
| J 电商法务(6) | ecom_copywriter / ecom_video_marketing / product_copywriter / product_video / paper_analysis / contract_review | `enhance_existing` 同上 |

**关键发现**：catalog 把 skill 仓库的 28 条**全部当 `tl_*`（工具）存**，但 skill 仓库本质是**方法论（skl_*）**。因此在 harvest 本源时产生两层价值：

1. **增强现有 28 条 `tl_*`**（enhance_existing，不新建）：用 SKILL.md 原文补全富字段。
2. **抽 `skl_*` 方法论资产（净新增）**：每个 skill 的"方法/步骤/手艺"应另建 `skl_*`（如 `skl_video_recreation`、`skl_contract_review`），与已存的 `tl_*` 形成"工具+方法论"配对。这是本源对 Curis 资产的**净新增贡献**，也是与 Pack F-J 的最大差异点。
3. **净新增 `tl_*`**：仓库中超出 28 条的 skill 所引用的新工具（需读 repo 精确判定，预估还有若干未覆盖工具）。

> 精确"28 条之外还剩多少 skill、能抽多少 `skl_*`"需在实现前置阶段读 `curispeng22-coder/skill` 仓库树得出确定性清单（本研究不越红线读源写资产，仅给出处置框架）。

---

## 4. 复用 `SourceAdapter` 范式的适配器清单

| 源 | 适配器类名 | 解析入口差异（vs 范式 1） | 主要产出资产 | 状态 |
|------|------|------|------|------|
| agency-agents | `AgencyMarkdownAdapter`（已落地） | `.md` frontmatter + `##` 章节切分 + NLP 抽能力 | `et_*/pt_*/skl_*/tl_*/wt_*/dt_*` | ✅ 试点 B 已交付 |
| ① CrewAI | `CrewYamlAdapter` | `.yaml` 直读 `role/goal/backstory/tools`；结构化无需 NLP 抽取 | `et_*/tl_*/wt_*` | 待实现 |
| ② curispeng22 | `SkillRepoAdapter` | 遍历 `SKILL.md` 目录；skill→`skl_*`、工具引用→`tl_*` | `skl_*/tl_*`（增强+净新增） | 待实现 |
| ③ Coze/Dify | `PlatformExportAdapter` | 读 bot DSL JSON；`nodes/plugins` 解析 + 私有字段剥离 | `wt_*/tl_*/et_*` | 暂缓 |
| ④ MCP Registry | `MCPManifestAdapter` | 读 server manifest JSON；`tools→tl_*`（纯工具源） | `tl_*` | 待实现 |
| ⑤ AutoGPT | `AgentConfigAdapter` | 读 agent config JSON；`goals/constraints/tools` 归并 | `et_*/tl_*` | 暂缓 |

**共性复用**：所有新 Adapter 继承同一 `SourceAdapter` ABC（`discover/fetch/parse/extract_capabilities/get_metadata`），输出同一 `CanonicalAgentSpec`，复用既有 `canonical.py` / `sanitize.py`（emoji/color 清洗）/ `security_scan.py`（三段正则）/ `adapter_base.py`。仅**新增 Adapter 文件 + 每源 manifest/seed 函数（opt-in）**，不改动试点 B 已落地代码。

---

## 5. 风险与治理（延续试点 B）

| 风险 | 处置（沿用试点 B） |
|------|------|
| 许可合规 | 关卡①逐源扫 SPDX；`copyleft`（GPL/AGPL/CC-BY-SA）拒绝 harvest；`Apache-2.0` 保留 NOTICE；**无 LICENSE 的个人仓库（curispeng22）须先确认授权再 harvest**。 |
| 安全三段 | `security_scan.py` 三段正则（credential / prompt-injection / overclaim）零漏报；模板永不持久化凭证。 |
| candidate vs active | 真实 DDL `skill_templates`/`tool_templates` 的 `status` CHECK **不含 `'candidate'`**（试点 B 评审已勘误）→ 统一用 `'draft'`（全部未激活、可回滚）。 |
| 命名冲突 | 每源用**不同 id 前缀**（`crew_` / `skill_` / `mcp_`）+ 入库前与 6 官方员工/115 工具/55 技能冲突校验，保证零冲突。 |
| 回滚 | 每源独立 opt-in seed 函数 + 独立回滚函数（按 id 前缀范围 `DELETE`），不挂默认 `initialize()`。 |

---

## 6. 约束遵守声明

- ✅ 本文**仅研究 + 适配评估**，无任何实现逻辑代码。
- ✅ **未 seed、未修改** 任何真实资产表 / `database.py`；仅对齐既有 schema 与 catalog。
- ✅ 未触碰 L2 红线：不接凭证、不建 marketplace、不 instantiation；所有结论为 draft/设计态。
- ✅ 所有映射假设严格对齐试点 B 已核实的真实 DDL（8 处偏差见 PRD 附 B）。

*研究完。后续产出见 `docs/plan/agent-conversion-multisource-prd.md`（范围建议 + 验收定义）。*
