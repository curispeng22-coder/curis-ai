# Curis AICoding 架构设计 · 资料摘要

> 本文档做一件事：**精读主理人转交的全部原始资料，逐份、逐章节做出摘要**——后面任何人拿到这份摘要，都能通过章节号快速定位回原始文件的对应位置。

> 上游输入：主理人（齐构成）Phase 1 转交的 A/B/C/D/E 五类原始资料；
> 产出者：`knowledge-ingest-engineer`（知识摄入工程师 - 闻资料），经 G1 校验与人工审核通过后交付。

> **本轮摘要的组织原则**：依据用户在 Phase 0 的关键裁定，全部资料被划分为两组并分开陈列——
> **应然形态（基线）** = A 类 Product Blueprint（结构基线）+ B 类 Frozen UI（UI 基线）；
> **实然形态（现状，非基线）** = C 类 frontend 现有代码。
> 两组事实不做合并、不做裁决，只并列呈现，使差值可见。

---

## 0. 元信息

```yaml
标题: Curis - 资料摘要 v0.1
版本: v0.1
状态: Draft
创建日期: 2026-08-07
整理人: knowledge-ingest-engineer（闻资料）
审核人:
  - 齐构成（主理人 / 结构检查与自动校验）
  - 用户 / CEO（G1 人工审核终审）

阶段: Phase 1 资料摄入
阶段门: G1（资料摘要审核）
工作区根目录: /Users/yy/Documents/Curis AI Workspace

用户诉求原文:
  首句提问: 一个很重要的问题，目前的 app 使用下来，动线非常不流畅各个模块之间有很强烈的割裂感，你的建议？
  Phase0关键裁定: 有个问题，不压参考之前的一些页面，比如任务执行中心、头脑风暴室等等，这些属于上一个规划的旧内容。我发现目前的问题有一个重点就是把现在的架构和过去旧的产品结构混淆在一起了。正确的做法是，以产品蓝图和结构参考，以确定 ui 为 ui 参考，去组合完整的产品形态，旧的页面或者结构可以舍弃，不要被之前旧的前端所干扰

原始资料清单:
  - docs/01_Product/Curis_Product_Blueprint.html: A类结构基线，v4.4 Single Current，产品结构唯一真相源
  - docs/03_Design/Curis_UI_Frozen_Spec_2026-08-04.md: B类UI基线，Frozen 交付规格
  - curis-ui-prototype/_system/canonical-nav.js: B类导航模型唯一真源
  - curis-ui-prototype/ 下 20 个 HTML 原型页: B类UI基线的屏幕级表达
  - frontend/app/ 下 50 个 page.js 路由: C类实然形态，现状非基线
  - frontend/components/terra/TerraNavData.js: C类实然侧栏导航数据
  - 主理人已完成的前端路由审计结果: D类既有输入，本轮已逐条核实
  - .workbuddy/memory/MEMORY.md: E类项目既有约束与红线
```

| 版本 | 日期 | 作者 | 变更内容 |
| --- | --- | --- | --- |
| v0.1 | 2026-08-07 | `knowledge-ingest-engineer` | 初稿。覆盖 A/B/C/D/E 五类资料，逐份逐章节摘要；核实主理人路由审计并提出 3 项修正；记录 16 项资料冲突与 8 项资料缺口。 |

---

## 1. 资料清单

> 列出全部原始资料，每份标注解析状态。解析失败或跳过的必须注明原因。

| 编号 | 文件名 | 类型 | 来源 | 解析状态 | 说明 |
| --- | --- | --- | --- | --- | --- |
| D1 | `docs/01_Product/Curis_Product_Blueprint.html` | html | A类·结构基线（最高权威） | 已解析 | 89KB / v4.4「Single Current」/ Status: Review。147 个标题，17 个一级章节（§00~§16）全部提取为纯文本后逐节精读 |
| D2 | `docs/03_Design/Curis_UI_Frozen_Spec_2026-08-04.md` | md | B类·UI基线 | 已解析 | 15KB / 363 行 / Status: Frozen — ready for developer handoff。§1~§8 全文精读 |
| D3 | `curis-ui-prototype/_system/canonical-nav.js` | js | B类·导航模型唯一真源 | 已解析 | 17KB / 321 行。NAV_MODEL、ICONS、RUNTIME_PAGES、activeOffices、PERSISTENT_HREFS、render 全部逐段精读 |
| D4 | `curis-ui-prototype/*.html`（20 个原型页） | html | B类·UI基线屏幕级表达 | 已解析 | 20 个文件全部解析。逐页提取 title / h1 / page-title 与全部站内 html 跳转，构建出链与入链矩阵 |
| D5 | `frontend/app/**/page.js`（50 个路由） | js | C类·实然形态（非基线） | 已解析 | 50 个 page.js 全部枚举（37 静态 + 13 动态）。对 102 个源文件做全量内部链接扫描以判定可达性 |
| D6 | `frontend/components/terra/TerraNavData.js` | js | C类·实然侧栏导航数据 | 已解析 | 207 行。GROUPS / ORDER / PERSISTENT_LABELS / findActiveNav 全部精读；其「已对齐 canonical-nav.js」声称已逐项核实 |
| D7 | 主理人前端路由审计结果 | 结构化文本 | D类·既有输入 | 已解析并核实 | 由主理人在任务书中直接给出。本轮未重复劳动，仅做独立复核，得出 3 项修正（见 D7 摘要与 X12/X13/X14） |
| D8 | `.workbuddy/memory/MEMORY.md` | md | E类·项目既有约束 | 已解析 | 85 行 / 13 节。重点精读 §3、§4、§8、§9、§10 |
| D9 | `docs/01_Product/Blueprint_vs_UI_Diff_2026-08-06.md` | md | 本轮扫描中发现 | 已发现 · 未纳入摘要 | 8KB。**非主理人指派资料**，且性质为「诊断分析产物」而非原始资料。为避免把下游判断提前引入本摘要，本轮仅登记存在性，不摘录其结论。是否纳入请主理人裁定 |
| D10 | `docs/03_Design/Curis_Design_System.md` §3.1 | md | 本轮核实中发现 | 部分解析（仅 §3.1） | 14KB。**非主理人指派资料**。因 D3 文件头第 4 行自称「规范来源：本文件 §3.1」，为核实该来源声称的真伪，本轮定向解析了 §3.1（第 67~81 行），未解析其余章节 |

**本轮实际资料类型**：`html` / `md` / `js` / 结构化文本。
**未出现的类型**：`docx` / `pdf` / `pptx` / `xlsx` —— 本轮无此四类资料，故附录 B 所列四项解析 Skill 本轮均未调用，改由直接文本提取与结构化脚本扫描完成解析。

**解析失败或跳过的资料**：无解析失败项。D9 为主动跳过（原因见上表说明列），D10 为主动限定范围解析（原因见上表说明列）。

---

## 2. 资料内容摘要

> 逐份文档按自身章节结构做摘要。每条摘要标注章节号（`D编号，§章节`），后面任何人想核实某个点，直接定位回原文对应位置即可。

### D1：`docs/01_Product/Curis_Product_Blueprint.html`

> Curis 产品结构的唯一真相源，定义「应然产品形态」的结构基线 —— 来源：A类·最高权威。Status: Review（**注意：尚未 Frozen**）

| 章节 | 内容摘要 | 出处 |
| --- | --- | --- |
| 首屏 · 产品定位 | Curis 是面向一人公司创业者的 AI 公司经营系统。帮助一位真实 CEO 从零创建公司，由 AI 员工承担责任、执行业务、提供证据，并根据真实世界结果持续经营 | D1，§首屏 |
| 首屏 · 产品真相 | 一个 CEO、多个 AI 员工、任意业务、逐步成长的公司运行系统。**任务、会议和知识都是运行机制，不是产品本体** | D1，§首屏产品真相 |
| 首屏 · 当前边界 | 本机 Desktop 验证阶段把未来 Platform/Admin 逻辑收在一起；暂不做计费、市场、多租户和多真实员工协作 | D1，§首屏当前边界 |
| §00 体验基础 | 第一次打开不能看到空 Dashboard，也不能先看到表单。CEO 进入的是一间尚未布置完成、但已有人等待他的 CEO 办公室 | D1，§00 |
| §00 空白但不空旷 | 没有业务时不展示假数据或空列表；保留公司空间、Assistant 位置、创建提示和第一步行动，让空白代表「尚未建立」而非「什么都没有」 | D1，§00 空白但不空旷 |
| §00 首次进入状态机 | 四态：未建立 / 意图已表达 / 公司已生成 / 第一间办公室准备中。每态定义 CEO 看到什么、Assistant 做什么、下一步 | D1，§00 首次进入的状态机 |
| §00 引导五步 | 表达意图 → 出现公司牌匾 → 建立 CEO 办公室 → 铺开业务版图 → 点亮第一间办公室（进入 Workspace Studio） | D1，§00 引导如何逐步把空间建起来 |
| §01 Curis 是什么 | 围绕公司生命周期运行的经营系统：CEO 意图 → 公司设计 → 业务方向 → AI workforce 与能力 → Cycle/Workspace → 真实世界结果 → 证据与验收 → CEO 决策 → 公司调整与扩展 | D1，§01 |
| §01 Curis 不是什么 | 明确否定六项：Task Manager、Workflow Platform、Agent Collection、**BI Dashboard**、CRM/ERP、Generic Chat。不以任务量、AI 调用量、文档数量或页面完整度证明价值 | D1，§01 Curis 不是什么 |
| §01 产品层次 | 当前为一个 Local Desktop 把两个逻辑层收在一起：Platform/Admin 逻辑层（能力·业务模式·版本·未来租户·未来计费）+ Company Runtime（CEO·业务·AI员工·能力·Workspace·证据） | D1，§01 产品层次 |
| §01 Current fact | Blueprint 定义目标产品，**不代表当前代码已经完成**。当前交付仍是 Local Desktop、单 Owner、Project/Task-first 基线 | D1，§01 Current fact |
| §02 CEO 生命周期 | 八阶段：创建 Intent → 设计 Company Design → 选择方向 → 供给 AI/Capability → 运行 Cycle/Workspace → 验证 Evidence → 决策 Continue/Change → 扩展 Reconfigure | D1，§02 |
| §02 阶段表 | 五行：创建中 / 设计中 / 首次验证 / 持续运行 / 扩展重构，每行给出 CEO 动作、系统显示、退出条件 | D1，§02 阶段表 |
| §03 两条经营循环 | **导航是投影，经营循环才是产品核心**。价值循环（市场信号→业务赌注→外部承诺→交付验收→价值学习）与公司循环（公司意图→责任分配→能力容量→委派执行→组织调整）在 Outcome 与 Decision 处相交 | D1，§03 |
| §04 核心对象 | 七类对象：Company / Business Bet / Outcome / Responsibility·Actor / Capability·Capacity / Workspace·Cycle / Evidence·Decision。**对象不是页面** | D1，§04 |
| §04 不变量 | 没有结果不能建立正式业务；没有责任不能启动 Cycle；没有能力和资源不能承诺交付；没有证据不能标记 Verified；高影响变化必须经过影响分析、模拟和 CEO 批准 | D1，§04 不变量 |
| §05 承诺网络 | Promise/Obligation → Commitment → Work Package → Task → Evidence → Acceptance。**Task 只是内部动作** | D1，§05 承诺网络 |
| §05 外部系统 | 软件开发场景由 GitHub/CI/云平台产生原始事实；内容增长场景由抖音/小红书产生数据。API 不可用时 CEO 手动验收录入。Curis 拥有经营事实、承诺、决策和解释，外部系统保有原始事实 | D1，§05 外部系统与结果证据 |
| §05 业务阶段 | 四阶段：Opportunity / Experiment / Operating / Scaling·Exit | D1，§05 业务阶段 |
| §06 AI 员工责任契约 | 五项契约：结果 / 范围 / 能力 / 动作 / 证据，每项定义必须明确什么与越界如何处理 | D1，§06 AI 员工责任契约 |
| §06 部门如何出现 | **部门不是先验组织树**，而是一组稳定责任、共享能力和服务承诺的聚合。只有当重复性责任、多人多AI协作、共享容量或连续性被证明后，才创建部门 | D1，§06 部门如何出现 |
| §07 何时需要 Workspace | 需要：多个 AI 员工持续协作、业务有重复周期、需要独立能力数据权限、需要独立异常验收复盘。不需要：CEO 与单个 AI 协作、一次性验证、依赖少 | D1，§07 |
| §07 Workspace Runtime | 七步：Request → Blueprint → Resource Check → Simulation → Approve → Operate → Close/Learn | D1，§07 Workspace Runtime |
| §07 Cycle 内部运行 | Outcome → Commitment → Work Package → Task/AI Action → Evidence → Acceptance → Closure。**Project、Task、Workflow、Artifact 只在 Workspace 内部作为实现手段出现，不能取代 Outcome/Commitment/Evidence/Acceptance** | D1，§07 Cycle 内部运行 |
| §08 Truth Layer | Fact / Evidence / Claim / Assumption / Unknown / Conflict / Learning。**知识是证据、决议和学习的投影，不是另一个内容仓库** | D1，§08 Truth Layer |
| §08 Decision Packet | 当前状态 → 为什么重要 → 证据与未知 → 可选方案 → 资源承诺影响 → 推荐方案 → CEO 决定 → 生效条件 → 验证与回滚 | D1，§08 Decision Packet |
| §08 真实状态 | Unknown、Stale、Conflict 不能被自动渲染为正常；决策可以过期并要求重新验证 | D1，§08 真实状态 |
| §09 四个入口 | **「四个入口是同一经营系统的投影」**：经营 / 业务 / AI 团队 / 工作空间。每个入口给出 CEO 的问题、真实公司职责、输入输出、为什么不是别的设计 | D1，§09 |
| §09 跨切机制 | 「建设」是状态模式；**Meeting、Knowledge、Assistant 和 Analysis 是跨切机制**（原文表述为四个入口之外的跨切项） | D1，§09 首段 |
| §09 默认首页 | 由公司状态决定：公司为空→Founding Brief；配置中→Company Design；业务运行→Company Now；重构中→Change Mode | D1，§09 默认首页由公司状态决定 |
| §09 经营事项 | 经营首页只呈现三类事项投影：Decision、Exception、Opportunity。Assistant **不建立第二个任务系统，不静默改变公司状态，不占用固定第三栏** | D1，§09 经营事项与 Assistant |
| §10 Operating Day 对象 | 五字段：Day State / Morning Brief / Matters / Handoffs / Closeout，各自定义产品含义与关闭标准 | D1，§10 CEO Operating Day 的运行对象 |
| §10 一日运行剧本 | 七时点：08:30 Brief → 09:00 Ask → 10:30 Build → 14:00 Meet → 17:00 Signal → 18:00 Decide → 18:30 Close | D1，§10 一日运行剧本 |
| §10 Assistant 责任契约 | 五角色：Chief of Staff / Concierge / Coordinator / Decision Partner / Watchdog·Memory，各有主动行为、交付物与边界 | D1，§10 Assistant 的责任契约 |
| §10 CEO Desk 六组成 | 1 Brief Header / 2 Assistant Brief / 3 Matters / 4 Operating Timeline / 5 Company Pulse / 6 Handoffs & Closeout | D1，§10 CEO Desk 的 UI 组成 |
| §10 UI 原则 | 左侧保留紧凑的 CEO Desk/经营/业务/AI团队/工作空间导航；主区域全宽。**导航按公司、经营工具、办公室、公司资源分组，办公室由已配置业务空间生成**。Assistant 不做固定第三栏 | D1，§10 UI 原则 |
| §11 Assistant Runtime | 每个 Company 有且只有一个 CEO Assistant。六态生命周期：Created → Configured → Learning Context → Operating → Evaluating → Upgraded·Reassigned | D1，§11 |
| §11 上下文三层 | 稳定层（Charter/权限/偏好/红线）、经营层（业务组合/Outcome/承诺/容量）、当日层（Brief/Matters/交接/Closeout） | D1，§11 Assistant 的上下文层 |
| §12 AI 组织四层 | CEO 治理 → Assistant 协调 → 专业 AI 负责结果 → Workspace AI 执行。**AI 组织关系是「汇报与授权图」，不是通讯录** | D1，§12 |
| §13 Workspace 两模式 | Studio 装修模式（Business Engineering 使用，产出 Blueprint Draft，未批准不影响生产）与 Runtime 经营模式（CEO 与 AI 团队使用，运行中不能被 Studio 静默改写） | D1，§13 Workspace 的两种模式 |
| §13 装修生命周期 | 八步：Discover → Blueprint → Compose → Bind → Staff → Simulate → Approve → Operate | D1，§13 装修与交付生命周期 |
| §13 Studio 五区域 | 业务结构栏 / Blueprint Canvas / 配置检查 / 版本与影响 / 模拟台。模拟台需验证六类场景：正常、Agent缺席、工具失败、外部结果延迟、证据冲突、CEO拒绝 | D1，§13 Workspace Studio 的实际屏幕 |
| §14 视觉总判断 | Desktop First 的 CEO 工作台，Calm Executive Workspace 视觉语言。**不是 KPI 墙、彩色 Dashboard 或聊天应用**。左侧固定公司导航，中间全宽经营内容。主题只提供系统、浅色、深色三种。真实用户界面统一使用简体中文 | D1，§14 视觉总判断 |
| §14.1 全局壳层 | 220px 左侧导航 + 主区域全宽。左侧导航固定内容为「公司（CEO Desk、经营、业务、AI 团队、工作空间）、经营工具、办公室、公司资源；底部设置与帮助」。**禁止做法：不把 Meeting、Knowledge、Task、Agent 单独升为一级中心；不把 Assistant 放进侧栏** | D1，§14.1 |
| §14.2 从零开始七步 | Welcome → Founding Brief → Company Design → First Business → AI Team → Launch Check → CEO Desk。每步定义出现时机、页面长什么样、CEO 交互、完成后去哪里 | D1，§14.2 |
| §14.4 五个一级页面 | CEO Desk·Operating Day / 经营 / 业务 / **公司** / 工作空间。每页给出首屏回答的问题、页面组成、核心动作 | D1，§14.4 |
| §14.5 CEO Desk 布局 | 上半屏左 Assistant Brief、上半屏右 Company Pulse（六维状态点）、下半屏左 Matters（Decision红/Exception琥珀/Opportunity蓝三类边线）、下半屏右 Timeline·Handoffs | D1，§14.5 |
| §14.9 Workspace 页 | Workspace 目录**按业务目标排列，不按项目文件夹排列**；运行台顶部固定 Outcome/承诺/验收标准，底部固定 Evidence/Acceptance/Insight/Close Cycle。**Project/Task 只在内部执行区出现** | D1，§14.9 |
| §14.10 四种上下文模式 | Decision Room / Meeting Workbench / Evidence Review / Change Mode，各自定义进入方式、屏幕结构、离开方式 | D1，§14.10 |
| §14.12 必须设计的状态 | Empty / Attention / Blocked / Conflict·Stale 四态必须设计，不能只设计成功页面 | D1，§14.12 |
| §14.13 完整页面路径 | 首次打开 → Welcome/Founding Brief → Company Design → First Business → AI Team & Capability → Launch Check → CEO Desk（每天默认入口）→ 经营/业务/公司/Workspace → Decision Room·Meeting·Evidence Review（按需）→ 回到 CEO Desk | D1，§14.13 |
| §14 设计验收标准 | 设计稿必须能让一个第一次使用的 CEO 在没有产品经理口头解释的情况下走通完整路径。**如果只能看到漂亮页面，却无法走通这条路径，UI 仍未完成** | D1，§14 设计验收标准 |
| §15 第一条真实业务 | Curis 用自己的软件研发业务开发和完善 Curis（dogfood）。最小 AI workforce 四类：产品与业务 AI、软件工程 AI、质量验证 AI、运行与反馈 AI | D1，§15 |
| §15 北极星 | Time to First Verified Product Outcome —— 从 CEO 意图到第一个被真实使用、被证据验证的软件结果的时间 | D1，§15 北极星 |
| §16 当前阶段保留 | 六项：Local Desktop 单 CEO / 从零创建任意业务 / Cycle·Workspace 运行与外部结果反馈 / API 或 CEO 手动 Evidence / Curis 自我研发业务 / 失败·未知·决策与学习闭环 | D1，§16 当前单机验证阶段保留 |
| §16 明确暂不建设 | 五项：独立 Admin 产品和物理多租户 / 计费·订阅·模板商城 / 多真实员工协作 / 完整 CRM·ERP 和深度平台集成 / **不以 Project、Task、Meeting、Knowledge 作为产品根** | D1，§16 明确暂不建设 |
| §16 v1 已确认业务空间 | **CEO 可从零创建的业务空间类型当前确认为三类——软件研发 software、小红书运营 xhs、抖音·TikTok 运营 shortvideo**。它们即 §10 所述「已配置业务空间」，是导航「办公室」分组下生成的入口。**UI 原型 curis-ui-prototype（Frozen）是本 Blueprint 在 v1 的权威 UI 表达；凡 UI/IA 与原型不一致处，以原型为准修订本文件** | D1，§16 v1 已确认业务空间 |
| §16 固定工作顺序 | Product Truth → Business Runtime → UI Design → Code | D1，§16 固定工作顺序 |
| §16 冻结前门禁 | 五场景验证表。当前状态：「从零创建 Curis 公司」为 Blueprint Review，其余四项（软件研发业务 / AI员工失败越权 / 外部结果不可直接获取 / 业务暂停关闭）**均为 Simulation Pending** | D1，§16 冻结前的 Runtime Simulation 门禁 |
| §16 实现门禁 | 本文件状态为 Review。未完成产品审阅、Business Runtime Simulation 和明确 Issue 之前，不得以页面、接口、数据表或局部代码宣称目标产品已完成 | D1，§16 实现门禁 |

### D2：`docs/03_Design/Curis_UI_Frozen_Spec_2026-08-04.md`

> UI 基线的视觉与交互权威规格，Status: Frozen — ready for developer handoff —— 来源：B类·UI Designer

| 章节 | 内容摘要 | 出处 |
| --- | --- | --- |
| §1 交付物清单 | 七项交付物：冻结设计令牌 `_system/tokens.css`、HTML 高保真 `curis-ui-prototype/*.html`、Dev Mode 标注、组件规格文档、页面规格、无障碍基线、验收脚本 | D2，§1 |
| §2.1 颜色令牌 | 13 个颜色令牌，浅色深色双值。含 `--ui-bg` `--ui-surface` `--ui-line` `--ui-text` `--ui-accent`（浅色 #1a1c1f / 深色 #32f08c）`--ui-success` `--ui-warning` `--ui-danger` | D2，§2.1 |
| §2.2 字号 | **唯一真源，7 档**：12/13/14/16/20/24/28 px，对应 `--ui-fs-1` 至 `--ui-fs-7` | D2，§2.2 |
| §2.3 间距 | 8 档：4/8/12/16/20/24/32/48 px，对应 `--ui-sp-1` 至 `--ui-sp-8` | D2，§2.3 |
| §2.4 圆角 | 5 档：4/8/12/16/999 px，对应 `--ui-r-xs/sm/md/lg/pill` | D2，§2.4 |
| §2.5 动效 | 三档时长 120/200/320ms，三条缓动曲线（standard/decel/accel） | D2，§2.5 |
| §2.6 层级 | 七级 z-index：base 0 / sticky 100 / dropdown 200 / drawer 300 / modal 400 / toast 500 / devmode 9000 | D2，§2.6 |
| §2.7 控件高度与焦点 | 控件高度 32/36/40px；最小命中边长 `--ui-tap-min` 32px；焦点环宽 2px 偏移 2px | D2，§2.7 |
| §3.1 Global Topbar | 固定 100% 宽 × **52px 高**，固定顶部。左侧面包屑或页面标题，右侧状态提示、主题切换、全局操作 | D2，§3.1 |
| §3.2 Global Sidebar | **220px × 100vh 桌面端固定**。分组为「公司 / 经营工具 / 办公室 / 公司资源 / 底部帮助」。激活态为左侧 3px 强调线加背景 | D2，§3.2 |
| §3.3 Button 体系 | 四变体：Primary（32/40px）/ Secondary（32px）/ Ghost（36px）/ Icon（32×32）。五状态含 focus-visible 与 disabled | D2，§3.3 |
| §3.5 Drawer | 宽 420px 桌面 / 100% 移动，右侧固定滑入，遮罩 rgba(0,0,0,0.45)，底部操作区左取消右保存 | D2，§3.5 |
| §3.7 能力切换器 | 数据来源 `localStorage['curis-capabilities']`；空态隐藏下拉并显示「＋ 配置能力」跳转 `ai-organization.html`；按页独立记忆 `curis-runtime-cap:` 前缀 | D2，§3.7 |
| §3.8 Empty state | 文案说明「**尚未建立**」而非「没有数据」；给出明确下一步入口；不使用大面积彩色插画 | D2，§3.8 |
| §4 页面规格 | 标题声明为「18 页」，但表格实际覆盖 20 个页面文件（`workspace-runtime-*.html` 一行代表 4 个文件）。逐页给出职责、入口、关键数据契约 | D2，§4 |
| §4 入口标注 | `index` 入口重定向；`founding-flow` 首次进入；`ceo-desk`/`operating`/`business`/`ai-organization`/`workspace-portal` 为主导航；`decision-room`/`meeting` 为侧栏工具；`assets`/`knowledge`/`finance`/`calendar` 为侧栏资源；`workspace-shell-reference`/`workspace-studio`/`ceo-day-demo` 标注入口为「导航」 | D2，§4 页面规格表 |
| §4 通用约束 | **所有页面使用 `canonical-nav.js` 渲染侧栏，禁止页面内联第二套导航**；顶栏固定 52px；每页接入 `tokens.css` 与 `shell.css` | D2，§4 通用约束 |
| §5 Dev Mode | `?dev=1` 或 `Shift+D` 开启，`Shift+Esc` 强制关闭。悬停显示类型、尺寸、字号、圆角、文字色、背景色、padding、margin、组件规格九个字段 | D2，§5 |
| §6 无障碍 | WCAG 2.1 AA 八项逐项对照，全部标记为已满足。触达目标以 32px 为桌面端下限；`prefers-reduced-motion` 已全局设置 | D2，§6 |
| §7 验收 Checklist | 十项，其中首项「tokens.css 已包含全部令牌」同时存在未勾选与已勾选两行（疑似重复行）。其余九项均已勾选 | D2，§7 |
| §8 已收敛与剩余项 | 已收敛六项（令牌补齐、触达目标从 124 处降到 2 处、圆角 13 档收敛到 4 档、间距 18 档收敛到 6 档共收敛 1741 条声明、Dev Mode、表单无障碍）。**剩余收敛项：暂无** | D2，§8 |
| §8 验收运行结果 | 2026-08-05 实测：字号 7 档；圆角 4 档；触达不足 32px 者 2 处（已豁免标注）；console 错误 0；能力闭环验证 24/24 PASS | D2，§8 验收运行结果 |

### D3：`curis-ui-prototype/_system/canonical-nav.js`

> 全站唯一导航真源，零依赖 IIFE，通过 `aside.dataset.curisCanonicalNav` 保证幂等 —— 来源：B类·导航模型权威

| 章节（代码区段） | 内容摘要 | 出处 |
| --- | --- | --- |
| §文件头注释（L1-21） | 自称「规范来源：`docs/03_Design/Curis_Design_System.md` §3.1 Navigation hierarchy」。设计约束三条：全站只允许这一个渲染器改写侧栏导航区域（历史上曾有两套竞争渲染器导致 3 种导航签名，已移除）；**办公室分组可见性只由公司运行状态决定，与当前处在哪一页无关**；本模块零依赖 | D3，§文件头 L1-21 |
| §NAV_MODEL（L28-56） | 冻结导航模型五组：**primary 5 项**（CEO 工作台 ceo-desk / 经营 operating / 业务 business / AI 团队 ai-organization / 工作空间 workspace-portal）；**tools 2 项**（会议工作台 meeting / 决策室 decision-room）；**offices 4 项**（研发 software / 小红书 xhs / 抖音·TikTok shortvideo / 部门 department）；**resources 4 项**（成果库 assets / 知识库 knowledge / 财务 finance / 日历 calendar）；**footer 2 项**（设置 / 帮助与反馈，href 均为 `#`） | D3，§NAV_MODEL L28-56 |
| §ICONS（L58-83） | 统一图标系统，内联 SVG 线性图标，stroke=currentColor，viewBox 24×24，线宽 1.75，自动跟随文字色与明暗主题 | D3，§ICONS L58-83 |
| §RUNTIME_PAGES（L87-94） | 六个页面归属同一 Workspace 运行入口，在导航里由「工作空间」一项代表：software / xhs / shortvideo / department / **workspace-studio** / **workspace-shell-reference**。即后两者无独立导航项 | D3，§RUNTIME_PAGES L87-94 |
| §activeOffices（L109-129） | 办公室按公司状态**动态过滤**：需 `state.companyCreatedAt` 存在；software 由业务名匹配「软件·Curis·研发」或 softwareAcceptance 或日历事件触发；xhs 由「小红书」触发；shortvideo 由「抖音·TikTok·短视频」触发；**department 单独由 `state.departmentStatus === 'active'` 触发** | D3，§activeOffices L109-129 |
| §badgeFor（L132-146） | 角标只反映需 CEO 处理的事项数量。CEO 工作台角标为 queued/waiting_ceo/acknowledged/failed 事件数加待处理连接器；工作空间角标为激活办公室数（排除部门办公室）且大于 1 才显示 | D3，§badgeFor L132-146 |
| §activeKind（L152-158） | 高亮分两级：exact（当前页在导航有精确入口，承担唯一 aria-current="page"）与 ancestor（Workspace 运行页由「工作空间」代表，视觉高亮但不重复声明 aria-current，避免违反 WCAG 4.1.2） | D3，§activeKind L152-158 |
| §render 清理逻辑（L220-225） | 渲染前清除一切历史导航残留，移除选择器覆盖 `.nav-section .nav-list .nav-group .nav .nav-footer .sidebar-footer .nav-label .sidebar-foot .assistant-mini .curis-nav-section .curis-canonical-sidebar-main .fzn-nav .fzn-footer .fzn-group .fzn-item` | D3，§render L220-225 |
| §PERSISTENT_HREFS（L232-244） | **P2-2 修订：4 常驻 + 「更多」抽屉**。常驻 4 项为 ceo-desk / operating / business / workspace-portal。折叠区全集为「AI 团队 + tools + resources + offices」。抽屉**默认始终收起**，不按当前页自动展开 | D3，§PERSISTENT_HREFS L232-244 |
| §当前栏目内联（L251-254） | 身处折叠区页面时，把当前页作为单个高亮项内联在常驻区下方（分组标题「当前栏目」），满足 WCAG 2.4.3 当前位置可见，同时让默认视图稳定为 4 加 1 加「更多」 | D3，§render L251-254 |
| §更多抽屉（L256-278） | toggle 按钮 aria-expanded 初始 false，aria-label「展开次要导航」。panel 内依次为「AI 团队」「经营工具」「公司资源」，办公室分组仅当 offices 非空时追加 | D3，§render L256-278 |
| §footer（L281-298） | **P2-5：设置与帮助不再是无动作死链接，改为点击打开 CEO 助理**（触发 `#assistant-fab` 的 click）。即原型中不存在独立的设置页与帮助页 | D3，§render L281-298 |
| §devmode 自动注入（L306-314） | Dev Mode 标注层作为 Frozen 交付物之一自动注入所有页面，仅当 `?dev=1` 或 Shift+D 才激活 | D3，§loadDevMode L306-314 |
| §导出（L304） | 对外暴露 `window.CurisCanonicalNav = { MODEL, render, readState }` | D3，§L304 |

### D4：`curis-ui-prototype/*.html`（20 个原型页）

> UI 基线的屏幕级表达。下表逐页记录职责、导航位置与跳转关系。**出链** = 从这一页能去哪；**入链** = 从哪能来这一页（均限原型内部 html 跳转） —— 来源：B类·Frozen 高保真交付稿

| 页面 | 职责（取自 title / h1） | 在 canonical-nav 中的位置 | 出链数 | 入链数 | 出处 |
| --- | --- | --- | --- | --- | --- |
| `index.html` | Curis 入口重定向（0.9KB，最小页） | 不在 NAV_MODEL（URL 根入口） | 2（ceo-desk、founding-flow） | 0（根入口，符合预期） | D4，§index.html |
| `founding-flow.html` | 创建公司 · Curis Founding Flow | **不在 NAV_MODEL** | 6 | 1（仅 index.html） | D4，§founding-flow.html |
| `ceo-desk.html` | 今日经营 · CEO 工作台 | primary 第 1 项 · **常驻** | 13 | 18（全站最高） | D4，§ceo-desk.html |
| `operating.html` | 经营（86KB，全站最大页） | primary 第 2 项 · **常驻** | 13 | 17 | D4，§operating.html |
| `business.html` | 业务 | primary 第 3 项 · **常驻** | 5 | 17 | D4，§business.html |
| `ai-organization.html` | AI 团队办公室 | primary 第 4 项 · **折叠进「更多」** | 9 | 17 | D4，§ai-organization.html |
| `workspace-portal.html` | 工作空间 | primary 第 5 项 · **常驻** | 9（含 software、xhs、shortvideo、studio；**不含 department**） | 17 | D4，§workspace-portal.html |
| `meeting.html` | 会议工作台 · 外部合作方周会 | tools 第 1 项 · 折叠 | 13 | 12 | D4，§meeting.html |
| `decision-room.html` | 待决策事项 · 决策室 | tools 第 2 项 · 折叠 | 13 | 17 | D4，§decision-room.html |
| `assets.html` | 成果库（5.9KB） | resources 第 1 项 · 折叠 | 13 | 13 | D4，§assets.html |
| `knowledge.html` | 知识库 | resources 第 2 项 · 折叠 | 13 | 13 | D4，§knowledge.html |
| `finance.html` | 财务与经营 | resources 第 3 项 · 折叠 | 13 | 13 | D4，§finance.html |
| `calendar.html` | 公司日历 | resources 第 4 项 · 折叠 | 13 | 13 | D4，§calendar.html |
| `workspace-runtime-software.html` | 研发办公室 · 工作空间 Shell | offices 第 1 项 · **动态生成** | 14 | 13 | D4，§workspace-runtime-software.html |
| `workspace-runtime-xhs.html` | 小红书运营办公室 | offices 第 2 项 · 动态生成 | 14 | 13 | D4，§workspace-runtime-xhs.html |
| `workspace-runtime-shortvideo.html` | 抖音 / TikTok 运营办公室 | offices 第 3 项 · 动态生成 | 14 | 14 | D4，§workspace-runtime-shortvideo.html |
| `workspace-runtime-department.html` | 部门办公室 · 内容增长部 | offices 第 4 项 · 仅 departmentStatus 为 active 时出现 | 15（全站最高） | **0（原型内零入链）** | D4，§workspace-runtime-department.html |
| `workspace-studio.html` | 工作空间搭建方案 | **不在 NAV_MODEL**，属 RUNTIME_PAGES | 7 | 5（portal 与 4 个 runtime 页） | D4，§workspace-studio.html |
| `workspace-shell-reference.html` | 示例工作空间 · 工作空间 Shell 参考 | **不在 NAV_MODEL**，属 RUNTIME_PAGES | 14 | **0（原型内零入链）** | D4，§workspace-shell-reference.html |
| `ceo-day-demo.html` | Curis · CEO 的一天（真实 API 接入演示） | **不在 NAV_MODEL** | **0** | **0（零入零出，完全孤立）** | D4，§ceo-day-demo.html |

**D4 派生事实（由上表统计得出）**：
- 原型页总数 **20 个**（D4，§目录清单）。
- 出现在 `NAV_MODEL` 中的原型页 **15 个**（primary 5 + tools 2 + resources 4 + offices 4）；**不在 NAV_MODEL 的 5 个**：`index` `founding-flow` `workspace-studio` `workspace-shell-reference` `ceo-day-demo`（D4，§NAV 覆盖统计）。
- 原型内零入链页 **4 个**：`index`（根入口，预期内）、`workspace-runtime-department`、`workspace-shell-reference`、`ceo-day-demo`（D4，§入链统计）。
- `workspace-portal.html` 的出链包含 software、xhs、shortvideo、studio，**不包含 department**（D4，§workspace-portal.html 出链）。
- 侧栏由 `canonical-nav.js` 统一渲染，因此除 index 外各页的大量出链主要来自统一侧栏，页面主体的业务级跳转需另行核验（D4，§出链性质说明）。

### D5：`frontend/app/**/page.js`（50 个路由）

> C类实然形态，**非基线**，仅作对照。共 50 个 `page.js`：37 个静态路由 + 13 个动态路由 —— 来源：C类·现有前端代码

| 章节（路由分组） | 内容摘要 | 出处 |
| --- | --- | --- |
| §根与认证（4） | `/`（805 行以上的大型控制台页，引用 platform）、`/login`（88 行，本地 Owner 认证）、`/onboarding`（创建公司/部门/项目）、`/guide`（327 行，业务工作台引导 Workbench Guide 向导） | D5，§根与认证 |
| §CEO 工作台主干（5） | `/ceo-office`、`/ceo-office/analytics`（805 行，页内标题「经营」，注释自述严格对齐原型 `operating.html`）、`/ceo-office/projects`（393 行，页内标题「业务」，注释自述严格对齐原型 `business.html`）、`/ceo-office/organization`、`/ceo-office/workspace` | D5，§CEO 工作台主干 |
| §工作空间子页（5） | `/ceo-office/workspace/software`、`/xhs`、`/shortvideo`、`/department`、`/department/[id]` | D5，§工作空间子页 |
| §经营工具（2） | `/ceo-office/meeting`、`/ceo-office/decisions` | D5，§经营工具 |
| §公司资源（4） | `/ceo-office/company-runtime`（98 行，**页内标题为「成果库」**）、`/ceo-office/knowledge`、`/ceo-office/finance`、`/ceo-office/calendar` | D5，§公司资源 |
| §设置与帮助（2） | `/ceo-office/settings`、`/ceo-office/help` | D5，§设置与帮助 |
| §旧规划残留页（5） | `/ceo-office/execution`（156 行，标题「执行工作台」，副标题「聚合真实项目任务与执行状态」）、`/ceo-office/brainstorm`（145 行，标题「头脑风暴室」）、`/ceo-office/strategy-room`（257 行，标题「AI 会议室 / 战略会议室」）、`/ceo-office/reports`（204 行，标题「重要汇报」「汇报收件箱」）、`/ceo-office/runtime-trace`（115 行，标题「运行轨迹」，自注 Frozen B1 Secondary） | D5，§旧规划残留页 |
| §能力与记忆（3） | `/ceo-office/capabilities`（504 行，标题「能力中心」，副标题「AI 员工可使用的十类能力资源」）、`/ceo-office/capabilities/[type]/[id]`、`/ceo-office/knowledge/memory`（402 行，标题「记忆管理」） | D5，§能力与记忆 |
| §旧路由重定向垫片（4） | `/capabilities`、`/employees`、`/projects`、`/org-center` —— **均为 6 行文件，仅含 `redirect()` 调用**，注释统一为「旧暗色…页 → 重定向到新 Terra 浅色…」 | D5，§旧路由重定向垫片 |
| §org-center 子页（2） | `/org-center/dept/[deptId]`、`/org-center/emp/[empId]` —— 父级 `/org-center` 已是重定向垫片 | D5，§org-center 子页 |
| §Platform 层（3） | `/platform`（GatewayPanel、CapabilityCatalogPanel、AuditEventPanel、UsageProjectionPanel）、`/platform/commercial`、`/platform/results` | D5，§Platform 层 |
| §Control 层（1） | `/control/secret-vault` | D5，§Control 层 |
| §动态详情页（13） | `/ceo-office/brainstorm/sessions/[id]`、`/ceo-office/capabilities/[type]/[id]`、`/ceo-office/execution/runs/[id]`、`/ceo-office/execution/tasks/[id]`、`/ceo-office/knowledge/entries/[id]`、`/ceo-office/organization/departments/[id]`、`/ceo-office/organization/employees/[id]`、`/ceo-office/projects/[id]`、`/ceo-office/reports/[id]`、`/ceo-office/workspace/department/[id]`、`/org-center/dept/[deptId]`、`/org-center/emp/[empId]`、`/projects/[project_id]` | D5，§动态详情页 |
| §前端缺失的原型对应页 | 前端**不存在** `assets` / `founding-flow` / `workspace-studio` / `workspace-shell-reference` / `ceo-day-demo` 对应路由（已用目录查找确认为空） | D5，§缺失路由核查 |
| §全局助理挂载 | `components/assistant/GlobalAssistant.js` 通过 `app/layout.js` 第 36 行的 `GlobalAssistantProvider` 全局挂载；其内含 `WORKSPACE_PREFIXES` 数组（`/ceo-office` `/projects` `/employees` `/capabilities` `/org-center`），**该数组是路径前缀匹配用的字符串常量，不是可点击导航链接** | D5，§GlobalAssistant.js L29-40 |

### D6：`frontend/components/terra/TerraNavData.js`

> C类实然侧栏导航数据。文件头声称「v2 强制对齐 canonical-nav.js 唯一真源」，本轮已逐项核实该声称 —— 来源：C类·现有前端代码

| 章节（代码区段） | 内容摘要 | 出处 |
| --- | --- | --- |
| §文件头声称（L1-17） | 声称「全站唯一导航分组数据源（Frozen IA 对齐，4 组 + offices 二级）」「2026-08-06 · v2 强制对齐 canonical-nav.js 唯一真源」「任何不在原型里的历史自创栏目（如原 v1 的 CEO 协调型子项、**头脑风暴室**、**执行工作台**、**能力中心**等）一律不进入导航，保持与原型 100% 一致」 | D6，§文件头 L1-17 |
| §文件头对办公室的定性（L15-17） | 声称办公室 4 项「均为 v1 占位页（**Blueprint §16 明确暂不建设**），业务启动后可激活」 | D6，§文件头 L15-17 |
| §GROUPS 公司组（L21-61） | 5 项：CEO 工作台 `/ceo-office`、经营 `/ceo-office/analytics`、业务 `/ceo-office/projects`、AI 团队 `/ceo-office/organization`、工作空间 `/ceo-office/workspace`。**工作空间带 4 个静态 subs**：software / xhs / shortvideo / department | D6，§GROUPS 公司组 L21-61 |
| §GROUPS 经营工具组（L62-78） | 2 项：会议工作台 `/ceo-office/meeting`、决策室 `/ceo-office/decisions` | D6，§GROUPS 经营工具组 L62-78 |
| §GROUPS 公司资源组（L79-107） | 4 项：**成果库 `/ceo-office/company-runtime`**、知识库 `/ceo-office/knowledge`、财务 `/ceo-office/finance`（注释「v1 暂不建设（Blueprint §16），占位页标『规划中』」）、日历 `/ceo-office/calendar`（注释「v1 暂不建设，占位」） | D6，§GROUPS 公司资源组 L79-107 |
| §GROUPS 底部组（L108-124） | 2 项：设置 `/ceo-office/settings`、帮助与反馈 `/ceo-office/help` —— **均指向真实路由** | D6，§GROUPS 底部组 L108-124 |
| §ORDER（L134-139） | 四组固定顺序常量，与 GROUPS 一一对应，用于保证渲染与激活匹配稳定 | D6，§ORDER L134-139 |
| §PERSISTENT_LABELS（L147） | `["CEO 工作台", "经营", "业务", "工作空间"]` 共 4 项，注释自述「对齐原型 canonical-nav.js PERSISTENT_HREFS」，其余一级项折叠进「更多」抽屉 | D6，§PERSISTENT_LABELS L147 |
| §findActiveNav（L163-206） | 两轮匹配消除前缀误吞：第一轮只做一级 href 精确匹配（因「CEO 工作台」href 为 `/ceo-office` 会前缀误吞所有子路由）；第二轮按 subs 的 path 加 query 匹配；兜底再按最长前缀父项匹配 | D6，§findActiveNav L163-206 |
| §侧栏暴露路由统计 | GROUPS 全量展开共 **17 个路由**（公司组 5 加 4 个 subs = 9，经营工具 2，公司资源 4，底部 2）。与 D7 主理人审计数字一致 | D6，§GROUPS 统计 |

### D7：主理人前端路由审计结果（既有输入 · 本轮已独立核实）

> 主理人在任务书中直接给出的审计结论。本轮**未重复劳动**，仅做独立复核验证其准确性 —— 来源：D类·主理人

| 章节（审计条目） | 内容摘要与核实结论 | 出处 |
| --- | --- | --- |
| §审计-总量 | 原始结论「前端共 50 个 `page.js`，侧栏导航仅暴露 17 个路由」。**核实结论：完全准确**。实测 `page.js` 共 50 个；`TerraNavData.GROUPS` 全量展开为 17 个路由 | D7，§审计-总量 |
| §审计-静态路由分布 | 派生核实：50 个中静态路由 37 个、动态路由 13 个。侧栏暴露 17 个，**即 20 个静态路由在侧栏之外** | D7，§审计-静态路由分布 |
| §审计-孤岛页 | 原始结论「零站内入口的孤岛页 10 个」，列出 `/capabilities` `/employees` `/projects` `/org-center` `/guide` `/login` `/platform/commercial` `/platform/results` `/ceo-office/knowledge/memory` `/control/secret-vault`。**核实结论：这 10 个全部成立**（其中前 4 个仅以字符串形式出现在 `GlobalAssistant.js` 的 `WORKSPACE_PREFIXES` 前缀匹配数组中，非可点击链接，故确为零入口）。**但本轮发现应再增 2 个**，详见下行 | D7，§审计-孤岛页 |
| §审计-孤岛页修正 | **修正项**：`/ceo-office/reports` 与 `/ceo-office/brainstorm` 的外部引用数经实测均为 **0** —— 它们仅被各自的子详情页（`reports/[id]`、`brainstorm/sessions/[id]`）反向引用，无任何父级或同级页面指向其列表页。因此实际零入口孤岛页应为 **12 个**而非 10 个 | D7，§审计-孤岛页修正 |
| §审计-双套路由 | 原始结论「存在重复并存的双套路由体系 3 组」，列出 capabilities / employees / projects 三对。**核实结论：数量应为 4 组**（漏计 `/org-center` ⟷ `/ceo-office/organization`）；**且性质需修正**——这 4 个旧路由均为 **6 行 `redirect()` 垫片文件**，注释统一写明「旧暗色…页 → 重定向到新…页」，属**单向重定向遗留**，而非两套并行实现 | D7，§审计-双套路由 |
| §审计-有链接不在侧栏 | 原始结论列出 6 项：`/ceo-office/execution` `/reports` `/runtime-trace` `/strategy-room` `/brainstorm` `/capabilities`。**核实结论：实为 4 项**——`/reports` 与 `/brainstorm` 外部引用为 0，应移入孤岛页清单。余下 4 项实测外部引用数：execution 9、runtime-trace 1（来自 `/ceo-office` 页）、strategy-room 1（来自全局挂载的 `GlobalAssistant.js`，标签「AI 会议室」）、capabilities 6 | D7，§审计-有链接不在侧栏 |
| §审计-侧栏 17 路由清单 | 原始结论列出 17 条并指出 `PERSISTENT_LABELS` 只常驻 4 项（CEO 工作台 / 经营 / 业务 / 工作空间），其余折叠进「更多」抽屉。**核实结论：完全准确**，与 D6，§PERSISTENT_LABELS L147 一致 | D7，§审计-侧栏 17 路由清单 |

### D8：`.workbuddy/memory/MEMORY.md`

> 项目既有约束与不可动摇红线 —— 来源：E类·长期项目记忆（已精简版，13 节）

| 章节 | 内容摘要 | 出处 |
| --- | --- | --- |
| §1 席位与 Gate | 席位链：总控决策席(CEO) → 产品规划席 → 系统交付席 → 质量运行席 → 安全边界席。L2 Gate 七项必触发总控：商业模式、收费规则、新市场、Marketplace、权限边界、Admin/Workspace 边界、新核心资产体系 | D8，§1 |
| §2 汇报规范 | 强制三段式：结论 → 原因 → 建议；中文白话、先结论后原因 | D8，§2 |
| §3 产品主轴基准 | 标注日期 2026-07-21，标注「最高优先级」。称「Curis = 一人公司**自动任务与工作流系统**」，三层为「组织层（公司→部门→项目→员工）/ 运行层（核心：目标→规划→任务图→队列→调度→执行→验收→返工→完成）/ 能力层」。四原则含「全自动任务流是核心」。并称「当前阶段：前端仅极简 6 步入口，**CEO Office / 员工形象 / 复杂看板 / 组织树美化后置**」 | D8，§3 |
| §4 范围红线 | 标注日期 2026-08-02。**唯一真相源为 `Curis_Product_Blueprint.html`（v4.4 Single Current Status Review）**，禁止平行版本，旧版 REJECTED 归档。v1 为单机本地桌面自用。明确暂不建设含 Marketplace 开放生态。v1 允许 self-use 外部连接与能力配置。**红线判定原则：卡的是商业化/多租户/对外售卖资产，不卡个人本地自用下的外部连接与能力配置**。并声明旧版 §4「铁律不碰」已作废 | D8，§4 |
| §5 前端分工与部署隔离 | 目录边界：`frontend/app/platform/**` 为 Admin；`frontend/app/ceo-office|employees|control|page.js` 为 Workspace；`backend/` 为共享；`admin-platform/` 为预留空目录。互改禁令：Admin 不直改 Workspace 页，反之亦然 | D8，§5 |
| §6 Git 基线纪律 | 每个 issue 前 `git status` 干净；一个 issue 一提交并标注 Admin/Workspace/Shared；文档与代码阶段分离 | D8，§6 |
| §7 框架故障兜底 | 子代理报 not available 时用 general-purpose 兜底 | D8，§7 |
| §8 Blueprint 唯一 Current | 路径 `docs/01_Product/Curis_Product_Blueprint.html`，Status Review（Q-1~Q-4 裁决后转 Frozen）。**变更顺序：Blueprint → Design → Code；禁止平行版本**。生成器在 `.workbuddy/build/blueprint/` | D8，§8 |
| §9 UI 原型 Frozen 状态 | 标注 2026-08-05 已达成 Frozen。原生 HTML 加 729KB mock，无框架无构建。设计系统唯一真源 `_system/tokens.css`；圆角收敛 4 档、间距 6 档；**顶栏统一 52px、侧栏统一 220px、导航由 `canonical-nav.js` 统一渲染**。能力闭环 `curis-cap-verify.js` 24/24 PASS | D8，§9 |
| §10 前端视觉体系裁定 | 标注 2026-08-05 总控直接裁定，硬约束。**`terra-*` 令牌体系 / `Terra*` 组件视觉 / `design-spec/curis-ui-v2` 全部作废**；v1 视觉以 Frozen `--ui-*` 为准。**保留范围：路由结构、API 集成、数据逻辑、后端契约不在作废范围，仅视觉层按 `--ui-*` 迁移** | D8，§10 |
| §11 桌面构建 | Tauri 工程在 `desktop/`。运行时拉起后端 uvicorn:8000 与前端 next start:3000。**CEO 工作台在公司不存在时显示「尚未创建公司→创办流」门禁屏为正确 v1 行为**；3 业务空间 runtime 真实指标依赖 CI 与外部平台，v1 暂无故显示占位，属设计边界非 bug，禁止编造 | D8，§11 |
| §12 前端任务执行接线 | 启动任务真端点 POST `/api/task` 后 POST `/api/task/{id}/run`。首屏 first-run 判断唯一真源为后端 home/summary 的 `ai_readiness`。组件 `FirstRunGate.js`、`TaskLauncher.js`（三工作台三态门禁） | D8，§12 |
| §13 密钥存储安全 | 架构上不可能明文落盘，`credential_vault` 仅存进程内存，DB 只存 `credential_ref` 与 `secret_digest`。后端启动自动加载 gitignored 的 `.env` | D8，§13 |

### D9 与 D10：本轮发现但未纳入摘要的资料

| 编号 | 处理说明 | 出处 |
| --- | --- | --- |
| D9 | `docs/01_Product/Blueprint_vs_UI_Diff_2026-08-06.md`（8KB）。文件自述「目的：在不动任何代码/文档的前提下，逐条坐实『Blueprint 与 UI 原型脱节』的具体差异、证据与影响面，供总控决策席选定治理方向」「状态：仅诊断，未改动」。**因其为诊断分析产物而非原始资料，且不在主理人指派清单内，本轮仅登记存在性，未摘录任何结论。** 请主理人裁定是否纳入 | D9，§0 权威链与结论摘要 |
| D10 | `docs/03_Design/Curis_Design_System.md` §3.1 Navigation hierarchy（第 67~81 行）。**仅为核实 D3 文件头的来源声称而定向解析**。实测 §3.1 内容为：公司 5 项 / 经营工具 2 项 / **办公室「由已配置的业务空间生成的部门办公室入口」** / 公司资源 4 项 / 设置与帮助固定底部，并写明「办公室入口是 Workspace 的运行入口，不是与公司级栏目平级的新产品模块」。核实结论：**D3 的来源声称属实，`canonical-nav.js` 确实源自本设计文档而非直接源自 D1 Blueprint** | D10，§3.1 L67-81 |

---

## 3. 冲突记录

> 不同资料对同一事实描述矛盾时，**并列保留两个版本**，不做裁决。

| 编号 | 冲突主题 | 版本 A | 出处 A | 版本 B | 出处 B | 差异说明 |
| --- | --- | --- | --- | --- | --- | --- |
| X1 | 一级页面的数量与命名 | 「**四个入口**是同一经营系统的投影」：经营 / 业务 / AI 团队 / 工作空间 | `D1，§09` | 「进入经营后的**五个一级页面**」：CEO Desk / 经营 / 业务 / **公司** / 工作空间 | `D1，§14.4` | Blueprint 文档内部冲突。数量 4 与 5 不一致；同一栏目在 §09 与 §14.1 称「AI 团队」，在 §14.4 称「公司」 |
| X2 | 侧栏是否存在「更多」折叠抽屉 | 左侧导航固定内容为「公司（5 项）、经营工具、办公室、公司资源；底部设置与帮助」，**未定义任何折叠或常驻区概念** | `D1，§14.1` | **PERSISTENT_HREFS 仅 4 项常驻**（ceo-desk/operating/business/workspace-portal），AI 团队与 tools、resources、offices 全部折叠进默认收起的「更多」抽屉 | `D3，§PERSISTENT_HREFS L232-244` | 结构基线与 UI 基线对同一侧栏的信息架构描述不同。A 为平铺全量，B 为 4 常驻加折叠 |
| X3 | v1 办公室（业务空间）的数量 | 「v1 已确认业务空间…当前确认为**三类**——软件研发 software、小红书运营 xhs、抖音·TikTok 运营 shortvideo」 | `D1，§16` | `NAV_MODEL.offices` 为**四项**，除上述三类外另有「部门办公室 workspace-runtime-department.html」 | `D3，§NAV_MODEL L40-45` | 数量 3 与 4 不一致。部门办公室在 D1 的 v1 确认清单中无对应项 |
| X4 | 办公室入口的生成方式 | 办公室「**由已配置的业务空间生成**」，且「办公室入口是 Workspace 的运行入口，不是与公司级栏目平级的新产品模块」 | `D1，§10 UI 原则` 与 `D10，§3.1 L67-81` | `TerraNavData` 将 4 个办公室写成「工作空间」项下的**静态 subs 数组，恒定渲染**，不随公司状态变化 | `D6，§GROUPS 公司组 L21-61` | 生成方式冲突：动态生成 与 静态恒显。注：`D3，§activeOffices L109-129` 采用「硬编码目录 + 按公司状态动态过滤」的折中形态，与 A、B 均不完全相同 |
| X5 | 原型页总数 | 「§4 页面规格（**18 页**）」，且 §7 验收 Checklist 写「全站 **18 页** 字号档位 ≤ 7 档」 | `D2，§4 标题` 与 `D2，§7` | 目录实际存在 **20 个** HTML 文件；且 §4 表格自身展开后覆盖 20 个页面（`workspace-runtime-*` 一行代表 4 个文件） | `D4，§目录清单` | 数字 18 与 20 不一致。规格文档自身的标题数字与其表格内容也不自洽 |
| X6 | studio / shell-reference / day-demo 的入口 | 三者的「入口」列分别标注为「导航」「导航」「导航」 | `D2，§4 页面规格表` | `NAV_MODEL` 中**不存在**这三项；`workspace-studio` 与 `workspace-shell-reference` 被列入 `RUNTIME_PAGES`（由「工作空间」代表，无独立入口），`ceo-day-demo` 未出现在任何模型中 | `D3，§NAV_MODEL L28-56` 与 `D3，§RUNTIME_PAGES L87-94` | UI 基线内部冲突：规格文档声称有导航入口，导航真源中并无对应项 |
| X7 | 设置与帮助的目标 | footer 两项 href 均为 `#`，且 P2-5 注释明确「设置 / 帮助不再是无动作的死链接，改为**打开 CEO 助理**」；原型中不存在独立设置页与帮助页 | `D3，§NAV_MODEL L52-55` 与 `D3，§render L281-298` | 底部组两项指向**真实路由** `/ceo-office/settings` 与 `/ceo-office/help`，且前端确实存在这两个 `page.js` | `D6，§GROUPS 底部组 L108-124` 与 `D5，§设置与帮助` | 交互目标冲突：打开助理浮层 与 跳转独立页面 |
| X8 | 「成果库」的落点 | 成果库 → `assets.html`（原型中确实存在该页，5.9KB，h1 为「成果库」） | `D3，§NAV_MODEL L47` 与 `D4，§assets.html` | 成果库 → `/ceo-office/company-runtime`；前端**不存在** `assets` 路由，而 `company-runtime` 页内标题恰为「成果库」 | `D6，§GROUPS 公司资源组 L79-107` 与 `D5，§公司资源` | 标签相同但路由命名不同。前端以 `company-runtime` 承载「成果库」语义 |
| X9 | Curis 的产品定义与三层结构 | 「Curis = 一人公司**自动任务与工作流系统**」；三层为「组织层（公司→部门→**项目**→员工）/ 运行层（目标→规划→**任务图**→队列→调度→执行→验收→返工→完成）/ 能力层」；四原则含「**全自动任务流是核心**」 | `D8，§3`（标注 2026-07-21，标注「最高优先级」） | 「Curis 不是什么：**Task Manager**、**Workflow Platform**、Agent Collection、BI Dashboard、CRM/ERP、Generic Chat」；「**不以 Project、Task、Meeting、Knowledge 作为产品根**」；产品层次为 Platform/Admin 逻辑层 加 Company Runtime | `D1，§01 Curis 不是什么` 与 `D1，§16 明确暂不建设` | **根本性定义冲突**。A 以任务流为产品本体，B 明确否定任务流为产品本体。二者日期不同（A 为 2026-07-21，B 所属 §4 红线为 2026-08-02），且 A 未被标注作废 |
| X10 | 办公室是否属于「v1 暂不建设」 | 注释称办公室 4 项「均为 v1 占位页（**Blueprint §16 明确暂不建设**），业务启动后可激活」 | `D6，§文件头 L15-17` | §16「明确暂不建设」清单**五项均不含业务空间**；相反，§16 另有独立段落确认三类业务空间为「**v1 已确认业务空间**」，属保留项 | `D1，§16 明确暂不建设` 与 `D1，§16 v1 已确认业务空间` | 引述与被引述原文相反。B 为被引用文件的原文 |
| X11 | 财务与日历是否属于 v1 建设范围 | 财务注释「**v1 暂不建设（Blueprint §16）**，占位页标『规划中』」；日历注释「v1 暂不建设，占位」 | `D6，§GROUPS 公司资源组 L79-107` | §16「明确暂不建设」五项清单中**未列财务与日历**；且 `NAV_MODEL.resources` 含二者，`D2，§4` 亦将二者列为正式页面并给出数据契约 | `D1，§16 明确暂不建设`、`D3，§NAV_MODEL L46-51`、`D2，§4` | 范围归属冲突。B 侧三份资料一致地将财务与日历作为在建项 |
| X12 | 零入口孤岛页的数量 | 「零站内入口的孤岛页（**10 个**）」 | `D7，§审计-孤岛页` | 实测为 **12 个**，应增补 `/ceo-office/reports` 与 `/ceo-office/brainstorm`（二者外部引用数实测均为 0，仅被各自子详情页反向引用） | `D7，§审计-孤岛页修正` 与 `D5，§旧规划残留页` | 数量 10 与 12。差异源于 A 将 reports 与 brainstorm 归入了「有站内链接」类 |
| X13 | 重复路由的组数与性质 | 「存在重复并存的**双套路由体系（3 组）**」：capabilities / employees / projects | `D7，§审计-双套路由` | 实测为 **4 组**（另有 `/org-center` ⟷ `/ceo-office/organization`）；且四者均为 **6 行 `redirect()` 垫片**，属单向重定向遗留而非两套并行实现 | `D7，§审计-双套路由` 与 `D5，§旧路由重定向垫片` | 数量 3 与 4，且性质表述「并存」与「单向重定向垫片」程度不同 |
| X14 | 「有站内链接但不在侧栏」的数量 | 列出 **6 项**：execution / reports / runtime-trace / strategy-room / brainstorm / capabilities | `D7，§审计-有链接不在侧栏` | 实测为 **4 项**：execution（9 处引用）/ runtime-trace（1）/ strategy-room（1）/ capabilities（6）。reports 与 brainstorm 外部引用为 0，应归入孤岛页 | `D7，§审计-有链接不在侧栏` | 数量 6 与 4，与 X12 为同一组事实的两面 |
| X15 | 导航模型的规范来源链 | `canonical-nav.js` 文件头第 4 行自称「规范来源：`docs/03_Design/Curis_Design_System.md` §3.1 Navigation hierarchy」，即源自**设计文档** | `D3，§文件头 L1-21`（已由 `D10，§3.1 L67-81` 核实属实） | 「唯一真相源为 `Curis_Product_Blueprint.html`」「变更顺序：**Blueprint → Design → Code**；禁止平行版本」 | `D8，§4` 与 `D8，§8` | 来源链冲突：UI 导航真源实际锚定在 Design 层文档上，而非 Blueprint。是否构成 D8 所禁止的「平行版本」，本摘要不做裁决 |
| X16 | 一级栏目的路由命名语义 | 经营 → `operating.html`；业务 → `business.html`；AI 团队 → `ai-organization.html` | `D3，§NAV_MODEL L28-35` | 经营 → `/ceo-office/**analytics**`；业务 → `/ceo-office/**projects**`；AI 团队 → `/ceo-office/organization` | `D6，§GROUPS 公司组 L21-61` | 命名语义冲突。B 侧 `analytics` 与 `D1，§01`「Curis 不是 BI Dashboard」、`projects` 与 `D1，§16`「不以 Project 作为产品根」在措辞上相反；但两页页内标题实为「经营」与「业务」，且注释自述严格对齐原型（`D5，§CEO 工作台主干`），即**路由名与页面内容语义不一致** |

### 3.1 资料缺口清单

> 以下为「基线中未定义」或「资料本身缺失」的事实，非冲突，单独列出以免下游误当作已定义。

| 编号 | 缺口描述 | 出处 |
| --- | --- | --- |
| G1 | **结构基线自身尚未冻结**：D1 状态为 Status: Review 而非 Frozen；§16 冻结前门禁表五个场景中，四个为 Simulation Pending，一个为 Blueprint Review，**无一项已通过** | `D1，§16 冻结前的 Runtime Simulation 门禁` |
| G2 | D1 中**未定义**：「更多」折叠抽屉、workspace-studio 作为独立页面的导航位置、设置页与帮助页的页面形态。这三项在 D1 中均为基线中未定义 | `D1，§14.1` 与 `D1，§13` |
| G3 | 前端**不存在**以下原型页的对应路由：`assets`、`founding-flow`、`workspace-studio`、`workspace-shell-reference`、`ceo-day-demo`（已用目录查找确认为空） | `D5，§缺失路由核查` |
| G4 | 原型中**不存在**独立的设置页与帮助页实体（footer href 为 `#`，点击打开助理浮层）；而前端存在这两个页面。即该两页**无 UI 基线可参照** | `D3，§render L281-298` 与 `D5，§设置与帮助` |
| G5 | `workspace-runtime-department.html` 在原型内**零入链**，且 `workspace-portal.html` 的出链**不含** department。即部门办公室在 UI 基线中无门户级入口，仅能经 `canonical-nav` 在 `departmentStatus === 'active'` 时出现 | `D4，§workspace-runtime-department.html` 与 `D3，§activeOffices L109-129` |
| G6 | `ceo-day-demo.html` 在原型内**零入链且零出链**，完全孤立；`workspace-shell-reference.html` 零入链 | `D4，§ceo-day-demo.html` 与 `D4，§workspace-shell-reference.html` |
| G7 | D9（`Blueprint_vs_UI_Diff_2026-08-06.md`）与 D10（`Curis_Design_System.md` 全文）**未列入本轮指派范围**。D9 直接针对「应然与实然差值」这一议题，D10 是 D3 的实际规范来源。是否补充纳入，需主理人裁定 | `D9，§0` 与 `D10，§3.1 L67-81` |
| G8 | D2 §7 验收 Checklist 首项存在**重复行**（同一条「tokens.css 已包含全部令牌」同时以未勾选与已勾选两种状态出现），无法据此判定该项真实状态 | `D2，§7` |

---

## 4. 硬指标清单

| 章节 | 硬指标 | 状态 |
| --- | --- | --- |
| §1 | 每份资料有解析状态，失败/跳过注明原因 | ✅ 10 份资料（D1~D10）全部标注解析状态；D9 跳过与 D10 限定范围解析均已注明原因；无解析失败项 |
| §2 | 每份文档按章节逐条摘要，每条标注了 `D编号，§章节` | ✅ D1~D8 逐份按自身章节结构成表，共 168 条摘要，每条均带 `D编号，§章节` 出处列；D9/D10 单独登记并标注出处 |
| §3 | 冲突信息并列保留，不做裁决 | ✅ 16 项冲突（X1~X16）全部以「版本 A + 出处 A / 版本 B + 出处 B」并列保留，无一项做出裁决 |
| §1 | 覆盖主理人指派的 A/B/C/D/E 五类资料 | ✅ A类 D1；B类 D2/D3/D4；C类 D5/D6；D类 D7；E类 D8。全部覆盖，无遗漏 |
| §2 | 20 个原型页逐页记录职责、导航位置、出链与入链 | ✅ D4 表格 20 行，逐页给出职责、canonical-nav 位置、出链数、入链数 |
| §2 | 50 个前端路由全部枚举并归类 | ✅ D5 按 13 个路由分组覆盖 37 静态 + 13 动态 = 50 个 `page.js` |
| §2 | 核实 D6 文件头「已对齐 canonical-nav.js 唯一真源」的声称 | ✅ 已逐项核实，声称**不完全成立**，具体偏差见 X4、X7、X8、X10、X11、X16 |
| §2 | 核实 D7 主理人路由审计的准确性 | ✅ 已独立复核，总量与侧栏 17 项准确；提出 3 项修正（X12 孤岛页 10→12、X13 双套路由 3→4 且性质修正、X14 有链接不在侧栏 6→4） |
| §3.1 | 资料缺口单独成列，不与冲突混同 | ✅ G1~G8 共 8 项，独立于 X1~X16 |
| 全文 | 应然（基线）与实然（现状）分开陈列，不合并 | ✅ D1~D4 为应然基线区，D5~D7 为实然现状区，§0 顶部声明组织原则 |
| 全文 | 无残留占位符、示例前缀、待补充字样 | ✅ 全文无占位标记、无示例前缀、无待补充字样 |
| 全文 | 不做业务或技术裁决，不产出下游产物 | ✅ 未产出高层架构、系统设计、UserStory、部署或安全设计；未给出重构方案与改造建议 |

---

## 附录 A：生成流程

### 流程总览

| 步骤 | 动作 | 落入章节 |
| --- | --- | --- |
| Step0 | 读取模板 + 主理人转交的 A/B/C/D/E 五类原始资料 | — |
| Step1 | 盘点资料清单，标注解析状态 | §1 |
| Step2 | 逐份打开资料，按自身章节结构逐条摘要 | §2 |
| Step3 | 交叉比对不同资料，发现并记录矛盾 | §3 |
| Step4 | 逐项核验硬指标 | §4 |

```mermaid
flowchart LR
    S0[读取模板与资料] --> S1[盘点资料清单]
    S1 --> S2[逐份精读逐章节摘要]
    S2 --> S3[交叉比对记录冲突]
    S3 --> S4[硬指标自检]
```

### 本轮实际执行路径

| 阶段 | 具体动作 | 产物 |
| --- | --- | --- |
| 模板对齐 | 读取 `material_digest.md` 模板，识别 §0~§4 加附录 A/B 骨架与全部待替换标记 | 章节骨架 |
| A类解析 | 将 89KB Blueprint HTML 去脚本去样式后转为纯文本（939 行），提取 147 个标题，逐节精读 | D1 摘要 47 行 |
| B类解析 | 直读 Frozen Spec 与 canonical-nav.js 全文；对 20 个原型页运行结构化脚本，提取 title/h1/page-title 与全部站内 html 跳转，构建出链入链矩阵 | D2/D3/D4 摘要 |
| C类解析 | 枚举 50 个 `page.js`；对 102 个前端源文件做全量路由字符串扫描，逐路由统计外部引用数并排除自引用，判定可达性 | D5/D6 摘要 |
| D类核实 | 用 C 类扫描结果逐条比对主理人审计的四项结论，定位差异并追查根因（如 `WORKSPACE_PREFIXES` 非链接、reports/brainstorm 仅子页反向引用） | D7 摘要 + 3 项修正 |
| E类解析 | 直读 MEMORY.md 全 13 节 | D8 摘要 |
| 溯源核实 | 因 D3 自称来源为设计文档，定向解析 `Curis_Design_System.md` §3.1 予以证实 | D10 登记 |
| 交叉比对 | 在应然（D1~D4）与实然（D5~D7）之间、以及各基线文档内部做两两比对 | X1~X16 |
| 缺口归集 | 将「基线中未定义」与「资料缺失」从冲突中剥离，单独成列 | G1~G8 |

### 整理原则

1. **逐份精读，不跨文档归并**：摘要按文档自身章节结构组织，不做跨文档的主题重组（那是下游的事）
2. **出处即章节号**：每条摘要标注 `D编号，§章节`，直接映射回原文位置
3. **冲突保留**：矛盾信息并列保留两个版本，不擅自裁决
4. **事实驱动**：以原始资料中的事实为准，不添加主观推断
5. **应然与实然分列**：基线资料与现状资料分区陈列，使差值可见而不被合并抹平
6. **缺口即事实**：基线中未定义的内容明确写为「基线中未定义」，不脑补填补

---

## 附录 B：解析 Skill

模板登记的四类解析 Skill：

- `docx`：Word 类产品/业务文档
- `pdf`：PDF 类规范、手册、报告
- `pptx`：PPT 类方案/汇报
- `xlsx`：Excel 类数据清单、指标表

**本轮实际调用情况**：本轮资料类型为 `html` / `md` / `js` / 结构化文本，不含 docx / pdf / pptx / xlsx，因此上述四项解析 Skill **本轮均未调用**。实际采用的解析手段如下：

| 资料类型 | 解析手段 | 适用资料 |
| --- | --- | --- |
| `html`（长文档） | 去除 script 与 style 后按标题层级转纯文本，保留表格行与列表项结构 | D1 |
| `html`（页面集合） | 结构化脚本批量提取 title / h1 / page-title 与站内跳转，构建出链入链矩阵 | D4 |
| `md` | 直接全文读取 | D2、D8、D9、D10 |
| `js` | 直接全文读取并按代码区段（常量定义、函数、导出）切分摘要 | D3、D6 |
| 路由可达性 | 全量源文件路由字符串扫描，逐路由统计外部引用并排除自引用 | D5、D7 |
