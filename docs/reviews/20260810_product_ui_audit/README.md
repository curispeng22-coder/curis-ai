# Curis Product UI Audit · Blueprint 5.0 对照现场

Status: Review  
日期：2026-08-10  
范围：Local Desktop 当前前端的 CEO Desk、能力中心、Workspace Studio、业务版图、AI 团队、会议工作台、成果页  
目标：验证 Blueprint 5.0 的完整产品形态是否已经在前端形成可用动线。

## 总体结论

当前前端已经有一套清晰的 Desktop 壳层、主题和 Runtime 视觉语言，但还不是完整的 CEO App。

主要差距不是视觉质量，而是产品链路：

1. CEO Desk 能看到 Runtime 快照，但没有把“下一步经营动作”真正推进下去。
2. 能力中心能注册模型，但还没有形成“模型 / Skill / Tool → AI 员工 → Workspace → 运行”的完整配置闭环。
3. Workspace Studio 已经像业务空间装修器，但 Bind / Staff / Simulate / Approve / Operate 仍然主要是展示状态。
4. AI 团队页仍读取旧 Department / Employee / Project 事实，与 Runtime Workforce Map 分裂。
5. 会议和日历仍是明确占位页。
6. 成果页仍展示硬编码的示例汇报，与“真实结果才能进入公司资产”的产品原则冲突。
7. 当前运行数据包含四个草拟 Workspace，其中“小红书增长实验室”不在三条同步业务规划中，说明运行数据清理和业务创建入口仍未完全收束。

## 证据截图

### Step 1 · CEO Desk

![CEO Desk](/Users/yy/Documents/Curis AI Workspace/docs/reviews/20260810_product_ui_audit/01-ceo-desk.png)

现场：

- CEO Desk 显示 4 个 Workspace、1 位 AI 员工、0 个待处理事项。
- Assistant 自动打开，但显示“未命名 Assistant / 尚未设置角色”。
- 业务版图只有“草拟中”和“目标结果尚未记录”。
- 主导航只显示 CEO 工作台、经营、业务版图、工作空间；能力、会议、成果等入口被收进“更多”。

问题：

- 默认入口可以看到状态，但看不到“现在应该做什么”的明确主动作。
- Assistant 已经存在，却仍处于未配置身份，削弱第一位 AI 员工的存在感。
- Workspace 数量和草稿数据本身没有转化为可执行的经营动作。
- “更多”隐藏了 CEO 必须使用的能力中心和经营工具。

### Step 2 · 能力中心

![能力中心](/Users/yy/Documents/Curis AI Workspace/docs/reviews/20260810_product_ui_audit/02-capabilities.png)

现场：

- 能力中心可以搜索、注册能力、注册自定义模型。
- 有模型、智能体、技能、工具、工作流、连接器、命令行、接口调用、事件回调、MCP 协议十类入口。
- 当前只有一个已启用模型。
- 页面没有在首屏展示模型如何分配给哪个 AI 员工、哪个 Workspace，也没有运行验证和成本入口。

问题：

- 目录完成度高于经营配置完成度，CEO 仍需要自己猜“接入后下一步是什么”。
- Skill / Tool 的接入、授权、验证、版本和绑定没有形成连续动线。
- 模型添加成功不等于公司获得能力；页面没有直接连接到岗位和业务结果。
- 首屏信息较克制，但能力层级仍偏“资源后台”，需要增加“供给到责任”的上下文。

### Step 3 · Workspace Studio

![Workspace Studio](/Users/yy/Documents/Curis AI Workspace/docs/reviews/20260810_product_ui_audit/03-workspace-studio.png)

现场：

- Studio 已展示 Discover → Blueprint → Compose → Bind → Staff → Simulate → Approve → Operate 八个阶段。
- 左侧可选择研发、小红书、抖音模板；中间显示阶段责任、岗位和 Simulation 场景；右侧显示配置检查。
- 当前表单主要输入办公室名称、目标结果、验收证据和失败备用路径。
- 绑定能力、岗位物化、Simulation、CEO Approve 和 Operate 仍是后续门禁。

问题：

- 产品形态已经接近“业务空间装修”，这是当前最符合 Curis 差异化的一页。
- 但 Bind 仍更像需求清单，缺少从能力中心选择真实模型 / Skill / Tool 的操作。
- Staff 仍更像计划岗位卡，缺少岗位→员工→能力→运行测试的连续确认。
- “保存 Draft 并形成候选岗位方案”在未填写目标时直接禁用，缺少 Assistant 帮助补全和解释缺项。
- 页面同时展示八个阶段、岗位、能力、检查和门禁，信息密度偏高；需要以业务结果为主线逐步展开，而不是一次展示全部治理状态。

### Step 4 · 业务版图

![业务版图](/Users/yy/Documents/Curis AI Workspace/docs/reviews/20260810_product_ui_audit/04-business-map.png)

现场：

- 业务版图以四张 Workspace 卡片展示业务。
- 每张卡片的业务目标和目标结果均为“尚未记录”。
- 卡片只显示 Simulation 次数和状态，没有收入、客户验收、平台反馈、投入或下一决策。
- “小红书增长实验室”额外出现在当前数据中。

问题：

- 视觉上仍然接近项目 / Workspace 列表，没有形成“公司战略版图”。
- 没有“创建新业务”或“继续经营 / 暂停 / 扩大”这类业务层动作。
- 缺少外部结果和业务阶段解释，CEO 无法判断为什么值得继续投入。
- 当前数据与三业务同步计划不一致，必须清理来源并区分真实创建与实验数据。

### Step 5 · AI 团队

![AI 团队](/Users/yy/Documents/Curis AI Workspace/docs/reviews/20260810_product_ui_audit/05-ai-team.png)

现场：

- AI 团队页显示“AI Workforce Map”，但实际读取的是 Workspace、业务部门、员工和项目旧记录。
- 页面显示 0 个部门、0 个员工、0 个项目。
- CEO Assistant 只在 CEO Desk Runtime 投影中出现，未在此页形成同一组织事实。
- 能力资产库只是跳转到能力中心。

问题：

- 这是当前最明显的双系统：Runtime Workforce Map 与 legacy Organization 页面并存。
- CEO 看到的组织关系、岗位、能力和状态在不同页面无法互相验证。
- 页面虽然视觉上像公司组织，但业务事实仍是旧 Department / Employee / Project 模型。
- 必须将组织页改为 Runtime AI 团队入口，旧员工管理只作为内部兼容或迁移视图。

### Step 6 · 会议工作台

![会议工作台](/Users/yy/Documents/Curis AI Workspace/docs/reviews/20260810_product_ui_audit/06-meeting-placeholder.png)

现场：

- 页面仅显示“会议工作台 · 规划中 · v1 暂不建设”。

问题：

- Blueprint 5.0 已将会议定义为 CEO 形成共识、决议和承诺的必要产品能力。
- 当前占位页使 Assistant 的会前准备、会议讨论、决议回写和 Workspace 交接无法成立。
- “规划中”不应继续作为用户可见的产品状态；应至少形成可用的会议创建、准备、讨论、决议草案和返回路径。

### Step 7 · 成果 / 汇报

![成果页](/Users/yy/Documents/Curis AI Workspace/docs/reviews/20260810_product_ui_audit/07-reports-fixture.png)

现场：

- 页面明确显示“示例快照 · 未接入真实数据”。
- 汇报列表和正文使用固定的人名、日期、项目和百分比。
- 内容与当前 Company Runtime、三条业务和 AI 员工没有关联。

问题：

- 这是违反当前产品真相的高风险区域：即使页面声明是示例，CEO 仍会把它看成公司的实际成果。
- 必须改成真实成果 / 证据收件箱；没有数据时显示空态和人工录入入口，不显示固定数字。
- 成果页应由业务 Workspace、外部反馈和 CEO 验收共同产生，而不是独立报告列表。

## 优先级建议

### P0 · 先消除双事实和假成果

1. 清理或隔离“小红书增长实验室”等非当前业务数据。
2. 将 AI 团队页切换为 Runtime Workforce 事实源。
3. 删除成果页硬编码示例，改为真实成果 / 手动反馈空态。
4. 让 CEO Desk 在没有待处理事项时提供下一步经营动作，而不是只显示“继续关注”。

### P1 · 补齐核心能力配置闭环

1. 能力中心增加模型 / Skill / Tool 的验证、权限、分配和运行测试。
2. AI 员工详情显示能力绑定、容量、成本、最近结果和失败。
3. Workspace Studio 的 Bind / Staff 直接消费能力中心真实资源。
4. Assistant 能从业务结果缺口提出岗位和能力方案。

### P2 · 补齐公司经营工具

1. 会议工作台：创建 → Assistant 会前准备 → 对话讨论 → 决议草案 → CEO 确认 → 承诺回写。
2. 日历：从承诺、检查点和回报时间生成，不显示预置日期。
3. 业务版图：业务目标、外部结果、投入、阶段和继续 / 暂停 / 扩大动作。
4. 成果、知识、记忆、成本统一回到 Company Runtime。

## 可访问性与交互风险

- 多处页面使用灰色小字表达关键状态，需要确保对比度和非颜色标识。
- “更多”收起导航导致能力中心、会议和成果入口不易发现。
- Studio 八阶段横向信息在小窗口下可能拥挤，需要键盘可达和清晰的当前阶段焦点。
- 能力类型以 Tab 展示时，应保证键盘切换、选中状态和屏幕阅读器语义。
- 空态不能只写“尚未记录”，必须同时说明 CEO 下一步。
- Assistant 自动打开会遮挡 CEO Desk；应保留首次出现的温和提示，并允许用户关闭且不反复打断。

## 证据边界

本轮通过当前本地前端和真实运行数据完成浏览器截图审计。截图可以证明页面层级、视觉层次、文案、入口和当前呈现的数据；不能单独证明后端执行、外部平台授权、模型真实调用、数据持久化和打包 Desktop 的端到端行为。
