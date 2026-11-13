# Curis Full Product HTML Design Prototype

> 性质：**DESIGN PROTOTYPE / DESIGN FIXTURE** — Final UI Master 之前的全产品视觉与交互验证载体。
> 不是 Frontend 实现、不接 Runtime、不写真实数据、不是 Product Truth。
> 入口：直接用浏览器打开 `index.html`（无需构建、无依赖、无网络）。
> 状态：**READY FOR CEO / CHATGPT REVIEW — 不自行进入 Final UI Master。**

## 运行

```bash
open index.html            # 或任何静态服务器
# 带参数：
index.html?theme=dark#/ceo     # 深色
index.html#/workspace/ws-xhs   # 内容增长专业工作面
index.html#/ceo?search=1       # 打开全局搜索
index.html#/ceo?assistant=working  # 助理状态（collapsed/expanded/working/result-ready）
```

## Route / Surface Index

| Route | Surface | Blueprint | 说明 |
|---|---|---|---|
| `#/ceo` | CEO 工作台 | P2 | 简报/待决定/正在运行/最新结果/公司脉搏（次级）；状态：normal/emptyFirst/needsCEO/error |
| `#/business` | 业务空间列表 | P3 | 3 个 Business（内容增长 / Curis 产品研发 / 宠物寄养·激活中）；空间工程部与数据分析部为原装部门，不经营自有 Business |
| `#/business/:id` | Business 详情 | P3 | 四部分合同：定义/经营状态/Workspace 目录/业务团队；激活中业务显示激活链（FLOW C） |
| `#/activate` | 新业务意图 | P3/C1 | CEO intent → Curis 理解 → 研究 → 建议 → CEO Gate |
| `#/workspace/ws-cg[/:surface]` | **内容增长工作空间**（内容增长专业） | P4 | 统一工作空间：六 Surface Domain Navigation + 团队运转（选题→调研→文案→视觉→发布）+ 内容运营面内 Channel Account 发布目标（内容 Variant 按账号复用）；FLOW A |
| `#/workspace/ws-rd[/:surface]` | **Curis 研发**（研发专业） | P4 | 交付总览/开发/评审/测试验证/发布 + 状态链（产品→架构→Runtime→Adapter→Test→Review）+ 灰度 Decision + Diff Utility；FLOW B |
| `#/workspace/ws-pet` | 宠物寄养工作空间（Generic） | P4/C2 | 新业务首个 Workspace |
| `#/org[/map\|dir]` | 组织中心 | P5 | 公司版图（4 部门）/ 员工目录（16 员工） |
| `#/employee/:id[/:sec]` | Employee Detail / 工作站 | P6 | 当前工作/责任/能力/对话/结果/设置 六 Tab |
| `#/talent[/:tab]` | 人才与能力（人才市场） | P7 | 外部能力发现：专家（Curis-ready 官方模板 / 外部 Candidate）/ 技能 / 连接器 三 tab + 分类 + 排序 + 搜索 + 安装态；公司内部员工在 组织中心 → 员工目录 |
| `#/skill/:id` | Skill 详情 | P7 | 用户语言/触发方式/权限/绑定员工 |
| `#/insights` | 经营洞察 | P11 | 司衡工作位：指标/归因/报告建议/Decision |
| `#/knowledge[/:id]` | 资料库 | P9 | 引用空间：来源/适用范围/被引用 |
| `#/meeting[/:id]` | 会议 | P10 | 列表/房间：参与者/议程/决议→Work |
| `#/models` | **模型配置**（左下头像菜单 → 模型配置 / AI 能力设置） | P12 | 主流厂商全列表（OpenAI/Anthropic/Gemini/DeepSeek/通义/豆包/智谱/MiniMax/Kimi/Mistral/xAI/Groq/硅基流动），输 Key 保存即用；对话内随时切换
| `#/settings[/:sec]` | Settings（14 节） | P12 | personal/company/models/providers/skills/mcp/connectors/permissions/memory/usage/notifications/appearance/shortcuts/about |
| `#/work/:id` | Agent Work 进度 | §8 | Plan→Steps→当前动作→工具（折叠）→协作→交接→elapsed/cost→Result 过渡 |
| `#/decision/:id` | CEO Decision | P2 | 白话 Decision + 证据 Reference + 三选项 |
| `#/result/:id` · `#/results` | Result / 成果库 | §9 | 证据链/被引用/继续工作；Utility：Preview⇄Source |
| `#/conversation/:empId` | 对话 | §9 | User/Employee 消息 + 文件引用 + 引用 + 工具折叠 + 成本内联 |
| 全局 | ⌘K 搜索 / 通知 / Floating 助理 | P13/P14/§10 | 搜索浮层（类型 chips+分组结果+预览）；通知四类；助理四态可拖动 |

## Fixture 说明

全部数据在 `js/fixtures.js`，**全部为 DESIGN FIXTURE**。语义消费 `PROFESSIONAL_BUSINESS_EXISTING_TRUTH.md`：
- 原装组织：空间工程部（沈砚/顾行/策明/苏格/梁筑/程验）+ 数据分析部（司衡）——姓名均为 fixture。
- 内容增长部（D 代 fixture）：周宁（部长）/ 陈真（资深运营·Business/Workspace Leader）/ 林月（调研·文案）/ 苏晴（视觉）/ 何川（数据分析）；Business **内容增长**，Workspace **内容增长工作空间**（统一空间内复用内容，按 Channel Account：小红书·AI 科技 / 抖音 / 公众号 分发）；默认流程：选题→调研→文案→视觉→发布。
- 研发部（D 代 fixture）：林涛（部长/Tech Lead）/ 孙浩（Workspace 负责人）/ 王琳（产品）/ 周岚（开发）/ 赵敏（QA）；Business Curis 产品研发，Workspace **Curis 研发**；默认流程：产品→架构→开发→测试。
- 全文禁用"办公室"词汇（08-24 CEO 裁定 Office 退出语义）。

## State 说明

- 页面级状态由左下 **STATE · DESIGN TOOL**（虚线框，设计测试工具，非产品 UI）切换；CEO 工作台：normal/emptyFirst/needsCEO/error；Workspace：normal/emptyFirst/working/error；Result：normal/loading/error。
- Composer 状态：idle（可输入）→ running（发送变停止 + "工作中·已排队"）→ 完成回执；禁用态见 code。
- 助理四态：collapsed / expanded / working / result-ready（`?assistant=` 或 ⌘J 循环切换）。
- 主题：默认 Light；`?theme=dark` 或右上切换；1024 宽自动收起 Context、Utility 变抽屉。

## 文件结构

```
index.html            单入口（hash 路由）
css/tokens.css        Frozen --ui-* 令牌（复制自 curis-ui-prototype/_system）
css/curis.css         V1 accent 仲裁（#806BE5，见 REVIEW）+ 组件样式
js/theme.js           主题控制（复制自 _system）
js/fixtures.js        DESIGN FIXTURE 数据
js/components.js      渲染组件（emp-row/work-card/composer/msg/decision…）
js/views-core.js      CEO/组织/员工/人才/洞察/资料/会议/设置
js/views-business.js  业务/工作面/Work/Decision/Result/对话
js/app.js             Router/四Pane/搜索/通知/助理/State 工具
screenshots/          24 张 Light + 5 张 Dark 关键 Surface
PROFESSIONAL_BUSINESS_EXISTING_TRUTH.md   Content Growth / RD 既有成果汇总
CURIS_FULL_PRODUCT_HTML_PROTOTYPE_REVIEW.md  验收评审记录
```

## 边界

DO NOT MODIFY PRODUCT AUTHORITY / RUNTIME / PRODUCTION FRONTEND / FIGMA；不 commit / push。完成后 STOP FOR CEO / CHATGPT REVIEW。
