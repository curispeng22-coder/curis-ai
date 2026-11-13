# CURIS BUILT-IN BROWSER CAPABILITY STUDY

**CGAP-01 Built-in Browser — 能力缺口研究报告**

Authority Class: **RESEARCH**（非 Current Authority；不修改任何 Curis 产品/Runtime/UI 决定）
Status: **Draft — Ready for CEO Review（已过 Reconciliation 轮 + Addendum 轮）**
Owner: 研究执行（受总控决策席约束）
Date: 2026-09-18（原始）／2026-09-18 **Reconciliation 轮**／**2026-09-20 Addendum 轮**
Supersedes / Related: 无。本文与 `docs/01_Product/Curis_Product_Blueprint.html` **不构成替代关系**；若冲突，以 Blueprint 为准。

Evidence: `evidence/01`–`evidence/10`

---

## ⚠️ RECONCILIATION 声明（2026-09-18 第 2 轮，**必须先读**）

本报告的**技术结论全部有效**，但**问题定义与风险定性已被修正**。请以
**`CURIS_BROWSER_USE_CASE_RECONCILIATION.md`** 为准阅读以下三节：

| 受影响位置 | 状态 | 说明 |
|---|---|---|
| §0 结论摘要 第 8 条 | ⚠️ **修正** | 平台协议风险从"P0 前置约束"**降级为 P1 风险登记项**；须区分 A 类（抓取公开/第三方内容）与 B 类（自有后台读取） |
| §8 平台合规 | ⚠️ **修正** | 上一轮把 A 类风险**未经分析等同于 B 类**。新增官方证据（`evidence/09`）：抖音官方**承认并支持**"用户授权后在第三方系统查看自己数据"这一产品目的；但**自动化机制层面仍为 UNKNOWN** |
| §11 第 1 / 2 / 18 问 | ⚠️ **修正** | 第 1 问"内置 Browser Surface"→ 补命名澄清；第 2 问同；第 18 问 MVP → **已重写**（见 RECONCILIATION §8） |
| §11 第 6 问（Agent 层） | ⚠️ **收紧** | 首版明确选 **路线 A（纯 Playwright 确定性）**；Stagehand/browser-use 降为后续可选 |
| §11 第 20 问 | ⚠️ **更新** | 登记条件更新（见 RECONCILIATION §15 第 15 问） |
| **§1–§7、§9、§10、§12、§13 及 R1–R15 全部结论** | ✅ **完全有效** | 技术选型**未因场景修正而变化** |

**一句话**：**变的是"我们为什么做"和"首版做到哪一步"，不是"用什么做"。**

---

## ⚠️ ADDENDUM 声明（2026-09-20 第 3 轮）

新增候选的源码级核验已完成，见 **`CURIS_BROWSER_ADDENDUM_2026-09-20_BROWSERSKILL_AND_JEV.md`** 与 **`evidence/10`**。

| 项 | 状态 | 说明 |
|---|---|---|
| **R7（Chrome 136）** | ⚠️ **细化适用范围** | Chrome 136 关闭的是 **`--remote-debugging-port` 在默认 data dir 上**，即 **CDP / Playwright 路线**；**浏览器扩展（`chrome.debugger`）是另一条通道，不受该政策约束**（`Tencent/BrowserSkill`，MIT，为现成证明）。**R7 不撤回**：Curis **仍须专用 profile**，但**理由**由"官方禁止"改为"**需要凭据罐级隔离**"（扩展路径的隔离是**窗口级**） |
| **§11 第 6 问（Agent 层）** | ⚠️ **补充** | L3 出现一种**更轻的形态**：`jev-ultrafast` 的"**有限类型化动作空间（8 个）+ 结构化选择 + 置信度**"（非自然语言规划）→ 作为未来**路线 B** 的设计输入，**不进首版** |
| **§11 第 15 问（候选）** | ⚠️ **补充** | 候选清单**新增 2 项**：`Tencent/BrowserSkill`（**P2 参考实现，v1 不启用**）、`browser-harness`（观察项）；新增**不采用** 1 项：`browser-use/jev-ultrafast` |
| **接入路径 P2** | 🆕 **新增待裁定项** | **P2（扩展附加真实浏览器）在 Chrome 136 之后仍然可行**，但因**隔离仅窗口级、无法服务多 Business 凭据罐隔离**，**研究建议 v1 不开放** |
| **R1–R15** | ✅ **全部保留** | 本轮**无一条结论被推翻**；技术选型未变 |

**一句话**：**第三轮是候选集的扩充与一条适用范围的细化，不是技术选型的变更。**

---

## 0. 结论摘要（先给结论）

1. **「内置浏览器」不是一个东西，是四个东西。** 用户给出的 A/B/C/D 四层区分是**正确且必要**的；本研究的核心结论是**它们不应被合并**（§2）。
2. **Curis 不需要自建 Browser Engine。** Playwright（Apache-2.0）足以作为自动化底座，且**无需引入任何 AGPL/GPL/SSPL 依赖**（§5）。
3. **在 macOS 上，「可被自动化控制」与「可被嵌入 Curis 窗口」是两个互斥集合** —— 这是 L1/L2 必须分离的第一性理由（§2.2）。
4. **"复用用户日常 Chrome 的登录态"这条路已被 Chrome 官方关闭**（Chrome 136，2025-03）。正确形态是 **Curis 自持专用 profile 目录，用户在其中登录一次** —— 这在安全上**优于**原设想（§4.1）。
5. **Authentication Stop Gate 必须由 Curis 自建**：Playwright / Puppeteer / 各 Agent 框架**均无 Pause/Resume 原语**（§6）。
6. **云浏览器与 CGAP-04 存在品类级冲突**：主流云厂商（Browserbase、Steel、browser-use Cloud、Anchor、Hyperbrowser）以"自动解 CAPTCHA / 自动重登 + MFA / 指纹伪装"为核心卖点（已独立复核）。**这不是挑供应商的问题**（§7）。
7. **成本不是决策判据**：云端 ≈$0.9–20/月，本地 ≈$0/月，**都在可忽略量级**。任何以"云更便宜"为据的论证不成立（§7.2）。
8. ⚠️ **RECONCILIATION 修正**（原表述"平台合规是产品可行性前置约束"）：抖音 5.1 的适用面限于 **A 类（抓取公开/第三方内容）**；**B 类（用户读自己后台）**的产品目的**被官方承认**（抖音官方文档明示支持"用户授权后在第三方系统查看自己数据"，`evidence/09`）→ 本项**降级为 P1 风险登记项**，仅"自动化机制"层为 UNKNOWN（§8）。
9. **是否登记为正式 Capability：可以登记，但必须收窄定义。** 当前定义的"内置浏览器"若指"绕过平台无 API 限制的通用采集器"，**不应登记**（§11）。⚠️ **RECONCILIATION**：收窄后的正式定义 = **Authorized Web Console Operation**（对**用户本人已授权** Web 后台的操作能力）；判定对象由模糊的"采集器"改为"**未授权**采集器"。

---

## 1. 研究范围与纪律

- **范围**：CGAP-01 Built-in Browser，及其与 CGAP-02 Computer Use / CGAP-03 Automation Trigger / CGAP-04 Auth Stop Gate 的**技术边界**。
- **严格遵守用户边界**：本轮仅 RESEARCH / WEB SEARCH / OFFICIAL DOCS / SOURCE REVIEW / ARCHITECTURE OPTIONS。**未修改** Curis 任何产品文件、Runtime、Frontend、Backend、视觉方案、Business Workspace、HTML Exploration；**未开发** Browser；无 commit / push；未创建 Figma。
- **方法降级声明**：受本机沙箱限制，**未执行 `git clone` 与本地运行**；以 **GitHub REST API + `raw.githubusercontent.com` 原文抓取** 完成 License / 活跃度 / 依赖 / API 面的同等核验。此为降级手段，已如实登记（`RESEARCH_JOURNAL.md` §0）。
- **左脑链路**：按用户长期约定，输入已经 `启动左脑.py input` 主链路与 `inject` 上下文注入（`RESEARCH_JOURNAL.md` §2.1）。

---

## 2. 核心问题：所谓"内置浏览器"到底应该是什么？

### 2.1 四层还原

| 层 | 用户给出的名字 | 本质 | 唯一职责 |
|---|---|---|---|
| **L1** | Embedded Browser Surface | 用户能否在 Curis 内**看见**网页 | 呈现 |
| **L2** | Browser Automation Runtime | Employee 能否**操作**网页 | 操作 |
| **L3** | Agent Browser Layer | Employee 能否**理解并规划**网页操作 | 理解与规划 |
| **L4** | Browser Session / Profile | 登录态如何**安全持续** | 状态与隔离 |

**关键认识**：这四层**不是同一事物的四个部分**，而是**四种不同性质的能力**（呈现 / 操作 / 认知 / 状态）。把它们打包成"一个内置浏览器"，是本轮研究要否定的直觉。

### 2.2 L1 与 L2 为什么必须分离（两条独立理由）

**理由一（第一性）：在 macOS 上两者是互斥集合。**

| 方向 | 可行载体 | 不可行 |
|---|---|---|
| 可被程序控制 | 仅 **Chromium 系**（CDP）；Playwright 官方文档明确 `connect_over_cdp` **仅支持 Chromium 系** | Playwright **无法驱动系统 WKWebView / 系统 Safari**（其 WebKit 是自带补丁构建，非 Safari） |
| 可直接嵌入 Curis | 仅 **系统 WKWebView**（Tauri 默认） | WKWebView **不可被 Playwright/CDP 控制** |

→ 若强行合并，会得到**"用户看得见但 Employee 操作不了"**的伪能力。这是**产品级欺骗**，必须避免。

**理由二（成本量级）：两者在 macOS 上的权限成本差一个量级。**

| 能力 | 所需 macOS TCC 权限 | 稳定性 |
|---|---|---|
| **Browser Automation**（Playwright 经 CDP 控制自带 Chromium） | **无需 Accessibility / Screen Recording** | 高（不依赖 TCC） |
| **Computer Use**（合成键鼠 + 截屏） | **Accessibility + Screen Recording + Automation 三项手动授权** | 低（签名/路径/版本变更即失效；Screen Recording 每月需复认） |

→ 若把 Web 自动化实现为"Computer Use 的一个用例"（截屏 + 点坐标操作浏览器），会**主动继承 Computer Use 的全部授权摩擦与脆弱性**。这是**明显的架构降级**。

### 2.3 核心问题的回答

> **「内置浏览器」应该是什么？**

**答**：应当拆成**两件事**：
1. **一个由 Curis 友好启动的、用户可见且可随时接管的真实浏览器窗口**（服务于 L2 + L4 + CGAP-04 的用户接管）。
2. **一个仅用于只读预览的嵌入式 WebView**（Tauri `WebviewUrl::External`），服务于"结果呈现"，**不承担自动化职责**。

**Curis 不需要自建浏览器渲染表面。** 它需要的是"**一个能被 Curis 启动、能被 Employee 控制、能被用户接管**的真实浏览器实例"。这三者同时成立的条件是：**该实例由 Curis 自己创建（因此可控制），并以 headed 模式运行（因此可见可接管）**。

---

## 3. 研究结论：主流 AI 产品是怎么做的

（来源：各产品官方文档 / 帮助中心 / 工程说明；二手转述已标注）

| 产品 | 能力名 | 层 | 执行位置 | 模型/视觉 | API | 会话与登录 | 来源性质 |
|---|---|---|---|---|---|---|---|
| **OpenAI ChatGPT Agent** | Agent Mode / Operator | L2+L3 | **OpenAI 托管虚拟浏览器（云 VM）** | CUA 视觉-动作模型 | API 侧**未见公开浏览器工具**；以 MCP 扩展能力为主 | 托管 profile；登录由用户交互完成 | 官方文档 |
| **Anthropic Claude** | Computer Use（**非浏览器专精**，是通用 GUI） | **L2'**（截屏 + 坐标键鼠） | 参考实现为 **Docker + Linux + Xvfb + VNC** | 视觉 + 坐标动作 | 模型 API 暴露工具，**执行环境由调用方提供** | 容器每次可重建 → **会话不天然持久** | 官方文档 + 官方仓库 |
| **Anthropic Claude in Chrome** | 浏览器扩展 | L2+L3 | **用户真实浏览器**（扩展内 `chrome.debugger.attach()`） | DOM + 视觉 | 无独立 API | **直接复用用户真实会话**（SSO/2FA 友好） | 官方文档 |
| **Manus** | 通用 Agent | L2+L3 | 云沙箱 | DOM + 视觉混合 | 无公开 SDK | 云侧 profile | 二手 |
| **豆包 / 元宝 / WorkBuddy** | 手机/桌面助手、内置浏览器 | L2(+L3) | 本地 App / 云端混合 | 视觉为主 | 无公开文档 | **未取得可验证的公开技术文档** | **未验证** |
| **智谱 AutoGLM / GLM-PC** | 手机/电脑操作 | L2' | **端侧 + Android 无障碍服务** | 视觉 | 无 | 依赖系统权限 | 二手 |
| **Browser Use** | 开源 browser agent | **L3** | 本地或 Cloud | **DOM 索引化 + 视觉兜底** | ✅ MIT SDK | Cloud profile sync **有损**（仅 cookie） | 首手 README |
| **Stagehand** | Playwright 之上的 AI 抽象 | **L3** | **本地或 Browserbase** | **a11y 树裁剪** | ✅ MIT SDK | `userDataDir` 本地持久；**`observe()` 凭据不进模型** | 首手 README |
| **Playwright MCP** | 浏览器工具暴露 | **L3（薄）** | 本地 | **a11y 快照** | ✅ Apache-2.0 | `--user-data-dir` / `--extension` | 首手官方文档 |

### 3.1 跨产品复现的四种架构模式

| 模式 | 代表 | 特征 |
|---|---|---|
| **M1. 云 VM + CDP + 视觉模型** | OpenAI Operator、Manus、OpenClaw 类 | 隔离好、可后台；**会话迁移难 + 风控概率高** |
| **M2. 扩展 + 用户真实浏览器** | Claude in Chrome、豆包插件、nanobrowser | **登录态零成本复用**；但**隔离性差**、依赖用户日常环境 |
| **M3. 端侧 + 系统无障碍服务** | AutoGLM、豆包手机 | **属 Computer Use**；需 OS 级 GUI 权限 |
| **M4. 本地 CLI/sidecar + Playwright** | Browser Use CLI、**Curis 的天然形态** | 可控、可见、可接管；适合桌面产品 |

### 3.2 对 Curis 的启示
- **M4 与 Curis 形态天然吻合**（Curis 是本地桌面 App + 本地后端）。
- **M2 的"复用真实会话"很诱人，但代价是隔离性与 CGAP-04 可执行性下降** → 建议仅作显式例外（`CURIS_BROWSER_SESSION_AND_SECURITY_MODEL` §2、`evidence/07` §Q3）。
- **M1 的"后台无人值守"是 C6 优势，但与 CGAP-04 及隐私冲突** → 降级为 Later/Provider。
- **M3 属 CGAP-02**，本轮不展开，但**必须与 Browser 并列为两个 Provider，不可合并**（§9）。

---

## 4. 会话与登录态（CGAP-01 的隐藏难点）

### 4.1 决定性证据：Chrome 136 政策（2025-03-17）

> **"from Chrome 136 ... `--remote-debugging-port` and `--remote-debugging-pipe` ... will no longer be respected if attempting to debug the default Chrome data directory."**
> 官方建议：自动化场景用 **Chrome for Testing**。（`evidence/03`）

Playwright 官方 API 文档亦明确：
> **"Due to recent Chrome policy changes, automating the default Chrome user profile is not supported. ... Create and use a separate directory."**（`evidence/07` §1）

**结论**：
- ❌ "挂到用户日常 Chrome"**已被官方关闭**，不应试图绕过（绕过即等同攻击 App-Bound Encryption 的同一手法）。
- ✅ 正确形态：**Curis 自持专用 profile 目录**（`(business_id, platform_key)` 二维隔离）。
- ✅ 附带安全收益：该 profile 使用**独立加密密钥**，与用户日常浏览数据天然隔离。
- ⚠️ 附带风险：全新 profile 首次登录中文平台，因设备/环境为"新设备"而**更易触发风控**。这是固有代价，须作为**已接受风险**登记。

### 4.2 会话持久化形态

| 形态 | 适用 | 判定 |
|---|---|---|
| `launchPersistentContext(userDataDir)` | 主方案 | ✅ 覆盖 cookies/localStorage/IndexedDB/SW/扩展/站点权限 |
| `storageState` JSON | 迁移/快照 | ⚠️ **官方原文：可直接冒用身份**；且**不持久 sessionStorage** |
| 云侧 profile sync | Cloud | ⚠️ **有损**：原文"transfers cookies, not local storage, IndexedDB, or extensions" |

**并发硬约束**：官方明确 **同一 user data dir 不允许启动多个浏览器实例**（SingletonLock）→ **并发采集无法共享 profile**，必须多 profile 或串行。**这是 Automation Queue 设计的先行约束。**

### 4.3 必须新增的 Curis 裁定项（本轮最重要发现之一）

Curis 既有硬约束："凭据不可能明文落盘"（DB 只存 `credential_ref` + `secret_digest`）。
但**浏览器 profile 内的会话材料本质上是可冒用凭据，且必须落盘**（会话要跨重启存活）。

→ **现有凭据边界未覆盖"浏览器会话材料"这一类新凭据。** 必须新增裁定：
1. 会话材料是否纳入凭据治理（是否引入独立 `profile_ref`）？
2. 落盘形态（Chromium 内建加密 / OS Keychain 包裹 / 仅依赖 FileVault）？
3. 是否允许离开本机（与 Cloud 路径直接相关）？
4. 删除语义（删除 Business 是否连带销毁 profile）？

---

## 5. L2 底座判定：Playwright 是否足以承担？

### 5.1 Playwright 完全解决的
导航 / 点击 / 输入 / 滚动 / 选择、DOM 读取、**`ariaSnapshot()`（含专为 LLM 设计的 `mode:'ai'`）**、截图（页面/整页/元素）、下载、上传（`setInputFiles`）、多标签/弹窗捕获、权限管控（`grantPermissions`，默认拒绝为佳）、headed/headless、**Trace Viewer / video / HAR 三类 Evidence**、持久 profile。
（注：旧 `page.accessibility.snapshot()` 已弃用/移除，应改用 `ariaSnapshot()`。）

### 5.2 Playwright **不**解决的（因此必须由 Curis 补）
1. **登录态获取本身** —— 必须用户在窗口中手工完成。
2. **CAPTCHA / MFA / 风控的停与续** —— 无检测、无 Gate。
3. **Pause / Resume** —— **框架无 HITL 原语**（提供的是可中断异步 API + 可持久化状态，非"人工介入后恢复"机制）。
4. **页面理解与规划** —— 属 L3。
5. **Evidence 的业务语义**（这是哪次经营的哪项指标）—— 属 Curis 自身。
6. **多 Business 隔离策略** —— 机制由 Playwright 提供，**策略必须 Curis 定**。

### 5.3 判定
> **Playwright 是充分且必要的 L2 底座**（Apache-2.0，可闭源集成，无 GNU/SSPL 传染）。
> **但它只覆盖"操作"这一层。Curis 必须在 L1 / L3 / L4 自建或另选。**

### 5.4 5 大集成风险（macOS / Tauri）
1. **Node 驱动依赖** —— Playwright Python 仍依赖 Node 驱动进程（额外运行时）。
2. **浏览器体积** —— Chromium ≈281MB（可规避：`channel:'chrome'` 复用系统 Chrome → 0 增量）。
3. **Chrome 136 政策** —— 必须自持 profile；"复用日常 profile"被官方文档级禁止。
4. **SingletonLock** —— 同 profile 不可双实例 → 并发需多 profile 或串行。
5. **版本钉死** —— Playwright 1.x 绑定特定浏览器修订；**升级 Playwright = 替换底层浏览器**，需纳入回归闸。

---

## 6. CGAP-04 Authentication Stop Gate

### 6.1 框架是否支持 Pause/Resume？—— 逐项核验结论

| 候选 | 原生 HITL / Pause-Resume |
|---|---|
| Playwright | ❌ 无原语 |
| Puppeteer | ❌ 无原语 |
| Playwright MCP | ❌（只暴露动作） |
| browser-use | ❌ |
| Stagehand | ❌ |
| Selenium | ❌ |

→ **CGAP-04 只能由 Curis 自建。** 有利事实：**headed 模式下浏览器窗口本就可被人类同时操作**，人类登录后 Curis 只需轮询状态即可继续 —— 这是最容易实现的 HITL 形态，**不需要任何框架级支持**。

### 6.2 实现要点（详见 `CURIS_BROWSER_SESSION_AND_SECURITY_MODEL`）
- **信号集合**：登出 / 会话失效 / CAPTCHA / MFA / 设备校验 / 风控 / 锁定 —— 可配置、可扩展、**fail-closed**（无法判定即按"需人工"处理）。
- **动作序列**：STOP → 落盘 checkpoint（run_id / step_index / url / title / observed_at / 三元组 / 已完成与待执行步骤 / 已采集数据）→ 创建 Human Gate → 通知用户（**不用飞书**，飞书仅升级事件）。
- **禁止项**：不得在 Gate 后再发任何导航/提交（循环必须 break 而非 continue）；无凭据猜测路径；**不集成任何 captcha-solving（含第三方打码）**；不模拟 OTP；不切账号试探；**不使用 stealth / 指纹伪装**。
- **Resume**：恢复前**重校验三元组一致（防串号）+ 重校验登录态真实有效（不假设"用户说好了"就是好了）**；从 step_index 继续；记录 resume 事件到 Evidence。

### 6.3 必须明确拒绝的反检测工具
patchright（Apache-2.0）、SeleniumBase CDP Mode（MIT）、undetected-chromedriver（**GPL-3.0**）、rebrowser-patches。
**理由（产品原则，非技术）**：CGAP-04 的承诺是"遇风控即停"，集成反检测工具把产品定义为"能绕过风控的东西" —— 一旦平台升级，行为从"停止"变为"隐蔽对抗"，法律与账号风险同步升级（`evidence/05`）。

---

## 7. Local vs Cloud

### 7.1 判据对比（详见 `CURIS_BROWSER_LOCAL_CLOUD_HYBRID_OPTIONS.md`）

| 判据 | Local | Cloud |
|---|---|---|
| 会话材料位置 | ✅ 不出本机 | ⛔ 出境（Provider 数据保留期 7–30 天） |
| **CGAP-04 相容** | ✅ 完全自控 | ⛔ **品类级冲突**（已独立复核） |
| 平台风控概率 | ⚠️ 中 | ⛔ 更高（数据中心 IP + 指纹不一致） |
| 用户可见/可接管 | ✅ 天然满足 | ❌ 依赖 Provider live view |
| 本地资源可及 | ✅ | ❌ |
| 后台长任务 | ⚠️ 依赖 Mac 在线 | ✅ 优势明确 |
| 成本 | ≈$0/月 | ≈$0.9–20/月 |
| 合法集成 | ✅ 全洁净 | ⚠️ 各自 ToS |

### 7.2 成本不构成区分度（重要修正）
本地方案存在**零增量体积路径**（`channel:'chrome'` 复用系统 Chrome）。云端成本 $0.9–20/月。
**两者都在可忽略量级 → 决策必须由 C1–C6 决定，不能由成本决定。**
尤须注意：**browser-use Cloud 的 $0.02/浏览器小时是全场最低，而它恰是最不适配 CGAP-04 的选项**（自带 stealth + CAPTCHA solving）。这个反差本身即为结论。

### 7.3 结论候选
**v1 推荐 Local-first（Option A）**，理由是 **C2（CGAP-04 品类级冲突）为排除性理由**，C1/C4 为强约束，C3 为次要论据 —— **而非因为便宜**。
Cloud 保留为**受严格约束的例外通道（Provider / Later）**，不在 v1 实现。
**明确否定**："敏感平台走 Local、其他走 Cloud"的 Hybrid —— 会导致**同账号双环境登录**，主动升高风控与账号安全风险，并使 CGAP-04 无法统一承诺。

---

## 8. 平台合规（⚠️ 本节定性已被 Reconciliation 修正 → P1 风险登记项，非"可行性前置约束"）

> ⚠️ **RECONCILIATION 修正（第 2 轮）**：上一轮把 **A 类**（抓取公开/第三方内容）的风险结论**未经分析等同于 B 类**（用户读自己后台）。
> 新证据（`evidence/09`）：抖音官方文档**明示支持**"用户授权后可直接在第三方系统查看自己发布的视频统计数据"，并称其为"**唯一官方认证的对外开放的抖音数据**" → **B 类的产品目的被官方承认**；**仅"自动化机制"层为 UNKNOWN**（U1/U3）。
> 本节下述条款原文**仍然有效**，但其**适用范围限于 A 类**；B 类结论以 `CURIS_BROWSER_USE_CASE_RECONCILIATION.md` §9 为准。

（`evidence/05`）

- **抖音《用户服务协议》5.1（官方原文）**：
  > "您不得使用任何插件、外挂、系统或第三方工具对抖音的正常运行进行干扰…**包括但不限于使用任何自动化程序、软件或类似工具接入抖音，收集或处理其中信息、内容。**"
  → 条文覆盖极广，**未区分"爬取他人数据"与"用户读取自己的经营数据"**。
- **小红书**：无公开 API；《用户协议》禁止自动化抓取；风险层级含反爬条款（民事）、刑法第 285 条、PIPL、封号（**且关联设备可能被永久拉黑**）。（第三方调研，需官方复核）
- **抖音电商《【不当获取/使用信息】细则》**（官方公示，2026-05-12 生效）：含"违规使用工具"，处置可至店铺清退。
- **官方数据通道可行性**：微信公众号 `datacube` 系列 = **唯一完全干净的通道**（已认证号即可）；抖音/快手需应用过审且**个人自媒体过审率不高**；B站/小红书/视频号**无官方创作者 API**。

### 结论
「内置浏览器」**不能**被定义为"绕过平台无 API 限制的通用采集器"。必须同时满足：
1. 用户在**自身授权范围内、针对自身账号**的经营数据读取；
2. **默认停在 Draft / Review Gate**，而非端到端无人发布（与既往"微信禁止 AI/脚本替代真人发布"结论一致并加强）；
3. **明确登记平台协议风险为已接受的产品风险**（由总控决策席裁定）；⚠️ Reconciliation 后精确化为"登记**机制层 UNKNOWN（U1/U3）**"；
4. **优先官方 API 通道**（如微信公众号 datacube），浏览器路径是**次选而非首选**。⚠️ Reconciliation 建议**在 API 与 Browser 之间再插入一档"平台官方导出文件 + Curis Import"**（`evidence/09` §5，需 CEO 裁定）。

**新增维度**：既往结论是"**发布**受限"；本轮确认"**读取/采集同样受限**"。
⚠️ **Reconciliation 补充限定**：上述"读取/采集受限"指的是 **A 类**；**B 类（读自己后台）产品目的已被官方承认**，故本条不得再被用作否定 B 类场景的依据。

---

## 9. Browser 与 Computer Use 的关系（不修改 Curis 模型，只给架构候选）

**结论：两者应并列，不应合并。**

| 维度 | Browser Capability | Computer Use Capability |
|---|---|---|
| 操作面 | **Web Surface only** | Desktop App / Finder / 系统对话框 / 专业软件 / 本地文件选择器 / 其它 GUI |
| 技术路径 | CDP 驱动真实浏览器 | 截屏 + 坐标键鼠（+ 视觉接地模型） |
| macOS 权限 | **无需无障碍/录屏** | **需 Accessibility + Screen Recording + Automation** |
| 稳定性 | 高 | 低（授权脆弱、每月复认） |
| 与 CGAP-04 关系 | 可统一实现 | 更难统一（GUI 级验证信号更复杂） |

**架构候选**：**两个并列 Provider，共享同一套 CGAP-04 Stop Gate 与 Evidence 契约**，但**不共享实现**。
**不建议**把 Browser 作为 Computer Use 的一个子能力 —— 会让浏览器自动化继承 GUI 级的权限成本与脆弱性。

---

## 10. Evidence Capture

用户要求：留下足够支撑**经营结果追溯**的 Evidence，**但不要无限保存整个网页**。

| 产物 | Playwright 支持 | 建议 |
|---|---|---|
| Screenshot | ✅（页面/整页/元素） | ✅ 每关键步骤 1 张，**元素级优先**（体积小、指向明确） |
| Page URL | ✅ | ✅ 必存 |
| Page title | ✅ | ✅ 必存 |
| Observed time | ✅（系统时间） | ✅ 必存（**含时区**） |
| Selected date range | Curis 语义 | ✅ 必存（采集所设的日期范围，**这是经营数据的关键维度**） |
| DOM snapshot | ✅ | ⚠️ **按需、单页、限深**；不整站保存 |
| Structured extracted data | ✅（`extract` / 自定义） | ✅ **主产物**（结构化 + schema 校验） |
| Execution trace | ✅ **Trace Viewer / HAR / video** | ✅ 每 run 一份 trace（**可回溯到"点了哪个元素"**） |
| DOM 全文 | — | ❌ **不保存**（既无必要，也触及合规风险面） |

**原则**：**Evidence 以"结构化数据 + 关键截图 + trace"为主，DOM 全文不入库。**
**新增建议**：Evidence 中应**显式记录本次采集走的是"确定性路径"还是"自愈/智能兜底路径"**（见 §11 的确定性优先原则），否则 Learning 会把不可复现的结果当作事实学习。

---

## 11. 二十问逐条回答

| # | 问题 | 回答 |
|---|---|---|
| **1** | Curis 是否真的需要"自己拥有一个内置 Browser Surface"？ | **不需要自建渲染表面。** 需要的是"由 Curis 启动、用户可见可接管的真实浏览器窗口"。嵌入式 WebView 仅保留为**只读预览**，不承担自动化。⚠️ **Reconciliation 命名澄清**："内置浏览器"只是**产品能力名称**，**不蕴含**技术上必须把浏览器渲染器嵌进 Curis 窗口。 |
| **2** | Browser Surface 和 Browser Automation 是否应该分开？ | **必须分开。** 两条独立理由：macOS 上"可控制"与"可嵌入"是互斥集合；两者权限成本差一个量级。⚠️ **Reconciliation 场景澄清**：本能力的真实主场景是 **Authorized Web Console Operation**（读用户自有后台），**不是**抓取公开/第三方内容。 |
| **3** | 推荐什么 Browser Engine？ | **Chromium 系**（Playwright 自带构建，或**系统 Chrome `channel:'chrome'`** 以省 281MB）。**绝不**自建引擎；**不用** Lightpanda（AGPL）。 |
| **4** | 推荐什么 Automation Runtime？ | **Playwright（Apache-2.0）** 为主；Puppeteer 备选；raw CDP 作补充通道。 |
| **5** | Playwright 是否适合作为核心底座？ | **是。** 覆盖"操作"全层且 License 洁净。但只覆盖 L2，"登录态获取 / Stop Gate / Pause-Resume / 页面理解"须 Curis 自建。 |
| **6** | Browser Use / Stagehand / Playwright MCP 各有什么价值？ | **browser-use** = L3 编排（⛔ **首版不采用**：第二编排器 + Cloud 反检测定位）。**Stagehand** = L3 抽象，**本地 `userDataDir` 模式 + `observe()` 凭据不进模型**（MIT + 有 Python SDK）→ ⏸ **Reconciliation 收紧为"后续可选、有准入条件"**。**Playwright MCP** = L3 薄工具层（Apache-2.0），**借鉴其工具集设计**。⚠️ **Reconciliation 定版**：**首版 = 路线 A（纯 Playwright 确定性，不引入 L3 智能层）**。 |
| **7** | Local / Cloud 如何选择？ | **v1：Local-first。** 决定性理由 = CGAP-04 与云浏览器**品类级冲突**；成本不是理由。Cloud 仅作 Later/Provider。**否定**"按平台分流"的 Hybrid。 |
| **8** | 用户已有登录 Session 如何安全复用？ | **不能复用日常 Chrome 默认 profile**（Chrome 136 官方禁止）。改为**Curis 自持专用 profile，用户在其中登录一次**；Curis**不解析**会话内容，只持映射与有效性信号。 |
| **9** | 是否应按 Business/Platform 隔离 Profile？ | **是，(business_id, platform_key) 二维独立。** 理由：平台风控指纹、Curis Business 隔离原则、失效爆炸半径。 |
| **10** | Authentication Stop Gate 如何实现？ | **Curis 自建。** 信号集合可配置 + **fail-closed**；STOP → checkpoint → Human Gate → 通知；Gate 后禁止任何导航/提交；不集成 captcha-solving / 不模拟 OTP / 不用 stealth。 |
| **11** | Browser 任务如何 Pause/Resume？ | **无框架原语。** Curis 编排层持有 plan + step_index + checkpoint；利用 headed 窗口让用户完成登录；恢复前**重校验三元组与登录态**。 |
| **12** | 如何支持自动触发的后台数据采集？ | 属 CGAP-03。**先行约束**：SingletonLock 使**同 profile 不可并发**；headed 与后台可见性存在取舍；Mac 休眠需任务恢复机制。**须在 Capability 立项时一并定义**。 |
| **13** | Evidence 应该保存什么？ | 截图（元素级优先）+ URL + title + 观测时间（含时区）+ 采集日期范围 + 结构化数据 + trace。**不保存 DOM 全文。**新增：**标记路径类型（确定性 / 自愈）**。 |
| **14** | Browser 和 Computer Use 是什么关系？ | **并列，不合并。** 两个 Provider 共享 CGAP-04 与 Evidence 契约，但不共享实现。 |
| **15** | 哪些开源项目值得直接采用？ | **R1**：Playwright、Playwright MCP。**R2**：Stagehand v4 本地模式、Chromium/CEF。**R3**：crawl4ai / ScrapeGraphAI（仅作内容抽取 Provider）、steel-browser（备选）。 |
| **16** | 哪些 License 允许 Curis 商业集成？ | ✅ Playwright/Puppeteer/Playwright MCP（Apache-2.0）、Stagehand/browser-use/cua/OpenAdapt/ScrapeGraphAI/SeleniumBase（MIT）、steel-browser/nanobrowser/Agent-S/crawl4ai（Apache-2.0）、Electron（MIT）、Tauri（Apache-2.0）、**CEF/Chromium（BSD-3-Clause，原文核验）**。⚠️ OmniParser（**CC-BY-4.0，原文核验**；权重条款另计）、WebView2（法律文本待核）、Playwright 的 Firefox/WebKit 构建（MPL-2.0 / LGPL，再分发义务待法务）。⛔ **Skyvern / Firecrawl / Lightpanda（AGPL-3.0）、undetected-chromedriver（GPL-3.0）、browserless（SSPL-1.0 或商业）**。 |
| **17** | 当前最大的技术风险是什么？ | **① `--remote-debugging-port` 成为本机新攻击面**（等价于任意 JS + 任意网络 + 完整 Cookie 访问）→ 必须仅绑 127.0.0.1、随机端口、短生命周期。**② 平台风控误伤**（新 profile = 新设备，首次登录易触发验证）→ 直接决定产品可用性。**③ 平台协议风险** → ⚠️ **Reconciliation 降级为 P1**：**A 类**（抓取公开/第三方内容）明确禁止、Curis 不采用；**B 类**（读自有后台）**产品目的已被官方承认**（`evidence/09`），仅"自动化机制"层为 UNKNOWN，且存在**官方导出 + Import**这条更干净路径。 |
| **18** | 最小可实现版本是什么？ | ⚠️ **Reconciliation 已重写** → 见 `CURIS_BROWSER_USE_CASE_RECONCILIATION.md` §8（14 步流程）。**要点**：目标明确为 **Authorized Web Console Operation**；平台首选改为"**用户实际拥有后台的平台**"（个人主体对官方 API 不可得，不构成 MVP 主体）；**Agent 层 = 路线 A（无 L3）**；**第 11–14 步（制造 Session 失效 → 必须 STOP → 重新登录 → Resume）为首要强制验收项**。原要点（单平台 / 单 Business / 确定性路径 / headed / 手工登录 / 遇验证即停 / 无 Cloud 无并发）**仍全部有效**。 |
| **19** | 后续 Computer Use 研究还缺什么？ | 缺：①macOS 上合成键鼠与截屏的**实际授权成功率与失效频率实测**；②**视觉接地模型选型**（OmniParser 的 CC-BY-4.0 + 权重条款问题未解）；③cua / Lume 的 **macOS 虚拟化在 Apple Silicon 上的资源与授权代价**；④**GUI 级 CGAP-04 的检测信号定义**（比浏览器难得多）；⑤macOS 版本升级对 TCC 授权的**回归影响**；⑥OpenAdapt "VERIFIED 才报告"机制能否**迁移为 Computer Use 的 Evidence 契约**。 |
| **20** | 是否已足够登记为正式 Capability Gap 解决方案候选？ | **更接近了，但仍未足够。** 若"内置浏览器" = "**未授权**采集器" → **不应登记**。应登记为：**「Authorized Web Console Operation — AI Employee 对用户本人已授权 Web 后台的操作能力」**。⚠️ **Reconciliation 更新前置条件**：① **U1/U3 法务或官方确认**；② 会话材料凭据治理裁定；③ **"官方导出 vs Browser"优先级的 CEO 裁定**；④ MVP（RECONCILIATION §8）验收通过；⑤ 命名变更走文档流程。**当前状态：RECONCILED — READY FOR CEO REVIEW，尚未登记。** |

---

## 12. 本报告的已知边界与未验证项

| 项 | 状态 |
|---|---|
| **未执行 clone 与本地运行** | 全部结论基于 README / 官方文档 / LICENSE 原文 / GitHub API；**无运行时实测** |
| **未做性能实测**（内存/CPU/耗时） | 均为结构性判断 |
| **Steel / Browserless / Cloudflare / AWS / Kernel / Anchor / Hyperbrowser 当期报价** | `△转述`，**未独立复核**（`steel.dev/pricing` 实际返回首页） |
| **各云 Provider 的规避类能力能否按项目关闭** | **未验证**（这是 Cloud 能否成立的关键前提） |
| **browser-use 的接地实现细节** | 未读源码 |
| **browser-use `from_system_chrome()` 与 Chrome 136 的兼容性** | **未验证**，存在冲突疑点 |
| **Playwright MCP 完整工具名清单** | 本轮仅取得部分（`--caps` 分组） |
| **中文平台对"新 profile 首次登录"的风控触发阈值** | 只能定性，**不可量化** |
| **小红书/快手条款** | 第三方转述，**需官方复核** |
| **MPL/LGPL 再分发义务、编解码器专利、OmniParser 权重条款** | **未做法务结论** |

---

## 13. 交付状态

```
BUILT-IN BROWSER CAPABILITY RESEARCH COMPLETE — READY FOR CEO REVIEW
（第 2 轮 Reconciliation 后：）
BROWSER CAPABILITY USE CASE RECONCILED — READY FOR CEO REVIEW
```

- 未修改任何 Curis Authority / Runtime / Frontend / Backend / 视觉 / Workspace / HTML Exploration。
- 未开发 Browser。未 commit / push。
- 全部产物为 RESEARCH / EVIDENCE 类，**不覆盖**任何 Current Authority。
- 本目录**不在** `docs/` 下，符合"不创建第二份 Current Blueprint"的纪律；如需进入正式生产线，应走 Pointer / CURRENT_STATE / CHANGE_LOG 流程。
- **第 2 轮变更范围**：仅纠正 Problem Definition / Primary Use Case / Risk Interpretation / MVP；**技术选型未变**。详见 `CURIS_BROWSER_USE_CASE_RECONCILIATION.md`。
- **第 3 轮（Addendum）变更范围**：新增候选核验 + **细化 R7 适用范围**；**无一条既有结论被推翻**。详见 `CURIS_BROWSER_ADDENDUM_2026-09-20_BROWSERSKILL_AND_JEV.md`、`evidence/10`。

```
BROWSER CAPABILITY ADDENDUM (BROWSERSKILL + JEV) COMPLETE — READY FOR CEO REVIEW
```
