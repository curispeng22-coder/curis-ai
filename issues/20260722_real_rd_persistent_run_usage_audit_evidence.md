# RealRD Persistent Run / Usage / Audit Evidence

## Objective

复用既有 RealRD Run、Usage 与 Audit 持久化，使同一 RealRD Run 能外部可追溯地关联模型 Token/价格/成本与每次工具执行审计。

## Scope

- 仅复用现有 Run/Step/Tool、Usage 与 Audit 数据模型及持久化路径；不建立分析平台、报表中心或第二套执行状态机。
- 每次工具执行审计与同一 Run/Step/Tool 精确关联；同一模型调用的 Token、价格、成本可回查到该 Run。
- 先完成无外网实现与 focused 验证；质量 PASS 后，另行申请一次真实调用取证。

## Security Boundary

- 审计不得记录 prompt、原始 diff、token、Authorization、Cookie、绝对路径或其他敏感原文。
- 只允许脱敏、可回查的关联标识、事件类型、时间、工具结果摘要、Token/价格/成本与撤销状态。
- 本 Issue 不注入 Key、不启模型、不出网、不做真实调用。

## Acceptance

1. 无外网 focused 验证证明一个 Run 的每个工具执行审计均能关联至精确 Run/Step/Tool。
2. 模型 Usage 的 Token、价格、成本可与同一 Run 关联；缺失或不一致 fail-closed，不伪造零值。
3. 持久记录不包含 prompt、原始 diff、token、Authorization、Cookie 或绝对路径。
4. 系统交付完成 focused 验证；质量运行席独立复核。质量 PASS 不等于真实调用取证 PASS。

## Non-goals

- 不新增模型/Provider/Gateway，不启动身份主线，不做前端、分析平台、Billing 或批量历史回填。
- 不修改既有历史 Run/Usage/Audit 来补造证据。

## Route

系统交付席单主线程无外网实现与 focused 验证 → 质量运行席独立复核 → 产品规划席收口；真实调用另立一次性 Gate。

## Implementation Evidence

- Status: 无外网持久化门 `PASS`；不等于真实调用取证。
- SHA: `a04b9d28`；质量独立 focused `34 passed / 2.35s`，`diff-check PASS`。
- 已验证：Run/Step/Tool 关联、Token/价格/成本持久化、scope/price/cost 写前 fail-closed 与敏感原文禁入。
- 后续仅可由单独的一次真实调用 Gate 取证；未获批准前不启动模型、不注入 Key、不出网。
