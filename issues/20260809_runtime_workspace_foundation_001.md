# RUNTIME-WORKSPACE-FOUNDATION-001：三业务 Workspace Runtime 基础

Status: Completed  
Decision: `PASS_RUNTIME_WORKSPACE_WITH_EXTERNAL_ACTIVITY_DB_BASELINE`  
Input: `PASS_TO_RUNTIME_FOUNDATION_IMPLEMENTATION_ONLY`  
Owner: Curis 产品 / Runtime 评审  
Date: 2026-08-09

## 1. 背景与目标

First Arrival 和 Company 物化已经通过，但 Company 仍没有真实业务 Workspace、Cycle、Stage
或 ContentItem 运行事实。现有 Project / Task / 旧 content workflow 只能作为内部执行适配，
不能作为 CEO 所见的业务状态。

本 Issue 只建立三条同步业务轨道共用的最小 Workspace Runtime 基础：

```text
Company
→ Workspace Blueprint 草稿 / 版本
→ Cycle 或 ContentItem
→ Stage / 版本 / 外部证据引用
→ SimulationRun
→ CEO 决策门
```

研发工作台第一个工作项固定为“完善 Curis”；小红书和抖音 / TikTok 各自产生独立
ContentItem，不把三条业务合并成一条固定内容管道。

## 2. 允许文件

允许修改：

- `backend/app/runtime/foundation.py`；
- `backend/app/runtime/simulation.py`；
- `backend/app/api/runtime_foundation_router.py`；
- `docs/00_Context/CURRENT_STATE.md`；
- `docs/08_Change_Log/CHANGE_LOG.md`。

允许新增：

- `backend/app/runtime/workspace.py`；
- `backend/tests/test_runtime_workspace_foundation.py`；
- `reviews/20260809_runtime_workspace_foundation_001_review.md`。

禁止修改 `backend/app/main.py`、任何 frontend、prototype、Desktop、活动数据库、旧
Company / Project / Task / content workflow 服务或清单外文件。保留所有 dirty diff。

## 3. 最小 Runtime 对象

### 3.1 Workspace

- Tenant / Company scoped；`business_type` 只允许 `RD | XHS | TTK`；
- 保存 Blueprint 草稿版本、运行版本、状态、Simulation 通过标记和变更原因；
- Blueprint / Stage / Agent / Capability / Connector / Platform Constraint / Reply Policy /
  Evidence Rule 任一变更必须使当前 Simulation 失效；
- 不创建默认 Workspace，不生成固定演示业务。

### 3.2 研发 Cycle

- `cycleId / workspaceId / outcomeRef / intentRef / lifecycleStatus / exceptionStatus /
  blueprintVersion / ownerRef / nextCheckAt`；
- 第一个 RD Cycle 的工作项名为“完善 Curis”；
- Stage 至少覆盖 `INTAKE → DESIGN → IMPLEMENT → VERIFY → ACCEPT → REVIEW → IMPROVE → ARCHIVE`；
- Project / Task / workflow 只能记录为 `executionRef`，不能改变 Cycle / Stage 状态。

### 3.3 内容对象

- XHS / TTK 必须独立创建 `ContentItem`，保存 platform、ContentVersion、当前 / 批准 /
  发布版本引用、生命周期、异常、验证状态、证据条件和下一检查点；
- ContentVersion 不可原地改写；CEO 拒绝回到 Draft 并保留版本审计；
- PublicationReceipt 只追加，平台 API 回执与 CEO 手动反馈必须区分来源和验证等级；
- InteractionItem 只建立最小绑定与风险 / ReplyPolicy / responseVersion 引用，不创建 CRM。

## 4. 最小受控 API

```text
POST /api/workspace/runtime/foundation/companies/{company_id}/workspaces
GET  /api/workspace/runtime/foundation/companies/{company_id}/workspaces/{workspace_id}
POST /api/workspace/runtime/foundation/workspaces/{workspace_id}/cycles
POST /api/workspace/runtime/foundation/workspaces/{workspace_id}/content-items
POST /api/workspace/runtime/foundation/workspaces/{workspace_id}/simulations
```

要求：

- 所有请求 Tenant scoped，写操作只接受明确 CEO；
- 每个写入都经过 Runtime Foundation / SimulationRuntime 和状态机，不直接更新 status；
- API 只返回安全投影，不返回 prompt、密钥、原始外部 payload 或隐藏思维链；
- Simulation 必须能关联 workspace / cycle / content item，并能记录失败、CEO 拒绝、手动反馈和外部回执；
- 不开放真实平台发布、不把 fixture 标记为 VERIFIED、不让前端任意写 `published`。

## 5. 必须证明

1. fresh / restart / Tenant / Company / Workspace 隔离与 integrity；
2. 三种 Workspace 可独立创建、查询和修改 Blueprint，互不混合；
3. RD “完善 Curis” Cycle 与 XHS / TTK ContentItem 独立持久化；
4. Blueprint 变更使关联 Simulation 失效，运行版本不被草稿覆盖；
5. CEO 拒绝、失败、未授权 / 手动反馈和版本错配安全阻断；
6. `contentId → simulationRunId → outcome / receipt` 与 `cycleId → stage → evidence`
   的反查键可查询；
7. Runtime Foundation / Simulation / API / First Arrival 联合回归不下降，全量基线失败数不新增；
8. 不修改 frontend、Desktop、prototype、活动数据库或旧执行链。

## 6. 明确不在本 Issue

- 三业务 Workspace UI、导航与视觉实现；
- 真实小红书、抖音 / TikTok、GitHub、CI 或云平台 API；
- 完整 AI 员工招聘 / 能力配置 UI；
- 真实外部成交、互动回复和商业化 Admin；
- 删除旧表、迁移旧 Project / Task 数据或修改旧执行状态。

## 7. 关闭条件

生成 `reviews/20260809_runtime_workspace_foundation_001_review.md`，记录 API、对象、状态机、
版本失效、三业务独立性、失败 / CEO 拒绝、重启 / 隔离、测试和临时 SQLite 证据。完成后暂停，
等待独立 Review；未通过前不得实现三业务 UI。

独立 Review 已通过。产品负责人确认 `data/curis.sqlite` 为唯一活动库、
`backend/data/curis.sqlite` 为遗留副本，并将本 Issue 期间观察到的活动库 SHA 漂移归入外部基线。
该裁定不授权任何数据库恢复、合并或清理。
