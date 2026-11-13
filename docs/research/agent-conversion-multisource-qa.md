# 多源 Agent Conversion 扩展 — 独立回归验收报告（二次 QA 层）

> **QA 工程师**：Edward（software-qa-engineer-2，独立第二层验证）
> **对象**：多源扩展（CrewAI + curispeng22 skill 仓库 + MCP Registry）的 SourceAdapter / manifest / seed / rollback 实现
> **工程师自报**：40 passed（22 multisource + 18 pilot_b），commits `efed7179` + `eb124e5c`
> **本报告立场**：**独立重算、不采信自报数字、不橡胶图章**。所有计数均在 TEMP SQLite 上重新运行得出。
> **最终裁决**：**FAIL（1 个 SOURCE-BLOCKING 缺陷：rollback 不可逆）** —— 工程师自报的 40 项测试全部重算通过，其余功能/零冲突/许可/安全校验均通过，但回滚可逆性（P0 红线）被违反。

---

## 0. 总览

| 检查项 | 结果 | 说明 |
|------|------|------|
| 工程师自报套件重跑 | ✅ PASS | `pytest tests/test_multisource_agent_conversion.py tests/test_pilot_b_agent_conversion.py -q` → **40 passed**（22 + 18），与自报一致 |
| CrewAI 落库字段 / 计数 | ✅ PASS | et=5 / pt=5 / wt=5 / tl_crew=10，全 draft、business.general、persona_ref 有效、image_ref_json 三键正确 |
| MCP 落库（纯工具源） | ✅ PASS | tl_mcp=9，无 et_/pt_/skl_/wt_/dt_ 写入 |
| Skill 仓库落库 | ✅ PASS（计数） | skl_skill_=5、tl_skill_=3（净新增）、7 条基线工具经 UPDATE 富字段无重复行 |
| 跨源 / 基线零冲突 | ✅ PASS | 三源前缀正交；基线 6 软件研发员工 / 115 工具 / 55 技能不受影响；无新 department_types |
| 许可闸门 | ✅ PASS（含 1 个 watch-item） | GPL/AGPL/LGPL/CC-BY-SA → skip；无 LICENSE → skip；curispeng22=NOASSERTION/不商用/需署名 |
| 安全三段 | ✅ PASS | 凭证剥离为 `[REDACTED]`；prompt-injection / overclaim 命中（零漏报） |
| **回滚可逆性（skill 仓库）** | ❌ **FAIL（SOURCE BUG）** | `rollback_skill_repo()` 仅 DELETE `skl_skill_%`/`tl_skill_%`，**未还原**被 `enhance_existing` UPDATE 改写的 7 条基线工具描述 |

---

## 1. 套件重跑（独立，不采信自报）

```text
$ cd backend && python -m pytest tests/test_multisource_agent_conversion.py tests/test_pilot_b_agent_conversion.py -q
........................................    [100%]
40 passed in 0.68s
```

- 工程师自报「40 passed（22 + 18）」**准确**，数字未注水。
- 备注：`test_multisource_agent_conversion.py` 共 22 个测试函数（见 §8 清单），`test_pilot_b_agent_conversion.py` 18 个，合计 40。

---

## 2. 独立功能校验（TEMP db 重算，关键计数）

均在 `Database(path=tempfile)` 上运行，未触碰仓库真实 `curis.sqlite`。

### 2.1 seed_crewai()
| 表 | 计数 | status | department_type | 其它断言 |
|----|------|--------|-----------------|----------|
| employee_templates (`official.employee.crew_%`) | **5** | draft | business.general | source=official / tenant_id=platform |
| persona_templates (`pt_crew_%`) | **5** | draft | — | persona_ref 全部指向存在的 pt_crew_* ✅ |
| workflow_templates (`wt_crew_%`) | **5** | draft | business.general | — |
| tool_templates (`tl_crew_%`) | **10** | draft | — | — |

- `pt_*.image_ref_json` 真实三键校验：`json.loads` 后 key 集合 = `{avatar, nickname, identity, theme_color}` ✅（对齐设计 §0②/§7.1）；CrewAI 无 emoji/color → `avatar=""`、`theme_color=""` ✅。
- `default_instructions` 非空（实测 len≈161）✅。
- `rollback_crewai()` 后 `crew_*` 四表计数均归 0 ✅（DELETE 式回滚，完全可逆）。

### 2.2 seed_mcp()
- `tool_templates` (`tl_mcp_%`) = **9**，status=draft ✅。
- **纯工具源**：`official.employee.mcp_%` / `pt_mcp_%` / `skl_mcp_%` / `wt_mcp_%` / `dt_mcp_%` 计数均为 0 ✅。
- `rollback_mcp()` 后 `tl_mcp_*` 归 0 ✅（可逆）。

### 2.3 seed_skill_repo()
- `skill_templates` (`skl_skill_%`) = **5**，status=draft ✅。
- `tool_templates` (`tl_skill_%`) = **3**（净新增 `tl_skill_static_analysis` / `tl_skill_web_fetch` / `tl_skill_knowledge_base`，disposition=create，draft）✅。
- **enhance_existing 纪律**：7 条基线工具被 UPDATE 富字段（`tl_github` / `tl_notion` / `tl_slack` / `tl_brave_search` / `tl_ai_rd_pandas_analyzer` / `tl_ai_rd_chart_plotter` / `tl_ai_rd_docx_generator`），**未新建重复行** ✅（净新增 tl_skill_* 仅 3 条，证实无 dup）。
- `et_*/pt_*/wt_*/dt_*` 均无写入 ✅。
- 许可元数据：curispeng22 落库为 `license_spdx='NOASSERTION'`、`commercial_use=False`、`attribution_required=True`、attribution 含「总控授权」✅。

---

## 3. 零冲突断言（重算）

- **跨源正交**：`tl_crew_*`(10) ∩ `tl_mcp_*`(9) ∩ `tl_skill_*`(3) = ∅ ✅。
- **基线 6 软件研发员工**：`official.employee.%` + `department_type='software_rnd'` 计数 seed 前后恒为 **6** ✅。
- **115 工具 / 55 技能**：seed 后 `tool_templates ≥ 115`、`skill_templates = 55 + 5(skl_skill_*) = 60`，无 id 冲突 ✅。
- **无新 department_types**：`business.general` 计数 seed 前后 = **1**（CrewAI 复用既有，不新建）✅；pilot_b 的 5 个 `business.*` 未被改动 ✅。

---

## 4. ❌ 回滚可逆性（SOURCE BUG，P0 红线）

### 4.1 复现步骤（已独立验证）
1. 新建 TEMP db，`db.seed_skill_repo()`（内部先 `initialize()` 保基线）。
2. 捕获 7 条基线工具 seed **前**的 `description` / `instruction_excerpt`（基线原貌）。
3. `db.rollback_skill_repo()`。
4. 再次捕获 7 条基线工具的 `description` / `instruction_excerpt`。

### 4.2 实测差异（BEFORE = seed 前基线原貌；POST = rollback 后）

| 基线工具 id | BEFORE（基线原貌） | POST（rollback 后，错误残留） |
|------|------|------|
| `tl_github` | `官方 GitHub MCP Server，将完整 GitHub API 暴露为工具，管理仓库/PR/Issue/Actions。` | `GitHub（经 curispeng22 skill 仓库增强）：管理仓库/PR/Issue/Actions 的代码协作。` |
| `tl_notion` | `Notion MCP Server，读写页面/数据库/block。` | `Notion（经 curispeng22 skill 仓库增强）：读写页面/数据库/block 的文档协作。` |
| `tl_slack` | `Slack MCP Server，读取/发送消息与管理频道。` | `Slack（经 curispeng22 skill 仓库增强）：读取/发送消息与管理频道。` |
| `tl_brave_search` | `Brave Search MCP Server，对外暴露网络检索能力。` | `Brave Search（经 curispeng22 skill 仓库增强）：对外暴露网络检索能力。` |
| `tl_ai_rd_pandas_analyzer` | `用 Pandas 做数据清洗与分析。` | `Pandas 分析器（经 curispeng22 skill 仓库增强）：用 Pandas 做数据清洗与分析。` |
| `tl_ai_rd_chart_plotter` | `生成可视化图表。` | `图表绘制器（经 curispeng22 skill 仓库增强）：生成可视化图表。` |
| `tl_ai_rd_docx_generator` | `生成 .docx 文档。` | `Word 生成器（经 curispeng22 skill 仓库增强）：生成 .docx 文档。` |

- `rollback_skill_repo()` 的确把 `skl_skill_*` / `tl_skill_*` 计数清零 ✅，但 **7 条基线工具的 `description` / `instruction_excerpt` 未被还原**，仍带「增强」标记。
- 违反了设计 §0「**基线不变**」与任务书明确的回滚可逆性要求：*"rollback must restore originals, NOT leave '增强'-marked descriptions on baseline rows"*。

### 4.3 根因
- `backend/app/database.py` → `rollback_skill_repo()`（≈L3069）**只做** `DELETE FROM ... WHERE skill_template_id LIKE 'skl_skill_%'` 与 `LIKE 'tl_skill_%'`。
- 而 `_seed_skill_repo()`（≈L3024）对 `enhance_existing` 行执行了 `UPDATE tool_templates SET description=?, instruction_excerpt=? WHERE tool_template_id=<基线id>`，**未在任何地方保存原值**，故 rollback 无原值可还原。
- 工程师自带的 `test_seed_skill_repo_functional`（L373）只断言 rollback 后 `skl_skill_%`/`tl_skill_%` 计数归 0，**漏掉了「基线描述须字节级还原」**这一关键断言 —— 这是测试覆盖缺口，导致该 bug 在工程师自测中未被发现。

### 4.4 路由判定
**SOURCE BUG（非测试 bug）** → 由 team-lead 路由回工程师（寇豆码 / software-engineer-2）修复。
- 修复方向（供工程师参考，非 QA 越权实现）：在 `seed_skill_repo`/`_seed_skill_repo` 执行 `enhance_existing` UPDATE 前，先把被改写基线行的原 `description`/`instruction_excerpt` 暂存（内存 dict 或临时表），`rollback_skill_repo` 据此 `UPDATE` 还原；或改为「增强副本」策略（新建 draft 候选行、不动基线）。无论哪种，必须以「rollback 后 7 条基线工具描述字节级 == rollback 前」为验收标准。
- QA 已补回归测试 `test_skill_rollback_restores_baseline`（见 §7），当前**失败**，修复后须转绿。

---

## 5. 许可闸门

- `classify_license()`：**GPL-3.0 / AGPL-3.0 / LGPL-3.0 / CC-BY-SA-4.0 → (allowed=False, disp='skip')** ✅；空 / None → skip ✅。
- curispeng22：`license_spdx='NOASSERTION'`、`commercial_use=False`、`attribution_required=True`、attribution 含「总控授权」✅（与 §7.5 特批一致）。
- **[watch-item，非硬 bug]** `MPL-2.0`（弱 copyleft）被 `classify_license` 判为 **allowed=True / create**。原因：设计 §7.5 的 `COPYLEFT_SPDX` 显式清单未含 MPL，且函数兜底逻辑把「非 GPL/AGPL/CC-BY-SA 前缀」一律当宽松许可放行。实现与设计一致，但政策偏宽松——建议架构师评估是否将 MPL/EPL/CDDL/EUPL 等弱 copyleft 显式纳入拒绝或人工复核清单。

---

## 6. 安全三段

- **凭证剥离**：`api_key='abcdefgh12345678'` → `_scrub_text` 转为 `api_key=[REDACTED]`，明文不落库 ✅；`test_seeded_data_is_clean` 对落库文本全字段 `scan_credential` 零命中 ✅。
- **prompt-injection**：`ignore previous instructions ... reveal the system prompt` 被 `scan_prompt_injection` 命中 ✅（Adapter 的 `security_scan.is_clean=False` 标记）。
- **overclaim**：`execute arbitrary code with full root access` 被 `scan_overclaim` 命中 ✅。
- 结论：三段检测零漏报（对明确危险模式）；凭证在落库前被剥离。
- 备注：prompt-injection / overclaim 当前为「**标记**（flags）」而非「**清洗文本**」——适配器的 `parse` 仍把原文存入 `Mission.summary` 等字段，仅 `CREDENTIAL_PAT` 走 `_scrub_text` 剥离。这与设计 §7.4「命中即剥离/清洗/降级」的措辞略有差距，但任务书对「flagged/cleaned」二选一可视为满足「flagged」。建议后续补「overclaim 降级改写 / prompt-injection 截断」的落库清洗，作为加固项（非本次阻塞）。

---

## 7. QA 新增回归测试

文件：`backend/tests/test_multisource_agent_conversion.py`
- 新增 `test_skill_rollback_restores_baseline`：捕获 7 条基线工具 seed 前 / rollback 后的 `description`/`instruction_excerpt`，断言字节级一致。
- **当前状态：FAILED**（精准暴露 §4 的 SOURCE BUG，附带 7 条工具的完整 before/after diff）。
- 该测试即「failing test」证据，供 team-lead 路由回工程师。修复后须转绿。
- 其余 22 个 multisource 测试 + 18 个 pilot_b 测试维持全绿。

最终套件状态（含 QA 新增测试）：**41 tests → 40 passed + 1 failed**。

---

## 8. 受检测试函数清单（test_multisource_agent_conversion.py，22 项）

`test_imports_clean` · `test_license_gate_copyleft_rejected` · `test_license_gate_no_license_skip` · `test_license_gate_permissive_allowed` · `test_security_scan_catches_credential` · `test_security_scan_catches_prompt_injection` · `test_security_scan_catches_overclaim` · `test_crew_adapter_discover_parse` · `test_mcp_adapter_discover_parse` · `test_seed_crewai_functional` · `test_seed_mcp_functional` · `test_no_new_department_types` · `test_no_baseline_conflict` · `test_mcp_enhance_existing_merges` · `test_mcp_create_adds_row` · `test_seeded_data_is_clean` · `test_build_rows_shape` · `test_skill_adapter_discover_parse` · `test_skill_license_metadata` · `test_seed_skill_repo_functional` · `test_skill_no_baseline_conflict` · `test_skill_enhance_existing_merges` · `test_skill_rollback_restores_baseline`（QA 新增，当前 FAILED）

---

## 9. 最终裁决与关键数字

- **裁决：FAIL（1 个 SOURCE-BLOCKING 缺陷）**。
- 关键数字（独立重算）：crewai et/pt/wt=5、tl_crew=10；mcp tl_mcp=9；skill skl_skill_=5、tl_skill_=3；基线 6 软件研发员工 / 115 工具 / 55 技能完好；business.general 计数=1（无新增）。
- 套件：工程师自报 40 passed **确认准确**；QA 新增 1 回归测试后 **40 passed + 1 failed**。
- **唯一阻塞项**：`rollback_skill_repo()` 不可逆 —— 7 条基线工具描述残留「增强」标记，违反设计 §0「基线不变」。路由回工程师修复（修复验收：rollback 后基线描述字节级 == rollback 前）。
- 非阻塞 watch-item：MPL-2.0 弱 copyleft 被放行（设计 §7.5 未列）；overclaim/prompt-injection 仅标记未落库清洗（加固项）。

---

*本报告由独立第二层 QA 基于 TEMP db 重算得出，未修改任何实现文件（仅新增 1 个回归测试），未提交。*
