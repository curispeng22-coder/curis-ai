# CURIS BROWSER TECHNOLOGY MATRIX

Authority Class: RESEARCH
Status: Draft（已过 Reconciliation 轮 + **Addendum 轮**）
Collected: 2026-09-18（原始）／2026-09-18 **Reconciliation 轮**／**2026-09-20 Addendum 轮**
Evidence base: `evidence/02`（License/活跃度）、`evidence/03`、`evidence/04`、`evidence/07`、`evidence/09`（官方通道与导出功能）、**`evidence/10`（BrowserSkill / Jev 源码级核验）**
License 数据来源：GitHub REST API (`license.spdx_id`) + `raw.githubusercontent.com` LICENSE 原文双重核验

> 判定口径：**Stars 仅作生态活跃度参考，不作为质量结论**。License 一律以原文核验为准。

> ⚠️ **RECONCILIATION 声明（第 2 轮）**：**本矩阵的逐层选型结论全部不变**（L0 Chromium / L1 可见真实窗口 / L2 Playwright / L4 自建 / L5 Later）。
> 变更仅在 **L3 复杂度**：**首版 = 路线 A（纯 Playwright 确定性）**，Stagehand / browser-use 降为**有准入条件的后续可选**（见 `CURIS_BROWSER_USE_CASE_RECONCILIATION.md` §7、§14）。
> 场景已明确为 **Authorized Web Console Operation**（读取用户**自有后台**中平台已向该用户展示的经营数据），**不是**抓取公开/第三方内容。
>
> ⚠️ **ADDENDUM 声明（第 3 轮，2026-09-20）**：**逐层选型结论仍全部不变**。仅新增候选行 —— **L2 新增"扩展驱动"分支行**（`Tencent/BrowserSkill`）、**L3 新增"动作选择器"型行**（`browser-use/jev-ultrafast`）；并**细化 R7 的适用范围**（Chrome 136 约束的是 **CDP / Playwright 路线**，**扩展路径不受限**）。详见 `CURIS_BROWSER_ADDENDUM_2026-09-20_BROWSERSKILL_AND_JEV.md`、`evidence/10`。

---

## 0. 先立坐标：五个不可混淆的层

本矩阵横向按**能力层**组织，纵向按**候选技术**组织。**同一个项目只能被放在一层**，跨层项目（如 browser-use 既是编排又自带运行时）需显式标注主层与依赖层。

| 层 | 名称 | 唯一职责 | Curis 应"Build"还是"Integrate" |
|---|---|---|---|
| **L0** | Browser Engine | 渲染、JS 执行、网络栈 | **绝不 Build**（用户明确要求：不重复造浏览器）→ Integrate |
| **L1** | Embedded Surface | 让用户**看见**网页 | Integrate（或**不 Build**，见 §2 结论） |
| **L2** | Automation Runtime | 让程序**操作**网页 | Integrate |
| **L3** | Agent Browser Layer | 让 LLM **理解并规划**网页操作 | **Build 薄层** + 可选 Integrate/Provider |
| **L4** | Session / Profile | 登录态安全持续 | **Build**（必须自建，见 `SESSION_AND_SECURITY_MODEL`） |

---

## 1. L0 — Browser Engine 候选

| Engine | 分发形态 | License | macOS ARM | 可否被 CDP 驱动 | Curis 判定 |
|---|---|---|---|---|---|
| **Chromium（源码）** | 自行构建 | **BSD-3-Clause**（`evidence/02`） | ✅ | ✅ | 不直接使用（构建成本极高） |
| **Playwright 的 Chromium 构建** | `ms-playwright` 缓存（≈281MB） | BSD/Apache 类（待法务复核编解码器） | ✅ | ✅（Playwright 控制） | ✅ **推荐（经 L2 引入）** |
| **Chrome for Testing** | 独立分发通道 | Chromium 同源 | ✅ | ✅ | ✅ 备选（Google 官方对自动化的推荐） |
| **系统 Chrome / Edge（`channel:'chrome'`）** | 用户已装 | 专有（用户自持） | ✅ | ✅ | ✅ 主方案（免分发体积） |
| **CEF** | 嵌入库（C++） | **BSD-3-Clause**（原文核验） | ✅ | 部分（需自建桥） | ⚠️ 仅在"必须在 Curis 内嵌 Chromium"时才考虑；v1 不必要 |
| **WKWebView** | macOS 系统 | 系统 SDK | ✅ | ❌ **无法被 Playwright/CDP 控制** | ⚠️ 仅作 Curis 自身 UI；**不可作自动化目标** |
| **WebKitGTK** | Linux | LGPL | n/a（非 macOS） | ❌ | 不适用（v1 单机 macOS） |
| **WebView2 / WebView2 Runtime** | Windows | 专有（技术分发指南已核验，法律文本待核） | ❌ | 部分 | 不适用（v1 macOS） |
| **Lightpanda** | 自研轻量引擎（Zig） | **AGPL-3.0** ⛔ | ? | 部分 | **不采用**（License 阻断闭源分发） |
| **Gecko / Firefox 构建** | `ms-playwright`（≈187MB） | **MPL-2.0** | ✅ | ❌（无 CDP） | 不采用（无 CDP，且体积成本） |
| **Playwright WebKit 构建** | `ms-playwright`（≈180MB） | LGPL/BSD | ✅ | ❌ | 不采用（**非 Safari，且无法驱动系统 WKWebView**） |

**关键结论**：**在 macOS 上，"可被自动化控制"与"可被嵌入 Curis 窗口"是两个互斥集合。**
- 可被 CDP 控制 → 只有 Chromium 系（且 Playwright 无法驱动系统 WKWebView / 系统 Safari）。
- 可直接嵌入 Curis（Tauri）→ 只有系统 WKWebView（不可被控制）。
→ 这就是 **L1 与 L2 必须分离的第一性理由**（第二理由是 `evidence/04` 的权限成本差异）。

---

## 2. L1 — Embedded Surface 候选

| 方案 | 是什么 | 用户能看见 | 能被 Employee 控制 | 引入新引擎 | Curis 判定 |
|---|---|---|---|---|---|
| **Tauri WebviewWindow + `WebviewUrl::External`** | Tauri 2 可在窗口内加载任意外部 URL | ✅ 真正嵌在 Curis 内 | ❌（WKWebView，无 CDP） | 否（复用系统 WebView） | ⚠️ **仅适用于"只让用户看"的只读预览** |
| **Tauri multi-webview（`window.add_child`）** | 单窗口内多 WebView 面板 | ✅ | ❌ | 否 | ⚠️ 同上；且官方标注 **unstable feature** |
| **Electron `BrowserView`/`WebContentsView`** | 嵌入 Chromium | ✅ | ✅（可开调试端口） | **是**（+Chromium 体积） | ❌ 会要求 Curis 从 Tauri 迁到 Electron，代价过大 |
| **CEF 嵌入** | 自嵌 Chromium | ✅ | 需自建桥 | **是** | ❌ 工程成本远超收益 |
| **独立 headed Chrome/Chromium 窗口（Playwright 启动）** | **一个真实浏览器窗口，Curis 之外的 OS 窗口** | ✅ | ✅ **同一实例，同一 profile** | 否（复用已引入的 L2 引擎） | ✅ **推荐主方案** |
| **headless + CDP `Page.startScreencast` 帧流转发** | 把画面流进 Curis 面板 | ✅（作为 Curis 内面板） | ✅ | 否 | ✅ **可选增强**（观察/回放）；**不替代**登录场景 |

### 2.1 核心判断：Curis 是否"需要自己拥有一个内置 Browser Surface"？

**答案（研究假设）：区分两种语义。**

| 语义 | 是否需要 Curis 自建 | 理由 |
|---|---|---|
| "用户能在 Curis **应用内**看到网页"（`WebviewUrl::External`） | **不需要作为自动化能力**，且**不应**与自动化绑定 | 系统 WKWebView 无法被自动化；绑定会制造"看得见但控制不了"的伪能力 |
| "用户在 Curis 发起、**能看到**真实被操作的浏览器" | **需要**，但载体是 **Playwright 启动的独立 Chrome 窗口**，不是嵌入式 WebView | 同一实例 = 同一 profile = 同一会话 = 用户可随时接管（这是 CGAP-04 实现的前提） |

→ **结论**：Curis **不需要自建浏览器渲染表面**；它需要的是 **"一个由 Curis 友好启动的、用户可见且可接管的真实浏览器窗口"**。
→ 嵌入式 WebView（Tauri External URL）保留为**只读预览/结果呈现**用途，**不承担自动化职责**。

**这一判断顺带解决一个产品一致性风险**：若把"Curis 内嵌网页"当作自动化表面，用户会看到页面但 Employee 无法操作它（技术不可行），形成产品级欺骗。必须避免。

---

## 3. L2 — Automation Runtime 候选

| Runtime | 语言 | License | 驱动引擎 | 连接已存在浏览器 | 持久 profile | 用户可见 | MCP | macOS ARM | Curis 判定 |
|---|---|---|---|---|---|---|---|---|---|
| **Playwright** | TS / **Python** / .NET / Java | **Apache-2.0** ✅ | Chromium, Firefox, WebKit（**自带构建**） | ✅ **仅 Chromium**（`connect_over_cdp`） | ✅ `launchPersistentContext` | ✅ `headless:false` | 官方有 `playwright-mcp` | ✅ | ✅ **推荐主底座** |
| **vercel-labs/agent-browser** | **Rust**（CLI + daemon，**无 Node 依赖**） | **Apache-2.0** ✅ | Chrome for Testing（默认）/ lightpanda（⚠️AGPL 勿用） | ✅ `connect` / `--cdp` / `--auto-connect` | ✅ `--restore` + 稳定 `--session` | 待核（headed 支持未确认） | 内置 `mcp`（stdio） | ✅ | ✅ **R1.5 强备选**（labs continuity 风险） |
| **Puppeteer** | TS/JS | **Apache-2.0** ✅ | Chrome / Chrome for Testing / Firefox | ✅（CDP） | ✅（userDataDir） | ✅ | 社区 | ✅ | ✅ 备选（生态不如 Playwright 广，Python 侧弱） |
| **raw CDP**（`chrome-remote-interface` 等） | 多语言 | MIT 类 | Chromium only | ✅（本质） | 需自行管理 | ✅ | 有 | ✅ | ⚠️ 作为 Playwright 的**补充通道**（取 Playwright 未暴露的域），不作主底座 |
| **Selenium / WebDriver** | 多语言 | **Apache-2.0** ✅ | 多浏览器（经 driver） | ✅ | 部分 | ✅ | 有 | ✅ | ⚠️ 不推荐（协议层更薄，异步/自动等待能力弱） |
| **WebDriver BiDi** | 规范 | 规范 | Chromium/Firefox | ✅ | 部分 | ✅ | — | ✅ | ⚠️ 关注（Playwright 未采用；生态未成熟） |
| **Cypress** | TS | MIT | 自有（跑在浏览器内） | ❌ | ❌ | ✅ | — | ✅ | ❌ 不适用（架构为测试设计，非任务自动化） |
| **patchright** | TS | Apache-2.0 | Chromium | ✅ | ✅ | ✅ | — | ✅ | ⛔ **不采用**（反检测，与 CGAP-04 冲突） |
| **SeleniumBase CDP Mode** | Python | MIT | Chromium | ✅ | ✅ | ✅ | 内置 MCP | ✅ | ⛔ **不采用**（同上；其卖点是"bypasses bot-detection"） |
| **undetected-chromedriver** | Python | **GPL-3.0** ⛔ | Chrome | ✅ | ✅ | ✅ | — | ✅ | ⛔ 双不合（License + 反检测） |
| **DrissionPage** | Python | 宽松（待核） | Chromium/CDP | ✅ | ✅ | ✅ | — | ✅ | ⚠️ 中文生态可用；**需核 License 与维护状态** |
| **`Tencent/BrowserSkill`**（**扩展驱动**） | Rust（CLI + daemon）+ TS（MV3 扩展） | **MIT** ✅ | 用户既有 Chrome / Edge（**扩展内 `chrome.debugger`**） | ✅ **扩展附加**（**不使用远程调试端口**） | ✅（用户日常 profile） | ✅（**独立 Agent Window**） | ❌（CLI + Skill 形态） | ✅ | ⚠️ **L2 的"扩展形态"分支**：能力域化为 **21 个类型化 tool**；隔离仅**窗口级**；**登记为接入路径 P2 参考实现，v1 不启用**（`evidence/10` §2–§5） |

### 3.1 Playwright 是否足以作为 Curis 底座？

| 需求 | Playwright 是否解决 | 说明 |
|---|---|---|
| 导航 / 点击 / 输入 / 滚动 / 选择 | ✅ 完全 | 核心能力 |
| 读 DOM | ✅ 完全 | 选择器体系 + `evaluate` |
| 读可访问性树 | ✅ | `ariaSnapshot()`（含 `mode:'ai'` 输出，专为 LLM 设计）；**旧 `page.accessibility.snapshot()` 已弃用/移除** |
| 截图 | ✅ 完全 | 页面/整页/元素级 |
| 下载 / 上传 | ✅ 完全 | `download` 事件 / `setInputFiles` |
| 多标签 / 弹窗 | ✅ 完全 | `context.on('page')` |
| 权限管控 | ✅ 完全 | `context.grantPermissions`（**默认拒绝为佳**） |
| 持久登录态 | ✅ | profile 目录（**且 Chrome 136 政策要求正是如此**） |
| 执行轨迹 / Evidence | ✅ 强 | **Trace Viewer**（`context.tracing`）、video、HAR（`recordHar`） |
| headed / 用户可见 | ✅ | `headless:false`；人类可同时操作 |
| **登录态获取本身** | ❌ **不解决** | 必须由用户在窗口中手工完成 |
| **CAPTCHA / MFA 停止** | ❌ 不解决 | 需自建检测 + Gate（CGAP-04） |
| **Pause / Resume** | ❌ 无原语 | 无内置 HITL；需编排层自持 checkpoint |
| **页面理解 / 规划** | ❌ 不解决 | 属 L3 |
| **Evidence 的业务语义** | ❌ 不解决 | 属 Curis 自身（L4/Evidence） |
| **多 Business 隔离策略** | ❌ 不解决 | Playwright 提供机制（多 context/profile），**策略必须 Curis 定** |

→ **判定：Playwright 是充分且必要的 L2 底座；但它只覆盖"操作"这一层。Curis 必须在 L1 / L3 / L4 自建或另选。**

### 3.2 Playwright 在 macOS/Tauri 上的 5 大集成风险
1. **Node 驱动依赖**：Playwright Python 仍依赖 Node 驱动进程 → 引入 Node 运行时（分发体积 + 进程管理）。
2. **浏览器体积**：Chromium ≈281MB（若不自带则需引导用户下载，或复用系统 Chrome 免体积）。
3. **Chrome 136 政策**：**必须**自持 profile 目录；任何"复用日常 profile"的实现都会被 Chrome 拒绝（官方文档级已确认）。
4. **SingletonLock**：同一 profile 不能双实例 → **并发采集需多 profile 或串行**（直接影响 Automation Queue 设计）。
5. **版本钉死**：Playwright 1.x 绑定特定浏览器修订；**升级 Playwright 会替换底层浏览器**，可能改变被自动化站点的行为 → 需纳入回归测试闸。

---

## 4. L3 — Agent Browser Layer 候选

（详见 `CURIS_BROWSER_AUTOMATION_AND_AGENT_LAYER.md` 与 `CURIS_BROWSER_OPEN_SOURCE_DEEP_DIVE.md`）

速览：

| 项目 | License | 层 | 定位 | Curis 判定 |
|---|---|---|---|---|
| **Playwright MCP** | **Apache-2.0** ✅（已核验） | L3 | 把浏览器动作暴露为 MCP 工具；基于 a11y 快照而非像素 | ✅ **优先评估**（作为 Provider 或借鉴工具集设计） |
| **browser-use** | **MIT** ✅ | L3（依赖 L2） | Agent 编排 + 元素索引化 DOM 序列化 | ⚠️ **首版不采用**（第二编排者）；可借鉴元素编号方案；Cloud 路径与 CGAP-04 冲突 |
| **Stagehand** | **MIT** ✅ | L3（L2 之上抽象） | `act` / `extract` / `observe` 自然语言操作 + 确定性重放 | ⏸ **后续可选**（首版不用）；**仅作有准入条件的降级路径**（RECONCILIATION §7.4） |
| **nanobrowser** | Apache-2.0 ✅ | L3（浏览器扩展形态） | 扩展内多 Agent 工作流 | ⚠️ 形态不符（Curis 是桌面 App 而非扩展） |
| **Skyvern** | **AGPL-3.0** ⛔ | L3 | 表单/工作流自动化 | ⛔ 不采用（License） |
| **Agent-S** | Apache-2.0 ✅ | L3/Computer Use | 类人电脑操作框架 | ⚠️ 偏 Computer Use，非浏览器专精 |
| **OmniParser** | CC-BY-4.0（**模型权重条款另计**） | 视觉接地模型 | 截屏 → 结构化 UI 元素 | ⚠️ 属 Computer Use 提升件，**非浏览器必需** |
| **cua** | MIT ✅ | Computer Use 基建 | 跨 OS 驱动 + macOS 虚拟化（Lume） | ⚠️ 属 CGAP-02，非本轮 |
| **crawl4ai / Firecrawl / ScrapeGraphAI** | Apache-2.0 ✅ / **AGPL-3.0** ⛔ / MIT ✅ | **另一层**（服务端抓取/抽取） | 不是浏览器自动化 | ⚠️ Firecrawl 不可闭源集成；其余可作 **Provider** |
| **OpenAdapt** | MIT ✅ | GUI 记录重放 | 非浏览器 | ⚠️ 属 CGAP-02 参考 |
| **`browser-use/jev-ultrafast`** | **MIT** ✅ | L3（**动作选择器**型） | 页面 → **编号元素表** → **Jev 模型直接选"动作 + 目标元素"**（一次请求）；仅 `TYPE_TEXT` 调小模型 | ⛔ **首版不采用**（① 能力边界**无 Shadow DOM / iframe / canvas / 上传 / 新标签页**；② **第二规划者**；③ 硬依赖 `TYPESAFE_API_KEY` **专有 SaaS**；④ **库龄 4 天**）（`evidence/10` §6） |
| **`browser-use/browser-harness`** | **MIT** ✅ | L2（连接 / 自愈 harness） | 连接 Chrome（README 提示"Allow remote debugging"） | ⚠️ **观察项**；须核验其是否依赖远程调试端口（若依赖，则受 Chrome 136 约束） |

---

## 5. L4 — Session / Profile

（完整设计见 `CURIS_BROWSER_SESSION_AND_SECURITY_MODEL.md`）

| 项 | 结论候选 |
|---|---|
| 载体 | Persistent Context（profile 目录）为主 |
| 隔离 | `(business_id, platform_key)` 二维独立 |
| 凭据 | Curis 不解析会话内容；仅持映射 + 有效性信号 |
| 落盘 | **需新增裁定**（现有凭据体系未覆盖"浏览器会话材料"） |
| 接入路径 | P1（自启专用 profile）**默认**；P2（Extension 附加真实浏览器）**为显式例外，v1 不开放**；P3（外部 CDP）不推荐。<br>⚠️ **Addendum 轮细化（2026-09-20）**：**P2 在 Chrome 136 之后仍然可行**——扩展路径（`chrome.debugger`）**不受**调试端口政策约束，参考实现 `Tencent/BrowserSkill`（MIT）。**否决 P2 的真实理由是"隔离仅窗口级，无法服务多 Business 的凭据罐隔离"**，**不是"被 Chrome 禁止"**。详见 `CURIS_BROWSER_SESSION_AND_SECURITY_MODEL.md` §2.1、`evidence/10` §4–§5 |

---

## 6. L5 — Cloud / Remote Browser Provider

观测日期：**2026-09-18**。**核验状态**列标注该行数据来源：`✔独立复核` = 本目录直接抓取厂商页确认；`△转述` = 来自并行研究的二手汇总，**未经独立复核**；`未公开` = 厂商未公布。

| Provider | 开源? (License) | 自托管 | 免费额度 | 公开起步价 | 会话持久化 | MCP/SDK | 核验 | **CGAP-04 兼容性** |
|---|---|---|---|---|---|---|---|---|
| **Browserbase** | 核心闭源；Stagehand=**MIT** ✅；官方 MCP repo **已归档** | ❌ | ✔ **$0：3 并发 / 1 浏览器小时 / 单 session 15 分钟** | ✔ **Developer $20/mo：25 并发 + 100 浏览器小时，超出 $0.12/浏览器小时**；Startup $99/mo：100 并发 + 500 小时，超出 $0.10/h | Contexts（可复用 profile） | SDK + MCP | **✔独立复核** | ⛔ **官方能力清单含 "Auto captcha solving"（Developer 起）与 "Stealth Mode"（Basic/Advanced）** |
| **Steel** | `steel-browser` = **Apache-2.0** ✅ | ✅（OSS server） | △转述 | △转述（`steel.dev/pricing` 实际返回首页，**价格未取得**） | 上下文/cookie 注入与复用 | SDK/CDP | **△转述 + 部分✔**（官网确认能力，未确认价格） | ⛔ **官网明示 "Auto CAPTCHA solving"、"Proxy and Browser Fingerprinting（never worry about getting flagged as a bot again）"、"Auto Sign-In"** |
| **Browserless** | 受限 | ⚠️ **商用需购商业许可** | △转述 | △转述 | 持久 session + replays | MCP + Playwright/Puppeteer | △转述 | ✅（无 stealth 卖点记录） |
| **Hyperbrowser** | ❌ 闭源云 | ❌ | △转述 | △转述 | 持久 + **指纹随机化** | SDK | △转述 | ⛔ **指纹随机化** = 反检测 |
| **BrowserCat** | ❌ | ❌ | △转述 | △转述 | 交互式多步/登录 session | Playwright/Puppeteer/CDP；MCP | △转述 | ⚠️ 未核验 |
| **Anchor** | ❌ | BYOC/On-prem（Enterprise） | △转述 | △转述 | **自动重登 + MFA** | MCP 原生 | △转述 | ⛔ **自动重登 + MFA 代填 = 直接违反 CGAP-04** |
| **Kernel** | ❌ | 未公开 | △转述 | △转述 | managed auth + vaults | Playwright/CDP/BiDi | △转述 | ⚠️ 需逐项配置审查 |
| **Notte** | ❌ | Enterprise | △转述 | △转述 | personas/sessions/vaults | SDK | △转述 | ⚠️ 未核验 |
| **Lightpanda Cloud** | **AGPL-3.0** ⛔ | ✅ | △转述 | △转述 | CDP | CDP/Puppeteer/Playwright；MCP | △转述 | ⚠️ License 阻断自托管集成 |
| **Cloudflare Browser Rendering** | `cloudflare/puppeteer` = **Apache-2.0** ✅ | ❌ | △转述 | △转述 | reuse sessions | Puppeteer/Playwright/CDP/MCP | △转述 | ⚠️ **未核验**（不可据转述判定干净） |
| **AWS Bedrock AgentCore Browser** | ❌ | ❌ | △转述 | △转述 | Live View + Session Replay | SDK | △转述 | ⚠️ 未核验 |
| **Azure Playwright Workspaces** | ❌ | ❌ | 未公开 | **未公开** | 动态 session | Playwright | △转述 | ⚠️ 定价不可得 |
| **E2B** | OSS sandbox | Enterprise（BYOC） | △转述 | △转述 | **非浏览器**（代码 sandbox） | SDK | △转述 | ⚠️ 层不符 |

### 6.1 ⛔ **不可启用的云端能力（产品原则硬约束）**

本表新增"CGAP-04 兼容性"列后暴露一个**必须显式处理**的问题：

**主流云浏览器厂商把"自动解 CAPTCHA / 自动重登 + MFA / 指纹伪装 / stealth"作为核心卖点。** 这一点已被**独立复核**（Browserbase、Steel 官网均直书其能力清单）。原因是这些厂商的目标客户是**大规模抓取与 RPA**——在那个场景里规避风控是产品价值本身。

**这与 Curis 的 CGAP-04 承诺正面冲突**：CGAP-04 要求"遇 CAPTCHA / MFA / 风控提示 **立即 STOP**、绝不规避"。若接入这些 Provider 的默认能力，等于 Curis 替用户规避平台风控，将 `evidence/05` 所载的平台协议与法律风险直接转移给用户。

→ **研究建议（须 CEO 裁定）**：
1. 若采用云 Provider，**必须在接入层显式关闭** captcha 求解、自动重登、MFA 代填、指纹随机化、stealth 等能力；**未确认可关闭者不予采用**，即便价格更低。
2. 按此标准，Browserbase（Developer 起含 captcha solving）、Steel、Anchor（自动重登+MFA）、Hyperbrowser（指纹随机化）**在当前原则下均不适配**。
3. 本列的净结论是：**"云浏览器"这一品类的主流商业定位与 Curis 的安全承诺不兼容**——这不是挑供应商的问题，而是品类定位冲突。该结论会显著加强 Local-first 的论证（见 `CURIS_BROWSER_LOCAL_CLOUD_HYBRID_OPTIONS.md`）。
4. 标注 `△转述` 的行**不得作为决策依据**，需在立项前逐项独立复核。
5. **（Reconciliation 补充）** 场景修正（读取自有后台而非抓取第三方）**不改变本节结论**——云浏览器的品类定位（规避风控）与 Curis 的"遇验证即停"承诺仍然冲突；且**场景修正后更不需要云**（自有后台天然是"用户本机 + 本机登录态"）。此外，平台官方**导出文件 + Curis Import** 提供了一条**完全不依赖云**的更干净路径（`evidence/09` §5）。

---

## 7. 汇总：Build / Integrate / Provider / Later

| 层 | 结论 | 类别 |
|---|---|---|
| L0 Browser Engine | Playwright/系统 Chrome 的 Chromium | **Integrate**（绝不自建） |
| L1 Embedded Surface | Playwright 启动的**可见真实浏览器窗口** | **Integrate**（不自建引擎） |
| L2 Automation Runtime | **Playwright**（Apache-2.0） | **Integrate** |
| L3 Agent Browser Layer | Curis 自建**薄层**；**首版 = 路线 A（纯 Playwright 确定性，无 L3 智能层）**；后续可按准入条件启用自愈；可借鉴 Playwright MCP 工具集设计 | **Build（薄）** + Provider 可选 |
| L4 Session / Profile | 自建（映射 + 隔离 + 有效性检测） | **Build** |
| L4 Auth Stop Gate | 自建（框架无 HITL 原语） | **Build** |
| L5 Cloud Provider | 仅承载后台长任务 | **Provider**（不集成） |
| Computer Use（CGAP-02） | 与 Browser 并列，不合并 | **Later** |
