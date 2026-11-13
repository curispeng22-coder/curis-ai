# Evidence 07 — Playwright 官方硬约束与"已存在浏览器"三条接入路径

Authority Class: EVIDENCE
Collected: 2026-09-18
Primary sources:
- `https://playwright.dev/docs/api/class-browsertype`
- `https://playwright.dev/docs/browsers`
- `https://playwright.dev/mcp/configuration/browser-extension`
- `https://playwright.dev/docs/connect`
- `https://github.com/microsoft/playwright-mcp`

---

## 1. 官方对"自动化默认 Chrome profile"的明确否定（决定性）

Playwright 官方 API 文档（`BrowserType`）原文警告：

> **"Due to recent Chrome policy changes, automating the default Chrome user profile is not supported. Pointing `userDataDir` to Chrome's main 'User Data' directory ... may result in pages not loading or the browser exiting. Create and use a separate directory."**

根因即 `evidence/03` 所载 Chrome 136 政策。

→ **本证据把 E1 从"博客政策"升级为"Playwright 官方文档级硬约束"**：
*Curis 不能、也不应试图自动化用户日常 Chrome 的默认 profile。*

同一文档另一条被低估的约束：

> **"browsers do not allow launching multiple instances with the same User Data Directory"**

→ profile 目录被 **SingletonLock** 保护：**同一 profile 同一时刻只能有一个浏览器实例**。
→ 架构含义：**并发采集无法共享 profile**；若要并发，必须多 profile 或串行。这是 Automation Queue 设计的先行约束。

---

## 2. 接入"已存在浏览器"的三条路径（官方支持，语义各不相同）

| # | 路径 | 机制 | 复用的是"用户的什么" | 前置条件 | 隔离性 | Curis 适配 |
|---|---|---|---|---|---|---|
| **P1** | **Curis 自启 + 专用 user-data-dir** | `launchPersistentContext(dir, {headless:false, channel:'chrome'})` | 该目录内**用户在此 profile 中登录过**的会话 | 无 | **高**（每 Business 一目录） | ✅ **主方案** |
| **P2** | **Extension 附加** | playwright-mcp `--extension`，经浏览器扩展 `chrome.debugger.attach()` 接入用户**正在使用**的 Chrome | **用户真实日常会话**：已登录状态、Cookie、**已安装扩展**、已开启标签页 | 需安装 Playwright 浏览器扩展；Chrome 需在运行 | 低（与用户日常浏览同进程） | ⚠️ **可选逃生通道** |
| **P3** | **CDP 附加** | `chromium.connectOverCDP('http://localhost:9222')` | 由**外部（用户或脚本）以 `--remote-debugging-port` + 非默认 user-data-dir 启动**的 Chrome | 目标浏览器须已带调试端口启动 | 中 | ⚠️ 技术路径，但体验依赖用户操作 |

**官方对 P2 的定位（原文语义）**：playwright-mcp 文档将该模式列为适用于 **SSO / 2FA 场景、依赖扩展的页面、以及已打开标签页**——即**当"重新登录一次"成本极高时**才使用。

**官方对 P3 的重要警告**（`browserType.connect_over_cdp` 中文官方文档）：
> "通过 Chrome DevTools 协议连接**仅支持基于 Chromium 的浏览器**。"
> "此连接的**保真度明显低于**通过 `browser_type.connect()` 建立的 Playwright 协议连接。"
> **警告**："Playwright 维护了一份用于启动浏览器的精心挑选的参数列表。如果您在没有 Playwright 的情况下启动浏览器且未传递完全相同的参数，在连接到浏览器时，**Playwright 的某些功能可能会失效**。"

→ P3 的风险是**功能静默降级**，而非报错。这对"证据可信度"是隐患。

---

## 3. 由此形成的架构建议（研究假设）

```
默认路径   P1：Curis 托管 profile（隔离、可控、可审计、无需扩展）
例外通道   P2：用户显式选择"连接我当前的浏览器"，仅用于 SSO/2FA 强绑定平台
不推荐     P3：作为主路径（功能静默降级 + 依赖用户手动带端口启动）
```

**关键取舍**：P2 复用"真实会话"的代价是把 Curis 与用户的**日常浏览环境混同**，直接违背 §3.3 的 Profile 隔离原则，并使 CGAP-04 的"停止并隔离"难以实现（无法界定"哪个标签页属于 Curis 的任务"）。
→ 建议：**P2 默认关闭**，作为用户显式授权的例外，且**必须在 UI 中明示"Curis 将可访问你当前浏览器中的页面"**。

---

## 4. 能力与体积（官方数据）

| 项 | 数据 | 来源 |
|---|---|---|
| 浏览器二进制体积（macOS） | Chromium ≈ **281MB**、Firefox ≈ **187MB**、WebKit ≈ **180MB** | `playwright.dev/docs/browsers` |
| 缓存位置（macOS） | `~/Library/Caches/ms-playwright` | 同上 |
| 覆盖变量 | `PLAYWRIGHT_BROWSERS_PATH`（`=0` 则装入 `node_modules`，用于 hermetic 打包） | 同上 |
| 驱动依赖 | 三语言绑定（JS/Python/.NET/**Java**）**底层均依赖一个 Node 驱动进程** | 官方架构 |

**对 Curis 的直接含义**：Curis 后端为 Python，但 **Playwright Python 仍需 Node 驱动**——即"引入 Playwright"= 同时引入 Node 运行时 + 约 281MB（仅 Chromium）浏览器二进制。这是**分发体积上的实质成本**，也是"是否值得拥有内置浏览器"必须回答的量化项。

## 5. 二进制许可（官方未展开，需法务复核）
- Chromium 构建：BSD/Apache 类（源码侧已核验为 BSD-3-Clause，见 `evidence/02`）
- Firefox 构建：**MPL-2.0**
- WebKit 构建：**LGPL / BSD**
→ MPL/LGPL 的**再分发义务**（源码可得性、动态链接边界、编解码器专利）官方文档**未展开**。**标记为待法务复核**。

## 6. 本证据纠正的一处平行研究误差
并行研究线曾标注 `microsoft/playwright-mcp` 许可"疑似 MIT，未确认"。
**本目录已通过 GitHub API + LICENSE 原文双重核验为 `Apache-2.0`**（见 `evidence/02`）。以核验结果为准。
