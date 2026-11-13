# 2026-07-18 Workspace R4 Agent Mode 失效/拒绝边界复核

- Issue：`issues/20260718_workspace_r4_agent_mode_failclosed_gate.md`
- 固定分支：`feat/roadmap-r1r2`
- 证据数据库：`deploy/curis/gateway/.generated/data/quality.sqlite`
- 结论：`PARTIAL`

## 复核范围

- 只读核验失败链路，确认失败后不隐式降级，且有显式拒绝原因。
- 只抽样 3 条失败 run 与 1 条运行 run。

## 结果

### 1）失败拒绝可复核

- 失败 run：
  - `wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc`
    - step6 失败，原因：`Model gateway input exceeds the approved limit`
  - `wfr-ecc7d911-f851-4c94-b4d6-98f657ad52f6`
    - step1 失败，原因：`X-Ceo-Id is required to write UsageEvent`
  - `wfr-69926fdb-21a2-4166-b6c6-37059309d7ff`
    - step1 失败，原因：`Model gateway request failed: <urlopen error [Errno -3] Temporary failure in name resolution>`

- 统一复核到的事件都有 `workflow.step.failed` 与 `workflow.run.failed` 双条记录，且都写明 `reason`。

### 2）失败后不得继续推进

- 3 个失败 run 的后续 step 全部 `pending`，不存在 `failed` 后出现 `running/succeeded/completed`（直接或间接）的证据：
  - `wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc`：失败在 step6，step7 pending
  - `wfr-ecc7d911-f851-4c94-b4d6-98f657ad52f6`：失败在 step1，step2+ pending
  - `wfr-69926fdb-21a2-4166-b6c6-37059309d7ff`：失败在 step1，step2+ pending

### 3）绑定/会话面向链路

- 失败链路中的已执行失败 step 均有可追溯的 `employee_id/employee_role/capability_binding_id`。
- 当前数据库样本内未出现“当前 step 已执行但绑定缺失导致失败”的失败样本；
- 当前样本内未出现“tenant/project/employee 明确失配失败”的失败样本。

## 结论

- 在现有历史样本中，Agent Mode 失败边界具备 **显式拒绝 + 无继续推进** 结论，符合 fail-closed 的核心闭环。
- 但 `作用域错配（tenant/project/employee）` 与 `绑定缺失直接命中失败` 的反例样本仍未观测到，需在后续新增 run 中补齐一类对照样本后转 `PASS`。

Handoff: sent to 产品规划席（确认定义）