# Curis UI 原型页面结构化规格

来源目录：`/Users/yy/Documents/Curis AI Workspace/curis-ui-prototype/`
抽取范围：根目录全部 **20 个 .html 文件**（子目录 `p0-preview/`、`p1-preview/` 仅含 PNG 截图，`_system/` 为共享 CSS/JS，均无 HTML）。
抽取重点：隐含路由、标题与面包屑、主区块与 UI 组件、示例数据字段与样例值、导航跳转、三业态差异。CSS 细节已忽略。

---

## 0. 全局共性（所有业务页共享）

### 0.1 共享资源
| 资源 | 作用 |
|---|---|
| `_system/tokens.css` | 设计令牌（`--ui-sp-*`、`--ui-fs-*`、`--ui-r-*`、`--ui-ctl-h-*`） |
| `_system/shell.css` | 全站外壳（侧栏 + 52px 顶栏） |
| `_system/theme.js` | 主题（dark / light / system） |
| `_system/canonical-nav.js` | 统一侧栏导航注入 |
| `_system/assistant-drawer.js` + `assistant-drawer.css` | 助理抽屉（仅 workspace-runtime-* 与 shell-reference、decision-room 引用样式） |
| `_system/runtime-capability.js` | 运行现场「当前能力」下拉（`#runtimeCapSelect`），与 AI 团队页能力库经 localStorage 同步 |
| `curis-prototype.js`（724KB） | 共享交互层：NAV_MAP 导航映射、toast、成果库/知识库/财务页动态渲染、状态存取（`readState()`） |
| `curis-api.js` | 真实后端 API 客户端，仅 `ceo-day-demo.html` 使用 |

### 0.2 全局侧栏（4 组 14 项，顺序固定）
| 分组 | 项 | 图标 | 目标页 |
|---|---|---|---|
| 公司 | CEO 工作台 | ◆ | ceo-desk.html |
| 公司 | 经营 | ◎ | operating.html |
| 公司 | 业务 | ◇ | business.html |
| 公司 | AI 团队 | □ | ai-organization.html |
| 工作空间 | 工作空间门户 | ▣ | workspace-portal.html |
| 工作空间 | 软件工作室 | ⌨ | workspace-runtime-software.html |
| 工作空间 | 短视频 | ▶ | workspace-runtime-shortvideo.html |
| 工作空间 | 小红书 | ✎ | workspace-runtime-xhs.html |
| 经营工具 | 会议工作台 | ⌘ | meeting.html |
| 经营工具 | 决策室 | ⚖ | decision-room.html |
| 公司资源 | 成果库 | ▦ | assets.html |
| 公司资源 | 知识库 | § | knowledge.html |
| 公司资源 | 财务 | ¥ | finance.html |
| 公司资源 | 日历 | ❑ | calendar.html |

侧栏底部固定标语：**「事实先于观点。共识必须回到责任与结果。」**
`ceo-desk.html` 侧栏额外含「设置 ⚙ / 帮助 ?」（`href="#"`，点击弹 toast「该入口将在设置中心接入」）。

### 0.3 顶栏（52px）
`Curis / <一级> / <二级>` 面包屑 + 右侧状态胶囊（同步状态 / Assistant 在线 / 待 CEO 决策计数）+ 主题切换（深色 / 浅色 / 自动）。

### 0.4 路由映射总表
| 文件 | 隐含路由 | 页面性质 |
|---|---|---|
| index.html | `/` | 0 秒 meta redirect → founding-flow |
| founding-flow.html | `/onboarding` | 6 步创建公司向导 |
| ceo-desk.html | `/ceo-office` | CEO 工作台（首页） |
| operating.html | `/ceo-office/analytics` | 经营分析 |
| business.html | `/ceo-office/projects` | 业务组合 |
| ai-organization.html | `/ceo-office/team` | AI 团队办公室 |
| workspace-portal.html | `/ceo-office/workspace` | 工作空间门户 |
| workspace-studio.html | `/ceo-office/workspace/studio` | 装修台（搭建方案画布） |
| workspace-runtime-software.html | `/ceo-office/workspace/software` | 研发运行现场 |
| workspace-runtime-xhs.html | `/ceo-office/workspace/xhs` | 小红书运行现场 |
| workspace-runtime-shortvideo.html | `/ceo-office/workspace/shortvideo` | 短视频运行现场 |
| workspace-runtime-department.html | `/ceo-office/workspace/template` | 未装修通用模板 |
| workspace-shell-reference.html | `/ceo-office/workspace/_shell-reference` | Shell 参考原型（开发用） |
| decision-room.html | `/ceo-office/decisions` | 决策室 |
| meeting.html | `/ceo-office/meeting` | 会议工作台（骨架页） |
| assets.html | `/ceo-office/assets` | 成果库 |
| knowledge.html | `/ceo-office/knowledge` | 知识库 |
| finance.html | `/ceo-office/finance` | 财务与经营 |
| calendar.html | `/ceo-office/calendar` | 公司日历 |
| ceo-day-demo.html | `/dev/ceo-day-demo` | 真实后端 API 联调页 |

---

## 1. index.html — `/`

- 标题：`Curis`
- 无面包屑。`<meta http-equiv="refresh" content="0;url=founding-flow.html">`
- 唯一内容：文案「正在进入 Curis…」+ 链接「开始创建公司」→ founding-flow.html

---

## 2. founding-flow.html — `/onboarding`

- 标题：创建公司向导；顶部为 **6 步进度导航**（非面包屑）：`欢迎 → 创业简报 → 公司设定 → 首个业务 → AI 团队 → 启动检查`
- UI 组件：步进器 + 分步 section（`data-step="0..5"`）+ 表单 + 卡片选择 + 检查清单 + 遮罩层

### 区块（自上而下）
1. **step 0 欢迎**：品牌标识、主 CTA「从零创建公司」`goToStep(1)`、次 CTA「使用业务模式」`selectTemplate()`、旁链「进入 CEO 工作台」→ ceo-desk.html
2. **step 1 创业简报**：助理气泡 + `#ceo-intent` textarea；按钮「让 Assistant 代拟」`draftBrief()` / 「填入示例」`fillSampleBrief()`；生成 6 个可 *接受 / 跳过* 的字段卡
3. **step 2 公司设定**：表单 + 实时「公司卡预览」
4. **step 3 首个业务**：4 张业态模板卡（可选中）+ 业务表单
5. **step 4 AI 团队**：6 张 AI 员工卡 + 能力容量列表 + CEO 审批 checkbox `#approve-team`
6. **step 5 启动检查**：检查清单（5 项）+ 3 种运行模拟 + `#launch-btn`（默认 disabled，勾选审批后解锁）→ `launchCompany()` → 遮罩「正在创建你的公司」→ 进入 CEO 工作台

### 数据结构

**创业简报 brief**（6 字段，每项可接受/修改/跳过，跳过标「待补充」）
```
why      为什么存在？   "一人公司的 CEO 需要一支真正能承担责任的 AI 团队…"
who      服务谁？       "第一阶段先服务 Curis 自己的 CEO…"
bet      第一个业务方向 "先用 Curis 自己的 AI 研发团队持续完善 Curis…"
outcome  第一个可验证结果 "30 天内完成 Curis v0.2，CEO 能真实走完创建公司…"
duty     最小责任       "产品方向、范围取舍、重大资源、真实验收…由 CEO 最终负责"
unknown  未知假设       "AI 团队能否在不增加 CEO 协调负担的情况下稳定交付…"
```

**公司对象 company**
```
name    "Curis"
legal   一人有限责任公司 | 个人独资企业 | 合伙企业 | 先以自然人主体运行
charter "帮助一人公司的 CEO 从零搭建并持续经营一家 AI 公司…"
values  ["证据优先","CEO 负责","透明交付","持续学习"]
```

**业务模板 template**（`data-curis-template`）— 与三业态严格对应
```
software 软件开发 · Curis 自研   "产品、研发、测试与 CEO 验收协同"
xhs      内容增长 · 小红书       "选题、脚本、发布与平台数据回传"
douyin   抖音 / TikTok 运营      "选题、制作、发布、数据回流与复盘"
custom   自由搭建               "不套用模板，从零描述"
```

**首个业务 bet**
```
opportunity  机会描述（textarea）
outcome      "30 天内完成 Curis v0.2 验收，并由 CEO 通过首轮真实使用"
timebox      30 天 | 60 天 | 90 天
evidence     外部反馈路径：CEO 验收+产品使用反馈 / 客户合同签署+收款记录 /
             产品使用数据 API / 手动周报+客户访谈 / 第三方平台数据导入
```

**最小 AI 团队**（6 卡，各带 2 个能力标签）
```
CEO 助理 Curis    经营简报 / 决策记录
产品 AI           需求拆解 / 验收标准
研发 AI           代码实现 / 回归修复
QA AI             场景回归 / 证据整理
运行反馈 AI       反馈归因 / 改进建议
平台能力          连接器授权 / 工具配置
```

**能力容量绑定**：内容生成能力 = 墨白 80%；策略分析能力 = 星河 60%；数据回收能力 = 齿轮 50%；商务跟进能力 = 待激活（CEO 暂代）。覆盖度 4/6。

**启动检查清单**：经营意图已表达 ✓ / 公司对象已生成 ✓ / 首个业务方向已定义 ✓ / **AI 团队已获批（待确认，唯一门禁）** / 风险与待补充项已知情 ✓
**运行模拟三场景**：正常 / 缺席（CEO 离线 7 天）/ 失败（验收未通过）

---

## 3. ceo-desk.html — `/ceo-office`

- 标题：`今日经营 · CEO 工作台 · Curis`
- 顶栏：`Curis · 软件开发 工作空间 · 短视频内容 工作空间 · 同步正常 3 分钟前 · Operating · 正常模式`
- 页头元信息：`2026-08-01 · 星期五 | 公司运行第 128 天 | 经营日状态：进行中 | 助理身份：Curis · CEO 首席助理 | 上次同步 09:14`
- 侧栏「CEO 工作台」带角标 **3**

### 区块（自上而下）
1. **今日简报**（`#brief-heading`）「早上好，今天有 3 个变化需要你留意」— 三段分组：**必须决定 / 建议关注 / 已由团队处理**，每段含标题、说明、证据 chips
2. **公司脉搏**（`#pulse-heading`）六维状态 + 4 张 KPI 卡
3. **经营事项**（`#matters-heading`）3 张 article 卡（决策 / 异常 / 新机会）
4. **自动运行**（`#routine-heading`）2 条节奏 + 「查看日历」→ calendar.html
5. **经营时间线**（`#timeline-heading`）6 个时点
6. **AI 团队当前承担**（`#handoffs-heading`）4 行责任人列表
7. **日终收束**（`#closeout-heading`）4 个计数 + 「去决策室」/「编辑明日承接」

### 数据结构

**今日简报 briefItem**
```
level=必须决定  : "是否批准短视频内容 工作空间的达人合作预算扩展？"
                  detail: Growth AI 监测到 2 条爆款内容 投入产出 超阈值，建议追加 ¥12,000；
                          11:00 前未决策 → 内容排期延后 2 天
                  chips: ["投入产出 周报 08.01","达人合作清单","现金流模拟"]
level=建议关注  : "软件开发 工作空间的 v0.2 验收延迟"（第三方登录回调不稳定，影响 4 小时）
                  chips: ["阻塞工单 #S-214","测试报告"]
level=已由团队处理: "昨日用户反馈聚类已完成"（47 条反馈 → 3 个高频痛点）
                  chips: ["反馈聚类报告","改进提案 #P-18"]
```

**公司脉搏 六维**（本页仅状态，无证据链展开）
```
价值 正常 | 执行 需关注 | 供给 正常 | 风险 有风险 | 方向 未知 | 连续性 正常
```
**KPI 卡 4 张**
```
近 30 天外部结果 ¥127,400 (+12.3% 环比)
本周任务完成率   84%      (42 / 48 项)
本月 AI 运行成本 ¥3,420   (-8% 环比)
本月 AI 用量     428M     (研发 42% / 内容 31%)
```

**经营事项 matter**：`{type, title, owner, impact, checkpoint, actions[]}`
```
待决策 | 批准短视频达人合作预算扩展 | Growth AI      | ¥12K 预算 · 2 条爆款内容 · 3 位达人 | 今天 11:00 | [决策→decision-room, 查看证据]
异常   | v0.2 验收因登录回调阻塞     | Engineering Lead| 发布延迟约 4 小时                  | 今天 14:00 | [查看, 委派]
新机会 | 短视频脚本 AI 可承接 30% 产能| Content AI     | 周产量 +12 条 · 成本 -18%          | 周一 10:00 | [调查, 暂缓]
```

**自动运行 routine**：`{time, name, desc}`
- 每天 08:00 · 小红书研究与选题 · 策略 AI 收集趋势并准备 3 条候选选题；无授权时保留手动数据窗口
- 每天 18:00 · 抖音 / TikTok 数据回流 · 数据回收 AI 同步播放/留存/互动/成交；失败升级 CEO 助理

**经营时间线**：09:00 AI 团队早报 / 10:30 达人预算决策准备 / 11:00 外部合作方周会 / 14:00 软件开发检查点 / 16:00 AI 交接 Growth AI→Content AI / 18:00 日终收束

**AI 团队承担 handoff**：`{initials, name, task, status, nextFeedback}`
```
EL Engineering Lead | v0.2 阻塞排查与修复          | 排查中  | 14:00 反馈
GA Growth AI        | 达人合作 投入产出 模拟与预算申请 | 待决策  | 11:00 截止
CA Content AI       | 下周脚本排期与素材预研       | 准备中  | 16:00 交接
RA Research AI      | 用户反馈聚类与产品改进提案   | 已完成  | 今日归档
```
**日终收束**：今日改变 2 / 已做决定 0 / 未解决 1 / 明日承接 3（18:00 自动生成）

### 跳转
「决策」「去决策室」按钮 → `decision-room.html`；「查看日历」→ `calendar.html`；侧栏各项按 0.2 表。

---

## 4. operating.html — `/ceo-office/analytics`

- 标题：`经营`；顶栏 `Curis · 经营办公室 · 可重复运行阶段 · 同步正常 2 分钟前 · Operating`
- 页头元信息：`2026-08-01 · 运行第 128 天 | 公司阶段：可重复运行 | 最近决策：批准内容增长扩大 | 待处理：3 项待决策 · 1 项阻塞 | 上次同步 09:47`

### 区块（自上而下）
1. **筛选 Tab 条**（`data-filter`）：全部 12 / 待决策 3 / 异常 3 / 机会 4 / 已关闭 2 — 联动下方带 `data-type` 的卡片
2. **公司脉搏**：6 张可点击展开的 `article.pulse-card`，展开后显示 **证据链**
3. **经营分析**：4 张图表卡
4. **关注 · 风险 · 阻塞**（共 6 项，按升级状态分组：需要关注 2 / 当前阻塞 2 / 已关闭）
5. **决策队列**：表格
6. **异常队列**：3 张 article（含遏制状态与恢复计划）
7. **机会雷达**：4 张 article（高/中信号）
8. **公司约束**：3 张卡

### 数据结构

**公司脉搏 pulse**（每维：`{name, status, summary, evidence[{text, source}]}`）
```
价值   正常    近 30 天外部结果 ¥127,400，较上月 +12.3%，3/4 业务产生可验证价值
  └ 金融研究 工作空间：3/5 信号命中（外部 API · Research Lead · 08-01 08:32）
  └ 内容增长业务：+2,400 阅读，14 条有效线索（平台后台 · Growth AI · 07-31 23:00）
  └ Curis 自研：尚未产生直接收入，处于构建中（CEO 验收记录 · Engineering Lead · 07-30）
执行   需关注  2 个工作空间偏离承诺（软件开发 v0.2 延迟 4h；短视频排期落后 1 天）
供给   正常    AI 团队综合容量 72%（研发 AI 80% / 增长 AI 60% / 内容 AI 55%；计算预算使用率 61%）
风险   有风险  外部数据授权 08-08 到期；登录回调偶发失败；达人 投入产出 模拟置信度仅 68%
方向   未知    抖音 / TikTok 是否扩大投入无结论（机会评估 #O-09；缺乏跨业务协同证据）
连续性 正常    Assistant Operating 质量 A-；今日 4 项 AI 交接按时完成；47 条反馈已归档
```

**经营分析 4 卡**
```
近 30 天外部结果趋势  ¥127,400（较上月 +12.3%，成本 -8%）  折线图
本周任务状态          84% 完成率（完成 42 / 关注 3 / 阻塞 3）  环图
AI 运行成本           ¥3,420 / 本月，用量 428M（-8%）
                      分布：研发 42% / 内容 31% / 增长 18% / 研究 9%
工作空间价值贡献      金融研究 ¥58,200 · 内容增长 ¥31,400 · 短视频 ¥21,000 · Curis 自研 构建中
```

**决策队列表格** 列：决策事项 | 影响范围 | 截止时间 | 推荐动作 | 操作
```
批准短视频达人合作预算扩展 | 增长营销 AI · 影响小红书运营工作空间 | ¥12K/月 · 3 位达人（预计 14 天回收）| 今天 11:00（剩 1.2 小时）| 批准并追加排期（置信度 68%，建议先小批量验证）| 决策→decision-room
是否扩大抖音 / TikTok 运营业务 | Business Analysis AI · 新业务线 | +2 AI 员工 · 1 个新工作空间 · 首月预算 ¥8K | 明天 12:00（剩 26 小时）| 生成业务搭建方案后决策 | 生成搭建方案
是否续约外部数据供应商 | Finance AI · 金融研究工作空间 | 数据连续性 + 备用源迁移 · 年成本 ¥24K | 08-08 18:00（剩 7 天）| 续约并迁移备用源 | 查看合同
```

**异常 exception**：`{title, desc, owner, containment 遏制状态, recovery 恢复计划, actions[]}`
```
v0.2 登录回调阻塞 | Engineering Lead | 已隔离测试环境 | 切换 mock 回调完成内部验收，周一联调，预计 4h 修复
外部数据授权 7 天后过期 | Finance AI | 已启动续约流程 | 48h 内取得续约意向，同步配置备用源
短视频内容发布延迟 | Content AI | 启用备用排期 | 脚本 AI 承接 30% 产能，非核心内容延后
```

**机会 opportunity**：`{signal 高/中, title, desc, source, expectedImpact, validation, checkpoint}`
```
高 | 短视频脚本 AI 可承接 30% 产能 | Research AI | 周产量 +12 条 · 成本 -18% | A/B 测试 2 周 | 周一 10:00
高 | 用户反馈聚类显示新需求       | Research AI | 产品方向输入            | CEO 审阅提案 | 今天 16:00
中 | 金融研究信号可扩展至港股     | Research Lead| 新增信号品类           | 数据源评估   | 08-05 10:00
中 | 内容增长跨平台分发           | Growth AI   | 阅读量 +20%             | 2 周实验     | 08-15 18:00
```

**公司约束 constraint**：`{name, value, desc, action}`
```
CEO 注意力容量 78%      剩余仅够 1 项高影响决策           → 查看注意力日历
外部平台授权   2 / 5    2 项待续签，影响 3 个工作空间     → 查看授权清单
AI 团队容量瓶颈 研发 AI 80%  Kernel 接近满载，避免并行     → 调配容量
```

---

## 5. business.html — `/ceo-office/projects`

- 标题：`业务`；顶栏 `Curis · 业务版图 · 2026 财年 Q3 · 同步中 · Operating` + 「问 Assistant」
- 计数条：运行中 2 / 实验中 1 / 暂停 0 / 总业务数 3
- Tab（role=tablist）：全部 / 运行中 / 实验中 / 暂停（`data-filter` 过滤 `data-stage`，无结果显示 `#emptyState`「该过滤条件下暂无业务。」）

### 区块
1. 页头 + 计数条 + Tab
2. **业务卡网格** `#portfolioGrid`（3 张，点击卡片打开右侧抽屉 `#businessDrawer` + `#drawerOverlay`）
3. **业务推进过程**（5 步，右侧栏）
4. **投入与结果**（右侧栏）
5. **高影响动作**（右侧栏）

### 业务卡数据模型（核心）
`{id, stage, name, goal（副标题）, stageBadge, valueHealth, executionHealth, targetOutcome 目标结果, externalResults 外部结果[3 指标], nextCheckpoint 下一检查点{name,date}, actions[]}`

```
① software-dev / stage=operating / 徽章「运行中」
   name 软件开发     goal 为 Curis 自身
   价值健康 正常   执行健康 需要留意
   目标结果：每两周交付可验收的软件增量，支撑 CEO 经营闭环
   外部结果：本周 commit 47 · CI 通过率 94% · CEO 验收 2/3
   下一检查点：发布 v0.2 @ 2026-08-03
   操作：[扩大][查看详情][暂停]

② content-growth / stage=operating / 徽章「扩大中」（drawer stage=Scaling）
   name 小红书运营   goal Curis 品牌增长
   价值健康 正常   执行健康 正常
   目标结果：通过高质量内容获取精准受众，建立 CEO 决策品牌心智
   外部结果：周阅读 +2,400 · 收藏率 8.7% · 线索转化 12
   下一检查点：内容矩阵评审 @ 2026-08-05
   操作：[扩大][查看详情][暂停]

③ short-video / stage=experiment / 徽章「Experiment」
   name 抖音 / TikTok 运营  goal 短视频增长实验
   价值健康 需要留意  执行健康 正常
   目标结果：验证短视频能否以更低成本放大内容触达与品牌认知
   外部结果：测试发布 6 条 · 平均播放 3.2K · 互动率 4.1%
   下一检查点：实验结论 @ 2026-08-10
   操作：[查看详情][关闭]
```

### 抽屉 businessData[id]（内联 JS）
`{title, stage, stageClass, commitments[{title, meta}], evidence[{name, value}]}` +
静态区：当前周期（周期 2026-W31 / 2026-07-27 → 2026-08-09 / 进行中）、业务影响（AI 员工 2 人、工作空间 1 个、月成本 ¥1,200、预期收入 ¥12,000）、高影响动作（扩大投入 / 暂停业务 / 关闭业务）、按钮「扩大投入 / 查看 工作空间 / 暂停业务」

```
software-dev  承诺：每两周交付可验收增量（Engineering AI · 验收 CEO）
                    CI 稳定率保持 90% 以上（Engineering AI · 来源 GitHub API）
content-growth 承诺：每周发布 3 篇深度内容（Content AI · 验收 Growth Lead）
                    线索转化率保持 5% 以上（Growth AI · 来源 CMS + 表单）
short-video    承诺：完成 6 条短视频测试发布（Video AI · 验收 Content Lead）
                    验证单条制作成本 < ¥200（Video AI · 来源 平台数据）
```

### 业务推进过程（5 步）
`1 确定方向 → 2 开始执行 → 3 真实反馈 → 4 决定下一步 → 5 下一 bet`

### 投入与结果（本周期）
```
AI 成本      ¥4,280   较上月 +12%
CEO 注意力   28%      目标 < 30%
外部结果总值 ¥18,600  ↑ 23% 较上月
投入产出     4.3x     ↑ 0.8x
下一步建议：继续运营 / 扩大投入
```

---

## 6. ai-organization.html — `/ceo-office/team`

- 标题：`AI 团队办公室`；面包屑 `Curis / 公司 / AI 团队办公室`；右侧「Assistant 在线 · 同步 2 分钟前」+ 按钮「决策室」
- 页头动作：「保存团队快照」「安排团队」；徽标「3 项待修复」
- 特色：多处 `data-spec='{name,size,states,tokens,note}'` 组件标注（设计规格自描述）

### 区块
1. **AI Workforce Map**（卡片 + 节点网格，点击 `data-employee` 打开员工抽屉）
2. **责任矩阵**（表格，6 列）
3. **升级队列**（3 项活跃）
4. **组织异常**（3 类，需 CEO 关注）
5. **能力与容量**（实时运行负载 6 项 + 「调整能力与成本」）
6. **能力资产库**（`#capabilityLibrary` + 「+ 添加能力」→ 能力抽屉）
7. 抽屉 ×2：`#employeeDrawer`、`#capabilityDrawer`

### 组织节点（11 个）
```
ceo                你（公司所有者）              正常
assistant          Curis（CEO 助理）             Operating
business-analysis  Atlas（业务分析 AI）          正常
business-engineering Forge（业务工程 AI）        关注
engineering        Kernel（工程 AI）             关注
growth             Spark（增长营销 AI）          正常
finance            Ledger（财务运营 AI）         正常
content-ws         XHS Mate（小红书运营 工作空间 AI）   正常
dev-ws             DevPilot（软件开发 工作空间 AI）     阻塞
research-ws        短视频 Mate（抖音/TikTok 工作空间 AI）正常
ops-ws             OpsBot（运营支持 工作空间 AI）       正常
```

### 员工抽屉 employees[key]
`{name, role, status, statusClass, contract 责任契约, authorization 授权范围, capabilities[], evidence[], escalation 升级规则, recent 最近动作}`
示例：
```
engineering / Kernel / 工程 AI / 关注
  contract: 软件实现、质量、技术风险
  authorization: 本专业范围内方案选择与风险判断
  capabilities: [代码实现, 代码审查, CI/CD, 技术债务管理]
  evidence: [Curis 自研 v0.3 功能开发 80% 完成, 测试环境授权过期阻塞]
  escalation: 技术阻塞或跨专业资源冲突时升级
  recent: 连续 3 天容量 > 80%，已触发容量告警
```
底部动作：调配 / 暂停 / 查看完整档案

### 责任矩阵表格
列：岗位 | 结果责任 | 协调责任 | 专业判断权 | 升级对象 | 可暂停由谁（●=完全，△=部分，—=无）
```
CEO 公司所有者   ● 最终      ● 最终仲裁    ● 不可委托  —                 —
CEO 助理 Curis   △ 今日经营  ● 跨专业协调  △ 授权内    CEO               CEO
业务分析 AI Atlas ● 本专业结果 △ 向下委派   ● 本专业    Assistant / CEO   Assistant
业务工程 AI Forge ● 本专业结果 △ 向下委派   ● 本专业    Assistant / CEO   Assistant
工程 AI Kernel   ● 本专业结果 △ 向下委派   ● 本专业    Assistant / CEO   Assistant
工作空间 AI      △ 具体交付  ● 流程执行    △ 流程内    Prof AI / 负责人  Prof AI / 负责人
```

### 升级队列（3 项）
```
DevPilot → Kernel → Curis → CEO | 测试环境授权过期，CI 阻塞 | 影响：Curis 自研 v0.3 交付 | [查看][处理]
XHS Mate → Spark → Curis        | 外部平台发布授权失败      | 影响：小红书今日内容发布   | [查看][协调]
短视频 Mate → Atlas             | 数据源质量低于置信阈值    | 影响：抖音/TikTok 数据回流准确性 | [查看][标记已处理]
```

### 组织异常（3 类，动作均为 [查看影响][进入决策室][安排团队]）
```
责任真空 | 抖音 / TikTok 工作空间缺少明确 负责人
判断冲突 | Spark 与 Kernel 对下月优先级建议不一致
容量过载 | Kernel 连续 3 天容量 > 80%，存在疲劳风险
```

### 能力与容量（6 项）
```
AI 团队总容量 72%   5 个专业 AI + 4 个工作空间 AI 平均负载
CEO 注意力    30%   今日 3 项待决策，已处理 2 项
外部平台配额  54%   内容发布 / 数据分析 / 代码仓库 API 综合
内容创作能力  可用   Spark + XHS Mate，本周 12 条内容已发布
软件开发能力  过载   Kernel + DevPilot，测试环境授权阻塞
数据分析能力  可用   Atlas + 短视频 Mate，平台数据等待授权
```

### 能力抽屉表单（写入 localStorage 能力库，同步 runtime 页 `#runtimeCapSelect`）
```
capType     模型(Model) | AI 员工(Agent) | 技能(Skill) | 工具(Tool) | 连接器(MCP)
capName     文本，示例占位「GPT-5、小红书发布器、财报分析 Skill」
capEffect   执行等级（影响面）：只读 | 检索 | 写入 | 执行
capResource 关联资源（可选）：API 地址 / 文件路径 / 外部系统
```

---

## 7. workspace-portal.html — `/ceo-office/workspace`

- 标题：`工作空间`；面包屑 `Curis / 工作空间`；右侧「同步中 · Assistant 在线 · 主题：跟随系统」
- 说明：「业务交付的真实空间。查看运行状态、进入 运行现场 或调整 装修台 搭建方案。」

### 区块
1. **Tab**（role=tablist）：运行中 3 / 装修中 0 / 已归档 0 + 主 CTA「+ 新建工作空间」→ workspace-studio.html
2. **概览卡 4 张**
3. **tabpanel `#panel-running`**：3 张工作空间卡
4. **`#panel-building` / `#panel-archived`**：空状态（图标 + 标题 + 说明 + CTA「打开装修台」）
5. `#toast` 提示条

### 概览卡
```
活跃周期 3      本周 3 个 Cycle 在运行
待 CEO 验收 1   软件开发 v0.2-sprint-3
阻塞 工作空间 1 小红书运营 · 平台授权
最近证据 2      CI pass · 2 分钟前
```

### 工作空间卡数据模型（三业态并列，差异明显）
`{name, business 业务, runStatus 运行状态徽章, currentCycle 当前周期, nextCheckpoint 下一检查点, progressOrBlock 进度/阻塞, externalResult 外部结果, actions[进入运行现场→data-runtime-page, 查看搭建方案→workspace-studio]}`

```
① 软件开发 工作空间   业务：Curis 自研          状态 Attention
   当前周期 v0.2-sprint-3 | 下一检查点 2026-08-03 18:00
   进度条 + 阻塞：测试环境授权待配置
   外部结果：✓ CI pass / CEO 验收待确认
   → workspace-runtime-software.html

② 小红书运营 工作空间 业务：小红书运营          状态 Blocked
   当前周期 week-32 | 下一检查点 等待平台授权后启动
   进度条 + 阻塞：平台授权未配置
   外部结果：− 等待授权与首篇发布
   → workspace-runtime-xhs.html

③ 抖音 / TikTok 运营 工作空间 业务：抖音/TikTok 运营  状态 On Track
   当前周期 创作中 | 下一检查点 2026-08-02 14:00
   AI 岗位：内容策略 · 脚本 · 剪辑 · 数据复盘（替代进度条）
   外部结果：− 待首条内容发布与数据回传
   → workspace-runtime-shortvideo.html
```
注：原「装修台」模态已按 P0-4/P0-5 移除，改为真实页面跳转。

---

## 8. workspace-studio.html — `/ceo-office/workspace/studio`（装修台）

- 面包屑 `Curis / 工作空间 / 工作空间搭建`；右侧「Assistant 在线 · 上次同步 4 分钟前 · 本地桌面 · CEO」
- H1「工作空间 搭建方案」；副标题「草稿 v0.3 · 5 个阶段已组装 · 3 项配置检查未通过」

### 区块（三栏布局）
1. **阶段流程条**：`Discover → 搭建方案 → Compose → Bind → Staff → Simulate → Approve → Operate`
2. **责任界面条**：BE Business Engineering AI（负责人·装修与交付）/ BA Business Analysis AI（分析包）/ PA Professional AI reviewers（专业审阅）/ CEO（Approver）；徽标「3 项待修复」
3. **左侧组件面板**（可拖拽 `.palette-item`，4 组 9 项）
   - 目标与阶段：目标结果、Stage
   - 岗位与员工：Role Slot、AI 员工
   - 能力与工具：Tool、Knowledge
   - 外部与验收：External System、依据、Acceptance
4. **中央画布**（标尺 px 0–1000 / 0–400，缩放 100% / 布局 / 历史；节点可拖拽）
5. **右侧配置检查面板**
6. **底部版本与提交条**

### 画布节点模型（8 节点，短视频/内容域示范）
`{stage 阶段名, owner 负责人, input 输入, output 输出, evidence 证据, failureExit 失败出口}`
```
信号 · Research AI    | 输入 平台热点、竞品选题、CEO 意图 | 输出 候选选题池（含置信度） | 证据 抖音/小红书 API 数据 | 失败：外部授权缺失 → 转人工录入
分析 · Analysis AI    | 输入 选题池 + 历史爆款数据       | 输出 优先级排序与机会标签   | 证据 互动率预测、风险评分 | 失败：数据冲突 → 请求补充来源
决策 · CEO            | 输入 分析包 + 推荐动作           | 输出 批准选题 / 拒绝 / 延后 | 证据 CEO 确认记录         | 失败：CEO 拒绝 → 返回选题池
脚本 · Script AI      | 输入 已批准选题 + 风格指南       | 输出 口播脚本、分镜、标题 3 选 | 证据 脚本版本 + CEO 反馈 | 失败：质量不达标 → 重写并标注原因
制作 · （剪辑）        | …                                | …                          | 证据 成片文件 + 版本差异  | 失败：渲染失败 → 切换备用工具
发布 · Publishing AI  | 输入 选定成片 + 发布计划         | 输出 抖音/小红书已发布链接 | 证据 平台返回发布 ID      | 失败：平台授权过期 → 暂停并通知 CEO
数据 · Data AI        | 输入 发布 ID、平台数据 API       | 输出 播放量、完播率、互动率 | 证据 平台原始数据 + 时间戳| 失败：数据延迟 → 标记为 Stale
复盘 · Review AI      | 输入 数据报告 + CEO 反馈         | 输出 复盘结论 + 下一周期建议| 证据 结论记录、采纳动作   | 失败：结论冲突 → 升级 CEO 裁决
```

### 配置检查（未通过 3 项 · 无法提交审批）
```
缺少 | 外部数据授权未配置       | 抖音/小红书账号授权缺失，信号节点无法获取平台数据
过载 | Research AI 容量告警     | 当前分配 85%，建议降至 70% 或增加实例
风险 | 缺少 CEO 手动反馈入口    | 脚本与成片验收依赖 CEO 主观判断，未配置结构化反馈节点
已通过 | 负责人已分配至每个节点 / Input·Output 已明确 / 失败出口已配置
按钮：[修复问题][运行模拟]
```

### 底部版本条
`草稿版本 v0.3 → 运行版本 v1.0 · 受影响周期：2 个` + [查看影响][运行模拟][**提交审批 → decision-room.html**]

---

## 9. 三个业态运行现场（核心差异区）

三页共用同一 **工作空间 Shell**（5 槽位）：**结果条 → 责任链 → 管道看板 → 右侧栏（外部结果与验收 / 本周期价值与成本 / 洞察与下一步 + CEO 决策队列）→ 详情抽屉**。
共用控件：面包屑、数据可信状态徽章、「去 装修台装修 →」链接、「待 CEO 决策：N」、`#runtimeCapSelect` 当前能力下拉、管道过滤（全部 / 待决策 / 关注）、`#detailDrawer` + `#drawerOverlay` + `#toast`、卡片拖拽换阶段（DnD）。
共用卡片模型：`{id, title, stage, owner, status(ontrack|attention|decision|done), statusLabel, evidence, checkpoint, urgent?, ci[]|stats{}}`
共用抽屉分区：当前状态（阶段 / 负责人 / 状态）→ 证据 → CI 或数据 → 动作（关闭 / 查看证据 / 推进到下一阶段）

### 9.1 workspace-runtime-software.html — `/ceo-office/workspace/software`（研发 software）

- 面包屑：`Curis / 工作空间 / 研发办公室 · Curis v0.2`；可信状态 **等待 CEO 验收**；待 CEO 决策 **1**
- 域声明：北极星 = **回归通过率**（目标 ≥95%），「非完成度%」

**结果条（5 指标，含口径 note）**
```
回归通过率（北极星） 100%   24/24 用例通过     口径：自动回归用例通过数 ÷ 总数（目标 ≥95%）
本周期版本           v0.2.0 待发布           口径：当前迭代版本号
开放缺陷             1      首启性能待观察     口径：未关闭 defect 数（目标 0）
待 review PR         3      阻塞 1 项          口径：等待评审的 PR 数
首次验收通过率       78%    工程实现 AI        口径：一次验收通过工作项 ÷ 总交付工作项
```
**责任链**：产品 AI「v0.2 范围」准备中 → 研发 AI「实现与发布准备」执行中 → QA AI「真实路径验证」验收中 → CEO「真实使用验收」待决策 1 项
**管道 stages**：需求池 backlog → 实现中 implement → 评审 review → 待发布 publish → 已发布 released（只读）
**管道 items（6，字段带 `ci[{t,k}]`）**
```
w1 CEO 真实使用验收路径 backlog  产品 AI 正常   证据 范围已锁定：创建公司→工作台→业务状态→下达指令 | 今日14:00 范围评审
w2 v0.2 核心实现       implement 研发 AI 正常   证据 commit c7a2e91 · 2h 前 | ci: commit c7a2e91(green), CI 绿(green)
w3 首启性能优化        implement 研发 AI 关注   证据 首屏 >2s，需排查主路径加载 | ci: perf 待查(amber)
w4 24 项回归套件       review    QA AI  待决策  证据 24/24 通过 · 等待 CEO 确认 | ci: 24/24 通过(green)
w5 验收包文档          publish   QA AI  正常   证据 验收包已生成，含真实路径脚本
w6 v0.1 已发布         released  研发 AI 已归档 证据 v0.1.0 已上线 · 运行 14 天 | ci: v0.1.0(green)
```
**右侧 · 外部结果与验收**：版本 v2.0.0? → `v0.2.0（commit c7a2e91）`、回归 24/24（QA AI 全部通过）、待 review PR 3（阻塞 1）、开放缺陷 1（首启性能）；验收项「v0.2 验收包 — CEO 真实打开产品，完成创建公司→工作台→业务状态→下达指令」[通过][打回]
**右侧 · 价值与成本**：工程实现 AI ¥1,920（78% 首次通过）· QA AI ¥380（24/24 回归）· 成本合计 ¥2,300（模型+工具）· 复用成果 6 份
**右侧 · 洞察与下一步**：「首启性能是唯一下周期风险」（首屏 >2s，开放缺陷 1 与待 review PR 3 应在发布前清零）
**CEO 决策队列**：v0.2 验收通过 / 退回修改 · 请求现场演示

### 9.2 workspace-runtime-xhs.html — `/ceo-office/workspace/xhs`（小红书 xhs）

- 面包屑：`Curis / 工作空间 / 小红书运营办公室 · 账号增长`；可信状态 **待授权平台 API**；待 CEO 决策 **2**
- 域声明：北极星 = **平均收藏率**（目标 ≥8%），「非阅读量」

**结果条**
```
平均收藏率（北极星） 8.6%    较上周 +1.8%        口径：收藏数 ÷ 阅读数（≥8%，反映内容沉淀价值）
本周发布             5       目标 12 条          口径：成功发布笔记数 ÷ 计划数
新增粉丝             1,248   API 未授权·待确认   口径：净增关注数（授权后自动拉取）
线索价值             ¥12,400 CEO 手动确认        口径：私信/评论转化商机估算（保守口径）
本周期 投入产出      2.1x    成本 ¥720           口径：估算商机价值 ÷ 内容生产成本
```
**责任链**：策略 AI「选题与方向」自动 → 分析 AI「拆解与 Brief」自动 → 内容 AI「产出与封面」执行中 → CEO「品牌边界与发布」待决策 2 项
**管道 stages**：选题池 topic → 草稿 draft → 封面制作 cover → 待发布（CEO 确认）publish → 已发布 published（只读）
**管道 items（8，`ci` 恒为空）**
```
x1 夏季通勤穿搭痛点选题 topic 策略 AI 正常  证据 趋势抓取：通勤+降温 搜索 +38% | 今日15:00 定题
x2 平价精华测评选题     topic 策略 AI 正常  证据 竞品 3 篇均收藏 >5% | 今日16:00
x3 3 个被低估的收纳神器 draft 内容 AI 关注  证据 正文 1.2k 字，需补实测图 | 明日11:00 补全
x4 通勤包防坑指南       draft 内容 AI 正常  证据 Brief 已对齐，正文草稿完成 | 明日14:00
x5 封面 A/B 测试稿      cover 内容 AI 待决策 证据 2 版封面待 CEO 选优 | CEO 选封面
x6 品牌合作披露话术     publish CEO 待CEO确认 证据 需确认是否标注「合作」| CEO 品牌边界确认
x7 敏感词复核           publish CEO 关注    证据「最/第一」类绝对化表述需改 | CEO 表述复核
x8 上周爆款·收纳合集    published 内容 AI 已归档 证据 收藏 1.2w · 投入产出 2.1x
```
**右侧 · 外部结果与验收**：本周发布 5/12、平均收藏率 8.6%、新增粉丝 1,248（API 未授权）、线索价值 ¥12,400（CEO 确认）；验收项「待发布内容包 — 品牌披露话术 + 敏感词复核」[通过][打回]
**右侧 · 价值与成本**：内容 AI ¥480（4 篇产出+封面）· 策略 AI ¥240（选题+拆解）· 成本合计 ¥720 · 复用成果 8 份
**右侧 · 洞察**：「收藏率已超 8% 目标，主攻封面点击→阅读」；推进平台 API 授权以自动拉取粉丝/互动数据
**CEO 决策队列**：待发布品牌/敏感确认 · 授权平台 API 后放量

### 9.3 workspace-runtime-shortvideo.html — `/ceo-office/workspace/shortvideo`（短视频 shortvideo）

- 面包屑：`Curis / 工作空间 / 抖音 / TikTok 运营`；可信状态 **同步中**；待 CEO 决策 **1**
- 域声明：北极星 = **完播率**（决定系统是否继续分发），「非播放量」

**结果条**
```
完播率（北极星） 38.2%  ↑ 2.1pp 周环比        口径：播完用户 ÷ 播放用户
总播放量         1.24M  ↑ 23% 较上周          口径：周期内全部视频累计播放
互动率           6.8%   ↑ 0.6pp               口径：（赞+评+转）÷ 播放
新增粉丝         4,721  ↑ 18%                 口径：周期内净增关注
投入产出         4.4x   内容产出价值 ÷ 投入   口径：可归因价值 ¥33,800 ÷（模型+投流）¥3,800
```
**责任链**：Growth AI「策略与选题方向」执行中 → Content AI「脚本与事实校验」执行中 → Video AI「拍摄与剪辑」执行中 → CEO「验收与决策」待决策 1 项
**管道 stages**：选题 topic → 制作 produce（脚本+拍摄+剪辑合并）→ 发布 publish → 数据 data → 复盘 review（只读）
**管道 videos（10，独有字段 `duration` 与 `stats{plays, completion, interaction, follows}`、`urgent`）**
```
v1 AI 员工不是聊天机器人：Curis 的组织观 topic  Growth AI 正常 0:45 热度信号：同类话题近 7 天播放均值 +34% | 今日14:00 前提交 3 个备选角度
v2 一人公司如何选第一条业务：5 个决策问题 produce Content AI 正常 1:20 脚本 v2 已通过事实校验，引用 3 条 CEO 过往决策 | 今日17:00 终稿
v3 为什么 CEO 必须先有状态再有动作      produce Content AI 关注 0:58 开篇 3 秒 hook 测试得分低于均值 | 明日10:00（urgent）
v4 从 Task 到 工作空间：Curis 的产品转向 produce Video AI 正常 1:05 分镜 6 个，已预约 CEO 今日15:00 录制 | 今日18:00 拍摄
v5 工作空间运行现场：业务如何被交付      produce Video AI 待决策 1:12 两版剪辑：A 版节奏快（完播预测 +8%），B 版信息密 | CEO 选 A/B（urgent）
v6 CEO 办公桌：每天第一眼该看什么        publish Video AI 正常 0:52 封面 3 张已生成，标题 A/B 就绪 | 今日20:00 定时发布
v7 AI 公司不是自动化：CEO 必须保留的三项决策 data Growth AI 正常 1:08 发布 24h，播放 89K，完播 35% | 48h 后复盘
   stats: plays 89K · completion 35% · interaction 5.9% · follows 312
v8 Curis 的冷静 CEO 工作空间设计理念     data Growth AI 关注 0:48 前 3 秒跳出率偏高 | 明日12:00 诊断报告（urgent）
   stats: plays 56K · completion 28% · interaction 4.1% · follows 178
v9 AI 员工不是聊天机器人                 review CEO 待验收 1:15 发布 72h，播放 142K，完播 41%，互动 8.2% | CEO 验收截止今日18:00（urgent）
   stats: plays 142K · completion 41% · interaction 8.2% · follows 847
v10 从 0 到 1 设计公司 OS：Curis 方法论  review CEO 已归档 1:30 复盘完成：复用「状态先于动作」框架
   stats: plays 203K · completion 44% · interaction 9.1% · follows 1.2K
```
**右侧 · 外部结果与验收**：总播放 1.24M、完播率 38.2%、互动率 6.8%、新增粉丝 4,721；**两条验收项（视频卡）**
```
《AI 员工不是聊天机器人》     播放 142K · 完播 41% · 互动 8.2% [通过][打回]
《一人公司如何选第一条业务》  播放 89K · 完播 35% · 互动 5.9%  [通过][打回]
```
**右侧 · 价值与成本**：可归因价值 ¥33,800（成交与线索）· AI 与投流成本 ¥3,800（模型 ¥1,200 · 投流 ¥2,600）· 每条平均成本 ¥317（12 条运行中）· 投入产出 4.4x（↑0.8x）；投流无回传凭证时保留为待验证成本
**右侧 · 洞察（2 条，独有「趋势分析」）**
```
趋势分析：「AI 组织关系」主题连续 3 周高于均值 → 建议追加 2 条同主题选题
下一周期：测试「口播 + 实拍」混合形式（实拍完播高 12%，制作时长 +40%，需评估产能）
```
**CEO 决策队列**：是否批准日更频率提升至 2 条

### 9.4 workspace-runtime-department.html — `/ceo-office/workspace/template`（未装修通用模板）

- 面包屑：`Curis / 工作空间 / 通用模板 · 未装修`；徽章 **模板预览 · 无真实数据**；**无「待 CEO 决策」计数**
- 核心规则：装修完成前不出现任何指标数值（系统不替业务编造口径）

**结果条（占位）**：北极星指标 —（装修时必填：指标名 + 当前值 + 口径说明，需写清分子分母与排除项）；辅助指标 ①产能类 ②质量类 ③成本类 ④价值类，均为「—」
**责任链（占位）**：角色①意图澄清与拆解 / 角色②生产执行 / 角色③结果回收与异常上报 / **CEO 必选**（验收·调整·暂停不可省略）
**CEO 不可静默执行的 6 件事**：对外发布、花钱、对外承诺、动权限、不可逆操作、扩大范围
**通用 9 槽位管道骨架**：`Intake 意图 → Produce 生产 1~N 段 → Deliver 交付 → Collect 结果回收 → Accept CEO 验收 → Review 复盘 → Improve 提升 → Archive 归档`
**右侧 · 外部结果与验收**：在办 / 待验收 / 已结项 / 返工 均为「—」；无授权时结果必须 CEO 补录并标「待验证」
**右侧 · 价值与成本**：本周期成本 / 产出价值 / 投入产出 / 证据等级 均「—」；只有「已验证」等级结果才能支持扩大业务，异常会冻结扩大权限
**右侧 · 装修这个空间**：5 步装修指引 → 「去 装修台装修 →」workspace-studio.html

### 9.5 workspace-shell-reference.html — `/ceo-office/workspace/_shell-reference`

- 面包屑：`Curis / 工作空间 / 示例工作空间`；待 CEO 决策 **2**
- 定位：Shell 参考原型（模板）。新业务接入 = 复制本文件填充 5 槽位（结果条 / 责任链 / 管道看板 / 侧栏面板 / CEO 决策队列）
- 结果条以小红书域作完整示范：平均收藏率 8.6%（口径：收藏数 ÷ **曝光数**）、本周发布 5/12、新增粉丝 1,248、线索价值 ¥12,400、投入产出 2.1x（口径：产出价值 ÷（模型+**人工**）投入）
- 责任链/管道为通用占位：角色 A/B/C + CEO；lanes：选题 idea 1 / 生产 produce 1 / 审核 review 1 / 发布 publish 0 / 回顾区 archive（只读）1
- 侧栏：线索价值 ¥12,400 · 投入产出 2.1x · 投入（模型+人工）¥5,900
- CEO 决策队列：待发布笔记品牌/敏感表达确认 · 授权后是否放量投放

---

## 10. decision-room.html — `/ceo-office/decisions`

- 标题：`待决策事项 · 决策室`；面包屑 `Curis / … / 决策室`；顶栏徽标 `#pendingBadge`「待 CEO 决策：N」（由数据长度动态生成）+ `#backBtn` 返回（history.back，否则回 ceo-desk.html）
- 页头：H1「待决策事项」+ 徽标「演示数据」
- 区块：`#inbox` 决策卡列表（可展开 accordion）+ `#emptyState`（⚖「当前没有待决策事项」）

### 决策卡数据模型 DECISIONS[]（内联 JS，全字段）
```
id, status(pending|decided|deferred|revised|rejected), statusText, title,
source 来源, submittedAt, dueAt, summary, context,
facts[{t 事实, s 来源}], unknowns[{t 未知, s 风险/建议}],
options[{key: approve|defer|revise|reject, tag 推荐, t 方案标题, d 说明}],
impact[{l 维度, v 值, d 说明, cls up|warn|''}],
notes[{cls: cycle|capacity|risk, t}],
sims{normal|absent|delay|reject: {title, outcome, metrics[[名,值],…]}},
outcomes{approve|defer|revise|reject: {title, body, action, next}}
```

### 卡片内 6 个编号分区（展开后）
`01 事实与证据 → 02 已知未知 → 03 可选方案（单选） → 04 影响分析 → 05 模拟结果（Tab：正常路径 / 执行角色缺席 / 外部延迟 / CEO 拒绝）→ 06 CEO 决策`
决策后写入 **依据 / 事实层记录**：决策动作、执行路径、记录时间、来源页面（决策室 / decision-room.html）、写入层（状态：不可篡改），生成证据 ID `decision://YYYY-MM-DD/<choice>-<timestamp>`，锁定按钮并将徽标改为 已决策/已延后/已退回/已拒绝，附「返回今日简报」。

### 示例数据（2 条）
**d1 · 待决策**「批准抖音 / TikTok 运营工作空间搭建方案 v0.3 → 运行版本 v1.1」
来源：工作空间工作台 · 业务工程 AI｜提交 2026-08-01 14:32｜截止 2026-08-02 10:00
- facts（5）：搭建方案 v0.3 已覆盖 v1.1 全部环节（commit #a4f9c2）/ 6 类运行模拟全部通过（正常·执行角色缺席·外部延迟·CEO 拒绝·工具失败·证据冲突）/ 内容 AI 与增长 AI 责任矩阵已对齐 / 外部平台授权均在有效期（抖音·小红书·视频号）/ 财务估算：月成本 +¥1,200，预期外部结果 +¥18,000（置信度 中）
- unknowns（3）：视频号新接口限流未实测 / 剪辑角色 4K 素材处理时长无真实数据 / 品牌安全审核阈值未确认
- options：A 批准并发布 v1.1（推荐，旧 v1.0 保留 14 天可回滚，首周检查点 8/5）/ B 延后 3 天 / C 要求修改 / D 拒绝并保留 v1.0
- impact：经营周期 Q3 内容增长（warn）/ AI 容量变化 +1 交接节点（内容 AI +20%）/ 财务影响 投入产出约 15:1（up）
- notes：cycle / capacity / risk（48h 内未接入真实账号数据 → 风险等级 正常→关注）

**d2 · 待决策**「小红书放量投放授权：是否在确认品牌安全阈值后开启」
来源：小红书运营办公室 · 增长 AI｜提交 2026-08-03 09:10｜截止 2026-08-03 18:00
- facts：近 7 日平均收藏率 8.6%（北极星）/ 线索价值 ¥12,400，周环比 +14% / 品牌安全审核清单草稿 v0.2 待确认阈值
- unknowns：放量后单日调用上限是否触发平台限流
- options：A 确认阈值并开启放量（推荐）/ B 延后至阈值确认 / C 暂不开启放量
- impact：线索价值 预期 +¥6K/月（up）/ 品牌风险 中（warn）/ 状态变化 关注 → 正常
- sims：normal +¥6K 状态正常 / delay 阻塞 1–2 天 状态关注 / absent 18h 内升级 / reject 成本 ¥0 维持现状

---

## 11. meeting.html — `/ceo-office/meeting`

- 标题：`会议工作台 · 外部合作方周会`；面包屑 `Curis / 经营 / 会议工作台`；右侧「CEO · 本地桌面 · 助理在线」
- 页头：`11:00 · Operating Day` / H1「外部合作方周会」/ 说明「把必须讨论的事情留在一场有边界的对话里。AI 员工负责准备背景、标记事实与未知，CEO 负责确认最后的承诺和决议。」/ 状态胶囊「进行中 · 3 位参与者」
- **静态 HTML 仅有页头骨架**，正文区域由 `curis-prototype.js` 动态渲染，无内联示例数据。

---

## 12. assets.html — `/ceo-office/assets`（成果库）

- 标题：`成果库`；顶栏 `Curis / 公司资产 · 成果有来源 · 可验证 · 可复用`
- 页眉：`公司知识与产出 / 成果库 / 每一份交付、外部结果和复盘都留下版本与证据…`

### 区块
1. **概览 4 卡**：已验证成果 18（过去 30 天）· 可复用工作流 6（跨工作空间）· 已连接来源 4（API / Connector）· 待补证据 2（需要 CEO 处理）
   （运行时由 JS 动态改写为：已记录成果 / 已保存工作流 / 来源已登记 / 需要 CEO 处理）
2. **所有成果**：筛选按钮 `data-asset-filter`：全部 / 软件开发 / 小红书 / 抖音 / TikTok / 公司知识（+ JS 追加「业务结果」）；列表容器 `[data-asset-list]`
3. 底部说明：AI 员工在每阶段提交带来源的产出；CEO 验收或外部数据确认后才变「已验证」

### 成果条目模型（由 `curis-prototype.js` 渲染）
```
{ type 类型, title 标题, owner 负责人, version 版本, evidence 证据,
  reuse 复用位置, source 来源, reviewed 是否已审阅, outcomeId, reviewAction }
示例：type='可复用流程', owner='CEO 助理', evidence='已保存能力组合 · 可带上下文复用', reuse='工作空间搭建'
```
行操作：`复用 / 去审阅`（data-asset-action="reuse"）、`查看`（detail → 弹窗展示来源、版本关系、贡献分配「待 CEO 确认」）
空态文案：「成果库还没有内容 — Agent 完成交付、CEO 验收或外部结果回传后，成果会带着来源和版本出现在这里。」

---

## 13. knowledge.html — `/ceo-office/knowledge`（知识库）

- 标题：`知识库`；顶栏 `Curis / 公司知识库 · 知识会进入每个工作空间，但不会绕过来源和权限`
- 页头动作：`导入资料`（data-knowledge-action="import"）/ `连接外部知识库`（="connect"）

### 区块
1. **概览 4 卡**：可引用资料 `[data-knowledge-count]` 126（文档、链接、图片、视频）· 最近更新 14（过去 7 天）· 已连接来源 `[data-knowledge-source-count]` 3（本地文件库 · Notion · 网页收藏）· 待确认来源 `[data-knowledge-pending]` 2（权限或引用范围未确认）
2. **公司资料**：搜索框 `[data-knowledge-search]` +「搜索」；筛选 `data-knowledge-filter`：全部 / 竞品 / 平台规则 / 内容素材 / 研发；列表 `[data-knowledge-list]`（JS 渲染，seed 为空，取自 state.knowledgeItems）
3. **外部来源**（4 条）
```
本地文件库    文档、图片、视频 · CEO 私有        已连接
Notion 工作区 竞品研究、内容规则 · 只读           已连接
网页收藏      浏览器收藏夹 · 最近同步 2 小时前    已连接
视频素材盘    等待 CEO 确认读取范围               待确认
```
4. JS 注入「当前工作流引用」上下文条 + `[data-knowledge-return]`「返回当前工作流」（依据 state.knowledgeReturnRoute）
5. 底部：资料更新后旧产出不被静默改写，下次运行标记版本变化并请求复核

---

## 14. finance.html — `/ceo-office/finance`（财务与经营）

- 标题：`财务与经营`；顶栏 `Curis / 财务与经营 · 口径：本周期 · 数据来源已标注`
- 页头动作：`补录收入`（data-finance-action="record"）/ `生成 CEO 财务简报`（="brief"）

### 区块
1. **概览 5 卡**
```
可确认收入   ¥28,600  本周期 · API + 手动
AI 运行成本  ¥3,840   模型调用与连接器
外部结果价值 ¥46,200  成交额与节省成本
经营毛利     86.6%    按可确认收入
待确认事项   3        需要 CEO 判断
```
2. **业务经营账表格**（列：业务 | 收入 | AI 成本 | 结果价值 | 投入产出）
```
Curis 自研     —        ¥1,920  节省研发 120h  3.4x
小红书运营     ¥8,600   ¥720    ¥12,400        2.1x
抖音 / TikTok  ¥20,000  ¥1,200  ¥33,800        4.4x
合计           ¥28,600  ¥3,840  ¥46,200        3.8x
```
口径提醒（`#finance-manual-note`）：外部平台未授权时收入与结果必须 CEO 补录，标「待验证」，不伪装成 API 事实
3. **AI 员工产出与成本**（关键指标 = 工作指标，非活跃度）
```
业务分析 AI · 已验证成果   12 / ¥42
内容制作 AI · 通过率       83% · ¥18/条
工程实现 AI · 首次通过     78% · 24/24
CEO 助理 · 经营提醒命中    91% · 3 次升级
容量风险                   内容制作 AI 78%
```
4. **下一步建议** + 按钮「查看成果库」（data-finance-action="assets" → assets.html）

---

## 15. calendar.html — `/ceo-office/calendar`（公司日历）

- 标题：`公司日历`；顶栏 `Curis / 公司日历 · 公司成立第 24 天 · 2026 年 8 月`
- 页头动作：`保存经营节奏`（data-runtime-action="save-workflow" data-workflow-name="CEO 每周经营复盘"）/ `连接日历 / 平台`（="authorize"）

### 区块
1. **月历网格**（一~日，2026 年 8 月；灰色=自动运行，实心=CEO 决策或业务里程碑）
```
08-01 研发回归 | 08-02 周报自动生成 | 08-03 小红书选题 | 08-04 CEO 经营日 |
08-05 视频数据回流 | 08-06 Curis v0.2 验收 | 08-07 复盘 | 08-09 内容发布 |
08-11 收入同步 | 08-13 周度经营简报 | 08-16 新一轮选题 | 08-18 AI 容量检查 |
08-20 业务扩展评估 | 08-23 财务结算 | 08-25 月度复盘 | 08-28 下月业务方向
```
2. **自动运行中的节奏**（4 条：名称 / 触发时间 · 负责人 · 输出或失败出口 / 操作）
```
小红书 · 每日研究        每天 08:00 · 策略分析 AI · 输出 3 条候选选题      [编辑]
抖音 / TikTok · 数据回流 每天 18:00 · 数据回收 AI · API 失败则提醒手动补录 [连接]
公司 · 每周经营简报      每周一 09:00 · CEO 助理 · 汇总财务、成果和风险    [已启用]
研发 · 回归检查          每次提交后 · QA AI · 失败时暂停发布并升级         [已启用]
```
3. **公司成长时间线**（`{time, title, desc, status}`）
```
07-09 第一天       Curis 公司成立                     已归档
07-12 首个业务     Curis 自研办公室启动               运行中
07-18 第一次外部结果 小红书首轮内容获得真实互动        已验证
08-04 今天         三条业务进入同一经营周期           进行中
```
4. 运行原则：每个任务有负责人、输入、输出、失败出口和升级条件；无连接器授权时保留手动录入窗口，不用假数据

---

## 16. ceo-day-demo.html — `/dev/ceo-day-demo`（真实后端联调）

- 标题：`Curis · CEO 的一天（真实 API 接入演示）`+ 徽标「示例数据」；无侧栏/面包屑
- 控件：`#base` 输入（默认 `http://localhost:8000`）、按钮「跑通正常 7 步闭环」`#run`、「跑通失败路径（无授权→扩大冻结）」`#fail`、`<pre id="log">` 日志区
- 依赖 `curis-api.js`；后端统一响应契约 `{code, message, data, trace_id, timestamp}`，`code===0` 为成功，**不做静默 mock**

### 正常路径 7 步（对应领域模型状态机）
```
① 创建业务方向 → ACTIVE
   createDirection({name:"小红书增长", template_type:"xhs", opportunity, target_outcome})
   → submitBrief → approveDirection(authorized=true)
② 承诺 → ACTIVE
   createCommitment({business_id, department_name:"增长组", name:"每周研究", target_outcome}) → firstResult
③ 工作空间 → OPERATING（三级门禁）
   createWorkspace → startBlueprint → passSimulation
   → submitApproval(issues_resolved, external_agent_reviewed) → approveLaunch
④ 节奏 → 到点自动开跑 → WAITING_CEO
   createCadence({name:"每日研究", schedule_text:"daily 08:00", escalation:{reason}}) → enableCadence → fire()
⑤ CEO 处理 → ACKNOWLEDGED → RESOLVED（openRun → resolveRun(reason)）
⑥ 外部数据回流 → 成果 VERIFIED + 贡献权重
   createOutcome({business_id, run_id, commitment_id, value:1200.0, evidence_grade:"VERIFIED",
                  source:"api", contributors:[{agent:"researcher",model:"gpt",weight:60},
                                              {agent:"writer",model:"claude",weight:40}]})
   → confirmAttribution
⑦ 记账归因 → setVerification("VERIFIED") → scaleDirection → SCALING（闭环完成）
```
### 失败路径
无外部授权 → `evidence_grade="UNVERIFIED"` → `setVerification("UNVERIFIED")` → `scaleDirection` **被拒（扩大冻结）**

### 后端资源与端点（`curis-api.js`）
```
BusinessDirection /api/ceo-day/business-directions [POST]
                  /{id}/submit-brief | /approve | /scale | /verification
Commitment        /api/ceo-day/commitments [POST] | /{id}/first-result | /fulfill
Workspace         /api/ceo-day/workspaces [POST] | /{id}/start-blueprint | /pass-simulation
                  | /submit-approval | /approve-launch
Cadence / Run     /api/ceo-day/cadences [POST] | /{id}/enable | /api/ceo-day/fire
                  /api/ceo-day/runs/{id}/open | /resolve
Outcome           /api/ceo-day/outcomes [POST] | /{id}/confirm-attribution
```

---

## 17. 三业态（software / xhs / shortvideo）差异总表

| 维度 | 研发 software | 小红书 xhs | 短视频 shortvideo |
|---|---|---|---|
| 运行现场页 | workspace-runtime-software.html | workspace-runtime-xhs.html | workspace-runtime-shortvideo.html |
| 侧栏名称 | 软件工作室 ⌨ | 小红书 ✎ | 短视频 ▶ |
| 业务页名称 / 阶段 | 软件开发（运行中 operating） | 小红书运营（运行中→扩大中 Scaling） | 抖音 / TikTok 运营（实验中 Experiment） |
| 业务页外部结果 | 本周 commit 47 / CI 通过率 94% / CEO 验收 2-3 | 周阅读 +2,400 / 收藏率 8.7% / 线索转化 12 | 测试发布 6 条 / 平均播放 3.2K / 互动率 4.1% |
| **北极星指标** | **回归通过率 100%（目标 ≥95%）** | **平均收藏率 8.6%（目标 ≥8%）** | **完播率 38.2%** |
| 明确否定的伪指标 | 「功能做了多少 / 完成度%」 | 「阅读量」 | 「播放量」 |
| 其余结果条指标 | 本周期版本 v0.2.0 / 开放缺陷 1 / 待 review PR 3 / 首次验收通过率 78% | 本周发布 5（目标 12）/ 新增粉丝 1,248 / 线索价值 ¥12,400 / 投入产出 2.1x | 总播放 1.24M / 互动率 6.8% / 新增粉丝 4,721 / 投入产出 4.4x |
| 数据可信状态 | 等待 CEO 验收 | **待授权平台 API**（粉丝数标「API 未授权·待确认」，线索价值「CEO 手动确认」） | 同步中（数据已回流） |
| 待 CEO 决策数 | 1 | 2 | 1 |
| 责任链 | 产品 AI → 研发 AI → QA AI → CEO（真实使用验收） | 策略 AI（自动）→ 分析 AI（自动）→ 内容 AI → CEO（品牌边界与发布） | Growth AI → Content AI → Video AI → CEO（验收与决策） |
| 管道阶段 | 需求池 / 实现中 / 评审 / 待发布 / 已发布(只读) | 选题池 / 草稿 / 封面制作 / 待发布(CEO 确认) / 已发布(只读) | 选题 / 制作(脚本+拍摄+剪辑合并) / 发布 / 数据 / 复盘(只读) |
| 卡片独有字段 | `ci[{t,k: green/amber}]` CI 与提交标签 | 无 ci（全空数组），证据偏内容与合规 | `duration` 时长 + `stats{plays, completion, interaction, follows}` + `urgent` |
| 工作项数量 | 6 | 8 | 10 |
| 成本构成 | 工程实现 AI ¥1,920 + QA AI ¥380 = ¥2,300（模型 + 工具/CI） | 内容 AI ¥480 + 策略 AI ¥240 = ¥720（模型 + 图片生成工具） | ¥3,800 = 模型 ¥1,200 + **投流 ¥2,600**；每条均价 ¥317 |
| 价值口径 | 无金额，用「复用成果 6 份 + 节省研发 120h」（财务页 投入产出 3.4x） | 线索价值 ¥12,400（私信/评论转化估算，保守口径）；投入产出 2.1x | 可归因价值 ¥33,800（成交与线索）；投入产出 4.4x |
| 验收对象 | 1 个「v0.2 验收包」（真实路径走通） | 1 个「待发布内容包」（品牌披露 + 敏感词） | 2 条视频（带播放/完播/互动三指标） |
| CEO 决策队列 | v0.2 验收通过 / 退回修改·请求现场演示 | 待发布品牌·敏感确认 / 授权平台 API 后放量 | 是否批准日更频率提升至 2 条 |
| 洞察结构 | 单条「下一周期改进」 | 单条「下一周期改进」 | **两条：趋势分析 + 下一周期**（独有趋势维度） |
| 门户卡辅助信息 | 进度条 + 阻塞「测试环境授权待配置」 | 进度条 + 阻塞「平台授权未配置」 | **AI 岗位列表**（内容策略·脚本·剪辑·数据复盘），无进度条 |
| 门户卡运行状态 | Attention | Blocked | On Track |
| AI 团队对应 工作空间 AI | DevPilot（阻塞） | XHS Mate（正常） | 短视频 Mate（正常） |
| 创建流程模板 key | `software` | `xhs` | `douyin` |
| 财务页经营账 | 收入 —，AI 成本 ¥1,920，结果价值「节省研发 120h」，投入产出 3.4x | 收入 ¥8,600，成本 ¥720，结果价值 ¥12,400，投入产出 2.1x | 收入 ¥20,000，成本 ¥1,200，结果价值 ¥33,800，投入产出 4.4x |

### 共性约束（三业态一致）
1. 每个域的北极星指标 **必须整体替换，禁止套通用模板**；每项指标必须显示口径 note。
2. 未获平台授权时结果由 CEO 补录并标「待验证」，不用估算值填满结果窗口。
3. 只有「已验证」等级结果才能支持扩大业务；结果异常冻结扩大权限（与 ceo-day-demo 失败路径一致）。
4. 责任链末端必须保留 CEO 节点；六件事（对外发布、花钱、对外承诺、动权限、不可逆操作、扩大范围）AI 不得静默执行。
