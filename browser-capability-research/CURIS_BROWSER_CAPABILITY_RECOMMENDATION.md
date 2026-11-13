# CURIS BROWSER CAPABILITY RECOMMENDATION

Authority Class: **RESEARCH — 架构候选（非裁定）**
Status: **Draft — Ready for CEO Review（已过 Reconciliation 轮 + Addendum 轮）**
Date: 2026-09-18（原始）／2026-09-18 **Reconciliation 轮**／**2026-09-20 Addendum 轮**
Evidence: `evidence/01`–`evidence/10`

> **本文不修改 Curis 模型。** 所有"推荐"均为**研究假设**，最终需总控决策席裁定。
> 阅读顺序建议：本文件 §0 → §3（推荐架构）→ §6（MVP）→ §7（风险）。

## ⚠️ RECONCILIATION 声明（2026-09-18 第 2 轮，**先读**）

本文的**技术选型（§1–§5、§9）全部不变**；**问题定义、风险定性、MVP 与 Agent 层复杂度已被修正**。
**请以 `CURIS_BROWSER_USE_CASE_RECONCILIATION.md` 为准**阅读以下位置：

| 受影响位置 | 状态 | 说明 |
|---|---|---|
| §0「推荐 L3」／§1／§3 Agent Layer | ⚠️ **收紧** | 首版明确 **路线 A（纯 Playwright 确定性）**；Stagehand/browser-use 降为**有准入条件的后续可选**（RECONCILIATION §7） |
| §0「最大的风险」 | ⚠️ **修正** | 平台协议风险 **P0 → P1**；须区分 **A 类**（抓取公开/第三方内容）与 **B 类**（用户读自己后台） |
| §6 MVP | ⚠️ **重写** | 目标明确为 **Authorized Web Console Operation**；平台首选改为"用户实际拥有后台的平台"（RECONCILIATION §8） |
| §7 风险登记「P0 平台协议风险」 | ⚠️ **降级 P1** | 产品目的已被官方证据支持，仅"自动化机制"层为 UNKNOWN |
| §8 待裁定 #1 | ⚠️ **更新** | 从"接受或规避平台协议风险"改为"接受**机制层 UNKNOWN**"，并新增"A/B 优先级裁定" |
| §10 登记判定 | ⚠️ **更新** | 判定对象由"采集器"改为"**未授权**采集器"；B 场景已可登记 |
| **§1–§5、§9** | ✅ **完全有效** | 技术选型结构未因场景修正而变化 |

**先读 `CURIS_BROWSER_USE_CASE_RECONCILIATION.md`**（含 A/B 风险区分、MVP 重写、Agent 层定版）。

> ⚠️ **ADDENDUM 声明（2026-09-20 第 3 轮）**：**§0–§10 的推荐全部不变**（Playwright 主选 / Local-first / headed / 专用 profile / Stop Gate / 首版路线 A）。
> 新增：`Tencent/BrowserSkill`（**MIT**）登记为**接入路径 P2 的参考实现**（**v1 不启用**）；`browser-use/jev-ultrafast` **不采用**；**R7 适用范围细化**（Chrome 136 限 CDP/Playwright 路线，**扩展路径不受限**）；**§8 待裁定增至 4 项**。详见 `CURIS_BROWSER_ADDENDUM_2026-09-20_BROWSERSKILL_AND_JEV.md`、`evidence/10`。

---

## 0. 一页结论

| 问题 | 结论 |
|---|---|
| Curis 需要自建浏览器吗？ | **不需要。** 不自建引擎、不自建渲染表面。 |
| "内置浏览器"应拆成几层？ | **4 层，不可合并**（L1 呈现 / L2 操作 / L3 理解 / L4 状态）。 |
| L1 与 L2 是否分离？ | **必须分离**（macOS 上"可控制"与"可嵌入"互斥；权限成本差一个量级）。 |
| 推荐 L2 底座 | **Playwright（Apache-2.0）** 为主；**vercel-labs/agent-browser（Apache-2.0）** 为强备选（Rust，无 Node 依赖）。 |
| 推荐 L3 | **Curis 自建薄层，确定性优先 + 智能兜底**；**首版 = 路线 A（纯 Playwright 确定性，不引入 L3 智能层）**；评估 **Stagehand v4 本地模式** 仅作**后续可选**（RECONCILIATION §7）。 |
| 推荐 L4 | **Curis 自建**（profile 映射 + 二维隔离 + 有效性检测 + Stop Gate）。 |
| Local 还是 Cloud？ | **v1：Local-first。** Cloud 降为 Later / Provider。 |
| 成本是否判据？ | **不是**（两者都在可忽略量级）。 |
| 最大的风险 | 调试端口攻击面 / 平台风控误伤 / **平台协议风险**（⚠️ Reconciliation 后 **P0 → P1**：产品目的已被官方证据支持，仅"自动化机制"层为 UNKNOWN）。 |

---

## 1. 推荐架构（逐层选型）

| 层 | 推荐选择 | 类别 | 理由（一句话） |
|---|---|---|---|
| **L0 Browser Engine** | **Chromium**（Playwright 自带构建，或 **Chrome for Testing**，或用户已装 Chrome `channel:'chrome'`） | **Integrate** | Google 官方对自动化场景的推荐路径；BSD/Apache 类许可洁净。 |
| **L1 Embedded Surface** | **Playwright/agent-browser 启动的可见 headed 真实浏览器窗口**（**非**嵌入式 WebView） | **Integrate** | 同一实例 = 同一 profile = 同一会话 = 用户可随时接管。 |
| **L1' 只读预览** | Tauri `WebviewUrl::External`（可选，Later） | Integrate | 仅用于结果呈现；**不承担自动化**（WKWebView 不可被控制）。 |
| **L2 Automation Runtime** | **Playwright（Apache-2.0）** 主选；`channel:'chrome'` 省 281MB | **Integrate** | 最成熟、文档最全、生态最大、许可洁净。 |
| **L2 备选** | **vercel-labs/agent-browser（Apache-2.0, Rust）** | **Integrate（备选）** | **纯 Rust 直连 CDP，无 Node 依赖**；自带 a11y-refs 与 session 隔离。 |
| **L2 备选（扩展形态）** | **`Tencent/BrowserSkill`（MIT；Rust CLI/daemon + MV3 扩展）** | **Later（v1 不启用）** | **接入路径 P2 的参考实现**：复用用户已登录浏览器 + 独立 Agent Window + 借还语义 + 能力域化 RPC；⚠️ **隔离仅窗口级**，不服务多 Business。 |
| **L3 Agent Layer** | **Curis 自建薄层**；⚠️ **首版 = 路线 A（确定性步骤，无 L3 智能层）**；自愈仅作**有准入条件的降级路径** | **Build（薄）** | 编排权必须留在 Curis；经营数据要求可复现。 |
| **L3 增强（后续可选）** | **Stagehand v4 本地模式（MIT）** | Integrate（**首版不用**） | `observe()` **凭据不进模型** + 自愈；有 Python SDK。 |
| **L3 借鉴** | **Playwright MCP 的工具集设计（Apache-2.0）** | 借鉴 | 工具粒度与 a11y 接地方案的成熟范式。 |
| **L4 Session/Profile** | Curis 自建：`(business_id, platform_key)` 二维 profile 目录 | **Build** | 隔离粒度必须由 Curis 定义。 |
| **L4 Auth Stop Gate** | Curis 自建（信号集合 + checkpoint + Resume） | **Build** | **所有框架均无 Pause/Resume 原语**。 |
| **L4 Evidence** | Curis 自建（结构化数据 + 关键截图 + trace） | **Build** | Evidence 的业务语义只有 Curis 知道。 |
| **L5 Cloud Provider** | **不作为 v1 默认**；保留接口位 | **Later / Provider** | 与 CGAP-04 品类级冲突。 |
| **Computer Use（CGAP-02）** | 与 Browser **并列 Provider**，共享 Stop Gate 与 Evidence 契约 | **Later** | macOS 权限成本高一个量级；不应合并。 |

### 1.1 Build / Integrate / Provider / Later 汇总

| 项 | 判定 |
|---|---|
| Browser Engine、渲染、DevTools 协议 | **绝不 Build** → Integrate |
| L1 呈现 | **Integrate**（且不为自动化自建表面） |
| L2 操作 | **Integrate**（Playwright / agent-browser） |
| L3 理解与规划 | **Build（薄）** + 可选 Integrate（Stagehand） |
| L4 会话 / 隔离 / Stop Gate / Evidence | **Build** |
| Cloud Browser | **Provider**（Later） |
| Computer Use | **Later**（独立 Provider） |
| 自建 HTML 渲染引擎 / 自建浏览器 | **明确不做** |

---

## 2. 三个候选方案（用户第 16 节要求至少 3 套）

### Option A — Local-first（**推荐**）

```
Browser Engine      Chromium（系统 Chrome via channel:'chrome'，或 Chrome for Testing）
Embedded Surface    Playwright 启动的可见 headed 窗口（非嵌入式 WebView）
Automation Runtime  Playwright (Apache-2.0)  ／ 备选：agent-browser (Apache-2.0, Rust)
Agent Layer         Curis 自建薄层；首版 = 路线 A（纯 Playwright 确定性，无 L3 智能层）
Session/Profile     本机 profile 目录，(business_id, platform_key) 二维隔离
Evidence            结构化数据 + 元素级截图 + URL/title/时间/日期范围 + Trace
Permission          仅 Files&Folders / Local Network；**无需 TCC 无障碍与录屏**
Human Gate          Curis 自建 Stop Gate + checkpoint + Resume
```
**优势**：CGAP-04 完全自控；会话不出本机；用户可接管；风控概率最低；许可全部洁净；成本≈$0。
**代价**：后台长任务依赖 Mac 在线；profile 目录增长需回收策略；调试端口需严格管控。
**适配度**：**与 Curis「单机本地自用 v1」定位完全一致。**

### Option B — Cloud-first（**不推荐用于 v1**）

```
Remote Browser      Browserbase / Steel / 其他
Automation          Provider SDK
Surface             Curis 内 live view
```
**优势**：后台无人值守；无需分发浏览器体积；并发弹性。
**阻断性问题**：
1. **CGAP-04 品类级冲突**（主流厂商以自动解 CAPTCHA / 自动重登+MFA / 指纹伪装为卖点，已独立复核）。
2. 会话材料离开本机（数据保留期 7–30 天）。
3. 数据中心 IP + 指纹不一致 → **风控概率上升**。
4. 用户接管登录体验不可控。
5. 云侧 profile sync **有损**（仅 cookie，不含 localStorage/IndexedDB/扩展）→ 现代 SPA 后台大概率要重登 → **自身抵消了"无人值守"优势**。

### Option C — Hybrid（**否定其常见形态**）

用户设想的形态是"普通个人账号走 Local、后台长任务走 Cloud、敏感平台走 Local"。
**本研究明确否定这一形态**，理由是它会制造一个比两个纯方案都更差的状态：

1. **同账号双环境登录** —— 同一账号在两个 IP、两套指纹下登录，是**最典型的"异常登录"模式**，主动升高风控与账号安全风险。
2. **CGAP-04 无法统一承诺** —— Local 侧可保证"遇验证即停"，Cloud 侧取决于 Provider 默认行为 → **安全合同被削弱为"取决于路径"**，而用户无法在 UI 上理解这个差异。
3. **权威会话归属不清** —— 哪一侧持有权威登录态？切换时如何防止串号？复杂度高但收益不明确。

**若未来确需 Hybrid**，唯一可接受的形态是：
> **Cloud 仅承载"无登录态"或"官方 API 已授权的只读任务"**，且**禁止与 Local 共享同一账号的登录态**；并且必须在接入层**显式关闭** Provider 的 captcha/自动重登/指纹能力。

---

## 3. 推荐技术栈（直接回答用户第 17 节）

| 用户列出的项 | 推荐 | Build / Integrate / Provider / Later |
|---|---|---|
| **Browser Engine** | Chromium（系统 Chrome 或 Chrome for Testing） | Integrate |
| **Embedded Surface** | 可见 headed 真实浏览器窗口（**不是** WebView） | Integrate |
| **Automation Runtime** | **Playwright（Apache-2.0）**；备选 **agent-browser（Apache-2.0, Rust）** | Integrate |
| **Agent Layer** | Curis 自建薄层；⚠️ **首版 = 路线 A（纯 Playwright 确定性，无智能层）** | **Build** |
| **Session / Profile** | Curis 自建；`(business_id, platform_key)` 二维目录 | **Build** |
| **Evidence** | Curis 自建；结构化数据 + 元素级截图 + trace；**不存 DOM 全文** | **Build** |
| **Permission** | 最小必要：Files&Folders / Local Network；**调试端口仅绑 127.0.0.1 + 随机端口 + 短生命周期** | **Build** |
| **Human Gate** | Curis 自建 Stop Gate（fail-closed）+ checkpoint + 重校验 Resume | **Build** |
| Cloud Browser | 仅保留接口位 | **Later / Provider** |
| Computer Use | 并列 Provider | **Later** |

### 3.1 L2 主选与备选的取舍（Playwright vs agent-browser）

| 维度 | Playwright | agent-browser |
|---|---|---|
| License | Apache-2.0 ✅ | Apache-2.0 ✅ |
| 语言/运行时 | TS 核心 + 多语言绑定，**Python 仍需 Node 驱动** | **纯 Rust CLI + Rust daemon，直连 CDP，无 Node** |
| 成熟度 / 生态 | 极高（96k stars，官方文档极全，企业级） | 高增长（42.8k stars，活跃）但**属 Vercel Labs 实验项目** |
| 默认浏览器 | 自带 Chromium（281MB） | **Chrome for Testing**（与 Chrome 136 官方建议一致） |
| 页面表征 | a11y `ariaSnapshot()`（含 `mode:'ai'`） | **a11y 树 + refs（确定性元素选择）** + 标注截图 |
| 会话隔离 | 多 context / 多 profile（**需自行编排**） | **`--session` 原生多隔离实例**（各自 cookie/storage/auth） |
| 会话持久 | `launchPersistentContext` | `--restore` + 稳定 `--session` 自动存取 cookie/localStorage |
| MCP | 官方 `playwright-mcp` | 内置 `mcp` 子命令（stdio） |
| 主要风险 | Node 依赖；1.x 绑定浏览器修订（升级即换浏览器） | **`labs` 项目continuity风险**（参考 `bytebot-ai/bytebot` 已归档） |

**建议**：**以 Playwright 为 R1 主选**（成熟度与文档是企业可用性的底线），**将 agent-browser 列为 R1.5 备选并作技术验证**——其"**纯 Rust、无 Node 依赖**"对 Tauri 栈是实质优势，且其 **`--session` 原生隔离**与 Curis 的二维隔离模型高度同构。**不建议把 agent-browser 作为唯一底座**（labs 项目的存续风险需要观察窗口）。

---

## 4. 与 CGAP-04 的一致性自检（逐项）

| CGAP-04 要求 | 本推荐架构如何满足 |
|---|---|
| 遇登出/验证/风控**必须 STOP** | Curis Stop Gate（fail-closed）；**不集成任何 captcha-solving / 自动重登 / MFA 代填 / stealth** |
| **保存执行位置** | checkpoint：run_id / step_index / url / title / observed_at / (business, platform, profile) 三元组 / 已完成与待执行步骤 |
| **创建 Human Gate** | Curis 内显式 Gate 记录（类型 = AuthRequired，附命中的具体信号） |
| **通知用户** | Curis 内呈现；**不使用飞书**（飞书仅升级事件） |
| 禁止重复尝试登录 / 猜密码 / 循环提交 | Gate 创建后**不得再发任何导航或提交**；循环必须 `break` 而非 `continue`；无凭据猜测代码路径 |
| 禁止绕 CAPTCHA / MFA / 切账号试探 / 规避风控 | 不集成对应能力；profile 与 Business 强绑定，不允许运行时切号 |
| **Resume from safe checkpoint** | 恢复前**重校验三元组一致（防串号）+ 重校验登录态真实有效**；从 step_index 继续；记录 resume 事件到 Evidence |

**关键前提**：本推荐之所以能满足全部要求，正是因为选择了 **Local-first + 自持 profile + 可见 headed 窗口 + 不启用云侧规避能力**。若选择 Cloud-first 或启用 stealth，**上述自检将逐项失效**。

---

## 5. 成本（已核验部分）

| 方案 | 月成本（30 次/日 × 3 分钟 = 45 浏览器小时/月） |
|---|---|
| **Local（推荐）** | **≈ $0**（含零增量体积路径：`channel:'chrome'` 复用系统 Chrome） |
| Browserbase Developer | ≈ $20（$20/mo 含 100 小时，不触发超额） |
| browser-use Cloud | ≈ $0.9（$0.02/浏览器小时） |

**结论**：成本**不构成判据**。
**并须注意其反面含义**：**browser-use Cloud 是最便宜的选项，同时是最不适配 CGAP-04 的选项**（自带 stealth + CAPTCHA solving）。**价格与"该不该用"无关。**

**本地的一次性成本**：Playwright + Node 驱动（若用 agent-browser 则为 0）；浏览器二进制 281MB（可用 `channel:'chrome'` 规避）。

---

## 6. 最小可实现版本（MVP，回答用户第 18 问）

> ⚠️ **本节已被 Reconciliation 重写** —— 最新定义见 `CURIS_BROWSER_USE_CASE_RECONCILIATION.md` §8（14 步流程）。**关键变更**：
> ① 目标由"经营数据采集"明确为 **Authorized Web Console Operation**；
> ② 平台首选**不再以"官方 API 优先"为主体**（个人主体对官方 API 不可得），改为**直接选一个用户实际拥有后台的平台**；
> ③ **Agent 层明确路线 A（无 L3 智能层）**；
> ④ **第 11–14 步（制造 Session 失效 → 必须 STOP → 重新登录 → Resume）为"必过"的首要验收项**。
> 下表保留原始形态供对照。

**目标**：用一个**最小、可验证、不触碰红线**的闭环，证明"AI Employee 能在用户授权下读取自己账号的经营数据并写回 Curis"。

| 项 | MVP 定义 |
|---|---|
| **平台范围** | **1 个**（⚠️ Reconciliation 修正：**直接选一个用户实际拥有后台的平台**；"优先微信公众号 `datacube` 官方 API"因**个人主体无可得资质**，不构成 MVP 主体） |
| **Business 范围** | **1 个** |
| **路径类型** | **确定性步骤脚本**（无 L3 智能层、无自愈） |
| **浏览器** | **系统 Chrome (`channel:'chrome'`)** + **Curis 专用 profile 目录** → 省 281MB，满足 Chrome 136 政策 |
| **可见性** | **headed（用户可见）** |
| **登录** | **用户手工登录一次**（Curis **不做**任何自动登录） |
| **登录态** | `launchPersistentContext`，单 profile，**不并发**（规避 SingletonLock） |
| **Stop Gate** | **必做**：最小信号集合（登录页出现 / 401 / 验证码容器 / "验证"/"频繁"文案）+ checkpoint + 用户通知 |
| **Evidence** | 截图（元素级）+ URL + title + 观测时间（含时区）+ **采集日期范围** + 结构化 JSON |
| **写回** | 写入 Curis Result（走既有 Result Intake 三模式中的 `MANUAL_ENTRY` 或 `IMPORT`，**不新建体系**） |
| **明确不做** | ❌ 无 Cloud ❌ 无并发 ❌ 无 stealth ❌ 无 captcha-solving ❌ 无 L3 智能规划 ❌ 无 Computer Use ❌ 无多平台 |
| **验收判据** | ① 用户能看到浏览器并完成登录；② 能采集到**一次真实经营数据**并写回；③ 制造一次"未登录"状态，**系统必须停下并生成 Gate**，不得自我重试；④ Evidence 可追溯（能回答"这个数字是几点、从哪个页面、哪个日期范围来的"） |
| **是否需先过 CEO** | **是。** MVP 立项前须完成 §7 的三项前置裁定。 |

---

## 7. 风险登记（回答用户第 17 问）

| 级别 | 风险 | 说明 | 缓解 |
|---|---|---|---|
| **P1**（⚠️ Reconciliation 由 P0 降级） | **平台协议风险** | **必须区分两类行为**：**A 类**（抓取公开/第三方内容）→ 抖音 5.1 明文禁止，**Curis 不采用**；**B 类**（用户在自有账号、经自己的后台读取平台已向该用户展示的数据）→ **产品目的被官方承认**（抖音官方文档明示支持"用户授权后在第三方系统查看自己数据"，`evidence/09`）；**仅"自动化机制"层为 UNKNOWN**（U1/U3）。 | **登记 UNKNOWN 交法务/官方闭环**（不断言禁止、不断言允许）；优先**平台官方导出 + Curis Import** 这条更干净路径；浏览器路径默认停在 Review Gate；不承诺端到端无人发布。见 RECONCILIATION §9。 |
| **P0** | **调试端口攻击面** | `--remote-debugging-port` 等价于"任意 JS 执行 + 任意网络请求 + 完整 Cookie 访问"。 | 仅绑 `127.0.0.1`；随机端口；短生命周期；会话结束即关；**绝不暴露 LAN**。 |
| **P1** | **平台风控误伤** | 新 profile = "新设备"，首次登录中文平台易触发验证；**且关联设备可能被永久拉黑**。 | 用户可见 + 低速 + 非并发；遇验证即停；**不采用 stealth 规避**；把风控视为合法结果上报。 |
| **P1** | **凭据治理缺口** | profile 内会话材料**必然落盘**，现有"凭据不落明文"规则**未覆盖这一类**。 | **须新增裁定**（纳入凭据治理 / 落盘形态 / 是否出境 / 删除语义）。 |
| **P1** | **Profile 目录增长** | 每 `(business, platform)` 一个目录。 | 闲置回收策略（需用户确认）；在 UI 明示磁盘占用。 |
| **P2** | **SingletonLock 并发限制** | 同 profile 不可双实例。 | 多 profile 或串行；纳入 Automation Queue 设计。 |
| **P2** | **Playwright 版本钉死** | 升级 Playwright = 换底层浏览器 → 可能改变被自动化站点行为。 | 纳入回归测试闸。 |
| **P2** | **Node 运行时依赖** | Playwright Python 仍需 Node 驱动。 | 评估 agent-browser（纯 Rust）作为替代。 |
| **P2** | **Evidence 膨胀** | Trace / video 体积大。 | 保留策略 + 定期清理；**不存 DOM 全文**。 |

---

## 8. 待 CEO 裁定的四项前置事项（第 3 轮新增第 4 项）

| # | 待裁定 | 为什么必须先定 |
|---|---|---|
| **1** | **"自动化机制"层 UNKNOWN（U1/U3）的接受**，以及 **"平台官方导出 + Import" 与 "Browser Capability" 的优先级** | A/B 已区分，**产品目的层面已被官方承认**；剩余为机制层 UNKNOWN，须由总控决策席显式登记"已接受"。优先级裁定见 RECONCILIATION §6.2。 |
| **2** | **"浏览器会话材料"是否纳入 Curis 凭据治理体系**（及落盘形态/是否出境/删除语义） | 与既有硬约束"凭据不可能明文落盘"存在结构性缺口，不补则该 Capability 违反既有安全基线。 |
| **3** | **Cloud Browser 是否在 v1 开放** | 本研究建议 v1 **不开放**；若 CEO 要求开放，必须在接入层显式关闭规避类能力，并需先完成"可关闭性"验证（当前未验证）。 |
| **4** 🆕 | **接入路径 P2（扩展附加真实浏览器）是否在 v1 开放** | 研究建议 **v1 不开放**。P2 在 Chrome 136 之后**技术上可行**（扩展路径 `chrome.debugger` **不受**调试端口政策约束；参考实现 `Tencent/BrowserSkill`，MIT），**但隔离仅窗口级、无法服务多 Business 凭据罐隔离**。若开放，须先定义"**P2 下如何保证 Business 级凭据隔离**"，并裁定"**是否允许信任用户日常 Chrome profile**"。详见 `CURIS_BROWSER_SESSION_AND_SECURITY_MODEL.md` §2.1、`evidence/10` §4–§5。 |

---

## 9. 后续 Computer Use 研究缺口（回答用户第 19 问）

见 `CURIS_BUILT_IN_BROWSER_CAPABILITY_STUDY.md` §11 第 19 问。摘要：
macOS 合成键鼠/截屏的**授权成功率与失效频率实测**；**视觉接地模型选型**（OmniParser 的 **CC-BY-4.0 + 权重条款**问题未解）；**cua / Lume 在 Apple Silicon 上的资源与授权代价**；**GUI 级 CGAP-04 的检测信号定义**（远难于浏览器）；**macOS 版本升级对 TCC 的回归影响**；**OpenAdapt 的 "VERIFIED 才报告" 机制能否迁移为 Computer Use 的 Evidence 契约**。

---

## 10. 是否可登记为正式 Capability Gap 解决方案候选（回答用户第 20 问）

**结论：可以登记为候选，但必须收窄定义（⚠️ Reconciliation 后概念性障碍已消除）。**

| 若定义为 | 结论 |
|---|---|
| "绕过平台限制的**未授权**采集器 / 通用爬虫" | ❌ **不应登记**（与 §7 风险登记冲突） |
| "**Authorized Web Console Operation**：AI Employee 对**用户本人已授权**的 Web 后台的操作能力（读取平台已向该用户展示的经营数据）" | ✅ **可以登记为候选** |

**登记前置条件**（⚠️ Reconciliation 更新，见 RECONCILIATION §15 第 15 问）：① **U1/U3 法务或官方确认**（自动化机制在自有后台场景的定性）；② 会话材料凭据治理裁定；③ **"官方导出 vs Browser"优先级的 CEO 裁定**；④ MVP（RECONCILIATION §8）验收通过；⑤ 命名正式变更走文档流程。

**当前状态**：
```
BROWSER CAPABILITY USE CASE RECONCILED — READY FOR CEO REVIEW
场景与风险定性已修正；技术选型未变。尚未登记为正式 Capability。
```
