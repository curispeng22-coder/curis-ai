# Workspace R4 第3项｜Mode 闭环验收（兼容与互斥）Gate（M4c）

- 日期：2026-07-18
- 状态：PARTIAL — 已复核 + 缺显式 mode/handoff 证据
- 父项：`issues/20260718_workspace_r4_mode_contract_validation_gate.md`
- Owner：质量运行席
- Next Seat：产品规划席
- 分支：`feat/roadmap-r1r2`

## 目标

确认 Agent / Workflow / Hybrid 三模式在单 run/单 project 场景下只允许单一主导模式，不出现并发互斥冲突；并验证既有实现可复用现有事实链。

## Must Do

1. 抽样检验同 run 的 mode 标记是否可归一到单一 mode 责任
2. 检查 step-role-capability 映射在不同 mode 声明下未发生重复执行或双重归属
3. 验证定义覆盖边界一致：无新字段依赖、无 schema 扩展，复核口径落到 run/step/result/evolution events

## 验收标准（只读）

- 无证据显示 Step 在不同模式间“重复归属”  
- 现有历史 run 可按既有模型还原 mode 合法链路

## 执行口令（质量运行席）

- 一次复核固定窗口内抽样：
  - 同 run 的 mode 候选是否归一为单一主导；
  - step 与 step_result 之间不存在重复归属；
  - mode 变更点与切换记录可由已有字段解释。
- 输出：冲突零容忍报告（有则列出冲突行，否则写“PASS”）。
- 约束

## 复核结果（一次性）

- 核验数据库：`deploy/curis/gateway/.generated/data/quality.sqlite`。
- 在同一 run 内，`workflow_steps` 每条 step 仅一次 `employee_role` 与唯一 `step_assignment`，无重复归属；
- 关键 role→binding 对应仅为 run 内部一一映射（tech_lead/PM/architect/frontend/backend/QA，step1/7 同 `tech_lead`）；
- 未检出同 step 重复 `capability_binding_id`；未检出同 run 同 step 的重复 `step_results`，无重复归属证据可解释为“两个 mode 并发执行”。

结论：
- 在现有字段模型下，兼容与互斥可按 run/step/角色链路复核为零冲突；
- **但仍缺少显式 `mode / handoff / switch / takeover` 字段，无法把“谁主导”从事实中按模式语义一一定名**，仅能做收敛近似复核。

Handoff: sent to 产品规划席（确认是否接受保守口径或补样本）

## 约束

- 不新增文件以外实现（定义类 issue）
- 不发起真实模型调用
- 不改前端、不改运行器、不改网关

Compact Handoff:
Issue:
`issues/20260718_workspace_r4_mode_contract_validation_compatibility_gate.md`
Objective:
确认三模式在同一 run 中互斥与兼容边界。
Special Constraints:
仅复核定义与历史事实，不新增接口、字段、行为。
Next Seat:
产品规划席（确认）→ 质量运行席（复核收口）
