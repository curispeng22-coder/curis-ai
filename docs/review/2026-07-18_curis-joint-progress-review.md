# Curis 联合开发进度复盘报告（2026-07-18）

> 参与方：Codex（Workspace 运行时）/ WorkBuddy（Admin 资产工厂）
> 对象：《2026-07-17 Curis 联合开发基线与自主推进计划》
> 方法：**只读核验**（代码 blob / 数据库 / API / 测试实跑 / E2E 证据），判定标准＝真实代码·数据·测试·E2E ＞ 契约与规划文档
> 核验基线：`Admin` 分支 HEAD `72186d58`（PR #2 已合入，main.py blob `0fa34bc6`、database.py blob `0d36c4df`）；测试实跑于后端干净环境
> 结论先行：R1/R2 完成，R3 纵向链路跑通但 115 个 Tool 全 mock/stub（真实 Tool 执行=空壳），R4 仅边界/契约收口且独立代码审计仍 OPEN。

---

## 0. TL;DR（一句话结论）

R1/R2 已真实完成并合入；R3「软件公司包→…→Token/成本」纵向链路已端到端跑通且产生真实模型调用与成本凭证，但 **Tool 真实执行能力是空壳（115 个 Tool 全 mock/stub）**；R4 大量项停留在边界/契约/Gate 收口层，真实可用能力有限。下一轮只补边界内三件事，L2 四项全暂停待总控解锁。

---

## 1. 第一至第四轮完成度

| 轮次 | 范围 | 判定 | 说明 |
|---|---|---|---|
| **R1** 统一运行基线 | Admin 可自主 8 项 | ✅ 完成 | 随 PR #2 合入 `72186d58`，双 lead PASS |
| **R2** 资产与实例化断点 | Admin 主导 9 项 + 孤儿实例 | ✅ 完成 | 18/2 孤儿实例改由 Workspace 处置并共享 VERIFIED/CLOSED |
| **R3** 真实纵向执行链路 | Codex 主导 7 步 | 🟡 部分完成 | 链路跑通、真实模型调用+成本凭证齐全；**115 Tool 全 mock/stub，真实 Tool 执行=空壳** |
| **R4** 长期运行能力 | 基线 §七 9 项 | 🟡 部分完成 | 第 1–7 项有代码但独立代码构造审计仍 OPEN；第 3 项仅边界定义；第 8/9 项仅边界/契约收口（未实现，触 L2） |

**逐 item 状态**（详见第 2 节证据）：
- R1.1–R1.8：全完成（含 R1.8 弱令牌修复 `d7c0b21`）。
- R2.1–R2.9：全完成（含 `wl_*`→`wt_*` 修正、6 只读 Catalog 路由、Tool/Workflow 能力态标注、资产完成度标准 094）。
- R3.1/R3.2/R3.4/R3.6/R3.7/R3.8：完成；R3.3/R3.5：**部分**（绑定层成立，但真实 Tool 执行为空壳）。
- R4.1–R4.7：有代码/边界+最小实现，但 `items_1_7_code_construction_audit_gate.md` 仍 OPEN；R4.3 仅边界；R4.8/R4.9 仅边界/契约。

---

## 2. 每项真实证据（commit / API / 数据库 / 测试 / E2E）

### R1 / R2（Admin 侧，已合入 `72186d58`）
- **Commit**：PR #2 `72186d58`；令牌修复 `d7c0b21`；093 实现 `f6e020e8`（经 cherry-pick）；能力态种子 `019217d`；测试 `d9157c9`；main.py blob `0fa34bc6`、database.py blob `0d36c4df`。
- **API（main.py 实测存在）**：
  - 令牌门禁 `_require_platform_admin`（main.py:1913）：未配置→401「Admin token not configured」；错令牌→401；`ADMIN_STRICT=true` 未配置→`create_app` 抛 RuntimeError 拒启动（main.py:773/781-785/3053）。
  - 6 条只读 Catalog GET：`/api/platform/{personas,dashboards,company-packages,company-templates,tools,workflows}`（main.py:1993/2006/2019/2056/2062/2068），均经门禁后返回真实 DB 投影（底层 `_list_catalog_rows` 真实 SELECT，非 stub）。
  - Workspace 融合：`identity_membership`/`resource_scope_policy`/`tenant_context` 三件套已在 main.py 导入+实例化+中间件注册（main.py:73/79/81/764/766/1028/1038）。
- **数据库（disk 只读 SELECT 核实）**：
  - `tool_templates` 115 行全部 `(catalog_visible=1, configured=0, executable=0, mock_or_stub=1)`；`workflow_templates` 18 行（16 `design_only` + 2 `structured_executable`）。能力态列经 `_ensure_column` 幂等加列（database.py:1627）。
  - 种子标注由 `_annotate_tool_capability`/`_annotate_workflow_capability` 真实调用，且显式「不伪造真实执行」——诚实声明。
- **测试（QA 实跑）**：`backend/` 下 `.venv` 环境 **16 passed / 0 failed**（令牌 4 + 实例化证据 7 + 093 路由 5），环境干净、未 pop stash。

### R3（Codex 主导，Admin 配合）
- **E2E 真实验证（091 VERIFIED/CLOSED）**：真实 HTTP 实例化 `ccp_ai_software_company` → Company `company-eefb53b2-…`、Dept 1 / Employees 6 / Workflow Instances 6 / Snapshots 13，`unresolved_refs` 三项全空；6 条 `wl_*` 均解析到真实 `wt_*`；`sub_package_refs=["cp_content_ops"]`、`connector_ids=[]`。
- **E2E 真实模型调用（R3 AI 研发部纵向链路 PASS）**：Run `wfr-33a17cee-…`，7 Step 全 succeeded；**真实 9,622 tokens / USD 0.01326900** / 模型 `gpt-5.4-mini-2026-03-17` / `final_report` 6,018B（SHA-256 `2d14cf90…`）。QA 内部复算 7 步 token 累加=9,622、成本=0.013269，自洽。
- **空壳证据**：115 Tool 全 `executable=0/mock_or_stub=1`，`real_model_gate` 实测 `official_models=0/model_gateways=0/有效能力绑定=0` → 真实执行仅 1 条模型网关调用，无真实 Tool 执行。

### R4（长期能力）
- 第 1–7 项：`r4_project_long_term_state_and_memory_gate` 等 Gate 已建并 PASS，但独立代码构造审计 `items_1_7_code_construction_audit_gate.md` **仍 OPEN**（"不以旧文档 PASS 替代实际代码核对"）。
- 第 3 项：`Agent/Workflow/Hybrid Mode` 已拆分为边界定义 Issue，**未实现**。
- 第 8/9 项：`r4_ai_secretary_closeout_gate` / `r4_team_migration_closeout_gate` PASS，但**仅只读边界/契约收口，未实现功能**（触 L2）。

---

## 3. 仍存在哪些断点、空壳或假完成

1. **🔴 Tool 真实执行 = 空壳（最重要）**：115 Tool 全 `mock_or_stub=1`，R3 真实执行仅 1 条模型网关调用，无任何真实 Tool 适配。属 R3.3/R3.5 的「部分完成」根因。
2. **🟡 R4 真实能力有限**：第 3 项（Agent/Workflow/Hybrid）仅边界定义；第 8/9 项（AI 秘书/团队迁移）仅边界/契约，未实现（触 L2）。
3. **🟡 R4 独立代码审计 OPEN**：`items_1_7_code_construction_audit_gate.md` 未闭合，"Gate PASS" 尚未被独立代码核对坐实，存在虚高风险。
4. **🟡 `workflow_instances=6` 与磁盘 DB 实测不符**：架构师核验 `data/admin.sqlite=0`、`data/curis.sqlite=0`、`data/workspace.sqlite=1`、根 `curis.sqlite=29`，**无候选库为 6**。原因：091 的"6"是某次 E2E 运行的瞬时结果（测试用临时 DB、R3 Run 写入 workspace.sqlite），非当前持久化状态——属**数据/声明口径需澄清**，非代码层假完成（代码未硬编码 6）。
5. **🟡 状态不同步**：`issues/shared/20260717_admin_r3_e2e_handoff.md` 仍 OPEN，而 Workspace 侧 `issues/20260717_workspace_r3_ai_rd_vertical_e2e.md` 已 PASS/CLOSED；R3 review 自述「未跑全量回归」，其自身验收标准的"无 R3 新增失败"条款未被覆盖。
6. **🟡 术语口径偏差**：任务描述"093 = 6 路由"，实际 `test_issue093_readonly_catalog_routes.py` 覆盖 4 路由，另 2 路由在 `test_r2_instantiation_evidence.py` 的 `test_six_catalog_routes_regression`——非测试缺口，属文档/口径不一致。

> 未发现有「只在文档里没真跑」的测试，也未发现「只有关键字无数据」的 E2E；上述均为真实证据层面的断点或收口缺口。

---

## 4. 当前已经能真实跑通哪条完整链路

链路：软件公司包 → 公司/研发部/员工 → Skill/Tool 绑定 → Project → Workflow/Task 执行 → 真实成果 → Token 与成本

| 段 | 判定 | 证据 |
|---|---|---|
| ① 软件公司包实例化 | ✅ E2E 验证 | 真实 HTTP 实例化；`unresolved_refs` 全空 |
| ② 公司 / 研发部 / 员工 | ✅ E2E 验证 | Company + Dept 1 + Employees 6 + Snapshots 13 |
| ③ Skill / Tool 绑定 | 🟡 部分 | 六角色绑定成立；但 115 Tool `executable=0`，**真实 Tool 执行=空壳** |
| ④ Project 创建 | ✅ E2E 验证 | R3 真实研发项目 + 负责人 + 目标 |
| ⑤ Workflow / Task 执行 | ✅ E2E 验证 | Run `wfr-33a17cee` 7 Step 全 succeeded，返回运行 ID |
| ⑥ 真实成果 | ✅ E2E 验证 | `final_report` 6,018B（SHA-256 `2d14cf90…`），可追溯 |
| ⑦ Token 与成本 | ✅ E2E 验证 | 9,622 tokens / USD 0.01326900 / `gpt-5.4-mini-2026-03-17` |

**链路总体判定**：①②④⑤⑥⑦ 已真实 E2E 验证；③ 的"绑定层"已验证但"Tool 真实执行能力"为空壳，真实执行仅由 1 条模型网关调用承担。

---

## 5. 距离长期稳定运行还缺什么

1. **真实 Tool 执行能力**：115 Tool 需真实适配或显式标 `design_only`，否则 R3 的"Tool 执行"段永远空壳。
2. **R4 真实能力**（Agent/Workflow/Hybrid Mode、AI 秘书、团队迁移）——均触 L2，须总控解锁。
3. **R4 独立代码审计收口**：把第 1–7 项已收口代码与各自 Gate 一致性坐实，避免"Gate PASS 但代码未核"。
4. **全量回归覆盖 R3**：当前 R3 review 自认未跑全量回归，需补一次以满足其自身验收标准。
5. **状态同步机制**：Admin 共享 Issue 与 Workspace 侧结论需对齐（R3 handoff、SHA 引用），避免跨团队"一方 PASS 一方 OPEN"。

---

## 6. 下一轮最重要的三项工作（仅边界内补齐，不含 L2）

1. **补全 093 后的目录 API 缺口（只读，不触 L2）**：093 仅补 persona/dashboard/company-package/company-template 四条 GET；后续消费仍需 Skill Template、Employee 绑定类、Capability Package 的统一只读路由。属"缺只读接口"（基线 §十 carve-out），可自主推进，建议单独开 Issue + 聚焦测试。
2. **收口 R3 暴露的官方资产/模板/ID 对齐（不触 L2）**：把 115 Tool 中"已配置但 mock/stub"逐步替换为真实可执行或显式标 `design_only`；对齐 16 个 `wt_*` design-only Workflow 与 active binding；固化 `official.employee.*` 10 行的绑定质量。属悬空引用/资产状态修复，边界内。
3. **关闭 R4 独立代码构造审计 + 统一"边界 vs 实现"口径（不触 L2）**：把 `items_1_7_code_construction_audit_gate.md` 闭合；将 `PROJECT_STATUS.md` 的"R4 closed"改写为"边界/契约收口完成"，以免误导真实完成度判断；把 R4 第 3 项从"边界定义"推进到最小实现（若仍在边界内）。

> 上述三项均落在 Admin 资产工厂既有边界内，不需总控逐项审批，可由团队按 R3 协作保障模式自动重启对应席位推进。

---

## 7. 暂停事项和 L2 Gate

| 项 | 内容 | 触发 L2 条款 | 状态 |
|---|---|---|---|
| 095-① | 外部连接器生态（`cp_content_ops.connector_ids` 悬空） | #3/#4/#5/#6 | 🔴 BLOCKED_L2 |
| 095-② | 真实计费/配额商业化（`quota_rules`/`pricing_rules`/`cmcf_*`） | #1/#2 | 🔴 BLOCKED_L2 |
| 095-③ | content 公司产品线（`ccp_ai_content_company` + 商业域 Dashboard） | #1/#2/#3 | 🔴 BLOCKED_L2 |
| 095-④ | 真实多租户隔离（ADR-0017 D1–D4 当前 design-only） | #5/#6 | 🔴 BLOCKED_L2 |
| R4-⑧ | AI 秘书（仅边界/契约，未实现） | #5/#6 | 🔴 暂停待总控 |
| R4-⑨ | Codex/WorkBuddy 团队迁移（仅边界/契约） | #5/#6 | 🔴 暂停待总控 |
| R4-③ | Agent/Workflow/Hybrid 真实实现 | 视是否超边界定义 | 🟡 仅边界，超界即 L2 |
| 多源连接器 | CrewAI/skill 仓库/Coze-Dify/MCP Registry 扩展 | #3/#4/#5/#6 | 🔴 L2 |

**处理**：全部暂停，提交总控；不自主推进。095 文件头维持 BLOCKED_L2（第 5 项弱令牌已 VERIFIED/CLOSED，不计入阻塞）。

---

## 8. 是否已跑通：8 段纵向链路

| 段 | 是否跑通 | 备注 |
|---|---|---|
| 软件公司包 | ✅ | 真实实例化，`unresolved_refs` 全空 |
| → 公司/研发部/员工 | ✅ | 1D/6E 真实落地 |
| → Skill/Tool 绑定 | 🟡 | 绑定层 ✅；**真实 Tool 执行 ❌（全 mock/stub）** |
| → Project | ✅ | 真实研发项目 + 负责人 + 目标 |
| → Workflow/Task 执行 | ✅ | 7 Step 全 succeeded，运行 ID 可追溯 |
| → 真实成果 | ✅ | `final_report` 6,018B，SHA-256 可核验 |
| → Token 与成本证据 | ✅ | 9,622 tokens / $0.01326900，内部自洽 |

**最终判定**：链路**基本跑通**——真实模型调用、Workflow 执行、成果产出、Token/成本凭证均已实证；唯一未跑通的是「**真实 Tool 执行**」（115 Tool 全 mock/stub，仅 1 条模型网关调用真实发生）。这是下一轮第一项边界内补齐的核心目标。

---

## 复盘后动作（依用户指令）

- **边界内补齐**：自动生成下一轮联合计划（`issues/shared/20260718_admin_next_round_joint_plan.md`），三项工作按 R3 协作保障模式自动重启对应席位推进，无需总控逐条下令。
- **L2 事项**：全部暂停并提交总控（本报告中第 7 节），不自主推进。
- **跨团队依赖**：继续通过 `issues/shared/` 流转，不另由用户中间传话；含 R3 共享 handoff 状态同步、SHA 引用对齐、全量回归补跑等收口项。
- **不新增功能 / 不碰前端 / 不改代码**（本次复盘只读）；下一轮计划落地时严守 git 纪律与 Shared 双确认。
