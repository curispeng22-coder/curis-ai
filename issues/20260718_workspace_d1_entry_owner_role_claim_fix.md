# Workspace：D1 入口 owner / CEO Claim 授权修复

- 状态：`CLOSED`
- 优先级：`P0`
- 当前责任席：系统交付席
- 安全复核：安全边界席
- 质量复核：质量运行席
- 父 Gate：`issues/20260718_workspace_d1_single_model_toolchain_entry_gate.md`

## 目标

在 D1 `_preflight` 创建唯一 claim 前复用既有身份角色校验，只允许 `owner` 或 `ceo` 角色进入；其他 active member 必须在模型、Tool、claim、写入之前 fail-closed。

## 最小修复

1. 复用现有可信身份 / membership 角色校验，不新增平行身份判断。
2. 角色非 `owner` / `ceo` 时返回既定拒绝，`model_call=0`、Tool=0、claim=0、写入=0。
3. 添加 focused 回归：错误角色、缺失角色、失效 membership 与合法 owner / ceo；每种负向路径均断言零模型 / 零 Tool / 零 claim。

## 禁止范围

- 不改角色模型、CEO 映射、模型/凭据/成本、D1 文件、pytest、前端或通用执行入口。
- 不启动、不注 Key、不调用、不出网。

## 验收

质量运行席独立复核角色拒绝和既有 D1 fixed-scope preflight；安全席确认复用可信身份链、无客户端角色覆盖。父 Gate 仅在双证据通过后重派收口。

## 收口结果

质量运行席在 `d57da0da` 复核：active owner / ceo 可进入；member、空角色、revoked 均为零模型 / 零 Tool / 零 claim，focused 6/6。安全边界席确认 `_claim_once` 前复用 TenantContext 当前 membership role，HTTP 无客户端 role / claim / scope 覆盖。见 `reviews/20260718_workspace_d1_entry_owner_role_claim_fix_review.md` 与 `reviews/20260718_workspace_d1_entry_owner_role_claim_fix_security_review.md`。
