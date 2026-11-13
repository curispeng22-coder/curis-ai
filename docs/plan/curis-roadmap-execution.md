# Curis 联合开发 Admin 团队四轮执行计划（自主推进拆解）

> 依据：`docs/review/2026-07-17_Curis_联合开发基线与自主推进计划.md`（基线文档）
> 性质：仅规划 / 跟踪 Markdown，**不改代码、不碰 Workspace 文件、不 git 提交**（代码改动由 eng/qa 在分支完成）。
> L2 判断口径：以基线第十节为准——「修复既有 Bug、悬空引用、缺失只读接口、测试和实例化断点，不触发 L2，可自主推进」；「新产品方向 / 新行业 / Marketplace / 真实计费 / 外部连接器 OAuth / 权限模型重大变化 / 大迁移」才触发 L2。

---

## 零、执行状态更新（2026-07-17 收尾）

**结论：** R1 / R2 的 A–E 修复波次已由 eng 与 qa 完成并提交。

**真实证据：**
- 分支 `feat/roadmap-r1r2`：R1（统一基线）+ R2（资产与实例化断点）A–E 全部实现。
- QA 独立验证：`12 passed` + `18 sanity PASS`；提交纯净、无 Workspace 泄漏。
- Draft PR #2 已开：`https://github.com/curispeng22-coder/curis-ai-workspace/pull/2`。
- 关键 commit `d7c0b21`：实现 R1.8 Admin 默认弱令牌修复（未配置 `PLATFORM_ADMIN_TOKEN` 时拒绝 Admin 请求 / 拒绝启动）。
- Admin 侧就绪资产：公司包 `ccp_ai_software_company` 可实例化、`workflow_instances=6`、Tool/Workflow 能力态已标注、**6 条只读 Catalog 路由已就位**。

**编号说明：** 本轮 R1/R2 落在一个 PR 波次内，按 team-lead 口径以「复用 091–095 + 新开 R3 共享 Issue」跟踪；前期提议的内部子号 096/097/098 现并入该波次（令牌=095 第 5 项、Tool/Workflow 状态=093/094 波次上下文），不再单开，避免双套编号。

### 零.1 PR #2 Shared 双确认状态（2026-07-17 更新）
- **Admin lead（齐活林 / 主理人）**：✅ PASS —— R1/R2 经 eng 实现 + QA 独立验证（12 passed / 18 sanity PASS），提交纯净、无 Workspace 代码泄漏，令牌修复与只读 Catalog 路由符合设计，准予合入 Shared `main.py`。
- **Workspace lead**：✅ PASS（用户于 2026-07-17 13:55 转达结论）。
- **结论**：双方双确认已完成，PR #2 **已于 2026-07-17 14:05 由 Admin lead 在干净 worktree 合入**（`Admin` fast-forward `7af20822 → 72186d58`，`main.py` blob = `0fa34bc6` 融合态，whitespace 检查通过，`origin/Admin` 已推送，PR #2 自动关闭）。
- **合入范围说明（重要）**：本次合入的是 `feat/roadmap-r1r2` 全部分支提交（12 commits / 45 files / +3048 行），其中既含 Admin 的 R1/R2（令牌门禁 + 6 只读 Catalog + Tool/Workflow 能力态 + 实例化证据测试），也含 Workspace 在共享 `main.py` 的逐 hunk 语义融合结果（`IdentityMembership` / `ResourceScopePolicy` / `TenantContext` / 6 路由全保留，blob `0fa34bc6`）及 R3 运行时提交（`model execution gate` / `OpenAI HTTPS egress` / 租户身份 L2 收口等）。后者经 Workspace 安全边界席 PASS + 32 focused tests 全过 + 双 lead PASS（见 `issues/shared/20260717_workspace_shared_main_manual_merge_preparation.md`）。
- 合入后 Workspace 基于 `Admin` rebase 并核对 `main.py` 共享改动；stash `348b688` 仍由 Workspace 按交接 Issue 去重恢复（禁止直接 pop）。
- 主工作树未受影响（Workspace 残留 + stash 348b688 原样保留）。

---

## 一、R1 统一运行基线（Admin 可自主推进部分）

> 分工（基线 R1）：WorkBuddy 确认 Admin 侧（DB / 资产事实源 / 端口 / 令牌策略）；Codex 确认 Workspace 侧。共同记录唯一启动基线。

| R1 项 | 内容 | 映射 Issue / 波次 | owner(我们) | 状态 / 验收标准 | 触发 L2 |
|---|---|---|---|---|---|
| R1.1 | 固定 Admin 侧唯一 commit | R1 基线记录 | pm-seat/eng | 已记录（PR #2 基线） | 否 |
| R1.2 | 明确 Admin 唯一数据库 | R1 基线记录 | arch/eng | `CURIS_DB` 路径明确 | 否 |
| R1.3 | Admin 进程 / 端口 / 启动命令 | R1 基线记录 | arch/eng | Admin 端口(8001) + 启动命令可复盘 | 否 |
| R1.4 | 明确 Admin 前端目录 | R1 基线记录 | arch | frontend-admin 目录明确 | 否 |
| R1.5 | 恢复后端依赖和测试环境 | R1 基线记录 | eng | pytest 可跑（QA 12 passed） | 否 |
| R1.6 | 固化本地一键启动 | R1 基线记录 | eng | 一键起 Admin | 否 |
| R1.7 | 重跑后端测试 + 边界测试 | R1 基线记录（复用 094） | eng | 12 passed + 18 sanity PASS | 否 |
| **R1.8** | **修复 Admin 默认弱令牌**（`main.py:1676-1678` 默认 `"platform-admin-dev"`，未配置拒绝） | **095 第 5 项**（commit `d7c0b21`） | arch/安全边界席 | **已实现 + 已合入 Admin**（PR #2, `main.py` blob `0fa34bc6`）：未注入 env 时 `/api/platform/*` 拒绝 | **否**（基线 R1.8 授权 + 安全 Bug 修复，非权限模型重大变更） |

**R1 完成标准（基线第四节）：** 同一 commit + 两后端可启动 + DB 路径明确 + 后端测试可执行 + 前端可构建 + 安全边界测试通过。Admin 侧 8 项全落地（PR #2）；Workspace 侧由 Codex 镜像。

---

## 二、R2 修复资产与实例化断点（WorkBuddy 主导修复）

> 分工（基线 R2）：WorkBuddy 主导修复；Codex 负责验证（读取 / 实例化 / 绑定 / 工作流真实生成）。

| R2 项 | 内容 | 映射 Issue / 波次 | owner(我们) | 状态 / 验收标准 | 触发 L2 |
|---|---|---|---|---|---|
| R2.1 | 修 `wl_*` 与真实 Workflow Template ID 不一致 | 091 | arch/eng | **CLOSED**：`wl_*`→`wt_*` 已解析 | 否（悬空引用修复） |
| R2.2 | 实例化后 Workflow 实例 > 0 | 091 + shared | arch/eng | **workflow_instances=6**；shared `20260717_admin_company_package_verify.md` = READY_FOR_VERIFY，等 Workspace 转 VERIFIED | 否 |
| R2.3 | 清理 18 孤儿员工实例 | 092 | **Codex / Workspace** | **排除执行**：属 Workspace 运行时；shared `20260717_admin_orphan_instances.md` 仍 OPEN 待确认 | 排除 |
| R2.4 | 清理 2 孤儿部门实例 | 092 | **Codex / Workspace** | **排除执行**：同上 | 排除 |
| **R2.5** | 补 Company Template / Company Package / Persona / Dashboard 等只读 GET | **093**（波次内） | arch/eng | **6 条只读 Catalog 路由已就位 + 已合入 Admin**（PR #2, blob `0fa34bc6`） | 否（缺只读接口，第十节 carve-out） |
| R2.6 | 清理未解释的 `sub_package_refs` | 091 | arch/eng | **CLOSED**：清为 `["cp_content_ops"]` | 否 |
| **R2.7** | Tool 状态标记：目录可见 / 已配置 / 可真实执行 / Mock-Stub | **R2 波次**（PR #2） | arch/eng | **已实现**：115 Tool 能力态已标注 | 否（资产状态标记） |
| **R2.8** | Workflow 状态标记：结构化可执行 / 只有设计 / 禁止实例化 | **R2 波次**（PR #2） | arch/eng | **已实现**：18 Workflow 能力态已标注 | 否（资产状态标记） |
| R2.9 | 建立资产完成度标准 | 094 | pm-seat | **DONE**：`docs/plan/admin-asset-completion-standard.md` | 否 |

**R2 完成标准（基线第五节）：** 公司包实例化得 Company + Department + Employee + Persona + Skill/ Tool Binding + Workflow Instance(=6)，每实例可追溯、无未解释悬空、Tool/Workflow 能力态清晰、有自动测试 + Workspace 消费证据。Admin 侧缺口仅剩 093 合入 + Workspace 验证；R2.3/4 交 Codex。

---

## 三、R3 打通真实纵向执行链路（Codex 主导，Admin 配合）

> 分工（基线 R6）：Codex 主导 Project / Employee / Task / Workflow / 模型工具调用 / 成果 / Token 成本 / E2E 测试；WorkBuddy **配合**补执行中发现的官方资产缺口。

**结论：** R3 运行时由 Codex 主导，Admin 不接管、不新开独立代码 Issue；Admin 只「准备就绪 + 配合补缺」。

**Admin 侧就绪（R1/R2 收尾成果）：**
- 公司包 `ccp_ai_software_company` 可实例化、`workflow_instances=6`；
- 6 条只读 Catalog 路由就位；
- Tool / Workflow 能力态已标注；
- 资产完成度标准（094）落地 → 满足 R3「配合补缺」前提。

**R3 协调件：** 新建 shared Issue `issues/shared/20260717_admin_r3_e2e_handoff.md`（OPEN），请 Codex 主导跑「AI 研发部」统一验证场景，Admin 配合补模板 / Skill / Tool / Workflow / Package 缺口（详见第五节）。

**R3 完成标准（基线 R6）：** 由 Codex 出真实 E2E 证据（8 项：项目目标 / 负责人 / 员工能力绑定 / Workflow·Task 执行记录 / 真实结果 / 成果位置 / Token·模型·成本 / 成败原因与下一步），Admin 不代出。

---

## 四、R4 补长期运行能力（R3 后顺次，每项单独 Issue）

> 前置：须 R3 通过（基线 R7：前三轮通过后按序自主推进，不得并行发散）。每项单独建 Issue、单独提交、单独验证。

| # | R4 项 | 建议 owner | 备注 / L2 复核 |
|---|---|---|---|
| 1 | Project 长期状态与项目级 Memory | Codex | 运行时域 |
| 2 | 同一员工多项目独立 Session | Codex | 多租户 Session 关联 ADR-0017，开 Issue 时复核 L2 #5/#6 |
| 3 | Agent / Workflow / Hybrid Mode | Codex | 运行时域 |
| 4 | 自动推进 / 超时 / 有限重试 / 恢复 | Codex | 运行时域 |
| 5 | 人工接管 / 停止 / 风险升级 | Codex | 运行时域 |
| 6 | 统一 Artifact / Output 后端 | Codex + Admin 资产侧配合 | 视成果中心归属 |
| 7 | 项目级 Token / 成本预算 | Codex | 触真实计费边界，可能 L2 #1/#2 |
| 8 | AI 秘书 | Codex | **八暂停**列明暂停 → 触 L2，须总控解锁 |
| 9 | Codex / WorkBuddy 团队迁移 | 双团队 | 职责边界变化，触 L2 #5/#6 |

**结论：** R4 不在本轮执行范围，仅列序；每项开 Issue 时按基线第十节逐项复核 L2，Admin 只接官方资产 / 目录相关子项。

---

## 五、跨团队 shared Issue 清单

> 命名规范（基线 §九）：`issues/shared/YYYYMMDD_<发起团队>_<主题>.md`；状态机 OPEN → ACKNOWLEDGED → IN_PROGRESS → READY_FOR_VERIFY → VERIFIED → CLOSED；重大决策用 BLOCKED_L2。

### 5.1 新建：`issues/shared/20260717_admin_r3_e2e_handoff.md`（OPEN）
- 发起：Admin；目标：Codex（Workspace）；主题：R3「AI 研发部」E2E 交接验证。
- 内容：请 Codex 主导跑通基线 §六「AI 研发部」场景；列出 Admin 侧已就绪资产（公司包可实例化 / workflow_instances=6 / 6 只读 Catalog 路由 / Tool·Workflow 能力态标注）；Admin 配合补缺口；禁止越界（不改 Workspace Runtime / 前端）。

### 5.2 既有：`issues/shared/20260717_admin_company_package_verify.md`（READY_FOR_VERIFY）
- 091 共享验证，状态不变，仍等 Workspace 消费转 VERIFIED（见第七节确认）。

### 5.3 既有：`issues/shared/20260717_admin_orphan_instances.md`（OPEN）
- 092 孤儿实例，状态不变，仍 OPEN 等 Workspace 确认处置方案 A/B（见第七节确认）。

---

## 六、Issue 095 更新（已落库）

`issues/095_admin_l2_gate_tracking.md` 已更新：
- **第 5 项（Admin 默认弱令牌）**：状态由 BLOCKED_L2 改为「**已实现（待 Shared 双确认合入 PR #2，commit `d7c0b21`）**」；
- **其余 4 项**（外部连接器 / 真实计费 / content 公司 / 多租户）仍 **BLOCKED_L2** 待总控；
- 095 文件头状态保持 BLOCKED_L2（因仍有 4 项阻塞）。

**原因：** 弱令牌是安全红线，但「未配置即拒绝」属 Bug 修复、基线 R1.8 已授权，不触发 L2（第十节 carve-out），故可从待决策转已实现。

---

## 七、执行纪律提醒（每轮按基线 §十二汇报）

1. 顺序铁律：R1 → R2 → R3准备/配合 → R4，不得并行发散；R1/R2/R3 门禁未过不进下一轮。
2. 修复类（悬空引用 / 缺只读接口 / 测试 / 实例化断点 / 弱令牌 Bug）全部不触发 L2，自主推进（PR #2 已证）。
3. 触 L2 项（095 余 4 项 + R4 标注项）一律停等总控，不擅自实现 / 补数据 / 渲染。
4. 每轮完成仅汇报：已完成 / 未完成 / 真实证据 / 当前阻塞 / 下一轮计划 / 是否触发 L2。
5. 所有 shared Issue 严格按基线 §九 走状态机；Admin 不越 Workspace 边界。

---

*本文档随 R1/R2 波次（PR #2）与 095 / shared Issue 状态同步更新。代码改动在分支完成，本文仅跟踪。*
