# CURIS PRODUCT CAPABILITY DERIVATION LEDGER

> Status: Draft（产品能力推导台账 · 供 CEO / ChatGPT 核对）
> Authority Class: REVIEW — 只登记"被真实场景逼出来的用户能力"；未登记来源链的功能一律视为 UNJUSTIFIED FEATURE，不得进入最终产品。
> Updated: 2026-09-14 · CAP-001 ~ CAP-011 · 来源：METHOD V2 VALIDATION S1–S6。
> 纪律：不为填表创造能力；每条必须有真实场景 + 用户选择 + 不支持的后果；区分 USER CAPABILITY（用户能做什么）与 SUPPORTING MODEL（系统为支撑它需要什么）；每条带可逆性 / 失败行为 / 规模测试 / 跨业务验证。

## 总表

| ID | Product Capability | Real Scenario | User Need / Choice | Without It（不支持会怎样） | Required Model（最少模型） | Scope | Placement | Validation |
|---|---|---|---|---|---|---|---|---|
| CAP-001 | Reuse Employee（把员工派到另一门生意任职） | S1：设计师同时服务内容/小说/电商 | 复用能力、集中履历与成本；选择"复用"而非"复制" | 必须复制员工→身份/履历/成本×3，管理崩（1.16） | Employee + Assignment + Responsibility（现有模型，无新对象） | CORE | 业务团队 / 组织（Add Where You Work） | S1；研发/电商复验 ✓ |
| CAP-002 | Create Similar Employee（创建相似员工，含复制预览） | S2：CEO 怕跨业务混淆，要独立设计员工 | 新身份、能力相同、人生从零 | 手工逐项重配能力，麻烦且易漏；用户怕复制走聊天记录 | Employee 创建 + **Capability Snapshot**（G-14）+ 排除清单（身份/对话/工作/结果/任职/业务记忆/账号权限/决策史） | CORE | 员工详情 / Talent（从专家模板） | S2；研发/电商复验 ✓ |
| CAP-003 | Bind Model Provider to Employee（把模型能力配给员工） | S3：有 OpenAI Key，要让开发员工会写代码 | 成本可控地把"大脑"配给人 | 全员烧最贵模型；或员工永远"不会" | Provider Registry + Binding + Usage（现行已具备，V2 场景确认） | INFRA | Settings（连接）→ 员工（绑定）→ Work（使用） | S3；内容/电商 ✓ |
| CAP-004 | Connect External Agent（连接 Codex/Zcode/Claude Code 等执行者） | S4：没有 API，只有订阅制外部 Agent | 让员工"使用"订阅的执行者 | 订阅制用户整体被挡在门外 | Agent Runtime Provider（五层：Capability/Provider/Runtime/Environment/Tool Access，C-06）+ Registry/Health | INFRA | Settings / Connections | S4；内容 Browser Agent ✓ |
| CAP-005 | Grant / Revoke Action Permission（授予/收回动作权限） | S1+S5：发布员工能发账号；分析员工只读数据 | 最小授权、可收可逆 | 要么全员可发（危险）要么发不了（卡死） | **Action Grant 最小语义**（C-16：Subject/Object/Action/Scope/Constraints/Expiry/Approval/Source/Status） | CORE | 员工/责任授权 | S1、S5；研发 merge/电商上架 ✓ |
| CAP-006 | Publish to Accounts / Schedule Publication（发布到账号/排期） | S5：内容已审核，发到多平台多账号 | 定时/立即、单发/矩阵发、按政策自动 | 发布停留在"准备好的内容"，经营不闭环 | Platform + Owned Account + Publication（逐账号）+ Receipt + Metrics | PROF（记录层 CORE） | 业务现场（发布队列/日历） | S5；上架/Deploy/连载 ✓ |
| CAP-007 | Reconnect External Account（重连账号授权） | S5：授权过期，发布前检查失败 | 恢复连接、业务继续；账号与历史不消失 | 业务静默中断 | Connection lifecycle（授权方式×协议，C-15）+ 失效状态投影 | INFRA | 失败提示直达 Settings | S5、S6 |
| CAP-008 | Switch Executor / Retry with Another Provider（换执行者重试） | S4：Codex 不可用，换 Zcode 或 API 模型 | 执行提供者可替换，员工与责任不变 | 一次订阅到期整个业务停摆 | Execution 归因记录 + Provider 多绑定 + Health | CORE（记录）+ INFRA | 执行现场 | S4 |
| CAP-009 | Transfer External Object（转移外部对象经营绑定） | S5/S6：业务关闭，账号/店铺要转给别的业务或回收 | 对象不失家、历史连续 | 对象被删或悬空，历史断裂 | Company 层身份 + Operating Binding（C-13 Model B） | CORE | Settings / 业务（转移动作） | S6 三例 ✓ |
| CAP-010 | Set Action Policy（设置业务动作政策：哪些自动发、哪些需确认） | S5：日常内容自动发，商业化内容要 CEO 确认 | CEO 不做审批机器人（日均动作<3） | CEO 被逐条审批淹没 | ACTION RISK & REVIEW MODEL（C-12 三档） | CORE（政策）+ PROF（业务默认值） | 业务设置 / 公司偏好 | S5；研发/电商 ✓ |
| CAP-011 | ~~Follow One Truth across Contexts~~ → **RECLASSIFIED as PRODUCT BEHAVIOR**（同一对象跨上下文投影与互跳） | S6：经营账号时点进重连；重连后回到业务现场 | 从任何一面直达同一对象的其他面，数据永不同步错 | 三份数据各自为政 | ONE TRUTH — MULTIPLE CONTEXTUAL PROJECTIONS | CORE | 三个上下文入口互跳 | S6 三例 ✓ |
| CAP-012 | Define Goal & Success Definition（定目标与成功定义：方向/时间/成功/偏离/约束/预算/停止条件） | S9："三个月做起来"落成可判断标准 | Leader 能独立回答"现在做得好不好" | 无标准则一切等老板；把指标当目标→刷量虚荣 | Goal 对象 + Success Definition 字段组 + Metric 引用（三层分离） | CORE（原则）/ PROF（取值） | Business 设置；对照在业务与洞察 | S9 四业务 ✓ |
| CAP-013 | Set / Adjust Strategy（制定与调整业务打法，含"不做什么"） | S10：打法=主题聚焦/双平台/案例优先/不投放 | 打法落成计划才有一致的经营；打法可被复盘 | Goal 直接到 Work→零散任务；无法复盘打法有效性 | Strategy 独立事实（版本化）+ Work 溯源（G-22）+ Envelope 约束 | CORE（原则）/ PROF（内容） | Business；执行在 Workspace | S10 四业务 ✓ |
| CAP-014 | Configure Operating Drivers（配置六类动力：节奏/安全线/政策化触发/提示判断） | S11：六种推进动力并存 | 业务不需 CEO 点火即可持续产生下一步 | 只有定时→对市场无反应；全靠判断→人盯 | 六动力 × 两档处置（机械触发需政策授权 / 提示待判断） | CORE | Business 配置；运行层触发 | S11 四业务 ✓ |
| CAP-015 | Set Leader Operating Envelope（按维度画授权圈） | S12：八项决定逐项判定 | CEO 放权不失控；Leader 清楚什么能自己干 | 事事请示或无边界放权 | Envelope 七维度×档位（自主/需确认/禁止），CEO 连续可调 | CORE | Business（CEO 设置、Leader 执行、使用留痕） | S12 四业务 ✓ |
| CAP-016 | View Absence / Return Summary（查阅缺席回归摘要，调时间窗、下钻） | S13：离开 3 天/30 天回来 | 10 分钟重新掌握公司 | 巡查复辟；真正等的决定被噪音淹没 | 压缩规则（正常=统计/例外=展开/待决=突出带建议）+ Leader 叙述 + 目标偏离对照 | CORE（结构）/ EXPR（呈现） | CEO 工作台；下钻到业务 | S13 四业务 ✓ |
| CAP-017 | Set Resource Contention Policies（设预算/配额/优先级政策；处理争用） | S14：两业务同时派活，账号会话排他 | 冲突诚实可见、可治理、可排队 | 任务静默失败；"员工坏了"误判 | 资源类型×占用状态×政策（七类争用，G-13） | CORE（机制）/ INFRA（资源） | 员工行/执行现场；政策在设置/业务 | S14 四业务 ✓ |
| CAP-018 | Set Business Budget & Spend Policy（设业务月度预算与超限政策；高成本动作前确认） | CG："每月 AI 费用不超过 100 美元"（T-CG-024） | 花费可控、可见、可预期 | 超支静默发生；无法按业务算账 | Usage Ledger + 预算层 + 超限政策（硬停/降级/仅提醒）+ 订阅类成本"预估"标注 | CORE（机制）/ PROF（取值） | Business 设置；提醒在通知；确认在发起处 | CG 样板验证（S-CG 跨切面 B） |
| CAP-019 | Manage Information Sources & Signals（配置信息源；收集信号；转机会/忽略） | CG：持续知道行业/平台/竞品/评论动态（T-CG-003） | 业务持续有"外面发生什么"的可信输入 | 经营与市场脱节，选题靠拍脑袋 | Source 配置 + Signal 对象（来源/时间/时效/可信度）+ 政策化自动收集 | PROF（CG 验证；跨业务共性维持 G-10 deferred） | Business 研究面 | CG 样板验证 |
| CAP-020 | Manage Observed External Entities（添加/停止观察竞品；引用其内容） | CG：观察竞品账号（T-CG-004） | 知己知彼，依据可带入选题 | 竞品信息散落聊天记录 | Observed External Entity 类型（C-11：无连接/无权限/只读）+ 公开数据获取（浏览器/人工） | CORE（对象类型）/ PROF（用法） | Business 研究面 | CG 样板验证 |
| CAP-021 | Manage Audience Engagement（处理评论/私信：拟回复、按政策发送、转机会） | CG：观众评论是回流也是选题来源（T-CG-020） | 不漏声音、回复得体、变废为宝 | 互动失管=口碑风险+机会流失 | 互动流 + 回复对外动作（走政策）+ 互动→信号→机会链接 | PROF | 业务现场互动流 | CG 样板验证 |
| CAP-022 | Capture & Apply Learning（复盘结论落地到打法/账号/员工；升级公司知识需两级确认） | CG："案例类互动率高"→下轮多用（T-CG-022/023） | 学到的东西真的改变下一轮 | 复盘聊完就散；经验无法沉淀 | Learning 结论卡 + 应用去向（Truth 写入）+ 升级流程（Leader 提出+CEO 确认，C-18） | CORE（原则）/ PROF（去向） | 复盘在业务；升级写 Knowledge | CG 样板验证 |
| CAP-023 | Adapt Content per Account（为账号生成/微调适配版并按平台规则校验） | CG：一条内容发小红书+抖音，形态要求不同（T-CG-012） | 一条内容安全发到多个不同要求的账号 | 手动改格式易出错、易违规 | Variant（绑定单账号，Domain Authority）+ Platform Rules（带来源/新鲜度，C-14） | PROF | 内容工作面/发布准备 | CG 样板验证 |

## 能力三分类（ROUND 2 CORRECTION — CEO 指令 5，2026-09-14）

> 总表中 CAP-001~CAP-010 为用户能力；CAP-011 经复核**不是用户能力**（用户不会"执行"一条投影原则），移入 PRODUCT BEHAVIOR。今后 Ledger 新增条目必须先归类。

**① USER CAPABILITY（用户能完成什么）**：CAP-001 Reuse Employee；CAP-002 Create Similar Employee；CAP-003 Bind Model Provider to Employee；CAP-004 Connect External Agent；CAP-005 Grant / Revoke Action Permission；CAP-006 Publish to Accounts / Schedule Publication；CAP-007 Reconnect External Account；CAP-008 Switch Executor / Retry with Another Provider；CAP-009 Transfer External Object；CAP-010 Set Action Policy；CAP-012 Define Goal & Success Definition；CAP-013 Set / Adjust Strategy；CAP-014 Configure Operating Drivers；CAP-015 Set Leader Operating Envelope；CAP-016 View Absence / Return Summary；CAP-017 Set Resource Contention Policies；CAP-018 Set Business Budget & Spend Policy；CAP-019 Manage Information Sources & Signals；CAP-020 Manage Observed External Entities；CAP-021 Manage Audience Engagement；CAP-022 Capture & Apply Learning；CAP-023 Adapt Content per Account。

**② PRODUCT BEHAVIOR（系统如何工作，用户不直接"执行"但直接感知）**：对外动作逐目标记录与部分成功追踪（S5）；Provider/账号失效时的三分离失败语义（S1/S3/S4/S5）；共享订阅并发/配额的诚实显示（S4/G-18）；同一对象在 Business/Settings/Employee 三上下文的投影与互跳（原 CAP-011，S6）；复制预览的"将复制/不会复制"呈现（S2）；业务自生成 Work 时记录"来源动力"（S11）；正常推进压缩为统计、例外才展开的回归摘要生成（S13）；争用发生时"阻塞·真实原因"的状态投影与自动排队/恢复（S14）；五类事实的分层投影与 Unknown 诚实表达（S8）。

**③ SUPPORTING PRINCIPLE / MODEL（内部一致性原则，不进用户语言）**：ONE TRUTH — MULTIPLE CONTEXTUAL PROJECTIONS；Identity / Connection / Execution 三分离；复制能力 ≠ 复制身份/历史；Capability Lifecycle（八步）；Action Grant 最小语义（C-16）；Capability Snapshot（G-14）；Assignment ≠ Grant（C-02）；对外动作六段通用核心 + 业务反馈层引用（C-17 R2）；External Object 四层绑定（C-13 R2）；**Business Operating Context 五类事实分层（S8）；Goal / Success Definition / Metric-Signal 三层分离（S9）；Strategy 独立事实 + Work 溯源（S10）；六类 Operating Drivers + 两档处置（S11）；Leader Operating Envelope 与 Action Grant 两层权限（S12）；CEO ATTENTION MODEL（正常压缩/例外展开/待决突出，S13）；AI Employee Resource / Contention = 资源类型×占用状态×政策，不用工时隐喻（S14）**。

## 每条能力的四项附加检验（CEO 指令 25–29）

**USER CAPABILITY vs SUPPORTING MODEL（指令 25）**
- CAP-002 是最典型的一条：用户看到的是一个动作「创建相似员工」；底层需要 Capability Snapshot + Employee Creation + Excluded History 三个支撑件。产品讨论只用「创建相似员工」，Snapshot 属于支撑模型不进用户语言。
- CAP-006：用户看到「发布」；支撑件是 Publication 逐账号记录 + Receipt + Metrics。
- CAP-005：用户看到「给林墨发布权限」；支撑件是 Grant 十字段语义。

**可逆性（指令 26）**
- CAP-001：撤任职线→历史保留、不再派活；可再加回。
- CAP-002：无工作记录可删；有记录走离职保留历史；【OPTION】能力差分同步给"改主意"留门（G-15）。
- CAP-003/004：解绑/换 Provider/收回授权——员工身份不变。
- CAP-005：收权即时生效；已发生的动作不被追溯撤销。
- CAP-006：未发的可撤计划；**已发的不可回滚**——平台删除是新的对外动作（G-16）。
- CAP-007/009：重连、转移均不动历史。
- 不可逆动作唯一一处：已发布内容不可真撤回——原因：对外事实已发生，与"已发生不回滚"原则一致，产品以"发更正"补偿。

**失败行为（指令 27）**
- Codex 不可用 ≠ 员工坏了：Provider 不可用 → 员工仍在 → 可切换执行者（CAP-008）。
- 账号授权过期 ≠ 账号消失：Connection 失效 → 发布不可执行 → 可重连（CAP-007），历史与身份保留。
- 复制能力后 Provider 未连 → 新员工"具备能力、暂不可执行"（诚实）。
- 部分发布成功 → 逐账号状态，失败账号独立重试。
- Identity / Connection / Execution 三分离是所有失败语义的统一标尺。

**规模测试（指令 28）**
- 50 员工/10 业务/80 任职线：按人（员工目录）与按线（业务团队）双向可查（CAP-001 的信息需求）。
- 10 账号×3 条/天：发布队列按账号/状态聚合，CEO 只看异常（CAP-006，G-17 信息需求）。
- 多员工共享一个 Codex 订阅：并发/配额诚实显示（CAP-004，G-18）。
- 50 个外部对象：搜索+上下文直达，不做"对象中心"大页（CAP-011）。

**跨业务验证（指令 29）**
- Action Grant：内容（林墨×账号×publish）✓ / 研发（开发×Repo×merge）✓ / 电商（运营×Store×edit_product）✓ → 有资格进 CORE。
- 对外动作骨架：发布/上架/Deploy/连载四案例 ✓ → CORE（专业语言保留）。
- One Truth 三投影：账号/Repo/Store ✓ → CORE。
- 员工负载表达：仅 S1 场景逼出，尚未跨业务复验 → 暂不进 CORE，登记 G-13（NOT YET JUSTIFIED 状态标注）。

## UNJUSTIFIED FEATURE 检查（指令 31：用户需要 vs 系统方便）
本轮 11 条能力全部来自场景后果（Without It 列非空）；无一条是"为了让数据库整齐"。内部概念（Snapshot、Grant 字段、Execution 归因）全部留在 SUPPORTING MODEL 层，不升格为用户产品概念。
