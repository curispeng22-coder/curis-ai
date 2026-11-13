# Evidence 08 — browser-use / Stagehand 首手源码级核验

Authority Class: EVIDENCE
Collected: 2026-09-18
Method: 直接抓取 `raw.githubusercontent.com/<owner>/<repo>/main/README.md` 原文（非二手转述、非博客）

---

## A. browser-use/browser-use（MIT, 115,108 stars, pushed 2026-09-15）

### A.1 产品形态（README 原文）
- 三条路径：
  1. **Fully Hosted Cloud** — 提交任务给托管 Agent API（agent + browser + infra 均由厂商运行）
  2. **CLI（Browser Harness）** — 给已有编码 agent（Claude Code / Codex / Hermes / OpenClaw / Cursor 等）加浏览器能力
  3. **Python Library** — 在自有代码里本地运行开源 agent；「connect to a **local or cloud** browser」
- 语言：Python（**>= 3.11**）与 TypeScript
- 作者：Magnus Müller、Gregor Žunič（"Made with ❤️ in Zurich and San Francisco"）

### A.2 License（原文）
> "The Python library is free and **MIT-licensed** (LICENSE). Model inference and hosted browsers are separate: API providers ... and Browser Use Cloud charge for usage."
> "This open-source library is licensed under the **MIT License**. For Browser Use services & data policy, see our Terms of Service and Privacy Policy."

→ **代码 MIT 可闭源集成；但 Cloud 服务受另行的 ToS / 隐私政策约束**（两套条款，勿混淆）。

### A.3 Cloud 定位与反检测（原文，**决定 CGAP-04 适配性**）
> "Browser Use is the open-source browser agent (Python and TypeScript), a **$0.02 per browser-hour** cloud browser with **stealth, CAPTCHA solving and residential proxies**, and a hosted agent API."

> "**Browser Use Cloud** provides **stealth browsers and proxies designed to reduce bot detection and CAPTCHA challenges**. ... Results depend on the site and challenge; no browser configuration guarantees that every CAPTCHA can be avoided or solved."

→ **Cloud 路径与 Curis CGAP-04（遇验证即停、绝不规避）直接冲突。**

### A.4 会话迁移的**损失性**（原文，关键）
> "**Profile sync transfers cookies, not local storage, IndexedDB, or extensions. Some sites may require you to sign in again.**"

→ 云侧 profile 同步是**有损的**：localStorage / IndexedDB / 扩展均不迁移。对现代 SPA 后台（登录态常驻 localStorage）而言，**迁移后大概率需要重新登录**。这直接削弱 Cloud 的"登录态复用"价值。

### A.5 本机浏览器复用（原文）
> "**Local browser:** Use `Browser.from_system_chrome()` to **reuse a Chrome profile**. See the real-browser guide and example."

→ ⚠️ **与 `evidence/03` 存在潜在冲突**：Chrome 136 起默认 profile 上的调试端口被禁用。该方法**是否通过复制 profile / 指定非默认目录规避**，本轮**未读源码验证**。**标记为待核**（不得据此假设"可复用日常 Chrome"）。

### A.6 相邻项目（README 表格）
| 仓库 | 用途 | 归属层 |
|---|---|---|
| Browser Harness / Harness JS | 给自己的 agent 浏览器控制权（CLI） | L3 接入 |
| Cloud SDK | 集成 Browser Use Cloud | L5 |
| **macOS Harness** | "Give your agent control of **Mac apps**, browsers, and files" | **CGAP-02 Computer Use** |
| Benchmark | 浏览器任务基准 | 评测 |
| video-use | 视频编辑 | 无关 |

---

## B. browserbase/stagehand（MIT, 24,332 stars, pushed 2026-09-18）

### B.1 定位（原文）
> "**Playwright was built for testing. Stagehand is built for agents**, in TypeScript, Python, and Go."

→ 明确是 **L2 之上的 L3 抽象**，非 L2 替代。

### B.2 License（原文）
> "Licensed under the **MIT License**. Copyright 2026 Browserbase, Inc. **"Stagehand" is a trademark of Browserbase, Inc.**"

→ MIT 允许闭源集成；**但 "Stagehand" 是商标** → 若在 UI/文档中引用其名，需注意商标使用规范（不构成集成障碍，但需登记）。

### B.3 **本地运行模式（对本研究最关键）**
TypeScript：
```typescript
import { localBrowser, Stagehand } from "@browserbasehq/stagehand";
// Cookies persist in ./browser-data, so the next run starts already signed in
const browser = await localBrowser.launch({ userDataDir: "./browser-data" });
```
Python：
```python
from stagehand import Stagehand, local_browser
browser = await local_browser.launch(user_data_dir="./browser-data")
```
> "**Local runs need Chrome installed.**"

→ **不强制 Browserbase**；`userDataDir` 持久化 cookie 正是 Curis 需要的"专用 profile"形态；且有 **Python SDK**（匹配 Curis 后端）。

### B.4 **凭据边界设计（对 Curis 极高价值，原文）**
```typescript
// observe() returns real selectors, so credentials never reach the model
const { data: email } = await stagehand.observe("find the email input");
await page.locator(email[0].selector).fill(process.env.APP_EMAIL!);
```
> "**observe() returns real selectors, so credentials never reach the model**"

→ 官方**主动设计了凭据隔离**：LLM 只负责"找到输入框"，**真实凭据由 Playwright locator 直接填入，不进入模型上下文**。
→ 这**与 Curis 既有凭据边界原则天然同向**（Curis 不允许密钥/凭据进入不可控通道）。**本研究中唯一一个"默认行为就符合 Curis 安全原则"的 L3 候选。**

### B.5 能力清单（原文表格）
| 能力 | 原文 |
|---|---|
| 熟悉 API | "The Playwright-style methods you and your agents already know: `goto`, `click`, `locator`, `screenshot`" |
| Token 效率 | "**Hybrid accessibility-tree trimming** gives agents exactly the page context they need and nothing more" |
| 低延迟 | "Stagehand runs **as an extension next to the browser**, cutting round-trip latency on every action" |
| 自愈 | "`act`, `observe`, and `extract` **refresh how an action happens when the site changes** underneath it" |
| 为 agent 而生 | "**WebMCP**, clipboard support, batch commands, **deep locators for nested iframes and closed Shadow DOMs**, OTel traces" |

### B.6 Browserbase 侧能力
```typescript
const browser = await browserbase.launch({ apiKey: ... });
const stagehand = await Stagehand.create({ browser, cache: true }); // 服务端缓存，不花 token
```
> "Verified mode, residential proxies, persistent contexts, and session recordings come with it."
> 托管 MCP：`https://mcp.browserbase.com/mcp`（暴露 `navigate` / `act` / `observe` / `extract`）

→ ⚠️ **`cache: true` 的语境指向 Browserbase 服务端**；**本地模式是否有等价缓存未确认**。
→ ⚠️ **勿与已归档的 `browserbase/mcp-server-browserbase` 混淆**：托管 MCP 是新产品，旧仓库已 ARCHIVED（`evidence/02`）。

### B.7 生态集成（原文）
> "Integrations: **CrewAI, Mastra, Deep Agents, Vercel AI SDK, Claude Code, Codex**"
→ 说明其被设计为**可被上层编排器调用**——与 Curis"Employee 作为编排者"的定位**相容**（不像 browser-use 自带编排器那样与 Curis 冲突）。

---

## C. 由本证据得出的**排除性结论**

| 项目 | 排除/采纳理由（基于原文，非推测） |
|---|---|
| browser-use **Cloud** | 原文自述含 "stealth, CAPTCHA solving, residential proxies" → **与 CGAP-04 冲突** |
| browser-use **整体（含本地）** | 自带 Agent 编排器 → 会在 Curis 内**出现第二个规划者**，与 Curis 四原则③④冲突 |
| Stagehand **本地模式** | 原文证实无需 Browserbase + 有 Python SDK + `observe()` 凭据隔离 → **唯一正面候选** |
| Stagehand **Browserbase 模式** | 与 Curis Local-first 定位及 CGAP-04 复核结果冲突 → **不作为默认** |
| Playwright MCP | Apache-2.0 + a11y 接地 + 丰富配置项 → **借鉴其工具集设计** |
