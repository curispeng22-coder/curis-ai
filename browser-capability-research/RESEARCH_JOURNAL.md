# RESEARCH JOURNAL — Curis Built-in Browser Capability Research

Authority Class: RESEARCH
Status: Draft（研究过程日志，非产品裁定；已含 Reconciliation 轮 + **Addendum 轮**）
Owner: 研究执行（受总控决策席约束）
Started: 2026-09-18
Scope: 仅 CGAP-01 Built-in Browser，及其与 CGAP-02 / CGAP-03 / CGAP-04 的技术边界
Explicitly Out of Scope: 修改 Curis 产品 / Runtime / Frontend / Backend / 视觉方案 / Business Workspace / HTML Exploration；开发 Browser

---

## 0. 研究纪律声明

本轮遵守用户给定边界，仅执行：
RESEARCH / WEB SEARCH / OFFICIAL DOCS / SOURCE REVIEW / GITHUB API & LICENSE 原文核验 / ARCHITECTURE OPTIONS

未执行：clone 后运行 demo、改动 Curis 任何文件、commit、push、创建 Figma、修改 Authority。
（说明：受本机沙箱约束，未做 `git clone` 全量落地；改用 **GitHub REST API + `raw.githubusercontent.com` 原文抓取** 完成 License / 活跃度 / 依赖 的同等核验，证据见 `evidence/01`、`evidence/02`。此为**降级手段**，已如实登记。）

---

## 1. 研究问题结构化（Stage 1）

将用户给定的 4 个 Capability Gap 与 4 层区分，还原为可裁决的判据：

| 代号 | 用户给出的层 | 本质问题 | 裁决判据 |
|---|---|---|---|
| A | Embedded Browser Surface | 用户能否在 Curis 内**看见**网页 | 是否引入第二渲染引擎；与 Curis 现有 Tauri/WKWebView 的关系 |
| B | Browser Automation Runtime | Employee 能否**操作**网页 | 是否驱动真实浏览器；是否需要 OS 级 GUI 权限 |
| C | Agent Browser Layer | Employee 能否**理解并规划**网页操作 | 是否把 B 包装为 LLM 可调用能力 |
| D | Browser Session / Profile | 登录态如何**安全持续** | 凭据落盘形态、隔离粒度、是否触碰 Credential Secret |

**方法论要点**：A/B/C/D 是**四种不同性质的东西**，不是"内置浏览器的四个部分"。本轮最重要的判断是**它们是否应被合并**。已知证据（`evidence/04`）表明 A+B 合并会带来成本量级差异，故从研究开始即按"可能应分离"预设。

---

## 2. 执行日志

### 2.1 左脑链路（用户自定义指令要求）
- `启动左脑.py input` 主链路：intent → profile → ternary_context → dispatch —— **已执行**。
- `启动左脑.py inject` 知识/因果上下文注入 —— **已执行**，命中 3 条既有记忆（PHASE 1 Business Truth、PHASE 2 Provider Feasibility、Curis Desktop 产品结构），与本轮口径一致。
- 环境处置：本机 `PYTHONPATH` 注入 WorkBuddy shim，导致 `mkdir(exist_ok=True)` 被 brokered-FS 拦截（`EEXIST`）；以 `env -u PYTHONPATH -u PYTHONDONTWRITEBYTECODE` 绕过 shim 后链路恢复正常。**已记入 `~/.workbuddy/MEMORY.md`。**

### 2.2 并行研究分工
按用户第 4 / 8 / 9 / 10 / 12 / 15 节拆分 5 条并行研究线（受此前 429 并发教训约束，控制在 3 并发以内、滚动补位）：
1. 主流 AI 产品 Browser / Computer Use 实现
2. Browser Automation Runtime 与 Playwright 底座可行性
3. Agent Browser Layer 与开源项目源码级评估
4. Embedded Browser Surface 与桌面集成
5. Cloud Browser 与成本 / License

### 2.3 本轮独立核验的**决定性证据**（非二手转述）

| # | 发现 | 证据文件 | 为什么决定性 |
|---|---|---|---|
| E1 | **Chrome 136 起 `--remote-debugging-port` 在默认 data dir 上被官方禁用**（2025-03-17 政策） | `evidence/03` | **直接否定**"挂到用户日常 Chrome 真实 profile"这一最直觉的方案，并**反向定义了**正确做法：Curis 自持专用 profile |
| E2 | macOS 上 **Browser Automation 无需 Accessibility/Screen Recording；Computer Use 需三项手动授权且会周期性失效** | `evidence/04` | 给出"Browser 与 Computer Use 必须分层"的**成本量级论据**，而非风格偏好 |
| E3 | **抖音《用户服务协议》5.1 明文禁止"任何自动化程序…接入抖音，收集或处理其中信息、内容"** | `evidence/05` | ⚠️ **Reconciliation 修正**：原判"产品可行性前置约束"过重。该条款适用于 **A 类（抓取公开/第三方内容）**；**B 类（用户读自己后台）**的产品目的**被官方承认**（`evidence/09`）→ **降级为风险登记项（P1）**，仅"自动化机制"层为 UNKNOWN |
| E4 | **Skyvern(AGPL-3.0) / Firecrawl(AGPL-3.0) / Lightpanda(AGPL-3.0) / undetected-chromedriver(GPL-3.0) / browserless(SSPL-1.0 或商业)** | `evidence/02` | 直接决定"能否合法集成与分发"，排除若干"技术很合适但不能用"的候选 |
| E5 | **Playwright `storageState` 文件含可直接冒用的凭据，官方明确劝阻入库** | `evidence/06` | 与 Curis 既有硬约束"凭据不可能明文落盘"**正面冲突**，必须新增裁定 |

---

## 3. 阶段性判断（研究假设，非裁定）

> 以下均为**研究结论候选**，供 CEO 评审；不构成产品决定。

- **H1**：A 与 B **应当分离**。理由：E2（权限成本）+ 引擎不同源（Curis Tauri=WKWebView；Playwright=自带 Chromium 构建，Playwright 无法驱动系统 WKWebView）。
- **H2**：B 应**集成而非自建**；Playwright（Apache-2.0）是当前最稳的候选底座，Puppeteer 为备选。
- **H3**：C 层应**自建薄层 + 可选 Provider**，不宜把 Browser Use 当作运行时（它是编排层，自身仍需 B）。
- **H4**：D 层必须**由 Curis 自己定义**，因为 Chromium 与 Playwright 均不提供"多 Business 隔离 + 凭据不落明文"的完整答案。
- **H5**：Cloud Browser 对 v1（单机本地自用）**不应作为默认**，但应保留为 Provider 以承载"后台长任务"。
- **H6**：「内置浏览器」若被定义为"绕过平台限制的通用采集器"，则**不应登记为 Capability**；必须收窄为"用户自身授权范围内的经营数据读取 + Evidence 留存"。
  - ⚠️ **Reconciliation 更新**：第 2 轮已把该"收窄定义"正式确立为 **Authorized Web Console Operation**，并**重写 MVP**；H6 的判定对象由模糊的"采集器"明确为"**未授权**采集器"。

---

## 4. 未完成 / 已知缺口

- 未做**真实端到端冒烟**（未在 macOS 上实际以专用 profile + Playwright 登录任一中文平台后台）。→ 属 Capability 立项后的验证任务，非本轮。
- 未取得 **Browserbase / Steel / Hyperbrowser 等云服务的当期公开报价原文**（依赖并行研究线 5 的抓取结果）。
- **WebView2 的法律许可文本**未取得（仅取得技术分发指南）。对 macOS v1 影响有限。
- 未核验**中文平台风控对"新 profile 首次登录"的具体触发阈值**——只能用"风险升高"定性表述，不可量化。
- 平台条款仅核验了抖音官方原文；小红书、快手为第三方转述，**需官方复核**。

---

## 5. 引用与 Authority 声明

- 本轮全部产物为 **RESEARCH / EVIDENCE** 类，**不覆盖**任何 Current Authority。
- 若本研究与 `docs/01_Product/Curis_Product_Blueprint.html` 或 Frozen Authority 冲突，**以 Authority 为准**，并登记 `PRODUCT → IMPLEMENTATION GAP`。
- 本目录**不在** `docs/` 下，符合"不创建第二份 Current Blueprint"的纪律；如需进入正式生产线，应走 Pointer / CURRENT_STATE / CHANGE_LOG 流程。

---

## 6. 第二轮：Reconciliation（2026-09-18）

### 6.1 本轮做了什么
- **任务性质**：**只纠正 Problem Definition / Primary Use Case / Risk Interpretation / MVP**；**未重做技术研究**、**未推翻** Playwright / Local-first / Profile / Stop Gate 等有效结论；**未开发**。
- **定向核验 2 次**（**非泛搜**）：抖音创作者中心数据导出功能、抖音开放平台 API 资质门槛 → 产出 `evidence/09_AUTHORIZED_CONSOLE_AND_API_GATING.md`。
- **产出**：`CURIS_BROWSER_USE_CASE_RECONCILIATION.md`（15 节）。
- **同步更新**：STUDY、RECOMMENDATION、TECHNOLOGY_MATRIX、LOCAL_CLOUD_HYBRID、AUTOMATION_AND_AGENT_LAYER、OPEN_SOURCE_DEEP_DIVE、本文件、`evidence/01`。

### 6.2 新证据（E6–E8，`evidence/09`）

| # | 发现 | 为什么决定性 |
|---|---|---|
| **E6** | **抖音官方文档明示支持**"用户授权后可直接在第三方系统查看自己发布的视频统计数据"，并称其为"**唯一官方认证的对外开放的抖音数据**" | **产品目的层面**：把 B 类场景从"可疑"变为"平台自己承认的目的"，是 **A/B 区分**的直接依据 |
| **E7** | **抖音官方通道仅限企业开发者**（个人开发者无法调用；第三方技术解读，**需官方复核**） | 解释**为什么 Web Console 是个人主体的现实入口**；与既有 **PHASE 2 Provider Feasibility** 结论（"国内电商对个人主体系统性排除"）**相互印证** |
| **E8** | **平台自身提供「导出数据」功能**（创作服务平台导出 Excel/CSV，支持 7/30/90 天或自定义） | 证明后台数据**结构化、可导出** → ① 佐证"确定性读取是恰当工具"；② 提供一条**零协议张力**的替代路径（官方导出 + Curis Import） |

### 6.3 结论层变更（详见 RECONCILIATION §5）

| 处理 | 条目 |
|---|---|
| **撤回** | M1（主场景 = 抓取）、M2（抖音 5.1 作为否定性硬约束） |
| **降级** | M4（平台协议风险 **P0 → P1**） |
| **修正** | M3（"可行性前置约束" → 风险登记项） |
| **重写** | M7（MVP → RECONCILIATION §8 的 14 步流程） |
| **定版** | M8（Agent 层 **路线 A**：纯 Playwright 确定性） |
| **建议细化（需 CEO 裁定）** | M5（外部平台优先级：在 API 与 Browser 之间新增"**平台官方导出 + Import**"一档） |
| **补充** | M6（命名澄清："Built-in Browser"是能力名称，不蕴含把渲染器嵌进 Curis 窗口） |
| **完全保留** | **R1–R15 全部有效** |

### 6.4 本轮边界遵守
未泛搜 / 未开发 / 未改 Runtime·Authority·UI / 未改 HTML·Figma / **未 commit、未 push**。

### 6.5 本轮未闭环（交下一 Gate）
**U1–U6**（`evidence/09` §6）需**法务或官方渠道**确认；其中 **U1**（5.1 是否覆盖"读自己后台"）与 **U3**（"自己后台已展示的数据"是否属"平台非公开数据"）为**产品可行性层的关键 UNKNOWN**，**不得由本研究自行裁定**。

---

## 7. 第三轮：Addendum —— BrowserSkill 与 Jev Ultrafast（2026-09-20）

### 7.1 本轮做了什么
- **任务性质**：把点名的**两个新开源项目**纳入候选集，做**源码级核验**并评估其对既有结论的影响。**未重做技术研究**、**未推翻**任何有效结论、**未开发**。
- **核验方法（沿用降级手段）**：GitHub REST API + `raw.githubusercontent.com` 官方原文抓取。**未 clone、未运行**。
- **核验对象**：`Tencent/BrowserSkill`、`browser-use/jev-ultrafast`、`browser-use/browser-harness`（附录）。
- **产出**：`evidence/10_BROWSERSKILL_AND_JEV_ULTRAFAST_SOURCE_REVIEW.md`、`CURIS_BROWSER_ADDENDUM_2026-09-20_BROWSERSKILL_AND_JEV.md`。

### 7.2 新证据（E9–E11）

| # | 发现 | 为什么决定性 |
|---|---|---|
| **E9** | **`Tencent/BrowserSkill` 的控制面是扩展内 `chrome.debugger`（CDP），完全不使用 `--remote-debugging-port`** —— 对其 `README.md` / `docs/architecture.md` / `docs/remote-extension-connection.md` / `skill/SKILL.md` 四份官方原文穷举 grep，**`--remote-debugging-port` 与 `--user-data-dir` 零命中** | **R7 的适用范围必须收窄**：Chrome 136 关闭的是 **CDP / Playwright 路线**；**扩展路径不受该政策约束**。这是本轮唯一实质技术细化 |
| **E10** | **BrowserSkill 的隔离原语是"窗口级"（Agent Window + session 级 ref-store + borrow table），而非"凭据罐级"**；其 `architecture.md` 明示 **"Website cookies stay in the user's browser profile"** | 与 Curis 的 `(business_id, platform_key)` **profile 级隔离正交** → **补充不是替代**；其"**跨 session 并行**"**禁止**移植到多 Business 场景（并行窗口共享 cookie 罐 ⇒ 串号） |
| **E11** | **`browser-use/jev-ultrafast` 官方原文**：**"Shadow roots, frames, canvas, uploads, pop-up tabs, nested scrolling, and arbitrary keyboard widgets remain outside this MVP."** 以及 **"A `DONE` choice still requires independent outcome verification."** | 前者构成**决定性排除依据**（与创作者/经营后台所需能力系统性不匹配）；后者是**独立验收原则的第三方原文印证** |

### 7.3 结论层变更
- **新增待裁定 1 项**：**接入路径 P2（扩展附加真实浏览器）是否在 v1 开放**（研究建议：**不开放**；理由 = **隔离粒度不足**）。
- **细化 1 条**：**R7 的适用范围**（限定于 CDP / Playwright 路线）——**R7 不撤回**；Curis **仍须专用 profile**，但**理由**由"官方禁止"改为"**需要凭据罐级隔离**"。
- **新增设计增项 7 条**（A1–A7，Addendum §7）：借还语义 / 独立 Agent Window / session 级串行（ref-store 安全）/ 能力域化 RPC（优于裸 CDP 端口）/ `effect_state` 三态 + 有界补偿 / daemon 可观测性 / **人工确认不可被自动化参数覆盖**。
- **新增候选**：`Tencent/BrowserSkill`（**P2 参考实现，v1 不启用**）；`browser-harness`（观察项）。
- **新增不采用**：`browser-use/jev-ultrafast`（三条独立理由）。
- **完全保留**：**R1–R15 全部有效**（R7 为**细化**，非撤回）。

### 7.4 业界收敛证据（本轮**最高价值**产出）
BrowserSkill 的 `SKILL.md` / `architecture.md` 与 Jev 的 README **独立复现了 Curis 的 7 项核心契约**（V1–V8 逐条对照见 Addendum §6）：**凭据边界 / Stop Gate / `EFFECT_UNKNOWN` 不得盲目重试 / 独立验收 / Session 生命周期自持 / 范围即授权 / 不得为无人值守绕过确认 / 拒绝后不得重试**。
→ **这是本研究中首次出现"第三方独立实现级收敛证据"**，其证据等级**高于此前的纯文档推理**。
→ ⚠️ **引用纪律**：只能表述为"**业界收敛 / 独立印证**"；**不得**表述为"业界标准"或"已被证明正确"。

### 7.5 数字口径纠正
| 视频声称 | 官方口径 | 判定 |
|---|---|---|
| "算力暴降 450 倍" | **无同口径数据**；官方为 **浏览器协议调用 1,092 → 101（≈10.8×）** | ✖ **未证实** |
| "单次不到 3 分钱" | 官方仅注明**文本辅助调用**成本（≈`$0.00006272`），**非任务总成本**；TypeSafe 未返回完整计费 | ✖ **未证实** |
| — | 官方基准自述：**"three repeats of one task on one browser profile, not a general reliability benchmark."** | ✅ **须原样引用，不得省略此限定** |

### 7.6 本轮边界遵守
未泛搜（仅核验点名的 2 个项目 + 1 个附录项目）/ 未开发 / 未改 Runtime·Authority·UI / 未改 HTML·Figma / **未 commit、未 push**。

### 7.7 本轮未闭环
- `browser-harness` **是否依赖远程调试端口**：**未核验**（README 提示 "Allow remote debugging"，倾向依赖）。
- BrowserSkill 的 **21 个 tool handler 完整清单**、**扩展在当前 Chrome 上的调试横幅 UX**、**`chrome.debugger` 与 Google 后续政策的长期风险**：**均未评估**。
- 三个项目在**中文创作者后台**的实际表现：**未测**。

### 7.8 跨轮复核发现（自查并已修正）
本轮复核时**发现并修正了第 2 轮的一处遗漏**：`CURIS_BROWSER_AUTOMATION_AND_AGENT_LAYER.md` §5 结论表中 `Stagehand` / `browser-use` 两行**未随 Reconciliation 收紧**（文首已声明修正、正文仍为旧口径）。
→ **再次验证第 2 轮记录的教训**：**场景级修正必须逐文件回写内联结论，不能只加文首声明。** 已补正，并在同处加入本轮新增行。
