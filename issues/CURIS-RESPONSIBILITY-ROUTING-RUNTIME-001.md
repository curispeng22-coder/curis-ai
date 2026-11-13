# CURIS-RESPONSIBILITY-ROUTING-RUNTIME-001

Authority Class: CURRENT · IMPLEMENTATION
Status: Implemented · Contract Alignment CEO Review Required
Date: 2026-08-19
Baseline: `b4344972562484692fb93a05720cccde371a2504`

## Goal

在不替换现有 Workflow、Pipeline、Orchestrator、RD/XHS Domain Runtime 的前提下，增加最小共享运行层：`Employee × Role × Scope = Responsibility Assignment`，并让同一 Work 在固定 Workflow Version 内依据明确结果信号完成 Default Next、显式偏离、Return、当前 Scope Leader escalation、Decision Gate 与 Result recovery。

## Feasibility Gate

- PASS：通用 `runtime_entities/runtime_links` 可承载 Assignment、不可变 Workflow Version 与现有 Handoff/Decision 对象。
- 不新增表，不做 destructive migration，不修改活动 SQLite。
- 旧 `WorkflowRuntime` 继续保持 mandatory sequential compatibility；新路由仅由显式 opt-in Work 使用。
- accepted RD/XHS Handoff、Decision、Artifact Review 与 Provider provenance 不改写。

## Allowed Files

- `backend/app/runtime/responsibility_routing.py`（新增）
- `backend/app/runtime/foundation.py`（仅登记两个 additive entity type）
- `backend/app/runtime/__init__.py`（仅导出共享 Runtime）
- `backend/tests/test_responsibility_routing_runtime.py`（新增）
- `issues/CURIS-RESPONSIBILITY-ROUTING-RUNTIME-001.md`
- `docs/reviews/CURIS_RESPONSIBILITY_ROUTING_RUNTIME_IMPLEMENTATION_REVIEW.md`

Pre-change SHA-256：

- `backend/app/runtime/foundation.py`: `48610cb64b1f5a7c71ce64d33c6e6e2d9d75936eb9608c5b3fe089c82d6335e2`
- `backend/app/runtime/__init__.py`: `c429b2c4868a3aa6a287a9827f3a05fe5c2eb500ebdacbfd4c18a70a7c010661`

Contract Alignment Delta pre-change SHA-256：

- `backend/app/runtime/responsibility_routing.py`: `672d83949bf4ed995e32975257932aa8ef8a76b603f6f6de4d59087556c68e9b`
- `backend/tests/test_responsibility_routing_runtime.py`: `e8638aee7cb121e39b372f018c7cda596c4a6b4022edcdfb1e87db0b7834aecf`
- `issues/CURIS-RESPONSIBILITY-ROUTING-RUNTIME-001.md`: `6f2a9aa23b5a0ef30e91d70ef873c968bbe16acf5dd087a70442bef789eb32f4`
- `docs/reviews/CURIS_RESPONSIBILITY_ROUTING_RUNTIME_IMPLEMENTATION_REVIEW.md`: `d4a9ecc6426dcaf883e71a411c8a30a721e30e285ed71b026d8c46eb051badd0`

## Explicit Exclusions

- 不修改 Product Blueprint、UI Blueprint 或 Frozen Authority。
- 不新增 UI、自由 DAG、自然语言万能 Router、负载均衡或 Organization Router。
- 不修改 `database.py`、`main.py`、`workspace.py`、legacy Workflow、Pipeline、Orchestrator。
- 不新增 Task；Handoff 复用现有 `HANDOFF` entity/lifecycle。
- 不新增第五套 Runtime、Collaboration Task、Review Task 或 Provider Session；Consult/Review 只作为同一 Work 的轻量持久化协作记录。
- 不推断 Workspace↔Department；不伪造跨层 Leader chain。
- 不 stage、commit、push。

## Runtime Truth

- Assignment 是 scoped canonical record；Holder、Current Executor、Employee Identity、Capability Binding 分离。
- Workflow version 是 immutable snapshot；运行中 Work pin vN，新 Work读取最新 vN+1。
- Default Flow 只是 Router 在 normal completion 时使用的 hint。
- Handoff 只传 Work、Assignment、Result/Artifact/Evidence refs 与短 context；不复制 Conversation。
- Holder 仅在 `CREATED→SENT→ACKNOWLEDGED→COMPLETED` 接受点后转移。
- Decision Gate 创建/复用同一 `DECISION_PACKET`，不伪装成 Handoff。
- Consult / Review 保持原 Responsibility Holder；只有真实责任转移才创建 Handoff。
- Review 的 revision 仅在 revision responsibility 与当前 Holder 不同时创建 Handoff；同责任修改不交接。
- Handoff ACK 是同一 SQLite transaction 内、完成 Holder transfer 前的 Runtime atomic acceptance；不伪装成人工确认或 Provider-native 回调。
- Business Operating Team 可在真实 `business_directions` scope 下运行，不强制伪造 Workspace；Company↔Business 的跨层 authority 仍保持未推断。
- Collaboration context 只保存 reference-first 摘要和成本；不创建 Provider Task/Session，不水合大段正文。

## Acceptance

1. Workspace/Business Assignment resolution。
2. Default next 与 dynamic deviation 均在同一 Work 内完成。
3. Explicit return、responsibility target、Workspace Leader escalation。
4. Holder transfer 后 Current Executor 仍独立且默认为 none。
5. Workflow vN pinning；编辑后新 Work使用 vN+1。
6. Employee binding / responsibility / order / input / output 编辑真实影响新版本 Runtime。
7. Result recovery、Decision Gate 与 restart persistence。
8. Reference-first context 有预算且不包含 Conversation history。
9. Handoff 不创建新 Task。
10. 内容增长与研发两个动态场景通过。
11. RD/XHS、Provider identity、Backend DB Safety focused no-regression。
12. Consult / Review holder-preserving，等待、重启、完成与 duplicate-safe 通过。
13. Review approve 可显式继续 default；request revision 仅在责任改变时 Handoff。
14. Business-only Operating Team scope 在无 Workspace 时可运行。
15. ACK atomic acceptance 在 transfer 前复核 Work、scope、workflow version、Holder、target Assignment/Employee 与 context refs。
16. Collaboration context cost 可读取，且新增 Task/Cycle/Provider Task/Provider Session 均为 0。
