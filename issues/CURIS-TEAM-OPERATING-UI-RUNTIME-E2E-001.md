# CURIS-TEAM-OPERATING-UI-RUNTIME-E2E-001

Authority Class: CURRENT · IMPLEMENTATION
Status: Implemented · CEO Review Required
Date: 2026-08-19
Accepted Runtime Baseline: `abb60e040`

## Goal

把产品中的“团队运转 / 默认流程”通过最小 UI/API Adapter 接到已接受的 `ResponsibilityRoutingRuntime`，并用内容增长 Workspace scope 与研发 Business scope 证明：UI 编辑发布 immutable version，New Work pin 新版本，Default Flow 可被 Consult / Return 动态偏离，且不创建第五套 Runtime。

## Allowed Files

- `backend/app/api/team_operating_router.py`（新增）
- `backend/app/api/runtime_foundation_router.py`（仅注册 Adapter）
- `backend/tests/test_team_operating_adapter.py`（新增）
- `frontend/lib/runtimeApi.js`（仅新增 Team Operating API client）
- `frontend/components/workspace/TeamOperatingDefinitionEditor.js`（新增）
- `frontend/components/xhs/XhsWorkspacePhaseOne.js`（仅嵌入团队运转区）
- `frontend/tests/teamOperatingDefinitionEditor.test.mjs`（新增）
- `issues/CURIS-TEAM-OPERATING-UI-RUNTIME-E2E-001.md`
- `docs/reviews/CURIS_TEAM_OPERATING_UI_RUNTIME_E2E_REVIEW.md`（新增）

Pre-change SHA-256：

- `backend/app/api/runtime_foundation_router.py`: `f8773324ebb2b2ab29e3ecb54057aff49af651e96bffbdfef58dd25d0fb9ec23`
- `frontend/lib/runtimeApi.js`: `57c6450224f4d2e6f1a65d36fd0348b3c99934ae238f179f569542ce409e59a0`
- `frontend/components/xhs/XhsWorkspacePhaseOne.js`: `cc04d82cd5de0f80506b0e943f3d050f9a852eece2c8bc13906f319328515743`

## Runtime Contract

- Frontend 不直接写 `runtime_entities`；Adapter 翻译产品 payload 与 canonical Assignment / Workflow snapshot。
- Add/Delete/Reorder/Responsibility/Employee/Input/Output 的保存发布 immutable vN+1。
- Running Work 继续 pinned vN；New Work读取 latest vN+1。
- Default Flow 是 hint，不是 mandatory sequence。
- Scope 必须显式为 Business 或 Workspace；Adapter 不替用户决定是否创建 Workspace。
- Consult / Review holder-preserving；Handoff / Decision 继续复用 accepted Runtime。

## Explicit Exclusions

- 不修改 Product Blueprint、Master Map、UI Blueprint 或 Frozen Authority。
- 不迁移全部 RD/XHS Domain Runtime，不重写 accepted Domain flow。
- 不新增 DAG、Workflow Engine、Task、Provider Session、Schema 或第五套 Runtime。
- 不重新设计页面；只接真实产品前端的轻量 Inline Editor。
- 不伪造 Provider execution；Routing E2E 与 Provider execution truth 分开报告。
- 不修改活动 SQLite；不 push。

## Acceptance

1. API读取当前 definition / published version / assignments / pinned Work 状态。
2. UI可增删、拖动排序、修改责任、Employee、Input、Output并发布。
3. invalid Employee、scope、zero/multiple Assignment fail closed。
4. Drag reorder 真实改变新版本 Default Flow，而非 mandatory route。
5. Employee / responsibility / input / output 进入新 Assignment snapshot。
6. Running Work pin v1；New Work pin v2。
7. 内容增长完成 Default + Consult + Return + Result recovery。
8. 研发 Business scope 完成 holder-preserving Consult 与真实 Return。
9. restart 后 definition、Work、collaboration、Result 可恢复。
10. Context cost、0 copied Conversation、Task/Session count 可审计。
11. focused + existing Runtime/XHS/RD/DB Safety no-regression。
12. Active DB size/mtime/SHA/integrity 不变。

## Implementation Result

- Runtime baseline commit: `abb60e040` (`feat(runtime): add responsibility routing control plane`).
- Product API/UI Adapter、immutable version、Business/Workspace scope、Content Growth/RD E2E 已实现。
- Browser UI 发布 v2：`topic → research → visual → copy → publish`；同一隔离库后端重启后仍读取 v2。
- 严格 pointer-drag 的自动化操作未能在 Browser/Chrome 触发 native drag event；可访问的上移/下移排序已真实发布 v2。该点交 CEO Review，不冒充 pointer-drag 已验收。
- Provider execution 未在本 Issue 伪造；Routing E2E 保持 0 provider Task / Session。
