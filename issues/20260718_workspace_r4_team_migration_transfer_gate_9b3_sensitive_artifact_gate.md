# Workspace R4 第9项｜9b.3｜凭据与敏感交接 Gate

- 日期：2026-07-18
- 状态：PASS（定义完成；待质量运行席复核）
- 父项：`issues/20260718_workspace_r4_team_migration_transfer_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席（定义）→ 质量运行席（复核）
- 分支：`feat/roadmap-r1r2`

## 目标

- 明确敏感信息在迁移中的不可传播边界。
- 固化“凭据、密钥、成员短期令牌不得跨 team 口头/文件转移”规则。

## 约束

- 仅文档边界；
- 不记录/写入明文；
- 不新增加密方案。

## 安全边界

- OpenAI/API Key、数据库直连串、临时 token 一律不入 `issues`/`reviews` 追踪范围。
- 只保留经安全边界席批准的最小引用：非秘密变量名、来源类别、回填方式、`mapped`/`blocked` 状态；不放置真实值。
- 任何需要运行的凭据场景必须使用环境注入说明，不进入本轮迁移材料。
- 来源、责任席或回填方式任一缺失/未批准时，状态固定为 `BLOCKED_L2`；逐项禁止转移、导出、回填、占位、沿用历史值、默认值或口头转交。

## 验收

- 遇到敏感信息缺失映射时，迁移任务直接阻断，返回“待凭据口径确认”。

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_team_migration_transfer_gate_9b3_sensitive_artifact_gate.md`
Objective:
固化第9项迁移凭据与敏感资产边界。
Special Constraints:
仅定义敏感信息边界，不改接入逻辑。
Next Seat:
质量运行席（复核）

Handoff: sent to 质量运行席
