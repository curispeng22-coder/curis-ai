# D1 execute() 完整闭环 — 实现 Issue（范围 B）

> **状态**：APPROVED（总控 gate 2026-07-20：A 通过后执行 B）
> **关联提案**：`issues/20260719_d1_execute_full_loop_proposal.md`（GATE_APPROVED，范围 A→B）
> **关联 A 实现**：`issues/20260720_d1_execute_a_implement.md`（A 已 PASS；QA review `reviews/20260720_d1_execute_a_qa.md`）
> **分支**：`feat/roadmap-r1r2`
> **铁律**：脱敏红线；不引多 Agent；单主执行；复用既有模块不重写；不读真实凭证

---

## 一、范围

- **选项 B = A 全部 + P1 全量**：执行结果落库 / 可观测 / 错误分类增强 / 与现有 workspace 运行时衔接。
- **不含**：多 Agent、复杂 UI、外部平台直连。仅新增**只读**状态端点（文本，无表单/提交）。

## 二、任务列表（B0–B5，源自提案第二节）

| 编号 | 任务名 | 涉及文件 | 依赖 | 阻塞安全边界席 |
|---|---|---|---|---|
| B0 | 完成选项 A 全量 | 同 A1–A5 | — | 同 A（A5 真实端到端仍 `@skip`） |
| B1 | 执行结果落库表 + ORM | `app/models/d1_execution_log.py` + 表注册 | B0 | 否（受 Git 基线纪律：仅在 `backend/app/` 内新增，不破坏 shared 核心 schema） |
| B2 | 编排层落库 + 错误分类增强 | `app/d1_execute.py` | B1 | 否 |
| B3 | 只读状态端点 | `app/main.py` | B0, B2 | 否 |
| B4 | 可观测（计数/时长/错误分类） | `app/d1_execute.py` + 复用 `EvolutionEventLog` | B2 | 否 |
| B5 | B 序列测试 | `tests/test_d1_execute.py` | B1–B4 | 同 A5 |

## 三、凭证阻塞说明（与 A 一致）

- 🔴 R3 网关凭证接入仍待**安全边界席裁定**（已飞书升级，未回）。
- B 的落库 / 可观测**不依赖真实网关**（记 execute 调用结果，无论真实或降级），可全量 mock 验证。
- A5 / B5 真实网关端到端仍 `@skip`，不硬编 Key。

## 四、Git 基线纪律（关键）

- **B1 落库仅在 `backend/app/` 内新增** `app/models/d1_execution_log.py`，定义 `d1_execution_log` 表 ORM（`id` / `tenant_id` / `task_type` / `status` / `error_category` / `duration_ms` / `token_count` / `created_at`），并在既有 `Database.initialize()` 中以**最小改动**注册该表（不破坏既有 schema、不删既有表）。
- 不修改 `backend/` 根下的 shared 文件（如 `database.py` 核心 schema 之外的文件）、不跨 Admin/Workspace 边界。
- 若实现发现必须改动 shared 核心文件，立即标红上报主理人，**不裸改**。

## 五、验收口径（QA 专项）

- **落库**：execute 成功 / 失败均写 `d1_execution_log`（结果摘要 / 时长 / 调用计数 / 错误分类），且落库内容**不含**路径 / 堆栈 / Key / 参数。
- **只读状态端点**：`GET /api/workspace/internal/d1-tenant-reservation/status` 返回 `READY` / `DEGRADED` / `FROZEN` 纯文本（或最小 JSON），无表单，不泄露凭证。
- **可观测**：调用计数 / 时长 / 错误分类可经 `EvolutionEventLog` 查得。
- **脱敏红线**：落库字段与状态端点零泄露。
- **纪律**：无新增 pip 依赖；不引多 Agent；零新增 UI（仅只读端点）。
- **测试**：既有 21 个 A 用例 + B 新增用例全过；真实端到端仍 skip。

## 六、交付流（工程师 → QA → 主理人）

1. 工程师批量写代码（B0–B5），完成后 IS_PASS 全局一致性审查。
2. QA 专项验证（含脱敏抽检 + 落库内容抽检 + 状态端点抽检），智能路由判定。
3. B 全通过后主理人汇报，B 闭环。

## 七、红线与升级纪律

- 同 A：脱敏 / 不读凭证 / 不重写既有模块（`d1_single_model_toolchain.py` / `model_gateway.py` / `local_rd_toolset.py` 仍不改）/ 单主执行。
- 若触碰 L2 七项任一项或需跨线改 shared 文件 → 立即停，升级安全边界席 → 飞书 → 等总控。
- 提交严格只含 B 文件；不串 R3/093/095 等其他 issue 挂起改动（各自 owner 提交）。
