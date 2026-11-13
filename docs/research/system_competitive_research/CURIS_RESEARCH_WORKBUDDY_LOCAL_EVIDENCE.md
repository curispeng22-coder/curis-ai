# CURIS_RESEARCH_WORKBUDDY_LOCAL_EVIDENCE — Workbuddy 本地一手使用痕迹（L2）

> Authority Class: RESEARCH / EVIDENCE（L2 Implementation / Resource Evidence；主路线仍以官方产品网络研究为准，见 CURIS_RESEARCH_WORKBUDDY_FUNCTION_INVENTORY.md）
> Date: 2026-09-12
> 来源：本机 `.workbuddy/` 目录（Workbuddy 在 Curis 工作区的真实运行痕迹）。只记录产品机制，不复制业务内容。

## 1. Workbuddy 在真实项目中体现的产品对象

| 对象 | 证据路径 | 产品机制推断 |
|---|---|---|
| 项目记忆（Memory） | `.workbuddy/memory/MEMORY.md`（v3 精简版长期记忆）+ `memory/YYYY-MM-DD.md` 每日日志 | 双层记忆：长期红线/裁定文件 + 按日过程日志；记忆由 agent 自己重整（"v3 精简版，2026-08-16 重整"） |
| Automations（自动化） | `.workbuddy/automations/automation-<id>/memory.md` | 每个自动化有独立 ID 目录与**执行记忆**；支持触发条件判定（"15 分钟内无下一步指令则经飞书推送软提醒"）、条件失效自判 SKIPPED/PAUSED/DELETE、防重复派发（"仍在跑→跳过，不重复派发"） |
| Teams（团队/子代理） | 日志中 TeamCreate、`software-engineer` / `software-qa-engineer` 角色 | 内置角色化子代理（工程师/QA），支持团队创建、成员不可用时降级 general-purpose、框架探针（probe-ok）健康检查 |
| Integrations | 飞书升级 webhook（`oc_…`） | 飞书仅用于升级事件（L2 Gate 7 项触发）；常规汇报不打扰 |
| Output（交付物） | `.workbuddy/output/*.md`（UserStory/系统设计/研究报告/部署设计等） | 以 markdown 文档为交付单元，按任务类型命名 |
| 汇报格式 | MEMORY.md "汇报强制三段式：结论→原因→建议" | 汇报格式可被用户规则约束（prompt 层，非产品功能） |
| Git 纪律 | 日志中 "仅 git add 五个产物路径，绝不 git add -A" | agent 接受路径级提交纪律指令 |

## 2. 关键产品事实（与网络研究互证）

1. **Workbuddy 是"运营型 agent 编排工具"**：它的自动化不是简单定时任务，而是带状态机（触发→判定→执行→记忆→自判失效）的持续运行代理。
2. **专家/技能生态规模**（来自 Curis 人才扫描自动化 2026-08-18 的记录）：Workbuddy 官方 `workbuddy.cn` 有 **专家中心（140+ 专家 / 12 行业）、SkillHub（7 万+ 技能）、连接器市场**三类目录。这是 Curis"人才与能力"对标的最直接规模参照。
3. **升级/审批链**：席位链（总控/产品规划/系统交付/质量运行/安全边界）+ L2 Gate 触发飞书升级——证明 Workbuddy 支持**用户自定义治理规则 + 外部通道升级**，这是"员工需要请示"的产品化先例。
4. **记忆可编辑性**：MEMORY.md 是用户/agent 共同维护的 markdown——记忆对用户透明可改，不是黑盒。

## 3. 对 Curis 的含义（OBSERVATION → PATTERN，仅记录）

- P：自动化=有记忆的持续代理（不是 cron）。Curis 若做 Automation（M-11），最小正确形态是"自动化有自己的执行记忆与失效自判"。
- P：升级链 = 权限边界的用户语言（"这事超出我的席位，已升级"）。与 Curis Permission 面（M-09）天然契合：员工请示 CEO 应是一等产品事件。
- P：专家/Skill/连接器三分类目录（140+/7万+/connector 市场）是人才与能力区的人气参照系；Curis 原装组织是差异化，但发现侧需要同等丰富的目录语言。
- GAP 候选：Curis 无 automation 对象（M-11 已登记）；无外部通道升级（飞书类）集成面。
