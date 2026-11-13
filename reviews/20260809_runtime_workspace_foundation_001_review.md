# RUNTIME-WORKSPACE-FOUNDATION-001 Review

Status: Review  
Decision: `PASS_RUNTIME_WORKSPACE_WITH_EXTERNAL_ACTIVITY_DB_BASELINE`  
Date: 2026-08-09

## 1. 结论

已在授权封闭清单内实现 RD / XHS / TTK 共用的 Backend Workspace Runtime Foundation。
三条业务共享 Workspace / Blueprint Version / Simulation 内核，但 RD 使用 Cycle + 8 Stage，
XHS 与 TTK 各自使用独立 ContentItem / ContentVersion / PublicationReceipt /
InteractionItem。旧 Project / Task / workflow 只允许继续作为 `executionRef`，本 Issue 未调用、
迁移或修改旧链。

Backend Foundation 代码与测试已完成。产品负责人确认 `data/curis.sqlite` 是唯一活动库，
`backend/data/curis.sqlite` 是遗留副本；本 Issue 期间观察到的 SHA 漂移归入外部活动库基线，
不再作为本 Issue 的关闭阻塞。本 Issue 的显式命令与新测试只使用 `/tmp` / pytest tmp_path，
没有把活动库作为目标，也未覆盖、恢复、合并或清理任一数据库。

放行时只读快照：`data/curis.sqlite` SHA-256 为
`c663222af90129012e41b542780c9dffcd302b540e27074a13fbd62cce65321e`；遗留
`backend/data/curis.sqlite` SHA-256 为
`2ba1f018832fefa50e45692f54191f053e7c4f4caa5a6fea90ab87a59d7bd368`。后续 Runtime 与 UI
只能把前者视为活动库；遗留库不得作为回退、合并或测试目标。

未实现三业务 UI、Desktop、真实平台连接或 Operating Version 的 CEO 上线审批。

## 2. 实际改动文件

修改：

- `backend/app/runtime/foundation.py`
- `backend/app/runtime/simulation.py`
- `backend/app/api/runtime_foundation_router.py`
- `docs/00_Context/CURRENT_STATE.md`
- `docs/08_Change_Log/CHANGE_LOG.md`

新增：

- `backend/app/runtime/workspace.py`
- `backend/tests/test_runtime_workspace_foundation.py`
- `reviews/20260809_runtime_workspace_foundation_001_review.md`

## 3. Runtime 对象与不变量

### Workspace / Blueprint

- `business_type` 只接受 `RD | XHS | TTK`，保存于 Workspace Blueprint；
- RD Blueprint 必须包含 `INTAKE → DESIGN → IMPLEMENT → VERIFY → ACCEPT → REVIEW → IMPROVE → ARCHIVE`；
- XHS / TTK 必须包含独立内容 8 Stage，且 platform 必须匹配 Workspace；
- Blueprint 拒绝 prompt、API Key、credential、secret 和 raw payload 字段；
- `runtime_workspace_versions` 保存不可变版本、Blueprint、变更类型和变更原因；
- 历史版本号不能复用；草稿修改不覆盖运行对象原有 `blueprint_version` 或既有 `operating_version`。

### RD Cycle

- 第一个 RD Cycle 工作项固定为“完善 Curis”；
- 保存 outcomeRef、intentRef、owner、executionRef、8 Stage、currentStage、evidenceRefs 和 nextCheckAt；
- `executionRef` 不参与 Cycle / Stage 状态写入；
- Cycle 失败与 CEO 拒绝均经过既有 Cycle 状态机并保留审计。

### XHS / TTK Content Runtime

- 两个平台只能在各自 Workspace 创建 ContentItem；
- ContentItem 与首个 ContentVersion 在同一 SQLite `BEGIN IMMEDIATE` 事务内创建并建立 `HAS_VERSION`；
- 任一步失败整包回滚，不残留 orphan ContentItem / ContentVersion；
- 新版本只允许追加到 DRAFT ContentItem，旧版本不原地改写；
- PublicationReceipt 只追加；版本错配 fail-closed，不产生发布成功事实；
- InteractionItem 绑定同一 ContentItem / Company / Workspace，并保存 source、风险、ReplyPolicy 和 nextCheckAt；
- 不创建 CRM、真实平台发布或旧 content workflow 记录。

## 4. 受控 API

```text
POST /api/workspace/runtime/foundation/companies/{company_id}/workspaces
GET  /api/workspace/runtime/foundation/companies/{company_id}/workspaces/{workspace_id}
POST /api/workspace/runtime/foundation/workspaces/{workspace_id}/cycles
POST /api/workspace/runtime/foundation/workspaces/{workspace_id}/content-items
POST /api/workspace/runtime/foundation/workspaces/{workspace_id}/simulations
POST /api/workspace/runtime/foundation/workspaces/{workspace_id}/content-items/{content_id}/receipts
POST /api/workspace/runtime/foundation/workspaces/{workspace_id}/content-items/{content_id}/interactions
```

- 所有写操作要求显式 `ceo_id` 与可信 `TenantContext` CEO 身份一致；
- 若可信 membership 带 company_id，还必须与目标 Company 一致；
- Company / Workspace / ContentItem 关联均按 Tenant fail-closed；
- Workspace Simulation API 只接受 `RD-001 | XHS-001 | TTK-001`，subject 必须匹配业务类型、
  Company、Workspace 和当前 Blueprint Version；
- HTTP Receipt / Interaction 入口只接受 `CEO_MANUAL`；Manual Receipt 固定为
  `RECEIVED + UNVERIFIED`，recordedBy 必须是当前 CEO；
- `PLATFORM_API + VERIFIED` 只允许现有可信 Backend service integration 写入。因为真实平台 API
  明确不在本 Issue，HTTP 客户端伪装平台回执或互动返回 403；
- 安全投影不返回 prompt、密钥、credential、raw payload、堆栈或数据库路径。

## 5. 事务一致性

### ContentItem bundle

ContentItem、首版 ContentVersion 与 `HAS_VERSION` link 使用同一连接和
`BEGIN IMMEDIATE`。聚焦测试人为制造 ContentVersion 主键冲突，事务回滚后预期 ContentItem
不存在，证明无 orphan version / item。

### Blueprint revision

`revise_blueprint()` 只调用 `SimulationRuntime.invalidate_workspace()` 的单一事务边界；该事务同时：

1. 标记同 Workspace 历史 SimulationRun `invalidated_at / invalidation_reason`；
2. 更新 Workspace 当前 Blueprint JSON / Version；
3. 将 `simulation_passed` 归零；
4. 追加不可变 Workspace Version 快照与 changeReason。

非法 change_kind、重复当前版本或复用历史版本在写入前拒绝。测试确认失败请求后 Workspace
仍保持 v2，Version 历史仍只有 v1 / v2，没有部分 v3 或未配对的失效事实。

## 6. Simulation 与反查证据

- `subject:{cycleId}` 或 `subject:{contentId}` 持久化在 Simulation input refs；
- Workspace 安全投影返回 `subject_id`，可执行 `cycleId → simulationRunId` 与
  `contentId → simulationRunId` 反查；
- RD Cycle 投影返回 currentStage、完整 8 Stage 与 evidenceRefs；
- Content Workspace 投影返回 ContentItem、Version、Receipt、Interaction 与 Simulation；
- Manual Receipt 不能满足 XHS / TTK PASS；加入可信 `PLATFORM_API + VERIFIED` Receipt 后，
  在 handoff、CEO decision、真实非 fixture Evidence、finalState 全部齐备时才允许 PASS；
- Blueprint v1 Simulation 在 Workspace 升级到 v2 后保留历史终态但增加失效标记，不能作为 v2 通过证据。

## 7. Fresh / Restart / Isolation / Integrity

临时数据库根：

```text
/tmp/curis-runtime-workspace-evidence
```

聚焦验证覆盖：

- fresh schema 的 Workspace 行数为 0，不生成默认业务；
- 同 Company 独立创建 RD / XHS / TTK 三个 Workspace，business_type 数为 3；
- 服务重启后 Workspace、Blueprint Version、Cycle / Content / Simulation 投影一致；
- wrong CEO、跨 Tenant、同 Tenant 错 Company、错 Workspace / ContentItem 均 fail-closed；
- RD Cycle `FAILED` 与 `REJECTED` 独立保留；
- XHS 与 TTK ContentItem / Version 不混合；
- Manual / Platform Receipt 验证等级分别为 UNVERIFIED / VERIFIED；
- `pragma integrity_check = ok`；
- schema fresh / upgrade 一致性联合测试通过。

## 8. 测试结果

Workspace Foundation focused：

```text
4 passed
```

Runtime Foundation / Simulation / API / Materialization / First Arrival / Workspace / schema 联合回归：

```text
44 passed
```

Backend 全量：

```text
1285 passed, 31 failed, 2 skipped
```

相对上一阶段 `1281 passed, 31 failed, 2 skipped`，新增 4 个 Workspace Foundation 测试通过，
既有失败数保持 31。失败仍属于输入前 Model Gateway / default newapi seed、旧 Digital Employee
执行绑定、旧前端源码断言和 Tenant Model Preference 等清单外基线；本 Issue 未修改或掩盖。

命令异常说明：

- Backend 全量命令退出码非 0，是上述 31 项既有失败导致；失败数没有增加；
- 一条只读 SQLite 证据查询使用 shell 双引号执行 `json_extract(..., '$[0]')` 时，`$[0]`
  被 shell 展开，返回 `bad JSON path: '0'`。这是证据打印命令转义错误，不是产品测试失败，
  其余查询与 `pragma integrity_check` 正常；未重跑或修改数据库掩盖该错误。

## 9. Pre-existing Diff 与边界

- `backend/app/main.py` 未修改；Router 继续由既有注册入口自动装配；
- 未修改 frontend、prototype、Desktop、旧 Company / Project / Task / content workflow；
- 所有本 Issue 新增测试和显式服务命令均使用 pytest tmp_path / `/tmp/curis-runtime-workspace-evidence`；
- 活动库 SHA 漂移经产品负责人裁定为外部活动基线；`data/curis.sqlite` 为唯一活动库，
  `backend/data/curis.sqlite` 仅为遗留副本；本 Issue 未恢复、覆盖、合并或清理二者；
- 未调用真实小红书、抖音 / TikTok、GitHub、CI 或云平台 API；
- 未执行 reset、checkout、删除或 dirty tree 清理；全部 pre-existing diff 保留。

## 10. 已知限制与下一步

- 本 Issue 保存并保护 `operating_version`，但不实现 CEO 上线审批；当前新 Workspace 的
  operating_version 为 0，后续必须由独立授权的 Operating Version Issue 处理；
- 平台 VERIFIED Receipt / Interaction 只提供可信 Backend service 边界，不提供公共 HTTP
  伪装入口；真实 Connector 集成需独立 Issue；
- 当前没有三业务 UI、浏览器 Workspace 流程或 Desktop 证据。

当前结论为 `PASS_RUNTIME_WORKSPACE_WITH_EXTERNAL_ACTIVITY_DB_BASELINE`。Runtime Workspace
Foundation 已通过，允许在独立授权清单内进入三业务 Workspace UI；该结论不代表 UI、真实平台
或 Desktop 已完成。
