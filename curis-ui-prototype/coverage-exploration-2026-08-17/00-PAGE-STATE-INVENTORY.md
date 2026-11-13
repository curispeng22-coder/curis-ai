# Curis Complete Product UI Coverage — Page/State Inventory

> 生成时间：2026-08-17
> 依据：Product Blueprint 5.1 · UI Blueprint · Frozen Workspace Shell Contract · Company OS Shared Authority · Frozen Visual Spec
> 性质：Coverage First / Visual Exploration 的页面清单，非 Production Authority

---

## 覆盖原则

1. **不新建 Blueprint 外产品系统**：所有页面必须能在当前 Product Blueprint / UI Blueprint 中找到依据。
2. **Shared Pattern 直接复用**：Navigation · 四 Pane Shell · Main Composition · Context/Utility · Employee Row · UI Status · Conversation · Composer · Employee Detail · Result→Utility 均按 Frozen Shell Contract 执行。
3. **Domain Business Surface 是探索重点**：每个 Workspace/页面主要探索「业务展示区放什么、Context 需要什么资料、Utility 需要什么专业视图」。
4. **状态必须存在**：每个一级区域至少包含 Normal / Empty / Loading / Error / Needs CEO 等关键状态之一。
5. **视觉方向**：安静、信息密集、低表面复杂度、高功能密度、克制 Card/Pill、以排版/留白/字重/灰度建立层级。

---

## 一级区域与页面总览

| 编号 | 一级区域 | 页面文件 | 核心覆盖目标 |
|------|---------|---------|-------------|
| A | 首页 / CEO 工作台 | `01-ceo-desk.html` | 简报/今日变化、问题处理/待决定、当前运行、结果复盘、CEO Assistant、首次创建、空态 |
| B | 业务空间 | `02-business-space.html` | 业务总览、业务详情、Workspace 入口、Workspace Engineering/空间工程、新建业务 |
| C | 组织中心 | `03-org-center.html` | 组织总览、部门/团队、员工列表、员工详情、汇报关系、组织建议 |
| D | 人才市场 | `04-talent-market.html` | 专家/Skill/Connector 浏览、专家详情、招募流程、已安装状态 |
| E | 资料库 | `05-library.html` | 资料首页、本地/外部/公司产生、文件阅读、搜索结果、权限引用 |
| F | 会议 | `06-meeting.html` | 会议首页、Company/Workspace Meeting 工作面、Proposal/Decision |
| G | 设置（头像菜单） | `07-settings.html` | 个人/公司/AI 能力/Connector/权限/运行成本/通知帮助 |
| H | RD Workspace | `08-rd-workspace.html` | 研发办公室入口、多 Employee Workstation、Context 文件树、Utility Code/Diff/Preview |
| I | Content Growth / XHS | `09-xhs-workspace.html` | 小红书运营办公室、日历/内容/数据/自动化、创作/审核 Presence |
| J | 全局能力 | `10-global-search.html` | 全局对象搜索、搜索结果、Recent |
| K | 重要状态集 | `11-states.html` | Empty / Loading / Failure / Needs CEO / Permission / Offline / 首次使用 |

---

## A. 首页 / CEO 工作台 (`01-ceo-desk.html`)

### A1 公司简报 / 今日变化（Normal）
- 顶部：页面标题「首页」+ Breadcrumb「Curis / 首页」+ T2/T3（默认收起）+ 搜索入口
- 主区：
  - 公司状态卡：公司名、当前业务数、员工数、今日待处理数
  - 今日变化列表（按影响排序）：业务/员工/结果/异常/待决定，每项含来源、时间、影响对象、下一步
  - CEO Assistant 入口：可展开 compact composer
- Context（默认收起，可展开）：最近工作 / 业务列表 / 待处理筛选
- Utility（点击变化/结果时展开）：变化详情、来源、负责人、版本、下一步

### A2 问题处理 / 待决定事项
- 主区：待处理队列，每项显示事实/影响/负责人/用户动作/完成后去向
- 包含 Decision Packet（Layer 0 Banner + Layer 1 Plain Package + Layer 2 Result Reference）
- 动作：批准/驳回/暂缓/查看方案/接管/恢复

### A3 当前运行工作
- 主区：运行中 / 等待用户 / 失败 / 已完成 工作卡片
- 每张卡片：业务/Workspace/员工/当前责任/下一步/预期结果

### A4 结果详情 / 验收 / 复盘
- 主区：结果本体、版本对比、外部反馈、目标对照、结论
- Utility：来源链、引用、权限、建议改动

### A5 首次创建公司状态
- 主区：CEO Assistant 对话式引导，最少必要追问，业务/Workspace 预览
- Utility：预览会形成什么、谁负责、能力缺口、人工回退

### A6 空态 / 等待 / 阻塞
- 尚无公司、公司已建但无业务、无运行工作、无结果等状态

---

## B. 业务空间 (`02-business-space.html`)

### B1 业务空间总览
- 主区：业务卡片列表，每张卡含价值/Workspace 数/负责人/最近结果/风险/下一检查点
- Context：业务筛选/分类

### B2 业务详情
- 主区：业务目标、价值、Workspace 列表、负责人、结果、风险、下一检查点
- Utility：业务设置/影响分析

### B3 Workspace 搭建预览 / 团队装配
- 主区：模板选择 → 办公室预览 → 团队 → 能力检查 → 启动
- Utility：影响预览/待修改版本

### B4 Workspace Engineering / 空间工程部
- 主区：空间工程办公室入口，显示「可委托建设新业务」能力
- 工作区：空间工程 Leader + 研究/设计/实施/Quality 员工
- Context：委托需求/历史项目
- Utility：方案预览/影响分析

### B5 新建业务 / 新建 Workspace
- 主区：简短表单/对话式创建

---

## C. 组织中心 (`03-org-center.html`)

### C1 组织总览
- 主区：三视图 Tab（组织结构 / 协作关系 / 员工）
- 组织结构：CEO → Assistant → 部门/业务 → 员工
- 协作关系：Employee ↔ Workspace ↔ Business 网络
- 员工列表：头像/姓名/岗位/当前责任/状态

### C2 部门浏览与详情
- 主区：部门卡（责任/成员/共享能力/影响业务）
- Utility：部门设置/历史

### C3 员工列表与快速查看
- 主区：员工行列表（复用 Employee Row Pattern）
- 点击头像/姓名 → Utility Employee Detail（六字段）
- 点击行其他区域 → Focus View / 进入 Workspace Workstation

### C4 员工能力设置
- Utility/Focu s：模型/Agent/Skill/Connector/权限/资料

### C5 招聘入口 / Workspace 组队
- 主区：从人才市场招募入口 + 从已有员工组队

---

## D. 人才市场 (`04-talent-market.html`)

### D1 人才市场首页
- 主区：Tab [专家] [技能] [连接器]；搜索/分类/推荐/已安装
- 专家卡：职业方向/擅长/示例/来源
- Skill 卡：适用岗位/依赖/版本
- Connector 卡：连接范围/风险

### D2 专家详情
- Focus View：身份/擅长/能力/案例/来源/招募 CTA

### D3 招募流程
- Focus View 多步：专家 → 公司身份/岗位/责任 → 业务/Workspace → 能力/资料/授权 → 确认

### D4 Skill / Connector 详情与安装
- Focus View：说明/依赖/许可/安装/授权

### D5 已招募 / 已安装状态
- 主区：已招募专家、已安装 Skill/Connector 列表及健康状态

---

## E. 资料库 (`05-library.html`)

### E1 资料库首页
- Context Sidebar（默认展开）：最近 / 本地 / 外部资料库 / 公司产生 / 文件夹
- 主区：最近访问/推荐/待索引项

### E2 文件 / 资料阅读
- 主区：资料正文
- Utility：来源/权限/引用/使用关系

### E3 搜索结果
- 主区：按类型分组结果
- Context：搜索范围/筛选

### E4 外部连接 / 权限
- Utility/Focus：连接设置、授权状态、同步范围

### E5 空态
- 无资料、无连接、搜索无结果

---

## F. 会议 (`06-meeting.html`)

### F1 会议首页
- 主区：即将开始 / 需要准备 / 历史会议

### F2 创建会议
- 主区：会议名称/来源/议题/参与员工/状态

### F3 Company Meeting / Workspace Meeting 工作面
- 主区：顶部会议信息；中央多员工 Conversation
- Context：议程/资料
- Utility：Proposal 详情/Decision/Action

### F4 Proposal / Decision
- 主区/Utility：支持/反对观点、Evidence、影响、未知、风险
- CEO 动作：批准/拒绝/修改/延后

---

## G. 设置 (`07-settings.html`)

> 从左下角头像菜单进入，不是一级导航

### G1 设置 Workspace 首页
- 主区：设置分类列表（个人/公司/AI 与能力/数据与应用）

### G2 个人偏好
- 主区：姓名/头像/语言/主题/通知/快捷键

### G3 公司设置
- 主区：公司资料/目标/规则

### G4 AI 与能力
- 主区：Provider/模型/Base URL/API Key/可用模型/测试/默认模型
- Connector 管理：已安装/授权/账号/权限/健康
- Skill / Agent / Tool 列表

### G5 权限与数据
- 主区：数据范围/外部动作确认/隐私/导出/本地数据管理

### G6 运行与成本
- 主区：连接健康/能力容量/成本预算/后台运行状态/诊断

---

## H. RD Workspace (`08-rd-workspace.html`)

### H1 研发办公室入口 / Domain Business Surface
- 主区：项目状态、目标、当前 Sprint/Cycle、关键结果、Blocker、Needs CEO
- 业务展示区：项目/目标/进度/结果

### H2 Shared Work Area / 多 Employee Workstation
- 产品经理、架构师、开发工程师、QA、Review 员工行
- 开发工程师工作中 → 默认展开 Conversation
- Conversation 内：自然消息 + 轻量状态行 + Result Reference（Diff/测试结果）

### H3 Context Sidebar
- 当前 Project/Workspace、Responsibility、相关文件/目录、Recent Work/Object

### H4 Utility Surface
- Code / Source、Diff / Changes、Preview / Result
- 显示所属责任 + 回到 Conversation 锚点

### H5 Needs CEO / Decision
- 顶部 Decision Banner（DB 变更/发布上线等不可逆操作）

---

## I. Content Growth / XHS Workspace (`09-xhs-workspace.html`)

### I1 小红书运营办公室入口
- 主区：总览/发布日历/内容/数据/自动化 Tab
- 今日待发、待审核、当前内容、近期表现、异常

### I2 内容生产工作区
- 员工行：运营/研究/策划/文案/视觉/数据分析
- Employee Presence：Note 卡头像 + 创作/审核 Presence

### I3 Context Sidebar
- 选题库（信号/素材）、内容日历、历史发布

### I4 Utility Surface
- 图文预览、图片、发布预览、数据详情、任务详情

### I5 发布后 Analytics
- System Activity：自动数据回收（Current Executor=none）

---

## J. 全局能力 (`10-global-search.html`)

### J1 全局搜索入口
- Navigation Pane Header Search icon 展开独立 Search Surface
- 空查询 → Recent
- 有查询 → 按对象类型分组：Business / Workspace / Employee / Business Object / Knowledge / Result / Meeting / Capability

### J2 搜索结果
- 图标 + 标题 + 组织/业务上下文 + 类型标签
- 点击直达对象/Workspace

---

## K. 重要状态集 (`11-states.html`)

集中展示跨页面关键状态，确保每个状态都有可浏览示例：

| 状态 | 示例场景 |
|------|---------|
| Empty | 尚无公司 / 无业务 / 无员工 / 无资料 / 无会议 |
| Loading | 数据加载中 / 员工正在初始化 |
| Failure | 任务失败 / 连接失败 / 模型不可用 / 权限拒绝 |
| Needs CEO | Decision Banner / 员工 needs_ceo / 能力缺口 |
| Permission | 请求 Computer Access / Connector 授权 |
| First-use | 首次创建公司 / 首次进入 Workspace |
| Offline/Unknown | 外部平台未连接 / 数据待回填 |
| Success/Completed | 结果已回收 / 任务完成 / 发布成功 |

---

## Shared Pattern 复用矩阵

| Pattern | 应用页面 | 说明 |
|---------|---------|------|
| Navigation Pane + 六区 | 全部 | 固定顺序，不增不减 |
| Context Surface | 资料库、RD、XHS、会议 | 按需展开，默认收起 |
| Utility Surface | 全部 | 点击对象/引用展开 |
| Employee Row | CEO 工作台、RD、XHS、组织中心 | 两行结构，点头像→Detail |
| Employee UI Status | 含员工的页面 | 空闲/工作中·<desc>/阻塞·<cause> |
| Conversation Surface | RD、XHS、会议、员工工作面 | 居中/Bounded/可拖拽 |
| Shared Composer Shell | 员工工作面、会议 | 语义槽位固定 |
| Result Reference | RD、XHS、会议 | 轻量引用→Utility |
| Needs CEO / Decision | CEO 工作台、RD、XHS、会议 | Banner + 三按钮 |
| CEO Decision Package | 需决策页面 | 8 要素语义 + Provenance |
| Employee Detail | 组织中心、各 Workspace | Utility 六字段 |
| Employee Presence | XHS、RD（可选） | 业务对象上贴头像 |
| System Activity | XHS Analytics | 非员工运行时 |

---

## DESIGN GAP（发现后记录，不自行修改 Frozen）

1. **Navigation 子项渲染**：Workspace 实例（如「小红书运营办公室」）在 Primary Nav 中的具体呈现方式（缩进/图标/active 态/owner 头像）Shell 未冻结（Shell §6 Open Question #7）。
2. **Utility Syntax Tokens**：代码高亮子令牌 `--ui-syntax-*` 未冻结，RD Utility 代码块用临时色值。
3. **Mobile Adaptive Surface**：<640px 转 Overlay 的具体交互未在产品中实例化。
4. **Workspace Studio 视觉**：Studio 的「当前运行版本 vs 待修改版本」具体视觉形态 Blueprint 有语义但无像素规范。

## PRODUCT DEFINITION GAP（标记但不脑补）

1. **抖音/TikTok Workspace**：Blueprint 定义了结构，但无专项 Design Brief，本轮只做轻量占位页面。
2. **财务/日历/成果库**：旧 UI Spec 中有页面，但 Blueprint 5.1 未明确为一级入口；本轮按「设置/资料库子能力」处理。
3. **具体 Provider 适配**：Codex/Claude Code/Coze 等 Provider 原生交互细节未经验证，Composer 中用通用占位。
4. **Agent Computer Access 运行时 UI**：ADR-0046 冻结权限语义，但具体 Computer Access 设置/请求界面未单独定义；本轮仅在 Composer 中显入口。

---

*Inventory by Design Engine Team Lead · 2026-08-17*
