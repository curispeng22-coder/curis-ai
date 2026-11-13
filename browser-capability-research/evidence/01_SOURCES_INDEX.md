# Evidence 01 — Sources Index & Audit Trail

Authority Class: EVIDENCE
Collected: 2026-09-18（原始）／2026-09-18 **Reconciliation 轮**／**2026-09-20 Addendum 轮**

---

## A. 证据文件清单

| 文件 | 内容 | 性质 |
|---|---|---|
| `repos.txt` / `repos2.txt` | 核验的仓库清单（两批，共 38 项） | 原始输入 |
| `github_repos_raw.json` / `github_repos_raw2.json` | **GitHub REST API 原始返回**（含 repo / license.spdx_id / stars / archived / pushed_at / created_at / language / description） | **机器可复核** |
| `02_LICENSES_VERBATIM.md` | License 分类矩阵 + LICENSE 原文核验 + 商用集成结论 | 首手 |
| `03_CHROME_136_REMOTE_DEBUGGING_CHANGE.md` | Chrome 136 调试端口政策（官方博客原文） | 官方一手 |
| `04_MACOS_TCC_PERMISSION_MODEL.md` | macOS TCC 权限模型与 Browser/Computer Use 成本差异 | 官方文档 + 社区技术指南 |
| `05_PLATFORM_TOS_AND_COMPLIANCE.md` | 中文平台服务条款与合规红线 | **官方原文** + 第三方转述（已标注） |
| `06_PLAYWRIGHT_AUTH_AND_SESSION_SEMANTICS.md` | Playwright 认证与会话语义（官方文档原文） | 官方一手 |
| `07_PLAYWRIGHT_OFFICIAL_CONSTRAINTS.md` | Playwright 官方硬约束 + 三条"已存在浏览器"接入路径 | 官方一手 |
| `08_BROWSER_USE_STAGEHAND_SOURCE_REVIEW.md` | browser-use / Stagehand README 首手核验（含原文引用） | **首手源码级** |
| `09_AUTHORIZED_CONSOLE_AND_API_GATING.md`（**Reconciliation 轮新增**） | 官方通道与 API 资质门槛、平台官方导出功能、A/B 风险区分、UNKNOWN 清单 U1–U6 | **官方原文 + 定向核验** |
| `10_BROWSERSKILL_AND_JEV_ULTRAFAST_SOURCE_REVIEW.md`（**Addendum 轮新增**） | `Tencent/BrowserSkill` 架构与 Agent 契约原文；`browser-use/jev-ultrafast` 机制/边界/数字口径；`browser-harness`；三仓库 License 与活跃度 | **首手源码级** |
| `01_SOURCES_INDEX.md`（本文件） | 来源索引 + 执行审计轨迹 | — |

---

## B. 主要一手来源（按主题）

### B.1 浏览器引擎与策略
- Chromium `LICENSE`（官方）：`https://chromium.googlesource.com/chromium/src/+/main/LICENSE?format=TEXT`（base64）
- Chromium 官网：`https://www.chromium.org/Home/`
- CEF `LICENSE.txt`：`https://bitbucket.org/chromiumembedded/cef/raw/master/LICENSE.txt`
- **Chrome for Developers**（Will Harris, 2025-03-17）：`https://developer.chrome.com/blog/remote-debugging-port`
- Microsoft WebView2 分发：`https://learn.microsoft.com/en-us/microsoft-edge/webview2/concepts/distribution`
- Tauri 配置/多窗口：`https://schema.tauri.app/config/2`、`https://tauri.app/fr/v1/guides/features/multiwindow`

### B.2 自动化运行时
- Playwright 认证：`https://playwright.dev/docs/auth`
- Playwright BrowserType（**含默认 profile 禁止自动化的官方警告**）：`https://playwright.dev/docs/api/class-browsertype`
- Playwright 浏览器与体积：`https://playwright.dev/docs/browsers`
- Playwright MCP 浏览器扩展模式：`https://playwright.dev/mcp/configuration/browser-extension`
- Playwright 官方中文 API 文档（`connect_over_cdp` 仅支持 Chromium）：`https://playwright.net.cn/python/docs/api/class-browsertype`
- `CDP session is only available in Chromium` 源码级溯源：`https://errors.standardbeagle.com/microsoft/playwright/cdp-session-is-only-available-in-chromium`
- Puppeteer 仓库：`https://github.com/puppeteer/puppeteer`

### B.3 Agent Browser 层
- browser-use `README.md`（首手）：`https://raw.githubusercontent.com/browser-use/browser-use/main/README.md`
- Stagehand `README.md`（首手）：`https://raw.githubusercontent.com/browserbase/stagehand/main/README.md`
- **vercel-labs/agent-browser `README.md`（首手）**：`https://raw.githubusercontent.com/vercel-labs/agent-browser/main/README.md`
- Playwright MCP 仓库：`https://github.com/microsoft/playwright-mcp`

### B.4 会话与安全
- macOS TCC / 权限申请（Swift，2026-02 更新）：`https://gist.github.com/Looking4OffSwitch/493e1f9fb9132f2826c4c377b3ce27fe/revisions`
- OpenClaw macOS 权限文档：`https://documentation.openclaw.ai/platforms/mac/permissions`
- Nektony 权限分级（macOS Tahoe 26 语境）：`https://nektony.com/how-to/manage-app-permissions-mac`

### B.5 平台合规（中文平台）
- **抖音《用户服务协议》官方原文**：`https://sf3-cdn-tos.douyinstatic.com/obj/ies-hotsoon-draft/douyin_agreement/agreements.html`
- **抖音电商《【不当获取/使用信息】细则》官方公示**：`https://school.jinritemai.com/doudian/web/article/aJijoYGzDLJ5`
- 小红书自动化合规风险调研（**第三方，需官方复核**）：`https://guancyxx.cn/zh/blog/xiaohongshu-automation-agent-skill-survey`
- 六平台官方数据通道对比（**第三方，需官方复核**）：`https://blog.csdn.net/teacherchen90/article/details/163481231`
- 抖音开放平台 API 规范解读（**第三方，需官方复核**）：`https://blog.csdn.net/gitblog_00188/article/details/157754256`

**（Reconciliation 轮新增来源，详见 `evidence/09`）**
- **抖音开放平台「视频数据解决方案」官方文档**（"用户授权后可直接在第三方系统查看自己发布的抖音视频…统计数据"原文）：`https://open.douyin.com/platform/resource/docs/ability/open-data/video-data-solution`
- **抖音经营号双授权模式官方文档**：`https://partner.open-douyin.com/docs/resource/zh-CN/mini-app/open-capacity/basic-capacities/douyin/`
- 官方 API 资质门槛（第三方技术解读，**需官方复核**）：`https://www.jzl.com/news/douyin-api-12`、`https://www.jzl.com/news/douyin-data-api`
- 平台自述风险边界（第三方转述，**需官方复核**）：`https://www.chanmama.com/yunyingquan/question/4385.html`
- 平台官方导出功能操作指南（第三方，**需官方复核**）：`https://www.80tg.com/news/56627.html`、`https://www.jzl.com/news/douyin-data-56`、`https://shankongmao.com/content/news/1025`

### B.6 云端与定价
- **Browserbase Pricing（独立复核）**：`https://www.browserbase.com/pricing`
- Steel（`/pricing` 实际返回首页，**价格未取得**）：`https://steel.dev/pricing/`

### B.7 新增候选的源码级核验来源（**Addendum 轮，2026-09-20**）
- **`Tencent/BrowserSkill` 架构文档（原文）**：`https://raw.githubusercontent.com/Tencent/BrowserSkill/main/docs/architecture.md`
- **`Tencent/BrowserSkill` 中文说明（原文）**：`https://raw.githubusercontent.com/Tencent/BrowserSkill/main/README.zh-CN.md`
- **`Tencent/BrowserSkill` Agent 契约（原文）**：`https://raw.githubusercontent.com/Tencent/BrowserSkill/main/skill/SKILL.md`
- `Tencent/BrowserSkill` 远程连接文档（用于核验"无远程调试端口依赖"）：`.../main/docs/remote-extension-connection.md`
- **`browser-use/jev-ultrafast` README（原文）**：`https://raw.githubusercontent.com/browser-use/jev-ultrafast/main/README.md`
- `browser-use/browser-harness` 仓库：`https://github.com/browser-use/browser-harness`
- GitHub REST API 核验端点：`https://api.github.com/repos/{owner}/{repo}`（`license.spdx_id` / `stargazers_count` / `archived` / `created_at` / `pushed_at` / `language`）

---

## C. 独立核验记录（本目录直接完成的交叉验证）

| # | 待验事项 | 方法 | 结论 |
|---|---|---|---|
| 1 | `microsoft/playwright-mcp` 许可 | GitHub API + LICENSE 原文 | **Apache-2.0**（纠正某并行研究的"疑似 MIT"） |
| 2 | `chromiumembedded/cef` 许可 | 技术文档原文（bitbucket） | **BSD-3-Clause**（GitHub 报 NOASSERTION 系非标准文件头所致） |
| 3 | `browserless` 许可 | LICENSE 原文 | **SSPL-1.0 OR Browserless 商业许可**；闭源商用需购证 |
| 4 | **OmniParser 许可** | GitHub API `/license` + 原文 base64 解码 | **`LICENSE` 文件实为 `CC-BY-4.0`（Attribution 4.0 International 全文）**；默认分支为 `master`。**并行研究曾报"README badge 为 MIT"，本目录核验未在 README 中找到 MIT 许可标注 → 以 LICENSE 原文为准（CC-BY-4.0）** |
| 5 | cua 的 `omni` extra 依赖 | `pyproject.toml` 原文 | 当前 main 分支 `omni = ["cua-som>=0.1.0,<0.2.0"]`，**未直接依赖 ultralytics**。并行研究称"omni extra 含 ultralytics（AGPL-3.0）"→ **未获证实，标注为未确认**（传递依赖未核验） |
| 6 | Browserbase 定价与规避能力 | 官方定价页 | **Free $0（3 并发 / 1 浏览器小时 / 15 分钟 session）；Developer $20/mo（25 并发 / 100 小时，超额 $0.12/h）；Startup $99/mo**。能力清单含 **"Auto captcha solving"（Developer 起）与 "Stealth Mode"**。数据保留 7/30/30+ 天 |
| 7 | Steel 能力（非价格） | 官网 | 明示 **"Auto CAPTCHA solving"、"Proxy and Browser Fingerprinting（never worry about getting flagged as a bot again）"、"Auto Sign-In"** → **CGAP-04 不相容** |
| 8 | `browserbase/mcp-server-browserbase` 状态 | GitHub API | **archived = true**（2026-07-20）→ 已废弃；Browserbase 现推托管 MCP |
| 9 | `undetected-chromedriver` 状态 | GitHub API | **最近推送 2025-07-05**（约 14 个月停滞）；License **GPL-3.0** |
| 10 | 新增候选 | GitHub API | **`vercel-labs/agent-browser`：Apache-2.0 / 42,827 stars / 活跃（2026-09-18）/ Rust**；`bytebot-ai/bytebot`：**archived**（2025-09-12）；`OS-Copilot/OS-Copilot`：MIT 但停滞（2024-09）；`rebrowser/rebrowser-patches`：**无声明许可** + 停滞（2025-05） |
| **11** | **B 类场景的官方通道是否存在**（Reconciliation 轮） | 抖音开放平台**官方文档**原文 | **存在**：官方明示"抖音帐号运营者或普通用户**完成授权后，可直接在第三方系统或应用内查看自己发布的抖音视频…统计数据**"，并称其为"**唯一官方认证的对外开放的抖音数据**"（`evidence/09` §1） |
| **12** | **官方 API 的资质门槛**（Reconciliation 轮） | 第三方技术解读（**需官方复核**） | **仅限企业开发者，个人开发者无法调用**；授权范围仅限"已授权用户自己发布的视频"，**恰与 Curis 主场景吻合但资质不开放**（`evidence/09` §2） |
| **13** | **平台是否提供官方导出功能**（Reconciliation 轮） | 第三方操作指南（**需官方复核**） | **是**：抖音创作服务平台 / App 数据中心均提供「导出数据」（Excel，7/30/90 天或自定义）；抖店后台「批量导出」CSV（`evidence/09` §5） |
| **14** | **`Tencent/BrowserSkill` 的 License 与活跃度**（Addendum 轮） | GitHub API | **MIT**；**5,675★**；`created 2026-06-22`；`pushed 2026-09-19`；**未归档**（`evidence/10` §1） |
| **15** | **BrowserSkill 是否依赖 `--remote-debugging-port`**（Addendum 轮，**关键**） | 四份官方原文穷举 grep | **不依赖**：`--remote-debugging-port` / `--user-data-dir` / `--remote-debugging-pipe` **零命中**；控制面为**扩展内 `chrome.debugger`**（`evidence/10` §4）→ **Chrome 136 调试端口政策不适用于扩展路径** |
| **16** | **`browser-use/jev-ultrafast` 的 License / 库龄 / 边界 / 数字口径**（Addendum 轮） | GitHub API + README 原文 | **MIT**；**7,551★**；**`created 2026-09-16`（库龄 4 天）**；官方自述排除 **Shadow roots / frames / canvas / uploads / pop-up tabs / nested scrolling**；**"450× / 3 分钱"无官方同口径数据**，官方为协议调用 **1,092 → 101**、基准自述"**非通用可靠性基准**"（`evidence/10` §6） |

---

## D. 执行审计轨迹（Audit Trail）

### D.1 左脑链路
- `启动左脑.py input`（主链路 intent → profile → ternary_context → dispatch）：**✓ 执行成功**
- `启动左脑.py inject`（知识/因果上下文注入）：**✓ 执行成功**，命中 3 条既有记忆（PHASE 1 Business Truth / PHASE 2 Provider Feasibility / Curis Desktop 产品结构），确认本研究与既有口径一致
- **环境异常与处置**：本机 `PYTHONPATH` 注入 WorkBuddy CLI shim（`sitecustomize.py` 的 brokered-FS 钩子），导致 `data/` 目录 `mkdir(exist_ok=True)` 抛 `PermissionError: EEXIST`。以 `env -u PYTHONPATH -u PYTHONDONTWRITEBYTECODE` 绕过 shim 后恢复正常。**诊断与解法已写入 `~/.workbuddy/MEMORY.md`。**

### D.2 并行研究分工与结果
受既往 **429 并发教训**约束，全程控制在 **3 并发以内、滚动补位**。

| 线 | 主题 | 结果 | 备注 |
|---|---|---|---|
| 1 | 主流 AI 产品 Browser / Computer Use 实现 | ✅ 交付 | 覆盖 OpenAI / Anthropic / Claude in Chrome / Manus / 中国产品 / Perplexity Comet 等 |
| 1' | 中国产品与海外其它 Agent 浏览器补充 | ✅ 交付 | 明确指出 豆包/元宝/WorkBuddy **未取得可验证的公开技术文档**；Zhipu 页面被 WAF 拦截 |
| 2 | 自动化运行时（Playwright 深潜） | ✅ 交付 | 提供 Playwright 官方"默认 profile 禁止自动化"原文与 `--extension` 模式 |
| 3 | Agent Browser 层与开源项目 | ⚠️ **首次派发框架层失败** → 重新派发 ✅ 交付 | 提供 `vercel-labs/agent-browser` 等新增候选 |
| 4 | Agent Browser 层源码级评估 | ✅ 交付 | 提供 Playwright MCP 工具名、Anthropic computer-use-demo 架构与安全警示、cua/Lume 机制 |
| 5 | 云浏览器与成本 / License | ✅ 交付 | 提供云厂商矩阵；**其报价多为转述，本目录仅对 Browserbase 做了独立复核** |

### D.3 诚实声明的限制
1. **未执行 `git clone`、未本地运行任何项目** —— 受本机沙箱限制，改用 GitHub API + `raw.githubusercontent.com` 原文抓取。**"未实际运行"是本轮全部性能类结论的边界。**
2. **未做性能实测**（内存 / CPU / 耗时）。
3. **未做法务结论**（MPL/LGPL 再分发义务、编解码器专利、OmniParser 权重条款、WebView2 法律文本）。
4. **并行研究的部分数据为二手转述**，已在 `CURIS_BROWSER_TECHNOLOGY_MATRIX.md` §6 以 `✔独立复核` / `△转述` 逐行标注，**并声明 `△转述` 不得作为决策依据**。
5. **平台条款**：仅抖音为官方原文；小红书 / 快手为第三方转述，**需官方复核**。
6. **中文平台风控的触发阈值不可量化**，全报告仅作定性表述（风险升高），未给出任何量化断言。

### D.4 未使用的工具（声明）
本轮**未**使用：修改 Curis 任何文件的编辑操作、Figma 相关能力、`git commit` / `git push`、任何浏览器自动化执行、任何 Curis Runtime 调用。
本目录**仅包含**研究产物（`.md` + `.json` + `.txt`）。

### D.5 Reconciliation 轮执行审计（2026-09-18 第 2 轮）

| 项 | 执行情况 |
|---|---|
| 任务性质 | **只纠正 Problem Definition / Primary Use Case / Risk Interpretation / MVP**；**未重做技术研究**、**未推翻** Playwright / Local-first / Profile / Stop Gate |
| 定向核验 | **2 次**（抖音创作者中心数据导出、抖音开放平台 API 资质门槛）→ `evidence/09`；**未做泛搜** |
| 左脑链路 | `启动左脑.py input` / `inject` 均执行；环境处置同 D.1（`env -u PYTHONPATH`） |
| 产出 | `CURIS_BROWSER_USE_CASE_RECONCILIATION.md`（15 节） |
| 同步更新 | STUDY、RECOMMENDATION、TECHNOLOGY_MATRIX、LOCAL_CLOUD_HYBRID、AUTOMATION_AND_AGENT_LAYER、OPEN_SOURCE_DEEP_DIVE、RESEARCH_JOURNAL、本文件 |
| 边界遵守 | **未**开发 / **未**改 Runtime·Authority·UI / **未**改 HTML·Figma / **未** commit·push |
| 未闭环项 | **U1–U6**（`evidence/09` §6）需法务或官方渠道确认；其中 **U1/U3** 为产品可行性层的关键 UNKNOWN |

### D.6 Addendum 轮执行审计（2026-09-20 第 3 轮）

| 项 | 执行情况 |
|---|---|
| 任务性质 | **纳入点名的新候选并做源码级核验**；**未重做技术研究**、**未推翻**任何有效结论、**未开发** |
| 核验方法 | GitHub REST API + `raw.githubusercontent.com` 官方原文抓取（**未 clone、未运行**） |
| 核验对象 | `Tencent/BrowserSkill`、`browser-use/jev-ultrafast`、`browser-use/browser-harness`（附录） |
| 左脑链路 | `启动左脑.py input` / `inject` 均执行；环境处置同 D.1（`env -u PYTHONPATH -u PYTHONDONTWRITEBYTECODE`） |
| 产出 | `evidence/10_BROWSERSKILL_AND_JEV_ULTRAFAST_SOURCE_REVIEW.md`、`CURIS_BROWSER_ADDENDUM_2026-09-20_BROWSERSKILL_AND_JEV.md` |
| 同步更新 | SESSION_AND_SECURITY_MODEL（**新增 §2.1 接入路径 P1/P2/P3** + R7 细化）、OPEN_SOURCE_DEEP_DIVE（§6.1 补录）、TECHNOLOGY_MATRIX（L2/L3 新行 + L4 接入路径行）、AUTOMATION_AND_AGENT_LAYER（**新增 §2.5** + §5 两行）、RESEARCH_JOURNAL（**新增 §7**）、本文件 |
| 结论层影响 | **细化 R7 适用范围**（Chrome 136 限 CDP/Playwright 路线；**扩展路径不受限**）；**新增 1 项待裁定**（接入路径 P2 是否在 v1 开放）；**新增 7 条设计增项**；**R1–R15 全部保留** |
| 边界遵守 | **未**泛搜 / **未**开发 / **未**改 Runtime·Authority·UI / **未**改 HTML·Figma / **未** commit·push |
| 未闭环项 | `browser-harness` 是否依赖远程调试端口（**未核验**）；BrowserSkill 的 21 个 tool 完整清单与扩展 UX（**未评估**）；三项目在**中文创作者后台**的实际表现（**未测**） |
| **自查发现** | 复核中发现**第 2 轮的一处遗漏**：`CURIS_BROWSER_AUTOMATION_AND_AGENT_LAYER.md` §5 结论表中 `Stagehand` / `browser-use` 两行**未随 Reconciliation 收紧**（文首已声明、正文仍为旧口径）→ **已补正**（`RESEARCH_JOURNAL.md` §7.8 有记） |

---

## E. 目录定位声明

本目录 `browser-capability-research/` 位于 **workspace 根目录**，**不在 `docs/` 下**。
因此：
- **不构成** `docs/01_Product/Curis_Product_Blueprint.html` 的替代或平行版本；
- **不产生** Current Authority；
- 符合 `AGENTS.md` §3「不创建第二份 Current Blueprint / Master Map / Page Map / UI Blueprint」的纪律。
- **若本研究需进入正式产品生产线**，必须走 Pointer / `CURRENT_STATE.md` / `docs/08_Change_Log/CHANGE_LOG.md` 流程，并由总控决策席裁定。
