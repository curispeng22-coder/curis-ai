# Workspace：D1 selfuse 一次性可信 Owner / CEO Provisioning

- 状态：`CLOSED`
- 优先级：`P0`
- 当前责任席：系统交付席
- 质量复核：质量运行席
- 父 Gate：`issues/20260718_workspace_d1_selfuse_trusted_identity_gate.md`

## 唯一目标

仅对现有唯一 `selfuse` tenant 建立一个可信、active 的 `owner` membership 与同值非空 CEO / active Company 映射，使 D1 固定 scope 能在后续静态预检中被可信验证。

## 固定输入

- issuer：`https://quality.issuer.local`
- subject_id：`quality-member-sub`
- 实际执行库：`deploy/curis/gateway/.generated/data/quality.sqlite`
- operation_id：由服务端在本次执行前生成并固定；同一 operation 只可幂等返回同一写入结果或整体拒绝。

## 受控写入边界

1. 服务全停、同一数据库、`BEGIN IMMEDIATE` 事务内执行；不提供 API、Header、Admin token 或外部网络入口。
2. 只新增本次所需 membership、CEO / Company 映射及脱敏 append-only 审计；不改 `tenant-a`、历史 Run / Usage、Package、Bridge、Workflow 或其他历史数据。
3. 写入前后精确核对 issuer / subject → selfuse → active owner → active Company → 同值非空 `ceo_id`。
4. 冲突、重复、非唯一、撤销 / 过期、CEO 不一致、写入计数或审计失败均整体 rollback；D1 claim / 模型 / Tool / 写入保持零。
5. HMAC 审计 Key 缺失即停止且不读取、不输出其值；审计不得含凭据、Header、Cookie、JWT、subject 原文或 D1 文件内容。

## 禁止范围

- 不启动 D1、不注 Key、不调用模型、不读写 D1 目标、不跑 D1 pytest、不出网。
- 不修订 D1 scope，不复用 tenant-a 或默认 / 客户端身份。

## 验收

质量运行席停机只读确认：同库唯一 active owner membership、active Company、同值非空 CEO 映射和 operation 审计成立；负向冲突 / 撤销条件 fail-closed；D1 Run / claim / Tool / Usage 仍为零，端口全关闭。

PASS 只允许重做 D1 静态预检与质量 Gate，不恢复模型调用。

## 收口结果

质量运行席确认固定 selfuse owner → active Company → 同值 CEO 唯一链、单条脱敏审计、幂等零重复、冲突零残留、D1 零副作用和端口全关闭均成立。见对应质量 Review；本 Issue 不授权启动、Key 或模型。
