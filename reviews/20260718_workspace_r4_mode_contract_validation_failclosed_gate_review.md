# 2026-07-18 Workspace R4 Mode 闭环验收（M4b）复核记录

- Issue：`issues/20260718_workspace_r4_mode_contract_validation_failclosed_gate.md`
- 固定分支：`feat/roadmap-r1r2`
- 复核数据库：`deploy/curis/gateway/.generated/data/quality.sqlite`
- 结论：`PASS`（fail-closed 核验成立）

## 取样失败 run

- `wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc`  
  - 失败 step：6
  - reason：`Model gateway input exceeds the approved limit`
- `wfr-ecc7d911-f851-4c94-b4d6-98f657ad52f6`  
  - 失败 step：1
  - reason：`X-Ceo-Id is required to write UsageEvent`
- `wfr-69926fdb-21a2-4166-b6c6-37059309d7ff`  
  - 失败 step：1
  - reason：`Model gateway request failed: <urlopen error [Errno -3] Temporary failure in name resolution>`

## 复核结论

- 三条失败 run 均有 `workflow.step.failed` + `workflow.run.failed`，并落 `reason`；
- 失败 step 之后的后续 step 无 `running/succeeded/completed`（仅 `pending`），无越步/越权继续执行；
- 关键拒绝点未出现“看似成功但未落 result”的沉默降级（均有状态与原因链）。

Handoff: sent to 产品规划席
