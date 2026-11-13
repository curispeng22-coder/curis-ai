# 代码 vs 产品蓝图 v5.0 审查报告

- **审查日期**：2026-08-07
- **审查基准**：`docs/01_Product/Curis_Product_Blueprint.html`（v5.0 · Single Current · Status: Review）
- **审查对象**：当前 `frontend/app/**` Next 代码 + 已交付后端双轨能力供给（#94）+ 已读 UI 原型 `curis-ui-prototype/_system/canonical-nav.js`
- **方法**：以蓝图为结构权威，盘点前端路由、导航数据源、关键页面实际交付，逐节对照蓝图 §03 App 地图 / §04 导航动线 / §07 能力中心 / §08 Workspace / §09 结果决策 / §10.7 红线 / §12 完成证明
- **结论总评**：当前代码已交付一个"能走通经营闭环"的可运行 v1 雏形，三大红线（不彩色 Dashboard / 不默认 Full Auto / 不 Agent Center）遵守良好。但存在一处**结构性偏离**（导航未对齐蓝图 7 组、能力中心被排除出主导航）、一处**闭环缺口**（决策→承诺后端未接通）、一处**范围残留**（Platform/Admin 超出 v1）。

---

## 1. 导航结构对照（蓝图 §04）— 主要偏离

蓝图 §04 定义 **7 个导航组**，当前代码（`frontend/components/terra/TerraNavData.js`）使用 **5 个组**，且对齐的是静态原型 `canonical-nav.js` 而非蓝图。两套基线冲突时未以蓝图为结构权威。

| 蓝图 §04 导航组 | 蓝图包含 | 当前代码 | 偏差 |
|---|---|---|---|
| 今日经营 | CEO Desk、Assistant 汇报、待决策、待验收、时间线 | 并入「公司」组的「CEO 工作台」单一项 | 未独立成组，组层级丢失 |
| 经营 | 公司脉搏、投入产出、风险、变化、决策 | 「公司」组内单一项 → `/ceo-office/analytics` | 页面本身好，但组层级丢失 |
| 业务 | 业务版图、业务详情、新业务、阶段决策 | 「业务版图」单一项 | 基本对齐（子集） |
| 公司 | AI 团队、岗位、部门、能力中心、资源 | 「公司」组含 AI 团队 / 工作空间，**不含能力中心** | **能力中心缺失** |
| 工作空间 | Workspace Portal、Studio、研发/小红书/抖音办公室 | 「公司」组「工作空间」单一项（子页未在 nav 展开） | 子办公室未露出 |
| 公司资产 | 成果、知识、记忆、财务、日历 | 「公司资源」组：成果库/知识库/财务/日历 | 改名 + **记忆缺失于 nav** |
| 经营工具 | 会议工作台、决策室、证据审查 | 「经营工具」组：会议工作台/决策室 | **证据审查缺失** |

**额外偏离**：当前代码多出「兼容入口」组（旧项目 / 旧执行 / 旧任务流水线）。蓝图无此组，属历史残留页面。按记忆 #14（旧结构清理纪律），不在双基线内的孤岛页/死链默认动作是**舍弃、不进导航**，不应作为常驻分组。

**能力中心可达性**：页面 `/ceo-office/capabilities` 功能丰富（见 §4），但**不在主导航**，仅经 `analytics` 页「查看授权清单」内联链接 + 旧 `/capabilities` 重定向进入。蓝图将其列为核心建设区（§03「核心建设中」、§04 归入「公司」组），应提升为一级入口。

---

## 2. 红线符合度（蓝图 §10.7）— 基本守住

| 红线 | 结论 | 证据 |
|---|---|---|
| 不复制 Agent Center | ✅ 遵守 | 顶层无 Agent Center；能力资源归入「能力中心」（蓝图要求位置），未主导航化 |
| 不复制彩色 Dashboard | ✅ 强遵守 | `analytics` 页以「公司脉搏六维 + 证据链」呈现；代码注释明确"后端未提供的事实一律显示空态或「—」，不填任何演示数字"；`NO_DATA = "—"` 纪律贯穿 |
| 不复制默认 Full Auto | ✅ 强遵守 | CEO Desk 实现「隔离验证 → CEO 批准/修改/拒绝/回滚」门禁；TaskLauncher 三态门禁（记忆 #12）；高影响动作需 CEO 决策 |

---

## 3. 关键页面交付状态

| 页面 / 路由 | 交付度 | 说明 |
|---|---|---|
| CEO Desk `/ceo-office` | ✅ 强对齐 | 今日简报 / 需 CEO 处理 / 业务版图 / AI 团队运行图（责任关系，非头像墙）/ 候选组织 Simulation / CEO 批准门禁 / 最近验证。规避"指标墙/任务列表首页"反模式 |
| 经营 `/ceo-office/analytics` | ✅ 强对齐 | 公司脉搏 / 经营分析 / 关注·风险·阻塞 / 决策队列 / 异常队列 / 机会雷达(空态) / 公司约束。数据纪律严，缺失即「—」 |
| 能力中心 `/ceo-office/capabilities` | ✅ 功能丰富 / ⚠️ 未进主导航 | 10 类能力（model/agent/skill/tool/workflow/connector/cli/api/webhook/mcp）、注册能力、注册自定义模型·智能体（租户私有）、迁移历史技能、搜索、双轨隔离。**分配闭环部分**由 CEO Desk 的 `CapabilitySupplyReview`（组织级分配 + 批准）承接 |
| Workspace Studio `/ceo-office/workspace/studio` | ✅ 强对齐 | `STUDIO_LIFECYCLE` 8 步（Discover→Blueprint→Compose→Bind→Staff→Simulate→Approve→Operate）映射蓝图 §08 装修流程；RD/XHS/TTK 三模板含阶段/岗位/能力/模拟场景/`externalResultSource`（`PLATFORM_API_OR_CEO_MANUAL` 等），直接对应蓝图 §09 外部结果来源 |
| 业务办公室 `workspace/software·xhs·shortvideo` | △ 需现场验证 | 路由存在、同命名空间；需确认规避"看板/旧任务表/彩色控制台"反模式，呈现"办公室运行/验收/证据" |
| 决策室 `/ceo-office/decisions` | △ 后端缺口 | UI 壳完整（DecisionCard / 状态 pill / 通过·退回·延后·拒绝）；但 `handleDecide` 为**本地占位**，代码注释"后端尚无审批端点，避免伪造任何结果"——决策→Commitment/Owner/DueDate/Evidence→回写 Workspace（蓝图 §10.6）的后端闭环**未接通** |
| 会议工作台 `/ceo-office/meeting` | △ 需验证 | 路由存在；Decision Proposal 闭环需验证 |
| 平台管理后台 `/platform` | △ 超范围 | 蓝图 §13 将 Platform/Admin 列为**阶段五未来商业化**，且 v1（记忆 #1）明确"暂不建设独立 Admin 产品"。代码中含完整 Admin 控制台（部门类型/策略/网关/官方能力目录/用量/审计），UI 解禁有 gate 注释且不在主导航——属超出 v1 范围，需总控确认保留为 gated 代码或剥离 |

---

## 4. 产品完成最低证明 7 条（蓝图 §12）

| # | 证明项 | 状态 | 说明 |
|---|---|---|---|
| 1 | CEO 从空公司创办并理解下一步 | △ | `onboarding` 存在；CEO Desk 门禁"公司尚未建立 → 开始创办公司"到位；创办流闭环需验证 |
| 2 | 添加验证模型/Skill/Tool 并分配 | ✅（部分） | 能力中心添加/验证/注册；分配经组织批准流（CEO Desk CapabilitySupplyReview） |
| 3 | AI 员工承担工作提交结果/证据/成本/失败 | △ | 执行与 runtime 状态存在；"提交结果/证据"在业务办公室的真实回流需现场验证 |
| 4 | 业务办公室查看运行/验收/真实反馈（非内部任务） | △ | 办公室路由存在；反模式规避需验证 |
| 5 | 根据结果调整能力/组织/业务/Workspace | ✅ | 决策室 + 会议 + CEO Desk 组织批准/回滚 |
| 6 | 三业务同一 Company OS | ✅ | `workspace/software·xhs·shortvideo` 同命名空间 |
| 7 | 未接入外部平台有明确人工反馈路径，不演示数据 | ✅ | `analytics` 与蓝图一致显示「—」；记忆 #11 确认 v1 显示「—」/空管道为设计边界 |

---

## 5. 风险与建议（按优先级）

- **R1（高）· 决策闭环后端缺口**：`decisions` 页 `handleDecide` 为占位，蓝图 §10.6 要求的"批准 → 创建 Commitment/Owner/DueDate/Evidence → 回写 Workspace → Assistant 跟进"后端未接通。否则"经营工具/会议决策"组名存实亡。建议补齐 `decideDecision` + Commitment 落库 + 回写。
- **R2（高）· 导航偏离 + 能力中心弱化**：按蓝图 §04 重构 `TerraNavData.js` 为 7 组；将能力中心提升为一级入口；移除「兼容入口」遗留分组；补齐「证据审查」「记忆」两项。
- **R3（中）· Platform/Admin 超范围**：`/platform` 完整 Admin 控制台超出 v1 红线。建议明确注释为 gated（现有 gate 注释已部分做到）或剥离，避免误暴露给单机自用用户。
- **R4（中）· 业务办公室交付验证**：`software/xhs/shortvideo` 需在浏览器实测，确认呈现"办公室运行/验收/证据"而非"看板/旧任务表/彩色控制台"。
- **R5（低）· 记忆入口缺失**：`knowledge/memory` 路由存在但 nav 未露，建议归入「公司资产」组对齐蓝图。

---

## 6. 总结

当前代码在**经营闭环、红线遵守、数据纪律、Studio 装修、双轨能力供给（#94）**上已高度对齐蓝图，是一份可运行的 v1 雏形。主要短板集中在：**① 导航结构偏离蓝图且能力中心被弱化；② 决策→承诺后端闭环未接通；③ Admin 残留超范围**。建议优先处理 R1、R2。

> 本审查以蓝图 v5.0 为结构权威直接产出结论。若需走 AICoding 架构专家团正式交付流程（G0–G6 阶段门），本报告可作为 G1/G2（现状评估）的输入基线。
