# SHARED-EMPLOYEE-EXECUTION-TRUST-001

**Status:** IMPLEMENTED / ACCEPTED
**Date:** 2026-08-17
**Owner:** Curis Shared Runtime

## Goal

在不新增 Employee / Identity Primitive 或数据库表的前提下，收口 Shared Runtime 的
业务员工身份与 Provider/Agent 执行归属：Runtime `AI_EMPLOYEE` 是 canonical business
identity；legacy Company Employee 是显式关联的 execution identity；Task、Capability
Binding、UsageEvent 和 Provider session 共同形成 callback provenance。

## Authority

1. `docs/00_Context/CURRENT_STATE.md`
2. `docs/03_Design/Curis_Company_OS_Shared_Authority.md`
3. `docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`
4. `docs/01_Product/Agent_Adapter_Contract.md`
5. `docs/01_Product/Agent_Adapter_Compatibility_Registry.md`
6. `docs/07_Decisions/ADR-0046-local-agent-computer-access-authority.md`

## Current truth and gap

- Runtime `AI_EMPLOYEE` 与 `employee_instances` 是两种现存表示；当前 Shared 投影只支持
  ID 完全相同的兼容解析。
- RD Agent 执行按能力选择 Company Employee，但没有把该执行身份显式、可审计地绑定回
  Runtime Employee；Result/Evidence 的 Provider callback provenance 因而不完整。
- Provider payload 不应自行声明 Curis Employee；Curis 必须从已持久化 Task、Capability
  Binding 和 UsageEvent 验证 callback actor。
- 现有 Handoff ACK 不携带可验证的接收 Employee/Provider execution evidence；本 Issue
  提供 Shared verifier，Domain 只能在 verifier 通过后记录 Provider-native ACK。
- `workspaces` 当前无 authoritative `department_id`；只存在 Project→Department 与
  Employee affiliation 事实。本 Issue 不推断、不迁移该关系。

## Canonical mapping rules

1. Runtime `AI_EMPLOYEE.entity_id` 是 Curis business Employee identity。
2. `AI_EMPLOYEE.data.companyEmployeeRef` 是显式 Company execution identity bridge；写入前
   必须验证同 tenant/company、active legacy Employee 与其真实 Capability Binding。
3. 旧数据仅在两个 ID 完全相同时允许 `EXACT_ID_FALLBACK` 只读兼容；禁止名称、岗位或
   Provider 的模糊匹配。
4. Provider callback 只在 Task scope、Company Employee、Capability Binding、UsageEvent、
   session（存在时）全部一致时标记 `VERIFIED`。
5. Responsibility Holder、Current Executor、Company execution Employee 和 callback actor
   保持独立字段；其中任一不得自动覆盖其它身份。

## Allowed files

```text
backend/app/employee_execution_identity.py
backend/app/shared_workspace_projection.py
backend/app/main.py                              # 仅 RD 既有 Agent dispatch/result owned hunks
backend/tests/test_employee_execution_identity.py
backend/tests/test_shared_workspace_projection.py
issues/SHARED-EMPLOYEE-EXECUTION-TRUST-001.md
reviews/SHARED-EMPLOYEE-EXECUTION-TRUST-001_review.md
```

## Mixed-source protection

- Pre-change SHA-256:
  - `backend/app/main.py`: `1f246f0ad788e586a8a579a9f79c188c3564f59d0b4687b74363fe33010f4a62`
  - `backend/app/shared_workspace_projection.py`: `ca478b4f04ec556d1bfe102f4e45a026771f045d19ca2c492aa34a8ed1328a8b`
  - `backend/app/runtime/workspace.py` (read-only): `2688bd3a174d82714f6bc99b2c37787559ea762540f2b53d970c9171f52dcdc1`
  - `backend/app/api/runtime_foundation_router.py` (read-only): `0e4abf4f6cd214f13ded6cc28b143ab8264a0effbf3371496cca733f43f4a789`
- `main.py` owned hunks are limited to `execute_runtime_business` identity bind/verify calls.
- Existing dirty or untracked Runtime/Foundation files are preserved and not staged by this Issue.

## Explicit exclusions

- Frozen Authority、Product Blueprint、UI、RD/XHS/TTK Domain lifecycle。
- 新 Employee/Identity/Permission/Workflow primitive 或 Schema migration。
- Provider mode/model/permission 推断；Full Computer Access。
- Workspace↔Department 猜测、名称映射或不可逆数据回填。
- 修改活动 SQLite、Secret、凭证、Provider private payload。

## Acceptance

1. Runtime Employee 可显式解析到同 Company 的 active execution Employee；跨 scope 拒绝。
2. 冲突 bridge、模糊匹配、缺失 Capability Binding fail closed。
3. 真实 Task/UsageEvent/session callback 可投影 canonical Runtime Employee provenance。
4. forged employee/task/capability/session callback 均拒绝。
5. Provider-native Handoff ACK verifier 只接受 SENT Handoff 的真实 target Employee 与已验证
   execution provenance；verifier 不自行改变 Handoff lifecycle。
6. Shared employee read projection 保持兼容并公开 bridge source/status。
7. stop/restart 后 bridge 与 provenance 可从同一隔离 SQLite 重建；持久化不等于 Provider
   仍在执行。
8. Workspace↔Department 输出仅来自现有 Project/affiliation 事实；缺直接关系标记 gap。
9. Existing discovery/binding/Codex execution、Shared read model、RD/XHS focused tests无回归。
10. 全部 backend tests 使用 repository-external SQLite，且三变量指向同一路径。

## Review

正式证据记录在 `reviews/SHARED-EMPLOYEE-EXECUTION-TRUST-001_review.md`。

## Implementation result

- `AI_EMPLOYEE.data.companyEmployeeRef` 保存显式、同 scope、active Company execution
  identity bridge；旧数据只保留 exact-ID read fallback。
- `execution.identity_bound` append-only event 把每个 Task 精确绑定到 Runtime Employee、
  Company Employee 与当次 Capability Binding；同一 legacy executor 被多个业务员工复用时，
  Task assignment 仍不产生 callback actor 歧义。
- Provider callback 由 Task、assignment event、active Capability Binding、`usage.task_execution`
  与 session 共同验证；forged task/employee/capability/session fail closed。
- RD 既有 Codex dispatch 在 owned hunks 中写入 bridge/assignment，并将 verified callback
  provenance 带回既有 `executionBinding`；Runtime Evidence/Outcome/Result projection 可读取
  canonical Employee provenance。
- `verify_handoff_ack()` 是提供给 RD/其它 Domain 的稳定 Shared verifier；它只验证当前
  SENT target 与 Provider execution evidence，不自行改变 Handoff lifecycle。
- 无新 schema、无全局状态、无 UI、无 Domain lifecycle 修改。
