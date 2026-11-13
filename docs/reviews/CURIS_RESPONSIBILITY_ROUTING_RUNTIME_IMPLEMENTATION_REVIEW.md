# CURIS RESPONSIBILITY ROUTING RUNTIME IMPLEMENTATION REVIEW

Authority Class: REVIEW
Status: Review
Disposition: IMPLEMENTED · CONTRACT ALIGNMENT CEO REVIEW REQUIRED
Date: 2026-08-19
Issue: `CURIS-RESPONSIBILITY-ROUTING-RUNTIME-001`
Baseline: `b4344972562484692fb93a05720cccde371a2504`

## 1. Verdict

Feasibility 与 bounded implementation 均通过。当前新增的是 opt-in Shared Responsibility Routing layer，不替换 legacy sequential `WorkflowRuntime`，不修改 Pipeline、Orchestrator、RD/XHS Domain Runtime，不新增 Task、表或 destructive migration。

真实闭环已经成立：

```text
Scoped Responsibility Assignment
→ immutable Workflow Version snapshot
→ existing Work pins vN
→ deterministic Result / Need signal
→ Default Next | Explicit Target | Return | Current-scope Leader | Decision Gate | Complete
→ existing HANDOFF / DECISION_PACKET lifecycle
→ accepted Holder transfer
→ Result refs recover to the same Work
```

## 2. Actual implementation

- `RESPONSIBILITY_ASSIGNMENT`：使用既有 `runtime_entities/runtime_links`，持久化 Employee、Role、Scope、Responsibility、Leader flag、Capability Binding refs、Input/Output Contract 与 revision。
- `RESPONSIBILITY_WORKFLOW`：每次发布生成不可变版本快照；保存 Assignment snapshot、Default Flow hint 与 `defaultNext`。运行中 Work pin vN；编辑 Assignment/顺序/合同后发布 vN+1，新 Work才读取 vN+1。
- `ResponsibilityRoutingRuntime`：只接受枚举化 signal，不做自然语言万能判断。
- Work projection：在同一 Domain Work 的 `data_json.responsibilityRouting` 与已有 `workContext` 中记录 Assignment、Holder、Executor、version、return stack、refs 和状态；不创建平行 Task。
- Handoff：复用既有 `HANDOFF` entity 与 `CREATED→SENT→ACKNOWLEDGED→COMPLETED` 状态机；完整 path、link、Holder transfer 在一个 SQLite transaction 内落库。
- Decision Gate：复用同一 `DECISION_PACKET`；重复等待请求返回原对象，CEO Decision apply 后恢复原责任，不生成 Handoff。
- Consult / Review：作为同一 Cycle Work 的轻量持久化 collaboration record；不创建 Task、Cycle、Provider Task、Provider Session 或第五套 Runtime。
- Context：只装配 Work/Workflow/Assignment 和最多 16 个 truth/result/artifact/evidence refs；问题上限 1000 字符、摘要上限 600 字符；不装载 Conversation history，并持久化 chars/bytes/ref count/hydration/provider-task cost。

## 3. Runtime truth boundaries

- `Responsibility Holder != Current Executor`：所有交接后 Holder 更新，Executor 保持 `none`，直到真实执行层接管。
- Capability Binding 只作为 Assignment requirement ref；本实现不伪造 Provider 可用性、mode、model 或 permission。
- Default Flow 只是 normal completion hint。显式 need/return/leader/decision 可以合法偏离。
- Consult / Review 不转移 Holder。Review request revision 只有在 revision responsibility 与当前 Holder 不同时才创建 Handoff；同责任 revision 保持 Holder。
- Handoff 不创建 Task；两个场景的 `tasks` count 始终为 0。
- Handoff ACK 是 transfer transaction 内的 Runtime atomic acceptance：在 Holder 变化前重新验证 pinned workflow/scope/Work/current Holder、target Assignment、target Employee availability/scope 和 reference-first context。它不是人工确认，也没有伪造 Provider callback。
- Legacy `WorkflowRuntime` 仍是 mandatory sequential，并通过原 focused regression。
- Department Assignment 可独立登记到真实 Department scope；Workspace↔Business↔Department authoritative chain 仍缺直接关系，因此本轮只实现当前 scope Leader，不伪造跨层 escalation。

## 4. Scenario evidence

### Content growth

隔离库 `pytest-168/.../content-routing.sqlite`：

- 6 Assignments、Workflow v1；Default Flow 为 `topic→research→copy→visual→publish`，Leader 不在 normal flow。
- normal completion 自动前进；research Consult Leader 后 Holder 仍为 research、Handoff count 不变；visual explicit return 回 copy；最后 publish completion 回收到同一 `cycle-content`。
- 最终：`status=COMPLETED`、Holder=`employee-publish`、Executor=`none`、6 个 completed Handoff、Consult=`COMPLETED`、0 Task、`integrity_check=ok`。

### RD dynamic deviation

隔离库 `pytest-168/.../rd-routing.sqlite`：

- v1 Default Flow：`product→architecture→development→test`。
- development 分别 Consult product 与 architecture；两个协作完成前后 Holder 始终为 development，Handoff count 不变。
- `STAY_AND_CONTINUE` 不生成 Handoff；test 的 `RETURN_OR_REVISION` 真实转回 development，修复完成后再回 test。
- 更新 test Employee Binding、Responsibility、Input/Output Contract 与顺序后发布 v2；原 Work仍 pin v1，新 Work读取 v2 和 `employee-test-v2`。
- 原 `cycle-rd-v1`：`workflowVersion=1`、Holder=`employee-test`、Executor=`none`、5 个 Handoff、2 个 completed Consult、0 Task、`integrity_check=ok`。

### Decision / Business scope

隔离库 `pytest-168/.../business-routing.sqlite`：

- 真实 `business_directions` 下、零 Workspace 的 Business-scoped Assignment/Workflow 可解析并运行；证明 Operating Team 不必伪造 Workspace。
- 重复 Decision Gate 只产生 1 个 `DECISION_PACKET`；CEO apply 后同一 Holder 恢复 ACTIVE；Handoff count=0、Task count=0、`integrity_check=ok`。

### Holder-preserving collaboration

隔离库 `pytest-168/.../collaboration-routing.sqlite`：

- Consult 可先持久化 `WAITING`，Runtime 重开后完成；duplicate key 返回同一记录，内容冲突 fail closed。
- 当前 Work pin workflow v1；发布 v2 和更换 reviewer 后，已有 Consult/Review 仍引用 v1 snapshot 与原 Employee。
- Review request 不转移 Holder。`APPROVE + continue_default` 只产生一次合法 default Handoff；重复 resolve 不产生第二次交接。
- `REQUEST_REVISION` 转给不同 responsibility 时产生 Handoff；同 Holder revision 不产生 Handoff。
- 最终：4 条 collaboration records、2 个 Handoff、0 新 Task、仍只有 1 个 Cycle、`integrity_check=ok`。
- context cost：`chars=609`、`bytes=1827`、`refsCount=16`、`hydratedBodiesCount=0`、`providerTaskCreatedByRouter=false`、`providerSessionCreatedByRouter=false`。

## 5. Persistence and failure truth

- `ResponsibilityRoutingRuntime(Database(existing_path))` 重开后读取同一 Work、Workflow version、Holder、Executor、Handoff refs 与 Result refs。
- Output Contract 要求 Result 时，当前 responsibility completion 未携带 Result ref 会 fail closed；不会推进、不会伪造完成。
- concurrent Holder/Assignment drift 在 Handoff transaction 前被拒绝。
- reference budget 与 compact-context budget 均由 focused test 证明。

## 6. Tests

隔离环境统一设置：

```text
CURIS_DB=/tmp/.../runtime.sqlite
CURIS_DB_PATH=/tmp/.../runtime.sqlite
CURIS_WORKSPACE_DB=/tmp/.../runtime.sqlite
```

结果：`20 passed`。

- `test_responsibility_routing_runtime.py`: 5 passed
- `test_runtime_foundation_persistence.py`
- `test_employee_execution_identity.py`
- `test_rd_phase2b_e2e_closure.py`
- `test_xhs_calendar_note_runtime.py`
- `test_phase6_workflow_mvp.py`
- `test_backend_test_db_safety.py`
- Python compile PASS
- `git diff --check` PASS

测试只出现既有 FastAPI `on_event` / asyncio deprecation warnings；无本 Issue failure。

## 7. Active DB safety

活动库 `data/curis.sqlite` 前后完全一致：

- size: `1232896`
- mtime_ns: `1786873339955841838`
- SHA-256: `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6`
- `pragma integrity_check`: `ok`

## 8. Changed files

- `backend/app/runtime/responsibility_routing.py`（新增）
- `backend/app/runtime/foundation.py`（additive entity registration only）
- `backend/app/runtime/__init__.py`（export only）
- `backend/tests/test_responsibility_routing_runtime.py`（新增）
- `issues/CURIS-RESPONSIBILITY-ROUTING-RUNTIME-001.md`
- `docs/reviews/CURIS_RESPONSIBILITY_ROUTING_RUNTIME_IMPLEMENTATION_REVIEW.md`

未修改 `database.py`、`main.py`、`workspace.py`、Product/Frozen Authority、RD/XHS UI 或任何活动数据库。

## 9. Remaining gaps

- 当前没有 UI/API editor adapter；Shared Runtime 已可由后续 bounded integration 调用。
- accepted RD/XHS Domain flows 未切换到新 Router；保持 opt-in，避免回归。后续迁移必须独立 Issue 与 Domain acceptance。
- Workspace↔Department 直接权威关系仍缺失；未实现自动 Workspace→Business→Department escalation chain。
- Business scope 已能使用真实 `business_directions`，但 Company↔Business 的 authoritative cross-layer relation 仍未在本 Issue 猜测或补造。
- 未实现自然语言 intent routing、负载均衡、组织自动创建、Generic Workspace UI 或自由 DAG。
- Provider execution bridge 可继续消费 Assignment context，但本 Issue 不自动启动 Provider，不伪造 execution/effective permission。

## 10. Contract alignment answers

1. `CONSULT`：已实现为 holder-preserving collaboration；可等待、重启恢复、完成，不创建 Handoff。
2. `REVIEW`：已实现为 holder-preserving collaboration；Review Request 不等于 Handoff。
3. Revision：仅责任真正变化时 Handoff；当前 Holder 自己修改时不交接。
4. Continue：`STAY_AND_CONTINUE` 保持原责任；Review approve 可显式选择 default continue。
5. Action vocabulary：兼容 `STAY_AND_CONTINUE`、`RETURN_OR_REVISION`、`ESCALATE`、`WAIT_DECISION`、`COMPLETE_CYCLE`，统一映射到现有最小 Router action。
6. Operating Team scope：Business 可依真实 Business record 运行，不再要求 Workspace；Workspace scope 保持既有真实关联校验。
7. Leader：当前 scope 内唯一 Leader 可解析；缺失或多 Leader 均 fail closed；未伪造跨层组织链。
8. ACK：`RUNTIME_ATOMIC_ACCEPTANCE` 表示 transaction 内验证并接受转移，不表示人工或 Provider-native ACK。
9. Atomicity：ACK 与 Holder transfer 同 transaction；transfer 前复核 pinned truth 与目标 Employee/Assignment。
10. Context durability：collaboration record 随同一 Work 持久化；reference-first，不复制 Conversation。
11. Context cost：字符、字节、引用数、水合数与是否创建 Provider Task/Session 可审计；本轮后两者均 false。
12. Duplicate truth：Consult/Review create/resolve 重复调用返回同一事实或 fail closed，不重复 Handoff。
13. Runtime boundary：未新增表、Task、Cycle、Review Runtime、Provider Task/Session 或第五套执行系统。

## 11. Commit status

未授权 commit；本轮未 stage、未 commit、未 push。当前实现等待 CEO Review。
