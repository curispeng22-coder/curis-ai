# Workspace R4 第4项｜自动推进、超时、有限重试与恢复 Gate

- 日期：2026-07-18
- 状态：PASS — 第4项已闭环（4a/4b/4c/4d 通过）
- 前置：`issues/20260718_workspace_r4_mode_contract_validation_gate.md`
- 父项：`issues/20260717_workspace_r4_project_long_term_state_and_memory_gate.md`
- Owner：产品规划席
- Next Seat：产品规划席（收口第4项并推进第5项）
- 分支：`feat/roadmap-r1r2`

## 目标

在第四轮内补齐“自动推进、超时、有限重试和失败恢复”最小长期运行闭环，先定义统一口径再做一次 focused 复核，禁止引入调度器、前端控制、外部服务和新执行逻辑。

## 前置约束

1. 不改 `ModelGatewayAdapter` 出网实现、网关、Provider/Model、凭据边界。
2. 不改前端与 Admin。
3. 不新增数据库 Schema。
4. 不发起新建 Run，不重试旧失败 run，不改写历史失败。
5. 保持第3项决议：无显式 `mode / handoff / switch / takeover` 字段为风险留白，仅标记为已知缺口，不阻断本项基础边界收口。

## Must Do

- 统一第4项口径定义：
  - 自动推进：`run-next-step` 的顺序推进与触发条件；
  - 超时：单次调用与恢复等待的边界；
  - 有限重试：本轮仅定义可复用边界，不做默认无限重试；
  - 恢复：失败后在不污染历史与 scope 的前提下的可续推判断。
- 给出“何时自动继续、何时停机、何时交由恢复流程/人工处理”的明确定义。
- 形成至少一条可复核演练脚本（不出网）：
  - 失败 run 的恢复判定；
  - 失败条件下的阻断结果；
  - 无显式 handoff 字段时的最小可复核 fallback。
- 输出一条给 `issues/20260718_workspace_r4_auto_progress_timeout_retry_recovery_gate_review.md` 的复核结果。

## 工单拆分（本项独立）

- 第4a｜推进口径定义（系统交付）
  - 统一 `run-next-step` 顺序窗口、触发边界、不可并行条件。
  - Issue：`issues/20260718_workspace_r4_auto_progress_advance_contract_gate.md`
- 第4b｜超时与阻断定义（系统交付）
  - 单次等待上限、失败停机标准、不可见漏跑边界。
  - Issue：`issues/20260718_workspace_r4_auto_progress_timeout_contract_gate.md`
- 第4c｜恢复与人工接管接口边界（系统交付）
  - 从失败到可恢复的最小判定集与不可逆字段保护。
  - Issue：`issues/20260718_workspace_r4_auto_progress_recovery_takeover_gate.md`
- 第4d｜focused 复核（质量运行）
  - 一轮验证第4a~4c 定义是否闭环。
  - Issue：`issues/20260718_workspace_r4_auto_progress_timeout_retry_recovery_validation_gate.md`

## 当前进展

- 已完成：4a/4b/4c 已由系统交付席闭环定义，4d focused 复核已 PASS。
- 当前不阻塞：本项以“只读派生恢复判定 + 历史不可变 + 人工接管人工决策”为准，不引入新字段。

## 验收标准

- 有明确、可复核的“继续推进/停机/恢复”三态规则。
- 失败不被静默吞掉，不做隐式降级。
- 重试不从“无限”扩展为无限；本轮仅支持有限边界复核。
- 结果能被复核脚本/历史数据库读取链路独立验证。

Compact Handoff:
Issue:
`issues/20260718_workspace_r4_auto_progress_timeout_retry_recovery_gate.md`
Objective:
定义第四轮第4项自动推进、超时、有限重试和恢复闭环，并形成 focused 复核。
Special Constraints:
不改现网出网实现，不加新服务，不改前端；第4项必须以保守、单窗口、可复核方式推进。
Next Seat:
系统交付席
