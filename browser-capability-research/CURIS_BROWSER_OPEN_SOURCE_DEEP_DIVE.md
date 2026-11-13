# CURIS BROWSER OPEN SOURCE DEEP DIVE

Authority Class: RESEARCH
Status: Draft（已过 Reconciliation 轮 + **Addendum 轮**）
Collected: 2026-09-18（原始）／2026-09-18 **Reconciliation 轮**／**2026-09-20 Addendum 轮**
Evidence: `evidence/01`（GitHub API 原始数据）、`evidence/02`（License 原文）、`evidence/07`、`evidence/08`、**`evidence/09`、`evidence/10`**

> **Stars 仅作生态活跃度辅助，不作为质量结论**（用户明确要求）。
> **License 一律以 `evidence/02` 的原文核验为准**，GitHub API 的 `spdx_id` 仅作交叉验证。
> **方法降级声明**：受本机沙箱限制，本轮**未执行 `git clone` 与本地运行**；改为 **GitHub REST API + `raw.githubusercontent.com` 原文抓取**完成 License / 活跃度 / 依赖 / API 面的同等核验。**"未实际运行"是本文件全部结论的已知边界。**

> ⚠️ **RECONCILIATION 声明（第 2 轮）**：本文件的 **License 分类（§3）、维护状态（§2）、macOS/ARM 兼容性（§4）、安全模型（§5）全部不变**。
> 仅 **§6 的采用形态调整**：**首版 L3 = 路线 A（纯 Playwright 确定性）**；`Stagehand` 由"R2 封装为 L3 加速器"收紧为 **"后续可选、须满足准入条件"**（RECONCILIATION §7.4）；`browser-use 整体不采用` 的理由补充"**第二编排者**"。
> 详见 `CURIS_BROWSER_USE_CASE_RECONCILIATION.md` §7、§14。

> ⚠️ **ADDENDUM 声明（第 3 轮，2026-09-20）**：新增 **§6.1 补录** —— `Tencent/BrowserSkill`（MIT，**登记为接入路径 P2 参考实现，v1 不启用**）、`browser-use/browser-harness`（观察项）、`browser-use/jev-ultrafast`（**不采用**）。**§2–§5、§7 全部结论不变**。详见 `CURIS_BROWSER_ADDENDUM_2026-09-20_BROWSERSKILL_AND_JEV.md`、`evidence/10`。

---

## 1. 逐项评估矩阵（对应用户第 8 节全部判据）

图例：✅ 支持 / ⚠️ 部分或有限 / ❌ 不支持 / `?` 未核验

| 项目 | License | 主语言 | 依赖 Chromium? | 依赖 Playwright? | macOS | ARM | Electron/Tauri 兼容 | 会话持久 | Profile 隔离 | 截图 | DOM 抽取 | 上传/下载 | Headed | Headless | Pause/Resume | 多标签 | 多会话 | MCP | API/SDK | 资源占用 | 安全模型 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Playwright** | Apache-2.0 | TS（多语言绑定） | ✅ 自带构建 | — | ✅ | ✅ | ✅（需 Node 驱动 + asar unpack 处理） | ✅ `launchPersistentContext` | ✅ 多 context / 多 profile | ✅ | ✅ + `ariaSnapshot()` | ✅ | ✅ | ✅ | ❌ **无原语** | ✅ | ✅ | 官方 `playwright-mcp` | ✅ 4 语言 | 中（每 context 独立进程） | 强（权限/隔离模型） |
| **Puppeteer** | Apache-2.0 | TS | ✅ Chrome / CfT | — | ✅ | ✅ | ⚠️ | ✅ `userDataDir` | ⚠️ 弱于 Playwright | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ⚠️ | 社区 | ✅ JS/TS 为主 | 中 | 中 |
| **raw CDP** | MIT 类 | 多语言 | ✅ Chromium only | — | ✅ | ✅ | ✅ | 需自管 | 需自管 | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ⚠️ | 有 | ✅ | 低 | ⚠️ 调试端口即攻击面 |
| **browser-use** | **MIT** | Python (>3.11) / TS | 经 L2 | ⚠️（未逐行核验） | ✅ | ✅ | ⚠️ | ✅ `from_system_chrome()` ⚠️待核 Chrome136 | ⚠️ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ⚠️ | ✅ | ✅ | 中高（含 LLM 调用） | ⚠️ Cloud 含 stealth → 与 CGAP-04 冲突 |
| **Stagehand** | **MIT** | TS / **Python** / Go | 经 L2 | ✅（Playwright 风格 API） | ✅ | ✅ | ⚠️ | ✅ **`localBrowser.launch({userDataDir})`** | ✅（每 userDataDir） | ✅ | ✅（`extract` + schema） | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅（托管 MCP） | ✅ 3 语言 | 中（a11y 裁剪降低 token） | ✅ **`observe()` 凭据不进模型** |
| **Playwright MCP** | Apache-2.0 | TS | 经 Playwright | ✅ | ✅ | ✅ | ✅ | ✅ `--user-data-dir` | ✅ `--isolated` | ✅ | ✅ a11y 快照 | ✅ | ✅ | ✅ | ❌ | ✅ | ⚠️ | ✅ **本身即 MCP** | ✅ | 中 | 中（`--extension` 模式降低隔离性） |
| **steel-browser** | Apache-2.0 | TS | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ | ✅ | 高（服务形态） | ⚠️ 云侧含 captcha/指纹能力 |
| **nanobrowser** | Apache-2.0 | TS | 经浏览器扩展 | ✅ | ✅ | ✅ | ❌ 形态不符 | ✅（复用真实浏览器） | ❌ | ✅ | ✅ | ⚠️ | ✅ | ❌ | ❌ | ✅ | ⚠️ | ❌ | ✅ | 低 | ⚠️ 扩展形态 |
| **Agent-S** | Apache-2.0 | Python | ❌（GUI 级） | ❌ | ⚠️ | ⚠️ | ❌ | n/a | n/a | ✅ | ❌ | ⚠️ | ✅ | ❌ | ⚠️ | n/a | ❌ | ❌ | ✅ | 高 | ⚠️ GUI 控制 |
| **cua** | MIT | 多 | ❌（OS 级） | ❌ | ✅（Lume 虚拟化） | ✅ Apple Silicon | ❌ | n/a | ✅（VM 级） | ✅ | ❌ | ⚠️ | ✅ | ✅ | ⚠️ | n/a | ✅ | ❌ | ✅ | 很高（虚拟机） | 强（VM 隔离） |
| **OmniParser** | CC-BY-4.0（权重条款另计） | Python | ❌（感知模型） | ❌ | ⚠️ | ⚠️ | ❌ | n/a | n/a | ✅（输入） | ✅（输出结构化元素） | ❌ | n/a | n/a | ❌ | n/a | ❌ | ❌ | ✅ | 高（模型推理） | ⚠️ 权重条款待核 |
| **OpenAdapt** | MIT | Python | ❌（GUI 记录重放） | ❌ | ✅ | ⚠️ | ❌ | n/a | n/a | ✅ | ⚠️ | ❌ | ✅ | ❌ | ⚠️ | n/a | ❌ | ❌ | ✅ | 中 | ⚠️ 键鼠录制 |
| **crawl4ai** | Apache-2.0 | Python | ✅（可选） | ✅（可选） | ✅ | ✅ | ✅ | ⚠️ | ❌ | ⚠️ | ✅ | ❌ | ⚠️ | ✅ | ❌ | ✅ | ❌ | ✅ | ✅ | 中高 | 中（**服务端抓取层，非浏览器自动化**） |
| **ScrapeGraphAI** | MIT | Python | ✅（可选） | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ⚠️ | ✅ | ❌ | ⚠️ | ✅ | ❌ | ✅ | ❌ | ❌ | ✅ | 中高 | 同上 |
| **Skyvern** | **AGPL-3.0** ⛔ | Python | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ⚠️ | ✅ | ✅ | 中高 | 中 |
| **Firecrawl** | **AGPL-3.0** ⛔ | TS | ✅ | ✅ | ✅ | ✅ | ⚠️ | ⚠️ | ❌ | ⚠️ | ✅ | ❌ | ⚠️ | ✅ | ❌ | ✅ | ❌ | ✅ | ✅ | 中高 | 中 |
| **Lightpanda** | **AGPL-3.0** ⛔ | Zig | ✅ 自研引擎 | ❌ | ✅ | ✅ | ⚠️ | ⚠️ | ⚠️ | ⚠️（无渲染，快照） | ✅ | ⚠️ | ⚠️ | ✅ | ❌ | ⚠️ | ❌ | ✅ | ✅ | **极低** | ⚠️ |
| **browserless** | **SSPL-1.0 或商业** ⛔ | TS | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ | ✅ | 高 | 中 |
| **patchright** | Apache-2.0 | TS | ✅ | ✅（fork） | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ | ✅ | 中 | ⛔ **反检测，与 CGAP-04 冲突** |
| **SeleniumBase** | MIT | Python | ✅ | ❌ | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ⚠️ | ✅ | ✅ | 中 | ⛔ CDP Mode 卖点为绕过检测 |
| **undetected-chromedriver** | **GPL-3.0** ⛔ | Python | ✅ | ❌ | ✅ | ✅ | ⚠️ | ✅ | ⚠️ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ⚠️ | ❌ | ✅ | 中 | ⛔ 双不合（License + 反检测） |

---

## 2. 依赖与维护状态（GitHub API 原始数据，`evidence/01`）

| 项目 | Stars | Archived | 最近推送 | 备注 |
|---|---|---|---|---|
| Playwright | 96,315 | false | 2026-09-18 | 高频维护 |
| Playwright MCP | 37,242 | false | 2026-09-17 | 2025-03 建库，增长极快 |
| Puppeteer | 95,590 | false | 2026-09-18 | 高频维护 |
| browser-use | 115,108 | false | 2026-09-15 | 高频维护 |
| Stagehand | 24,332 | false | 2026-09-18 | 高频维护 |
| steel-browser | 7,661 | false | 2026-09-16 | 活跃 |
| cua | 23,071 | false | 2026-09-18 | 活跃 |
| Agent-S | 12,318 | false | 2026-09-05 | 活跃 |
| OmniParser | 25,404 | false | **2026-07-20** | ⚠️ 约 2 个月未推送（微软研究项目，节奏本就慢） |
| OpenAdapt | 1,729 | false | 2026-09-14 | 活跃 |
| SeleniumBase | 13,025 | false | 2026-09-18 | 活跃 |
| patchright | 4,623 | false | 2026-09-13 | 活跃 |
| **undetected-chromedriver** | 12,843 | false | **2025-07-05** | ⚠️ **约 14 个月未推送**（事实上的停滞） |
| **browserbase/mcp-server-browserbase** | 3,411 | **true** | 2026-07-20 | ⛔ **已归档** |
| CEF | 4,788 | false | 2026-09-17 | 活跃 |
| Tauri | 111,161 | false | 2026-09-18 | 活跃 |
| Electron | 123,135 | false | 2026-09-18 | 活跃 |

### 2.1 值得注意的三个维护信号
1. **`browserbase/mcp-server-browserbase` 已归档**（2026-07-20），且 Browserbase 现推**托管 MCP**（`mcp.browserbase.com`）。→ **任何引用旧仓库的方案应视为已废弃**。
2. **`undetected-chromedriver` 停滞约 14 个月**。→ 即便不考虑 License 与原则问题，其**工程可用性也已存疑**。
3. **OmniParser 约 2 个月未推送**（相对其历史节奏属正常，但需在采用前确认活跃度预期）。

---

## 3. License 分类（决定**能否合法集成与分发**）

### ✅ 可闭源集成与分发
Playwright（Apache-2.0）、Playwright MCP（Apache-2.0）、Puppeteer（Apache-2.0）、Stagehand（MIT）、browser-use（MIT）、cua（MIT）、nanobrowser（Apache-2.0）、steel-browser（Apache-2.0）、SeleniumBase（MIT）、patchright（Apache-2.0）、Agent-S（Apache-2.0）、OpenAdapt（MIT）、crawl4ai（Apache-2.0）、ScrapeGraphAI（MIT）、Electron（MIT）、Tauri（Apache-2.0）、CEF（BSD-3-Clause，原文核验）、Chromium（BSD-3-Clause，原文核验）

### ⚠️ 需附义务 / 需法务复核
- **OmniParser（CC-BY-4.0）**：署名义务；**且模型权重通常有独立条款，与代码许可不同** → 必须单独核验。
- **Microsoft WebView2**：技术分发指南允许随应用打包，但**法律许可文本未取得** → 标记待核（对 macOS v1 影响有限）。
- **Playwright 自带浏览器构建**：Chromium（BSD 类）、Firefox（**MPL-2.0**）、WebKit（**LGPL/BSD**）→ **MPL/LGPL 的再分发义务与编解码器专利需法务复核**；官方文档未展开。
- **screenpipe**：自定义 `LICENSE.md`，非 SPDX 标准 → 未解读。

### ⛔ 闭源分发受阻（不可作集成组件）
| 项目 | License | 影响 |
|---|---|---|
| **Skyvern** | AGPL-3.0 | 网络服务条款传染 |
| **Firecrawl** | AGPL-3.0 | 同上 |
| **Lightpanda** | AGPL-3.0 | 同上（自托管亦受阻） |
| **undetected-chromedriver** | GPL-3.0 | 传染性强 |
| **browserless** | SSPL-1.0 或商业许可 | **闭源商业使用须购商业许可**（原文核验） |

> **重要区分**：⛔ 仅针对**"作为代码/组件集成进 Curis 并分发"**。
> 若仅作为**外部 Provider（Curis 通过 API 调用其托管服务）**，则不适用同一分析——但那要受 Provider 自身 ToS 约束（例如 Browserless 需购许可、AGPL 项目托管服务的条款另计）。**"调用服务"与"集成代码"是两个不同的法律问题，不可混为一谈。**

---

## 4. macOS / ARM / Electron / Tauri 兼容性专项

| 项 | 核验结果 |
|---|---|
| **Playwright 浏览器二进制的 macOS ARM 支持** | ✅ 官方 `playwright install` 提供 arm64 构建（本机为 Apple Silicon，`~/Library/Caches/ms-playwright` 为官方缓存路径） |
| **体积（macOS）** | Chromium ≈281MB / Firefox ≈187MB / WebKit ≈180MB（`evidence/07` §4） |
| **Playwright Python 的运行时依赖** | ⚠️ **仍依赖 Node 驱动进程**（官方架构），对"纯 Python 后端"是额外依赖 |
| **Tauri 集成** | ⚠️ Curis 桌面壳为 Tauri（Rust + 系统 WebView）→ **Playwright 只能作为 sidecar 子进程运行**，无法嵌入 Tauri 的 WebView；两者是**进程级并行**关系 |
| **Electron 集成** | ⚠️ 已知需处理 `asar` unpack、`PLAYWRIGHT_BROWSERS_PATH`；本项目**不需**（Curis 非 Electron） |
| **CEF 嵌入 macOS** | ⚠️ 可行但工程成本高（C++ 桥、签名、notarization、体积）；v1 **不建议** |
| **Tauri 加载外部 URL** | ✅ Tauri 2 支持 `WebviewUrl::External` 与多窗口；多 WebView 单窗口（`window.add_child`）**官方标注 unstable** |

---

## 5. 安全模型对比（决定哪个候选能承载 CGAP-04）

| 候选 | 安全模型要点 | 与 CGAP-04 的相容性 |
|---|---|---|
| **Playwright** | 多 context 隔离；显式 `grantPermissions`（默认拒绝）；`--remote-debugging-port` 为最大攻击面 | ✅ **相容**（Stop Gate 由上层实现） |
| **Stagehand（本地）** | `observe()` **凭据不进模型**；a11y 裁剪减少上下文暴露 | ✅ **相容度最好** |
| **Playwright MCP** | `--isolated` 提供每会话隔离；但 **`--extension` 模式复用用户真实浏览器 → 隔离性下降** | ⚠️ 相容，但 `--extension` 模式须谨慎 |
| **browser-use（本地）** | 自带编排器；Cloud 侧 stealth | ⚠️ 本地可用，Cloud ⛔ |
| **browser-use Cloud / Browserbase / Steel / Anchor / Hyperbrowser** | **反检测/自动登录为卖点** | ⛔ **不相容** |
| **patchright / SeleniumBase CDP / undetected-chromedriver** | 专为规避检测设计 | ⛔ **直接冲突** |
| **cua** | VM 级隔离（macOS 虚拟化） | ✅ 强隔离，但**属 Computer Use 层** |

---

## 6. 可直接采用的候选（结论候选，非裁定）

### 6.0 补录：本轮后段核验的新增候选

| 项目 | License | Stars | Archived | 最近推送 | 语言 | 判定 |
|---|---|---|---|---|---|---|
| **vercel-labs/agent-browser** | **Apache-2.0** | 42,827 | false | **2026-09-18** | **Rust** | ✅ **R1.5 强备选**（见下） |
| bytebot-ai/bytebot | Apache-2.0 | 11,082 | **true** | 2025-09-12 | TS | ⛔ **已归档**，不可用 |
| OS-Copilot/OS-Copilot | MIT | 1,794 | false | **2024-09-09** | Python | ⛔ 停滞约 2 年，不作为依赖 |
| rebrowser/rebrowser-patches | **无声明许可** | 1,431 | false | 2025-05-09 | JS | ⛔ 无许可 + 停滞 + 反检测 |
| FASTSHIFT/playwright-stealth | — | — | — | — | — | 仓库已不存在（404） |

#### vercel-labs/agent-browser — 为什么值得单列

README 首手核验要点：
- 定位：**"Browser automation CLI for AI agents. Fast native Rust CLI."**
- 架构：**client-daemon，纯 Rust daemon 直接使用 CDP，"no Node.js required"** ← **对本研究是决定性差异**（Playwright Python 仍需 Node 驱动）
- 默认引擎：**Chrome for Testing**（与 Chrome 136 官方建议一致）；`--engine` 亦可选 lightpanda（⚠️ AGPL，勿启用）
- 页面表征：**无障碍树 + refs（"best for AI"、"deterministic element selection from snapshots"）**，另有 `--annotate` 标注截图供多模态
- 会话隔离：**`--session` 原生多隔离实例**（各自浏览器实例、Cookie、存储、认证状态）
- 会话持久：`--restore` + 稳定 `--session` → 跨重启自动存取 cookie 与 localStorage
- 连接既有浏览器：`connect <port>`、`--cdp`、**`--auto-connect`**（自动发现运行中的 Chrome）；`--profile` 支持 Chrome profile 名或持久化自定义目录
- MCP：内置 `agent-browser mcp`（stdio）
- Token 优化：`screenshot --if-changed`、`--threshold`、`snapshot --delta`、`-i`/`-c`/`-d` 过滤、`--max-output`
- License：**Apache-2.0** ✅

**风险（必须登记）**：属 **Vercel Labs**（实验性标签）→ **continuity 风险**。同批核验的 `bytebot-ai/bytebot` 已归档，即为该类风险的实例。
**另需核验**：其 `--profile Default`（复用真实 Chrome 默认 profile）与 **Chrome 136 政策**是否冲突（`evidence/03`）；以及是否支持 headed 可见模式。

### 6.1 补录（Addendum 轮，2026-09-20）：BrowserSkill / Jev Ultrafast / browser-harness

> 来源：`evidence/10`。核验方法同 §7 边界（GitHub API + 官方原文，**未 clone、未运行**）。

| 项目 | License | Stars | created | pushed | 语言 | 层 | Curis 判定 |
|---|---|---|---|---|---|---|---|
| **`Tencent/BrowserSkill`** | **MIT** ✅ | 5,675 | 2026-06-22 | 2026-09-19 | TS + Rust | **L2（扩展驱动形态）** + 窗口级 L4 | ✅ **登记为接入路径 P2 的参考实现 + 设计吸收源**；**v1 不启用** |
| `browser-use/browser-harness` | **MIT** ✅ | 17,752 | 2026-04-17 | 2026-09-12 | Python | L2（连接/自愈 harness） | ⚠️ **观察项**；须核验其是否依赖远程调试端口 |
| `browser-use/jev-ultrafast` | **MIT** ✅ | 7,551 | **2026-09-16** | 2026-09-18 | Python | L3（**动作选择器**型） | ⛔ **首版不采用** |

**三个关键判断**
1. **BrowserSkill 的控制面是扩展内 `chrome.debugger`（CDP），不使用 `--remote-debugging-port`** —— 四份官方原文穷举 grep **零命中** → **不受 Chrome 136 调试端口政策约束**（`evidence/10` §4）。这是本轮唯一实质技术细化，落点是 **R7 的适用范围**。
2. **其隔离原语是窗口级（Agent Window + ref-store + borrow table），不是凭据罐级** → 与 Curis 的 `(business_id, platform_key)` profile 隔离**正交**，是**补充不是替代**；其"**跨 session 并行**"**禁止**移植到多 Business 场景（`evidence/10` §5）。
3. **Jev 的排除依据（官方原文）**：**"Shadow roots, frames, canvas, uploads, pop-up tabs, nested scrolling, and arbitrary keyboard widgets remain outside this MVP."** —— 与创作者/经营后台（现代 SPA）所需能力**系统性不匹配**；且硬依赖 **`TYPESAFE_API_KEY`**（专有 SaaS 推理），与 Curis"能力可替换不写死"存在张力。

详见 `CURIS_BROWSER_ADDENDUM_2026-09-20_BROWSERSKILL_AND_JEV.md`、`evidence/10`。

### 6.2 候选清单

| 优先级 | 项目 | 采用形态 |
|---|---|---|
| **R1** | **Playwright**（Apache-2.0） | 直接集成，作为 L2 底座（成熟度与文档是企业可用性底线） |
| **R1** | **Playwright MCP**（Apache-2.0） | 借鉴其工具集设计；可选 Provider |
| **R1.5** | **vercel-labs/agent-browser**（Apache-2.0, Rust） | **强备选**：无 Node 依赖 + 原生 session 隔离 + a11y refs；受 labs continuity 风险约束 |
| **R2** | **Stagehand v4 本地模式**（MIT） | ⏸ **后续可选**（首版不用）：封装为 L3 加速器（凭据隔离 + 自愈），**须满足准入条件**（RECONCILIATION §7.4） |
| **R2** | **Chromium / CEF**（BSD-3） | 仅在"必须嵌入式渲染"时；v1 不需要 |
| **R3** | **crawl4ai / ScrapeGraphAI**（Apache-2.0 / MIT） | 仅作内容抽取 Provider，**不承担浏览器自动化** |
| **R3** | **steel-browser**（Apache-2.0） | 自托管方案备选；须确认可关闭 captcha 能力 |
| **P2 参考** | **`Tencent/BrowserSkill`**（**MIT**） | **接入路径 P2（扩展附加真实浏览器）的参考实现**；**v1 不启用**；吸收其窗口级沙箱、借还语义、`effect_state` 三态、能力域化 RPC |
| 观察 | **`browser-use/browser-harness`**（MIT） | L2 连接/自愈 harness；须核验其是否依赖远程调试端口 |
| 观察 | **cua / Agent-S / OmniParser / OpenAdapt** | 属 CGAP-02 Computer Use 研究范畴 |

### 明确不采用
**Skyvern、Firecrawl、Lightpanda**（AGPL-3.0）、**browserless**（SSPL/商业）、**undetected-chromedriver**（GPL-3.0 + 停滞）、**patchright / SeleniumBase CDP Mode**（反检测，与产品原则冲突）、**browser-use 整体**（第二编排器 + Cloud 反检测定位）、**bytebot**（已归档）、**OS-Copilot**（停滞）、**rebrowser-patches**（无许可 + 停滞 + 反检测）。
**Addendum 轮新增**：**`browser-use/jev-ultrafast`**（MIT）—— 理由：① 能力边界**系统性不匹配**（无 Shadow DOM / iframe / canvas / 上传 / 新标签页）；② **第二规划者** + 硬依赖 `TYPESAFE_API_KEY`（专有 SaaS 推理）；③ **库龄 4 天**，官方自述"MVP"、基准为"单一任务、单一 profile、非通用基准"。

---

## 7. 本文件的已知边界

1. **未实际 clone / 运行任何项目** —— 全部结论基于 README / 官方文档 / LICENSE 原文 / GitHub API。
2. **未做性能实测** —— 资源占用列均为结构性判断（进程模型），**非测量值**。
3. **browser-use 的接地实现细节未核验**（未读源码）。
4. **CM 相关的 `from_system_chrome()` 与 Chrome 136 政策的兼容性未核验**。
5. **"Pause/Resume 全部标 ❌"是就"框架原生原语"而言** —— 不代表做不到，而是**必须由 Curis 自建**（`CURIS_BROWSER_SESSION_AND_SECURITY_MODEL` §5.3）。
6. **CFP / 编解码器专利、MPL/LGPL 再分发义务未做法务结论**。
