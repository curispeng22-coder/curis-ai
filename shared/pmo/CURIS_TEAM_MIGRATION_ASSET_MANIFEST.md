# Curis Codex / WorkBuddy 团队迁移资产清单

- 清单版本：`curis-team-migration-manifest/1.0.0`
- 唯一权威路径：`shared/pmo/CURIS_TEAM_MIGRATION_ASSET_MANIFEST.md`
- 生效日期：2026-07-18
- 范围：仅登记第9项现有文档引用，不承载或迁移实体内容

## 版本规则

- Codex 与 WorkBuddy 只能引用本文件及同一版本号，不得复制清单正文或维护第二份清单。
- 条目变化必须发布新版本；旧版本保留原行级内容，不就地改写历史版本语义。
- 清单条目只证明文档引用范围，不授权移动、复制、导出或回填任何实体。

## 资产条目（逐行固定）

| 条目 | 类型 | 路径 | 用途 |
| --- | --- | --- | --- |
| `TM-001` | Issue | `issues/20260718_workspace_r4_codex_workbuddy_team_migration_gate.md` | 第9项总 Gate |
| `TM-002` | Issue | `issues/20260718_workspace_r4_team_migration_rollout_queue.md` | 串行任务队列 |
| `TM-003` | Issue | `issues/20260718_workspace_r4_team_migration_scope_gate.md` | 9a 范围 Gate |
| `TM-004` | Issue | `issues/20260718_workspace_r4_team_migration_scope_gate_9a1_owner_boundary_gate.md` | 9a.1 职责边界 |
| `TM-005` | Issue | `issues/20260718_workspace_r4_team_migration_scope_gate_9a2_artifact_scope_gate.md` | 9a.2 资产范围 |
| `TM-006` | Issue | `issues/20260718_workspace_r4_team_migration_scope_gate_9a2_canonical_manifest_fix_gate.md` | 9a.2 同源清单修复 |
| `TM-007` | Issue | `issues/20260718_workspace_r4_team_migration_scope_gate_9a3_exclusion_gate.md` | 9a.3 禁止项与依赖 |
| `TM-008` | Issue | `issues/20260718_workspace_r4_team_migration_scope_gate_9a_rollup_gate.md` | 9a 汇总 Gate |
| `TM-009` | Issue | `issues/20260718_workspace_r4_team_migration_transfer_gate.md` | 9b 交接 Gate |
| `TM-010` | Issue | `issues/20260718_workspace_r4_team_migration_transfer_gate_9b1_handoff_contract_gate.md` | 9b.1 交接契约 |
| `TM-011` | Issue | `issues/20260718_workspace_r4_team_migration_transfer_gate_9b2_fail_rollback_gate.md` | 9b.2 失败回滚 |
| `TM-012` | Issue | `issues/20260718_workspace_r4_team_migration_transfer_gate_9b3_sensitive_artifact_gate.md` | 9b.3 敏感资产边界 |
| `TM-013` | Issue | `issues/20260718_workspace_r4_team_migration_transfer_gate_9b_rollup_gate.md` | 9b 汇总 Gate |
| `TM-014` | Issue | `issues/20260718_workspace_r4_team_migration_closeout_gate.md` | 第9项收口 Gate |
| `TM-015` | Review | `reviews/20260718_workspace_r4_team_migration_scope_gate_9a1_owner_boundary_gate_review.md` | 9a.1 质量证据 |
| `TM-016` | Review | `reviews/20260718_workspace_r4_team_migration_scope_gate_9a2_artifact_scope_gate_review.md` | 9a.2 质量证据 |
| `TM-017` | Review | `reviews/20260718_workspace_r4_team_migration_scope_gate_9a2_artifact_scope_security_review.md` | 9a.2 安全证据 |
| `TM-018` | Knowledge | `knowledge/NOW.md` | 当前 Gate 指针，不复制历史正文 |

## 明确禁止项

- Admin 正式生产数据库、Workspace 运行或历史数据库、任何数据库副本与恢复材料。
- 公司、部门、项目、员工、Workflow、Task、Run、Result、Execution、Usage 或审计记录等运行实体。
- Secret、Key、API key、Cookie、JWT、member token、Credential Vault 内容、环境文件及任何运行凭据或可恢复派生值。
- 源码、前端、构建产物、依赖目录、缓存、日志原文和非第9项文档。
- 复制、移动、重建、导出、回填、改写历史或以同名文件维护清单副本。

## 双侧唯一引用

- Codex 引用入口：`issues/20260718_workspace_r4_team_migration_scope_gate_9a2_canonical_manifest_fix_gate.md`。
- WorkBuddy 注册工作区：`/Users/yy/Documents/Curis AI Workspace`（登记证据：`/Users/yy/.workbuddy/app/sessions.json` 的 `workDir`）。
- WorkBuddy 引用入口：`.workbuddy/memory/MEMORY.md`。
- 两侧引用版本：`curis-team-migration-manifest/1.0.0`。
- 两侧引用目标：`shared/pmo/CURIS_TEAM_MIGRATION_ASSET_MANIFEST.md`。

## 回滚

- 仅删除两侧新增的版本/路径引用并撤销本清单文档；不得触碰任何数据库、凭据、运行实体或历史记录。
