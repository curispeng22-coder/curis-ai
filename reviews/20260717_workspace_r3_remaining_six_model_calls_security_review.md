# R3 剩余六次模型调用安全 Review

Issue：`issues/20260717_workspace_r3_remaining_six_model_calls_l2_gate.md`  
结论：`PASS`（仅六步有限调用安全契约；不等于六步已执行）。

## 前置复核

此前唯一阻塞已由正式证据解除：CEO 映射 Issue 已 `CLOSED — PASS`；总负责人批准 `ceo_id=ceo-f9d4d433-18af-45c9-8c16-f5ea31ecf5ae`；`membership-quality`（issuer `https://quality.issuer.local`、subject `quality-member-sub`、`tenant-a`、`company-a`、owner/active）与 active `company-a` 已写入同一值；active mapping=1、冲突=0、幂等待变更=0。该映射不是客户端 Header、Admin token、默认值或测试 fixture。

因此可信 CEO 前置满足，可复核并通过本六步有限调用契约。六步尚未执行，仍不得在本 Review 中宣称 R3 完成。

## 待批准后的唯一验收契约

- 仅 Run `wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc`，累计最多 7 次；每个指定 Step 最多一次。
- 顺序固定：`requirement_clarification → architecture_design → frontend_execution → backend_execution → qa_verification → final_report`。
- 每次 Adapter 调用前重新校验可信 subject、active membership、tenant/company/project、binding、可信 CEO、Provider/Model/Gateway/出口、前序状态、精确 Run+Step 计数和累计预算。
- 任何失败、重复、越界、顺序错误、预算超限或撤销均立即拒绝；不重试、不 Fallback、不跳步、不重置、不创建第二 Run。
- 首步 USD 0.001707，剩余六次最大 USD 0.09216，全 Run 最大 USD 0.093867，继续受 USD 0.10 硬上限约束。
- 回滚不得恢复旧额度、重复执行、Header-only CEO、默认 CEO 或跳过 UsageEvent。

## 结论边界

PASS 仅授权产品规划席提交总负责人确认后的既有有限调用契约，不授权实施或出网。每一步仍必须在 Adapter 前重新校验可信 CEO 映射、Run/Step 状态、精确计数和累计预算；任何失败立即停机。

实施前只允许 focused 的不出网测试；真实验收须逐步证明计数、顺序、失败停机、累计预算、撤销和脱敏审计，且必须先通过可信 CEO Gate。

Next Seat：产品规划席。  
Handoff：sent to 产品规划席。
