# MVP Phase 4 / S6 — Capability Registry

Status: CLOSED — PASS

Owner seat: 系统交付席

Approval date: 2026-07-29

Expected review: `reviews/20260729_mvp_phase4_s6_capability_registry_review.md`

## Objective

按 Curis v1.0 既定 Capability 模型完成：

- T013：在唯一 Workspace Capability Registry 注册并管理 Model / Agent / Skill / Tool / Workflow / Connector 六类能力。
- T014：把现有 `skl_skill_*` 历史 Skill 迁移进统一 Registry。

## Product Boundary

- Capability 是 AI Employee 的资源，不作为独立业务入口，不改变 Project → Task 执行关系。
- 复用既有 `official_models` 统一能力目录、CapabilityCatalog、SkillRuntime 与员工 Capability Profile，不新增表、Admin 或第二套 Registry。
- MVP Workspace 下沉既有能力目录写能力；商业计费、配额、Marketplace 与平台发布仍冻结。
- 历史 Skill 保留原 `skill_templates`，以相同稳定 ID 登记进 Registry；因 `NOASSERTION / 不商用 / draft 候选` 边界，迁移后保持 inactive，禁止自动启用或实例化。
- S7 Model Gateway 调用、Fallback、成本统计与新的六类员工绑定不在本 Sprint 实现。
- 不存储或展示密钥、Token、Authorization 或凭证明文。

## Implementation

- 扩展既有统一目录使 `agent` 成为合法能力类型，并增加 Workspace Registry 的列表、详情、创建、启停和 Skill 迁移路由。
- Registry 输出使用固定安全字段，运行元数据只暴露描述、版本、I/O、状态和迁移来源。
- 能力中心与详情页改读真实 Registry，提供六类动态计数、创建、状态管理和历史 Skill 迁移。

## Allowed Files

- `issues/20260729_mvp_phase4_s6_capability_registry.md`
- `reviews/20260729_mvp_phase4_s6_capability_registry_review.md`
- `backend/app/main.py`
- `backend/app/catalog_constants.py`
- `backend/app/capability_catalog.py`
- `backend/app/capability_registry.py`
- `backend/tests/test_d5_capability_catalog.py`
- `backend/tests/test_mvp_phase4_s6_capability_registry.py`
- `frontend/lib/capabilities.js`
- `frontend/app/ceo-office/capabilities/page.js`
- `frontend/app/ceo-office/capabilities/CapabilityFormDrawer.js`
- `frontend/app/ceo-office/capabilities/[type]/[id]/page.js`
- `knowledge/NOW.md`
- `knowledge/CURRENT_CONTEXT.md`
- `PROJECT_STATUS.md`
- `TASKS.md`

## Acceptance

1. 用户可在唯一 Workspace Registry 查看并注册六类能力，不需要 Platform Admin。
2. 能力列表、详情、类型计数、来源、状态、版本与描述来自真实持久化数据。
3. 用户可启停普通 Registry 能力；不存在或非法类型明确失败。
4. 五个 `skl_skill_*` 历史 Skill 可幂等迁移，稳定 ID、描述和来源可追溯。
5. 历史 Skill 保持 inactive draft 候选，不能绕过许可边界自动启用。
6. Registry 响应和事件不含密钥、Token、Authorization、凭证明文或原始运行元数据 JSON。
7. 不新增依赖、数据库表、Admin、Marketplace、计费或模型调用。
8. 聚焦测试、Frontend lint/build、完整后端回归与 Desktop/Mobile 浏览器 E2E 通过。
