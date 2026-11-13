# CURIS — FULL PRODUCT RETHINK REVIEW · 2026-09-14

Authority Class: REVIEW  
Status: Review  
Disposition: PARTIAL KEEP / CORRECTIONS REQUIRED / BASELINE CANDIDATES ONLY  
Owner: CEO / Product Review；本报告为 Codex 独立审查意见  
Target Authority: Product Blueprint 及其下游文档，仅在 CEO 裁决后按正式流程修订  
Next Gate: CEO PRODUCT REASONING REVIEW  
Scope: 最近24小时的全产品推导审查 + AiToEarn 当前公开源码、官方资料与真实产品操作  
Boundary: NO CURIS CODE / RUNTIME / SCHEMA / UI / AUTHORITY CHANGE / COMMIT / PUSH

## 1. Executive Conclusion

**Zcode 找到了更有价值的产品问题，但没有完成新产品基线的验证。** 最值得保留的变化，是把 Curis 从“组织 AI 做工作”推进到“让工作持续改善一项真实业务”；把外部账号、机会、收入与人的必要操作放回经营现场；把员工身份与具体业务责任分开。

这主要是对现有 Company OS 的深化。当前 Blueprint 已写有持续工作、真实反馈与下一轮经营，Master Map 已规定持续 Business、有限 Cycle、Strategy Envelope 和真实跨周期验收。不能把这些描述成今天才首次出现，也不能因为新说法更顺，就宣布现行结构无效。[A1–A5]

**总评：方向 KEEP，推导方法 CORRECT，整体晋升 Frozen 暂不通过。** 有四类阻断：

1. **真实性混写。** 纸面场景通过、业务需要、接口存在、局部实现和完整产品验收被写成同一种 VERIFIED；“127项”“12/12”“20/20”不是127项真实功能或完整经营闭环验收。
2. **结构与语义冲突。** Product Language 把完整员工对话放进 Right Context；部分推导把所有 Result 强制归于 Business；这分别碰到现行 Shell 和四层 canonical scope 边界。
3. **经营事实过度推出。** 有效粉丝与总粉丝、奖励上限与预期收入、现金到账与利润、按钮存在与能力可用没有始终分开。
4. **竞争前提不成立。** “其他 Agent 只做单次任务、没有持续经营”不能再作为 Curis 的价值证明。AiToEarn 官方 OpenClaw 工作方法已经覆盖机会、接单、交付、收益查询与下一轮；它是否在当前账号上稳定跑通，仍需独立验证。[S10–S13]

**AiToEarn 值得进入有边界的外部 Provider / Opportunity Source 验证，不值得直接接管 Curis 的 Core。** 本轮真实进入产品、读取任务、检查账号与发布入口、创建独立草稿箱并验证刷新后存在；未发布、接单、付费、绑定新账号，也未完成收益结算。源码证明了若干执行机制，不能代替本账号端到端验收。

## 2. 这24小时实际完成了什么

### 2.1 时间与归属边界

审查窗口固定为 **2026-09-13 12:06:26—2026-09-14 12:06:26，Asia/Shanghai**。这是收到“过去24小时”要求后锁定的审查切片，后续研究耗时不移动窗口。

结合 git status、diff、修改时间、CURRENT_STATE、CHANGE_LOG 和文档引用，识别出 **15份窗口内研究/产品/审查文本**，记录路径、mtime、SHA-256。窗口内未找到对应提交；工作区含大量既有未提交改动，因此：**可以审查这些材料，不能用 mtime 证明每一行都是 Zcode 在此窗口创作，也不能把整个 dirty diff 归给 Zcode。** CURRENT_STATE / CHANGE_LOG 的相关更新在窗口之前，只作为当前真相参照。[E0]

### 2.2 按主题看成果

| 主题 | 实际新增或推进 | 审查判断 |
|---|---|---|
| Curis 定义 | 重新列出普通人面对 AI 的经营、上下文、组织和持续性问题 | 问题更具体；竞争对手描述过度 |
| 产品全景 | 七区、Shell、Employee、Conversation 等结构盘点 | 可作清单；不是完整实现验收，后续专业业务部分仍待补 |
| 推导方法 | 从真实业务到能力、Owner、Placement，再到表达 | 顺序正确；尚有先定对象再找理由的反例 |
| 员工与组织 | Company 唯一身份、多业务责任投影、配置复制 | 值得保留；权限、历史和部门关系需收敛 |
| 经营生命周期 | 责任持续、周期有限、无人值守后的接续与注意力 | 多数与既有 Authority 一致，属于深化 |
| Content Growth | 从内容生产链扩展到账号、资格、机会、变现、复盘 | 更接近真实业务，但尚未证明获客和利润 |
| 抖音现场 | 创作者中心、收入与任务入口、Web/Mobile 边界 | 有具体证据；可见性不能代表交付或结算完成 |
| AI/User Boundary | 明确 AI 可以组织闭环但不能包办所有动作 | 本轮最有价值的修正之一 |
| 产品语言 | 经营问题对应页面信息和操作入口 | 部分过度搬运平台后台，且出现 Pane 冲突 |
| HTML 对账 | 修正早期“已完成”叙述，登记待复验项目 | 仍是待验收，不能当本轮视觉通过 |

没有发现能把本批推导整体升级为 Current 的新正式接受记录。文档中的“CEO已确认”按作者记录处理；涉及结构变更仍应定位正式 Decision，而非由本审查代签。

## 3. Curis 产品理解发生了什么变化

原先容易强调：有员工、有工作空间、能调模型、能分任务。现在更强调：**谁持续对哪项经营结果负责，当前采用什么策略，外部发生了什么，下一轮为什么继续或改变。**

建议的 North Star 候选：

> Curis 帮普通用户把可用的 AI 能力与必要的人工协作组织起来，在明确目标、预算和权限内持续经营一组真实业务；让工作、外部反馈、结果和下一次判断保持连续，降低用户反复交代、追踪和协调的成本。

商业业务必须关心收入、成本和可持续收益；内部研发、能力建设、研究等工作也有价值，不能全部强迫映射成直接收入。**“赚钱”是商业经营的约束和检验，不是所有 Company Work 唯一合法目标。**

相对现行 Blueprint：这是深化和可验证性修正，不是把 Company OS 换成任务市场或赚钱机器人。相对部分旧研究：需要修正“组织越像真人公司越有价值”“所有专业流程都应在 Curis 重建”“Work 完成即经营成功”的倾向。

## 4. 新核心价值是否成立

成立，但目前是待验证的产品价值主张。必须让用户在真实业务中感受到以下增量：

| 用户问题 | Curis 应证明的增量 | 不能拿什么代替 |
|---|---|---|
| 每次重新交代背景 | 合法范围内延续目标、责任、事实与决策 | 长聊天记录或无限 Context |
| 多项业务互相打断 | 统一呈现需要 CEO 判断的变化，并保留各自责任 | 多 Agent 同时运行的数量 |
| 做了很多却没改善 | 用外部结果检验策略和下一轮投入 | 任务完成率、生成篇数 |
| 账号/工具经常失效 | 明确可用性、等待、人工接续及恢复点 | 提示“运行中” |
| 成本和风险失控 | 预算、权限、承诺与证据一致 | 每一步都弹审批 |

“一人 AI 公司”不是承诺用户不再工作，而是减少重复协调和机械操作，把有限的人类注意力用于真实需要人的地方。普通人是否理解部门和业务层级、是否愿意持续使用，仍需要用户证据；不能从模型优美推出零学习成本。[R1、R3–R6]

## 5. “经营”与“执行”的区别

执行回答“东西做出来了吗”；经营回答“这个东西对谁有用，带来什么变化，值得继续投入吗”。执行是经营的一部分，不能用二者互斥来制造差异。

建议沿用既有对象，补清关系：

| 对象 | 应补强的经营语义 | 不应新增的负担 |
|---|---|---|
| Business | 持续目标、价值对象、策略边界和责任 | 一个业务一个巨大流程图 |
| Workspace | 当前专业工作与经营现场 | 把它降成文件夹，或强制一个账号一个空间 |
| Employee | 对结果负责的身份与当前职责 | 把员工数当产能或成本单位 |
| Work / Result | 执行产物、评估结果及后续引用连续 | 把所有 Result 都叫收入回执 |
| Evidence / KPI | 来源、时间、范围、定义和不确定性 | 把未知数据显示成零 |
| Operating Intelligence | 比较、解释、支持下一判断 | 再建一套 Metric / Result 真源 |
| CEO Desk | 变化、异常、需要判断的事项 | 每个任务都要求 CEO 查看 |
| Strategy / Learning | 根据证据形成有边界的调整 | 把报告归档当成“已经学习” |

**工作成功、平台接受、业务有效、形成应收、实际到账、获得利润是不同事件。** 市场反馈也不总是即时或可归因；曝光增长和收入增长的相关性不自动证明某条策略有效。[R7–R14]

## 6. Business Logic → Product 方法

应作为所有 Business 的标准推导方向，但作为审查方法，而不是给用户增加17个表单。最小顺序是：

1. 谁需要什么价值，谁付费或验收，机会从哪里来，成本与失败是什么。
2. 现实中如何完成，哪些平台、身份、资格和时间约束不可绕开。
3. AI、API、Computer Use、人各自能做到哪一步；证据和恢复从哪里来。
4. 哪些已有 Curis primitive 已能承担，哪些只是缺表达或实现，哪些才是新语义。
5. 确认 Owner、Context、权限、状态、持久性与跨表面关系，再决定 Placement 和 UI。
6. 用真实成功、失败、等待、恢复和第二周期检验，而不只跑故事。

现有 Methodology 已有经营意图、调查、专业责任和验证路线。本批补强了外部平台现实、人工边界和结果回流，适合原位收敛；不需要第二套“唯一方法”。[A3、R3–R6]

仍违反方法的地方：

- PC118 / PC120 / PC125 因多个内容平台都需要，就把资格地图、结算、直播相关能力升入 Core；跨平台不等于跨业务不变量。
- Product Language 从每个经营问题直接生成一个页面块；信息需要被回答，不代表必须永久占一个面板。
- 以“两个业务想象场景都能解释”为 Core 证据；这仍是推理，不是两个真实业务运行证明。
- Capability Ledger、Gap Register 与 Round2 修正不同步：G06仍保留旧七步 External Action，G07仍残留单一绑定表达。
- “127 VERIFIED”实际主要是业务推导成立；必须拆成 REQUIRED、OBSERVED、DOCUMENTED、IMPLEMENTED、ACCEPTED 等含义，不混用完成标记。

## 7. Employee / Responsibility / Conversation

**保留：一个 Company Employee Identity，可以通过不同 Assignment 服务多个 Business；组织图是责任投影，不必复制员工身份。** Responsibility 是持续要求，Holder 可以变化；历史工作不能随着换人改写。[A2–A4、R3–R6]

“一个 Employee ≈ 一个长期 Agent 会话身份”只能帮助解释连续性，不能作为实现等式。更准确的是：**一个长期员工身份，管理多个有范围、有主题、有执行记录的 Conversation。** 当前 Master Map 允许同一 Conversation 跨 Assignment 延续，但明确历史消息/引用不能被新的 scope 重写；不需要机械地“一 Assignment 一聊天”。

| 议题 | 应收敛的规则 |
|---|---|
| Context 隔离 | 明示当前 Business / Responsibility / Account；切换不重绑定历史消息，不自动读另一个客户资料 |
| 配置复制 | 复制可复用能力配置，生成新身份；不复制凭证、Grant、客户上下文或私人历史 |
| 能力绑定 | Employee ≠ Provider ≠ Runtime；同一身份可以使用不同合法执行能力 |
| 工作路由 | 责任、可用性、授权、预算决定接手，不只按名字或默认模型 |
| 并发 | 争用的是账号会话、仓库环境、配额等具体资源；不默认给 AI 员工套8小时人力制或全局锁 |
| 经验共享 | 通用经验也需来源和脱敏检验；“不带数据”不是自动安全证明 |
| Department | 现有身份有 Department；跨业务投影不直接证明行政归属可无限多对多，需正式澄清 |

模型订阅也不等于可调用的受支持 Adapter。Model、Agent Runtime、Tool/MCP、执行环境和模态是不同维度，不应把所有外部能力硬塞进一个 Provider 类型。复用同一 Employee 更不意味着三项业务成本自动降到三分之一。

## 8. Content Growth 为什么仍值得作为样板

**继续，但缩小到一项有真实机会、有交付边界、有反馈路径的业务。** 数字资产、外部平台、持续账号、发布状态、数据延迟和商业结果，能同时检验 Company OS 的核心假设。

“AI能做很多内容”不足以证明它最容易赚钱。内容市场竞争、买方来源、审美质量、平台规则、账号资格、归因和人工维护，都可能成为主成本。电商与内容业务谁更容易，取决于具体模式，不能整体下结论。

优先选择能回答这六件事的样板：谁要什么；从哪里取得机会；具备什么资格；能否合法完成交付；怎样验证结果；失败之后谁做什么。先检验一个模式的连续两轮，不能同时铺开13种变现方式。Content Growth 是验证样板，不应变成 Core 的业务枚举或唯一收入观。[R8–R14、A3]

## 9. 抖音研究真正证明了什么

这轮材料的重要价值是把“内容链”拉回真实经营：账号有长期状态，资格影响可选机会，机会有时限和条件，数据有延迟，手机与人的操作不能凭空消失。**这些大多可以提炼为通用原则；抖音门槛、页面和变现方法不能通用化。**

本轮审查读取了 Zcode 的现场记录；其中抖音 L1 是前序研究证据，**不是本轮重新登录抖音复现全部动作**。创作者中心可见、收入页/任务入口存在，不能证明实际接单、发布、收益审核和结算已经跑通。

需要修正的具体断言：[R7]

| 位置/断言 | 问题 | 合理修正 |
|---|---|---|
| §18 与 §25.13 有效粉丝定义 | 一处 VERIFIED，一处 UNKNOWN | 以可追溯当前官方定义与账号值为准 |
| M11 用4粉丝推资格差196 | 总粉丝不等于有效粉丝 | 有效值未知则差额未知 |
| M24 起点0粉丝，§26/M11为4 | 案例口径不一致 | 明示是假设账号或统一现场时点 |
| 奖励上限推首月收益 | 上限不等于期望值，更无接单/验收概率 | 写场景预算，不写收益预测 |
| M3/M14 App-only 概括 | 现场又看到 Web 任务入口 | 区分具体机会种类与动作；未发现不等于不存在 |
| 导出入口 | 只看到按钮 | 格式、下载内容、可持续导入均待验 |
| “仅两处人工断点” | 忽略登录、资格、找机会、审核、补证、提现等工作 | 按完整周期记录人工耗时和等待 |
| 曲线差分/归因 | 比率不能直接差分；累计值可因校正变化 | 保留单位、窗口、定义与修订信息 |

“10万播放无收入必然因为资格”“某内容类型必然低转化”“Curis具有唯一防御力”均缺因果证据。保留作为待检验假设，不作为产品真相。

## 10. AI / User Boundary 是否成立

**成立，且应成为通用能力判断方式；当前混在一起的分类必须拆开。**

| 维度 | 应回答的问题 |
|---|---|
| 执行路径 | AI直接、API/Connector、Computer Use、AI辅助人工、必须用户执行 |
| 当前可用性 | 已验证、条件可用、未连接、未知、不支持、未来候选 |
| 决策权限 | 提供信息、分析、建议、批准、实际执行分别由谁授权 |
| 结果可信度 | 来源、回执、最终状态、外部核验、延迟与过期 |

Computer Use 可以已验证，也可以未连接；User Required 可以是平台身份动作，也可以只是当前工具不足。UNRELIABLE 不等于 UNVERIFIED。不能把某次研究工具不支持上传，写成 Curis 或平台永远不能上传。[R11]

B2承认 Publishing/Analytics 未连接、Evaluation 等待，B14却把当前系统称作成熟 L3 经营能力，证据不支持。研究员在浏览器里完成动作，也不是 Curis Runtime 已拥有该动作。

应保留“经营闭环不等于全自动闭环”；修正“所有接单永远 CEO 手动”“所有发布都手动”等绝对要求。实际身份操作、重大商业承诺必须遵守权限和平台要求；低风险动作能否在已批准边界内执行，应由现行授权规则决定，不能新建一套审批真源。

人工交接需要：明确对象、要做的动作、截止时间、完成证据、接续责任与恢复位置。复用现有 Work / Attention / Decision，不能另建“人工任务系统”。

## 11. 上一版 Product Language 为什么复杂化

部分原因确实是 Boundary 做晚了：把“Curis需要知道”误推成“Curis需要完整管理”。另一原因是从问题清单直接映射页面，导致每个名词都要求一个永久区块。[R14]

| 内容 | Curis 应持有/表达 | 外部平台保留 Owner |
|---|---|---|
| 资格 | 是否满足、来源、时点、缺口及下一动作 | 平台资格审核与原始材料系统 |
| 收益 | 与 Work / Business 关联的已核验结果、状态、口径 | 平台钱包、提现执行和结算规则 |
| 机会 | 有限摘要、条件、截止、来源和接单状态 | 原始市场订单与平台裁决 |
| 账号 | 经营责任、连接健康、可用动作和授权范围 | 平台身份、安全认证与账号系统 |
| 用户待处理 | 对现有事实的注意力投影 | 不能成为第二份 Decision / Handoff 真相 |

Goal 不能定义成“赚钱方式”；Result 不能缩成“回执+指标”；Opportunity 不应强制每条都流向 Revenue，还应允许拒绝、过期、失败和无利可图。押金占用现金，不当然等于费用；预估、应收、已结算、已到账和利润须分开表达，平台提供什么就诚实显示什么。

P9/P13/P14/P15 把完整 Conversation 放到 Right Context，不能以“保持 Four-Pane”作为合规解释。Current 允许 Context 提供导航和引用，完整工作对话在 Main；Utility 可读 Result/Evidence。这里必须先改正研究建议，再讨论视觉。[A4、R14]

## 12. 对 Core / Package / Provider 的影响

**先复用已存在的 primitive，不因新名词就加一个中心、一套表或执行系统。** 以下是架构建议，不是 Schema 授权。

| 层 | 适合承担 | 本轮不应塞入 |
|---|---|---|
| Core | canonical身份与四层scope、Responsibility/Assignment、Conversation、Work、Result/Evidence、Decision、授权、Usage、持续性与恢复 | 抖音资格、直播条件、平台钱包、各站结算公式 |
| 共用产品语义 | 结果来源/时效、外部动作状态、接续点、业务价值引用 | 新建Revenue总账、Learning系统、Marketplace来重复既有对象 |
| Business Package | 账号经营、机会解释、业务指标、收入/成本口径、专业策略与工作面 | 修改Company身份、绕开统一授权 |
| Platform Adapter / Provider | 连接、平台字段、执行协议、回执映射、受限能力 | 决定Curis员工身份、CEO战略与跨业务责任 |
| 外部平台 | 原始订单、身份认证、审核、钱包、平台争议和结算 | 被Curis显示一个副本就丧失Owner |

Revenue / Business Result 有必要成为可读、可引用的经营信息，但“业务关注它”不证明需要新的 Core primitive。Learning 应首先表现为 Evidence → Review/Decision → Strategy adjustment → next Work 的连续性。Operating Cycle 已有语义；不能再做第二个循环引擎。

Observed Object 也可能需要只读 Connection / Grant。正确边界是“没有经营控制权或写权限”，不是“观察对象绝不能有连接”。Company 所有权、业务使用关系、主要经营责任和动作授权需要分开；多处使用不代表多处可自由发布。[R3–R6]

## 13. Curis 与普通 Agent 的重新定位

“Agent完成Task，Curis经营Business”可作内部提醒，不能作排他性事实。强 Agent 可以有持续会话、工具、项目和长期任务；AiToEarn/OpenClaw 甚至已有经营 Playbook。本轮没有重新全量验收 ChatGPT/Codex/Zcode，因此也不对它们作“没有某能力”的负面认证。

Curis 必须证明的差异是：**跨业务的责任、权限、外部事实和经营判断被长期统一管理，并且比用户直接使用现成 Agent + 专业工具更省协调、更可信。**

一个可反驳的验收方式是：同一真实业务、相近预算和可用工具，对比两轮运行中 CEO 的重复说明、人工协调、漏接续、结果错误归属和策略调整质量。若 Curis 只多了部门树和聊天窗口，却没有这些改善，其新增结构就没有证明价值。

## 14. AiToEarn 历史研究回顾

项目空间检索到23个涉及 AiToEarn 的文档路径，包含研究、复用方案、资产映射、架构 Review、Shared Contract 和 Current 引用。本轮重点回读历史研究/架构结论与决策段落；**不声称23份文档所有内容都逐字复审**。旧资料是 HISTORY / RESEARCH，不成为当前 Authority。[H1–H5]

| 阶段 | 看到了什么 | 当时结论 | 本轮修正 |
|---|---|---|---|
| 7月复用研究 | 多平台、MCP、Relay、市场和OpenClaw | 大量能力可复用，甚至给出约85%的复用估计 | 该比例是类别分摊，不是实际接口覆盖率或工程验收 |
| 资产/最终方案 | 公共代码、自有OAuth、Connector思路 | 倾向自托管、直接复用部分实现 | 自托管不自动获得平台能力、资质或零维护成本 |
| 架构Review | 从内容营销产品与Company OS差异评估 | 倾向不把它当Curis整体基础 | 保留边界；不能由README没展开推断没有Schema、回执或Analytics |
| 合规判断 | Relay/白标与自托管的条款问题 | 出现“100%合法”“非法”等绝对表述 | 不能替代具体版本许可、平台协议和部署方式判断 |

**市场与OpenClaw不是今天首次发现。** 新价值在于：当前经营视角使我们更重视它作为机会网络和执行桥的作用，而不只是“能复用多少发布代码”。使用用户自己的外部账号连接，和把第三方服务白标转售，是不同模式；本轮不作法律定性，也不执行任何商业接入。

## 15. AiToEarn 当前版本与真实研究

### 15.1 版本边界

| 对象 | 本轮版本/来源 | 证据边界 |
|---|---|---|
| 主公开仓库 | yikart/AiToEarn，commit `9413d73918271bd716b9ea59f61c9f59e485619b` | 已clone并阅读关键执行链；未本地构建/运行 |
| 最新发布标签 | `v2.5.0`，2026-06-24 | Release不同于9月仓库HEAD，也不等于当前线上构建 |
| 桌面策略 | `v1.8.0`公告停止Windows/macOS/Android客户端更新、聚焦Web | 本轮以当前Web为主，没有把旧Electron作为现行体验 |
| OpenClaw官方插件 | yikart/aitoearn-openclaw-plugin，commit `c5c5e722b150167249aafa448ebaee80cb4d3840` | 已clone、阅读运行桥与经营技能；未安装/认证执行 |
| 官方CLI包 | `@aitoearn/openclaw-plugin-cli`，npm当前返回`1.0.23` | 下载解包静态查看，未执行安装脚本 |
| 线上产品 | 本机macOS / Chrome，AiToEarn中文站，现有登录session | App build与账户tier未核实；不把UI版型绑定到上述commit |

主仓库采用 Next/React 前端、Zustand与Lexical相关组件，后端为Nest应用、MongoDB与Redis/队列。运行版公开代码与商业服务边界必须分开；仓库里未找到市场服务完整实现，不能据此说线上市场不存在。[S1–S13]

### 15.2 实际操作与结果

| 操作 | 实际结果 | 证据 |
|---|---|---|
| 进入已登录产品 | 淘金广场、团队、Agent、内容管理、发布、数据、互动等可访问入口 | E1–E3 |
| 浏览市场并打开任务 | 可读奖励、名额、平台、交付和保留要求 | E2、E3 |
| 查看我的频道 | 现有抖音频道离线，浏览器插件未安装 | E4 |
| 创建研究草稿箱 | `CURIS-RESEARCH-TEST-2026-09-14`创建成功，刷新后仍在 | E5 |
| 打开发布编辑器 | 账号选择、草稿内容入口、发布相关控件出现；未提交 | E6 |
| 关闭编辑器 | 出现“填写内容将保存、下次可恢复”的提示并成功关闭 | E7；本次未填写正文，不等于正文恢复已验 |
| 打开数据统计 | “已更新0/0”“暂无采集数据”，同时核心指标为0 | E8 |
| 生成内容入口 | 页面显示预计消耗额度 | 未生成，未消费付费资源 |

只创建上述研究草稿箱。没有接赚钱任务、发作品、评论、邀请人员、绑定账号或导出凭证。研究草稿箱保留供用户后续处理。

### 15.3 Issues / PR 不当成验收

检查公开Releases、25条Issues结果与15条PR结果。#566已合并的开源2.5同步是版本线索；#587重复发布修复、#571互动、#570去重等 **closed但未merged**，不能写成已经上线。#586报告TikTok远端已接受而本地检查点未落下导致重试重复；#581报告抖音Relay回调账号问题，closed也不等于本轮验证已解决。#592为Facebook失败报告，未复现。[G1–G5]

#575尤其容易误读：其正文说明调用在到达AiToEarn前被Codex安全审查阻止，不能把它当作AiToEarn服务故障的证据。Issues是报告者证据，不是本轮复现结果。[G6]

## 16. AiToEarn Execution Layer

### 16.1 真正值得参考的结构

公开实现把能力拆为账号、平台Provider、发布流程、平台记录、查询和分析。`PlatformIntegrationRegistry`按实际方法与配置产生能力元数据；一个平台出现在列表里，不代表授权、发布、编辑、数据、评论都可用。[S2]

`PublishRecord`包含用户、流程、任务、账号、平台、内容、状态、平台作品ID/链接、错误和待完成信息。复合唯一约束能够防部分本地重复记录，不能保证第三方平台恰好执行一次。[S3]

`PublishTaskService.processPublishJob`检查队列状态后执行Provider，区分等待用户、平台定时、等待最终完成和已发布，失败可能刷新凭证并有限重试。**网络失败后结果不明，需要先核对外部状态；不能把自动重试本身叫可靠。** OpenClaw MCP客户端也有传输重试，其调用副作用仍需要幂等/核验边界。[S4、S12]

### 16.2 能力矩阵

| 能力 | 当前证据 | 可否宣称解决Curis问题 |
|---|---|---|
| 多平台账号连接 | L2账号作用域与Provider；L1现有频道离线 | 有实现参考；本账号连接未验收 |
| 普通/多平台发布 | L2 Flow/Record/队列；L3正式文档；L1编辑器入口 | 有明确执行能力基础；本轮未真实发布 |
| 抖音发布 | L2 `DouyinPublishProvider`返回handoff链接、等待用户、查询完成 | 证明不是纯服务端全自动；手机动作仍可能必要 |
| Browser Plugin | L3列XHS/视频号/抖音路径、进度与结果 | 可参考执行桥；本机未安装，未实测 |
| Relay | L2客户端转发、资源上传、回调路径 | 能描述桥接边界；不能冒充知道私有远端实现 |
| Analytics | L2 Provider查询/快照；L1无采集数据 | 不支持、未采集、过期和真实0需分开；没有本轮有效数据链 |
| Engage | L2评论读取/提交/通用互动工具；L3接口 | 分平台、账号、权限验证；未发任何真实互动 |
| 失败恢复 | L2状态保护、错误、有限重试、草稿持久化 | 机制可参考；未完成线上失败恢复E2E |

文档明确部分发布依赖浏览器插件；抖音另有handoff等待。插件API文档含敏感登录材料字段，不能直接把原始响应交给模型或写研究日志。本轮未调用这些接口，也未读取Cookie。[D1、D2]

前端的草稿恢复过滤无效账号和失效媒体，发布前检查会聚焦错误项。这些比单纯“有发布按钮”更值得借鉴：**恢复必须处理当前环境变化，而不是把旧状态原样塞回去。**[S8、S9]

## 17. AiToEarn Operating / Monetization

**它已经超出普通发布工具，但尚不能被本轮证据认证为完整自主经营公司。**

线上任务详情实际可见：奖励计算、名额、发布平台、提交期限和内容保留要求。本轮打开的任务为小红书推广类，按互动计价、存在单条上限，并要求限时交付和保留内容；读取详情没有接受订单。[E3]

官方创作者文档解释任务领取、交付、审核和异常处理；广告主文档解释目标和定价；短剧说明涉及资格、素材、生成、人工检查、发布和效果/结算。官方收益分配说明也提醒实际任务和实际收益条件优先，不宜直接拿分成表算收入。[D3–D6]

OpenClaw官方经营材料给出：

- `listTaskMarket → getTaskDetail → acceptTask → userTaskId → 发布/作品链接 → submitTask → 状态查询`；
- Affiliate链接、佣金和结算查询；
- Campaign申请、交付要求和验证；
- 样品任务可能涉及地址、押金；
- 查询结果后复盘并决定下一轮。[S13]

这些是**官方流程证据L3**，即使文件存在公开仓库，也不是市场服务端功能已验证的L2证据。插件运行桥能动态发现并调用远端工具是L2；当前账号到底返回哪些工具、是否能接单/结算，本轮没有认证调用，仍UNKNOWN。

它解决的是平台上的供需匹配和若干收入路径，不代表读取了抖音App里所有机会，也不代表解决选品、团购、商单、利润归因与跨业务资源配置。平台奖励、商业成交、佣金、提现和利润应分开。推广平台自身获得的奖励也不能直接证明外部客户对某项业务长期买单。

## 18. AI-readable Opportunity Market 是否重要

**重要；机制层面已经有足够证据成立。** 商家把机会、交付条件和奖励放到结构化市场，AI可以理解任务，而不必先把抖音App所有机会页面自动化。[E2、E3、S13]

但这里的“绕过”是替代机会来源，不是绕过权限：发布、资格、账号身份、接单条款和结算仍受原平台约束。

| 命题 | 判断 |
|---|---|
| 市场内容能被AI读取 | L1：本轮DOM可读任务列表与详情 |
| 有面向Agent的任务工具设计 | L3官方工具清单/Playbook，L2插件远端发现桥 |
| 当前登录账号可以通过MCP接单 | UNKNOWN，未做认证工具发现与调用 |
| Agent能完成任务并获得收入 | DOCUMENTED流程，非本轮E2E |
| 覆盖所有外部App-only机会 | 不成立 |
| 有稳定正收益与充足买方需求 | 未证明 |

对Curis真正重要的是：**先选择AI可以合法获取和完成的机会，再决定经营什么。** 这比先建一个全行业Workspace、再发现没有客户和执行入口更实际。

可接受机会需要校验：买方/来源、适用地区、资格、预算/押金、截止、交付与验收条件、保留义务、争议恢复、收益状态和用户授权。外部 `taskId` / `userTaskId` 是来源引用，不能替代Curis Work身份。

## 19. AiToEarn 与 Curis 的结合方式

| 角色 | 建议 | 不可越过的边界 |
|---|---|---|
| Capability Provider | 候选：发布、账号状态、数据、有限互动 | 逐账号逐动作验证，不能笼统授予全平台可用 |
| MCP Provider | 候选：员工通过受控工具调用 | 动态工具清单不是永久授权；副作用前校验范围和当前权限 |
| Adapter实现参考 | 值得：能力注册、状态映射、异步回执、handoff | 不直接搬整个技术栈或重复执行系统 |
| External Business Network | 优先：只读机会源，再验证单任务交付 | 平台市场状态不成为Curis业务全局真相 |
| Competitive Reference | 强：Agent已经可以消费经营方法和市场 | 不以“有组织树”代替真实价值 |

推荐第一步是 **只读机会与能力可用性验证**，第二步才是经过独立授权的有限执行。选择用户已有合法账号，保留自己的Business/Work/Result/Usage引用；AiToEarn管理其外部连接和任务状态，Curis管理责任与经营上下文。

接入前最小检查：当前账号工具发现、平台方法覆盖、费用、权限、结果映射、超时未知状态、重试去重、撤销/取消边界、断线恢复、结算真实性。上述检查是后续候选工作的验收条件，不是本轮已实施接入。

不建议先建自托管整套AiToEarn、Curis自有市场或新的Relay。先证明现有合法服务能为一个真实业务提供不可替代的价值，再讨论依赖控制。公开代码版本和线上商业工具不完全对应，自托管不能假设自动拥有任务市场。[S1、S10–S13]

## 20. 后续Business战略

优先“数字化、AI能覆盖主要工作、机会可获得、验收明确、人工边界可负担”的少量业务，战略合理。**有AI能力只是供给，有愿意付费的客户和可交付路径才是业务。**

以下10类仅为筛选假设，不是产品支持清单、收益推荐或立刻新增Package：

| 候选业务 | 价值/付费对象 | 首先要验证的约束 |
|---|---|---|
| 内容营销交付 | 有明确Brief的小企业/市场任务 | 客户来源、版权、发布权限、结果口径 |
| 多语言内容本地化 | 有既有内容的品牌/创作者 | 语言质量、术语、人工校验、交付验收 |
| 小型网站维护 | 已有网站的小企业 | 获客、凭证隔离、部署责任、持续支持 |
| 文档与知识整理服务 | 有授权资料的团队 | 隐私、准确性、授权范围、可验证质量 |
| 商业信息监测 | 有具体问题的客户 | 数据许可、时效、来源、是否愿意续费 |
| 产品资料与商品内容制作 | 合法商家 | 商品事实、夸大宣传、平台格式、审核 |
| 数据清洗与定期报告 | 有自有数据的小团队 | 数据安全、质量标准、反馈与错误责任 |
| 小型自动化服务 | 重复数字流程明确的客户 | API可用性、维护成本、失败回滚 |
| 数字内容/IP产品 | 有可触达受众的经营者 | 原创性、分发、真实需求、长期资产价值 |
| 微型软件产品 | 有窄问题和潜在买家的经营者 | 产品发现、维护、客服、支付与获客 |

先筛掉需要大量不可替代线下操作、未经授权高风险动作、未知机会源或收入无法核验的模式。不要同时建设10支业务。先用Content Growth与一个不同类型的已有业务场景检验：哪些真的是Core不变量，哪些只是专业方法。

## 21. KEEP / CORRECT / REJECT

### KEEP

1. 从真实经营结果倒推工作，而不是从AI能生成什么倒推业务。
2. 员工身份唯一、责任可以投影到多个业务，配置复用不等于身份复制。
3. 账号是持续经营对象，Platform、Account、Connection、Workspace应分开。
4. 外部机会、资格、时效和收益状态参与策略判断。
5. AI不包办所有动作，Curis仍可组织完整交接与恢复。
6. 责任持续、周期有限；数据与结果驱动下一轮。
7. 先业务事实和边界，再能力/Owner/Placement，最后UI。
8. 把AiToEarn看作执行桥、机会网络和竞争参照，而非仅发布工具。

### CORRECT

1. 新North Star是现行Company OS的深化，不是推翻全部旧定义。
2. Employee是长期身份，不是一个无限会话或固定模型实例。
3. 收入不是所有Work的唯一结果；到账、利润、押金与预估分开。
4. 能力类型、当前可用性、决策权限、证据可信度分维度表示。
5. Core吸收不变量，Package承担专业规则；不按名词数量增加对象。
6. 两个场景的纸面推导只能支持候选，不能证明跨域运行完成。
7. 运营自主性受当前授权与Strategy Envelope约束，不能把所有调整都归Leader或所有动作都归CEO。
8. 多账号数据可以合理汇总，但须统一口径并去重，不能一律禁止汇总。
9. Capability/Gap Ledger应跟随Round2修正，不能保留互相冲突的七步/六步、单一/多重绑定口径。
10. AiToEarn市场及插件的官方说明需要与实际工具发现分开。

### REJECT

1. “其他Agent只能单次执行，因此Curis天然独有持续经营”的排他性论证。
2. 把127项业务需求、12/12或20/20场景通过写成产品能力已验证。
3. Publishing/Analytics未连接时宣布当前完整经营闭环已成立。
4. 完整Conversation进入Right Context并声称不违背当前Shell。
5. 所有Result必须归属Business、从而排除Company/Department合法结果。
6. 有效粉丝缺口用总粉丝计算；奖励上限直接推预期收入。
7. 市场页面、API文档或closed PR作为已完成发布/收益链的证明。
8. 把资格、钱包、结算、直播完整后台直接提升为Core。
9. “自托管100%合法/零依赖”“Relay一定非法”等未经具体证据审查的绝对结论。
10. 以未复验的HTML修改或模拟回复宣布产品/视觉验收完成。

## 22. New Baseline Candidates

以下全部是 **CANDIDATE ADDITION / CLARIFICATION**，不是Authority写入。风险、运行影响和下一证据已列出，避免“接受想法”等同“接受实现”。

| ID / 名称 | 问题与参考 | 产品/UI影响 | Runtime影响 | 复杂度/风险 | 优先级 / Authority关系 | 下一证据 |
|---|---|---|---|---|---|---|
| N1 经营结果连续性原则 | Work完成不等于业务改善；本批推导、AiToEarn任务状态 | 当前工作与外部结果、下一判断可追踪 | 优先复用Work/Result/Evidence/Decision/Cycle | 中；误归因风险 | P0，深化现有合同 | 一项真实业务两轮，含失败/等待 |
| N2 能力真实性表达 | 平台Logo或接口存在被当可用 | 显示动作范围、当前状态和证据 | 复用Capability/Connection/Grant，不新注册中心 | 中；状态过期风险 | P0，符合Current | 断线、不支持、未知、恢复均可辨 |
| N3 人工接续合同 | 人做完后系统失去连续性 | 具体动作、对象、证据、返回点 | 复用Work/Attention/Handoff | 中；重复执行风险 | P0，需确认既有合同缺口 | 一个真实等待→人工完成→接续案例 |
| N4 员工身份与责任投影 | 多业务复用被误当多员工或混Context | 当前服务范围与历史清晰 | 核实既有Assignment隔离和历史规则 | 中；跨业务泄露风险 | P0澄清，不自动改Department关系 | 同身份两业务，换Holder/切话题无越权 |
| N5 经营事实可信度 | 未采集/过期/0混淆 | 来源、时间、定义、未知状态 | 复用Evidence/Analytics边界 | 中；错误决策风险 | P0，深化Data Trust | 延迟、缺失、校正、单位冲突样例 |
| N6 AI-readable Opportunity Source | 业务缺真实机会；AiToEarn市场 | 专业业务中的来源、条件、截止与状态 | 受控只读Adapter，外部ID映射 | 中；条款/供应依赖 | P1，新能力候选，留Package/Provider | 当前账号可读且可完成的真实机会 |
| N7 商业结果口径 | 奖励/收入/利润混写 | 专业结果卡区分预估、应收、结算、到账 | 优先使用Result/Evidence扩展，不新账本 | 中高；口径和归因风险 | P1，业务Package候选 | 一笔真实收益与成本证据核对 |
| N8 CEO离开后的恢复摘要 | 返回后需重读大量消息 | 变化、待判断、未知和下一动作 | 消费已有Activity/Attention/Result | 中；遗漏关键变化 | P1，已有CEO Desk语义深化 | 对比人工重建上下文时间与漏项 |
| N9 推导证据与晋升纪律 | 推理被标作验收 | 文档区分需要/观察/实现/接受 | 无新Runtime | 低；错误晋升风险高 | P0，现有治理落实 | 清除本批矛盾并有Owner/Next Gate |
| N10 外部副作用未知状态恢复 | 超时重试可能重复发布；AiToEarn源码/Issue | 明确“结果待核验”，提供核对路径 | 复用Execution幂等/回执/恢复 | 高；真实外部副作用 | P1，需差距审计 | 平台已接受但本地未落账的受控测试 |

不建议本轮新增：Core钱包、全行业市场、专门Learning系统、新Usage账本、第二套Work执行器。需要的表达先消费现有Truth；只有证明现有模型无法表达，再提交正式架构变更。

## 23. Current Authority Conflicts

**没有在本轮选取的Current入口中确认新的Current对Current冲突。以下主要是研究建议与Current冲突；因此停止向Authority/UI传播这些建议，但可以完成本次审查。**

| ID | 研究问题 | 当前Authority | 判定 / Owner / 恢复入口 |
|---|---|---|---|
| AC1 | Product Language P9/P13/P14/P15完整Conversation放Right Context | Shell：Conversation/Working在Main；Context不承载完整对话 | CONFIRMED RESEARCH CONFLICT；Product修正文案或向CEO提交明确Challenge，再入UI |
| AC2 | Result∈Work∈Business作为所有结果关系 | 四层Company/Department/Business/Workspace共同消费Result/Evidence | CONFIRMED RESEARCH CONFLICT；保留source Work+canonical scope，不强制Business |
| AC3 | PC118/120/125把跨平台资格/结算/直播升Core | Core持identity/truth/execution/security/ref；Package持专业composition | BOUNDARY CONFLICT / CANDIDATE未获准；Architecture说明为何现有primitive不足 |
| AC4 | 员工多个业务投影被扩展成部门归属任意变更 | Current有Department身份与Assignment；没有由本批研究批准新的归属基数 | UNRESOLVED SEMANTIC CHANGE；CEO澄清行政归属与服务投影，不能自行改schema |
| AC5 | Workspace canonical identity被说成Business不重要 | Business是持续经营身份，Workspace是实际工作环境 | CONFIRMED MISREAD；修正叙述，不删Business |

Definition Rebuild 的历史Part7已经标为不接受/被后续修正，不能再次把减少一级区、降级Meeting/Department、替换Four-Pane当成当前建议。但Part8/下一步仍指向旧7.x的内容应清理，防止失效方案继续下传。[R1]

可以保留一个 **PRODUCT AUTHORITY CHALLENGE假设**：Business必须Department+Workspace的创建过程，是否给普通用户带来额外负担？目前没有真实用户证据足以推翻结构。先优化合法责任转译与渐进呈现，再观察；不能把“可能复杂”当裁决。[A1–A4]

当前产品完整Conversation在Main的规定仍有效；本轮不重新设计Four-Pane。HTML Review仍有C-REJECTED及部分修复待复验记录，本次推理审查不提供像素验收。**Final UI Master保持既有暂停/待门禁状态。**[R15]

## 24. 下一步与CEO直接答案

### 24.1 最少且有效的下一步

1. **先审本报告的N1–N5、N9与AC1–AC5。** 接受哪些原则，哪些只是待研究，写清Verdict / Disposition / Owner / Target Authority / Next Gate。不要一键把15份推导全部Frozen。
2. **由原推导Owner修正事实和相互矛盾。** 重点是完成状态、Pane、Result scope、有效粉丝、收入口径与陈旧Ledger。修正不等于准许改Current Authority。
3. **准备一个有真实机会的Content Growth验证方案。** 用已有系统承担目标、责任和证据；AiToEarn先作为只读机会/能力来源候选。后续真实接单、发布、费用和账号授权另按具体范围批准。
4. **定义真实经营验收。** 至少两轮；包含外部交付证据、延迟结果、一次失败/等待/恢复、成本记录以及下一轮为何改变。业务没有收入时如实记录，不能为了闭环编收入。
5. **用一个不同业务做合同压力测试。** 区分纸面可解释与真实运行证据。只有前者，不把它写作跨域已验收。

### 24.2 十二个问题，直接回答

**1. 最重要的三个发现？** 经营结果比工作数量重要；AI不能包办全部动作但产品必须接续完整责任；机会来源和外部执行边界决定业务能否落地。它们不是全部从零发现，今天的价值在于把已有原则逼近现实。

**2. 哪些是特例，哪些通用？** 抖音资格、平台钱包、CPE任务和发布方式是专业特例；身份/责任分离、证据时效、真实反馈、权限、人工接续、恢复和下一周期是通用原则。

**3. Curis如何定义自己？** 帮普通用户组织AI与必要人工协作，在边界内持续经营真实业务，并让目标、工作、结果和下一判断保持连续。

**4. 与Codex/Zcode/OpenClaw的真正区别？** 不是谁更会执行，也不是对方不能持续工作；Curis要证明跨业务责任、事实连续性和CEO协调效率的增量。目前仍是需要真实验收的差异。

**5. Content Growth还值得继续吗？** 值得，但先做一种可获取机会、可完成交付、可核验结果的模式；不要同时建全内容商业体系。

**6. AiToEarn解决了什么？** 提供多平台执行实现、状态和人工handoff参考，并有真实可读的任务市场。它没有自动把这些能力安装进Curis，本账号实际发布和收益链也未验收。

**7. 是否解决经营而不只是发布？** 部分是。市场条件、接单、交付、审核与官方收益工具流程属于经营；稳定利润、所有外部机会和完整自主循环未被本轮证明。

**8. 应不应该接？** 应进入小范围验证候选，先只读机会和可用性，再决定是否授权单任务执行。不建议立刻整体集成。

**9. 放哪一层？** Business Package消费的外部Opportunity Source与Capability/MCP Provider；平台细节在Adapter，不改Curis Core身份和执行真源。

**10. 哪些值得新基线候选？** N1经营连续性、N2真实能力状态、N3人工接续、N4员工责任分离、N5数据可信度、N9推导证据纪律；N6/N7应先作为专业业务候选验证。

**11. 哪些旧基线要重审？** 先修正研究中的竞争假设、业务/空间误读、平台后台搬运和未验收状态；当前结构不整体推翻。Conversation放置、四层scope必须守住；Department归属如要变更，提交明确Challenge。

**12. 下一步最应该做什么？** CEO选择接受的原则并退回矛盾，然后用一项真实业务跑出有证据的两轮经营。继续增加页面或名词，不能替代这项证明。

### 24.3 最终裁决

- FULL PRODUCT REASONING REVIEW: **本报告范围完成，存在明确待验证项；作者归属无法仅凭工作区完全认证。**
- ZCODE RESEARCH: **PARTIAL KEEP / CORRECTIONS REQUIRED。**
- NEW PRODUCT BASELINE: **CANDIDATE ONLY，未晋升。**
- AITO EARN: **真实Web操作 + 关键源码审查完成；发布/接单/收益E2E未完成。**
- CURRENT PRODUCT STRUCTURE: **UNCHANGED；研究冲突已登记。**
- ORIGINAL FULL COMPETITIVE RESEARCH / PIXEL ACCEPTANCE: **本报告不代替它们的完成门禁，不宣称整体完成。**
- NEXT: **STOP FOR CEO REVIEW。**

## 附录A：证据口径与可复查索引

L1=本轮真实操作；L2=公开源码；L3=官方文档/官方流程；L4=官方营销；L5=第三方/Issue报告；L6=推理。A=当前Authority/Implementation入口；R=被审查材料；H=历史材料。R中记录的前序L1不升级为本轮L1。仓库中存放的文字Playbook按L3，不因在GitHub就冒充已实现代码。

本报告没有生成Curis UI，没有调用Curis Runtime或数据库，没有运行第三方发布脚本，没有修改原研究文档。只新增本研究目录及独立外部源码目录。Pointer/Current State/Change Log未更新，因为没有晋升Current；本报告自身索引是研究入口。

### A：Current与实现入口
- **A1** [PRODUCT_DOCUMENT_POINTER.md](</Users/yy/Documents/Curis AI Workspace/docs/00_Context/PRODUCT_DOCUMENT_POINTER.md>) — Current Required Input路由；不是研究晋升许可。
- **A2** [Curis_Product_Blueprint.html](</Users/yy/Documents/Curis AI Workspace/docs/01_Product/Curis_Product_Blueprint.html>) — CURRENT/Frozen；重点持续经营、Business身份、四区、Strategy。
- **A3** [Curis_Product_Master_Map.md](</Users/yy/Documents/Curis AI Workspace/docs/01_Product/Curis_Product_Master_Map.md>) — CURRENT/Frozen；当前修订优先于旧checkpoint，Cycle/Assignment连续性。
- **A4** [CURIS_PRODUCT_STRUCTURE_BASELINE_PRE_DESIGN_RESEARCH.md](</Users/yy/Documents/Curis AI Workspace/docs/01_Product/CURIS_PRODUCT_STRUCTURE_BASELINE_PRE_DESIGN_RESEARCH.md>) — CURRENT/Frozen；四层scope、Package First、结构开放边界。
- **A4-Shell** [Curis_Workspace_Shell_Contract_And_Shared_Patterns.md](</Users/yy/Documents/Curis AI Workspace/docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md>) — Frozen空间职责；完整Conversation在Main。
- **A4-UI** [Curis_Product_UI_Blueprint.html](</Users/yy/Documents/Curis AI Workspace/docs/01_Product/Curis_Product_UI_Blueprint.html>) — Current UI消费入口；本轮核对相关空间条款。
- **A5** [CURRENT_STATE.md](</Users/yy/Documents/Curis AI Workspace/docs/00_Context/CURRENT_STATE.md>) — Implementation Truth路由；候选不等于整体Accepted。
- **A5-Log** [CHANGE_LOG.md](</Users/yy/Documents/Curis AI Workspace/docs/08_Change_Log/CHANGE_LOG.md>) — 窗口外的受控基线记录，不算本日新增交付。
- **A5-CG** [CONTENT_GROWTH_CHANNEL_CAPABILITY_EVIDENCE_AUDIT.md](</Users/yy/Documents/Curis AI Workspace/docs/reviews/CONTENT_GROWTH_CHANNEL_CAPABILITY_EVIDENCE_AUDIT.md>) — 历史范围内Review/Evidence；本轮不重新认证当前连接器实现。
- **A5-Contract** [CONTENT_GROWTH_SHARED_CONTRACT_PLAN.md](</Users/yy/Documents/Curis AI Workspace/docs/03_Design/CONTENT_GROWTH_SHARED_CONTRACT_PLAN.md>) — 核对发布策略与权限边界，不能从本报告授权实现。

### R：15份窗口内审查输入

这些是被审查材料；研究、推导及作者自审不因文件位于01_Product就成为Current。具体mtime与原始hash见E0。
- **R1** [CURIS_PRODUCT_DEFINITION_REBUILD.md](</Users/yy/Documents/Curis AI Workspace/docs/01_Product/CURIS_PRODUCT_DEFINITION_REBUILD.md>)
- **R2** [CURIS_FULL_PRODUCT_STRUCTURE_AND_INTERACTION_INVENTORY.md](</Users/yy/Documents/Curis AI Workspace/docs/01_Product/CURIS_FULL_PRODUCT_STRUCTURE_AND_INTERACTION_INVENTORY.md>)
- **R3** [CURIS_PRODUCT_DERIVATION_REBUILD.md](</Users/yy/Documents/Curis AI Workspace/docs/01_Product/CURIS_PRODUCT_DERIVATION_REBUILD.md>)
- **R4** [CURIS_PRODUCT_DERIVATION_ROUND1_CORRECTION.md](</Users/yy/Documents/Curis AI Workspace/docs/01_Product/CURIS_PRODUCT_DERIVATION_ROUND1_CORRECTION.md>)
- **R5** [CURIS_PRODUCT_DERIVATION_METHOD_V2_VALIDATION.md](</Users/yy/Documents/Curis AI Workspace/docs/01_Product/CURIS_PRODUCT_DERIVATION_METHOD_V2_VALIDATION.md>)
- **R6** [CURIS_PRODUCT_DERIVATION_GAP_REGISTER.md](</Users/yy/Documents/Curis AI Workspace/docs/01_Product/CURIS_PRODUCT_DERIVATION_GAP_REGISTER.md>)
- **R7** [CURIS_DOUYIN_REAL_PLATFORM_OPERATING_DEEP_DIVE.md](</Users/yy/Documents/Curis AI Workspace/docs/01_Product/CURIS_DOUYIN_REAL_PLATFORM_OPERATING_DEEP_DIVE.md>)
- **R8** [CURIS_CONTENT_GROWTH_BUSINESS_LOGIC_V2.md](</Users/yy/Documents/Curis AI Workspace/docs/01_Product/CURIS_CONTENT_GROWTH_BUSINESS_LOGIC_V2.md>)
- **R9** [CURIS_CONTENT_GROWTH_BUSINESS_TO_PRODUCT_TRANSLATION.md](</Users/yy/Documents/Curis AI Workspace/docs/01_Product/CURIS_CONTENT_GROWTH_BUSINESS_TO_PRODUCT_TRANSLATION.md>)
- **R10** [CURIS_CONTENT_GROWTH_FULL_PRODUCT_CAPABILITY_DERIVATION.md](</Users/yy/Documents/Curis AI Workspace/docs/01_Product/CURIS_CONTENT_GROWTH_FULL_PRODUCT_CAPABILITY_DERIVATION.md>)
- **R11** [CURIS_CONTENT_GROWTH_AI_USER_OPERATING_BOUNDARY.md](</Users/yy/Documents/Curis AI Workspace/docs/01_Product/CURIS_CONTENT_GROWTH_AI_USER_OPERATING_BOUNDARY.md>)
- **R12** [CURIS_PRODUCT_CAPABILITY_DERIVATION_LEDGER.md](</Users/yy/Documents/Curis AI Workspace/docs/01_Product/CURIS_PRODUCT_CAPABILITY_DERIVATION_LEDGER.md>)
- **R13** [CURIS_BUSINESS_TO_PRODUCT_TRANSLATION_LEDGER.md](</Users/yy/Documents/Curis AI Workspace/docs/01_Product/CURIS_BUSINESS_TO_PRODUCT_TRANSLATION_LEDGER.md>)
- **R14** [CURIS_CONTENT_GROWTH_PRODUCT_LANGUAGE_DERIVATION.md](</Users/yy/Documents/Curis AI Workspace/docs/01_Product/CURIS_CONTENT_GROWTH_PRODUCT_LANGUAGE_DERIVATION.md>)
- **R15** [CURIS_HTML_RECONCILIATION_REVIEW.md](</Users/yy/Documents/Curis AI Workspace/docs/prototypes/full-product-html/CURIS_HTML_RECONCILIATION_REVIEW.md>) — 待复验状态，不作像素通过证据。

### H：历史AiToEarn研究
- **H1** [aitoearn-reuse-research.md](</Users/yy/Documents/Curis AI Workspace/docs/research/aitoearn-reuse-research.md>) — 历史来源，不覆盖Current。
- **H2** [aiearn-content-marketing-reuse-plan.md](</Users/yy/Documents/Curis AI Workspace/docs/research/aiearn-content-marketing-reuse-plan.md>) — 历史来源，不覆盖Current。
- **H3** [aiearn-asset-mapping.md](</Users/yy/Documents/Curis AI Workspace/docs/research/aiearn-asset-mapping.md>) — 历史来源，不覆盖Current。
- **H4** [aiearn-content-marketing-final-decision.md](</Users/yy/Documents/Curis AI Workspace/docs/research/aiearn-content-marketing-final-decision.md>) — 历史来源，不覆盖Current。
- **H5** [Curis_AiToEarn_Architecture_Review.md](</Users/yy/Documents/Curis AI Workspace/docs/03_Design/Curis_AiToEarn_Architecture_Review.md>) — 历史来源，不覆盖Current。

### S：公开源码与符号索引

主仓库：`yikart/AiToEarn@9413d73918271bd716b9ea59f61c9f59e485619b`；插件：`yikart/aitoearn-openclaw-plugin@c5c5e722b150167249aafa448ebaee80cb4d3840`。下列链接固定commit。除特别说明外为L2静态阅读，未运行源码测试。
- **S1** [UnifiedMcpModule](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/unified-mcp/unified-mcp.module.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/unified-mcp/unified-mcp.module.ts`；统一MCP模块边界与导入。
- **S1-Tools** [ChannelsMcpController](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/mcp/channels.mcp.controller.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/mcp/channels.mcp.controller.ts`；发布、查询、数据、评论工具。
- **S2** [PlatformIntegrationRegistry](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/platforms.registry.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/platforms.registry.ts`；按Provider方法和配置生成能力元数据。
- **S3** [PublishRecord](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/libs/mongodb/src/schemas/publish-record.schema.ts) — `project/aitoearn-backend/libs/mongodb/src/schemas/publish-record.schema.ts`；流程/账号/平台状态、作品引用与唯一索引。
- **S4** [PublishTaskService.processPublishJob](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/publish/tasks/publish-task.service.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/publish/tasks/publish-task.service.ts`；发布队列与waiting/finalize/retry分支。
- **S4-State** [PublishStateService](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/publish/tasks/publish-state.service.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/publish/tasks/publish-state.service.ts`；条件状态更新；本轮按相关方法阅读，非全类审计。
- **S5** [DouyinPublishProvider](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/douyin/douyin-publish.provider.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/douyin/douyin-publish.provider.ts`；用户handoff和结果查询。
- **S6** [RelayClientService](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/relay/relay-client.service.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/relay/relay-client.service.ts`；远端Relay桥及资源转发。
- **S6-Callback** [RelayCallbackController.handleRelayCallback](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/relay/relay-callback.controller.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/relay/relay-callback.controller.ts`；账号/完成回调处理。
- **S7** [AnalyticsService.fetchAccountAnalytics](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/analytics/analytics.service.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/analytics/analytics.service.ts`；用户账号范围、Provider/Relay、快照与不支持分支。
- **S8** [usePublishDialogStorageStore](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-web/src/components/PublishDialog/usePublishDialogStorageStore.tsx) — `project/aitoearn-web/src/components/PublishDialog/usePublishDialogStorageStore.tsx`；IndexedDB草稿恢复与失效账号/媒体过滤。
- **S8-Close** [useCloseDialog](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-web/src/components/PublishDialog/hooks/useCloseDialog.tsx) — `project/aitoearn-web/src/components/PublishDialog/hooks/useCloseDialog.tsx`；关闭确认。
- **S9** [useValidatedPublishTrigger](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-web/src/components/PublishDialog/hooks/useValidatedPublishTrigger.ts) — `project/aitoearn-web/src/components/PublishDialog/hooks/useValidatedPublishTrigger.ts`；发布前错误聚焦和阻止提交。
- **S10** [definePluginEntry/register](https://github.com/yikart/aitoearn-openclaw-plugin/blob/c5c5e722b150167249aafa448ebaee80cb4d3840/packages/runtime/index.ts) — `packages/runtime/index.ts`；环境过滤、动态工具注册、实际callMcpTool桥、金额单位说明。
- **S10-Schema** [工具schema处理](https://github.com/yikart/aitoearn-openclaw-plugin/blob/c5c5e722b150167249aafa448ebaee80cb4d3840/packages/runtime/src/tools.ts) — `packages/runtime/src/tools.ts`；工具快照、schema规范化；不证明远端当前可用。
- **S11** [loadToolDefinitionsSync](https://github.com/yikart/aitoearn-openclaw-plugin/blob/c5c5e722b150167249aafa448ebaee80cb4d3840/packages/runtime/src/tool-discovery.ts) — `packages/runtime/src/tool-discovery.ts`；远端发现、超时与缓存回退。
- **S12** [callMcpTool / runWithMcpRetry](https://github.com/yikart/aitoearn-openclaw-plugin/blob/c5c5e722b150167249aafa448ebaee80cb4d3840/packages/shared/src/mcp-client.ts) — `packages/shared/src/mcp-client.ts`；Streamable HTTP、连接管理与传输重试。
- **S13** [官方工具说明](https://github.com/yikart/aitoearn-openclaw-plugin/blob/c5c5e722b150167249aafa448ebaee80cb4d3840/packages/runtime/skills/aitoearn-earn/references/current-mcp-capability.md) — `packages/runtime/skills/aitoearn-earn/references/current-mcp-capability.md`；L3：市场、Affiliate、Campaign等工具清单。
- **S13-Paths** [官方收益路径](https://github.com/yikart/aitoearn-openclaw-plugin/blob/c5c5e722b150167249aafa448ebaee80cb4d3840/packages/runtime/skills/aitoearn-earn/references/monetization-paths.md) — `packages/runtime/skills/aitoearn-earn/references/monetization-paths.md`；L3：经营方法，而非服务端代码。
- **S13-Loop** [官方执行Playbook](https://github.com/yikart/aitoearn-openclaw-plugin/blob/c5c5e722b150167249aafa448ebaee80cb4d3840/packages/runtime/skills/aitoearn-earn/references/execution-playbooks.md) — `packages/runtime/skills/aitoearn-earn/references/execution-playbooks.md`；L3：接单、交付、结果与下一轮。

### D：官方文档与版本资料
- **D1** [发布流程](https://docs.aitoearn.ai/zh/use/publish-flow/index.md)；[本轮保存副本](</Users/yy/Documents/Curis AI Workspace/docs/research/full-product-rethink-2026-09-14/official-publish-flow.md>)。L3，2026-09-14读取。
- **D2** [插件发布](https://docs.aitoearn.ai/zh/use/plugin-publish/index.md)；[本轮保存副本](</Users/yy/Documents/Curis AI Workspace/docs/research/full-product-rethink-2026-09-14/official-plugin-publish.md>)。L3，2026-09-14读取。
- **D3** [创作者任务](https://docs.aitoearn.ai/zh/help/creator/index.md)；[本轮保存副本](</Users/yy/Documents/Curis AI Workspace/docs/research/full-product-rethink-2026-09-14/official-creator.md>)。L3，2026-09-14读取。
- **D4** [广告主任务](https://docs.aitoearn.ai/zh/help/advertiser/index.md)；[本轮保存副本](</Users/yy/Documents/Curis AI Workspace/docs/research/full-product-rethink-2026-09-14/official-advertiser.md>)。L3，2026-09-14读取。
- **D5** [短剧流程](https://docs.aitoearn.ai/zh/help/short-drama/index.md)；[本轮保存副本](</Users/yy/Documents/Curis AI Workspace/docs/research/full-product-rethink-2026-09-14/official-short-drama.md>)。L3，2026-09-14读取。
- **D6** [收益分配说明](https://docs.aitoearn.ai/zh/help/revenue-sharing/index.md)；[本轮保存副本](</Users/yy/Documents/Curis AI Workspace/docs/research/full-product-rethink-2026-09-14/official-revenue-sharing.md>)。L3，2026-09-14读取。
- **D7** [v2.5.0](https://github.com/yikart/AiToEarn/releases/tag/v2.5.0)、[v1.8.0](https://github.com/yikart/AiToEarn/releases/tag/v1.8.0)；Release公告不等于线上构建ID。

### G：Issues / PR
- **G1** [#566](https://github.com/yikart/AiToEarn/pull/566) — 开源2.5同步，merged。
- **G2** [#587](https://github.com/yikart/AiToEarn/pull/587) — TikTok去重修复，closed但未merged。
- **G2-Engage** [#571](https://github.com/yikart/AiToEarn/pull/571) — 互动扩展，closed但未merged。
- **G2-Dedup** [#570](https://github.com/yikart/AiToEarn/pull/570) — 去重扩展，closed但未merged。
- **G3** [#586](https://github.com/yikart/AiToEarn/issues/586) — 重复发布报告，未复现。
- **G4** [#581](https://github.com/yikart/AiToEarn/issues/581) — 抖音Relay回调报告，closed不等于本轮复验。
- **G5** [#592](https://github.com/yikart/AiToEarn/issues/592) — Facebook失败报告，未复现。
- **G6** [#575](https://github.com/yikart/AiToEarn/issues/575) — 请求未到达服务，不作为服务故障证据。

### E：本轮证据和测试对象
- **E0** [输入清单与hash](</Users/yy/Documents/Curis AI Workspace/docs/research/full-product-rethink-2026-09-14/input-inventory.json>)；[git status起始快照](</Users/yy/Documents/Curis AI Workspace/docs/research/full-product-rethink-2026-09-14/git-status-snapshot.txt>)；[docs diff统计](</Users/yy/Documents/Curis AI Workspace/docs/research/full-product-rethink-2026-09-14/git-diff-docs-stat.txt>)。
- **E1** [发布页面截图](</Users/yy/Documents/Curis AI Workspace/docs/research/full-product-rethink-2026-09-14/evidence/01-publish.png>)。同目录txt保存相应DOM状态（有保存的项目）。
- **E2** [真实市场截图](</Users/yy/Documents/Curis AI Workspace/docs/research/full-product-rethink-2026-09-14/evidence/02-market.png>)。同目录txt保存相应DOM状态（有保存的项目）。
- **E3** [任务详情截图](</Users/yy/Documents/Curis AI Workspace/docs/research/full-product-rethink-2026-09-14/evidence/03-task-detail.png>)。同目录txt保存相应DOM状态（有保存的项目）。
- **E4** [频道离线/插件未安装](</Users/yy/Documents/Curis AI Workspace/docs/research/full-product-rethink-2026-09-14/evidence/04-channel-state.png>)。同目录txt保存相应DOM状态（有保存的项目）。
- **E5** [研究草稿箱](</Users/yy/Documents/Curis AI Workspace/docs/research/full-product-rethink-2026-09-14/evidence/05-research-draft-box.png>)。同目录txt保存相应DOM状态（有保存的项目）。
- **E6** [发布编辑器入口](</Users/yy/Documents/Curis AI Workspace/docs/research/full-product-rethink-2026-09-14/evidence/06-publish-preflight.png>)。同目录txt保存相应DOM状态（有保存的项目）。
- **E7** [关闭恢复提示，未验证正文恢复](</Users/yy/Documents/Curis AI Workspace/docs/research/full-product-rethink-2026-09-14/evidence/07-close-recovery.txt>)。同目录txt保存相应DOM状态（有保存的项目）。
- **E8** [无采集数据与零值并存](</Users/yy/Documents/Curis AI Workspace/docs/research/full-product-rethink-2026-09-14/evidence/08-data-stats.txt>)。同目录txt保存相应DOM状态（有保存的项目）。

保留的研究对象：AiToEarn草稿箱 **CURIS-RESEARCH-TEST-2026-09-14**。没有需要撤销的发布/接单/付费操作；未主动删除测试对象。

### 证据限制

- 主仓库与插件采用固定commit阅读；线上build未知，不作完全同版本断言。
- 公开主仓库中针对市场工具/实体名称的检索未命中完整实现，只能说明本次检索覆盖内未定位；不是证明市场所有代码必然闭源。
- 未对当前账号认证调用MCP，也未验证评论、发布、接单、结算、离线恢复；不能把文档能力转成账号可用性。
- 原Curis材料中的实现边界主要回到当前Router与已有Review，本轮没有重跑Curis Runtime；旧Review的缺失不能自动代表今日所有代码状态。
- 第三方运行材料按证据读取，未执行其中的账号、收益或安装指令。
- 研究报告中所有架构建议为L6，等待CEO裁决，不写入Frozen。
