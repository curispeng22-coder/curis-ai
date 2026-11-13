# Workspace 产品动线第一纵向切片

## Objective

在 48 小时内基于现有代码与页面做只读盘点，从两条候选中选定最快能真实闭环的一条产品动线；本 Issue 不写实现。

## Candidates

### A. 项目运行工作台

进入 Company / Department / Project → 与负责人设定目标 → 计划/启动 → 进度/成果 → 批准/返工/暂停。

### B. 模型、Agent、Skill/Tool、凭证配置

填写 → 安全保存 → 测试连接 → 绑定 → 可用状态。

## Required Evidence

每条候选仅核对：

1. 已有真实入口页面；
2. 用户实际操作；
3. 后端真实保存或执行；
4. 页面显示真实状态/结果；
5. 失败是否能被用户理解和处理。

复用既有 Company、Department、Project、Employee、RealRD、Task、Workflow、Secret Vault、CEO Evidence。若跨 WorkBuddy/Admin 的缺口确实存在，才建立 Shared Issue。

## Output

报告只写四项：

1. 新增前端可操作能力；
2. 已闭环动线；
3. 当前能力缺口；
4. 下一段。

## Boundaries

- 禁止实现、mock、页面假交互或为未来扩底座。
- `trusted identity source` 只读核对继续作为候选 A 的输入；若不存在，仅写“不存在”，不得设计临时替代。
- RealRD 单次取证、Key 准备、容器改造保持 `PAUSED_BY_USER_PRIORITY`。

## Route

系统交付席只读事实盘点 → 产品规划席选择唯一动线 → 总控确认后才建立实现 Issue。

## Selection And Result

**Status: CLOSED — A_SELECTED_IDENTITY_BLOCKED**。

首条锁定 A「项目运行工作台」。B 同时缺可信身份、Secret Vault 与连接测试三个敏感范围，不是最快真实闭环。

### 新增前端可操作能力

当前仅能真实宣称：打开页面 → 提交目标 → 项目/Task/Graph 计划保存 → 看到 DAG、空态或失败态。证据为 `9165f41f` 的浏览器/API Review。

### 已闭环动线

入口 → 提交目标 → 保存计划 → 显示 DAG；失败时页面明确显示且可重试/说明阻塞。

### 当前能力缺口

不存在可复用且已批准的可信 OIDC/OAuth 签发或交换源。生产 Gateway 因此拒绝真实操作；不得把 401 拒绝态写成可操作。Project 页尚未真实闭环启动 Run、成果/成本展示、审批/拒绝/返工；进程重启后仅能明确无动作，不能伪造进度。

### 下一段

总控若批准产品级可信登录入口，才建立其唯一实现 Issue；之后按同一 A 动线继续接真实启动、状态、成果、成本与决策。RealRD 取证继续暂停。
