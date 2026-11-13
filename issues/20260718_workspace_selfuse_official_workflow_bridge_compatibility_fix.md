# Workspace：selfuse 迁移后的官方 Workflow 版本桥兼容修复

- 状态：`CLOSED`
- 优先级：`P0`
- 当前责任席：系统交付席
- 质量复核：质量运行席
- 父 Gate：`issues/20260718_workspace_real_rd_tool_closure_prerequisite_gate.md`

## 目标

修复 selfuse 迁移后官方 Workflow 来源不能被版本化 bridge 解析的回归，恢复 Wave1/2 的既有运行路径；不改变版本桥的精确来源和 fail-closed 安全边界。

## 已知证据

- 固定 SHA：`0947b9e6`。
- 全量：655 通过 / 28 失败 / 2 跳过 / 7 错误。
- 新增影响：Wave1/2 出现 8 个失败和 7 个错误，根因是 official Workflow 来源无法通过 bridge 解析。

## 最小范围

1. 追踪 selfuse 迁移与官方 Workflow 来源解析的共同入口，修复该入口的兼容性，不在各调用点打补丁。
2. 保持 Package / version / bridge / Workflow 版本的精确校验；禁止 default、latest、same-name、客户端覆盖或跨租户回退。
3. 补最小 focused 回归，覆盖 selfuse 官方来源的正向解析和缺失 / 版本错配 / revoked / design_only 的拒绝。

## 禁止范围

- 不改 Package / Bridge 资产、历史 Run、模型、网关、成本、前端或 Tool 实现。
- 不启动模型、不注 Key、不出网；provenance Step1 继续暂停。

## 验收

1. 系统交付席 focused 通过，并说明根因和公共修复点。
2. 质量运行席先验证 Wave1/2 新增失败与错误已解除，再重跑父 Gate 的全量回归。
3. 只有全量结果不再包含这 8 失败 / 7 错误，父 Gate 才可解除并进入第 2 步。

## 验证结果

质量运行席在 `f01b3df4` 独立复核：focused 28/28，Wave 扩展 45 通过 / 2 环境跳过；全量 671 通过 / 20 既有失败 / 2 跳过 / 0 错误。原 8 个失败和 7 个错误均清零，负向 fail-closed 保留。见 `reviews/20260718_workspace_selfuse_official_workflow_bridge_compatibility_fix_review.md`。
