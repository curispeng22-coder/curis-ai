# CURIS FULL PRODUCT HTML DESIGN PROTOTYPE — REVIEW

> Authority Class: RESEARCH / EVIDENCE（设计原型验收记录；不构成 Product Authority）
> Status: **CURIS FULL PRODUCT HTML DESIGN PROTOTYPE — READY FOR CEO / CHATGPT REVIEW**
> Date: 2026-09-12
> 位置：`docs/prototypes/full-product-html/`（入口 `index.html`；截图 `screenshots/`）
> 消费：Frozen Product Structure Baseline、`CURIS_DESKTOP_PRODUCT_AND_DESIGN_DIRECTION.md`、`CURIS_PIXEL_LEVEL_COMPETITIVE_REFERENCE_MATRIX.md`、`CURIS_PAGE_REFERENCE_BLUEPRINT.md`（P1–P14）、Visual Standard、UI Audit / Problem Register、`PROFESSIONAL_BUSINESS_EXISTING_TRUTH.md`（本原型前置研究，含 Content Growth / RD 既有权威汇总）。
> 边界遵守：未修改 Product Authority / Runtime / 生产 Frontend / Figma；未 commit / push。

---

## 1. 覆盖页面（对照指令 §2）

| 要求项 | 状态 | 证据截图（screenshots/） |
|---|---|---|
| 七区：CEO 工作台 | ✅ 去后台化（简报行→待决定→正在运行→最新结果→公司脉搏次级） | 01, dark-01 |
| 业务空间（列表+详情+激活） | ✅ | 02, 22 |
| 组织中心 | ✅ 公司版图/员工目录 | 07 |
| 人才与能力 | ✅ 三 tab+精选+分类+排序+搜索+安装态 | 09, 10, 11 |
| 经营洞察 | ✅ | 12 |
| 资料库 | ✅ | 13 |
| 会议 | ✅ | 14 |
| Employee Detail / 工作站 | ✅ 六 Tab（工作/责任/能力/对话/结果/设置） | 08, dark-08 |
| Workspace Working Surface | ✅ 三个不同构专业/通用面 | 03, 04, 05, 06, 23 |
| Settings | ✅ 14 节全做（非空壳） | 15, 16 |
| Global Search ⌘K | ✅ 类型 chips+分组结果+预览 | 17 |
| Notifications | ✅ 四类 | （面板实现，键入即现） |
| Floating CEO Assistant | ✅ 四态+可拖动+跨区存在 | 18, dark 系列 |
| Conversation + Shared Composer | ✅ 组件级（见 §3） | 08（对话 Tab 内嵌） |
| Agent Work / Progress | ✅ Plan/Steps/当前动作/工具折叠/协作/交接/elapsed/cost | 19 |
| Result / Artifact / Utility | ✅ 证据链+被引用+Utility Preview | 20 |

## 2. 三条验收链（指令 §25.10）

- **FLOW A — Content Growth**：`#/business/biz-cg` → `#/workspace/ws-xhs`（六 Surface Domain Navigation + 团队运转 pills + 工作区）→ 林月工作卡（选题研究，交接至 内容运营）→ `#/work/w-tuwen`（定位调整 Decision 升级 CEO）→ `#/decision/d-xhs`。措辞消费 Domain Authority（Opportunity→Intent→Target Account Set→Content Variant→Publication；EST 标注；回执来自 Connector）。
- **FLOW B — RD**：`#/business/biz-rd` → `#/workspace/ws-rd`（产品→架构→Runtime→Adapter→Test→Review 状态链 + 灰度 Decision Banner + Context 代码树）→ `#/work/w-login`（周岚联调，工具活动折叠，交接赵敏）→ `#/workspace/ws-rd?util=1`（Diff/Source/Preview Utility）→ `#/decision/d-release`。措辞消费 08-rd-workspace anatomy 与 Instance Spec（waiting ≠ idle 等）。
- **FLOW C — New Business**：`#/activate`（CEO intent → 理解 → 研究 → 建议 → CEO Gate）→ `#/business/biz-pet`（激活链六步：意图→空间工程部承接→研究→设计→激活建议→开始经营）→ `#/workspace/ws-pet`（Generic Workspace）。
- **十条验收问题（25.11）均可从 UI 自然回答**：经营哪些业务（02）；属于什么部门（面包屑+详情头）；谁负责（详情头+Workspace Shell）；团队在做什么（工作区 emp-row 状态）；为什么由 TA 做（Work 页 Context"为什么由 TA 做"+责任解析）；运行到哪里（经营五要素/交付状态链）；Result/Evidence（20 证据链）；需要 CEO 判断什么（01 简报"需要决定"+Decision Banner）；两个业务明显不同（03 vs 05：六 Surface+内容日历 vs 状态链+代码树+灰度门禁）；同一 Company OS（同壳/同员工系统/同 Composer/同状态词典）。

## 3. 交互实现清单（指令 §4）

七区导航+业务子树 ✅｜Sidebar selected/hover ✅｜Context 收起/展开（⌘\语义、按钮）✅｜Utility 打开/关闭（?util=1 或按钮）✅｜员工行→详情 ✅｜Work→Progress ✅｜Result→Utility ✅｜对话切换（工作区行展开/员工 Tab/独立路由）✅｜Composer 输入/附件/@引用 ✅｜Model/执行者菜单 ✅｜权限 chip 循环（最小→白名单→完全访问变警示色）✅｜工作模式 chip ✅｜Send→Working→Stop→回执 ✅｜Talent 三 tab+安装切换 ✅｜Skill 详情/绑定 ✅｜Settings 分类导航 ✅｜⌘K 开关+结果跳转 ✅｜通知面板跳转 ✅｜助理展开/收起/working/result-ready/拖动 ✅｜State Switcher（虚线标注 DESIGN TOOL）✅。

## 4. 使用的 Reference（按 Blueprint，统一过 Curis token）

Navigation/侧栏密度 → Linear（E9）｜搜索浮层 → Linear（L4）｜Composer 容器/占位/发送 → Claude（L4）｜权限 chip → WorkBuddy"允许完全访问"（L3）｜文件引用卡 → WorkBuddy（L4）｜消息操作行+成本内联 → WorkBuddy（L4）｜Agent 进度右栏/子任务头像 → ChatGPT Codex（L2/L3）｜工具折叠 → Cursor（L3）｜Result Preview → Cursor（Preview⇄Source）｜Utility 编辑深度 → 扣子（L2）｜Settings 壳 → Cursor（L3）｜Usage 拆分 → 扣子（L3）｜人才市场结构 → Workbuddy 专家中心（L2，卡片 anatomy L4）。全部组件使用 Frozen `--ui-*` token；无竞品色值/图标混入。

## 5. VISUAL AUTHORITY REVIEW REQUIRED（未私自解决）

1. **Accent 冲突**：本原型 accent 采用 Frozen `CURIS_VISUAL_STANDARD_V1`（Direction D / `#806BE5`，浅色深实心主按钮、深色 `#9B88EC`）。被复制的 D 代 `_system/tokens.css` 携带旧 UI Frozen Spec 的 `#32f08c` 绿（Pointer #4 已注明被 V1 取代）。**CEO 需最终确认 accent**：若维持 V1 紫，本原型即为迁移示范；若重启视觉方向，仅需改 `css/curis.css` 顶部三个变量。
2. 研究简报 §8 曾把"紫色使用失控"列为审计问题——本原型以"accent 只做焦点/激活/链接/小指示线"的纪律使用紫色（D 代纪律），未大面积铺色；是否合意请 CEO 在 Review 中裁定。
3. Dark 默认值：D 代 theme.js 默认 Dark（Frozen stance）；本原型默认 Light（指令"Light 为主"），Dark 为一等支持。默认值归属 Final UI Master 决定。

## 6. 已知问题 / 未覆盖项（如实登记）

1. `emp-row` 展开内嵌对话在长对话时高度较大，收起态记忆未做（原型级取舍）。
2. Composer 的 running 状态为 2.2s 模拟，无真实流式；回执文案为演示。
3. 通知面板未做"全部已读/分组过滤"二级交互。
4. Search 预览为 Property 行占位文案（Linear 式结构的示意），未渲染真实对象预览。
5. 经营洞察图表用 KPI+行替代真实 chart（Figma 172 基线应在 Final UI Master 消费，未在原型重画图表）。
6. 会议房间内嵌讨论（Figma 214 基线）未在原型重画——按 Blueprint P10 消费已验收基线，原型只做列表/详情骨架。
7. Skill 安装后的"绑定到哪个员工"引导为单步原型（无向导流）。
8. RD Diff 语法高亮使用临时色（`--ui-syntax-*` 未冻结，DESIGN GAP #2，沿 D 代登记）。
9. 移动端/自适应只验证到 1024（指令不要求 Mobile）。
10. State Switcher 覆盖 CEO/Workspace/Result 三类页面的关键态；其余页面仅有 normal 态。

## 7. 自检结论（指令 §20）

产品语义（七区/Company OS/责任链/会议/Result→Evidence）✅ 与 Frozen 结构一致，无第二套 IA；Four-Pane 按"Navigation+Main 默认、Context/Utility 按任务出现"实现（03 无 Utility、06 全四 Pane、08 无 Context）✅；信息层级（行优于卡、卡仅聚合）✅；主/次动作分明 ✅；Empty（CEO first-run、Workspace first、反馈/商业化 Optional 空态）✅；Loading（Result loading 态）✅；Error（简报错误横幅、对话错误+重试）✅；状态词典统一 ✅；密度/对齐/滚动（1440/1280/1024）✅；Hover/Selected/Focus（:focus-visible accent 环）✅。

## 7.5 CEO Review 第一轮纠偏记录（2026-09-12，已修）

| CEO 指正 | 依据 Authority | 修正 |
|---|---|---|
| 空间工程部/数据分析部是 Curis 原装能力，无自有 Business；"空间工程经营"不存在 | Structure Baseline §3.2（原装部门） | 删除"空间工程经营"Business；公司版图标注"原装"，说明"不经营自有 Business，按需承接经营意图"；业务空间仅 内容增长 / Curis 产品研发 / 宠物寄养（激活中） |
| 小红书运营是旧叫法；最新结论 = 统一内容增长部有专属工作空间，内容复用，按社媒账号分发 | CONTENT_GROWTH_CEO_AUTHORITY_DECISION_RECONCILIATION + Domain Authority（Channel Account ≠ Workspace） | Business 更名 **内容增长**，Workspace 更名 **内容增长工作空间**；内容运营面新增"渠道账号"发布目标行（小红书·AI 科技/抖音/公众号，内容 Variant 按账号复用） |
| 公司版图不是部门+员工名字罗列 | ORGANIZATION_CENTER_PAGE_CONTRACT（Variant A · Department Container，Business-first，渐进展开） | 公司版图改为 Department Container：Business 为主要节点、人员默认收起（"展开人员"渐进披露）、原装部门标注、数据分析部显示经营洞察工作位 |
| 人才与能力不是公司员工罗列 | TALENT_MARKET_PRODUCT_MAP + ORGANIZATION_CENTER 合同 §3.2（外部 Expert/Skill/Connector；内部员工在员工目录） | 人才与能力改为人才市场：专家（Curis-ready 官方模板 vs 外部 Candidate，含版本/来源/安装验证边界）/ 技能 / 连接器；页头注明内部员工位置 |
| 模型配置=主流厂商全列表+输 Key 即用，且入口在左下头像菜单而非 Settings | MODEL_PROVIDER_REGISTRY（official_byok 13 厂商）+ EMPLOYEE_CONVERSATION_MODEL_EXPERIENCE_CONTRACT（左下 CEO 头像菜单 → 模型配置） | 新增左下头像菜单（模型配置/AI 能力设置、个人设置、公司设置）与 `#/models` 页：13 家主流厂商 + 聚合网关 + 本地模型（Ollama），输 Key 保存即用、模型自动发现；Settings 保留但入口语义以头像菜单为准 |

## 8. STOP GATE

本原型到此为止：不进入 Final UI Master、不改 Figma、不开发 Frontend、不改 Frozen Visual Standard。
**CURIS FULL PRODUCT HTML DESIGN PROTOTYPE — READY FOR CEO / CHATGPT REVIEW**
下一 Gate（由 CEO/ChatGPT 执行）：完整找茬 → 修 Prototype → Design Language Closure → 再决定进入 Final UI Master。
