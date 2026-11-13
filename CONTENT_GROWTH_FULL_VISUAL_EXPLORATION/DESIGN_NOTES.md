# Content Growth — Full Interactive Visual Exploration
## Design Notes for CEO Review

### 整体方向
沿用 06 Curis Hybrid 的色彩体系：Quiet Dark Navigation（#3A4A52）+ Warm Neutral Working Surface（#F1EFDD）+ Soft Green Focus（#8FB850），并以独立语义状态色承载健康/阻塞/风险。目标是把 Production Overview 那种「简洁、干净、紧凑但不拥挤、层级清楚」的质量扩展到全部七区。

### Shell 与导航
- 统一单入口 `index.html`，七区、详情、Work Surface、Employee、Conversation、Decision 全部在同一应用 Shell 内切换。
- 左侧导航固定 214px，使用 quiet dark；当前区用 soft green 激活态，徽标数字只在「需要推进/异常」口径上显示。
- 顶栏保留返回、面包屑、经营边界、团队持续经营状态；高频入口保持克制，不堆砌。

### 信息密度与层级
- 经营：Portfolio 表格首屏给出账号组合健康、重点资源、Pipeline、结果与下一轮决定；Account Scope 切换作为全站唯一入口。
- 研究与选题：灵感 / 选题池 / Reference / Proposal 分层；提案详情左侧封面、右侧关键判据与目标交付，底部展开「目标交付」确认开工。
- 内容制作：队列 → Workbench；Workbench 顶部是内容标题与元数据，中间是方法步骤条，下面是当前步骤产物、版本历史、执行结果与交接。
- 发布、账号、复盘、素材：各自按业务内容选择最合适的表达（日历/列表、档案卡片、KPI+图表+判断、紧凑列表/大图网格）。

### 关键交互
- 导航切换、Work 进入、Employee Modal、Conversation Drawer、Decision Modal、Artifact 版本展开均已通过 Puppeteer 验证，无运行时错误。
- Conversation 保留四种范围（team / employee / work / step）， drawer 内显示实际接收人、责任原因、并行工作提示。
- Workbench 的版本历史展开后可见 v1/v2/v3 与责任人/原因/当前状态。

### 已知问题 / 下一轮待解决
1. **favicon 404**：本地服务器无 favicon，控制台报 404，不影响功能。
2. **颜色标记未完全 token 化**：data.js / visuals.js / analytics-r5.js 中仍有少量平台色与图表色使用硬编码 hex； production 落地时应映射到统一 tokens。
3. **Analytics 图表配色**：当前 BI 颜色偏冷/饱和，与新暖色工作面尚未完全调和。
4. **Workbench 页面较长**：步骤多时需要滚动；可考虑为长 Workbench 增加步骤锚点或 sticky step rail。
5. **无 URL deep link**：当前状态仅保存在 JS 内存，刷新后回到经营区；CEO review 用本地交互足够，后续如需分享需补充路由序列化。
6. **硬约束提醒**：本探索目录使用独立的 `styles.css` tokens；正式 frontend 实现需切换到 `--ui-*` 设计 tokens，禁止 inline hard-coded hex。
