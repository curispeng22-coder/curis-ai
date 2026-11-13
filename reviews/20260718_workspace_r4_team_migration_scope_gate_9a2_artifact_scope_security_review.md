# R4 团队迁移 9a.2 资产范围安全 Review

Issue：`issues/20260718_workspace_r4_team_migration_scope_gate_9a2_artifact_scope_gate.md`  
结论：`PASS`

## 允许范围

仅允许迁移或更新第 9 项相关的 `issues/*`、`knowledge/*` 收口说明及 `reviews/*` 收口契约引用。迁移动作只能更新引用关系，不能复制、移动或重建运行实体。

## 明确排除

以下内容一律禁止迁移、复制、移动、导出或回填：Admin 正式生产数据库、Workspace 历史执行数据库、生产/历史执行记录、Secret、Key、API key、Cookie、JWT、member token、Credential Vault 内容及任何运行凭据。安全席不读取这些值。

文档即使包含凭据路径、变量名或运行记录引用，也只能保留脱敏引用，不得携带值、可恢复材料或实体副本。

## 验收与回滚

迁移前后仅核对双方文档清单版本和引用一致性；发现数据库、凭据、历史执行实体或非第 9 项内容进入范围，立即停止并保持阻塞。回滚只撤销引用关系变更，不触碰任何数据库、Secret、Key 或运行实体。

Next Seat：产品规划席。  
Handoff：sent to 产品规划席。
