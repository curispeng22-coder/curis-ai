# THREE-DOCUMENT CONSISTENCY AUDIT

Status: READY FOR CEO FINAL PRODUCT TRUTH REVIEW  
日期：2026-08-18  
Owner：Product Architecture Authority Consolidation  
范围：唯一 Product Blueprint、Product Master Map、UI Blueprint 及其上位 Frozen Authority  

## 0. 审计结论

三份文档已经共享同一条产品方向：Curis 是普通用户可使用的 AI Company OS；Company OS 固定、Workspace 开放；人才与能力负责外部能力发现；员工、结果、资料、会议和 CEO 决策形成经营闭环。Final Delta 已完成当前产品空间、经营洞察、公司版图、Business Exit 与 CEO 跨日连续性的语义对齐；剩余事项是 CEO 最终 Product Truth Review 以及后续 Runtime / UI 实现依赖，不再是三文档模型冲突。

本轮不创建第二套产品结构，也不修改 Runtime、Schema、Prototype 或代码。审计后将：

1. 由 Product Blueprint 收口产品模型和用户语义；
2. 由 Master Map 展开页面、字段、动作、入口和反向入口；
3. 由 UI Blueprint 消费前两者并表达空间，不反向改变模型；
4. 对与 Frozen Shared Authority / Frozen Workspace Shell 的潜在冲突保留 `REVIEW REQUIRED`，不自行强制改写。

## 1. 三份文档当前各自定义了什么

| 文档 | 当前贡献 | 当前状态 |
| --- | --- | --- |
| Product Blueprint 5.3 | 产品身份、七个主区域、经营洞察、Company/Department/Role/Employee、人才与能力、Workspace、资料库、Assistant、结果/会议/成长、产品反推能力、Business Exit、CEO 跨日连续性 | 当前产品语义权威；经营洞察为第七个一级导航，等待 CEO Final Product Truth Review |
| Product Master Map 3.0（原 v2.0 文件原位升级） | 对 Blueprint 的结构化展开：用户路径、CEO 工作台、经营洞察、Analyst/Report/Visualization、组织版图、人才与能力、资料、会议、Workspace、Desktop 壳、CEO 注意力及对象字段合同 | 当前合同集中在文件前部 `CURRENT v3.0 CONTRACT`；原 §1–24 仅作历史推导，冲突处不得继续作为产品规则 |
| UI Blueprint 1.0 | 七区导航、四 Pane/Adaptive Surface、Employee Workstation、Composer、Conversation、会议、经营洞察、Studio 和 Workspace 视觉/空间消费关系 | 已消费公司版图 / 员工目录、人才与能力、Employee 三态与 Operating Intelligence Baseline；最终组件与像素仍留给 UI 专项 |

## 2. 粒度差异与真实冲突

> **历史审计边界：** 本节及其后的 §3–§6 保留 Final Delta 之前的审计过程与判断，便于追溯；其中关于“六区”“九个产品空间”或旧正式名称的表述不再是 Current Product Truth。最终收口以本文件 §7D 与三份 Current 文档前部为准。

### 2.1 只是粒度不同

- Blueprint 讲“业务空间是开放的专业办公室”，Master Map 补充了 Portal、Studio 和三类样板，UI Blueprint 补充 Pane 与 Conversation；这是层级展开，不是三套产品。
- Blueprint 讲“员工 = 有公司身份的专家/Agent”，Master Map 和 UI Blueprint 分别补充 Workstation、Employee Row、Composer；这些是表现层与运行支撑，不改变员工产品定义。
- Blueprint 与 Master Map 都保留真实结果、来源、CEO 验收、失败恢复；UI Blueprint 将其表现为状态、Utility 和返回原工作现场；属于同一闭环的不同视图。

### 2.2 需要修正的结构漂移

| 发现 | 判断 | 处理 |
| --- | --- | --- |
| Blueprint 的主导航曾是六区；Operating Intelligence UX Baseline 后确认经营洞察成为第七区 | 产品空间与导航层级已完成最终收敛 | Final Delta 已将七个一级产品统一写入 Blueprint / Master Map / UI；对话仍为独立工作 Surface，设置仍由头像菜单进入 |
| Blueprint 的 Organization 仍以 Department/Position/Employee/Workspace Team 为主 | 缺少 Company→Department→Business→Role→Employee Binding 的经营阅读顺序，且没有明确 Employee 是可替换执行主体 | 增加组织链、Role Detail、Employee Directory/Profile 和招聘/组队分离；保留 Department 渐进形成与 Frozen Business=Team+Office |
| Business、Workspace、Workflow 在不同文件中接近同义 | 会让 UI 把 Business Detail 做成 Workspace 运行页，或把 Workflow 做成 Runtime DAG | 正式分离 Business Detail、Business Workflow Definition、Workspace Task Flow Runtime；不新增底层 Runtime primitive |
| “能力中心/AI 团队/知识与成果/财务/日历”在旧 UI/视觉目录中出现为平级页面 | 与当前六区模型冲突或属于 Workspace/头像/资料库内的细分面 | 收敛为人才与能力、资料库、设置、业务 Workspace 内部专业视图；保留历史页面作为非权威参考，不删除历史 |
| Settings 在 Blueprint/Master Map 主要是头像菜单描述 | 不缺能力，但缺 IA 与 Model Provider/Agent Provider 分离 | 吸收 Settings Research 的六组 IA；设置仍不占一级导航，作为产品空间可从头像或上下文进入 |
| Conversation 在 Blueprint 分成 Assistant/Employee/Meeting/Thread，但没有同一 Employee Conversation 的双入口真相 | 可能出现 Workspace 和全屏对话两套记录 | 明确 Employee Conversation 是同一记录，在 Workstation 与 Full Main Conversation 中投影；最近工作只是快捷入口 |

## 3. CEO 工作台历史定义检查

没有找到正式 Supersede 记录推翻 CEO 工作台的历史职责。公司状态、业务运行、公司事件流、今日简报、Needs CEO、风险提示仍是有效产品职责，不能因导航重构被删除。

- **Activity**：发生了什么；
- **Notification**：哪些值得 CEO 知道；
- **Needs CEO**：哪些需要 CEO 行动；
- **Blocked**：工作状态为何无法继续；
- **Assistant**：消费同一事实、排序、解释、协调和跟进，不建立第二状态系统。

审计判断：此前文档存在“职责已保留但页面契约不够显式”的遗漏，属于 Authority Drift / Design Gap，不是 Superseded。Blueprint 和 Master Map 将补一条明确契约；UI 只表达，不重新定义。

## 4. Frozen Authority 复核

| Frozen Authority | 结论 |
| --- | --- |
| Company OS Shared Authority §9：长期 Business = Operating Team + Business Workspace；渐进工作形态合法 | 与 Company→Department→Business→Role→Employee Binding 兼容。Department 仍不是招聘前置；短期 Conversation/Task/临时团队可合法停止 |
| Workspace Shell Contract：六区导航、四 Pane、Main 自成立、Employee Workstation 属于 Main 工作区 | 本轮消费，不改 Shell；“对话/设置”作为产品空间而非新增导航。任何 Shell 语义冲突保留 Review Required |
| Design System / Frozen Visual Spec | 只影响 UI 表达，不在本轮改令牌或视觉像素 |
| Settings Research / CEO Review V1 | 作为 Settings IA 输入，Provider 与 Agent Provider 保持分离 |

## 5. 新产品模型缺口

本轮正式补齐以下产品契约：

1. 九个产品空间与六个一级导航的关系；
2. Company→Department→Business→Role→Employee Binding；一人多岗、一岗多人、Role 拆分、Sub-team；
3. Business Detail 与 Business Workspace 分离；Business Workflow Definition 与 Workspace Task Flow Runtime 分离；
4. Role Detail 的责任、能力、容量、负载和绑定字段；
5. Employee Directory 的 Employment Status / Work Status 分离，以及员工档案字段；
6. Create Where You Organize / Add Where You Work；选择已有、创建新的、从市场获取；
7. 人才与能力中的 Expert、Skill、Connector、职业能力组合/岗位能力包；
8. Employee Conversation 的同一真相与双入口；
9. Meeting 完整链路与 Business Feedback 回写；
10. Workspace Engineering 完成长期业务建设后，必须登记回同一 Company OS Business Truth；
11. Settings 六组 IA 与 Model Provider / Agent Provider 分离；
12. Master Map/UI 的页面级字段、动作、反向入口和来源权威。

## 6. 重大变更记录（原定义 → 新定义 → 影响）

| 原定义 | 新定义 | 影响范围 |
| --- | --- | --- |
| 六个区域 + 设置/对话为跨层能力 | 九个产品空间；六个继续占一级导航，对话、设置和数据洞察为不占一级导航的产品空间 | Blueprint 产品空间表、Master Map 页面合同、UI IA；不改 Frozen 六区 Shell |
| 组织以 Department/Position/Employee 为主 | Company→Department→Business→Role→Employee Binding，Employee 为可替换执行主体 | Organization、Business、Role、Employee 页面；不强制 Department |
| Workspace 可承载业务与流程，但边界隐含 | Business Detail（经营定义）≠ Business Workspace（专业运行）；Workflow Definition ≠ Task Flow Runtime | Business 页面、Workspace Portal/Studio、运行实现映射 |
| 人才市场主要是专家/技能/连接器发现 | 人才与能力 = Expert/Skill/Connector + 职业能力组合/岗位能力包；专家经招募和公司关系后才成为 Employee | Talent、Organization、Employee、Settings |
| 员工是专家/Agent，档案字段未完整列出 | Employee Directory/Profile 同时呈现身份、岗位、状态、能力、工作、结果、成长和运行配置 | Organization UI、Employee Workstation、审计/权限 |
| 设置是头像菜单能力集合 | 设置是完整产品空间，头像是入口；六组 IA，Provider 类型分开 | Settings UI 与上下文返回 |
| Business 只能创建，复用关系未定义 | Business Duplication 从已验证 Operating Model 创建独立 Business Identity；Copy Preview 明确复用、重配和禁止复制 | Business Detail、Business Space、Organization Center、Workspace 返回；不复制员工身份、凭证、执行、结果或历史 |

## 7A. CEO Confirmed Product Delta（历史记录；已被 §7D 收口）

本节记录本轮 CEO Review 已确认、已回写三份当前文档的 Delta；本节不是新 Blueprint，也不授权代码实现。

1. **Current Truth 去重**：Master Map 原 v2.0 的 §1–24 明确标记为 `HISTORICAL / SUPERSEDED APPENDIX`；文档前部的 v3.0 页面合同、唯一 Product Blueprint v5.2 与 UI Blueprint 同步章节才是当前组织、页面和命名。Runtime / Internal 关系继续保留，但与 Product Organization Map 分层阅读。
2. **正式一级名称**：统一为“人才与能力”；Market / Discover 是内部 Surface。三份当前文档不再把“人才市场”作为一级产品名称，历史章节中的旧称仅用于来源追溯。
3. **Employee UI Status**：共享员工状态只消费 Frozen Shell 的“空闲 / 工作中·<desc> / 阻塞·<cause>”；已完成、等待和是否达成归 Goal / Task / Result，不修改 Runtime Schema。
4. **字段级展开**：Master Map 前部 `CURRENT v3.0 CONTRACT` 已逐字段覆盖 Company、Department、Business、Role、Employee Profile、Expert、Skill、Connector、Meeting、Settings、Business Duplicate，并为每个对象列出 Page Mission、Entry、Sections、Fields、Actions、Create/Edit Fields、Drill-down、Reverse Entry、Shared/Domain/Mixed、Source Authority。
5. **Organization Center**：正式收敛为“公司版图 / 员工目录”。默认阅读为 Company → Department → Business → Business Operating Model → Role Structure → Employee Binding；Business 进入 Business Detail / Operating Model，不直接跳 Workspace；Role 展开后才查看 Employee Binding；协作关系仅按需打开。
6. **成长与复制联动**：公司版图展示新增 Business、扩张、Role 增加/拆分、Staffing、空岗、Department/grouping、Business Duplication 后的新独立经营单元；新 Business 只登记一次并出现在同一 Company Map / Organization Truth，不新增 Runtime Primitive。

### Delta recheck

| 检查项 | 结果 |
| --- | --- |
| 旧组织模型 | 仅在 Master Map 原 §1–24 历史区保留；文档前部 v3.0 页面合同 / Blueprint / UI 已替换 |
| “人才市场”旧正式名称 | 当前三份文档统一“人才与能力”；旧称仅作为历史来源或专项文件名称 |
| Employee completed/waiting | 已从 Shared Employee UI Status 移除；仅在 Goal / Task / Result 语义中出现 |
| Organization 三视图旧规则 | 当前默认只有公司版图 / 员工目录；协作关系改为按需视图 |
| 字段级展开不足 | Master Map 前部 `CURRENT v3.0 CONTRACT` 已完成 12 个核心对象逐字段合同，新增 Insights |

本轮状态：`PASS WITH DELTA — STOP FOR FINAL REVIEW`。

## 7B. CEO Final Cleanup（待验收）

本轮仅处理 stale / conflict cleanup，不扩展产品模型：

- Product Blueprint 的 Employee 示例改为三态；完成 / 等待只在 Goal / Task / Result 中表达。
- UI Blueprint 的 Composer 统一消费 Frozen Shell 槽位：Input、+、访问权限、工作模式、已选资源、Model·Agent、Voice、Send。
- UI Blueprint 明确 Global Capability（搜索、通知、CEO Assistant）不等于 Global Topbar；Workspace 只使用 Pane-local Header。
- Master Map 原 v2.0 内容仍保留，但已在前部声明为 `HISTORICAL / SUPERSEDED APPENDIX`；前部 v3.0 页面合同是唯一 Current Contract 阅读入口。
- Current 文件名收敛为 `Curis_Product_Blueprint.html`、`Curis_Product_Master_Map.md`、`Curis_Product_UI_Blueprint.html`；Pointer、AGENTS、Current State、当前产品/设计引用已迁移，历史 Review / Migration / Closure 文档保留原始路径语义。

最终扫描项：Employee completed/waiting、旧 Composer、Global Topbar 误读、人才市场 Current 正式名称、旧 Organization Current 规则，均已在当前三份文档清除或标为历史；本节状态 `READY FOR CEO ACCEPTANCE`。

## 7C. Bounded Final Delta — 数据洞察（历史记录）

本轮恢复的是历史产品能力在 Consolidation 中的遗漏，不是重新发明第二套分析产品。三份 Current 真源现已同步：

1. Product Blueprint 将“数据洞察”定义为正式产品空间，职责是消费既有 Company Truth、Result、Usage、Cost、Execution、Feedback、Review；CEO 工作台仍负责注意力、异常、简报、结果、待处理和下一决定。
2. Master Map 增加完整 Insights Page Contract：范围、入口/返回、Sections、逐字段指标、Actions、Filters、Compare、Drill-down、Reverse Entry、Source Authority 与 Shared / Domain / Mixed 边界；对象字段合同由 11 个扩展为 12 个。
3. UI Blueprint 增加 Insights 空间合同和 CEO Desk / Insights 边界；所有指标必须显示 source / freshness / unknown / manually entered。不同 Model / Agent 的比较必须关联 Result Quality、CEO Acceptance 与 External Business Result。
4. 三份文档均保留 `NAVIGATION PLACEMENT — REVIEW REQUIRED`：数据洞察先从 CEO Desk、Business、Workspace、Employee Profile、公司版图和 Assistant 进入 scoped view，不改变 Frozen 六区，也不新增 Runtime / Schema / Analytics Truth。
5. 同轮完成 UI Blueprint 重复章节编号清理，并将 Master Map Settings contract 同步为 Settings Research 的六组 IA 与 Model Provider / Agent Provider 分离。

本轮严格为产品/治理文档变更；未修改 Runtime、Schema、数据库、Frozen Shell、代码或高保真设计。该节为本次统一 Delta 前的历史记录；当前以 §7D 为准。

## 7D. CURIS FINAL PRODUCT ARCHITECTURE DELTA（待 CEO Final Product Truth Review）

本轮已一次性消费 CEO 已接受的 Operating Intelligence UX Baseline、Company Map Variant A / Department Container、Business Exit Lifecycle 与 CEO Operating Day Cross-day Continuity：

- Product Blueprint v5.3：经营洞察 / Operating Intelligence 成为第七个一级产品空间；补入默认 Company Support Organization、Analyst 责任分层、Business Exit 与 CEO 跨日连续性。
- Master Map v3.0：补入经营洞察 IA、Report / Analyst / Visualization / Data Trust / Benchmark 合同，以及 Business Exit / CEO Operating Day 跨层合同。
- UI Blueprint：同步七区导航、经营洞察工作区、报告与 Conversation、语义安全图表切换、Company Map 与退出/跨日表达。

### 一致性复核

| 检查项 | 结果 |
| --- | --- |
| 一级产品 | 三份统一：CEO 工作台、业务空间、组织中心、人才与能力、经营洞察、资料库、会议 |
| 经营洞察边界 | 三份统一为既有 Truth / Result / Usage / Cost / Execution / Feedback / Review 的消费面；不创建第二套 Analytics Runtime；CEO Desk 负责注意力，经营洞察负责深度分析 |
| Analyst / Report | 三份统一 Company Analyst（数据分析部）与 Business Analyst 分层；Report 结构 FACT / INTERPRETATION / UNKNOWN / RECOMMENDATION / EVIDENCE；解释不升级为 Company Fact |
| Company Map | 三份统一 Department Container → Business → Role / Staffing → Employee Reference；Business Detail 不直接跳 Workspace；Duplicate 回同一 Company Map |
| Business Exit | 三份统一 Pause / Reduce / Transfer / Close / Merge / Split 进入 Business Detail Actions，不新增 Exit Center / Runtime Primitive |
| CEO Operating Day | 三份统一 Brief → Matters → Handoff → Decision → Exception → Evidence → Learning → Closeout 跨日承接，不新增 OperatingDay Primitive |
| 状态与来源 | 三份统一 Source / Freshness / Verified / Manual / Unknown / Stale / Missing / External；不以未知显示 0，不以图表生成无合同健康结论 |

本轮状态：`READY FOR CEO FINAL PRODUCT TRUTH REVIEW`。未修改代码、Runtime、Schema、数据库、Frozen Shell 或高保真设计。

## 7. 仍需 CEO Review 的真实冲突

1. “对话、设置”是否永远作为不占一级导航的产品空间，还是未来要升级为一级导航。当前七个一级产品空间已确认；对话与设置继续作为不占一级导航的产品空间。
2. Business Detail 的“Business Workflow Definition”在 UI 上是否需要独立编辑面，还是仅作为 Business Detail 的一个 Section。产品语义已确定，呈现层待 UI 专项设计。
3. Role 是否允许脱离 Business 先创建。当前支持渐进组织和 Role 独立存在，但具体创建入口由 Master Map/UI 表达。
4. Workspace Engineering 的长期建设结果如何登记 Company OS Truth，当前只有产品原则，未形成 Runtime/API 实现契约。
5. 人才与能力 Market / Discover 的外部来源、许可证、适配器和撤回责任仍是 Review 文档，不能被当作已接入能力。
6. Business Template 与 Business Duplication 的底层持久化关系尚未形成 Frozen Runtime/Schema 契约；本轮只确认产品关系，不新增 Runtime Primitive。一个 Business 服务多个外部账号的适用性仍由 Domain Operating Model 决定。

## 8. 审计后的交付顺序

```text
Product Blueprint（本轮先收口产品语义）
→ Product Master Map（页面/字段/动作/入口展开）
→ UI Blueprint（空间/IA/表面消费）
→ Business Runtime Blueprint / Issue
→ Code / Browser / Desktop / Runtime evidence
```

本审计是工作稿，不是第二份 Blueprint。它保留冲突与缺口，供 CEO Review 和后续实现排队使用。
