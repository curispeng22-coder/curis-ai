# CURIS BROWSER ADDENDUM — BrowserSkill 与 Jev Ultrafast

**新增候选的核验与影响评估（第 3 轮）**

Authority Class: **RESEARCH — ADDENDUM**（非裁定）
Status: **Draft — Ready for CEO Review**
Date: **2026-09-20**
前序：`CURIS_BROWSER_USE_CASE_RECONCILIATION.md`（第 2 轮，问题定义与风险定性）
Evidence（新增）：**`evidence/10_BROWSERSKILL_AND_JEV_ULTRAFAST_SOURCE_REVIEW.md`**
Evidence（既有）：`evidence/01`–`evidence/09`

> 本轮**只做**：把两个新出现的开源项目纳入候选集、做**源码级核验**、评估其对既有结论的影响。
> **未重做技术研究**、**未推翻** Playwright / Local-first / Stop Gate / Route A、**未开发**、**未改** Curis Authority / Runtime / UI / HTML / Figma。

---

## 0. 一页结论

| 问题 | 结论 |
|---|---|
| 两个项目是否存在且可信 | ✅ **均存在**。`Tencent/BrowserSkill` **MIT / 5,675★ / TypeScript + Rust / 活跃**；`browser-use/jev-ultrafast` **MIT / 7,551★ / Python / 但库龄仅 4 天**（`evidence/10` §1） |
| 是否推翻既有结论 | ❌ **一条都没推翻**。**R1–R15 全部有效**（§9） |
| 有没有产生**新的**结论 | ✅ **有一条实质性技术细化**：**R7 的适用范围须收窄**（§3）——Chrome 136 关闭的是 **CDP + 默认 profile** 这条路，**扩展路径不受该政策约束** |
| 这条细化会不会让 Curis 改用"用户日常 Chrome" | ❌ **不会**。Curis 需要**凭据罐级**（per-Business profile）隔离，而扩展路径的隔离是**窗口级**（§5）。**Curis 仍须持有专用 profile**，但**理由的表述必须更正** |
| BrowserSkill 的定位 | **L2（扩展形态）+ 部分 L4**。**不是 Playwright 的替代**，而是**接入路径 P2 档（扩展附加真实浏览器）的现成 MIT 参考实现 + 可吸收的窗口级沙箱设计** |
| Jev Ultrafast 的定位 | **L3 的一个更轻形态（结构化动作选择器）**。**首版明确不采用**（§8） |
| 本轮最有价值的产出 | ✅ **业界收敛证据**：BrowserSkill 的 `SKILL.md` / `architecture.md` 与 Jev 的 README **独立复现了 Curis 的 6 项核心契约**（§6）——含 **`EFFECT_UNKNOWN` 不得盲目重试**、**凭据边界**、**范围即授权**、**`DONE` ≠ 验收通过** |
| 是否改变技术选型 | ❌ **不改变**。Playwright（L2 主选）/ Local-first / headed / 专用 profile / Stop Gate / 首版路线 A —— **全部维持** |
| 新增待 CEO 裁定 | **1 项**：**接入路径 P2（扩展附加真实浏览器）是否在 v1 开放**（§11） |

---

## 1. 本轮边界

| 允许 | 执行 |
|---|---|
| 纳入新候选 + 源码级核验 | ✅ 完成（`evidence/10`；GitHub API + 官方原文） |
| 评估对既有结论的影响 | ✅ 完成（本文件） |
| 文档增量更新 | ✅ 完成（见 §12） |

| 禁止 | 执行 |
|---|---|
| 重做技术研究 / 泛搜 | ✅ 未做（仅对**两个点名项目**核验） |
| 推翻既有有效结论 | ✅ 未做 |
| 开发 / 改 Runtime / 改 Authority / 改 UI | ✅ 未做 |
| HTML / Figma | ✅ 未做 |
| commit / push | ✅ 未做 |

---

## 2. 层定位（沿用本研究的四层模型）

| 项目 | 主层 | 依赖层 | 形态 | Curis 判定 |
|---|---|---|---|---|
| **Tencent/BrowserSkill** | **L2 Automation Runtime**（分支形态：**扩展驱动**） | L0（用户既有 Chromium） | CLI(Rust) + daemon(Rust) + **MV3 扩展** | ✅ **纳入候选：接入路径 P2 的参考实现**（§4） |
| └ 其 `session-manager/` + borrow table | **L4 Session/Profile**（**窗口级**子集） | — | — | ✅ **可吸收**（§7） |
| └ 其 `operation-audit` | L4 Evidence | — | — | ✅ 与既有 Evidence 契约同向 |
| **browser-use/jev-ultrafast** | **L3 Agent Layer**（**动作选择器**型） | L2（经 `browser-harness`） | Python 库 + 本地 inspector | ⛔ **首版不采用**（§8） |
| **browser-use/browser-harness** | **L2**（连接/自愈 harness） | L0（CDP） | Python | ⚠️ **登记为 L2 观察项**（§10） |

> **要点**：BrowserSkill **不是**"又一个 Playwright"。它把 L2 实现为**浏览器扩展内的 CDP 调用**，因此**既不需要自带浏览器二进制，也不需要远程调试端口**——这恰好落在本研究的 **P2 接入路径**上。

---

## 3. ⚠️ 本轮唯一实质技术细化：**R7 的适用范围必须收窄**

### 3.1 事实（`evidence/10` §4，五份官方原文穷举 grep 核验）

| 命题 | 判定 |
|---|---|
| Chrome 136 政策限制 `--remote-debugging-port` / `--remote-debugging-pipe` **在默认 data dir 上** | ✅ **不变**（`evidence/03` 官方原文） |
| BrowserSkill **完全不使用**远程调试端口（控制面 = 扩展内 `chrome.debugger`） | ✅ **成立**（零命中） |
| 因此**扩展路径**在 Chrome 136 之后**仍然可行** | ✅ **成立** |

### 3.2 R7 的**正确表述**（原表述限定于 CDP/Playwright 路线）

| | ❌ 原表述（过宽） | ✅ 细化后表述 |
|---|---|---|
| 内容 | "复用用户日常 Chrome profile 这条路**已被官方关闭**" | "**Chrome 136 关闭的是 `--remote-debugging-port` 在默认 data dir 上的使用**——即 **CDP / Playwright 路线**已被关闭。**扩展（`chrome.debugger`）是另一条通道，不受该政策约束**（BrowserSkill 为其现成证明）。" |
| 对 Curis 的指示 | （隐含）用户日常 Chrome 完全不可用 | **CDP 路线下**：Curis **必须**自持专用 profile（不变）。**扩展路线下**：技术上可附着用户 Chrome，**但 Curis 仍不采用**，理由是**隔离粒度**（§5），**不再是"官方禁止"** |

### 3.3 为什么这条细化**重要**（而非学术性措辞修正）

1. **它把一条"硬禁令"还原为"两条通道的取舍"** —— 避免后续评审以"Chrome 禁止"为由**误否**一个技术上可行的方案，也避免团队误以为"扩展路径 = 绕过官方限制"（**它是官方支持的正常机制**，不是绕过）。
2. **它改变了 P2 档的性质**：P2 从"理论上存在、实践上被 Chrome 封死"变为"**有现成 MIT 实现、可用**"（§4）。
3. **它同时暴露了 P2 的真实代价**：窗口级隔离**提供不了多 Business 所需的凭据罐隔离**（§5）——**这才是 Curis 不选 P2 的真正理由**。

---

## 4. 接入路径 P1 / P2 / P3 —— 细化后重述

> 依据：`CURIS_BROWSER_SESSION_AND_SECURITY_MODEL.md` §6「接入路径」+ 本轮 `evidence/10`。

| 档 | 形态 | Chrome 136 之后是否可行 | 参考实现 | Curis v1 判定 |
|---|---|---|---|---|
| **P1** | Curis **自启专用 profile**（Playwright `launchPersistentContext`） | ✅ **可行**（本就是政策要求的形态） | Playwright | ✅ **默认采用**（不变） |
| **P2** | **浏览器扩展**附加到**用户已有浏览器** | ✅ **可行**（⚠️ 本轮澄清：**不受** Chrome 136 调试端口政策约束） | **`Tencent/BrowserSkill`（MIT）** | ⚠️ **仍为显式例外，v1 不开放**——理由是**隔离粒度不足**（窗口级 ≠ 凭据罐级），**不是**"被禁止" |
| **P3** | 经**外部 CDP 端点**接入（`connectOverCDP`） | ⚠️ 取决于端点来源；若指向**默认 data dir** 则**不可行** | Playwright `connect_over_cdp` | ❌ **不推荐**（不变） |

### 4.1 P2 的**新增取舍矩阵**（供 CEO 裁定，见 §11）

| 维度 | P1（自启专用 profile，默认） | P2（扩展附加真实浏览器，BrowserSkill 形态） |
|---|---|---|
| License | Apache-2.0（Playwright） | **MIT**（BrowserSkill）✅ |
| 浏览器二进制 | 需自带（281MB）或复用系统 Chrome | **零**（复用用户已装 Chrome/Edge） |
| 登录态获取 | 用户在 Curis profile 内**重登一次** | **直接复用用户已在 Chrome 中的登录态** |
| **隔离粒度** | ✅ **凭据罐级**（每 Business × Platform 独立 profile） | ❌ **窗口级**（多窗口共享同一 cookie 罐） |
| **多 Business 支持** | ✅ **支持** | ❌ **不支持**（同平台多账号会互相覆盖） |
| 用户日常浏览干扰 | 无（独立窗口） | 低（**独立 Agent Window** + 借还需确认） |
| Stop Gate 可施行性 | ✅ 完全自控 | ⚠️ 可行（内置 human-in-loop），但**依赖扩展设置** |
| 新增攻击面 | CDP 调试端口（须严格管控，R14） | **loopback WS 监听（默认 52800）** + **扩展 origin 白名单** + 可选远程 WSS |
| 权限域 | CDP 全量（任意 JS / 任意网络 / 完整 Cookie 访问） | **21 个类型化 tool handler**（能力域化，**更窄**） |
| 凭据边界 | Curis 不解析 | **"Never extract credentials, cookies, tokens"** 为明文契约；**cookies 不出浏览器 profile** |
| 与 Curis v1 定位 | ✅ **完全一致**（单机本地自用 + 多 Business 隔离） | ⚠️ 需先解决"多 Business 隔离"缺口 |

**研究结论（非裁定）**：**P1 仍为默认**。P2 的价值在于**零二进制分发 + 复用已登录态**，但其**窗口级隔离与 Curis 的多 Business 前提冲突**。**建议 v1 不开放 P2**，**保留为 v1.5+ 的增强档**（届时须先定义"P2 下如何保证 Business 隔离"）。

---

## 5. 隔离原语的**层不同**（关键差异，须写入 L4）

| 维度 | BrowserSkill | Curis |
|---|---|---|
| 隔离载体 | **窗口级**：Agent Window + session 级 ref-store + borrow table | **凭据罐级**：`(business_id, platform_key)` 独立 profile 目录 |
| 底层 profile | **用户日常 Chrome profile**（"Website cookies stay in the user's browser profile"） | **Curis 专用 profile** |
| 跨 session 是否共享登录态 | **共享**（同一 profile ⇒ 同一 cookie 罐） | **不共享** |
| 并发模型 | 同 session 串行 / **跨 session 并行** / 跨浏览器 `--browser` | **同 profile 不可并发**（SingletonLock，R15） |
| 隔离目标 | 防**跨 session 的 ref 混淆与误写** | 防**跨 Business 的账号/数据串号** |

### 5.1 三条结论

1. **两者正交，不是替代** → **Curis 的 profile 级隔离仍然必需**（多 Business 是产品前提）。
2. **BrowserSkill 的"多 session 并行"不可移植到 Curis 多 Business 场景** → 并行窗口共享 cookie 罐，**若两个 Business 使用同一平台的不同账号，会互相覆盖登录态**。这是一个**新登记的负面结论**，可用于拒绝"照搬 BrowserSkill 并发模型"的提案。
3. **窗口级沙箱可作为 Curis L4 的增项**（§7）—— 它解决 Curis 现有设计**未表述**的一个问题：**同一 session 内 ref-store 的时效性与跨任务串扰**。

---

## 6. 业界收敛证据（本轮**最高价值**产出）

> 以下为**逐字原文**对照（来源：`evidence/10` §3、§6）。这是**独立第三方实现**对 Curis 既有契约的**复现级印证**，可用于提高评审置信度。

| # | Curis 既有契约 | BrowserSkill（`SKILL.md` 原文） | Jev Ultrafast（README 原文） | 收敛度 |
|---|---|---|---|---|
| **V1** | **凭据边界**：Curis 不知道/不处理/不导出 Password·Cookie·Token（§10.3） | **"Never extract credentials, cookies, tokens, or other secrets."** | "Owned tabs share the existing Chrome profile." + 模型输出不入可执行件 | ✅ **2/2** |
| **V2** | **Stop Gate**：遇 login/CAPTCHA/MFA 必须 STOP 并交人（R8） | **"With help enabled, request help for login, CAPTCHA, OTP, payment confirmation…"**；**"Respect rejection or the blocker; do not repeat the request."**；**"内置 human-in-loop"** | `BLOCKED` 为**一等动作**（8 个动作之一） | ✅ **2/2** |
| **V3** | **`EFFECT_UNKNOWN`**：写后未知**不得降级**为普通 failed、**不得盲目重试** | **`effect_state` (`none`/`committed`/`unknown`)**；**"an unknown effect is preserved across timeout or transport loss and must not be retried blindly"**；`borrow_outcome_unknown` → **"Do not bypass an outcome through another browser backend."** | 执行前重校验页面新鲜度与遮挡 | ✅ **1/1 + 1 部分** |
| **V4** | **独立 Verification**：不采信执行方自述完成 | 要求**结果验证与证据回写**；operation audit 为一等对象 | **"A `DONE` choice still requires independent outcome verification."** | ✅ **2/2** |
| **V5** | **Session 生命周期由 Curis 拥有**，**不依赖空闲超时** | **"Always run `bsk session stop <id>` on success and failure… Do not rely on idle cleanup"**；idle 5 min = **安全网** | — | ✅ **1/1** |
| **V6** | **范围即授权**：任务范围外的动作不得执行 | **"Stop at the requested goal; a trace grants no additional authorization."**；**"Never invent tab IDs or keep a user tab across unrelated work."** | "Only supported operations and targets are offered."（动作域收窄） | ✅ **2/2** |
| **V7** | **不得为"无人值守"绕过人工确认** | **"Deprecated `--unattended`, `--no-confirm`, and `BSK_REQUEST_HELP=off` cannot override these settings. Never change browser storage/settings to bypass them."**；用户设置**对所有会话具有最终决定权** | — | ✅ **1/1** |
| **V8** | **授权请求被拒后不得重试**（Gate 后 break 而非 continue） | **"Do not repeat pending, denied or timed-out borrows."**；`fill_value_mismatch` → **"no blind refill"** | — | ✅ **1/1** |

**判定**：**8 条契约中，7 条获得至少 2/2 或 1/1 的独立第三方原文印证**；无一条被第三方做法**否证**。
→ 这是本研究中**首次出现"第三方独立实现级收敛证据"**，其证据等级**高于此前的纯文档推理**。

> ⚠️ **引用纪律**：以上只能表述为**"业界收敛 / 独立印证"**，**不能**表述为"业界标准"或"已被证明正确"。第三方做法一致**不等于**正确，只说明**该设计不是 Curis 的独有偏好**。

---

## 7. 值得吸收的设计要点（**增项，不改变既有结论**）

| # | 可吸收点 | 来源 | 落到 Curis 的哪一层 |
|---|---|---|---|
| **A1** | **"显式借用 / 归还"语义**：操作他人（用户）已打开的页面必须显式声明，用毕归还 | BrowserSkill borrow table | **L4 Session** —— 补足 Curis 现有设计未表述的"对**用户既有页面**的操作授权"语义 |
| **A2** | **默认独立 Agent Window**：任务在自己的窗口执行，**不占用用户正在使用的窗口** | BrowserSkill | **L4 Session** —— 与 Curis"headed 可见可接管"一致，但**更明确**（不干扰用户） |
| **A3** | **同一 session 串行化 RPC（ref-store 安全）** | BrowserSkill | **L4 Session** —— 补足 **ref 时效性**问题（Curis 现有设计未表述） |
| **A4** | **能力域化的本地 RPC（21 个类型化 handler）优于裸 CDP 端口** | BrowserSkill | **L4 安全** —— 作为 R14（调试端口攻击面）的**缓解设计参考**：把"任意 JS/任意网络/完整 Cookie 访问"收窄为**类型化动作集** |
| **A5** | **`effect_state` 三态 + "取消不释放队列、改为有界补偿"** | BrowserSkill `architecture.md` | **L4 执行语义 / CGAP-03** —— 为 Curis 已裁定的 `EFFECT_UNKNOWN` 提供**队列层落地做法** |
| **A6** | **daemon 的 `daemon.lock` / `daemon.json` / trace log** | BrowserSkill `~/.bsk/` | **L4 可观测性** —— 与 Curis Evidence 契约同向 |
| **A7** | **扩展设置的用户最终决定权 + 废弃"跳过确认"参数** | BrowserSkill | **L4 Gate 治理** —— "**人工确认不可被自动化参数覆盖**"应写入 Curis Gate 设计 |

> **注**：A1–A7 **均为增项**，**不得**据此改写 Curis 既有 Frozen 结论；应在 Capability 立项时作为**设计输入**提交。

---

## 8. Jev Ultrafast 判定：**首版明确不采用**

### 8.1 三条独立理由（任一条已足够）

| # | 理由 | 依据 |
|---|---|---|
| **R1** | **能力边界与 Curis 主场景系统性不匹配** | 官方原文：**"Shadow roots, frames, canvas, uploads, pop-up tabs, nested scrolling, and arbitrary keyboard widgets remain outside this MVP."** —— 而创作者/经营后台（抖音创作者中心等现代 SPA）**大量使用** Shadow DOM（Web Components）、iframe（数据面板）、Canvas（趋势图）、**文件上传/导出**、新标签页。**主场景所需能力多数在其排除清单内** |
| **R2** | **引入第二个规划者 + 专有 SaaS 依赖** | 它是**带动作决策循环的 L3 Agent**（"A browser agent with a dynamic, indexed action space"），会与 Curis Employee 构成**两个规划者**（同 browser-use 整体的否决理由）；且硬依赖 **`TYPESAFE_API_KEY`（专有推理服务）**，与 Curis 四原则②"**能力可替换不写死**"存在张力 |
| **R3** | **成熟度不足** | **库龄 4 天**（created 2026-09-16）✔；官方自述为 **"outside this MVP"**、基准为 **"three repeats of one task on one browser profile, not a general reliability benchmark."** |

### 8.2 附带风险登记

| 项 | 说明 |
|---|---|
| Chrome 连接方式 | 明确要求 **"Allow remote debugging in Chrome when prompted"** 且 **"Owned tabs share the existing Chrome profile"** → **走 Chrome 136 收紧的那条路径**（`evidence/03`） |
| 商业指向 | README 顶部为 **Browser Use Cloud waitlist 引流**；该云即本研究已判定**与 CGAP-04 品类级冲突**的那一类 |
| 数字口径 | 视频"**450× / 3 分钱**"**无官方同口径数据**；官方口径为**协议调用 1,092 → 101（≈10.8×）**、**中位耗时 −25%** |
| 端口 | 本机 inspector `127.0.0.1:8766`（与本机"左脑"面板 8765 相邻，**同机部署存在竞争可能**——仅供登记） |

### 8.3 但**保留**两条正面价值

1. ✅ **"`DONE` ≠ 独立验收通过"** —— 可**直接引用**为 Curis 独立 Verification 原则的业界印证（V4）。
2. ✅ **"结构化动作空间 + 类型化选择"** 的分层思想 —— 与 Curis `Deterministic First / AI Recovery Second` **同向**：当未来启用**路线 B（AI 恢复）**时，应优先选择**"有限类型化动作 + 结构化选择"**形态，而非"自由文本规划"形态。**这是对 §7.4 路线 B 的一个正向设计输入。**

---

## 9. 不改变的结论（**全部维持**）

| # | 结论 | 本轮状态 |
|---|---|---|
| R1 | 不自建 Browser Engine | ✅ 不变 |
| R2 | Chromium 系（系统 Chrome / CfT） | ✅ 不变 |
| R3 | **Playwright 为 L2 主选**；`agent-browser` 为 R1.5 备选 | ✅ 不变（BrowserSkill **不构成** L2 主选替代，它是 **P2 接入形态**的参考实现） |
| R4 | **Local-first（v1）** | ✅ 不变 |
| R5 | headed 浏览器，用户可见可接管 | ✅ 不变（BrowserSkill 的"独立 Agent Window"**强化**之） |
| R6 | Curis 专用 persistent profile，`(business_id, platform_key)` 二维隔离 | ✅ **不变，且理由更清晰**（§5：窗口级隔离不足） |
| **R7** | Chrome 136：不能复用用户日常 Chrome 默认 profile | ⚠️ **细化适用范围**（§3）：**限定于 CDP/Playwright 路线**；扩展路径不受该政策约束 |
| R8 | Authentication Stop Gate（含全部禁止项） | ✅ 不变（且获 **V2/V7/V8** 独立印证） |
| R9 | Evidence 最小集合 | ✅ 不变（A5/A6 为增项） |
| R10 | Browser 与 Computer Use 并列，共享 Stop Gate 与 Evidence 契约 | ✅ 不变 |
| R11 | License 阻断项（AGPL-3.0 / GPL-3.0 / SSPL 等） | ✅ 不变（两个新项目均 **MIT**，**不在**阻断项内） |
| R12 | 云浏览器与 CGAP-04 品类级冲突 | ✅ 不变（Jev 的 README 引流云亦属该类） |
| R13 | 成本不是判据 | ✅ 不变 |
| R14 | `--remote-debugging-port` 是本机最大攻击面 | ✅ 不变（A4 提供**缓解设计参考**：类型化 RPC 优于裸端口） |
| R15 | SingletonLock：同 profile 不可并发 | ✅ 不变（BrowserSkill 在 **session 级**串行、**跨 session 并行**——但**其跨 session 并行不可移植**，见 §5.1） |

**一句话**：**本轮是候选集的扩充与一条适用范围的细化，不是技术选型的变更。**

---

## 10. 新增候选登记（增量）

| 优先级 | 项目 | License | 采用形态 | 本轮判定 |
|---|---|---|---|---|
| **P2 参考实现** | **`Tencent/BrowserSkill`** | **MIT** ✅ | **扩展驱动**的 L2（+ 窗口级 L4） | ✅ **登记为接入路径 P2 的参考实现 + 设计吸收源**；**v1 不启用** |
| 观察 | **`browser-use/browser-harness`** | **MIT** ✅ | L2（连接/自愈 harness） | ⚠️ 登记为 L2 观察项；**须核验其是否依赖远程调试端口**（其与 `jev-ultrafast` 同族，README 提示"Allow remote debugging"，倾向依赖） |
| **不采用** | **`browser-use/jev-ultrafast`** | MIT ✅ | L3（动作选择器） | ⛔ **首版不采用**（§8）；仅吸收 2 条设计输入 |

---

## 11. 待 CEO 裁定（**本轮增至 5 项**，原 4 项 + 新增 1 项）

| # | 待裁定 | 状态 |
|---|---|---|
| 1 | "自动化机制"层 UNKNOWN（U1/U3）的接受 | **不变**（第 2 轮提出） |
| 2 | **"平台官方导出 + Import" 与 "Browser" 的优先级** | **不变**（第 2 轮提出） |
| 3 | 会话材料是否纳入 Curis 凭据治理 | **不变**（第 2 轮提出） |
| 4 | Cloud 是否在 v1 开放 | **不变**（第 2 轮提出；本轮无改变其结论的新证据） |
| **5** | **接入路径 P2（扩展附加真实浏览器）是否在 v1 开放** | 🆕 **本轮新增**。研究建议：**v1 不开放**，且须先定义"**P2 下如何保证 Business 级凭据隔离**"；若开放，须同时裁定"**是否允许信任用户日常 Chrome profile**" |

---

## 12. 文档增量更新

| # | 文件 | 更新内容 |
|---|---|---|
| 1 | **新增** `evidence/10_BROWSERSKILL_AND_JEV_ULTRAFAST_SOURCE_REVIEW.md` | 两个项目 + `browser-harness` 的源码级核验（License / 活跃度 / 架构 / 契约原文 / 边界 / 数字口径） |
| 2 | **本文件（新增）** | 层定位、R7 细化、P1/P2/P3 重述、隔离原语对比、8 条收敛证据、7 条设计增项、Jev 判定、新增裁定项 |
| 3 | `CURIS_BROWSER_SESSION_AND_SECURITY_MODEL.md` | **接入路径 P1/P2/P3 表**更新（P2 可行性澄清 + 隔离粒度理由 + 参考实现）；R7 表述细化 |
| 4 | `CURIS_BROWSER_OPEN_SOURCE_DEEP_DIVE.md` | §6 新增候选（BrowserSkill / browser-harness / jev-ultrafast 及判定） |
| 5 | `CURIS_BROWSER_TECHNOLOGY_MATRIX.md` | L2 新增"扩展驱动"行；L3 新增"动作选择器型"行 |
| 6 | `CURIS_BROWSER_AUTOMATION_AND_AGENT_LAYER.md` | §2 新增分层判定（BrowserSkill = L2 扩展形态；Jev = L3 动作选择器）；§5 结论表新增行 |
| 7 | `RESEARCH_JOURNAL.md` | 新增 §7「第三轮：Addendum」 |
| 8 | `evidence/01_SOURCES_INDEX.md` | §A 新增 `10`；§B 新增来源；§C 新增核验行 |

**未修改**：`docs/` 下任何文件、Curis Runtime / Frontend / Backend / Authority / UI / HTML / Figma。**未 commit、未 push。**

---

```
BROWSER CAPABILITY ADDENDUM (BROWSERSKILL + JEV) COMPLETE — READY FOR CEO REVIEW
仅新增候选与细化 R7 适用范围；技术选型未变。
```
