# Workspace R4 第3项｜Agent Mode 边界定义 Gate

- 日期：2026-07-18
- 状态：OPEN — IN_PROGRESS（M1a/M1b 已复核并形成 partial）
- 父项：`issues/20260718_workspace_r4_agent_workflow_hybrid_mode_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席
- 分支：`feat/roadmap-r1r2`

## 目标

在不改动现有执行核心、不新增前端和不改变现网凭据边界前提下，给出“Agent Mode”最小可信语义边界，明确定义：

- 何时进入 Agent Mode（触发与入口）
- Agent Mode 下的执行边界（run/step/员工约束）
- 与同项目多项目 Session 的作用域关系
- 失败与人工接管的最小阻断条件

已细分子项：

- M1a：`issues/20260718_workspace_r4_agent_mode_entry_criteria_gate.md`（系统交付）  
- M1b：`issues/20260718_workspace_r4_agent_mode_failclosed_gate.md`（系统交付）

## 执行顺序

- 先 `issues/20260718_workspace_r4_agent_mode_entry_criteria_gate.md`
- 再 `issues/20260718_workspace_r4_agent_mode_failclosed_gate.md`

## Must Do

1. 固定 Agent Mode 的定义与可观测字段（可放在 Issue/Review 里，不改行为）
2. 明确禁止项：不得新增 provider 直调、不得新增凭据存储、不得改动 Tool/System Runtime 的既有流程
3. 定义 mode 与 run 的失效模式（如 token 过期、缺 scope、绑定缺失）fail-closed 行为
4. 给出最小单点验收命令（不出网、不 mock），仅校验定义一致性与边界可复核性

## 先后关系

- 先完成：`issues/20260718_workspace_r4_agent_mode_entry_criteria_gate.md`
- 再完成：`issues/20260718_workspace_r4_agent_mode_failclosed_gate.md`

## 允许范围

- 只做 Product/Mode 术语和边界定义、验证脚本/查询口径规范
- 只读核验现有 run/step/usage/tags 与权限边界
- 不实现代码，不调用模型，不改现网流程

## 紧急阻塞条件

- 若定义导致与 run 现有 7 步模型执行顺序冲突（需改执行循环）
- 若需要新增 endpoint/表/secret

Compact Handoff:
Issue:
`issues/20260718_workspace_r4_agent_mode_profile_gate.md`
Objective:
定义 Agent Mode 触发、边界与 fail-closed 规则，形成可复核的最小语义规格。
Special Constraints:
仅定义，不实现；不新增 API/数据库/前端；不改模型网关、凭据或 Task/Workflow 执行器。
Next Seat:
产品规划席（确认通过标准）→ 系统交付席（确认边界落地文档）→ 质量运行席（focused 复核）
