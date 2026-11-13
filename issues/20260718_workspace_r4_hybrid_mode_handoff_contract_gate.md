# Workspace R4 第3项｜Hybrid Mode 人机交接契约 Gate（M3b）

- 日期：2026-07-18
- 状态：OPEN — PARTIAL（缺少可复核的人机交接痕迹，待决定是否补样本）
- 父项：`issues/20260718_workspace_r4_hybrid_mode_profile_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席
- 分支：`feat/roadmap-r1r2`

## 目标

定义 Hybrid Mode 中人机交接的最小契约，确保任一端交接后上下文不泄露、不串项目、不中断可审计闭环。

## 必须定义

1. 交接时点：何时从 Human→Model、Model→Human 交接可判定成功
2. 交接失败定义：交接上下文缺失/冲突时直接阻断
3. 上下文不可携带项：避免将无效/敏感字段透传到下一阶段
4. 结果归档：最终状态必须可从历史 run/step/result 复原

## 最小复核（只读）

- 检查既有 evidence 里 `run/step/result/execution` 的字段是否能还原“谁做了什么决策”的链路

## 执行口令（系统交付席）

- 只读核验一条 end-to-end run：
  - Human/Model 决策转移点是否有可见痕迹；
  - 交接后上下文是否未跨项目/跨角色复用；
  - 交接失败场景是否非成功路径落地（有明确失败原因）。
- 产物：交接轨迹字段映射与结论。

## 约束

- 不改数据库、不改模型调用入口、不改日志格式
- 不引入“自动降级”逻辑，不新增 external 调用
- 仅定义和验证可复核条件

## 当前复核

- 复核输出：`reviews/20260718_workspace_r4_hybrid_mode_handoff_contract_gate_review.md`（PARTIAL，当前仅能确认“未见显式交接事件”）

Compact Handoff:
Issue:
`issues/20260718_workspace_r4_hybrid_mode_handoff_contract_gate.md`
Objective:
给出 Hybrid 的人机交接边界与失败阻断，避免无痕串接。
Special Constraints:
仅定义，不改行为，不改 API，不改数据模型。
Next Seat:
产品规划席（确认定义）→ 系统交付席（对齐复核）→ 质量运行席（focused 复核）
