# Curis 完整产品开发路线与 EvoFlow 借鉴清单

Status: Review  
日期：2026-08-10  
性质：产品规划与开发前置清单；本文件不授权业务代码修改。  
产品基线：[Curis Product Blueprint 5.0](../01_Product/Curis_Product_Blueprint.html)

## 0. 这份路线解决什么问题

EvoFlow 已经证明：AI 员工、Agent、Skill、MCP、会议、自动化、知识和成本可以被做成用户看得懂、点得动、能够持续使用的产品。

Curis 已经拥有更高层的经营内核：

~~~
Company → Business → Outcome → Commitment → Evidence
→ Acceptance → Decision → Company Change
~~~

当前问题不是缺少更多概念，而是：

- 能力没有被包装成 CEO 可用的供给系统；
- AI 员工、岗位、模型和 Skill 没有形成连续装配路径；
- Workspace Studio 尚未真正连接能力和岗位；
- 组织页、业务页、成果页存在旧事实或示例数据；
- Meeting、自动化、成本健康和日历没有形成完整用户入口；
- UI 已有壳层，但页面仍有“后台 / 项目列表 / 规划中占位”的残留。

本路线的目标是：

> 用 EvoFlow 级别的清晰度和便捷性，承载 Curis 的 CEO 经营闭环，而不是把 Curis 改造成 Agent Center 或 Workflow 平台。

## 1. 当前产品终局

### 1.1 Curis 是什么

Curis 首先是一款完整 Desktop App，其核心用途是帮助一位 CEO：

~~~
创建公司
→ 形成第一业务
→ 配置模型 / Skill / Tool / 知识
→ 组建 AI 团队
→ 搭建业务 Workspace
→ 运行和交接
→ 获得客户 / 平台 / CEO 验收结果
→ 做出决策
→ 调整能力、组织和业务
→ 持续经营和扩展
~~~

Local Desktop 只决定数据和连接在本机运行，不减少 CEO 必需能力。这里必须区分两件事：

- **产品完整性**：单机版也必须具备模型、Skill、Tool / Connector、知识、权限、成本、AI 员工、Workspace、结果和决策所需的完整使用面；CEO 必须能从添加能力开始，把它验证、分配给员工并在真实业务中使用。
- **交付顺序**：这些能力可以分阶段实现，但不能因为当前只有一个真实 CEO、暂不商业化，就从产品形态中删除或改成静态占位。

可以暂缓的是 Platform / Admin 的多租户、计费、模板市场和云端运营包装，不是本地公司的能力供给链。

### 1.2 完整 App 区域

| 区域 | 真实职责 | 关键页面 |
| --- | --- | --- |
| 首次进入 | 让 CEO 从空白建立公司 | 公司创办、Assistant 访谈、公司确认 |
| 今日经营 | CEO 每天进入和返回的位置 | CEO Desk、经营日、事项、时间线 |
| 经营 | 判断公司是否健康和方向是否需要调整 | 公司脉搏、风险、机会、投入产出 |
| 业务 | 管理正在经营的业务版图 | 业务版图、业务详情、新业务、阶段决策 |
| AI 团队 | 管理责任、关系、状态、容量和结果 | 组织图、员工、岗位、健康度 |
| 能力中心 | 管理模型、Skill、Tool、连接器和知识供给 | 资源目录、详情、安装、验证、分配 |
| Workspace | 业务办公室和装修过程 | Portal、Studio、研发 / 小红书 / 抖音办公室 |
| 会议与决策 | 形成共识、决议和承诺 | Meeting Workbench、Decision Room、Evidence Review |
| 公司资产 | 保存可复用的结果和知识 | 成果、知识、记忆、成本、日历 |
| 设置 | 管理本地 App 和身份 | CEO、连接、本地数据、主题、备份 |

## 2. EvoFlow 可借鉴机制转译表

| EvoFlow 机制 | Curis 吸收方式 | UI 落点 | 不照搬的部分 |
| --- | --- | --- | --- |
| Agent 卡片 | 统一 AI Workforce Card Contract | AI 团队、员工详情、Workspace 团队带 | 不把 Agent 作为顶层产品 |
| Agent / Skill / Connector 切换 | 统一能力资源目录 | 能力中心 Tab 与搜索 | 不做无审查的插件货架 |
| 一键安装 | 对话式能力发现、权限审查、模拟、批准、回滚 | Assistant + 能力中心安装抽屉 | 不默认 Full Auto |
| AI 员工配置 | 岗位、责任、汇报、预算、排班、交接、日报、健康 | 员工详情、组织图、健康页 | 不默认 Unlimited Budget |
| 组织树 | CEO → Assistant → 专业 AI → Workspace AI | AI Team 组织地图 | 关系变更要有影响预览和版本 |
| 员工健康 | 成本、结果、返工、空转、审批超时、过载 | CEO Desk 摘要、AI Team Health | 不做孤立 Token 监控 |
| Workflow/App | 完成一次业务后沉淀 Workspace Blueprint | Workspace Studio 高级编辑 | 不新增顶层 Workflow 平台 |
| 自然语言自动化 | 经营节奏、事件触发、下一次运行预览 | Assistant、日历、Workspace 设置 | 不要求 CEO 学 Cron |
| Global Assistant | Workbench / Conversation / Meeting 三态共享运行体 | 浮层 + CEO Desk | 不做第三栏，不遮挡主操作 |
| 多 AI 会议 | 轮次、点名、参与者、状态和聊天室阅读感 | Meeting Workbench | 讨论不能自动成为 Decision |
| 模型 / 连接 / 安全设置 | 本地模型、Skill、Tool、数据范围、权限和诊断 | 能力中心、设置 | 不因缺模型阻断公司设计草案 |
| 资产与知识 | 结果、来源、记忆和决策引用 | 公司资产、Evidence Review | 不做脱离业务的文档仓库 |

## 3. 统一 UI 布局语言

### 3.1 固定 App Shell

~~~
左侧：Company OS 导航（稳定、低噪）
顶部：当前公司 / 页面上下文 / 主题 / Assistant
中间：当前经营任务
右侧：按需 Context Drawer，不固定占位
全局：可收纳 Assistant 浮层
~~~

固定导航：

1. 今日经营
2. 经营
3. 业务版图
4. AI 团队
5. 能力中心
6. 工作空间
7. 公司资产
8. 经营工具
9. 设置 / 帮助

导航按 CEO 问题组织，不按数据库表组织。

### 3.2 统一实体卡片

所有 AI 员工、岗位、能力、Workspace 卡片使用同一信息层级：

1. 身份：图标 / 名称 / 一句话价值
2. 当前状态：可用、工作中、等待、阻塞、草案、待批准
3. 责任：负责什么结果
4. 供给：模型、Skill、Tool、知识
5. 健康：最近活动、结果、成本、容量
6. 主动作：查看、配置、委派、批准、暂停、交接

### 3.3 统一详情交互

~~~
列表 / 版图
→ 点击实体
→ 右侧抽屉或详情页
→ 查看责任与上下文
→ 执行一个主动作
→ 看到影响预览
→ 确认或撤销
→ 回到原位置
~~~

### 3.4 统一状态体验

每个页面必须有：

- 空态：说明尚未建立和下一步；
- 草案：允许继续设计，不冒充已运行；
- 待授权：说明缺少什么连接 / 权限；
- 运行中：显示负责人、阶段和预计回报；
- 等待 CEO：显示为什么需要 CEO；
- 阻塞 / 失败：显示原因、责任和最小恢复方式；
- 未知 / 冲突 / 过期：不显示虚假健康；
- 已验收：显示证据和可复用位置。

### 3.5 页面级布局契约

页面先按 CEO 要解决的问题组织，再决定组件。以下是设计和开发必须共同遵守的首屏骨架：

| 页面 | 首屏必须出现 | 主动作 | 不能退化成 |
| --- | --- | --- | --- |
| 首次进入 | 空白但不空旷的公司空间、Assistant 欢迎、建立公司进度 | 表达意图并确认公司草案 | 空白后台或复杂设置表单 |
| CEO Desk | Assistant 汇报、公司变化、待决策、异常、AI 团队状态 | 处理一件经营事项 | 指标墙或任务列表首页 |
| 业务版图 | 业务卡片、外部结果、阶段、投入、风险、下一决定 | 进入业务或创建新业务 | 无结果的项目列表 |
| 能力中心 | Model / Skill / Tool / Connector / Knowledge 资源、连接状态、供给缺口 | 添加、验证、绑定或替换 | 只展示 Agent 的插件货架 |
| AI 团队 | 组织关系、员工卡片、责任、容量、健康 | 创建岗位、配置、批准或调整员工 | 平级头像墙或技术日志 |
| Workspace | 办公室身份、团队状态、周期、执行、证据、结果 | 验收、交接、调整或进入 Studio | 看板、旧任务表或彩色控制台 |
| Meeting Workbench | 议题、参与者、自然讨论流、事实 / 观点标签、决策草案 | 批准、修改或拒绝 Decision Proposal | 只有聊天记录或自动生效结论 |
| 公司资产 | 成果、证据、知识、引用、成本和日历上下文 | 复用、引用或回写决策 | 脱离业务的文档仓库 |

这张表是 UI 设计和前端实现的共同入口；组件、数据接口和路由都必须服务于对应的主动作。

## 4. 完整业务链路清单

### Flow A：首次创建公司

- [ ] 空白但不空旷的首次空间
- [ ] Assistant 自我介绍与能力说明
- [ ] CEO 表达经营意图
- [ ] Assistant 形成公司、业务和结果草案
- [ ] CEO 修改 / 确认
- [ ] Company 与 Assistant 建立
- [ ] 第一业务创建
- [ ] 最小 AI 团队和能力方案生成
- [ ] 进入 Workspace Studio
- [ ] 返回 CEO Desk 并显示下一步

### Flow B：配置模型、Skill、Tool

- [ ] 添加多个模型提供商和模型
- [ ] 凭证引用不明文落盘
- [ ] 连接测试、默认模型、备用模型
- [ ] 接入 Skill / Tool / Connector
- [ ] 显示来源、版本、权限、数据范围、副作用和成本
- [ ] 安全扫描 / 许可检查 / 连接诊断
- [ ] 形成可调用能力
- [ ] 分配给岗位、AI 员工和 Workspace
- [ ] 运行测试
- [ ] 失败、替换、停用和回滚
- [ ] 记录成本和调用历史

**单机版完成判定：** CEO 至少可以添加两种模型或模型配置、接入并停用一个 Skill、完成一次连接 / 能力测试、把能力绑定给 AI 员工和 Workspace，并在一次真实运行后看到调用结果、错误、成本和可撤销路径。只有展示目录而不能完成这条链，不算能力中心完成。

### Flow C：雇佣 / 配置 AI 员工

- [ ] CEO 或 Assistant 提出岗位
- [ ] 说明结果、责任、输入、输出和验收
- [ ] 推荐模型、Skill、Tool、知识和 Workspace
- [ ] 预览预算、权限、风险和影响
- [ ] 保存草案
- [ ] 隔离 Simulation
- [ ] CEO 批准
- [ ] 员工上岗
- [ ] 排班 / 节奏 / 预算 / 超限策略
- [ ] 工作、交接、日报、审批和验收
- [ ] 健康、成本、容量和绩效
- [ ] 暂停、替换、交接和归档

### Flow D：创建 / 装修 Workspace

- [ ] 选择业务模板或从空白开始
- [ ] 描述业务目标和外部结果
- [ ] 设计阶段和阶段 Owner
- [ ] 安排岗位、汇报和交接
- [ ] 选择模型、Skill、Tool、知识和数据窗口
- [ ] 配置节奏、验收、失败和人工备用
- [ ] 检查能力供给
- [ ] 试运行和失败模拟
- [ ] CEO 确认
- [ ] 生成运行版本
- [ ] 进入业务办公室
- [ ] 版本变更使旧运行方案可追溯并可回滚

### Flow E：运行三条业务

#### 研发工作台

- [ ] 接收“完善 Curis”任务
- [ ] 产品 / 技术方案
- [ ] 工程实现
- [ ] 构建 / 测试 / 浏览器验证
- [ ] CEO 验收或退回
- [ ] 真实成果归档
- [ ] 下一周期和能力改进

#### 小红书运营工作台

- [ ] 内容方向和用户目标
- [ ] 内容版本和平台差异
- [ ] CEO 审核
- [ ] 授权发布或手动发布
- [ ] 评论 / 私信 / 互动回流
- [ ] 播放、点赞、收藏、涨粉、线索或成交反馈
- [ ] 复盘和下一轮内容策略

#### 抖音 / TikTok 运营工作台

- [ ] 内容目标和视频版本
- [ ] 脚本、剪辑、发布责任
- [ ] CEO 审核和授权
- [ ] 平台回执
- [ ] 播放、完播、互动、涨粉、订单和成交反馈
- [ ] 复盘、调整和下一周期

### Flow F：会议与决策

- [ ] Assistant 识别需要会议的事项
- [ ] 会前准备背景、事实、未知、议题和参与者
- [ ] 会议中使用自然讨论流
- [ ] 事实 / 观点 / 建议 / 异议轻量标记
- [ ] AI 员工轮次、点名和状态
- [ ] 形成 Decision Proposal
- [ ] CEO 批准 / 修改 / 拒绝 / 延后
- [ ] 生成 Commitment、Owner、Due Date、Evidence Requirement
- [ ] 回写 Workspace
- [ ] Assistant 跟进和提醒

### Flow G：持续经营与自动化

- [ ] CEO Desk 每日汇报
- [ ] 经营节奏与日历
- [ ] 事件触发、周期触发和风险阈值
- [ ] 下一次运行预览
- [ ] 输入数据、责任人和预计成本
- [ ] 运行失败和恢复
- [ ] 成本健康和结果健康
- [ ] 业务扩大、暂停、退出和资源释放
- [ ] 新业务复制和 Workspace 扩展

## 5. 开发顺序与依赖

### Phase 0：产品与事实收束（前置，不写业务代码）

目标：避免三套产品再次混入。

- [ ] Blueprint 5.0 与 EvoFlow 转译章节确认
- [ ] UI 现状审计报告确认
- [ ] 当前路由和导航唯一化
- [ ] 清理 / 隔离 fixture、示例报告和旧组织事实
- [ ] 明确 Runtime、legacy Project/Task、prototype 的事实级别
- [ ] 形成唯一前端、唯一 Desktop 启动和唯一数据入口
- [ ] 建立本路线对应的 Issue 编号和 Allowed Files

依赖：无。  
完成条件：CEO 确认产品地图、导航和阶段顺序。

### Phase 1：App Shell + CEO Assistant + CEO Desk

目标：让 CEO 每天有一个可靠的进入和返回位置。

- [ ] Assistant Identity / 首位员工配置
- [ ] CEO Desk 今日简报、待决策、异常、机会、时间线
- [ ] Assistant Workbench / Conversation / Meeting 三态
- [ ] 当前页面上下文感知
- [ ] Assistant 主动事项、解释“为什么现在”
- [ ] 事项可转 Decision / Commitment / Workspace
- [ ] 共享浮层安全边距、避让和收纳
- [ ] 无数据时下一步行动，而不是空指标

依赖：Phase 0、Company Runtime 基础、Assistant Runtime。

验收：从 App 打开开始，CEO 能理解公司状态，并能进入一个明确经营动作。

### Phase 2：Capability Center 完整供给链

目标：让 CEO 能自己把模型和 Skill 变成可用能力。

- [ ] 模型提供商 / 模型多条记录
- [ ] 凭证引用、连接测试、默认 / 备用模型
- [ ] Skill、Tool、Connector、Knowledge 统一资源目录
- [ ] 详情：来源、版本、许可、权限、数据范围、副作用、成本
- [ ] 安装 / 接入前审查
- [ ] 运行测试和诊断
- [ ] 角色 / 员工 / Workspace 分配
- [ ] 启停、替换、回滚
- [ ] 调用、成本、失败和容量观察

依赖：Phase 1 的 Assistant 指引、现有 Capability Registry。

验收：CEO 从添加模型开始，能把它分配给员工并通过一次真实能力测试。

### Phase 3：AI Team 与组织运行

目标：让 AI 员工成为可管理的责任主体。

- [ ] AI Workforce Map
- [ ] 员工 / 岗位统一 Card Contract
- [ ] 组织树和汇报关系
- [ ] 能力绑定、Workspace 归属、Owner
- [ ] 排班、节奏、预算、审批和超限策略
- [ ] 工作项、交接、日报、验收
- [ ] 成本健康、结果健康、容量和异常
- [ ] 变更影响预览、版本化、回滚
- [ ] 草案 → Simulation → 批准 → 上岗 → 归档

依赖：Phase 2 能力供给链、Runtime 员工对象。

验收：CEO 能创建一个岗位、配置能力、模拟、批准、让员工完成工作并查看结果。

### Phase 4：Workspace Studio 与业务办公室

目标：让 CEO 能搭建业务空间，而不只是配置 Agent。

- [ ] 业务分析和模板选择
- [ ] Outcome、输入、输出、Owner、验收
- [ ] 阶段、节奏、岗位、交接
- [ ] 能力、知识、数据窗口和权限
- [ ] 失败与人工备用路径
- [ ] Simulation 场景和结果
- [ ] CEO Approve、发布运行版本、回滚
- [ ] 业务办公室首屏、团队带、执行区、证据区、结果区
- [ ] 运行版本与 Draft 分离
- [ ] Workspace 内部可沉淀重复方案

依赖：Phase 2、Phase 3、Workspace Runtime。

验收：CEO 能从一句业务描述装修出一间可运行办公室，并看到业务团队和下一检查点。

### Phase 5：三业务纵向闭环

目标：研发、小红书、抖音同时形成真实业务闭环。

- [ ] 研发：Cycle / code / test / acceptance / next cycle
- [ ] 小红书：ContentItem / Version / Approval / Publish / Interaction / Feedback
- [ ] 抖音：Video / Version / Publish Receipt / Metrics / Feedback
- [ ] 每条业务的 API 与手动反馈窗口
- [ ] 失败、未授权、数据延迟、冲突、CEO 拒绝
- [ ] Assistant 业务上下文和主动跟进
- [ ] 结果回写业务版图和 CEO Desk

依赖：Phase 1–4。

验收：三条业务都能从创建到结果反馈，不用 fixture 或静态数字冒充真实业务。

### Phase 6：Meeting / Decision / Commitment

目标：让会议成为公司状态变化的受控入口。

- [ ] 会前准备
- [ ] 讨论流
- [ ] Fact / Opinion / Proposal / Objection / Unknown 标签
- [ ] AI 员工点名、轮次、实时状态
- [ ] Decision Proposal
- [ ] CEO 审批
- [ ] Commitment / Owner / DueDate / Evidence
- [ ] Workspace 回写和 Assistant 跟进
- [ ] 会议历史、引用、复盘

依赖：Phase 1、Phase 3、Phase 5 的真实业务上下文。

验收：会议结束后形成可执行承诺，并能在 Workspace 查看执行结果。

### Phase 7：自动化、日历、成果、知识和健康

目标：让公司能连续运行，而不是每次都靠 CEO 手动推动。

- [ ] 自然语言节奏配置
- [ ] 事件触发与风险阈值
- [ ] 下一次运行预览
- [ ] 经营日历由承诺和检查点生成
- [ ] 成果 / Evidence 收件箱
- [ ] 知识与记忆引用
- [ ] AI 成本健康
- [ ] 公司 / 业务 / 员工 / Workspace 健康
- [ ] 备份、恢复、本地运行诊断

依赖：Phase 5、Phase 6、Usage / Evidence 基础。

验收：CEO 能查看一段时间内公司如何运行、花了什么成本、产出了什么结果并决定下一步。

### Phase 8：完整 Desktop 交付

目标：让产品不仅逻辑完整，也真正适合长期使用。

- [ ] 桌面启动、单实例、更新和恢复
- [ ] 主题、中文、键盘、焦点、可访问性
- [ ] 所有页面统一空态和失败态
- [ ] 所有页面无旧导航和旧文案混入
- [ ] 1440×900、1024×768、深 / 浅 / 系统主题
- [ ] 打包、安装、数据迁移和本机备份
- [ ] 完整 CEO 一天浏览器 / Desktop 验收

依赖：Phase 1–7。

## 6. 建议的 Issue 划分

| Issue | 主题 | 对应阶段 | 主要结果 |
| --- | --- | --- | --- |
| PRODUCT-001 | Blueprint / UI / Runtime 事实收束 | 0 | 唯一产品真相和清理清单 |
| APP-001 | CEO Desk + Assistant 三态 | 1 | CEO 每日入口和全局 Chief of Staff |
| CAP-001 | 模型 / Skill / Tool 能力供给链 | 2 | 添加、验证、分配、运行 |
| TEAM-001 | AI Team Card / Organization / Health | 3 | 员工成为责任主体 |
| STUDIO-001 | Workspace Studio 完整装修链 | 4 | 业务空间可搭建和发布 |
| BIZ-001 | 三业务纵向运行闭环 | 5 | 研发、小红书、抖音真实结果 |
| MEETING-001 | Meeting Runtime → Decision | 6 | 讨论进入承诺和执行 |
| OPS-001 | 自动化 / 日历 / 成果 / 健康 | 7 | 持续经营与复盘 |
| DESKTOP-001 | Desktop 完整交付验收 | 8 | 长期可用的本机 App |

每个 Issue 在开发前必须明确：

- 产品场景和用户动线；
- UI 页面和状态；
- Runtime 对象和持久化事实；
- CEO / Assistant / AI 员工职责；
- 输入、输出、下一阶段和失败路径；
- Allowed Files；
- 浏览器 / Desktop 验收证据；
- 不得带入的旧链路。

## 7. 完成定义

Curis 不能以“页面完成”“接口完成”或“测试通过”作为最终完成。每个阶段至少证明：

1. CEO 能从用户入口进入；
2. 页面显示真实 Company / Business / Workspace 事实；
3. 配置和运行动作真的改变正确对象；
4. AI 员工有责任、能力、状态、输出和证据；
5. 失败、等待、拒绝、未知和恢复路径存在；
6. 结果能进入验收和 CEO 决策；
7. 决策能影响下一轮业务、能力或组织；
8. UI 视觉和中文语义统一；
9. 旧 Project / Task / fixture 不会成为新事实源；
10. Desktop 本地使用能完整走通。

## 8. EvoFlow 参照边界

### 必须学习

- 实体可见：头像、身份、简介、状态、动作；
- 少步骤：对话式配置、快速安装、下一次运行预览；
- 组织可读：汇报、岗位、员工、健康；
- 执行可见：Workbench、运行、失败、等待、审批；
- 会议可读：参与者、轮次、点名、实时状态；
- 资源可用：Model、Skill、Tool、Connector 的目录和详情；
- 结果关联：成本、产出、责任和业务上下文。

### 不直接复制

- 顶层 Agent Center；
- 顶层 Workflow / App 平台；
- 科幻会议舞台；
- 彩色 Dashboard；
- 默认 Full Auto / Unlimited Budget；
- 未审查的第三方能力一键安装；
- 模型缺失就阻断所有公司设计；
- 组织关系立即生效；
- 浮层遮挡主操作；
- 多 Agent 讨论直接产生公司决策。

## 9. CEO 最终确认清单

进入开发前，CEO 需要确认：

- [ ] Curis 的完整 App 区域和导航顺序
- [ ] CEO Assistant 三态（工作台 / 对话 / 会议）
- [ ] AI Workforce Card Contract
- [ ] 模型 / Skill / Tool 的能力供给链
- [ ] AI 员工生命周期和组织关系
- [ ] Workspace Studio 八阶段装配路径
- [ ] 三条业务的纵向运行顺序
- [ ] Meeting → Decision → Commitment 闭环
- [ ] 自动化、日历、成果、知识和成本健康的位置
- [ ] P0–P8 开发依赖关系
- [ ] 旧链、fixture 和示例数据清理策略
- [ ] 每个 Issue 的验收证据标准

本清单确认之前，不进入“一气呵成”的集中开发；确认后按 Issue 顺序执行，不在开发中重新发明产品。

### 9.1 CEO 确认矩阵

| 确认项 | 当前定义证据 | 进入开发的判断 |
| --- | --- | --- |
| Curis 是完整 Local Desktop App | Blueprint §01、§12–§13；Current State 产品定位 | 不因单机而删减模型、Skill、Tool、权限、成本或运行能力 |
| CEO 每日经营入口 | Blueprint §02、§04–§05；页面级布局契约 | CEO Desk 是默认进入和所有事项的返回中心 |
| CEO Assistant 是第一位 AI 员工 | Blueprint §05、EvoFlow 转译 §10；AI Workforce Card Contract | Assistant 有身份、生命周期、主动汇报、分流和跟进，不新增第二任务系统 |
| Capability Center 完整供给链 | Blueprint §07；Flow B；CAP-001 | 必须能添加、验证、分配、运行、观察、替换和回滚 |
| AI 团队和组织关系 | Blueprint §06；Flow C；TEAM-001 | 员工按岗位和结果管理，不做平级 Agent 货架 |
| Workspace 是业务办公室 | Blueprint §08；Flow D；STUDIO-001 | 从业务描述到 Studio、模拟、批准、运行和回滚闭合 |
| 三条业务同步建设 | Flow E；BIZ-001 | 研发、小红书、抖音共享 Company OS，但保留各自业务差异 |
| 会议进入决策闭环 | Blueprint §09；Flow F；MEETING-001 | 讨论只能形成 Proposal，CEO 决定后才生成 Commitment |
| 公司持续经营 | Flow G；OPS-001 | 日历、自动化、结果、知识、成本和健康回到 CEO Desk |
| EvoFlow 借鉴边界 | §02、§08；研究报告与截图证据 | 学习可见性和少步骤，不复制 Agent Center、Dashboard、Full Auto 或科幻会议 |
| 历史资料隔离 | Current State、Change Log、历史文档标识 | 旧 Blueprint / UI 只作证据，不作为开发依据 |
| 开发顺序与门禁 | Phase 0–8、Issue 表、完成定义 | CEO 确认后才创建正式 Issue，不在实现阶段重新定义产品 |

**确认结果：** `待 CEO 确认`  
**确认后动作：** 创建 PRODUCT-001 及 Phase 1–8 正式 Issue；未确认前仅允许产品审阅和事实修正，不进入业务代码集中开发。

## 10. 证据来源

- EvoFlow 深度研究：/Users/yy/Documents/大魔王知识库/资料/EvoFlow 深度产品研究：Curis 可借鉴能力、体验与终局形态.md
- EvoFlow 本地截图：/Users/yy/Documents/Curis AI Workspace/artifacts/evoflow-audit-2026-08-09/
- Curis 当前 UI 审计：docs/reviews/20260810_product_ui_audit/README.md
- Curis 当前 Blueprint：docs/01_Product/Curis_Product_Blueprint.html
- Curis 当前事实：docs/00_Context/CURRENT_STATE.md
