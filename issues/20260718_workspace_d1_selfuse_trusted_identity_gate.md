# Workspace：D1 selfuse 可信 Owner / CEO 身份前置 Gate

- 状态：`CLOSED`
- 优先级：`P0`
- 发起：产品规划席
- 决策：总控决策席
- 安全复核：安全边界席
- 父 Issue：`issues/20260718_workspace_real_rd_tool_e2e_d1_tenant_reservation.md`

## 阻塞事实

D1 入口固定 scope 是 `selfuse`，并在 claim 前要求 active `owner` / `ceo` 与非空 `ceo_id`。当前 `quality.sqlite` 的 `selfuse` 没有符合条件的可信 membership；现有 membership 属于 `tenant-a`，不能替代。

## 裁决请求

只允许裁决一个最小方案：

1. 对 `selfuse` 进行一次性、可审计、幂等的可信 owner / CEO membership + CEO 映射 provisioning；或
2. 正式修订 D1 固定身份 scope，并重新做完整安全 / 质量预检。

无论选择哪一项，都不得使用客户端 Header、默认身份、Admin token、同名推断或跨 tenant 复用。

## 安全要求

- 仅服务端可信 issuer / subject → active membership → selfuse → owner / ceo → 非空 CEO 的精确链。
- 冲突、重复、撤销、过期、跨 tenant、role 不符或 CEO 不一致均 fail-closed、零 claim / 模型 / Tool / 写入。
- 不启动、不注 Key、不调用模型、不读写 D1 目标、不修改历史 Run / Usage；不得输出凭据或身份原文。

## 后续

安全与总控批准后才可建立一次性受控 provisioning Issue；该 Issue 质量 PASS 后，再重新静态核验唯一隐藏注入命令。

## 安全复核结论

安全边界席结论为 `BLOCKED_L2`，唯一建议是停机、一次性、`BEGIN IMMEDIATE`、幂等、脱敏审计的 selfuse trusted provisioning，不修订 D1 scope。可信链必须是“受信 issuer + subject → active membership(selfuse, owner) → active Company → 同值非空 `ceo_id`”；冲突、重复、撤销、过期、CEO 不一致或审计缺失均整体 rollback，D1 claim / 模型 / Tool / 写入保持零。

当前唯一缺口是总控批准 selfuse 的精确 issuer + subject 映射；不得猜测、合成或用 Header/default/Admin token/跨租户身份替代。见 `reviews/20260718_workspace_d1_selfuse_trusted_identity_gate_review.md`。

## 总控批准输入

- issuer：`https://quality.issuer.local`
- subject_id：`quality-member-sub`
- 目标：现有唯一 `selfuse` tenant；创建一条新的 active `owner` membership 与同值非空 CEO / active Company 映射。

实施仅限 `issues/20260718_workspace_d1_selfuse_trusted_provisioning.md`。Provisioning PASS 不恢复 D1；之后仍需重新静态预检与质量 Gate。

Provisioning 已由质量运行席 PASS；身份前置 Gate 收口，现仅允许重做 D1 静态预检。
