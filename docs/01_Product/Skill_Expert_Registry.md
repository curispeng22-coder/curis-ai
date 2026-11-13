# Curis Skill / Expert Registry

Status: Review  
Updated: 2026-08-14  
Source: 当前 Talent Market/Skill Runtime、只读公共资源生产线、Agent Skills 开放规范与公开来源审计。

## 1. 产品边界

Skill 是可复用能力资源；Expert 是经 Curis 组合、验证后可招募的专业角色；Employee 是用户实际招募后、归属 Company 并承担责任的实例。

```text
Skill source → source/security/license review → Skill resource
Skill resources + role contract → Expert template → Curis task validation
Expert template → recruit → EmployeeInstance
```

`Expert != Employee`。公开仓库、README、`SKILL.md`、扫描成功或 Candidate 都不能直接成为员工，也不能升级为 `CURIS_READY`。

## 2. 统一来源记录

每个导入资源必须保留：

- `source_url`、`source_owner`、`source_type`、`origin_path`；
- `license_spdx`、商业使用判断、许可证证据；
- `version`/commit、内容 `digest`；
- security scan、依赖、脚本/工具声明；
- capability tags、Curis compatibility、适配器版本；
- maturity、真实任务 Evidence、失败恢复 Evidence。

优先复用 [Agent Skills 开放规范](https://agentskills.io/specification) 的 `SKILL.md`、`license`、`compatibility`、`metadata`、`allowed-tools` 与可选 `scripts/references/assets` 结构。外部内容仍逐项做许可证和安全判断，不因格式兼容自动信任。

## 3. 当前 Registry

| 类别 | 名称/来源 | Discovery | 当前状态 | 真实证据 | Employee bindable | Workspace usable | 下一动作 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Skill | Curis 55 个 active SkillTemplate | 现有 DB/API | LIVE | 已有发现、纳入公司资源、员工绑定和安全 excerpt Runtime | 是，经 Company resource binding | 是，受员工/运行时门禁约束 | 保持现有链，不复制 Skill 系统 |
| Expert | Curis 官方角色模板 | 现有人才市场 | LIVE | 产品经理、架构师、后端、前端、QA 等已有模板招募链 | 招募后成为 Employee | 是，仍需具体 Capability | 按真实任务继续积累角色证据 |
| Agent Candidate | `agency-agents-zh` / CrewAI 快照 | 只读生产线 | DISCOVERABLE | 17 个 Agent Candidate；未完成组合/运行验证 | 否 | 否 | 逐个完成许可证、组合、任务与恢复验证 |
| Skill Candidate | OpenClaw/GitHub `SKILL.md` 快照 | `SkillRepoAdapter` / `OpenClawSkillAdapter` | BLOCKED | 5 个 Skill 被扫描；缺许可证，进入 BLOCKED | 否 | 否 | 取得明确许可证或排除 |
| Open format | Agent Skills | `SKILL.md` | READY | 当前 parser/安全边界可复用；未证明任一新来源可运行 | 否，除非完成 Curis 门禁 | 否 | 以单项来源验证，不批量上架 |
| Public ecosystems | Anthropic Skills、GitHub Copilot Agent Skills、ClawHub、GitHub curated repos | source adapter | RESEARCHED | 官方/公开格式与来源已调研；未作 Curis 运行证明 | 否 | 否 | 按需求和许可证逐项导入 |

[GitHub Copilot Agent Skills 文档](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills)确认其采用开放 Agent Skills 标准，并支持多个标准技能目录；这只证明格式生态可复用，不证明仓库条目满足 Curis 许可证、安全或运行门禁。

## 4. Expert 组合原则

首选公司经营中高频、可形成明确输入/输出和验收的角色，而不是按来源仓库批量包装：

- 已有并优先验证：产品经理、架构师、后端工程师、前端工程师、QA 工程师；
- 已有模板可继续验证：DevOps 工程师、Tech Lead；
- 可从现有 Candidate 研究但尚非 Curis-ready：产品趋势研究、营销内容、增长、社媒策略、财务分析。

专家成熟度沿用既有生产线：

```text
DISCOVERED → CANDIDATE → COMPOSED → VALIDATED → CURIS_READY
                                      ↘ BLOCKED
```

`CURIS_READY` 最少需要一个真实 Curis 任务、结果/Evidence、权限边界和失败恢复证明。当前只读生产线快照共 27 条资源：17 Agent、5 Skill、5 MCP；新增 `CURIS_READY=0`。

## 5. 不做的事

- 不创建第二套 Skill、Expert、Employee 或 Talent Market 数据模型。
- 不按“热门 Skill 数量”批量上架无许可证、无安全审计、无任务证据的资源。
- 不复制第三方私有 prompt、隐藏规则或受限内容。
- 不把 Expert 页面做成 Agent Marketplace；外部 Agent 属于导入/连接生态。

Review 结论：`CAPABILITY ECOSYSTEM REVIEW REQUIRED`。
