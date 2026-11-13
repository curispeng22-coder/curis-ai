# CURIS BROWSER AUTOMATION AND AGENT LAYER

Authority Class: RESEARCH
Status: Draft（已过 Reconciliation 轮 + **Addendum 轮**）
Collected: 2026-09-18（原始）／2026-09-18 **Reconciliation 轮**／**2026-09-20 Addendum 轮**
Evidence: `evidence/02`（License 核验）、`evidence/07`（Playwright 官方约束）、`evidence/08`（browser-use / Stagehand 源码级核验）、`evidence/09`、**`evidence/10`**

> 用户明确要求：**Browser Use / Stagehand / Playwright MCP 分别解决哪一层**，且**必须读源码/官方文档验证**。
> 本文件的结论全部来自 README / 官方文档的**首手核验**，未核验项显式标注。

> ⚠️ **RECONCILIATION 声明（第 2 轮）**：本文对 §2 各项目的**分层判定全部不变**（Playwright MCP / browser-use / Stagehand 均属 **L3**）。
> **变更在 §3 的落地策略**：**首版明确采用「路线 A = 纯 Playwright 确定性」**（见新增 §3.0）；**Stagehand / browser-use 降为有准入条件的后续可选**。
> 本轮新增论据：主场景目标平台是**稳定后台 + 已知导航路径 + 确定性数据页**，且平台自身提供**「导出数据」**功能（`evidence/09` §5）→ **页面数据是规整的**，确定性选择器读取是**恰当工具**（RECONCILIATION §7.2）。

> ⚠️ **ADDENDUM 声明（第 3 轮，2026-09-20）**：新增 **§2.5**（`Tencent/BrowserSkill` = **L2 扩展形态**；`browser-use/jev-ultrafast` = **L3 动作选择器型**；`browser-use/browser-harness` = L2 观察项）；**§5 结论表新增两行**。
> **§1–§4 的分层判定与 §3.0 的首版定版（路线 A）均不变**。详见 `CURIS_BROWSER_ADDENDUM_2026-09-20_BROWSERSKILL_AND_JEV.md`、`evidence/10`。

---

## 1. 三层职责的严格定义

| 层 | 输入 | 输出 | 判断标准（"它是不是这一层？"） |
|---|---|---|---|
| **L2 Automation Runtime** | 明确指令（点击这个选择器、跳到这个 URL） | 页面状态变化 | **是否需要 LLM 才能工作？** 不需要 → L2 |
| **L3 Agent Layer** | 自然语言目标 + 页面状态 | 下一步动作 / 结构化数据 | **是否把"页面理解 + 规划"作为核心价值？** 是 → L3 |
| **L4 Session/Profile** | — | 登录态持续 | **是否管长周期状态与隔离？** 是 → L4 |

---

## 2. 逐项目判定（首手核验）

### 2.1 Playwright MCP（microsoft/playwright-mcp）→ **L3**，Token 效率型

| 项 | 核验结果 | 来源 |
|---|---|---|
| License | **Apache-2.0** ✅ | GitHub API + LICENSE 原文（`evidence/02`） |
| 维护 | Microsoft，37,242 stars，2026-09-17 有推送 | GitHub API |
| 语言 | TypeScript（Node） | 同上 |
| 接地方式 | **可访问性快照（accessibility tree）而非像素** | 官方文档（`evidence/07`） |
| 关键能力 | 持久 profile（`--user-data-dir`）、`--cdp-endpoint`、`--isolated`、`--headless`、`--browser`、`--storage-state`、`--save-trace`、`--save-session`、**`--extension`** | 官方配置文档（`evidence/07`） |
| 接入已存在浏览器 | ✅ 三种：CDP 端点、`--cdp-endpoint=chrome`（需在 `chrome://inspect` 开启"允许远程调试"）、**浏览器扩展** | 同上 |

**判定**：**L3，且是本层最"薄"的实现**——它不做规划，只把 L2 的动作**暴露为 MCP 工具**，由**外部 Agent（调用方）**负责思考。
→ 对 Curis 的意义：**它是"工具集设计"的最佳参考样板**，也可作 Provider。但注意：**它把"规划"外包给了调用方**，所以它**不能替代** Curis 自己的 Employee 规划能力。

### 2.2 browser-use → **L3（编排）**，自带 L2 调用、可选 L4/L5

首手核验（`README.md`）：
- License：**MIT** ✅（README 明示 "The Python library is free and MIT-licensed"）；作者 Magnus Müller、Gregor Žunič；115,108 stars
- 语言：**Python（>=3.11）与 TypeScript**
- 形态：三条路径 ——（1）全托管 Cloud Agent API；（2）CLI（Browser Harness，给自己的编码 agent 加浏览器能力）；（3）Python 库，本地跑 agent，「connect to a **local or cloud** browser」
- **本机浏览器复用**：README 明确 `Browser.from_system_chrome()` "to reuse a Chrome profile"，并指向 real-browser 指南与示例
- **接地方式**：README 未逐条列出 DOM/视觉方案；`use_vision` 等为已知配置项（**未在本轮核验源码**）→ 标为待核
- MCP：README 顶部含 `mcp-name: com.browser-use/browser-use`，文档含 MCP 章节
- **Cloud 的会话迁移限制（关键原文）**：
  > "Profile sync transfers **cookies, not local storage, IndexedDB, or extensions**. Some sites may require you to sign in again."
- **Cloud 的反检测卖点（关键原文）**：
  > "Browser Use is the open-source browser agent ..., a **$0.02 per browser-hour** cloud browser with **stealth, CAPTCHA solving and residential proxies**, and a hosted agent API."
- 相邻项目：`browser-use/macos-harness`（"control of Mac apps, browsers, and files"）→ **属 CGAP-02 Computer Use 范畴**

**判定**：**L3**（编排 + 规划），依赖 L2，可选 L4（profile）与 L5（cloud）。
→ 对 Curis 的意义：**其整体不宜直接采用**（它自带一套 Agent 编排，会与 Curis 的 Employee/规划体系重叠，违反"不重复造轮子"的反向约束——即 Curis 不该再引入第二个编排器）；
→ 但**其 Cloud 的"stealth + CAPTCHA solving"定位与 CGAP-04 直接冲突**，其 Cloud 路径不适配；
→ **其 `from_system_chrome()` 的思路值得借鉴**，但需按 Chrome 136 政策复核可行性（见 §4 待核项）。

### 2.3 Stagehand（browserbase/stagehand）→ **L3，且是本层**唯一**"保留 Playwright 心智模型"的抽象**

首手核验（`README.md`）：
- License：**MIT** ✅（"Copyright 2026 Browserbase, Inc."；**"Stagehand" 是 Browserbase 的商标**）
- 语言：**TypeScript / Python / Go**（v4 起三语言）
- 自我定位（原文）：
  > "**Playwright was built for testing. Stagehand is built for agents**, in TypeScript, Python, and Go."
- **本地运行（关键）**：
  ```ts
  const browser = await localBrowser.launch({ userDataDir: "./browser-data" });
  // Cookies persist in ./browser-data, so the next run starts already signed in
  ```
  → **不强制 Browserbase**；Python 侧为 `local_browser.launch(user_data_dir="./browser-data")`；"Local runs need Chrome installed."
- API 面：`observe()` / `act()` / `extract()`，外加 Playwright 风格 `goto` / `click` / `locator` / `screenshot`
- **安全特性（对 Curis 极高价值，原文）**：
  > "`observe()` returns **real selectors, so credentials never reach the model**"
  → 即：**凭据填写走 Playwright locator，不进入 LLM 上下文**。这与 Curis 的凭据边界原则**天然同向**。
- 自愈：> "`act`, `observe`, and `extract` **refresh how an action happens when the site changes** underneath it."
- Token 效率：> "**Hybrid accessibility-tree trimming** gives agents exactly the page context they need and nothing more."
- 运行形态：> "Stagehand runs **as an extension next to the browser**, cutting round-trip latency"
- 其他：WebMCP、clipboard、batch commands、**nested iframes 与 closed Shadow DOM 的 deep locators**、OTel traces
- Browserbase 侧：server-side caching（`cache: true`）、residential proxies、verified mode、session recordings、**托管 MCP（`https://mcp.browserbase.com/mcp`，暴露 navigate/act/observe/extract）**
- **注意**：托管 MCP 是**新的**；GitHub 上的 `browserbase/mcp-server-browserbase` 仓库**已归档**（`evidence/02`）——两者不是同一物，勿混淆

**判定**：**L3**，运行在 L2（Playwright）之上，**本地模式无需 L5**。
→ 对 Curis 的意义：**本层最值得优先评估的候选**。理由：①MIT 可闭源集成；②**有 Python SDK**（匹配 Curis 后端语言）；③本地 `userDataDir` 模式与 Curis 的 profile 方案完全同构；④`observe()` 的"凭据不进模型"设计直接服务 Curis 的凭据边界。

### 2.4 澄清**常见误解**（用户第 10 节明确要求）

| 常见混淆 | 澄清 |
|---|---|
| "Browser Use 是一个浏览器" | ❌ 它是 **Agent 编排框架**（L3），底层仍要一个真浏览器（L2）。它自己**不渲染任何页面**。 |
| "Playwright MCP 是 Browser Use 的替代品" | ❌ 层不同。Playwright MCP 是**工具暴露层**（L3 的薄形态），**不含规划**；Browser Use 是**含规划的编排器**。 |
| "Stagehand 是 Playwright 的竞品" | ❌ README 原文自述其**建立在 Playwright 心智模型之上**（`goto`/`click`/`locator`/`screenshot` 同名）。它是 **Playwright 之上的 AI 抽象**（L3），不是替代 L2。 |
| "用了 Browser Use 就不需要 Playwright" | ❌ browser-use 仍需 L2 浏览器；它只是把 L2 的调用包了起来。 |
| "Chromium / Playwright / CDP 是同一件事" | ❌ **Chromium = 渲染引擎（L0）**；**CDP = Chromium 暴露的调试协议（L0 的接口）**；**Playwright = 跨引擎的自动化框架（L2）**，它通过 CDP 或自有协议驱动引擎。三者是"引擎 / 协议 / 框架"的关系。 |
| "MCP 是浏览器" | ❌ MCP 是**能力暴露协议**，与浏览器无关。Playwright MCP = 用 MCP 暴露浏览器动作。 |
| "Browser Use Cloud 和 Browserbase 是一回事" | ❌ 两家公司。均为云浏览器/Agent 服务，均以 stealth/反检测为卖点，**均在 CGAP-04 上不适配**。 |

### 2.5 Addendum 轮新增项目的层判定（2026-09-20，`evidence/10`）

| 项目 | 主层 | 判定依据（原文） | Curis 判定 |
|---|---|---|---|
| **`Tencent/BrowserSkill`** | **L2**（**扩展驱动**分支）+ **窗口级 L4** | 控制面 = 扩展内 `chrome.debugger`（`architecture.md` 系统图 `Ext -->|CDP + WebExt| Tabs`；`browser-driver/` = "CDP-backed browser operations"）；**不含 LLM 规划**（仅 CLI 命令 + **21 个类型化 tool**）→ **不是 L3** | ✅ **登记为接入路径 P2 的参考实现**；**v1 不启用** |
| **`browser-use/jev-ultrafast`** | **L3**（**动作选择器**型） | 自带决策循环：页面 → **编号元素表** → Jev 选"动作 + 元素"（一次请求）；`BLOCKED` / `DONE` 为**一等动作** | ⛔ **首版不采用**（见 §5） |
| **`browser-use/browser-harness`** | **L2**（连接 / 自愈 harness） | README 自述 "Self-healing harness"，为 L3 提供 Chrome 连接 | ⚠️ 观察项 |

> ⚠️ **对 L3 分类的一处补充（重要）**：**L3 并不只有"自然语言规划器"一种形态。**
> `jev-ultrafast` 展示了一种**更轻的 L3** —— **动作是有限类型化集合（8 个），模型只输出结构化"选择 + 置信度"，不生成自然语言动作描述**，且**无 site-specific 脚本**（原文：**"There are no site-specific action scripts or prepared field strings in the policy."**）。
> → 这**改变了 §7.4 路线 B（AI 恢复）的设计输入**：未来若启用，应**优先选择"有限类型化动作空间 + 结构化选择"**形态，而非"自由文本规划"形态（`CURIS_BROWSER_ADDENDUM_2026-09-20_BROWSERSKILL_AND_JEV.md` §8.3）。

---

## 3. Curis 的 L3 设计建议：**确定性优先 + 智能兜底**

由上述核验可推出一个关键结论：**L3 不应是"要么全 LLM、要么全脚本"的二选一。**

### 3.0 首版定版（⚠️ Reconciliation 收紧）

> **首版 = 路线 A（纯 Playwright 确定性）**：**不引入任何 L3 智能层**，即下表**第 1 行即为首版唯一执行路径**。
> - **路线 B（Stagehand `act`/`observe` 自愈）= 后续可选**，须**同时**满足两条准入条件才可启用：① 确定性路径失败**已连续发生且被记录**；② 该次采集在 Evidence 中被**显式标记为"自愈路径"**（RECONCILIATION §7.4）。
> - **路线 C（browser-use 式完整 Agent）= 首版不采用**（会形成"两个规划者"，违背 Curis 四原则③④）。
> - **理由**：主场景是"**稳定后台 + 已知导航路径 + 确定性数据页**"，**确定性路径正是其最佳适用形态**；且平台自身提供「导出数据」功能，证明页面数据**规整**（`evidence/09` §5）。

**原则**（正式采用）：`Deterministic First ／ AI Recovery Second`

| 场景 | 机制 | 理由 |
|---|---|---|
| **已知平台 + 已知布局**（如公众号 datacube 后台、抖音创作者中心固定报表） | **确定性 Playwright 步骤** | 快、零 token、**可审计、可复现、Evidence 可验证**——经营数据的采集要求"同一输入得同一结果" |
| **已知平台 + 布局变更**（平台改版） | **Stagehand `act`/`observe` 自愈** | 避免每次改版都要改脚本 |
| **未知平台 / 长尾页面** | **Curis 自身规划 + a11y 快照（借鉴 Playwright MCP 的接地方案）** | 通用兜底 |
| **凭据填写** | **Playwright `locator`（Stagehand `observe()` 模式）** | **凭据不进 LLM 上下文** |

**为什么不直接把 Stagehand 或 browser-use 当作 L3 全量**：
1. **编排权必须留在 Curis**：Curis 的 Employee 是"调用能力的岗位"，若引入第二个编排器（browser-use 的 Agent），会出现**两个规划者**，违背 Curis 的四原则之③④。
2. **确定性是经营数据的硬需求**：`act()` 的"自愈"意味着**同一条指令在不同时刻可能执行不同动作**。对"采集经营指标"这类任务，**不可复现的结果会污染 Evidence 与 Learning**。
3. **但"自愈"能力值得拥有**——只是应作为**降级路径**而非主路径，并在 Evidence 中**显式标记该次采集走了自愈路径**。

---

## 4. 未核验项（诚实登记）

| 项 | 状态 |
|---|---|
| browser-use 的**具体接地实现**（DOM 编号 / a11y / vision） | README 未列明，**未读源码** → 待核 |
| browser-use `from_system_chrome()` 在 **Chrome 136 政策**下的实际可行性（默认 profile 已被禁止调试） | **未验证**，存在与 `evidence/03` 冲突的疑点 |
| Playwright MCP 的**完整工具名清单** | 本轮未取得完整清单（仅取得配置项） → 待核 |
| Stagehand v4 的**中文站点**在 a11y 快照下的表现 | 未测 |
| Stagehand `cache: true` **是否仅限 Browserbase**（本地模式是否有缓存） | README 语境指向 Browserbase，**未确认本地可用** |
| 各项目的**实际运行**（本轮未 clone 运行） | 受本机沙箱限制，未执行 |

---

## 5. L3 结论候选

| 候选 | 判定 | 类别 |
|---|---|---|
| **Playwright（L2）直接使用 + Curis 自建薄 L3** | ✅ **主路径** | Build（薄） |
| **Stagehand v4 本地模式** | ⏸ **后续可选**（首版不用）；可作为 L3 加速器候选（尤其 `observe()` 的凭据隔离设计） | Integrate（**有准入条件**，RECONCILIATION §7.4） |
| **Playwright MCP** | ✅ **借鉴其工具集设计**；可作 Provider | 借鉴 / Provider |
| **browser-use 整体** | ⛔ **首版不采用**（第二编排器 + Cloud 反检测定位） | 不采用 |
| **`browser-use/jev-ultrafast`** | ⛔ **首版不采用**（① 能力边界**不含 Shadow DOM / iframe / canvas / 上传 / 新标签页**；② **第二规划者**；③ 硬依赖 `TYPESAFE_API_KEY` **专有 SaaS**；④ **库龄 4 天**）。**但吸收**其"**结构化类型化动作空间**"与"**`DONE` ≠ 验收通过**"两条设计输入 | 不采用（设计输入） |
| **`Tencent/BrowserSkill`（L2，非 L3）** | ⚠️ **非本层**：它是 **L2 扩展形态**。登记为**接入路径 P2 参考实现**，**v1 不启用**；吸收其窗口级沙箱 / 借还语义 / `effect_state` 三态 | 参考实现 |
| browser-use `from_system_chrome` 思路 | ⚠️ 借鉴，须过 Chrome 136 复核 | 借鉴 |
| **Skyvern** | ⛔ AGPL-3.0 | 不采用 |
| **crawl4ai / ScrapeGraphAI** | ⚠️ 属内容抽取层，非浏览器自动化；可作 Provider | Provider |
| **Firecrawl** | ⛔ AGPL-3.0 | 不采用 |
