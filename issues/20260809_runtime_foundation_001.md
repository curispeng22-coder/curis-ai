# RUNTIME-FOUNDATION-001：Curis Business Runtime Foundation

Status: Completed  
Decision: `IMPLEMENTED_REVIEWED_WITH_BASELINE_BLOCKERS`  
Product input: `PASS_TO_RUNTIME_FOUNDATION_REVIEW`  
Owner: Curis 产品 / Runtime 评审  
Date: 2026-08-09

本 Issue 已获得产品负责人目标中的代码委托授权，允许指定会话按封闭清单实施 Backend Runtime Foundation。
授权不包含前端、桌面壳、旧数据库、真实平台 API 或清单外文件；Runtime / Simulation / UI / Desktop 仍必须逐阶段验收。

实现输入快照：`docs/reviews/runtime-foundation-review-2026-08-09/INPUT_SNAPSHOT_2026-08-09.md`。

## 1. 目标

建立一套可持久化、可重启、可反查、可审计的 Business Runtime Foundation，使以下链路不再依赖旧 Project/Task 聚合、页面状态或内存对象：

```text
FoundingRun → Company → CEOAssistant → AIEmployee / RoleSlot / CapabilityBinding
→ Business / Workspace → Cycle / Handoff → Evidence / Acceptance
→ DecisionPacket → SimulationRun → 下一周期
```

研发工作台、小红书运营工作台、抖音 / TikTok 运营工作台共享该内核；研发工作台的第一个任务是“完善 Curis”，不是新的业务类型。

## 2. 实现范围（仅后端 Runtime）

1. FoundingRun / Company Formation：确认、恢复、拒绝、失败。
2. CEOAssistant：Company 唯一性、身份、Context、生命周期、升级 / 换责和质量快照。
3. AIEmployee / RoleSlot / CapabilityBinding：身份、汇报、授权、容量、撤权、缺能力、退回和 `orgVersion`。
4. 统一状态入口与审计：非法流转、错误 Actor、终态写入和 `from/to/trigger/actor/at/reason`。
5. Cycle / Handoff / DecisionPacket / Acceptance / Evidence：输入、输出、Owner、下一阶段、拒绝、回滚和关闭。
6. SimulationRun：正常、失败、CEO 拒绝、恢复、重启和按 Company / Workspace / Scenario 查询。
7. ContentItem、ContentVersion、ContentReview、PublicationReceipt、InteractionItem、InteractionResponse 最小契约。
8. 研发 Stage Runtime 与内容 Stage Runtime 对旧执行链的 `executionRef` 适配。
9. Workspace Blueprint 版本、`simulationPassed` 失效和 Operating Version 分离。
10. FIRST-ARRIVAL-001、ORG-001、RD-001、XHS-001、TTK-001 的最小 fixture / 手动证据入口；所有 fixture 结果保持 `UNVERIFIED`。

## 3. 封闭文件清单（候选）

### 3.1 允许修改的现有文件

- `backend/app/database.py`
- `backend/app/runtime/__init__.py`
- `backend/app/runtime/models.py`
- `backend/app/runtime/states.py`
- `backend/app/runtime/state_machine.py`
- `backend/app/runtime/registry.py`
- `backend/app/runtime/store.py`

### 3.2 允许新增的文件

- `backend/app/runtime/foundation.py`
- `backend/app/runtime/simulation.py`
- `backend/app/runtime/legacy_execution_adapter.py`
- `backend/tests/test_runtime_foundation_state_contracts.py`
- `backend/tests/test_runtime_foundation_persistence.py`
- `backend/tests/test_runtime_foundation_isolation.py`
- `backend/tests/test_runtime_foundation_simulation.py`
- `backend/tests/test_runtime_foundation_legacy_adapter.py`
- `reviews/20260809_runtime_foundation_001_review.md`

### 3.3 只有治理同步时允许修改

- `docs/reviews/runtime-foundation-review-2026-08-09/README.md`
- `docs/00_Context/CURRENT_STATE.md`
- `docs/08_Change_Log/CHANGE_LOG.md`

## 4. 禁止修改

- `frontend/`
- `curis-ui-prototype/`
- `desktop/`
- `data/curis.sqlite`
- `backend/data/curis.sqlite`
- `backend/app/main.py`
- 旧研发 / 内容运行模块（除非通过 Issue Amendment）
- 真实小红书、抖音 / TikTok API
- 旧表物理删除或历史数据回填

## 5. 必须证明的证据

- fresh / upgrade / 重复迁移一致性；
- 所有目标对象重启恢复；
- Tenant / Company / Workspace 隔离；
- 合法 / 非法状态转换和 Actor 校验；
- `WAITING_CEO` 不会被自动批准；
- 组织、能力、Connector、ReplyPolicy 或 Evidence Rule 变化使 Simulation 失效；
- 旧 Workflow 只保留为 `executionRef`；
- 以下反查链完整可查：

```text
foundingRunId → companyId → assistantId
assistantId → Brief / Handoff / DecisionPacket / Closeout
RoleSlot → AIEmployee → CapabilityBinding
cycleId → Handoff → Evidence → Acceptance → Decision
contentId → runId → outcomeId
interactionId → responseVersion → externalReceipt
```

建议测试命令：

```text
backend/.venv/bin/python -m pytest -q backend/tests/test_runtime_foundation_*.py
backend/.venv/bin/python -m pytest -q backend/tests
```

## 6. 前置阻塞与授权条件

在正式授权前必须解决：

1. Runtime Foundation Review 取得 `PASS`。
2. 选择完整 Foundation 范围；不能只实现 Content / Simulation 子集，否则 First Arrival 与 ORG Simulation 没有基础。
3. 明确 Runtime PASS 与 UI Browser Evidence 是两个阶段：Foundation / Simulation 先判定运行闭环；UI 迁移后再补人类浏览器证据。
4. 冻结输入文档到确定 Git 提交 SHA；不能以污染的工作树作为实现基线。
5. 使用临时数据库完成 fresh / upgrade / restart 验证；不得直接修改当前活动数据库。
6. 由产品负责人确认最终文件清单、输入 SHA、回滚方式和实现授权。

## 7. 后续路线（不属于本 Issue）

```text
Foundation PASS
→ FIRST-ARRIVAL / ORG / RD / XHS / TTK Simulation PASS
→ UI / 导航 / CEO Assistant / Workspace 迁移 Issue
→ Tauri 桌面壳接入目标 Runtime
→ .app 启动 / 重启 / 崩溃恢复 / 数据隔离 / 发布验证
→ 可投入使用的桌面应用
```
