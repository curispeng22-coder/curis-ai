# CURIS PAGE REFERENCE BLUEPRINT（页面拼装蓝图）

> Authority Class: RESEARCH / EVIDENCE — Final UI Master 的逐页拼装参考（不构成 Product Authority）
> Status: COMPLETE — STOP FOR CEO / CHATGPT REVIEW
> Date: 2026-09-12
> 配套：`CURIS_PIXEL_LEVEL_COMPETITIVE_REFERENCE_MATRIX.md`（组件级矩阵与 E1–E9 实拍证据）；引用格式：Ref 名称（级别 | 证据）。
> 统一化总规则（全页适用，正文不再重复）：
> ① 所有 L3/L4 组件过 Curis token（V1 中性阶 + 单一 accent + 状态三色小面积）；
> ② 每页最多两个视觉口音来源（结构骨架 L2 + 组件 L4）；
> ③ 状态词典唯一（空闲/工作中·<desc>/阻塞·<cause>/待执行/执行中/已完成/已暂停/失败）；
> ④ 图标全套 Curis icon system（借 anatomy 不借 path）；
> ⑤ 冲突裁决：交互流程听 Best Reference、信息层级听 Curis Object Model、视觉密度听 Linear。

---

## P1 全局壳（App Shell）

- Product semantics：**L0**（七区 Structure Baseline）
- Navigation 轨：Linear 侧栏（L4 | E9）——组标签 11 大写灰、行 h28 字13、子项缩进；分组=工作区（CEO 工作台/业务空间）+ 组织与运营（组织中心/人才与能力/经营洞察/资料库/会议）
- 计数徽标：WorkBuddy 任务(7) 式计数（L3 | E1）——用于待处理/运行中
- 底部：账户行 Claude "yy · Gateway"式（L3 | E4）+ 设置入口（头像菜单）
- 右上：通知中心（L2 | ChatGPT 任务通知模式）+ 全局搜索入口（⌘K）
- Pane 骨架：四独立 Pane（**L0 Frozen Shell**），宽度节奏 Cursor 230/弹性/380（L2 | E6）
- 桌面 chrome：原生窗口（L1）；二期 Linear 式标题栏搜索 tab（L2 | E9）

## P2 CEO 工作台

- Product semantics：**L0**（注意力/简报/决定）
- 结构：今日简报（3–5 行）→ 需要你决定（Decision 队列）→ 正在运行 → 最新结果；公司脉搏收次级
- 简报/运行行：Linear 行节奏 h36（L1/L4 | E9）；行 anatomy=状态点+标题+meta+动作
- Decision 卡 anatomy：Claude 错误横幅分层（标题/解释/Details/双按钮）（L2 | E4）→ 背景说明/P7 选项/Evidence 引用/批准·驳回
- Running Work 行：ChatGPT 右栏压缩（L2 | E5）——员工头像+Work 名+当前动作+子任务计数；完成摘要 Cursor "Worked for 14m"式（L3）→ "用时 X 分钟 · 消耗 ◇Y · 交付 N 个结果"
- Latest Result：WorkBuddy 产物卡（L4 | E1）
- 空态：**Claude 空态**（L4 | E4）——问候+一句叙事+主行动；禁零值统计卡
- Employee Activity：ChatGPT 子智能体头像组（L3 | E5）

## P3 业务空间（列表 + 业务详情）

- Product semantics：**L0**（Business=持续经营身份）
- 业务行/卡：Linear Project 行+预览卡字段节奏（L2 | E9）——名/状态/本周一句话/Workspace 数
- 空态：Claude 空态式（L4 | E4）——单一主行动"创建第一个业务/交给空间工程部"
- 业务详情 Property 行：Linear Properties（Backlog/Lead/Target date 行）（L3 | E9）→ 负责人/状态/Workspace 数
- 禁止：统计卡联排、双空态重复（Problem Register P-BIZ-01/02）

## P4 Workspace 工作面（四 Pane）

- Product semantics：**L0**（Four-Pane Frozen Shell + Domain Surface）
- Context Pane：ChatGPT"环境信息"分节卡 anatomy（L2 | E5）——节=最近工作/业务列表/待处理筛选，每节+号
- Main：D 代 Domain Surface + Employee Row 两行结构（**L0 合规**），行节奏 Linear（L4 | E9）
- Utility：扣子全高工作台深度（L3 | E8）+ WorkBuddy 面板 chrome（tabs/全屏/收起）（L4 | E1）
- 面包屑+Surface tabs：WorkBuddy 顶栏共存式（L3 | E1）——修复换行断裂
- Conversation（员工工作会话）：见 P8 组件

## P5 组织中心（公司版图 / 员工目录）

- Product semantics：**L0**（公司版图/员工目录双 Tab 已验收）
- 版图：L0（Department Container 结构不动），密度/边线 Linear 化（L1）
- 员工目录行：D 代两行结构（L0）+ Linear 行节奏（L4 | E9）
- 员工卡（卡态视图）：WorkBuddy 专家卡 anatomy（L4 | E2）——avatar40+名+部门·Role+两行当前责任+3 关键词 chip；"原装"徽标位=特邀专家徽标位
- Search/Filter：Linear 筛选+搜索浮层（L3 | E9）

## P6 Employee Detail / 员工工作站（新核心页）

- Product semantics：**L0**（Employee=公司成员身份）
- Header：WorkBuddy 专家卡头部放大（L4 | E2）——头像 56+名+部门·Role+状态点+动作（对话/派工作/···）
- 分区结构：Claude Projects 页分区逻辑（L2 | 库存）——身份与组织关系 / 责任（长期+当前）/ 能力（能力卡→展开 Skill·Model 绑定）/ 当前工作（见下）/ 最近结果 / 对话 / 设置
- Responsibility 字段参考：Devin Playbook 五段（L2 字段 | 库存）用户化
- 当前工作区：ChatGPT 右栏节卡（L2 | E5）+ Work 步骤 checklist（Manus/Cursor，L2）+ 当前动作行（Cursor 折叠卡，L3）
- 最近结果区：WorkBuddy 产物卡行（L4 | E1）→ 点开 Utility
- 对话区：P8 Conversation 组件
- 状态 truthful：缺模型/缺 Holder 显式空态（L0 Phase A.1）

## P7 人才与能力（专题蓝图）

- Product semantics：骨架可复刻、原装组织叙事 **L0**
- **Talent Home**：WorkBuddy 专家中心整页结构（**L2 | E2**）——顶部三 tab 分段（员工/技能/连接器）+ 右侧搜索+我的员工；"精选场景"轮播 →"从一件事开始"（示例业务牵引）；专家⇄团队切换 → 员工⇄部门；分类 chips+排序（L4 | E2/E3）
- **员工卡**：WorkBuddy 专家卡（**L4 | E2** 实测 anatomy）
- **技能市场**：WorkBuddy SkillHub（**L2 | E3**）——精选技能 4 列内联 + 安装、推荐/SkillHub/套件（→自建/岗位包，需产品裁决）、我安装的计数、添加技能
- **技能卡**：WorkBuddy（**L4 | E3**）；来源徽标=官方/社区/自建
- **技能/连接器详情**：Coze 插件详情字段（L2 | 库存）+ WorkBuddy 连接器授权绿点状态（L2 | 库存）
- **安装流**：内联 + → 确认 → "绑定到哪个员工"引导（Curis 特有步骤，交互学 Cursor 扩展安装 L3）
- **Model/Capability 绑定**：Coze 节点级模型设置结构（L2 | 库存）+ Curis 能力用户语言卡（L0）
- **详情页（员工）**：见 P6
- 成果反查导购：WorkBuddy 灵感模式（L1 | 库存）——"从这个结果招同款"

## P8 Conversation + Composer（组件蓝图，跨页复用）

**Conversation**
- 任务型布局：WorkBuddy 任务视图（L2 | E1）
- 用户消息：ChatGPT 气泡（L4）；员工消息：文本流+结构卡+身份行（L3）
- 限宽：中心 ~720 逻辑 px（L4）
- 文件引用：WorkBuddy 附件卡 2 列网格（**L4 | E1**）
- 引用/来源：行内 chip+来源汇总（ChatGPT，L2 | E5）
- Tool Activity：Cursor 折叠卡（L3）；Thinking：Claude 折叠（L2）
- Progress：扣子步骤行 ○→✓（L3 | E8）
- Result Reference：产物卡→右栏 Utility（L3 | E1/E8，正合 Frozen）
- 操作行：WorkBuddy icon 行（**L4 | E1**）+ 成本内联"共消耗 ◇X · 模型"（**L4 | E1**）
- Error/Retry：Claude 横幅（L4 | E4）+ 重新生成（L3）
- Timestamp：Cursor 相对时间（L3 | E6）

**Composer（逐组件）**
- 容器：Claude 浮卡（**L4 | E4**）；槽位=Frozen X10（输入/＋/访问权限/工作模式/执行者/发送）
- 占位：Claude 20px 句式含 @/提示（L4 | E4 + WorkBuddy E1）
- 模型选择：Claude 内联文字下拉（**L4 | E4**）
- 执行者（员工）选择：同模型选择形（L3；Curis 槽位 L0）
- 访问权限：WorkBuddy"⚠允许完全访问"chip（**L3 | E1**）
- 发送/停止：圆钮 up-arrow，发送⇄停止同位，禁用灰（L4/L3 | E4/E1）
- Queue/Steering：Cursor（L2 | 库存）

## P9 资料库

- Product semantics：L0（Company Reference Space；消费已验收 Figma 187 基线）
- File Row：Linear Document 行（L4 | E9）
- 阅读面：WorkBuddy 右栏 markdown 阅读器（**L3 | E1**）——头部=来源/适用范围/版本/被引用数
- Used By 反向引用：**L0** 呈现（列表行）
- 搜索/筛选：Linear 浮层限定资料类型（L3 | E9）

## P10 会议

- Product semantics：**L0**（消费已验收 Figma 214 基线——不重做 IA）
- Decision 卡：P2 Decision anatomy（L2 | E4）
- 参会/说话人：通用会议语言（L1）；纪要转写=未来候选（Manus，L1）

## P11 经营洞察

- Product semantics：**L0**（消费已验收 Figma 172 基线）
- 图表视觉：安静无装饰（L1，Linear/Notion 语言）
- Cost/Usage 视图：扣子积分页拆分（L3 | E7）——按员工/模型/业务
- Report 阅读：WorkBuddy 阅读器（L3 | E1）

## P12 Settings

- Shell：Cursor 左类右容+设置搜索（**L3 | 库存**）；分区=五类（Direction §2.7，Claude P11 五分法）
- 模型行：Cursor Models 行（**L3 | 库存**）+ Vision/Reasoning/Context 徽标
- Provider：WorkBuddy 本地 Key+Cursor BYOK 字段（L2）+ 凭据三态
- Skill/MCP：Cursor（**L3 | 库存**）
- Permission：Cursor Approvals & Execution 档位页（**L3 | 库存**）+ 四层 Scope 展示（L0）
- Memory：Claude 逐条+来源（**L3 | 库存**）
- Usage：扣子积分页（L3 | E7）+ Claude usage ring 就地（L3）
- Appearance/Shortcuts/About：Claude/Cursor 常规（L2/L3）

## P13 全局搜索 / ⌘K

- **Linear 搜索浮层 L4 整体复刻**（E9）：输入 h48 + 类型 chips（员工/业务/工作空间/结果/资料/会议/动作）+ 分组结果行（类型列+图标+标题+meta）+ 右侧 380 预览（Property 行）
- 动作区：新建工作/派工作/发起会议（命令面）

## P14 通知中心 + 全局助理浮层

- 通知：四类分组（结果就绪/需决定/阻塞/会议），行 anatomy=Linear 行+深链（Devin Slack 三按钮模式，L1）
- 助理浮层：ChatGPT Classic Option-Space 形态（L2 | 库存）——系统级唤起、当前上下文感知；**内容=P8 对话+Composer，禁统计卡**（Problem Register C3）

---

## 验收自检（本蓝图的完成标准）

明天重画任一 Final UI Master 页面时：
- 页面骨架 → 本蓝图对应 P 节；
- 每个组件 → PIXEL_MATRIX §3 对应行标注的（竞品, Surface, 级别, 证据文件）；
- 打开 `evidence/pixel-reference/<product>/*.png` 即见真实参照。

**STOP FOR CEO / CHATGPT REVIEW——不自行开始 Final UI Master。**
