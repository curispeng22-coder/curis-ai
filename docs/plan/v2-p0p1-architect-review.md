# Curis 资产工厂 V2 · P0/P1 增量独立架构评审报告

> 评审人：高见远（软件架构师）
> 评审日期：2026-07-11（Agent 框架恢复后，B 方案降级执行复核）
> 评审对象：`backend/app/database.py` 增量 + `docs/research/domain/official-tool-catalog-v1.md`
> 参考输入：`docs/plan/v2-p0p1-impl-design.md`、`docs/plan/v2-p0p1-architect-brief.md`
> 评审方式：独立静态审阅（未运行；所有改动尚未 git 提交）
> 结论：**有条件 PASS（Conditional Pass）**

---

## 〇、评审范围与边界确认

需复核的落地增量（均在 `backend/app/database.py` 中，由 `initialize()` 挂载）：

| 增量 | 落点 | 实测数量 | 与 brief 一致 |
|---|---|---|---|
| `tool_templates` 新建 + seed | `_seed_tool_templates`（L1725） | **115** | ✅ |
| `skill_templates` + `version`/`category` 列 + seed | `_ensure_column` L952-953 + `_seed_skill_templates_airnd`（L1886） | **52**（ai_rd Pack A） | ✅ |
| `wt_*` 工作流容器 | `_seed_workflow_template_containers`（L1958） | **16** | ✅ |
| `persona_templates` 形象字段 | `_ensure_column` L950 + `_seed_persona_image_refs`（L2001） | **6** | ✅ |
| `employee_template` CEO 汇报标准注入 | `_seed_employee_templates_phase1`（L2152） | **6**（`et_*`） | ✅ |

✅ 四项数量与 team-lead brief 完全吻合；三份输入文件均存在（`database.py`、`catalog-v1.md`、`impl-design.md` 均在位），CEO 汇报标准引用文档 `docs/ai-development-organization/ceo-reporting-standard.md` 亦存在，无悬空引用。

---

## 一、架构正确性（建表 / seed / 幂等 / schema 漂移）

**结论：建表与 seed 模式稳健，无破坏性迁移，幂等设计基本到位。**

1. **建表幂等**：`tool_templates` 用 `create table if not exists`（L1733），含 `tool_template_id` 主键、`unique(tenant_id, slug)`（L1749）、`source`/`status` 的 `check` 约束、`version`/`created_at`/`updated_at` 默认值——模式合理、具备基本治理约束。✅
2. **Seed 幂等**：全部 seed 用 `insert or ignore`（tool/skill/persona/employee/company_package）或 `on conflict(id) do update`（wt_ 容器，L1988）。可重复 `initialize()` 不重复插入。✅
3. **Additive 列扩展安全**：`version`/`category`（skill）、`image_ref_json`（persona）均经 `_ensure_column`（L1371）添加——该助手先查 `sqlite_master` 再 `pragma table_info` 校验列存在，并把 `current_timestamp` 归一为大写 `CURRENT_TIMESTAMP`（规避 SQLite 常量默认值报错）。无 schema 漂移风险。✅
4. **已知幂等弱点（非阻塞）**：`tool_templates` 的 seed 仅 `insert or ignore`、无 `on conflict do update`——一旦某行被错误 seed，重跑 `initialize()` 不会修正，需手工 migration 覆盖。建议后续对 tool/skill 也改用 `on conflict do update`（与 wt_ 一致），便于纠错。
5. **`(tenant_id, slug)` 唯一约束实测无冲突**：115 条 slug 全唯一（已人工核对：`postgres` vs `postgres_connector`、`docker` vs `docker_run`、`pdf` vs `pdf_parser`、`docx` vs `docx_generator` 均为不同 slug，无撞键）。✅

---

## 二、DB seed 与 catalog 文档一致性

**结论：外部生态部分的 ID/数量可对应，但"全表一一对应"不成立；安全等级未入表导致无法在 DB 层核验。**

### 2.1 数量关系（结构性一致）

| 来源 | 数量 | 是否在 DB | 说明 |
|---|---|---|---|
| ai_rd 执行器（内部） | 30 | ✅ 入表 | **catalog 文档未收录**（文档仅覆盖外部生态） |
| Pack A 外部连接器 | 16 | ✅ 入表 | active |
| Pack C 通用/框架 | 15 | ✅ 入表 | active |
| Pack D 内容公司 | 14 | ✅ 入表 | active |
| Pack E 电商公司 | 12 | ✅ 入表 | active |
| Pack F–J（skill 仓库） | 28 | ✅ 入表 | active |
| **合计 DB** | **115** | — | 30 + 85（A+C+D+E+F+G+H+I+J） |
| Pack B 商业职能 | 12 | ❌ 未入表 | **candidate**，文档明确待二轮 |

- DB 115 = ai_rd 30（DB-only）+ catalog active 85；Pack B 12 为 doc-only candidate。结构自洽。✅
- 85 条 catalog active ID **全部**在 DB 中存在（已逐包核对 A/C/D/E/F/G/H/I/J），无漏 seed、无 ID 错位。✅

### 2.2 非一一对应的两点（须文档澄清）

- **(a) 30 条 ai_rd 工具在 DB 但不在 catalog 文档**：catalog 文档自述"单一真相源"（§二），实际 DB 比文档多 30 条内部执行器。文档该表述对**整表**不成立，仅对"外部生态部分"成立。
- **(b) Pack B 12 条在文档但不在 DB**：符合"candidate 待评估"设计，属预期。

### 2.3 安全等级未入表（关键一致性缺口）

catalog 文档 §七 标注"高等级 21 条"（A 8 + C 3 + E 10），但 `tool_templates` **无任何安全等级列**。因此：
- 安全等级在 DB 层**无法查询、无法过滤、无法驱动最小权限**；运行时若要做高危工具审批/沙箱，必须从 markdown 解析——脆弱且易漂移。
- catalog 文档 §二称"DB 仅存核心列 name/description/tool_type/source/version"——**不准确**：实际列还有 `slug`/`default_capability_types_json`/`instruction_excerpt`/`tenant_id`/`status`/`created_at`/`updated_at`。

### 2.4 语义重叠（建议 QA 确认，疑为有意）

内部执行器与外部 MCP 存在同名能力两份：`tl_postgres`↔`tl_ai_rd_postgres_connector`、`tl_docker`↔`tl_ai_rd_docker_run`、`tl_pdf`↔`tl_ai_rd_pdf_parser`、`tl_docx`↔`tl_ai_rd_docx_generator`。疑为"内部执行器 vs 外部 MCP 连接器"有意区分，但 catalog 文档未收录 ai_rd 侧，故重叠未被文档说明。

### 2.5 小瑕疵

- `tl_desktopcommander`（缺字母 k）在文档与 DB 中拼写一致地错误（真实项目名 DesktopCommander）。仅 cosmetic，但建议修正 slug/name 以免后续集成困惑。

---

## 三、Gate 边界与红线核查

**结论：未触碰硬性红线；但内容/电商工具包 + 内容/商业看板已越出 impl-design 声明的冻结边界，须 L2/总控裁定。**

| 红线 | 核查结果 |
|---|---|
| 真实凭证 | ✅ 无任何凭证列；`source='official'`；catalog 明确"只编目元数据，不接入真实凭证"。 |
| 实例化 | ✅ 仅模板（template）行；未建 `company_instances`/`employee_instances`；content/commercial 无 `company_package`/`employee_template`。 |
| Employee CRUD | ✅ 仅 `insert or ignore` 官方模板 seed，无运行时实例 CRUD。（详见 §四 双模板问题） |
| 多 Agent 生态 | ✅ `tl_agency_agents` 仅作 `agent_framework` 类型工具编目，**未**转换为 Employee（符合 L2 #4 冻结）。 |
| 向量库 | ⚠️ `tl_ai_rd_vector_db_query`/`vector_db_upsert`（`tool_type='vector_search'`）入表——但仅为**模板元数据**，本增量未建任何向量库基础设施。属"元数据描述能力"而非"搭建向量子系统"，建议向 L2 澄清该红线是否涵盖工具模板描述。低危。 |
| 复杂 UI | ✅ 沿用 FastAPI+SQLite，零 UI 新增。 |

### 3.1 ⚠️ 越界落地（须裁定）

impl-design §8.2 明文："内容/商业线（ai_content/ai_commercial）：…`tl_*` 未 seed —— 属暂停四项中的「新商业包」L2 Gate，**本批不动**。"

**但代码实际 seed 了：**
- Pack D 内容公司工具 **14 条** + Pack E 电商公司工具 **12 条**；
- Pack F–J **28 条**中含内容/电商类技能（`ecom_copywriter`、`product_video`、`ecom_video_marketing`、`product_copywriter` 等）；
- `dashboard_templates` 中 **ai_content（3 块）+ ai_commercial（2 块）** 公司型看板（L2256-2296）。

即：本增量把"新商业包"相关的**工具编目 + 公司型看板模板**落了地，超出 impl-design 声明的冻结边界。

**性质判定（非硬红线违规）：**
- 未实例化任何商业公司、未建 Marketplace、未碰收费、未转 Employee、无真实凭证 → **不构成硬性红线突破**。
- 但 catalog 文档 §七「下一步」已自行将 Pack D/E 视为"已 seed"并要求 QA 为"新增 26 条（Pack D/E）写回归测试"——**catalog 文档与代码都越了 impl-design 的界，impl-design 是三者中唯一陈旧的一方**。强烈暗示 B 方案期间总控已口头批准该扩张，但未回填设计文档。

**裁定建议（见结论）：** 须由总控/L2 明确"批准 Pack D/E + 内容/商业看板落地"或"将其拆出单独提交待 Gate"；无论哪种，impl-design §8.2 必须修订以反映真实边界。

---

## 四、关键架构决策评估：`tool_templates` 富字段是否应入表

**问题**：当前 `tool_templates` 仅 core 列，富字段（适用部门/适用员工/需要权限/认证方式/安全等级）放 catalog 文档作单一真相源。是否合理？

**评估：当前决策"有条件合理"，但安全等级应尽早入表。**

- **保留文档为真相源的合理之处**：P0/P1 阶段只是 Admin 官方工具库的**元数据库**，人读、可评审、可版本化；避免对尚在演进的字段过早建表（YAGNI）；降级执行期落地快。
- **不可接受之处（治理缺口）**：**安全等级**是 21 条高危工具的治理关键字段，仅存 markdown 意味着 DB 永远无法驱动最小权限/审批/沙箱——catalog 声称的"高等级均附最小权限"在系统里**不可执行、不可验证**。
- **建议（additive，向后兼容）**：经 `_ensure_column` 增加两列——
  - `security_level text check (security_level in ('high','medium','low'))`；
  - `applicable_departments_json text`（默认 `'[]'`）。
  
  并由 seed 从 catalog 文档回填。这样既不破坏现有 schema，又让最关键治理字段可在 DB 层过滤/校验。**其余富字段（认证方式/需要权限/适用员工）暂留文档即可**，待真正有运行时消费时再扩展，避免过度设计。

> 该扩展为 **P1 改进项**（非 P0 阻断），因为当前没有任何运行时代码消费安全等级；但若后续要做工具绑定/审批，必须先有此列。

---

## 五、其他架构观察

### 5.1 Employee 双模板体系（冗余，P1 清理）
存在两套并存的 6 人研发员工模板：
- `official.employee.*`（`_seed_employee_template_contract`，L1460）：通用指令、**无** CEO 汇报标准、**无** persona/skill/tool 绑定；
- `et_*`（`_seed_employee_templates_phase1`，L2152）：含 CEO 三段式标准 + persona/skill/tool 绑定。

二者代表同一 6 角色，CEO 标准仅存在于 `et_*`。若任何运行路径误用 `official.employee.*`，将缺失 CEO 标准与绑定。旗舰包 `ccp_ai_software_company` 引用 `et_*`（闭环 ✅），但双套并存是架构异味，建议归并或明确"主用 et_*、official.* 为遗留契约基"（impl-design §8.3「P1-2 默认绑定细化」已预见）。

### 5.2 wt_* 闭环
16 个 `wt_*` 容器与 16 个 `wl_ai_rd_*` 引用对齐 → ai_rd 线 0 悬空 ✅。但 20 个 content/commercial `wl_*`（ai_content 11 + ai_commercial 9）引用尚不存在的 `wt_*` → **有意悬空**（冻结），且这些公司型**无** `company_package`/`employee_template` 实例化。旗舰包 `ccp_ai_software_company` 的 `et_/pt_/skl_ai_rd_/tl_ai_rd_/wl_ai_rd_*` 引用全部存在 ✅。

### 5.3 收费体系
本增量**未触碰**任何 billing 表（plans/quotas/billing_events/pricing_rules/quota_rules 系 Phase-8 既有、本次未改）。✅ 但 Phase-8 Billing MVP 与"收费体系暂停"的关系属**既有独立问题**，不在本增量范围，建议总控另行确认其已获批准。

---

## 六、风险与待办

### P0（提交前必须处置）
| # | 项 | 动作 |
|---|---|---|
| P0-1 | **impl-design §7 与 §8.2 陈旧**：§7 写"tool_templates：30"，实际 115；§8.2 冻结声明与实际落地矛盾。 | 修订文档：§7 改为 115；§8.2 修订为"经总控 B 方案批准，Pack D/E + 内容/商业看板已落地；Pack B 仍 candidate"。 |
| P0-2 | **Pack D/E + 内容/商业看板越界落地**的授权状态不明。 | 总控/L2 明确：批准（则 P0-1 文档化即可）/ 或拆出单独提交待 Gate。 |

### P1（应修，非阻断）
| # | 项 | 动作 |
|---|---|---|
| P1-1 | 安全等级/适用部门未入表 | 按 §四 additive 加 `security_level` + `applicable_departments_json` 并回填。 |
| P1-2 | Employee 双模板冗余 | 归并 `official.employee.*` 与 `et_*`，或显式声明主用 `et_*`。 |
| P1-3 | 语义重叠工具未文档化 | 在 catalog 标注 postgres/docker/pdf/docx 内外部双份的差异。 |
| P1-4 | `tl_desktopcommander` 拼写 | 修正 slug/name 拼写。 |
| P1-5 | 向量库工具模板意图 | 向 L2 澄清"向量库"红线是否涵盖工具模板描述（当前仅元数据）。 |
| P1-6 | seed 纠错能力 | tool/skill seed 由 `insert or ignore` 升级为 `on conflict do update`。 |

### 改进项（非缺陷）
- catalog 文档"单一真相源"表述应限定为"外部生态部分"，并补录 ai_rd 30 条内部执行器，消除 doc/DB 口径差。
- 建议为 tool/skill/wt/persona/et 各 seed 增加"非空描述 + 唯一 slug"的自检断言，纳入 Phase-1 QA 套件。

### git 提交 + QA 建议（明确答复）
- **建议 git 单独 Admin 提交**：是。将本增量（database.py 5 处 seed/_ensure_column + catalog 文档）作为**独立 commit**，标题如 `feat(admin): P0/P1 工具/技能/工作流/形象 seed（B 方案复核）`，便于审计 115 条扩张与 Gate 边界。不要与其他改动混批。
- **建议派 QA 写回归测试**：是，且必须在提交前完成。覆盖：
  1. `tool_templates` 计数 == 115，全部 `description` 非空，`(tenant_id, slug)` 唯一；
  2. `skill_templates` Pack A == 52，`version`/`category` 非空；
  3. `wt_*` == 16，且 ai_rd `wl_→wt_*` 悬空 == 0；
  4. `persona_templates` 6 条 `image_ref_json` 已填充；
  5. `et_*` 6 条 `default_instructions` 含《CEO 汇报标准》三段式；
  6. Pack B 12 条**未**入表；
  7. 全库仅 20 个 content/commercial `wl_→wt_*` 为有意悬空（其余 0）。

---

## 七、结论与下一步

### 结论：**有条件 PASS**

- ✅ 无硬性红线突破；建表/seed 幂等稳健、无破坏性迁移；ai_rd 线引用全闭环；CEO 汇报标准已正确注入；agency-agents 仅编目未转 Employee。
- ⚠️ 两项条件须在提交前闭合：
  1. **总控/L2 对"Pack D/E + 内容/商业看板越界落地"的明确裁定**（批准则文档化；否则拆出）；
  2. **修订陈旧的 impl-design §7/§8.2**，使设计文档与真实落地一致（可追溯性闸门要求）。
- 🔧 P1 改进（安全等级入表、双模板归并、文档口径校正、QA 回归测试）建议在本次提交或紧邻提交内完成；其中 **QA 回归测试为提交前置条件**。

### 下一步建议（顺序）
1. **总控/L2**：裁定 Pack D/E + 内容/商业看板（批准 or 拆出）；
2. **修订** `v2-p0p1-impl-design.md` §7（115）、§8.2（真实边界）；
3. **架构师（我）**：落地 P1-1 富字段 additive 列（security_level + applicable_departments_json）并回填；
4. **QA（严过关）**：独立编写并运行 §六所列回归测试，0 失败方可合并；
5. **单独 Admin commit**：以上齐备后，独立提交并标注 B 方案降级执行复核结论。

> 说明：本评审为独立静态审阅，未运行代码。若运行态与静态审阅一致（impl-design §7 自报"fresh temp DB 实测"），上述结论成立；QA 回归测试将最终验证数量/闭环断言。
