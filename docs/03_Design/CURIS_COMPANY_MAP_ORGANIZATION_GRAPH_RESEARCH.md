# CURIS COMPANY MAP / ORGANIZATION GRAPH RESEARCH

> **Authority Class**：RESEARCH  
> **状态**：RESEARCH / REVIEW  
> **Disposition**：CONSUMED BY CURRENT PRODUCT TRUTH（Company Map / Organization Center）；本文件仍只解释研究依据，不定义 Current。
> 本文的 Variant A / Department Container 仅作为产品与交互方向被消费；最终视觉仍由 Current UI Blueprint 与后续 Design Authority 决定。
> **范围**：Curis「组织中心 → 公司版图」的信息架构、图谱结构与交互方式研究。
> **日期**：2026-08-18
> **停止态**：`CURIS COMPANY MAP / ORGANIZATION GRAPH RESEARCH — STOP FOR CEO REVIEW`

---

## 0. 结论摘要（CEO 一分钟版）

Curis 公司版图的目标不是画一张「汇报关系树」，而是让 CEO 一眼看到**公司长成什么样、业务扩张到什么程度、哪里空岗、哪里有风险**。

**本研究最终推荐（详见 §13–§14）：**

1. **默认主视图 = Option C（Hybrid Company Map）**：以 Department 为分组容器、Business 为一级节点、Role 为可展开 chip、Employee 默认隐藏的「业务版图」视图；员工反查交给已有的「员工目录」独立 Surface。
2. **不采用传统 HR Org Chart、不采用全自由 Network Graph、不采用数据大屏**。
3. **技术首选 React Flow（@xyflow/react，MIT）**，第二选择 AntV G6（MIT，中文文档完善），不建议 GoJS / yFiles / BALKAN OrgChart / UNICEF react-org-chart。
4. 公司版图与 Workspace 的边界保持：**点击 Business → Business Detail / Operating Model，绝不默认跳办公室**（Blueprint 已定，本研究会支撑该边界的具体交互）。
5. 大公司扩展（10 Dept / 50 Business / 200 Role / 500 Employee）的答案不是「更强布局算法」，而是 **Progressive Disclosure + 员工默认隐藏 + Focus Mode + 搜索 + 过滤 + Minimap**。

---

## 1. Curis 问题定义

### 1.1 产品使命（来自 Blueprint · 组织中心）

> 公司版图不是传统 HR Org Chart，而是让 CEO 一眼看到公司现在长成什么样、业务扩张到什么程度；员工目录从 Employee 反查 Role、Business 和 Department。协作关系不作为默认平级主视图，只在公司版图中按需展开。

**要回答的 CEO 问题（Blueprint 第一视觉层）：**

| 第一视觉层 | 表达什么 |
|---|---|
| Department 分布 | 稳定责任聚合和新形成的组织分组 |
| Business 分布 | 公司经营范围和新增业务 |
| Business 当前状态 | 正在形成、运行、暂停、阻塞或需要 CEO 关注 |
| Role / Staffing 概况 | 岗位数量、空岗、增加、拆分和绑定变化 |
| Risk / Blocker / 最近重要 Result | 轻量经营信号，不默认展开全部员工 |

### 1.2 核心设计张力

| 张力 | 说明 | 处理原则（本研究） |
|---|---|---|
| 版图感 vs 报表感 | 要看「公司长成什么样」，不是看指标 | 结构优先于数字；Badge / 色边表达状态，不用图表 |
| 一眼看懂 vs 信息完整 | 第一屏不能塞满所有字段 | 直接显示最小集，Hover 次集，Click 进入 Detail |
| 组织关系 vs 业务关系 | Curis 需要同时表达 Organization + Business Portfolio + Role/Staffing + Growth | 默认主视图 = 业务版图；组织/汇报关系按需展开或交给员工目录 |
| 图谱 vs 树 | 自由网络图表达多关系，但会产生交叉线爆炸 | 默认层级 + 受控展开，杜绝全自由网络图 |
| 编辑 vs 浏览 | 结构编辑（+ 建部门/业务/Role）与日常浏览冲突 | Create Where You Organize；Add Where You Work（Blueprint 已 Frozen） |

### 1.3 不重做、不推翻的边界（Current Authority）

- 阅读顺序（Frozen）：`Company → Department → Business → Business Operating Model → Role Structure → Employee Binding`（Blueprint）。
- 反查顺序：`Employee → Role → Business → Department`（员工目录）。
- 点击 Business → **Business Detail / Operating Model**，不直接跳 Workspace（Blueprint）。
- 展开 Role 后才查看 Employee Binding（Blueprint）。
- Business Duplication 创建的新 Business **必须自动出现在同一 Company Map / Organization Truth**（Blueprint）。
- 编辑模型（Frozen）：`Company + → Department；Department + → Business；Business/Team + → Role；Role + / Employee Directory + → Employee；Workspace → Add Employee（只组队，不复制身份）`。
- Business = Team + Office（Shared Authority §9 · Frozen）；渐进工作形态保留。
- 空间工程部为默认第一核心 Department。
- 本研究报告**不修改** Product Blueprint / Master Map / UI Blueprint / Frozen Authority / Shell；不写代码；不做高保真；不新增 Runtime Primitive。

---

## 2. Current Authority 边界（读取到的当前事实）

**已确认并消费的当前模型（研究输入，非新定义）：**

1. **Product Blueprint**（v5.x · Review）：组织中心 = 公司版图（默认）+ 员工目录（反查）；第一视觉层五要素；Business Detail ≠ Business Workspace；复制业务 → 自动进 Company Map；Role Detail 六要素（Identity / Responsibility / Workflow Relationship / Required Capability / Staffing / Capacity·Load / Employee Binding）；Create Where You Organize / Add Where You Work。
2. **Product Master Map**（v3.0）：组织中心 = 展示公司关系，不要求用户从零设计组织；默认阅读顺序 `公司 → 业务 → 责任 → 员工 → 当前工作 → 结果`；部门/Shared Service 出现必须由真实工作触发（重复责任 / 共享依赖 / 独立责任容量）；组织建议卡需说明「为什么现在出现、聚合什么、影响什么、需确认什么」。
3. **Product UI Blueprint**：组织中心 = 一级导航 + 公司版图/员工目录；公司版图默认展示 Department、Business、经营状态、Role/Staffing、风险和重要结果；点击 Business → Business Detail / Operating Model；员工目录反查 Role/Business/Department；协作关系只按需展开。Context Sidebar 不用于员工列表；员工对话进 Profile/Workstation，不压进组织图旁的 Pane。
4. **Company OS Shared Authority**（§0–§9 · Frozen）：Employee ∈ Organization（组织轴）；Employee 经 Service/Assignment 可服务多个 Office；Assignment = 容量/资格非硬路由；Organization Routing 仅 WHO 解析；TEAM_LEAD_ONLY_ON_EXCEPTION 仅限任务路由层；§9 Business = Team + Office（Frozen）；三层语义 Process asks WHAT / Organization decides WHO / Capability determines HOW。
5. **Frozen Workspace Shell / P1–P7**：四栏（Nav / Context / Main / Utility / Search·History）职责；Employee Workstation 复用 Conversation-first；Employee Detail 复用 Utility Pattern；Context Isolation 保持（长期历史不自动全量注入）。

**结论**：公司版图的「信息层级」与「边界」已被 Authority 定义清楚；本研究只补**如何表达（图结构/交互/缩放/编辑/成长）**，不碰语义模型。

---

## 3. 竞品 / 开源研究

### 3.1 图谱 / 组织可视化库（核实到 2026-08）

| 库 | 许可证 | 维护状态 | 关键能力 | 商用注意 |
|---|---|---|---|---|
| **React Flow**（@xyflow/react） | MIT | 极活跃（v12.11.x，周更） | 节点=React 组件；内置 Zoom/Pan/Background/Minimap/Controls/NodeToolbar；Group 节点（parentId）；拖拽 | 默认带 attribution，Pro 订阅可移除；MIT 无商用限制 |
| **AntV G6**（antvis/G6） | MIT | 活跃（v5.1.x） | 图引擎；10+ 布局；Combo 分组；折叠/展开；动画；自定义节点；中文文档完善 | MIT 无限制；Canvas 渲染，富节点样式成本高 |
| **Cytoscape.js** | MIT | 活跃（周更/月更，11K+ stars） | 图论算法+可视化；大图；依赖零 | 面向图分析；树布局/分组需扩展（dagre 等）；Canvas |
| **D3** | MIT | 极活跃 | hierarchy/tree 布局原语；完全自由 | 低层：渲染/交互全自建，工期长 |
| **vis-network** | Apache-2.0 OR MIT | 活跃 | 物理图、拖拽、聚类 | 面向交互网络图，富 DOM 节点弱 |
| **Sigma.js** | MIT | 活跃（12K+ stars） | WebGL 大图渲染 | 渲染层，树/分组需自组 |
| **UNICEF react-org-chart** | MIT | **停滞**（最后更新 ~2020，周下载 ~460） | D3 SVG 组织树；懒加载；百万折叠节点 | 仅作设计参考，不建议生产使用 |
| **OrgChart JS（BALKAN）** | Community 版 MIT（功能受限）/ 商业版 EULA | 活跃（v9.3.x，2026-07 仍在发版） | 专为组织图：展开/折叠、搜索、多节点绑定 | 商业版闭源 EULA、需购买；Community 功能受限 |
| **GoJS** | 商业（Individual $3,995 / Team $6,990 / Group $11,950，per-developer 永久） | 成熟稳定 | 组织图/树/分组/撤销/导出 SVG/图像；React 支持 | 商用成本高；无运行时版税 |
| **yFiles** | 商业（单开发者约 $11,900 起，perpetual royalty-free） | 成熟稳定 | 最强布局算法；组织图 300+ demo | 商用成本高 |

### 3.2 现代组织产品（如何解决大组织浏览 / 折叠 / 聚焦 / 空岗）

| 产品 | 关键做法 | 对 Curis 的借鉴 |
|---|---|---|
| **ChartHop** | ① **Org Chart 上直接叠加多数据点**（角色/地点/成本/风险着色）② **动画 Timeline Slider**：回放组织结构随时间演进 ③ 拖拽式 Org Modeling（改组织=拖节点，生成 scenario 审批流）④ Data Sheet 表格视图与图并存 ⑤ Map 视图 | 「时间轴回放成长」是表达公司扩张的顶级参考；节点着色表达状态值得借鉴；编辑走 scenario+审批，不直接改真相 |
| **Rippling** | **Employee Graph 作为数据主干**：角色/部门/汇报变化自动传播到 IAM/权限/设备 | 组织图是数据真源层，不只是「一张图」；任何结构变化必须自动驱动下游（Curis：Role 拆分→Routing/Assignment 生效） |
| **Workday** | 企业级 HCM：矩阵汇报、Supergroup/动态组、headcount planning、组织架构与预算联动 | 大组织多视图并存；汇报关系可矩阵化（Curis 一人多岗 → 矩阵化表达可借鉴） |
| **Lattice** | 组织图叠加绩效/成长数据 | 节点附加轻量经营信号（Curis：Risk/Result badge） |
| **Deel** | 全球化合同工组织图 | 多身份/多归属员工表达 |
| **Pingboard / Workvivo** | 专注组织图：部门折叠、Focus mode、人员搜索、远程大屏展示 | 折叠+聚焦+搜索是普通用户默认交互；大屏 TV 模式可作「版图墙」参考 |
| **Team Topologies**（方法论） | 团队类型：Stream-aligned / Platform / Enabling / Complicated-subsystem；交互模式：Collaboration / X-as-a-Service / Facilitating | Role 拆分为 Sub-team 的语义表达；「平台型团队服务多个业务」→ 员工服务多 Office 的可视化思路 |

### 3.3 Business Architecture / Capability Map（比 HR Org Chart 更接近 Curis 的表达）

| 模型 | 核心 | 对 Curis 的借鉴 |
|---|---|---|
| **Business Capability Map** | 表达「公司能做什么」（WHAT），稳定、独立于汇报结构；TOGAF 明确警告不要把 Org Chart 直接转置成 Capability Map | **公司版图应表达「公司正在经营什么」**（业务组合），而不是「谁向谁汇报」——这正是 Curis 与 HR Org Chart 的差异根源 |
| **Operating Model Map** | 经营模式如何由价值流 + 能力 + 组织协作构成 | Business Operating Map 衔接层的参考（Goal/Strategy/Workflow/Role/Capability 分面） |
| **Enterprise Architecture Map** | 业务/数据/应用/技术多层联动 | 不建议照搬（Curis 不需要企业级多层 EA） |
| **Strategy Map**（Balanced Scorecard） | 财务/客户/内部/学习成长因果链 | 可作为 Business 健康度下钻的内容参考，但**不作主视图** |
| **Business Portfolio Map**（波士顿矩阵等） | 以二维轴（如增长×份额）排布业务组合 | 可作「业务组合」筛选视角（Growth×Health），不默认启用 |
| **Value Stream Map** | 端到端价值流 + 角色/交接 | 支撑 Workflow-Role 关联（F 节），与 Business Operating Map 同一思想 |
| **Team Topologies** | 团队形态与交互模式 | 支撑 Sub-team / 跨业务服务关系表达 |

**关键洞察**：传统 HR Org Chart 只回答 WHO；Business Capability/Portfolio Map 回答 WHAT；Curis 公司版图必须**以 WHAT 为骨架、以 WHO 为按需下钻**——即「业务版图」为主视图、「组织/汇报」为展开层。这与 Blueprint「协作关系不作为默认平级主视图」完全一致。

---

## 4. Pattern Matrix（候选模式 → Curis 适用性）

| 模式 | 说明 | 表达什么 | Curis 适用性 | 备注 |
|---|---|---|---|---|
| 传统 Org Tree（汇报树） | 父=管理者，子=汇报者 | WHO 汇报给谁 | ✗ 默认视图 | 无业务版图感；Blueprint 已排除 |
| 横向层级树 | Company→Dept→Business→Role 横排 | 层级归属 | ◎ 作为折叠交互骨架 | 缺分组容器与状态表达 |
| 分组容器（Nested Group） | Department/分组=外框，Business=内部节点 | 业务组合分布 | ✅ 核心结构 | 支持中间分组（国内/海外） |
| 自由 Network Graph | 节点+边表达任意关系 | 多对多关系 | ✗ 默认；△ 按需 | 一人多岗/跨团队会产生交叉线爆炸 |
| Radial / Circular | 中心放射 | 中心性 | ✗ | 中文标签阅读差；Curis 无中心枢纽语义 |
| Cluster（力导向聚类） | 物理聚类 | 亲疏关系 | ✗ | 无稳定布局，无法记忆位置 |
| Canvas + Zoom | 无限画布缩放 | 大图浏览 | ✅ 作为交互层 | 配合 LOD（Level of Detail） |
| Dashboard / 大屏 | 指标图表组合 | 数据结论 | ✗ | 「不变成 Dashboard」是硬约束 |
| Timeline Slider | 时间轴回放结构变化 | Growth 演进 | ◎ 高价值备选 | ChartHop 参考；v1 可选 |
| 表格/列表（Data Sheet） | 行=对象 | 全字段管理 | ◎ 员工目录已承担 | 不替代版图 |
| Focus Mode + Breadcrumb | 聚焦某部门/业务，路径面包屑 | 大组织导航 | ✅ 必选 | 10 Dept/50 Business 后必需 |
| Search + Filter | 搜索定位 + 风险/空岗/新变化过滤 | 快速定位 | ✅ 必选 | 员工默认隐藏的前提 |
| Minimap | 缩略图 | 大画布定位 | ✅ 必选（大公司） | React Flow 内置 |
| LOD（按缩放级别换信息密度） | 远=计数，近=名称 | 缩放语义 | ✅ 高价值 | 避免「缩小后密密麻麻」 |
| 节点内 Badge / 色边 | 状态/计数小标记 | 空岗/风险/新业务 | ✅ 核心 | 直接可见但轻量 |
| 路径高亮（Path Highlight） | 高亮某员工/业务所在路径 | 反查定位 | ◎ 员工目录已承担 | 版图内点击员工时可用 |

---

## 5. Company Map 信息层级（核心问题 A 的答案）

### 5.1 默认第一屏展示什么

**默认主层级（Blueprint 已定，本研究给出表达方式）：**

```text
Company（根部，默认收成一行公司名 + 总览计数）
└─ Department（分组容器，默认展开到「部门+业务」级）
   ├─ Business（一级节点，默认全部可见）
   │   └─ Role（chip 行，默认折叠，显示 数量/空岗）
   │       └─ Employee（默认隐藏，展开 Role 后才显示）
   └─ …（更多 Business）
```

**决策原则**：
- **默认展开到 Department → Business 两级**；Role 折叠为计数 chip；Employee 默认隐藏（Blueprint「不默认展开全部员工」）。
- 第一屏不是全公司全节点平铺，而是「所有部门 + 所有业务 + 角色计数」。

### 5.2 Business 节点最小信息集（直接显示 / Hover / Expand / Detail）

| 信息 | 默认直接显示 | Hover / Popover | 进入 Detail | 理由 |
|---|---|---|---|---|
| Name | ✅ | | | 定位必需 |
| Goal | | ✅ | ✅ | 防 Dashboard：不在节点上铺全文 |
| Leader | ✅（小头像/名字） | | ✅ | CEO 主要入口（§9） |
| Operating Status（运行/暂停/阻塞/形成中） | ✅（色边/小标） | | ✅ | 第一视觉层 |
| Role count | ✅（chip：`· 4岗`） | | ✅ | Staffing 概况 |
| Staffing / Vacancy | ✅（`2/4 · 空2` 空岗高亮） | | ✅ | 空岗是 CEO 关注点 |
| Health | | ✅ | ✅ | 需 Domain 定义（见 §16） |
| Risk / Blocker | ✅（Badge） | ✅ | ✅ | 第一视觉层 |
| Latest Result | | ✅ | ✅ | 轻量信号，不铺在节点 |
| Workspace Entry | （不显示） | | ✅（按钮） | 边界：点节点≠进办公室 |

> **铁律**：第一屏是「一眼看懂公司长什么样」，不是「看所有经营指标」。任何想在节点上堆数字的冲动，都先放到 Hover 或 Detail。

---

## 6. Business Portfolio 表达（核心问题 B 的答案）

### 6.1 表达「业务版图」的推荐结构：Department 分组 + Business 节点 + 可选中间分组

```text
内容增长部（Department 分组容器）
├─ 国内内容（可选中间分组 Sub-group）
│  ├─ 小红书（Business 节点）
│  ├─ 抖音
│  └─ 公众号
└─ 海外内容（可选中间分组）
   ├─ TikTok
   ├─ YouTube
   └─ Instagram
```

**研究结论**：
- **Nested Group（分组容器）+ 横向层级树**最适合 Curis Desktop：
  - Department = 外框容器（可折叠）；Business = 内部节点；中间分组（国内/海外）只在需要时形成（对应 Master Map「部门由真实工作触发」——中间分组同理，不强制创建）。
  - 横向（从左到右）优于纵向：Business 名多为中文短词，横向层级 + 分组外框的阅读顺序最自然；纵向树会因 Role 展开把宽度拉爆。
- **不用** Radial / Cluster / 自由 Graph：Curis 没有中心枢纽语义，中文标签在放射/力导向布局中阅读困难，且布局不稳定会让 CEO 无法记忆「我的公司长什么样」。
- **Map 隐喻**：可以是「业务版图」而非字面地图；不引入地理坐标。

### 6.2 早期 → 扩张的可视化

```text
早期：    内容增长部 └─ 小红书
扩张中：  内容增长部 ├─ 小红书 ├─ 抖音 └─ 公众号
进一步：  内容增长部 └（国内/海外分组）→ 6 个 Business
```

新 Business 出现 = 分组内新增节点（带 `NEW` 标记，见 §7）。分组形成 = 容器外框出现。Business Duplicate = 同分组内复制出的新节点（带来源标识，Hover 显示「由 小红书 复制」）。

---

## 7. 成长表达（核心问题 C 的答案）

### 7.1 可感知的成长信号与表达手段

| 变化 | 表达手段 | 说明 |
|---|---|---|
| 新 Business 出现 | 节点出现 + `NEW` Badge（N 天后淡出） | 「最近变化」时间窗 |
| Business Duplicate | 新节点 + Hover 来源提示 | 复制关系不画永久边 |
| Business 扩张（Business 增加） | 分组内节点数、部门计数徽章 | 计数而非图表 |
| Department 增加 | 新分组容器出现 | 容器级 |
| Role 增加 | Role chip 计数 +1 | 计数徽章 |
| Role 拆分 → Sub-team | Role 节点下出现子分组 | 对应 Shared Authority 语义 |
| Staffing 增长 | `2/4 → 3/4` 计数变化 | 数字变化即可感知 |
| 一岗多人 | chip 显示多头像 | 见 §8 |
| 一人多岗 | Employee 多 Role chips | 见 §8，不画交叉边 |
| 空岗 | 空 Role 用虚线节点 + `空岗` 标记 + 招募动作 | 第一视觉层 |
| Business 暂停/调整 | 状态色边（暂停=灰，调整=琥珀） | 状态色 |
| Risk / Blocker | 红色/琥珀 Badge | 第一视觉层 |
| 最近变化整体 | 「最近变化」过滤 + 节点微光 | 不是常驻动画 |

### 7.2 研究结论：不要用「动画」表达成长

- **ChartHop 的 Timeline Slider（时间轴回放）是唯一强烈建议保留的成长表达**：拖动时间轴回放组织结构演进（部门/业务/员工数变化）。它既表达成长，又不把静态视图做成大屏。
- **不建议**：节点大小随业务规模变化（会造成「谁大谁重要」误导）、常驻飘动/粒子动画、图表嵌入节点。
- **推荐**：`NEW`/`变更` 徽章 + 时间窗（如「本周新增 3 业务」摘要条）+ Timeline Slider（v1 可选，见 §16 决策点）。
- 「不要为了表达成长把图做成数据大屏」是硬约束：成长信息用**徽章、计数、状态色、时间窗摘要**表达，不用柱状图/折线图。

---

## 8. Role / Staffing 表达（核心问题 E 的答案）

### 8.1 默认形态

```text
Business 小红书
└─ 文案岗 · 2人          ← Role chip：名称 + 人数 + 状态点（满载/空岗/超载）
   ├─ 员工 A             ← 展开后：员工小节点（头像 + 姓名）
   └─ 员工 B
```

### 8.2 多形态表达

| 形态 | 表达 | 交互 |
|---|---|---|
| 一岗多人 | Role chip 显示多头像 + 人数 | 展开看全部 |
| 空岗 | 虚线 Role chip + `空岗` Badge + `+ 招募` | 点招募 → 新建员工 / 绑定已有 / 从人才与能力招募 |
| 一人多岗 | Employee 在**主 Role** 下出现一次；其他 Role 下用 `同头像 chip`（不画边） | 点 chip 或员工头像 → Employee Profile 展示全部 Role |
| Sub-team | Role 节点下再分组 | 对应 Role 拆分语义 |

### 8.3 研究结论：禁止默认用复杂 Network Graph 解决关系

- 一人多岗 / 跨业务服务是 **Employee ∈ Organization 轴** 的语义（Shared Authority），**员工只出现一次（主 Role），其余位置用轻量 chip 引用**；员工详情（Profile）才是展示全部 Role 的权威位置。
- **不画交叉边**：`Employee A ——[虚线]—— 抖音文案岗` 这类跨业务边，在 50 Business/500 Employee 时必然爆炸。
- 汇报关系（如果有）只在「组织视图」模式或员工详情中呈现，不是默认主视图的边。

---

## 9. 大公司扩展（核心问题 D 的答案）

### 9.1 研究结论：靠「浏览机制」而不是「布局算法」

10 Department / 50 Business / 200 Role / 500 Employee 的问题，**不是算法能解决的，是 Progressive Disclosure 解决的**。参考 ChartHop / Workday / Pingboard 的做法：

| 机制 | Curis 采用 | 说明 |
|---|---|---|
| Progressive Disclosure | ✅ 必选 | 默认只展开到 Department→Business；Role 折叠计数；Employee 默认隐藏 |
| 员工默认隐藏 | ✅ 必选 | 500 个员工节点永不默认平铺 |
| Collapse / Expand | ✅ 必选 | Department 容器、Business、Role 均可折叠 |
| Focus Mode + Breadcrumb | ✅ 必选 | 点 Department → 聚焦该部门全屏；面包屑返回 |
| Search | ✅ 必选 | 全局搜索：Business / Role / Employee 名称；命中后高亮路径并聚焦 |
| Filter | ✅ 必选 | 空岗 / 风险 / 最近变化 / 状态 过滤 |
| Minimap | ✅ 大公司必选 | React Flow 内置 |
| Zoom + LOD | ✅ 高价值 | 缩小=只显示计数；放大=显示名称；再放大=显示 Role/Employee |
| Lazy loading | ✅ | 按需加载子级（展开时才取数据） |
| 路径高亮 | ◎ 员工目录承担 | 版图内点员工 → 高亮其所在 Business 路径 |
| Timeline Slider | ○ v1 可选 | 成长回放 |

### 9.2 推荐组合（10 Dept / 50 Business / 200 Role / 500 Employee 时）

```text
默认：所有 Department 容器（折叠 Business）→ 计数徽章（每部门 N 业务 / M 岗 / K 人）
聚焦：点击部门 → 该部门内 Business 全部展开
下钻：展开 Business → Role chips → 展开 Role → Employee
定位：Search 命中 → 自动展开路径 + 高亮 + 居中
过滤：仅看「空岗」/「风险」/「本周新增」
```

---

## 10. Editing Model（核心问题 G 的答案）

### 10.1 `+` 按钮放在哪里

**结论：直接出现在节点上（Hover 显现），遵循 Frozen 编辑链：**

```text
Company + → Department        （公司级 + 在侧栏/公司头）
Department + → Business        （Department 容器头部 Hover 出 +）
Business / Team + → Role        （Business 节点 Hover 出 +）
Role + / Employee Directory + → Employee（Role chip Hover 出 +）
Workspace → Add Employee        （只组队，不复制身份）
```

- `+` **Hover 显现**（不是常驻），避免「编辑器感」。
- 创建入口统一弹「Create vs Add Existing vs Recruit」选择（Blueprint：每个添加动作支持选择已有、创建新的或从人才与能力获取）。

### 10.2 编辑方式研究

| 方式 | 建议 | 理由 |
|---|---|---|
| 节点上 `+`（Hover） | ✅ 采用 | Create Where You Organize |
| Context Menu（右键） | ✅ 采用（次要路径） | 移动/复制/暂停/解散等操作 |
| Drag & Drop 移动 Business | ◎ 可选（需确认） | 跨部门移动业务是低频结构变更；拖拽直观但易误操作；建议「拖到目标容器 + 确认」或「右键菜单选择」 |
| 节点 Reorder | ◎ 分组内排序支持 | 轻微拖拽排序可接受 |
| 自由画布拖拽节点位置 | ✗ 禁止 | 结构是真相，不是画布装饰 |
| Employee Binding 拖拽 | △ 谨慎 | 绑定 = 责任变更，必须走确认/变更记录（Master Map：责任变化必须另有明确的变更与交接记录） |
| 空岗 / Vacancy | ✅ 虚线节点 + 招募动作 | 直接可操作 |

**编辑原则**：**浏览是默认态，编辑是显式动作**。所有结构变更（建/拆/移/绑定）都要有明确入口与确认，避免误操作改变 Organization Truth。

---

## 11. Business Operating Map 衔接（核心问题 F 的答案）

### 11.1 边界（Blueprint 已 Frozen）

```text
Company Map（组织中心）      → 公司怎么组成 / 业务怎么分布
Business Detail              → 这项业务怎么经营（Goal/Strategy/Workflow/Role/Capability/Team）
Business Workspace           → 这项业务现在怎么执行（专业 UI + 员工工作）
```

**点击 Business → Business Detail / Operating Model，绝不默认跳办公室**（Blueprint）。公司版图中的 Business 节点点击 → Business Detail；Detail 内有明确的 `进入办公室` 入口（UI Blueprint：Business Detail 主要动作含「进入办公室」）。

### 11.2 Business Operating Map 的分面表达（不用一张图全塞）

**研究结论：用「分面 + 联动高亮」，不用单图大杂烩。**

| 分面 | 表达 | 与 Company Map 关系 |
|---|---|---|
| Overview | Goal / Operating Strategy / Team / 关键指标摘要 | 点击 Business 后的第一屏 |
| Workflow Definition | 流程节点图（Node 顺序/Branch/Gate/Trigger） | 独立视图；**Workflow 与 Role 非 1:1** |
| Organization 分面 | Role Structure + Staffing + Employee Binding | 即 Role Detail 的聚合视图 |
| Required Capability | 岗位能力包需求 | 独立列表 |
| Responsibility Mapping | **联动高亮**：点 Workflow 节点 → 高亮负责该节点的 Role；点 Role → 高亮其责任流程节点 | 解决「Workflow 与 Role 不是 1:1」的关键交互 |

- **Swimlane（泳道）只作参考，不默认采用**：Curis 流程是「责任流转 + 交接」，不是「每人一条泳道」；泳道在 Role 多、流程复杂时反而难以阅读。
- 建议在 Workflow Definition 视图内用 **Role overlay（角色覆盖层）**：流程节点上用色块标注当前 Responsibility Holder（P1），点角色高亮其全部流程节点——这正是 Shared Authority「Process asks WHAT / Organization decides WHO」的可视化。
- **不要试图用一张图同时解决 Company Map + Workflow + Staffing**——这是本研究最明确的技术判断之一。

---

## 12. 技术方案比较（只形成建议，不写代码）

### 12.1 维度比较（核实 2026-08）

| 维度 | React Flow | AntV G6 | Cytoscape.js | D3 | BALKAN OrgChart | GoJS | yFiles |
|---|---|---|---|---|---|---|---|
| React/Next 适配 | ✅✅ 原生（节点=组件） | △ 需封装 | △ 需封装 | △ 全自建 | △ 需封装 | ◎ 官方支持 | △ 需封装 |
| License | MIT | MIT | MIT | MIT | Community MIT(受限)/商业 EULA | 商业 $4k–$12k | 商业 ~$11.9k 起 |
| Custom Node | ✅✅ 任意 React 组件 | ◎ Canvas 自定义成本高 | △ | ✅ 全自建 | ◎ 模板 | ◎ 模板 | ◎ 模板 |
| 大图性能 | ◎ 万级可（配合隐藏） | ◎ 强 | ✅✅ 强 | ◎ | ◎ | ✅✅ 强 | ✅✅ 最强 |
| Tree 布局 | ◎（dagre/elk 扩展） | ✅ 内置多布局 | △（dagre 扩展） | ✅ 自建 | ✅✅ 专为组织树 | ✅✅ 专为组织图 | ✅✅ 最强 |
| 分组容器（Compound） | ✅（parentId group） | ✅（Combo） | △（compound 节点） | ✅ 自建 | △ | ✅✅（Group） | ✅✅（Group） |
| 折叠/展开 | ✅ | ✅ | ✅ | 自建 | ✅✅ | ✅✅ | ✅✅ |
| Zoom/Pan | ✅✅ 内置 | ✅✅ 内置 | ✅ | 自建 | ✅ | ✅✅ | ✅✅ |
| 拖拽 | ✅✅ 内置 | ✅ 内置 | ✅ | 自建 | ✅ | ✅✅ | ✅✅ |
| Edge | ✅（含分组边） | ✅ | ✅ | 自建 | △（组织树边） | ✅✅ | ✅✅ |
| Search | 自接 | 自接 | 自接 | 自接 | ✅ 内置 | ✅ | ✅ |
| Minimap | ✅ 内置 | ✅ 内置 | △ | 自建 | ✅ | ✅ | ✅ |
| Accessibility | ✅ 支持 | △ | △ | 自建 | △ | ◎ | ◎ |
| Export | ✅（html-to-image） | ✅ | ✅ | ✅ | ✅ | ✅✅ | ✅✅ |
| 维护活跃度 | ✅✅ 极高 | ✅ 高 | ✅ 高 | ✅✅ 极高 | ✅ 高（商业驱动） | ✅ 稳定 | ✅ 稳定 |
| Bundle/复杂度 | 中 | 中 | 小 | 小（但全自建） | 小-中 | 中 | 大 |

### 12.2 推荐

| 排名 | 方案 | 理由 |
|---|---|---|
| **1. Curis 首选** | **React Flow（@xyflow/react）** | 与 Curis Next.js 前端原生契合（节点即 React 组件 → 富业务节点/员工卡片直接可做）；MIT 无商用限制；维护极活跃；内置 Zoom/Pan/Minimap/Controls/NodeToolbar；Group 节点支持 Department 容器；渐进披露 + 员工默认隐藏使大图性能风险可控。代价：默认 attribution（Pro 订阅可移除，商用桌面产品建议订阅）。 |
| **2. 第二选择** | **AntV G6** | MIT + 中文文档完善（Curis 中文团队友好）；Combo 分组、多布局、动画强；若未来需要更强布局算法（如复杂子图分析）可作为升级路径。代价：Canvas 渲染使富 DOM 节点成本高、React 集成需封装。 |
| **3. 不建议** | GoJS / yFiles（商业成本高，虽能力最强）；BALKAN OrgChart（商业闭源 EULA，Community 受限）；UNICEF react-org-chart（2020 年后停滞）；D3 原生（全自建，工期不可控）；Cytoscape.js / Sigma / vis-network（面向图分析/大图渲染，树+分组+富节点组合不匹配） | 见 §15 详细理由 |

> **技术结论**：公司版图的复杂度不在「渲染 500 节点」，而在「富业务节点 + 分组 + 渐进披露 + 状态表达」。React Flow 是唯一在这四点都原生契合的选择。

---

## 13. 三个候选方案

### Option A · 传统层级增强型（Enhanced Hierarchy Tree）

**信息结构**：Company → Department → Business → Role → Employee 的增强型树；节点做富卡片（状态色、计数、空岗标记）。

```text
Curis 公司
├─ 内容增长部
│  ├─ 小红书 · 运行中 · 3/4 岗
│  │  ├─ 文案岗 · 2人
│  │  │  ├─ 员工 A
│  │  │  └─ 员工 B
│  │  └─ 视觉岗 · 1人 · 空1
│  └─ 抖音 · 形成中
└─ 空间工程部
   └─ …
```

- **优点**：熟悉、实现简单、折叠机制天然、编辑入口直接、与 Blueprint 阅读顺序完全一致。
- **缺点**：仍像「组织树 + 业务字段」，版图感弱；业务组合分布不明显（看不到「国内/海外」这类并行业务分组一眼扫过）；Business 状态/成长信号要靠节点内字段，视觉层次容易变成列表。
- **适合 Curis 程度**：中（能实现，但使命表达打折）。
- **公司变大后**：靠折叠 + 搜索可撑住，但「一眼看懂公司长什么样」变弱。
- **编辑复杂度**：低。

### Option B · Business Portfolio / Company Map 型（业务组合版图）

**信息结构**：Department = 分组容器；Business = 一级卡片节点（状态色边 + Goal/Leader Hover + Role 计数 + 空岗/风险 Badge）；Role = chip；Employee = 默认隐藏，仅 Profile 承载。

```text
┌─ 内容增长部（12 岗 · 3 空 · 新增 1）──────────┐
│  ┌─ 国内内容 ─────────┐  ┌─ 海外内容 ──────┐  │
│  │ 小红书 ●运行 3/4岗 │  │ TikTok ○形成 0/2 │  │
│  │ 抖音   ●运行 2/2岗 │  │ YouTube ○形成   │  │
│  │ 公众号 ○暂停       │  └─────────────────┘  │
│  └────────────────────┘                       │
└───────────────────────────────────────────────┘
```

- **优点**：直接命中「一眼看懂业务版图」使命；业务组合/扩张/空岗/风险在结构上天然可见；员工隐藏使扩展性极好；与 Blueprint 第一视觉层完全对齐。
- **缺点**：Role/Employee 下钻路径弱（要靠 chip 展开 + Profile）；汇报关系完全不表达（但 Blueprint 本来就不要求默认展示）；一人多岗/跨业务关系需靠 Profile。
- **适合 Curis 程度**：高。
- **公司变大后**：Department 容器 + Focus Mode + Minimap 可撑住 50 Business。
- **编辑复杂度**：中（+ 在容器/节点 Hover，结构清晰）。

### Option C · Hybrid Company Map 型（推荐）

**信息结构**：默认 = Option B（业务版图）；Role 可在 Business 节点内就地展开（chip → 员工小节点）；「员工目录」为独立反查 Surface（Blueprint 已存在）；预留「组织视图」模式（Role 树/汇报关系）按需切换。

```text
默认（版图）：   Department 容器 → Business 卡片 → Role chip（计数/空岗）
下钻：          展开 Role → 员工小节点 → 点员工 → Profile
反查：          员工目录 Surface：Employee → Role → Business → Department
可选：          组织视图模式：Role 结构树（含一人多岗 chip 引用）
```

- **优点**：两全——业务版图（B 的使命表达）+ 组织下钻（A 的熟悉交互）+ 员工目录反查（Blueprint 已定）；编辑入口清晰；扩展性与 B 相同。
- **缺点**：实现量最大（两套视图形态 + 联动）；「组织视图」若做不好会变成模式负担（建议 v1 只做默认版图 + 就地展开，组织视图延后）。
- **适合 Curis 程度**：最高。
- **公司变大后**：与 B 相同 + 员工目录兜底所有反查。
- **编辑复杂度**：中（默认视图编辑 + 员工目录编辑两入口并存，需保证 Organization Truth 单一）。

### 推荐：Option C（Hybrid Company Map）

理由：
1. Blueprint 已同时定义「公司版图（默认）」与「员工目录（反查）」——Option C 是这两个 Surface 的天然实现，不是新发明。
2. 默认视图用 B 的业务版图语义，使命表达最强；Role/Employee 就地展开保留 A 的熟悉交互。
3. 员工默认隐藏 + 员工目录反查，让 500 Employee 规模可浏览。
4. 与「点击 Business → Business Detail，不跳 Workspace」「协作关系不默认平级展示」等 Frozen 边界全部兼容。

---

## 14. 最终推荐（合并方案）

**Curis 公司版图 = Option C（Hybrid Company Map），技术栈 = React Flow。**

落地要点（研究建议，待 CEO 确认后进入设计）：

1. **默认视图**：Department 容器（可折叠）→ Business 卡片（Name + 状态色边 + Leader 头像 + Role 计数 chip `·N岗` + 空岗 Badge + Risk Badge；Goal/Health/Latest Result 走 Hover）→ 展开 Role → 员工小节点。
2. **员工默认隐藏**：任何视图都不默认平铺全部员工；员工只在展开 Role、员工目录或搜索结果中出现。
3. **点击语义**：Business 卡片点击 → Business Detail / Operating Model；Role chip 点击 → Role Detail；员工点击 → Employee Profile；都不跳 Workspace（Detail 内有显式「进入办公室」）。
4. **成长表达**：`NEW`/变更 Badge + 时间窗摘要（本周新增 N 业务）+ 可选 Timeline Slider（ChartHop 参考）。
5. **编辑**：`+` 按钮 Hover 显现（Company→Dept、Dept→Business、Business→Role、Role→Employee）；空岗虚线节点 + 招募动作；右键菜单做移动/复制/暂停；结构变更全部确认（Organization Truth 不可被误操作污染）。
6. **大公司**：Focus Mode + Breadcrumb + 全局 Search + Filter（空岗/风险/最近变化）+ Minimap + Zoom-LOD + Lazy loading。
7. **员工目录**（Blueprint 已定）：反查 Employee → Role → Business → Department；一人多岗在 Profile 完整展示。
8. **技术**：React Flow；Business 节点 = 自定义 React 组件；Department = group node；分层加载；attribution 用 Pro 订阅移除（商业桌面产品）。

---

## 15. 明确不推荐什么（NOT Recommended）

| 不推荐 | 原因 |
|---|---|
| 传统 HR Org Chart 作为默认主视图 | 只表达 WHO 汇报给谁，没有业务版图感；Blueprint 已明确排除 |
| 全自由 Network Graph（一人多岗/跨业务画交叉边） | 50 Business / 500 Employee 时边爆炸；与「协作关系不默认平级展示」冲突 |
| 数据大屏 / Dashboard 化（节点内嵌图表、常驻动画） | 「不变成 Dashboard」是硬约束；成长用徽章/计数/时间窗，不用图表 |
| Radial / 放射布局 | 中文标签阅读差；Curis 无中心枢纽语义 |
| 力导向 Cluster 作为默认布局 | 布局不稳定，CEO 无法形成空间记忆（每次打开公司「长不一样」） |
| 用节点大小表达业务规模 | 误导「谁大谁重要」；用计数/徽章即可 |
| Swimlane 作为 Workflow 默认表达 | Role 多、流程复杂时阅读差；用 Role overlay 联动高亮 |
| 一张图同时表达 Company Map + Workflow + Staffing | 必然变成大杂烩；分面 + 联动高亮 |
| GoJS / yFiles | 能力最强但商业授权成本高（$4k–$12k+），Curis Desktop 单产品不需要 |
| BALKAN OrgChart（商业版） | 闭源 EULA；Community 版功能受限；组织树向但缺自由扩展 |
| UNICEF react-org-chart | 2020 年后停止维护；仅作参考 |
| D3 原生实现 | 低层全自建，工期不可控；除非团队有专门可视化工程师 |
| Cytoscape.js / Sigma / vis-network | 面向图分析/大图渲染，树+分组+富 DOM 节点组合不匹配 |

---

## 16. 仍需 CEO 决定的问题

1. **Business「Health」的定义**：健康度由谁定义、用什么事实构成（结果时效？风险数？成本？Domain 定义？）——公司版图节点上的 Health 指标不能是拍脑袋字段。
2. **Timeline Slider（成长回放）**：是否进入 v1？还是 v1 只做 `NEW` 徽章 + 时间窗摘要？（ChartHop 参考，工程成本中等）
3. **中间分组（国内/海外）**：是否允许 Department 与 Business 之间存在「中间分组」层级？它算 Sub-department 还是纯展示分组？（Master Map 部门触发逻辑是否适用于中间分组）
4. **一人多岗的默认展示**：员工只在主 Role 下出现、其余用 chip 引用——是否接受？（接受则避免交叉边）
5. **编辑方式**：是否允许 Drag & Drop 移动 Business 跨 Department？（建议允许但需确认弹窗；也可 v1 只做右键菜单）
6. **组织视图模式**：Option C 中的「组织视图」（Role 树/汇报关系）是否延后到 v2？（建议延后）
7. **Company Map 的默认展开级别**：默认「Department→Business」两级全展开，还是默认折叠到 Department 容器？（建议默认展开到 Business，小型公司一眼看完；大型自动降级为容器态）
8. **公司版图的导出/分享**：是否支持导出图片/分享链接（供 CEO 复盘或汇报）？（建议 v1 支持导出 PNG）
9. **Business 状态与 Risk 的事实来源**：版图上所有状态/Badge 必须来自 Business Runtime 真实事实（不是手动填写）——需要确认哪些 Runtime 事实驱动哪些状态（对齐「禁止编造」纪律）。
10. **Business Duplicate 的来源标识**：新复制 Business 是否需要永久保留「由 X 复制」关系？（建议 Hover 提示 + 非永久边，避免版图被复制关系连线污染）

---

## 附录 A · 高价值公开参考（供后续 Design Agent 研究）

| 参考 | 链接 | 截图建议 |
|---|---|---|
| React Flow 官网/文档 | https://reactflow.dev | 截图：group node + minimap + custom node 示例 |
| React Flow GitHub | https://github.com/xyflow/xyflow | 维护活跃度证据 |
| AntV G6 官网 | https://g6.antv.antgroup.com | 截图：combo 分组 + 树布局示例 |
| ChartHop（成长回放/数据叠加） | https://www.charthop.com | 截图：Org Chart + timeline slider + 节点数据点着色（需登录则截图其 marketing 页） |
| ChartHop 功能页（People Analytics） | https://www.charthop.com/landing-pages/people-analytics | 截图：多视图并存（org chart/data sheet/map） |
| Rippling「employee graph」概念 | https://www-b.rippling.com/blog/your-idp-fully-informed | 组织图作为数据主干的思想证据 |
| Business Capability Map 定义 | https://www.brimco.io/terms/business-capability-map | 「what vs who」的权威区分 |
| Capability Model vs Org Chart | https://capstera.com/insights/why-capability-models-outlast-org-charts | 「能力模型比组织图长寿」论据 |
| TOGAF Business Capabilities Guide（PDF） | https://governance.foundation/assets/frameworks/togaf/g189%20-%20Business%20Capbility.pdf | 「不要把 Org Chart 转置成 Capability Map」警告 |
| Team Topologies | https://teamtopologies.com | 团队形态/交互模式参考 |
| UNICEF react-org-chart | https://github.com/unicef/react-org-chart | 仅设计参考（已停滞） |
| BALKAN OrgChart JS | https://balkan.app/OrgChartJS | 组织树交互参考（商用注意） |
| GoJS 定价页 | https://gojs.net/4.0.2/pricing | 商用成本证据 |
| yFiles 定价页 | https://www.yfiles.com/pricing | 商用成本证据 |

---

*本文档为研究建议；已消费的产品/交互结论写入 Current Authority，本文不反向定义 Current。*  
*CURIS COMPANY MAP / ORGANIZATION GRAPH RESEARCH — STOP FOR CEO REVIEW*
