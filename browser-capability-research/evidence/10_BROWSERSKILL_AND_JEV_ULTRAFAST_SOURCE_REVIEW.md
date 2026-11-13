# Evidence 10 — BrowserSkill 与 Jev Ultrafast 源码级核验（Addendum 轮）

Authority Class: EVIDENCE
Collected: **2026-09-20**（Addendum 轮）
性质：本条为**新增候选的源码级核验**。核验方法 = **GitHub REST API + `raw.githubusercontent.com` 原文抓取**（与 `evidence/02` 同法；**未 clone、未本地运行**）。

> **降级声明（沿用）**：受本机沙箱限制，本轮**未执行 `git clone` 与本地运行**。全部结论基于仓库 README / `docs/` 官方文档 / `skill/SKILL.md` 原文 / GitHub API。
> **「未实际运行」是本文件的已知边界**，一切性能类结论**均无本目录实测**。

---

## 0. 核验状态图例

| 标记 | 含义 |
|---|---|
| ✔独立复核 | 本目录**直接抓取官方原文或 API** 确认 |
| △转述 | 来自二手笔记 / 视频 / 第三方，**未经官方原文确认** |
| ✖未证实 | 有来源声称，但**官方原文未支持或明确无同口径数据** |

---

## 1. 仓库级事实（GitHub REST API，2026-09-20 抓取）

| 项 | `Tencent/BrowserSkill` | `browser-use/jev-ultrafast` | `browser-use/browser-harness`（附录） |
|---|---|---|---|
| License (`spdx_id`) | **MIT** ✔ | **MIT** ✔ | **MIT** ✔ |
| Stars | **5,675** ✔ | **7,551** ✔ | 17,752 ✔ |
| 主语言（API 报告） | **TypeScript** ✔ | **Python** ✔ | Python ✔ |
| created_at | 2026-06-22 ✔ | **2026-09-16** ✔ | 2026-04-17 ✔ |
| pushed_at | 2026-09-19 ✔ | 2026-09-18 ✔ | 2026-09-12 ✔ |
| archived | false ✔ | false ✔ | false ✔ |
| description（原文） | "Let AI agents use your real, logged-in browser without interrupting your work. CLI + extension for browser automation across any shell-capable AI agent…" ✔ | "i. am. speed." ✔ | "Browser Harness \| Self-healing harness that enables LLMs to complete any task." ✔ |

### 1.1 两条**必须登记**的事实

1. **BrowserSkill 已明确采用 MIT License** ✔ —— 二手笔记中"视频称无许可证/默认保留所有权利"的说法**已过时**。（与笔记自身的修正一致，本目录独立复核确认。）
2. **`jev-ultrafast` 库龄 = 4 天**（created 2026-09-16，核验时 2026-09-20）✔ —— **7,551 stars in 4 days** 属热度信号；**不构成成熟度证据**。其 README 自述为 MVP，且**未设 release 稳定承诺**。
3. **`browser-harness` 是 Jev 的 L2 连接层**（`uv sync` 安装，`browser-harness --doctor`）✔ —— 它本身是一个 **MIT / 17.7k stars / 活跃**的独立项目（"Self-healing harness"），**应与 `jev-ultrafast` 分开评估**（前者是可复用的 L2 候选，后者是 L3 决策层）。

---

## 2. BrowserSkill 架构核验（`docs/architecture.md` 原文）

### 2.1 系统链路（原文系统图，逐节点转录）✔

```
[Agent harness]  Claude Code / Cursor / Codex
        │ shell: bsk …
        ▼
[Developer machine]
  bsk CLI  ◄──JSON Lines / UDS──►  bsk daemon  ◄──WebSocket JSON──►  bsk extension (MV3)
        ▼
[Chromium]
  extension ──CDP + WebExt──►  User tabs + Agent Windows
```

### 2.2 组件事实（原文）✔

| 组件 | 关键事实（原文要点） |
|---|---|
| `bsk` CLI（Rust，`crates/bsk-cli`） | 动词-名词子命令（`bsk session start`、`bsk click`…）；IPC 发现 daemon，仅在缺失时自动拉起（`BSK_AUTO_START=0` 可禁）；JSON Lines over `$BSK_HOME/run/daemon.sock`；默认 home `~/.bsk` |
| `bsk` daemon（同一二进制） | **本地模式监听 loopback WebSocket，默认端口 52800**（`--port` 可配）；**握手校验 `Origin: chrome-extension://…`**；维护 `browsers`（已连扩展）与 `sessions`（Agent Window 绑定）；**per-session queue 串行化同一 session 的 tool call** |
| 状态文件 `~/.bsk/` | `daemon.lock`（**advisory lock —— 单 daemon 实例**）、`daemon.json`、`daemon.log`（rolling trace）、`daemon.pid` |
| `bsk` extension（`apps/extension`） | **WXT / MV3 Chromium 扩展**（React popup + service worker）；`tools/` = `ToolDispatcher` → **21 个 tool handler**；`session-manager/` = sessions / Agent Window / **ref-store（`@e1`）**；**`browser-driver/` = CDP-backed browser operations**；`content/` = Agent Window 内的控制浮层 |
| `bsk-protocol`（Rust） | 共享类型 + JSON Schema 生成；TS 侧镜像帧结构，经测试与 schema dump 保持同步 |

### 2.3 会话与沙箱模型（原文）✔

- **Session** = 不透明 ID（v0.1 为 4 个小写字母）+ **专用 Agent Window** + session 级 ref-store + **borrow table**。
- **Sandbox-only**：**写工具要求目标 tab 位于 Agent Window 内，除非该 tab 是从用户 profile 显式 *borrowed***。
- **`bsk session stop` 是强制步骤**；**idle timeout（默认 5 min）仅为安全网**。
- **同一浏览器的多个 session → 多个 Agent Window，完全隔离**。
- 远程内容读取/操作**必须**为任务创建或显式借用的 tab；页面自行打开的弹窗、或被移入 Agent Window 的用户 tab，**不会**自动变为受控。

### 2.4 并发策略（原文）✔

| 范围 | 策略 |
|---|---|
| 同一 session | daemon **串行化 RPC**（ref-store 安全） |
| 不同 session | **并行** |
| 多浏览器 | `bsk session start --browser <id>` |

### 2.5 连接安全（原文）✔

- 本地模式 **loopback 绑定**；服务端模式经**认证 WSS**（明文监听仅在 loopback 后置于 TLS 终止或开发用途）。
- **WS upgrade 时做扩展 origin 白名单校验。**
- **"Website cookies stay in the user's browser profile."** —— 远程设备凭据存于**扩展 origin 的 IndexedDB**；内置服务端只存**凭据哈希**于私有 `BSK_HOME`；配对与设备授权治理远程访问。
- **`evaluate` 在 sandbox 模式下仅限 Agent Window 内的 tab。**
- **操作审计（启用时）存于 daemon 宿主**（远程模式下亦在服务端）。

### 2.6 关键：**`effect_state` 三态契约（原文原文，最高价值）**✔

> Browser-side operations report **`effect_state` (`none`, `committed`, or `unknown`)**、`phase`、`cleanup_state`.
> **Confirmed success wins over a late cancel; an unknown effect is preserved across timeout or transport loss and must not be retried blindly.**
> A transfer deadline sends cancellation to the extension and **keeps the session queue occupied for bounded compensation rather than abandoning an in-flight browser effect.**

→ **与 Curis 已裁定的 `EFFECT_UNKNOWN`（写后未知不得降级为普通 failed）语义同构**，且给出了**队列层面的落地做法**（取消不释放队列，改为有界补偿）。**这是本轮最有价值的技术细节。**

### 2.7 文件传输边界（原文）✔

- **上传/下载仅支持本地连接**；远程 session 返回 `unsupported`。
- 仅 CLI 读上传源、写下载目标；扩展**从不接收** agent 侧路径。daemon 为存储能力的权威，签发不透明的 session 级 transfer ID，私有暂存、注入私有暂存路径，**在验证路径/类型/symlink 边界/字节上限后才接手清理与导入**。
- 上传暂存**保留到 session teardown**（页面可能在后续表单提交时才读附件），session stop / 浏览器断连 / daemon 崩溃重启时释放。

---

## 3. BrowserSkill 的 Agent 契约（`skill/SKILL.md` 原文引用，逐条）✔

> 本节引用为**逐字原文**，是「业界收敛」判断的证据基础。

| # | 原文（节选） | 位置 |
|---|---|---|
| C1 | "**Never extract credentials, cookies, tokens, or other secrets.**" | 头部规则 |
| C2 | "**Always run `bsk session stop <id>` on success and failure**, unless keeping the session open is part of the user's request. This also returns borrowed tabs. Returned tabs stay open in the user's window. **Do not rely on idle cleanup** or stop/restart the shared daemon to finish a task." | 核心循环 |
| C3 | "**Stop at the requested goal; a trace grants no additional authorization.**" | 核心循环 |
| C4 | "**Never invent tab IDs or keep a user tab across unrelated work. Do not repeat pending, denied or timed-out borrows.**" | Borrowing |
| C5 | "For **`borrow_outcome_unknown`**, inspect tab/session state first: the tab may already have moved. **Do not bypass an outcome through another browser backend.**" | Borrowing |
| C6 | "Deprecated `--unattended`, `--no-confirm`, and `BSK_REQUEST_HELP=off` **cannot override these settings**. **Never change browser storage/settings to bypass them.**" | Borrowing |
| C7 | "With help enabled, request help for **login, CAPTCHA, OTP, payment confirmation**…" | Human steps |
| C8 | 恢复表：Help `cancelled` / `timed_out` → "**Respect rejection or the blocker; do not repeat the request.**" | Human steps |
| C9 | `fill_value_mismatch` → "Read the field… **Correct only a remaining difference; no blind refill or immediate handoff.**" | 错误处置 |
| C10 | "**There is no default token cap.** With `observe --max-tokens <n>`…" | observe |
| C11 | "navigation, loss of control or **a debugger reconnection** does [invalidate refs]" | ref 失效条件 |

### 3.1 扩展设置的用户优先权（`README.zh-CN.md` 原文）✔

扩展弹窗提供**两个默认开启**的独立设置，并 **"用户在插件中保存的设置对所有会话具有最终决定权"**：

| 借用标签页前确认 | 允许请求人工协助 | 实际行为 |
|---|---|---|
| 开 | 开 | 借用需要确认；求助正常弹窗 |
| 开 | 关 | 借用需要确认；求助返回 `disabled` |
| 关 | 开 | 借用免确认；求助正常弹窗 |
| 关 | 关 | 借用免确认；求助返回 `disabled` |

> README 另注：**"不再跳过确认或关闭人工协助"**（即该设置体系是**收口**方向，而非放开无人值守）。

### 3.2 官方中文说明中的产品级定位（原文）✔

- "**不中断你的工作**：浏览器任务在独立可见的 **Agent Window** 中运行，不影响你继续使用自己的浏览器。"
- "**内置 human-in-loop**：遇到 captcha、登录、确认弹窗等**必须由人处理**的步骤时，Agent 可以**主动请求你接管**，完成后再继续任务。"
- "需要 Agent 操作你**已打开的标签页**？必须**显式借用**该标签，任务结束后**归还**，其余浏览器窗口不受影响。"
- 支持矩阵：**Chrome 与 Microsoft Edge 已支持**；其他可加载 Chromium 扩展的浏览器通常可用；**Firefox 计划中**。

---

## 4. ⚠️ 关键反向核验：BrowserSkill **不依赖** `--remote-debugging-port`

**方法**：对 `README.md`、`README.zh-CN.md`、`docs/architecture.md`、`docs/remote-extension-connection.md`、`skill/SKILL.md` 五份原文做关键词穷举 grep（`remote[- ]debugging`、`--user-data-dir`、`user-data-dir`、`chrome.debugger`）。

**结果** ✔：
- **`--remote-debugging-port` / `--remote-debugging-pipe` / `--user-data-dir` 零命中。**
- 控制面为**扩展内 `chrome.debugger`（CDP）**：`architecture.md` 系统图 = `Ext -->|CDP + WebExt| Tabs`；`browser-driver/` = "CDP-backed browser operations"；典型调用第 4 步 = "Extension dispatcher validates sandbox rules, **invokes CDP via `BrowserDriver`**"。
- `SKILL.md` 中出现的 "**debugger reconnection**" 指**扩展内 debugger 会话的断开重连**（`chrome.debugger` detach/attach），**不是**远程调试端口。

### 4.1 该核验的**准确含义**（不得过度引申）

| 命题 | 判定 |
|---|---|
| Chrome 136 政策（`evidence/03`）限制的是 **`--remote-debugging-port`/`--remote-debugging-pipe` 在默认 data dir 上** | ✅ **不变**（官方原文） |
| BrowserSkill 走的是**扩展路径**，因此**不受**该政策直接约束 | ✅ **成立**（本节核验） |
| 因此"复用用户日常 Chrome"在**扩展路径下仍可行** | ✅ **成立** |
| 因此**R7 被推翻**（即"复用日常 profile 已被官方关闭"作废） | ❌ **不成立**。R7 的原始表述针对的是 **CDP / Playwright 路线**。**扩展是另一条通道，而非同一条通道的绕过**。R7 应被**细化（限定适用范围）**，而非撤回 |
| 因此 Curis **不需要**专用 profile | ❌ **不成立**。Curis 需要的是**按 Business 隔离凭据罐**，而扩展路径的隔离在**窗口级**（见 §5），**提供不了这一层** |

---

## 5. 隔离原语的**层不同**（关键差异）

| 维度 | BrowserSkill | Curis（既有结论） |
|---|---|---|
| 隔离载体 | **窗口级**：Agent Window + session 级 ref-store + borrow table | **凭据罐级**：`(business_id, platform_key)` **独立 profile 目录** |
| 浏览器 profile | **用户日常 Chrome profile**（扩展装在其内；"cookies stay in the user's browser profile"） | **Curis 专用 profile**（每 Business × Platform 一份） |
| 跨 session 共享 | **同一 profile ⇒ 同一 cookie 罐**（多 Agent Window 并行 ≠ 多登录态） | **不共享**（每个 profile 独立登录态） |
| 并发 | 同 session 串行 / 跨 session 并行 / 跨浏览器 `--browser` | **同 profile 不可并发**（SingletonLock，R15） |
| 隔离目标 | 防**跨 session 的 ref 混淆与误写** | 防**跨 Business 的账号/数据串号** |

### 5.1 结论（对本研究是**补充**，不是替代）

- BrowserSkill 的隔离**解决的是"同一登录态下的多任务互不干扰"**；
- Curis 的隔离**解决的是"多 Business、可能多账号的登录态共存"**；
- → **两者正交**。Curis 的 profile 级隔离**仍然必需**（多 Business 是 Curis 的产品前提）；BrowserSkill 的**窗口级沙箱 + 借还表**是 Curis 现有设计**尚未表述**的**可吸收增项**（见 Addendum §6）。
- ⚠️ 同时意味着：**BrowserSkill 的"多 Agent 并行"能力不可直接移植到 Curis 的多 Business 场景**（并行窗口共享 cookie 罐 ⇒ 若两个 Business 用同一平台的不同账号，将互相覆盖登录态）。

---

## 6. Jev Ultrafast 核验（`README.md` 原文）

### 6.1 定位与机制（原文）✔

- 自我定位：**"A browser agent with a dynamic, indexed action space."**
- 动作空间（**有限且类型化**）：`CLICK`、`TYPE_TEXT`、`SELECT`、`SCROLL_UP`、`SCROLL_DOWN`、`WAIT`、`DONE`、`BLOCKED`。**"Only supported operations and targets are offered."**
- 决策形态：**一次 TypeSafe 请求**同时输出 `operation` 与 `click_target` / `type_text_target` / `select_target`；**"Target questions are speculative"** —— 若操作为 `CLICK`，仅 `click_target` 可执行。**"Two decisions, one network round trip."**
- 文本生成：**仅 `TYPE_TEXT` 调小模型**（示例为 OpenRouter `inception/mercury-2.5`，关闭 reasoning；亦可配 Gemini / GLM / DeepSeek 的 OpenAI 兼容接口）。
- **"There are no site-specific action scripts or prepared field strings in the policy."**
- **"The Flights example supplies a goal and independently verifies the outcome."**

### 6.2 与 Chrome 的连接方式（**对本研究至关重要**）✔

> **"Chrome connects through Browser Harness… Run `uv run browser-harness --doctor` if it needs connecting. Allow remote debugging in Chrome when prompted."**
> **"Owned tabs share the existing Chrome profile."**

→ **Jev 明确依赖"远程调试 + 用户现有 Chrome profile"**，即 **`evidence/03` 所指 Chrome 136 收紧的那条路径**，并且**使用的是用户真实 profile**。
→ **反向强化 R7**：连 browser-use 团队 2026-09 的新项目也仍走此路径并要求用户"允许远程调试"。**这不是我们的臆测，而是该品类的现实成本。**

### 6.3 安全建构（原文）✔

> **"Model output never becomes selectors, coordinates, shell commands, or executable JavaScript. Text-helper output must parse as a small JSON object before typing."**
> **"Every executed target is resolved from an observed node. The executor rechecks page freshness and click occlusion."**

→ **模型输出不得成为可执行件**、**执行前重校验** —— 与本研究的"代码掌握执行/权限/停止条件"同向。

### 6.4 ⚠️ 独立验收入口（原文，最高价值）✔

> **"A `DONE` choice still requires independent outcome verification."**

→ **明确把"Agent 自述完成"与"独立验收通过"分开建模**，与 Curis 的**独立 Verification 原则同构**，且来自一个**真实浏览器 Agent 项目**。

### 6.5 能力边界（原文**逐字**，对本研究为**决定性排除依据**）✔

> "The DOM reader handles common HTML and ARIA controls, **not the full accessible-name specification**.
> **Shadow roots, frames, canvas, uploads, pop-up tabs, nested scrolling, and arbitrary keyboard widgets remain outside this MVP.**"

### 6.6 性能数字的正确口径（纠正视频说法）✔ / ✖

| 数字 | 官方原文口径 | 判定 |
|---|---|---|
| 演示耗时 | **7,073 ms**（Google Flights，Zürich→London） | ✔ |
| 中位耗时 | **9.450 s → 7.092 s（−25%）**，六次交替运行，两版本各 **3/3** 通过 | ✔ |
| 浏览器协议调用 | **1,092 → 101**（≈**10.8×** 减少） | ✔ |
| **"算力暴降 450 倍"** | **官方无同口径数据** | ✖ **未证实** |
| **"单次不到 3 分钱"** | 官方仅注明示例中的**文本辅助调用**成本（约 `$0.00006272`），**非任务总成本**；且 TypeSafe 只返回 token 用量、**未返回该任务的完整计费金额** | ✖ **未证实** |
| 样本强度 | 原文自述：**"three repeats of one task on one browser profile, not a general reliability benchmark."** | ✔ —— **须原样引用，不得省略此限定** |

### 6.7 商业与依赖（原文）✔

- README 顶部即 **"The Browser Use Cloud waitlist is open… Join the waitlist"** → **该项目同时是 Browser Use Cloud 的引流入口**（该云即本研究已判定**与 CGAP-04 品类级冲突**的那一类）。
- 运行依赖：**`TYPESAFE_API_KEY`（专有 SaaS 推理服务）+ 一个文本模型 API Key**。
- 本机 inspector：**`http://127.0.0.1:8766`**（注意：与本机"左脑"面板的 **8765** 相邻，同机部署时**存在端口竞争可能**——仅供登记，非本轮结论）。

---

## 7. 本证据文件的净结论

1. **两个项目均 MIT、均活跃、均非归档** ✔；但 **`jev-ultrafast` 库龄 4 天**，**成熟度不足以进入任何首版路径**。
2. **BrowserSkill 的架构核验产生一条真实的、此前未记录的技术事实**：**扩展路径（`chrome.debugger`）不受 Chrome 136 的远程调试端口政策约束** → **R7 需细化适用范围**，且必须**同时保留"Curis 仍需专用 profile"**（理由从"官方禁止"改为"Curis 需要凭据罐级隔离"）。
3. **BrowserSkill 的隔离原语是窗口级，与 Curis 的凭据罐级正交** → **补充，不是替代**；且其"多 session 并行"**不可移植到多 Business 场景**。
4. **SKILL.md / architecture.md 提供了 6 条可直接引用的"业界收敛"原文**（C1–C9、`effect_state` 三态），覆盖：**凭据边界、强制 session stop、范围即授权、不重试被拒授权、未知结果不得绕过、不得为无人值守关闭确认、`EFFECT_UNKNOWN` 不得盲目重试**。
5. **Jev 的能力边界（无 Shadow DOM / iframe / canvas / 上传 / 新标签页）与 Curis 主场景（现代 SPA 创作者后台）系统性不匹配** → **首版明确不采用**。
6. **视频中的"450×/3 分钱"无官方同口径数据** → 引用时**必须**用法定的 **10.8×（协议调用）** 与 **−25%（中位耗时）**，并**原样带上"3/3、单一任务、单一 profile、非通用基准"的限定**。

---

## 8. 本文件的已知边界

| 项 | 状态 |
|---|---|
| **未 clone / 未本地运行任一项目** | 全部结论基于官方 README / `docs/` / `SKILL.md` / GitHub API；**无本机运行时实测** |
| BrowserSkill 的 **21 个 tool handler 完整清单** | 未逐项取得（仅取得计数与分类） |
| BrowserSkill 扩展在当前 Chrome 版本上的**调试横幅 / UX 影响** | **未验证** |
| `chrome.debugger` 与 Chrome 后续版本政策的**长期风险** | **未评估**（Chrome 136 已表明 Google 会收紧自动化面） |
| Jev 的**真实站点兼容度** | 未测；仅有官方自述的能力边界 |
| 两项目在**中文创作者后台**（抖音/小红书等）上的实际表现 | **未测**（本轮不涉及平台登录与实操） |
| 任何性能/成本数字 | **本目录无实测**，一律以官方原文口径转述并标注 |
