# Workspace：D1 单次模型到受控工具链入口 Gate

- 状态：`CLOSED`
- 优先级：`P0`
- 发起：产品规划席
- 决策：总控决策席
- 安全复核：安全边界席
- 架构意见：系统交付席
- 父 Issue：`issues/20260718_workspace_real_rd_tool_e2e_d1_tenant_reservation.md`

## 缺口

当前默认 `create_app` 未注册 `LocalRDToolset`、唯一 `command_id` 或 D1 的“单次模型 → 受控 diff → 固定 Tool 链”入口。`start-local` 只能启动既有 R3 Workflow 模型 Gate。用内联 Python / Shell 拼接入口会违反禁止通用执行器的边界。

## 请求的最小方案

仅为 D1 Issue 增加一个服务端、不可泛化的入口：接受已固定的两读/一路径、4 KiB diff、唯一 `command_id` 与既有模型 Gate 的单次输出；依次调用既有 LocalRDToolset 的 Reader / Search / Writer / Test Runner / Git Client；所有输入均服务端固定，客户端不得覆盖。

## 不可扩大

- 不做通用 Agent、通用 Shell / Python、任意命令、任意路径、动态 Tool 选择或第二模型调用。
- 不改 Provider、Model、Gateway、成本规则、前端、Admin 资产或 provenance Step1。
- 未裁决前不启动、不注 Key、不调用、不读写 D1 文件、不运行测试。

## 决策后验收

若获批准，安全与交付必须证明：入口只可在 D1 固定范围内运行；所有 preflight、敏感扫描、diff、命令、审计、零模型 Tool Usage、失败停机与无 fallback 均复用既有已验收边界。完成后交质量 focused 复核；D1 模型调用仍须在该入口 PASS 后执行。

## 安全契约已通过

安全边界席已在 `reviews/20260718_workspace_d1_single_model_toolchain_entry_security_review.md` 给出 PASS。入口不得接受客户端参数；固定 D1 Run / scope、两输入、唯一脚本、4 KiB diff、唯一 command_id / argv 和 Reader/Search→Writer→TestRunner→GitClient 顺序。禁止通用 ToolExecutor fallback、dynamic planner、Shell、Python、任意 Tool 与第二模型调用；任一 preflight / 扫描 / preimage / 审计 / Key 存在性失败均零写入并停止。本 PASS 不授权启动、注 Key 或模型调用。

## 实施授权

总控已批准仅实现本 Gate 所述不可泛化 D1 服务端入口及无出网 focused 验证。模型、凭据、Token / 成本 Gate 继续独立冻结；实施阶段不得启动、注 Key、调用模型、执行目标写入或运行 D1 pytest。

## 当前质量阻塞

质量复核发现 `_preflight` 没有限制 `identity.role` 为 `owner` / `ceo`；普通 active member 如有 CEO 映射可能抢占唯一 claim，并在 Key 存在时触发模型。唯一修复项为 `issues/20260718_workspace_d1_entry_owner_role_claim_fix.md`；修复前父 E2E 保持等待，不得启动。

角色修复已获质量与安全双 PASS，现重派父入口静态收口。真实模型调用仍未获此处授权。

## 收口结果

质量运行席在 `d57da0da` 独立复核：unittest 12/12、compileall / diff-check PASS；固定空请求 / scope、owner / ceo claim、Reader→Search→Writer→唯一 TestRunner→Git diff / check、单次 claim、无 planner / fallback 与失败回滚同修订成立。见 `reviews/20260718_workspace_d1_single_model_toolchain_entry_gate_review.md`。本 Gate 的 `BLOCKED_L2` 已解除，但不替代父 E2E 的模型 / 凭据 Gate。
