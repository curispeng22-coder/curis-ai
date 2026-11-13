# Source Control Baseline Freeze

> 阶段：Source Control Stabilization / Git Baseline Freeze
> 触发：Admin Platform 与 Workspace 两条线在同一仓库内连续推进，Phase-5～Phase-9A 存在大量未提交源码与文档，导致后续「零代码」「只改文档」「只改某模块」的交付证据无法被 `git diff` 干净证明。
> Checkpoint 提交：`83f017bf chore(project): checkpoint phase 5-9a current state`
> 本文档状态：已随独立提交纳入仓库（见文末变更记录）。

---

## 1. 为什么需要 checkpoint

同一 Git 仓库内并行推进两条线：

- **Admin Platform（商业运营控制中心）**：Plan / Pricing / Quota / Capability Package / Billing 配置面。
- **Workspace（运行时）**：EmployeeInstance / WorkflowRun / usage_event / audit_event / tenant_private / Credential Vault / Employee Runtime。

两条线从 Phase-5 起**从未提交**，全部累积在工作树中。这导致一个治理性缺陷：

> 任何后续「本阶段零代码」「本阶段只改文档」「本阶段只动 Admin」的声明，都无法在 git 层面被干净证明——`git diff` 永远显示一大片既往阶段的源码改动。

Checkpoint 的目的**不是重新审批历史**，而是把当前有效工作状态一次性冻结为一个干净的 Git 基线，使之后的每个 issue 都能以「干净工作树」为起点，恢复 `git diff` 的可审计性。

---

## 2. 当前脏工作树原因

| 项 | 值 |
|----|----|
| 旧基线（HEAD before checkpoint） | `f8ac0491 docs(workspace): finalize phase4 employee contracts and issue` |
| 分支 | `main` |
| tracked 修改文件数 | 34 |
| untracked 条目数（含目录，展开后） | 145（→ 224 实际文件） |
| 合计进入 checkpoint 的文件数 | **224** |
| 插入 / 删除行 | +37,865 / −171 |

**根因**：Phase-4 提交之后，Phase-5～Phase-9A 的全部工作（含 Admin 商业配置与 Workspace 运行时）均以「落盘但不提交」方式推进，累积成脏工作树。这并非代码缺陷，而是**流程纪律缺失**（未做到一个 issue 一个提交）。

---

## 3. Checkpoint 包含哪些阶段

| 阶段 | 主题 | 主要落点 |
|------|------|---------|
| Phase-5 | Credential Vault (G2) / Workflow MVP 准备 | Workspace 运行时基底 |
| Phase-5.5 / 5.6 | Post-G2 收尾与评审 | Workspace 边界 |
| Phase-6 | Workflow MVP | `workflow_runtime.py` |
| Phase-7 | Local Demo / Commercial Validation / Value Event 设计 | 商业雏形 + 研究文档 |
| Phase-7.5 / 7.7 | Billing Readiness 评估 | Admin 契约 |
| Phase-8 | Billing MVP（Admin 开发，G1 通过） | `billing_store.py` + platform 路由 + 面板 |
| Phase-8.5 | Commercial Readiness | 商业契约 + 包装研究 |
| Phase-8.6 | Admin Commercial Configuration Audit + Design | 4 份设计/审计文档 |
| Phase-9A | Plan Config Adjust / Commercial Design Freeze | 套餐可配置化修正 |

---

## 4. 文件归属（两队 + shared）

> 归类依据：`admin-platform/`、`backend/app/billing_store.py`、`frontend/app/platform/*`、商业契约/研究文档 → **Admin**；`workspace/`、`credential_vault.py`、`workflow_runtime.py`、`employee_templates.py`、Workspace 路由与运行时 → **Workspace**；跨线核心（DB schema、路由入口、工具链、PMO） → **Shared**。

### 4.1 Admin Platform 负责

**源码（✅ 含源码改动）**
- `backend/app/billing_store.py`（新）
- `backend/app/main.py`（platform 路由：`/api/platform/plans`、`/quotas`、`/capabilities`、`/billing-events` 等，全部 `_require_platform_admin` 守卫）
- `backend/app/database.py`（内含 Admin 商业表：`plans` / `quotas` / `capability_catalog` 及 seed）
- `frontend/app/platform/page.js`（新）
- `frontend/app/platform/PlanManagementPanel.js` / `QuotaManagementPanel.js` / `UsageDashboardPanel.js` / `BillingEventPanel.js`（新）

**文档/契约（✅ 含文档改动）**
- `docs/contracts/admin-plan-management-contract.md`、`admin-quota-contract.md`、`admin-capability-package-contract.md`、`admin-workspace-commercial-boundary.md`
- `docs/contracts/commercial-configuration-contract.md`、`commercial-data-flow.md`、`pricing-contract.md`、`pricing-package-contract.md`、`billing-domain-contract.md`、`billing-rule-contract.md`、`quota-rule-contract.md`、`capability-package-contract.md`、`employee-seat-contract.md`、`value-event-*.md`
- `docs/decisions/commercial-operation-roadmap.md`、`commercial-package-model-v1.md`、`commercial-roadmap.md`
- `docs/release/phase7-demo-polish-commercial-readiness.md`、`phase75-*.md`、`phase8-workspace-billing-support-implementation-report.md`、`phase9a-commercial-design-freeze.md`
- `docs/research/domain/{pricing-model-research,curis-packaging-research,billing-readiness-assessment,workspace-commercial-readiness,value-measurement-research}.md`
- `admin-platform/`（新目录）

### 4.2 Workspace 负责

**源码（✅ 含源码改动）**
- `backend/app/credential_vault.py`（新，金库逻辑：DB 仅存 digest/元数据，绝不存明文 secret）
- `backend/app/department_activation.py`（新）
- `backend/app/runtime_capability_context.py`（新）
- `backend/app/usage_meter.py`（新）
- `backend/app/workflow_runtime.py`（新）
- `backend/app/employee_templates.py`（改）
- `backend/app/codex_executor.py`（改）
- `backend/app/orchestrator.py`（改）
- `backend/app/result_store.py`（改）
- `backend/app/tool_executor.py` / `tool_router.py`（改）
- `backend/app/evolution_event_log.py`（改）
- `backend/app/ceo_context.py`（新，agent 运行时上下文 — *归属略有不确定，按 Workspace 运行时归类*）
- `frontend/app/page.js`（改，Workspace 主界面）
- `frontend/app/taskViewModel.mjs` / `taskViewModel.test.mjs`（改）

**文档/契约（✅ 含文档改动）**
- `docs/contracts/workflow-runtime-contract.md`
- `docs/decisions/ADR-0017-multitenant-department-catalog.md`、`ADR-0029-model-gateway-production-security-boundary.md`、`ADR-0031-workspace-company-foundation-boundaries.md`、`ADR-0032-workspace-department-activation-boundaries.md`
- `docs/release/phase4-*.md`、`phase45-*.md`、`phase5-g2-credential-vault-*.md`、`phase55-*.md`、`phase6-workflow-mvp-*.md`、`phase65-*.md`、`phase7-*-demo-*.md`、`phase8-workspace-billing-support-implementation-report.md`
- `docs/demo/phase4/5/6/7-*.md`
- `workspace/`（新目录）
- `reviews/`（061–085，均为 Workspace 阶段评审）
- `issues/`（064–087 中 Workspace 相关切片 gate 与本地 demo 证据）

### 4.3 Shared（两队共用 / 基础设施）

- `backend/app/database.py`（**核心 schema，shared**；Admin 在其中新增商业表，但文件本身是跨线基础设施）
- `backend/app/main.py`（**中央路由，shared**；同时服务 workspace 与 platform 路由）
- `.gitignore`、`AGENTS.md`、`README.md`、`PROJECT_HANDOFF.md`
- `knowledge/CURRENT_CONTEXT.md`
- `docs/pmo/`（本目录）
- `shared/`（新目录，显式 shared）
- `tools/`、`plugins/`、`diagrams/`、`deploy/`、`docs/99_Archive/curis_workspace_blueprint/`、`curis_workspace_blueprint/ADR/`
- `docs/standards/`、`docs/prototypes/`、`docs/product/`、`docs/demo/`、`docs/design/`（混合）
- `.workbuddy/`（工具链记忆/自动化，非产品）
- `.agents/`（工具链）

**不确定归属文件（已保留，未删除）**
- `backend/app/database.py`、`backend/app/main.py`：跨线核心，按 shared 归类，但内含 Admin 商业表/路由。
- `backend/app/ceo_context.py`：agent 运行时上下文，暂归 Workspace，如后续发现属 shared 再调整。
- `reviews/`、`docs/design/`、`docs/demo/`：混合内容，按主导主题归类，不强行拆分。
- `docs/contracts/usage-value-event-boundary.md`、`value-event-*.md`：商业+运行时边界，按 shared/Admin 边界契约处理。

---

## 5. Checkpoint 后新规则（强制）

1. **每个 issue 开始前必须确认 `git status` 干净**（基于本 checkpoint `83f017bf`）。
2. **一个 issue 一个提交**；提交信息标注 issue 编号与归属线（Admin / Workspace / Shared）。
3. **文档阶段不得混入源码**；**代码阶段不得混入无关文档**。
4. **Admin 文件只进 `admin-platform/` 与 Admin 范围**（商业配置、platform 路由、商业契约）。
5. **Workspace 文件只进 `workspace/`、`backend/app/`、`frontend/app/`（Workspace 范围）**。
6. **Shared 文件必须说明两队共用原因**（如 `database.py` 跨线 schema、`main.py` 路由入口）。
7. **任何跨线变更必须先开 shared contract / gate**（如 Admin 要读 Workspace 运行时状态，须经边界契约批准，不得直接改 Workspace 执行链）。
8. **红线保持**：不修改 Workspace 执行链、不修改 Credential Vault 明文语义、不把商业规则写死代码、不开发 payment/invoice/Marketplace/Promotion/ROI（均须独立 gate 解锁）。

---

## 6. 验证记录（checkpoint 前置条件，全部通过）

| # | 验证项 | 命令 | 结果 |
|---|--------|------|------|
| 1 | `git status` | `git status --short` | ✅ 179 条目（34 tracked + 145 untracked，展开 224 文件）已枚举并归类 |
| 2 | `git diff --check` | `git diff --check` | ✅ exit 0，无空白错误 |
| 3 | 后端回归测试 | `backend/.venv/bin/python -m pytest -q` | ✅ **356 passed, 0 failed**（16.06s） |
| 4 | 前端 lint | `npm run lint`（eslint .） | ✅ exit 0，无错误 |
| 5 | 前端 build | `npm run build`（Next.js 16） | ✅ exit 0，编译 + TS 检查通过，4 路由静态生成 |
| 6 | secret scan | 高信号密钥格式 + `api_key="..."` 赋值 + `.env` 检查 | ✅ 零命中；真实 `deploy/new-api/.env` **未跟踪、未进提交**；`credential_vault.py` 为金库逻辑 |
| 7 | `/api/platform/*` Workspace runtime scan | `grep` main.py platform 路由（1057–1600 行） | ✅ Admin 路由**不调用** `credential_vault` 写入 / `workflow_runtime` 执行 / `orchestrator.run` / employee 实例创建 / `tool_executor`；所有 Workspace 运行时写入均集中在行 <1057 的 workspace 路由区，Admin/Workspace 边界在路由层成立 |

> 验证结论：**全部通过 → checkpoint 授权建立**（符合「验证通过才创建基线提交」规则）。

---

## 7. 是否可恢复 Phase-9A 开发

**可以。** 验证全部通过，基线已冻结为干净状态（`83f017bf`，工作树清洁）。Phase-9A 商业配置开发可在 checkpoint 之后、遵循第 5 节新规则恢复推进，且每个 issue 将以干净 `git status` 为起点，其「只动 Admin」「零代码红线」等声明可被 `git diff` 干净证明。

恢复前置建议：
- Phase-9A 首任务仍为 **P0 订阅价落点**（Phase-8.6 审计识别的唯一 P0：`plans` 表无 `price`/`billing_cycle` 列）。
- 9B（Invoice/Payment）/ 9C（Marketplace）/ 9D（Value Pricing）仍须对应独立 gate 解锁，本阶段红线禁止提前实现。

---

## 8. 本阶段严格禁止（执行纪律回顾）

- ❌ 不新增产品功能（仅冻结基线 + 治理文档）
- ❌ 不借 checkpoint 混入未说明的新代码（224 文件均为既往 phase-5-9a 工作，无新增逻辑）
- ❌ 不删除不确定归属文件（全部保留并归类）
- ❌ 不 `reset` / `checkout` / 清理他人文件（仅 `add` + `commit` 当前状态）
- ❌ 不把 checkpoint 当作功能验收结论（checkpoint 仅恢复 Git 可审计基线，不代表重新审批历史阶段）

---

## 变更记录

| 提交 | 说明 |
|------|------|
| `83f017bf` | `chore(project): checkpoint phase 5-9a current state` — 冻结 224 文件工作树为干净基线 |
| （本提交） | `docs(pmo): add source-control-baseline-freeze` — 本文档，记录冻结原因/归属/新规则 |
