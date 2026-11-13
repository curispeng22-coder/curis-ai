# Workspace R4｜第1～7项代码构造独立审计 Gate

- 日期：2026-07-18
- 状态：OPEN
- Owner：质量运行席（独立审计）→ 产品规划席（收口）
- 分支：`feat/roadmap-r1r2`

## 目标

独立核对第四轮第1～7项的已收口代码构造是否仍与各自 Gate 一致；确认后才继续第8项 8a 队列。

## 审计范围

1. 第1项：项目长期状态与 Memory。
2. 第2项：多项目 Session 与上下文隔离。
3. 第3项：Agent / Workflow / Hybrid Mode 边界。
4. 第4项：自动推进、超时、恢复与人工接管边界。
5. 第5项：停止、人工接管、风险升级边界。
6. 第6项：统一 Artifact / Output 投影与跨租户可见性。
7. 第7项：项目级 Token / 成本 / 预算口径与阻断。

## 核对要求

- 逐项从对应 Gate 与现有 Review 抽取验收点，核对实际代码入口、数据读取路径、fail-closed 行为和 focused 测试证据是否一致。
- 检查第1～7项之间是否存在相互覆盖、绕过、重复状态源或跨租户泄露路径。
- 只读审计；不改实现、不新建接口、不跑全量、不启动运行时。
- 若发现问题，按严重度列出唯一最小修复 Issue；未发现问题，明确“可恢复 8a.1a.2”。

## 验收

- 产出独立 Review，逐项记录：代码入口、证据、结论（PASS / BLOCKED）。
- 明确跨项结论和唯一下一步。
- 不以旧文档 PASS 替代实际代码核对。

## Compact Handoff

Issue:
`issues/20260718_workspace_r4_items_1_7_code_construction_audit_gate.md`
Objective:
独立审计第四轮第1～7项已收口代码构造。
Special Constraints:
只读；不改实现、不启动、不跑全量；若通过才恢复第8项队列。
Next Seat:
质量运行席

Handoff: sent to 质量运行席
