# R4 团队迁移 9a.3 排除边界安全 Review

Issue：`issues/20260718_workspace_r4_team_migration_scope_gate_9a3_exclusion_gate.md`  
结论：`PASS`

## 不可迁移与不可扩展

本轮排除新前端、AI Secretary、Dashboard、第三方 OAuth/Connector、生产账务/计费、外部 billing，以及未形成既定审计链路的数据清理。不得借迁移名义读取、复制、重建或变更这些资产和依赖。

Secret、Key、OAuth token、Connector 凭据、账务数据、隐私数据和跨租户运行实体均不进入迁移范围；安全席不读取密钥值。

## 新范围阻断

任何新范围必须先交总控决策席裁决；涉及身份、凭据、外部服务、隐私或跨租户时并行交安全边界席。裁决前冻结，不得在第 9 项内顺手扩展、清理、外部联通或改变审计链路。

## 回滚

仅可回滚已批准的文档引用或迁移清单变更；不得触碰生产数据库、外部服务、凭据、历史执行数据或未审计清理对象。

Next Seat：产品规划席。  
Handoff：sent to 产品规划席。
