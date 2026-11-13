# Curis UI Reference Map

**Status: REVIEW REQUIRED**  
**日期：2026-08-14**  
**性质：**唯一 UI Blueprint 的参考映射工作稿；不是第二份 Blueprint，不重定义 Product Blueprint、Page Map、Runtime 或正式业务代码。

## 1. 目的与依据

本稿把已经存在的竞品研究转为可执行的 UI 选择，避免再以需求清单拼装页面。它只回答四件事：当前场景主要借谁、借哪个已经成熟的行为、Curis 不借什么、Curis 必须补回的公司语义。

已读取并使用：

1. `docs/01_Product/Curis_Product_Blueprint.html`（5.1，Frozen）
2. `docs/01_Product/Curis_Product_Page_Map_v1.0.md`（Review）
3. `docs/01_Product/Curis_Product_UI_Blueprint.html`（唯一 UI Blueprint，REVIEW REQUIRED）
4. `docs/03_Design/Curis_Design_System.md`（Frozen）
5. `docs/01_Product/Curis_Product_Rethink_Reasoning_2026-08-13.md` §11（已有参考机制矩阵）
6. `docs/research/competitors/coze.md`
7. `docs/competitive-analysis-evoflow-vs-curis-2026-08-04.md`
8. `docs/reviews/2026-08-04-curis-ui-audit-report.md`、`docs/reviews/2026-08-05-frontend-ui-audit.md`、`docs/03_Design/UI_Exploration_Gap_Audit_2026-08-04.md`

### 输入缺口

请求中点名的 `Curis_Product_Experience_And_Competitor_Audit_2026-08-10.md` 不在当前主目录、受控附件或可检索的非依赖文件中。没有将不存在的文档写成已读事实。本稿以 2026-08-13 产品重新推导中已收敛的引用矩阵作为正式替代输入；若该原始审计随后迁回主目录，应只补充来源与证据，不自动覆盖本稿的产品边界。

## 2. Curis 的统一方式

Curis 不做竞品拼贴。统一来自：同一个 220px 一级导航、同一组中性令牌与交互反馈、同一套“对象可进入 / 对话可持续 / 返回不丢现场”规则，以及 Company → Business → Workspace → Employee → Result 的回流关系。

不同页面的布局只由当前任务决定：

| 任务关系 | 使用的空间 |
| --- | --- |
| 需要持续工作或持续对话 | 主工作区 / Full Workspace |
| 临时完整阅读并判断一个对象 | Focus View |
| 不离开当前工作而看或改辅助对象 | Inspector |
| 持续浏览目录、集合、线程、文件 | Shell Context Sidebar |
| 两三行状态、筛选、通知、上下文操作 | Popover |

## 3. 场景参考映射

| Curis 场景 | 主要参考与直接吸收的行为 | Curis 不复制 | Curis 自己增加的公司化能力 |
| --- | --- | --- | --- |
| Desktop Shell | **Linear**：稳定一级层级、最近工作、搜索、紧凑当前态；**Codex / Notion**：项目面包屑、按需上下文栏、可最大化工作现场。 | Linear 的 Issue / Project 作为根语义；给每页固定第二栏。 | 六个已冻结一级区；跨 Workspace 的公司、业务、员工和结果返回。 |
| CEO Assistant | **ChatGPT**：从问题进入、保留会话与上下文；**Codex**：当前任务附近的连续对话。 | 把它变成所有点击后的统一聊天弹窗，或固定第三栏。 | 仅有一个 CEO Assistant 身份；跨区域解释、建议、委派与返回原工作。 |
| Workspace Conversation | **Codex / Claude Code**：项目 → thread → conversation；文件、Diff、终端、Review 随当前工作出现。 | 将 Thread、Diff、Terminal、Test、Review 永远并排展示。 | 对话带业务、员工、资料与结果上下文，结束后回写办公室和公司。 |
| Employee Conversation | **Coze**：中央 Conversation + 底部 Composer；按需打开模型、Skill、知识、工具和连接设置。 | 让员工只是组织图旁的属性卡，或让 CEO Assistant 冒充员工。 | 岗位、责任、汇报、所属业务 / Workspace、工作历史、成果和成长。 |
| Meeting Conversation | **群聊 / 多 Agent 会话**与 **Coze**：持续消息流、成员、引用、@提及、底部 Composer。 | 静态发言卡 + 常驻 Decision Proposal 双栏。 | 会议有公司或 Workspace 上下文；Proposal 从讨论生成，并返回责任与来源工作。 |
| Talent Market | **Workbuddy**：专家分类、搜索、市场卡片、专家团、完整专家 Focus View、单一招募 CTA；**Coze**：Skill / Connector 的能力说明和设置入口。 | 把专家当公司员工；把完整档案塞进 Inspector；品牌、素材或专有文案。 | 招募后才进入公司身份、岗位、责任、业务、Workspace 与员工化装配。 |
| Organization | **OpenOPC**：Company / Position / Employee / Executor 分层；成熟组织图：结构和协作分开阅读。 | 固定公司结构、工程化 first-run 或 CLI 模型配置。 | 部门不是招聘前置；组织图之外有协作关系、员工对话和结果历史。 |
| R&D Workspace | **Codex / Claude Code**：线程是主入口，对话与 Composer 是主工作，文件 / Diff / 终端 / 测试 / Review 是上下文切换。 | IDE 面板永久全开；DAG / Runtime 成为首页。 | AI 员工与公司资料、工作历史、启动缺口和结果回到 Business。 |
| Content Workspaces | **ChatGPT / AI 内容产品**：围绕正在讨论和正在做的内容对象；**Relevance AI**：多 Agent 在熟悉对话里协作。 | 将日历、看板、团队、数据、发布一次铺开。 | 内容对象带业务目标、责任人、公司资料、审批、真实结果与人工回填。 |
| Knowledge Library | **Notion**：局部 Context Sidebar、面包屑、阅读工作面、版本 / 恢复；**Workbuddy**：资料作为专家工作输入。 | 把 Curis 做成通用页面编辑器。 | 资料显示来源、权限、引用、使用员工 / Workspace 与公司产生的结果。 |
| Settings | **Codex / Coze / Notion**：头像 Popover → 独立 Settings Workspace → 左侧目录 + 右侧设置内容。 | 设置成为第七个一级区；把模型和凭据复制进员工或市场卡片。 | Provider、能力、连接与权限明确标注发现 / 待授权 / 已验证的事实边界，并返回原来源。 |
| Long-running work | **Relevance AI**：日常使用与 Builder 分离、@员工 / 多 Agent 在对话中协作；**EvoFlow**：进度、等待、恢复和人工介入。 | DAG / Workflow Builder 作为 Curis 普通用户入口，或复制 EvoFlow 专有术语与代码。 | 以业务、员工、结果、等待我和下一检查点表达，不伪造执行或恢复事实。 |

## 4. Conversation System 决策

| 对话类型 | 所属上下文 | 默认入口 | 核心工作面 | 关闭 / 返回 |
| --- | --- | --- | --- | --- |
| CEO Assistant Conversation | Company + 当前页面 | 顶栏、快捷键或全局浮层 | 按需浮层；必要时跳入对应主工作区 | 回到唤起的页面与状态。 |
| Workspace Conversation | 当前 Business / Workspace / Thread | Workspace thread 列表或当前会话 | Full Workspace 的中央 Conversation + Composer | 保留 Thread、滚动、附件与当前对象。 |
| Employee Conversation | 当前 Employee | 组织中心员工对象或 Workspace 团队对象 | 中央 Conversation + Composer | 回到员工来源；Inspector 不替代对话。 |
| Meeting Conversation | Company Meeting 或 Workspace Meeting | 会议列表、业务 / Workspace 的会议入口 | 中央 Conversation Stream + Composer | 回到会议来源和未完成讨论。 |

禁止“与团队对话”打开 CEO Assistant。它只在 CEO 明确需要跨公司理解、建议或委派时出现。

## 5. Composer 作为公共原语

所有工作对话使用同一阅读节奏和同一 Composer 骨架：

```text
[添加]  [资料 / 附件]  输入当前要说的话…  [模型或执行对象]  [发送]
```

Workspace 增加 `@员工`、Skill、Tool、文件和当前对象；Meeting 增加 `@参与者`、引用资料与 Proposal；Employee 固定当前员工并可显示模型 / Skill 状态。工具动作在 Composer 或对象 hover 中出现，不以一排文字按钮替代对话。

## 6. Reference Map 的执行约束

1. 每个视口只有 0–1 个强主 CTA；对象、行、卡片和面包屑优先成为自然入口。
2. Feed / Conversation 优先于“每条内容一张 Card”；状态用小标签，不给所有信息上色。
3. Context Sidebar 必须是 Shell 的可选 sibling，不得嵌在业务 `.content` Grid 内。
4. 研发、内容和会议先显示“我们现在正在做什么”和可继续的 Composer；次要上下文按当前对象出现。
5. 所有示例数据继续明确为 `REVIEW REQUIRED · 示例快照 · 非真实运行`；Reference 不等于接入、授权、健康或执行证据。

## 7. 后续合并位置

通过 Review 的决策将原位合并回唯一 `docs/01_Product/Curis_Product_UI_Blueprint.html` 的“完整产品高保真原型决策”章节；本稿保留为研究输入，不成为平行 UI Blueprint。
