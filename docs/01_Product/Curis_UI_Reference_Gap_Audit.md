# Curis UI Reference Gap Audit

**Status: REVIEW REQUIRED**  
**日期：2026-08-14**  
**性质：**当前 Prototype 的 Reference-Driven UI 审计工作稿；不是 Blueprint、不是正式代码验收，也不声称示例页面已经接入业务事实。

## 1. 审计范围与方法

范围是当前 `docs/01_Product/Curis_UI_Blueprint_Prototype.html` 的结构与交互。以 `Curis_UI_Reference_Map.md`、Product Blueprint 5.1、Page Map、Frozen Design System 和已有竞品研究为判断依据。结论只决定下一次原型重做的方向，不改变 Product Blueprint、Master Map、Page Map、Runtime 或正式业务代码。

### 总结

当前原型已经正确表达了六区、专家不等于员工、Focus View、资料阅读与不同 Workspace 的意图；但它仍把这些意图渲染成“说明卡片 + 文字按钮 + 固定面板”的需求清单。最高优先级不是再加功能，而是把持续工作的 Conversation、Composer、Shell Context Sidebar 和渐进出现的专业上下文做成真正的界面骨架。

## 2. 逐场景差距

| 场景 | 当前实现 | 主要参考 | 当前为何不自然 | 本轮修正 |
| --- | --- | --- | --- | --- |
| 首页 | 简报、变化、经营、待决定并列成多张卡片，且每张卡片含文字 CTA。 | Linear + ChatGPT。 | CEO 需要先看到一件最值得继续的事；页面像解释产品的概览。 | 收敛为一条工作叙事：Assistant 摘要、当前焦点、连续对象列表；对象点击进入来源，Assistant 是按需对话。 |
| 一级导航 | 六区正确，但最近工作和全局操作仍以页面按钮逻辑表现。 | Linear。 | 壳层稳定性有了，信息密度与最近工作的“继续”感不足。 | 使用紧凑稳定的 nav、Recent 与命令式搜索；保留六区，移除页面内重复入口。 |
| Context Sidebar | `.contextlay` 作为 `.content` 内部 Grid，资料库和 Workspace 重新发明一套二栏。 | Notion + Codex。 | 不是 Shell sibling，折叠不会让主区自然扩展，也会让各业务重复实现。 | Shell 只在 `context` 状态存在时插入 Context Sidebar；资料库与研发 Workspace 共享其出现、折叠和恢复规则。 |
| 人才市场 | 有 Tab、搜索、分类、卡片和 Focus View，但市场头部与专家卡解释文字偏多。 | Workbuddy + Coze。 | 卡片像功能介绍，CTA 密度高，浏览节奏不像成熟市场。 | 将卡片压缩为身份、擅长、可用状态与一个自然进入点；详情 Focus View 再承载案例、来源、职业能力和招募。 |
| 专家详情 / 招募 | Focus View 方向正确；详情中仍解释“为何不用 Inspector”，招募步骤表单密度偏后台。 | Workbuddy。 | 面向用户的页面混入 Blueprint 解释；专家判断与员工装配之间跳转不够自然。 | 从真实专家档案开始；招募作为连续专注装配，只有一个推进动作，并用返回保持市场位置。 |
| 组织中心 | 绝对定位节点 + 网格背景 + 多个说明层；员工工作面与组织浏览断裂。 | OpenOPC + 成熟组织图。 | 图只证明“有节点”，没有体现结构、协作和继续工作的关系。 | 结构 / 协作 / 员工是三种可切换阅读模式；员工对象直接进入完整 Employee Conversation。 |
| 员工 | 工作面有信息与 Inspector，但对话不像真正持续的 Agent 对话，底部没有永久 Composer。 | Coze。 | “与员工工作”仍接近详情页；用户无法自然继续当前协作。 | 中央 Conversation Stream + 固定 Composer；当前责任简短置顶，配置和能力按需进 Inspector。 |
| 研发 Workspace | 文件、Diff、Terminal、Test、Review 作为三列 / 多块同时铺开。 | Codex + Claude Code。 | 需求清单被直接映射为面板，Conversation 不像主轴。 | Context Sidebar（项目 / thread / 文件）+ 主 Conversation；点击文件 / Diff / Terminal / Review 才切换当前工作上下文，Inspector 只在必要时出现。 |
| 小红书 Workspace | 日历、看板、团队、数据等被同时铺开。 | AI 内容产品 + Relevance AI。 | 首屏不知道团队此刻在做什么；更像运营 dashboard。 | 当前内容对象 + 团队 Conversation + Composer 为核心；日历、内容集合、数据按阶段或对象切换。 |
| 短视频 Workspace | 素材、预览、脚本、剪辑、审核、发布和反馈并列。 | AI 创作产品 + Relevance AI。 | 一眼像完整生产流程说明，无法进入当前视频的工作。 | 围绕当前视频和 Conversation；素材 / 脚本 / 编辑 / 审核随阶段在同一主区切换。 |
| 资料库 | 资料导航正确，但 `contextlay` 错置；阅读、属性、来源的边界尚不清晰。 | Notion + Workbuddy。 | 资料目录不是 Shell 空间，内容和属性容易并列成面板。 | Shell Context Sidebar + 主区阅读；来源、权限、引用、使用关系只在不打断阅读时用 Inspector。 |
| 会议 | 消息样式存在，但静态发言与 Proposal 容易被做成并列区域，Composer 不是真正交互核心。 | 多人对话产品 + Coze。 | 会议像纪要版面，非正在讨论的工作空间。 | 顶部议题 / 参与者，中央 Conversation Stream，底部 Meeting Composer；资料、成员、Proposal 按需打开，Proposal 在讨论后出现。 |
| 头像菜单 | 有 Popover，但项目中仍把部分设置触发做成文字按钮与单独页面逻辑。 | Codex。 | 账户操作没有足够紧凑的“用户菜单 → 设置空间”连续性。 | 保持左下头像 Popover，设置进入独立 Workspace，并从原来源返回。 |
| 设置 | 有 Settings Workspace 和目录，但页面内容仍是大量解释性信息。 | Codex + Coze + Notion。 | 设置应该帮助完成一次配置，而非解释整个能力体系。 | 分类目录 + 任务化设置表单 / 状态；模型、连接器和权限使用简短事实、测试与返回。 |
| 首次引导 | 有 CEO Assistant 双栏，但预览、说明和操作并列偏多。 | ChatGPT。 | “一句话开始”被可视化成产品说明页。 | 让 Assistant Conversation 是主角；公司 / 业务 / Workspace 预览作为对话产生的少量可确认对象。 |
| CEO Assistant | 被实现为右下 Popover 且用预设气泡 / 文字按钮互动。 | ChatGPT + Codex。 | 全局入口正确，但容易替代所有本地 Conversation。 | 只处理 CEO 跨公司问题；Workspace、Employee、Meeting 继续在各自主区对话；对话可进入具体对象而不夺走本地上下文。 |

## 3. 结构性根因

1. **按功能名切页面。**当前实现把“需要有 Thread / Diff / Terminal / Review”翻译成同时可见的面板，而没有先问用户现在在继续哪件工作。
2. **按组件先行。**Inspector、Context Sidebar、Dialog 都已出现，但没有按空间选择规则分配给当前任务。
3. **解释进入产品。**“这里不是……”等 Blueprint 说明进入可见原型，增加噪音并遮蔽真实对象。
4. **Conversation 不是原语。**缺少贯穿 Workspace、员工与会议的 Composer，使“对话”退化成助手入口或静态气泡。
5. **Context Sidebar 不是 Shell。**内嵌 `.content` 导致它只是某页的局部布局，无法表达可选、折叠、主区扩展这一公共契约。

## 4. 强制重做顺序

1. 先建立 Conversation System 与统一 Composer。
2. 将 Context Sidebar 提升为 Shell sibling，并真实演示资料库与研发 Workspace 的出现 / 折叠。
3. 以 Conversation 为主轴重做研发 Workspace、员工工作面和会议室。
4. 以“当前内容对象 + Conversation”重做小红书和短视频 Workspace。
5. 用 Workbuddy / Coze 的真实浏览密度修正人才市场、员工和设置。
6. 最后删去说明性文字、重复 CTA 和不必要的 Card，再合并已通过决策回唯一 UI Blueprint。

## 5. 验收问题

- 用户是否能看出每一段对话属于 CEO、某个员工、某间办公室还是某场会议？
- 输入框是否真实、持续且具有当前上下文，而不是“继续对话”按钮？
- 文件、资料、成员、Proposal 和配置是否只在需要时出现？
- Context Sidebar 是否真的脱离业务内容结构，并在折叠后释放主区宽度？
- 用户是否能从一个对象自然进入下一个工作，而无需阅读设计说明或点击多组文字按钮？

## 6. 事实边界与下一步

本审计不证明真实模型、Connector、员工、会议、发布、数据或恢复已经接通。下一步只允许更新当前 Prototype 与唯一 UI Blueprint，并继续保持 `REVIEW REQUIRED`；正式业务实现仍需独立 Issue、真实 Browser/Desktop、持久化、失败恢复和 Business Runtime 证据。

