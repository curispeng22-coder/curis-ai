# CURIS CURRENT UI AUDIT — 找茬审计

> Authority Class: RESEARCH / EVIDENCE（UI/Interaction 审计；不推翻 Frozen Product Structure）
> Status: COMPLETE（基于现有截图与原型资产；Final UI Master 本身 PAUSED，无更高视觉权威存在）
> Date: 2026-09-12
> 证据源：
> - A 代（旧）：`curis-ui-prototype/p1-preview/*.png`（黑/绿 accent、使用已废弃"办公室"词汇的一代原型）
> - B 代：`docs/reviews/multi-surface-workspace-screenshots/*.png`（1440 宽、七区导航 + Surface 列 + Main + Utility 四列结构）
> - C 代（真实前端）：`docs/reviews/20260813_current_state_product_drift_audit/*.png`（frontend/ 实然运行截图）
> - D 代（最新原型）：`curis-ui-prototype/coverage-exploration-2026-08-17/`、`department-business-work-surface-2026-08-18/`（消费 Frozen Shell Contract 的全产品覆盖原型，质量自评 PASS）
> - 审计方法：视觉模型直接读图 / headless 渲染。所有尺寸/颜色为像素级目测，标注 APPROXIMATE。
> 边界：只批评 UI / Interaction，不评判 Frozen Product Structure（七区、Company OS、Four-Pane、原装组织均为合法结构，不在推翻范围）。

---

## 0. 最重要的系统性发现（先于逐页找茬）

| # | 发现 | 级别 |
|---|------|------|
| S1 | **三套以上视觉语言并存**：冻结 Visual Standard V1 是 Direction D / `#806BE5` 紫；A 代原型用 黑色主按钮 + 绿色 accent（APPROXIMATE `#22c55e` 系）；B 代截图用 中性灰 + 黑字主按钮 + 状态彩色 chip（amber/green/blue）。且真实前端 `frontend/app/globals.css` 的 FROZEN `--ui-*` token 用的是旧 UI Spec 的 `#32f08c` 绿，同时 `organizationCenter.module.css`、`meeting/page.js`、`OperatingIntelligence.js` 内联 `#806BE5`——实现层自身就有两套 accent（见 CURIS_UI_EVIDENCE_CATALOG.md）。冻结视觉标准在任何一层都未被统一消费。 | P0 Directional |
| S2 | **A 代原型使用已废弃词汇"办公室"**（侧栏"办公室"分组、"经营办公室"、"小红书运营办公室"、多处空态文案）。CEO 已于 2026-08-24 裁定 Office 退出产品语义（Workspace 是唯一 canonical identity）。这批原型继续把被否决的模型画给用户看。 | P0 Directional |
| S3 | **A 代与 B 代信息架构不一致**：A 代侧栏是 公司/工作空间/经营工具/公司资源 四组 + 成果库/知识库/财务/日历；B 代是 工作区/组织与运营 两组 + CEO 工作台/业务空间/组织中心/人才与能力/经营洞察/资料库/会议（七区）。两代都存在于资产库中，若被当作"当前 UI"会直接误导设计研究。 | P0 Directional |
| S4 | **空状态是所有页面的主体**：A 代几乎每页以 0 统计卡 + 全屏空态卡构成（活跃周期 0 / 待 CEO 验收 0 / 可引用资料 —…）。first-run 体验被设计成"报表后台没有任何数据"，而不是"公司正在等你启动"。 | P0 Directional |
| S5 | **网页后台感（admin-dashboard feel）**：统计卡四联排、tab+计数、面包屑、表单式卡片，全是 SaaS 后台模板语汇；与"桌面 AI 公司 OS"应有的空间感/对象感/活动感不符。 | P0 Directional |
| S6 | **无桌面 App 质感**：无原生窗口控件区设计、无 dock/tabbed window 语义、无全局命令面（⌘K）、无菜单栏语义；悬浮"询问助理"气泡是网页 widget 形态，不是 desktop companion。 | P1 Structural |

---

## 1. App Shell / 全局导航（A、B 代对照）

**A 代侧栏**（APPROXIMATE 宽 300px，浅灰底）：
- 分组：公司（CEO 工作台/经营/业务/AI 团队）、工作空间（工作空间门户/软件工作室/短视频/小红书/部门）、经营工具（会议工作台/决策室）、公司资源（成果库/知识库/财务/日历），底部 设置/帮助。
- 问题：
  - P1：**侧栏项目与七区结构不符**（见 S3），且同一层级混有"区域（经营）+ 对象类型（业务）+ 实例（软件工作室/短视频/小红书）"，语义混乱。
  - P1：侧栏上下两端各出现一次标语"事实先于观点。共识必须回到责任与结果。"——口号重复占据导航空间，是营销文案入侵产品壳。
  - P2：图标为通用线性图标，无分组折叠能力，14+ 项平铺。

**B 代侧栏**（APPROXIMATE 宽 218px）：
- 分组：工作区（CEO 工作台/业务空间）、组织与运营（组织中心/人才与能力/经营洞察/资料库/会议），与七区结构一致。✅ 结构正确。
- 问题：
  - P1：仍无全局搜索/⌘K；"人才与能力"在侧栏是一个入口，但截图集中没有任何其界面证据（与 CURRENT_STATE"Capability 用户语言"P1 缺口一致）。
  - P2：当前项高亮为浅灰底 + 黑字，选中态与 hover 态区分弱（APPROXIMATE 同为 #f0f0f0 系）。

## 2. CEO 工作台

**A 代**（ceo-desk，深色截图）：
- 布局：顶部 meta 文字条（尚未启动·星期五｜公司运行第 等待公司创建 天｜经营日状态…）→ 欢迎卡（含"创建公司"绿色按钮）→ 三个纵向堆叠的"等待"框（待 CEO 输入/待运行记录/待结果归档，每个内部一条 bullet 空文案）→ 右栏"公司脉搏"6 格（全部"等待启动"）→ 底部"真实结果回流"。
- 问题：
  - P0：**视觉重心错误**——首屏最大的可点对象是"创建公司"绿色按钮，但页面标题是"今日经营"；空态把"今日经营"六个维度全部以"等待启动"重复六遍，信息量为零却占据半屏。
  - P1：meta 文字条用竖线分隔 5 组状态词，纯文本无层级，像日志行不像"今天的工作台"。
  - P1：三个"等待"框样式完全相同、纵向堆叠，无注意力优先级——CEO 注意力面恰恰最需要优先级。
  - P2：深色模式绿色 accent 与品牌冻结紫色无关（S1）。

**与竞品初步对照**（详细 A/B 见 CROSS_PRODUCT_MATRICES）：ChatGPT/Linear 类产品的空态是"一个主行动 + 少量解释"；Curis A 代空态是"六个零值仪表 + 三段重复空话"。

## 3. 工作空间门户 / 业务空间（A 代 workspace-portal、business）

- P0：**四个 0 值统计卡（活跃周期/待 CEO 验收/阻塞工作空间/最近证据）是典型网页后台语汇**；在新公司 first-run 时全部为 0，占据黄金位置。
- P1：**双空态重复**——上半屏"公司空间还没有办公室"卡内嵌"创建第一间办公室"卡，下半屏又有"公司还没有业务空间 / 第一间办公室还没有建立"卡；同一件事说三遍，CTA 文案还不一致（开始创建公司 → / 开始创建公司）。
- P1：筛选 segmented（运行中 0/装修中 0/已归档 0）在没有任何对象时展示，是把空状态当过滤器用。
- P2："装修中"作为状态词口语化且与其他状态（运行中/已归档/阻塞）不同体系。

## 4. 专业工作区（Four-Pane / Surface 体系）

**B 代（multi-surface 截图）是当前最接近 Frozen Shell Contract 的一代**：导航轨 + Domain Nav（SURFACE 列表：经营总览/研究与洞察/内容运营/增长与评估/反馈/商业化）+ Main + Utility/Employee 面板。✅ 骨架正确。逐项找茬：

- P1：**顶部面包屑在 Utility 打开时被压缩换行**（06 截图中"业务空间/内容增长部/小红书运营"折成 3 行，与右侧 Surface tabs（总览/研究/内容/增长/反馈）挤压），层级表达崩溃。
- P1：**Research Surface 的对象卡（趋势/竞品/受众三联卡）信息密度好，但证据（evidence）行、交接（handoff）行、责任人 chip 全部平铺在卡内**，卡高 ~250px 三列排满后仍出现大量留白差异；"交接至 内容运营：生成 3 个实测选题"用虚线框 chip 表达，可点性不可辨（是链接？是按钮？是状态？）。
- P1：**Utility 面板（06）信息太薄**：对象标题 + 一段预览文字 + 三个按钮（发布前检查/编辑正文/查看历史版本），没有元数据（负责人、状态、版本号、关联证据、更新时间全缺）；与 Employee Quick Panel（03，字段完整：当前责任/当前工作/状态/当前交接/最近成果）形成明显的深度不均。
- P1：**Employee Quick Panel 是全产品最好的组件**（字段层级正确、责任→工作→状态→交接→成果叙事完整），但它的四个动作按钮（直接对话/查看当前工作/查看交接/打开完整员工工作站）里"打开完整员工工作站"指向的完整工作站没有任何截图证据——又是"有一层面没一层"。
- P2：状态 chip 体系（制作中/待发布/待确认/进行中/已归档）色彩语义不统一：制作中=绿、待确认=amber、进行中=绿 outline、已归档=灰；"进行中"与"制作中"并存（一个 Surface 用"制作中"、另一个用"进行中"）。
- P2：头像 chip（陈/李/王 20px 圆形字母头像）+ 姓名 + 角色三类信息重复出现在对象卡的行尾，一行内出现 [AI][陈真][制作中] 三个 chip，密度过载。

**A 代（workspace-runtime-xhs，旧）**：整页是单列长滚动 dashboard：4+1 统计卡 → 9 节点 pipeline chip 行（信息搜集→拆解→分析→产出→待发布→数据→复盘→提升→归档）→ 当前内容队列 → 真实结果与 CEO 判断 → 下一轮优化建议 → 底部"当前能力组合"条。问题：
- P0：**这不是 Four-Pane Workspace Shell**——没有 Context/Utility/Conversation 空间，是营销页式长图布局；与 Frozen Shell Contract（#45）直接冲突。作为"当前 UI"证据必须标记为 A 代旧物。
- P1：9 chip pipeline 每个都带两行小字 + 状态，横向溢出风险高（1440 已满宽）。
- P1："当前能力组合：GPT-5 · 内容制作 AI … 预估 ¥0.18"直接把实现细节（模型名/工具清单）平铺在页面底部，用户语言缺失（与 CURRENT_STATE "Capability 用户语言"P1 一致）。

## 5. 会议

- A 代 meeting-light：整页 90% 留白，一张卡 + 一个 556×84 的巨型黑按钮"开始创建公司 →"。P0：**把"创建公司"作为会议页的最大 CTA 是层级错误**（会议空态的正确主对象应是"会议会在公司运行后出现"的一次解释 + 返回入口）。P2：右上角"没有进行中的会议"pill 是全页唯一状态信息。
- A 代决策室（decision-room，未附截图，同代样式）：同问题族。
- 与 Frozen "Meeting Room 1440×900 UI ACCEPTED"（Figma 214 系列）不在一个设计体系——会议已有被接受的 Figma 基线，A 代原型与其冲突（S3 的又一实例）。

## 6. 资料库（A 代 knowledge-light）

- P1：**四联统计卡（可用资料 —/最近更新 —/已连接来源 0/待确认来源 —）在空库时全部为占位符**，占首屏 1/4。
- P1：双栏（公司资料 / 外部来源）中，左栏有搜索 + 分类 chip（全部/竞品/平台规则/内容素材/研发），右栏整块只有一句"还没有已连接的外部知识来源"——左右信息密度严重失衡。
- P1：与已 ACCEPTED 的 Figma 资料库基线（187:2 / 187:276 / 187:550 / 187:824，Reading-first + Reference Row 结构）完全不同代。A 代原型不能代表已验收方向。
- P2：底部"使用方式：…"整行小字说明，是开发者注释式的产品文案。

## 7. 经营洞察（A 代 operating-light）

- P0：**公司脉搏 6 卡（价值/执行/供给/风险/方向/连续性）每张内容完全相同**（"还没有真实经营记录；首轮运行或结果回传后，这个维度才会有状态。"），六张卡 × 同一句话 = 视觉噪音；且风险卡的"等待启动"用了红色/粉色 pill（APPROXIMATE），给空态错误地染上告警色。
- P1：顶部 meta 条与 CEO 工作台同病（运行第 128 天｜阶段｜最近决策｜待处理 3 项决策·1 项阻塞｜同步 09:47 纯文本行）。
- P1：与已 ACCEPTED 的 Operating Intelligence Figma 基线（172:3 系列，Overview/Scoped Analysis/Explore/Report 四状态）不同代。

## 8. AI 组织 / 人才与能力 / 员工

- **全套资产中没有任何一张人才与能力（Expert/Marketplace/Skill）界面截图**，也没有 Employee Detail / Employee Workstation 完整页截图。CURRENT_STATE 也把"Employee/Result 最终工作面"列为 Remaining Core P1。
- P0：**Curis 最差异化的对象（AI 员工）在当前 UI 资产里没有一张像样的脸**：只有 B 代的 Quick Panel 抽屉。招聘、Skill 安装、能力绑定、Employee Detail 全部无 UI 证据（实现侧 Talent & Capability 曾登记 IMPLEMENTED/ACCEPTED，但视觉资产缺位）。
- 这正是本轮竞品研究 Workbuddy Expert / Coze Agent 卡片拆解的直接服务对象。

## 9. Composer / Conversation / CEO 助理

- B 代 Assistant 面板（07）：右侧 355px 抽屉，头部（AI 头像 + "CEO 助理 / 公司级全局员工 · aware of AI 科技"）+ 位置 chip + 消息气泡。
  - P1：**截图中看不到 Composer 输入区**（面板下半部为空），全局助理的输入面不存在或不可见；"可拖动、可收起、跨七区"的 Floating Assistant（Phase B 已实现）在视觉资产中无对应。
  - P1：助理回复是大段纯文本（三条堆叠），无结构化（建议卡/决策卡/引用），与"工作伴侣"定位不符——像客服回复不像 copilot。
  - P2："aware of AI 科技"是内部术语（awareness 机制）暴露给用户。
- A 代悬浮"询问助理"气泡：右下角 pill + "正在等待 CEO 表达经营意图"状态行。P2：等待状态文案把系统内部状态（等输入）当作常驻广告位。

## 10. 视觉系统逐项（跨页汇总，APPROXIMATE）

| Token | A 代 | B 代 | 冻结标准 (V1) |
|---|---|---|---|
| 品牌强调 | 绿 `#22c55e` 系 | 无品牌强调（黑主按钮） | `#806BE5` 紫 |
| 主按钮 | 黑底白字 / 绿底白字 | 黑底白字 | 未执行 |
| 卡片边框 | 1px `#e5e7eb` 系 | 1px `#e5e7eb` 系 | 未执行 |
| 卡片 radius | ~12px | ~10px | 未执行 |
| 页面标题 | 28–32px 粗 | 20–24px 粗 | 未执行 |
| 正文 | 13–14px | 13–14px | 未执行 |
| 阴影 | 几乎无（平面） | 几乎无 | 未执行 |
| 状态色 | 绿/amber/红 混用 | 绿/amber/blue | 未执行 |
| 密度 | 低（大卡大留白） | 中 | 未执行 |
| 深色模式 | 有（整页深灰 `#111827` 系） | 未见证据 | P2 记录中 |

结论：**冻结的 CURIS_VISUAL_STANDARD_V1 在任何一代资产中都未被消费**。Final UI Master 重启时视觉层需要从 token 层重建，而不是修修补补。

## 11. 问题清单汇总（Problem Register 输入）

P0 Directional（方向性，动摇观感）：
1. 三套视觉语言并存，冻结视觉标准零消费（S1）
2. 已废弃"办公室"模型仍在 UI 资产中流通（S2）
3. 两代 IA 冲突且无标记，设计研究易被旧代误导（S3）
4. 空状态 = 报表后台（S4、§2、§3、§6、§7）
5. CEO 工作台/经营页视觉重心与注意力模型错误（§2、§7）
6. AI 员工（核心差异化对象）没有完整 UI 脸面（§8）

P1 Structural（结构性）：
7. 网页后台语汇（统计卡/筛选器/面包屑）代替桌面对象语汇（S5）
8. 无全局搜索 / ⌘K / 命令面（B 代侧栏 + 所有页面）
9. Four-Pane 中 Utility 深度不足、Employee Workstation 完整页缺位（§4）
10. 面包屑/顶栏在多面板开启时崩溃（§4）
11. 全局助理无可见 Composer、回复无结构（§9）
12. 状态词汇不统一（制作中/进行中；装修中）（§3、§4）
13. 会议页层级错误 + 与已验收 Figma 基线脱节（§5）
14. 实现细节（模型名/工具清单/aware 机制）暴露为用户文案（§4、§9）

P2 Polish（打磨）：
15. 选中/hover 态区分弱；chip 体系色彩语义不统一（§1、§4）
16. 侧栏标语重复；空态文案啰嗦说三遍（§1、§3）
17. 深色模式仅 A 代有且用错误 accent（§10）
18. 头像 chip 行密度过载（§4）

---

## 12. 与竞品 A/B 对照（摘要表；完整矩阵见 CURIS_COMPETITIVE_CROSS_PRODUCT_MATRICES.md）

| Surface | Curis 现状 | 竞品参照 | 差距本质 |
|---|---|---|---|
| 员工/专家卡片与详情 | 仅 Quick Panel 抽屉；无 Detail 页证据 | Workbuddy Expert 卡+详情、Coze Agent 配置页、Claude Projects | 员工作为"公司成员"的脸面缺位；身份/责任/能力/工作/成果没有可浏览的对象页 |
| 工作进度 | 无独立呈现（A 代以 pipeline chip 装饰） | Zcode todo+工具卡、Manus 任务列表+Computer 面板、Devin plan/browser pane | Curis 有 Work/Result Runtime 但没有"正在工作的员工"可视化 |
| Conversation/Composer | 全局助理无 Composer 证据；回复纯文本 | 全部竞品：Composer 是第一公民（附件/模型选择/工具开关） | Composer 成熟度是"像不像桌面 AI App"的决定项 |
| 结果/产物 | 成果库 nav 存在；无 Result 视图证据 | Manus 交付物、Claude Artifacts、Devin PR/replay | Result→Evidence 链是 Curis 强项，但无消费面 |
| 空状态 | 零值仪表盘 | 竞品用单一主 CTA + 叙事 | 首跑体验决定第一印象 |
| Settings | A 代仅侧栏"设置"一项，无任何 Settings 页证据 | 竞品 Settings 均为多节完整面（见 SETTINGS_MATRIX） | Curis Settings 产品面完全缺证据（实现有 Model Management UI 一角） |

---

## 13. C 代补充：真实前端（2026-08-13 drift audit 截图）

> 证据：`docs/reviews/20260813_current_state_product_drift_audit/*.png`（真实 frontend/ 运行截图，早于 09-09 Phase B 集成，但代表实然 UI）。

- C1（P0）：**内部术语直接暴露给 CEO**——"当前没有等待、失败或缺失的 SimulationRun。"（SimulationRun 是 Runtime 对象名）；"来源：Company Runtime"；"Workspace 是业务运行单元"。CEO 用户语言完全缺失。
- C2（P0）：**全局助理以"未命名 Assistant / 尚未设置角色"为标题**出现在 CEO 工作台右侧——默认身份未兜底，第一印象是"半成品"。
- C3（P1）：助理面板内部又是三张 0 值统计卡（待处理 0 / 风险提示 0 / 我正在关注 0）+ 与主区重复的"今日简报"，且底部有 60 字免责声明常驻；助理面板 = 迷你报表 + 表单，不是对话伴侣。
- C4（P1）：助理面板有"自动判断 / 查询 / 执行"三段模式切换——这是一个好概念（对应 Work 的三种介入深度），但无任何解释、无选中态差异说明。
- C5（P1）：**真实 Settings 页只有"公司设置"**（公司档案：名称/法人代表/注册地/行业 + 品牌主题 + 通知偏好，且标注"本地草稿态·未接入真实数据"）；页脚直接写"（遵循 §10.1，不修改全局 --ui-* token）"——**开发者规范注释被当作用户文案渲染**。模型、Provider、员工、权限、隐私、数据、存储等设置面全部不存在（呼应 WS10 Settings 行）。
- C6（P1）：真实前端侧栏仅 4 项（CEO 工作台/经营/业务版图/工作空间）+ "更多"折叠——与七区结构、A 代、B 代都不同，是**第四套 IA**。七区在实然前端中尚未落位（Phase B 前截图，需 09-09 后重新取证）。
- C7（P2）：左下角用户身份 chip（"总结·Admin"类）与头像 fallback 字母"N"无身份语义。
- C8（P1）：**错误态是全屏裸错误**——"加载失败 / Failed to fetch"+ 单个"重新读取"按钮（见 drift audit `organization.png`、`knowledge.png`）：无错误解释、无返回/替代路径、无重试进度、英文原始报错直接暴露；且当时侧栏多个目的地（AI 团队、知识库）直接落在死页上。（注：知识库等区域在 08-13 后已有验收实现，此处证据用于错误态设计本身的缺失。）

## 14. D 代补充：coverage-exploration-2026-08-17 + department-business-work-surface-2026-08-18（当前最好的设计资产）

> 证据：`curis-ui-prototype/coverage-exploration-2026-08-17/`（11 页 + index，含 00-PAGE-STATE-INVENTORY / 01-DESIGN-TOKENS / 02-QUALITY-REVIEW 自评 PASS 4-5 分/维）；`department-business-work-surface-2026-08-18/`。本审计以 headless Chrome 渲染 `01-ceo-desk / 04-talent-market / 07-settings` 后目测（注：headless 渲染可能损失部分 JS 布局，结论以其 HTML 结构与自评报告交叉验证）。

**D 代是什么**：消费 Frozen tokens.css + Shell Contract 的全产品覆盖原型（CEO 工作台/业务空间/组织中心/人才市场/资料库/会议/设置/RD Workspace/XHS Workspace/全局搜索/状态集）。六区导航、四 Pane、无全局 Topbar、Employee Row 两行结构、Composer 语义槽位（含 Execution Selector 区分 Agent≠模型）、Result Reference→Utility 均合规。视觉方向"安静、信息密集、低表面复杂度"（对标 Linear/Notion 手感），Anti-Slop 自评 5/5。**这是 Final UI Master 重启时最可信的输入池。**

D 代找茬（不推翻其"最佳输入"地位）：
- D1（P0，继承 G-01）：**D 代深色主题 accent 是 `#32f08c` 绿**（沿旧 Frozen Spec），与 Visual Standard V1 `#806BE5` 仍然冲突。accent 裁决悬而未决，D 代不是视觉终点。
- D2（P1）：**字段呈现是"标签堆叠"而非"对象卡"**——人才市场专家详情为 身份/擅长/能力/案例/来源/招募/许可·授权 逐行 label+value，无头像档、无能力可视化、无安装状态丰富度；与 Workbuddy Expert / Coze Agent 的市场级卡片语言差距大。D 代解决"有没有"，未解决"是不是产品"。
- D3（P1）：**员工详情有骨架无工作面**——组织关系/长期责任/当前责任/能力 chips/最近结果/状态 已列全（好），但无 Conversation、无 Work 进度、无 Result 消费区；"打开完整员工工作站"的完整形态仍不存在于任何一代。
- D4（P1）：**设置与全局搜索在 D 代仅为 IA 骨架**（设置五类：个人偏好/公司设置/AI 与能力/权限与数据/运行与成本；全局搜索页存在），但字段级内容未填充，且未进入任何实现。
- D5（P2）：headless 渲染下部分页面（01-ceo-desk）四 Pane 高度分配失衡（Utility 内容占据大面积），需在浏览器中复核。

**修正前文两处结论**：
- §8 P-TAL-01 修正：人才与能力**有** D 代 IA 骨架（浏览/招募流程/已安装 × 专家/技能/连接器 + 专家详情字段），但**没有产品级市场/详情界面**；结论仍为 P0 缺"脸面"，证据补 D 代。
- §12 Settings 行修正：Settings 有 D 代五类 IA 骨架（UI ONLY），实现侧仅公司档案草稿——状态为 UI ONLY + PARTIAL 实现，非完全缺失。

## 15. 审计边界声明

- 本审计基于仓库内现有 PNG/HTML 资产；当前实现（frontend/ Next.js + Tauri 桌面）的运行时截图未包含在资产内，前端代码结构与 token 由 CURIS_UI_EVIDENCE_CATALOG.md 单独盘点。
- A 代原型（curis-ui-prototype/p1-preview 等）按其内容与词汇判断为 2026-08 中旬前产物，与 B 代 multi-surface 截图（1440，含七区导航）不同代；两代均非 Final UI Master（PAUSED）。
- 本审计不推翻任何 Frozen Product Structure；§0-S2/S3 指出的是资产与 Authority 的冲突，应通过标记 A 代资产为 HISTORY/VISUAL REFERENCE ONLY 解决。
