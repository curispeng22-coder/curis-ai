# R4 团队迁移 9b.3 敏感交接安全 Review

Issue：`issues/20260718_workspace_r4_team_migration_transfer_gate_9b3_sensitive_artifact_gate.md`  
结论：`PASS`

## 可保留的最小格式

迁移材料最多保留以下非秘密元数据：

```text
variable_name: <非秘密变量名>
source: <部署密钥设施 / 环境注入 / 受控运行时配置>
backfill: <部署时注入 / 运行前由授权席配置>
status: mapped | blocked
```

允许记录变量名、来源类别、回填方式和状态；不得记录来源路径中包含的秘密内容、连接串、实际值、可恢复材料或复制内容。来源必须写类别，不写密钥存储内容。

## 明确禁止

OpenAI/API Key、数据库连接串、密码、token、Cookie、JWT、member token、OAuth secret、Connector 凭据、完整 Authorization、私钥及运行凭据不得进入 `issues`、`reviews`、聊天交接、迁移包或任何文档附件。安全席不读取这些值。

## 缺失与回填

敏感变量缺少已批准的来源、责任席或回填方式时，状态必须为 `blocked`，迁移保持 `BLOCKED_L2`；不得用占位值、历史值、默认值、口头转交或猜测映射。只有部署/运行时由现有密钥设施注入，材料本身不承载凭据。

## 验收与回滚

只检查变量名、来源类别、回填方式和状态，不读取变量值；发现敏感值或不可追溯映射立即停止。回滚仅撤销文档引用/状态，不触碰 Secret、Key、数据库或运行凭据。

Next Seat：产品规划席。  
Handoff：sent to 产品规划席。
