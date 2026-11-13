# 下一轮联合计划（边界内补齐）· 2026-07-18

> 发起：Admin（齐活林 / 主理人）｜目标：Codex（Workspace）+ WorkBuddy（Admin）
> 来源：2026-07-18 联合复盘报告（`docs/review/2026-07-18_curis-joint-progress-review.md`）
> 流转规则：跨团队依赖一律经 `issues/shared/`；不另由用户中间传话。
> 纪律：本次复盘只读；本计划落地时**不新增功能、不碰前端、不改代码以外的约定**，严守 git 纪律与 Shared 双确认。

## 状态：OPEN（边界内自主推进，L2 项已单列暂停）

---

## 一、边界内三项补齐（Admin 可自主，按 R3 协作保障模式自动重启对应席位）

### 1. 补全 093 后的目录 API 缺口（只读，不触 L2）
- **问题**：093 仅补 persona/dashboard/company-package/company-template 四条 GET；后续消费仍需 Skill Template、Employee 绑定类、Capability Package 的统一只读路由。
- **动作**：开内部 Issue → 架构师出最小设计（复用 093 风格 + `_require_platform_admin`）→ 工程师加路由 + `database.list_*` 投影 → QA 补 401+200 种子行测试。
- **范围**：仅缺只读接口（基线 §十 carve-out），不新增写操作、不触 L2。
- **验收**：新增路由 200 且含种子行；401 门禁；pytest 全绿。

### 2. 收口 R3 暴露的官方资产/模板/ID 对齐（不触 L2）
- **问题**：115 Tool 全 `executable=0/mock_or_stub=1`；16 个 `wt_*` design-only 与 active binding 需对齐；`official.employee.*` 10 行绑定质量需固化。
- **动作**：
  - 把"已配置但 mock/stub"的 Tool 逐步替换为真实可执行适配器，或显式标 `design_only`（诚实声明，不伪造）。
  - 对齐 16 `wt_*` design-only 与 active binding，消除悬空/不一致。
  - 固化 `official.employee.*` 10 行绑定（6 software_rnd 镜像 + 4 content_growth persona）。
- **验收**：能力态字段与真实能力一致；无"标可执行实为 mock"的假完成；QA 复跑 `test_tool_and_workflow_capability_states_are_not_overstated` 仍 PASS。

### 3. 关闭 R4 独立代码构造审计 + 统一"边界 vs 实现"口径（不触 L2）
- **问题**：`items_1_7_code_construction_audit_gate.md` 仍 OPEN；`PROJECT_STATUS.md` 写"R4 closed"易误导。
- **动作**：
  - 把 R4 第 1–7 项已收口代码与各自 Gate 一致性坐实，闭合独立代码审计。
  - 将 `PROJECT_STATUS.md` 的"R4 closed"改写为"边界/契约收口完成"，并标注第 3/8/9 项未实现（触 L2）。
  - 在边界内把 R4 第 3 项（Agent/Workflow/Hybrid）从"边界定义"推进到最小实现（若超出边界即升 L2）。
- **验收**：审计 Gate CLOSED；文档口径与代码真实状态一致。

---

## 二、跨团队收口项（需 Codex / Workspace 配合，经本 Issue 流转）

| 项 | 负责方 | 动作 |
|---|---|---|
| R3 共享 handoff 状态同步 | Admin ↔ Workspace | `issues/shared/20260717_admin_r3_e2e_handoff.md` 由 OPEN 更新为与 Workspace PASS 一致（Workspace 侧 `issues/20260717_workspace_r3_ai_rd_vertical_e2e.md` 已 PASS/CLOSED） |
| R3 SHA 引用对齐 | Admin ↔ Workspace | 对齐 R3 issue 与 review 的固定 SHA（758da525 ↔ b0f791f7），在文档中说明时间线 |
| R3 全量回归补跑 | Workspace / Codex | 补一次全量回归以满足 R3 review 自身"无 R3 新增失败"验收条款（当前 review 自认未跑） |
| `workflow_instances=6` 落点澄清 | Admin ↔ Workspace | 确认 091 闭环实例写入哪个 DB、是否被后续运行重置；统一"瞬时 E2E 结果"与"持久化计数"口径，避免声明歧义 |

---

## 三、L2 暂停项（提交总控，不自主推进）

- 095 余 4 项：外部连接器生态 / 真实计费 / content 公司产品线 / 真实多租户隔离 — 均 BLOCKED_L2。
- R4 第 8 项 AI 秘书、第 9 项团队迁移 — 仅边界/契约收口，功能实现触 L2 #5/#6，暂停待总控。
- 多源连接器扩展（CrewAI/skill 仓库/Coze-Dify/MCP Registry）— L2。

> 上述任一项如需推进，走总控 L2 解锁流程（安全边界席 → 飞书升级 `oc_1b559ad633e40345229275d15f7e8d42` → 等总控决策），不在本计划自主范围。

---

## 四、交付与跟踪

- 本计划拆分出的子任务各自开独立 Issue（Admin 侧落 `issues/`，跨团队落 `issues/shared/`）。
- 每项完成经 QA 验证后 CLOSED；Shared 改动（main.py/database.py）走 Admin+Workspace 双确认。
- 主理人齐活林汇总进度，按"结论→原因→建议"三段式向总控汇报，不重复历史过程。
