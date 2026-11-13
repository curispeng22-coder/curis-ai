# Workspace D1 入口 owner / CEO Claim 修复安全 Review

- Issue：`issues/20260718_workspace_d1_entry_owner_role_claim_fix.md`
- 结论：`PASS`（仅安全边界复核；不授权启动、注Key、模型调用或扩大 D1 范围）
- 质量依据：`reviews/20260718_workspace_d1_entry_owner_role_claim_fix_review.md`

## 结论与证据

1. D1 `_preflight()` 从 `TenantContext.current_identity()` 读取服务端当前身份，并同时校验固定 tenant、`membership_status=active`、`role in {owner, ceo}`、非空 `ceo_id` 和 `request_id`。
2. 该角色判断位于 `_claim_once()` 之前；拒绝路径不会进入唯一 claim、Reader/Search、Writer、TestRunner、GitClient 或模型调用。因此错误角色、空角色和 revoked membership 均满足零模型、零 Tool、零 claim、零业务写入。
3. `TenantContext` 的生产身份来自可信 Gateway → active membership 查询，角色取自 membership；issuer、subject、tenant 和 company 关系由服务端校验。D1 路由不接收客户端 role、claim、project、task、run 或路径参数；tenant 仅作为服务端 membership 查询的目标选择，不能单独授权；HTTP 请求体非空也直接拒绝。
4. 现有 focused 质量证据为 6 passed；负向用例覆盖 `member`、空角色和 revoked membership，均断言 model=0 且 Reader/Writer/Git/claim 调用合计为 0。安全席未启动服务、未读凭据、未注Key、未调用模型或出网。

## 安全边界

- 仅复用既有身份 / membership / TenantContext 链，不新增角色模型、CEO 映射、平行身份源或客户端 role/claim 授权分支。生产配置拒绝 self-use/test 身份模式；测试适配器不构成生产授权。
- `owner` / `ceo` 是 D1 入口唯一允许角色；普通 active member 不因拥有 `ceo_id` 而获得 claim 权限。
- D1 专用入口的固定 scope、Provider/Model/Gateway、凭据、Token/成本和受控 Tool 链不因本修复改变。Provenance Step1 仍为 `PAUSED_BY_NEW_PRIORITY`。
- 本 PASS 仅解除 owner/CEO claim 授权修复的安全阻塞；不等同真实模型执行或 D1 E2E 通过，后者仍须遵守既有 `WAIT_FOR_OWNER_INJECTION` / 总控 Gate。

## 交接

Next Seat：产品规划席
Handoff: sent to 产品规划席
