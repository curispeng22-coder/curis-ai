# CURIS BROWSER LOCAL / CLOUD / HYBRID OPTIONS

Authority Class: RESEARCH
Status: Draft（已过 Reconciliation 轮）
Collected: 2026-09-18（原始）／2026-09-18 **Reconciliation 轮**
Evidence: `CURIS_BROWSER_TECHNOLOGY_MATRIX.md` §6、`evidence/04`、`evidence/05`、`evidence/07`、**`evidence/09`**

> 用户明确要求：**不要预设答案**。本文件先给判据，再给测算，最后给结论候选。

> ⚠️ **RECONCILIATION 声明（第 2 轮）**：本文的 **Local/Cloud 判据与结论全部不变**（v1 推荐 Local-first；Cloud 降为 Later/Provider；否定 Hybrid 常见形态）。
> **场景修正使 Local-first 的论证更强**：主场景为 **Authorized Web Console Operation**（AI Employee 进入用户**本机已登录**的自有后台读取经营数据），其"会话不出本机 + 用户可接管"的天然属性与 Local-first **完全同构**，会话材料出境在语义上更无必要（新增论据见 §5.1 第 5 条）。
> 同时，平台官方**导出文件 + Curis Import** 构成一条**零协议张力**的更干净替代路径（`evidence/09` §5、RECONCILIATION §6.2）。

---

## 1. 判据（先定标准，再比方案）

| # | 判据 | 为什么它是判据 |
|---|---|---|
| C1 | **会话材料在谁手里** | 直接决定凭据边界与隐私（`evidence/06` §7 新裁定的核心） |
| C2 | **与 CGAP-04 是否相容** | 云厂商主流卖点是"自动解 CAPTCHA / stealth"，与"遇验证即停"冲突（已独立复核） |
| C3 | **平台风控触发概率** | 数据中心 IP + 指纹与日常环境不一致 → 异常登录概率**上升**（`evidence/05`） |
| C4 | **用户可见性 / 可接管性** | CGAP-04 的 Resume 依赖"用户能在同一浏览器里完成登录" |
| C5 | **本地资源可及性** | 本地文件、本地网络、本地已装工具 |
| C6 | **后台长任务可行性** | 用户不主动打开时能否完成采集 |
| C7 | **成本** | 需实测，不可凭印象 |
| C8 | **可合法集成与分发** | License 阻断项（`evidence/02`） |

---

## 2. 成本测算（本目录自行推演，假设显式列出）

### 2.1 假设（Curis v1 典型负载）
- 每日 **30 次**采集任务
- 每次任务 **3 分钟**浏览器时间
- → 每日 90 分钟 = **45 小时/月**

### 2.2 云端成本（仅用**已独立复核**的价格；其余不参与计算）

| Provider | 计算 | 月成本 |
|---|---|---|
| **Browserbase Developer** | $20/mo 含 100 浏览器小时 > 45h → **不触发超额** | **≈ $20/月** |
| **Browserbase Free** | 1 浏览器小时 + 15 分钟/session 上限 + 3 并发 → **不够用** | 不可行 |
| **Browserbase Startup** | $99/mo，明显超出需求 | $99/月（过度） |
| **browser-use Cloud** | README 原文自述 **$0.02/浏览器小时** → 45h × $0.02 | **≈ $0.9/月** |
| Steel / Browserless / Cloudflare / 其他 | **价格未独立复核（`△转述`）**，或厂商定价页未返回价格（`steel.dev/pricing` 实际返回首页） | **不予测算，避免臆测** |

> **结论（重要）**：在已核验数据下，云端成本量级为 **$0.9 ~ $20/月**。
> 这是一个**可以忽略**的金额。因此：
> **C7（成本）不是决策判据，且任何以"云更便宜/本地更便宜"为由的论证都不成立。**
> 尤其注意：**browser-use Cloud 的 $0.02/浏览器小时是全场最低**——而它恰恰是**最不适配 CGAP-04** 的选项（自带 stealth + CAPTCHA solving）。
> 这个反差本身就是本轮最有力的证据：**"能用"与"该用"是两个完全不同的问题。**

### 2.3 本地成本

| 项 | 量级 | 说明 |
|---|---|---|
| 货币边际成本 | **≈ $0/月** | 使用用户自有 Mac 算力 |
| 一次性分发体积 | **+281MB**（Chromium）/ **+180~187MB**（若含 WebKit/Firefox） | `evidence/07` §4；**可规避**：`channel:'chrome'` 复用系统 Chrome → **0 增量** |
| 运行时依赖 | **+Node 驱动** | Playwright Python 仍依赖 Node 驱动（`evidence/07` §4） |
| 内存 | 每 context/page 独立进程模型；**未取得权威单值** | 标为待实测 |
| 磁盘（profile） | 每 `(business, platform)` 一个目录 | 随 Business 数增长；需闲置回收策略 |
| 电力 | 可忽略 | — |

**关键发现**：本地方案**存在一条 0 增量体积路径** —— 用 `channel:'chrome'` 驱动用户**已安装**的 Chrome，不下载 Playwright 浏览器构建。代价是失去"版本钉死"的可预测性。

### 2.4 成本结论
**C7 不构成区分度**：云端 ≈$20/月，本地 ≈$0/月，但两者都在"可忽略"量级，且本地需承担 Node 运行时与工程复杂度。
→ **决策必须由 C1–C6 决定，不能由 C7 决定。**

---

## 3. 逐判据对比

| 判据 | Local Browser | Cloud Browser |
|---|---|---|
| **C1 会话材料位置** | ✅ 全程留在本机 profile 目录 | ⛔ 会话材料需迁移/注入 Provider，**离开本机**（多数 Provider 有 7–30 天数据保留期） |
| **C2 CGAP-04 相容** | ✅ **完全自控**，我方可实现"遇验证即停" | ⛔ **品类级冲突**：Browserbase（Auto captcha solving / Stealth Mode）、Steel（Auto CAPTCHA solving / fingerprinting / Auto Sign-In）、Anchor（自动重登+MFA）、Hyperbrowser（指纹随机化）均以规避风控为卖点（Browserbase 与 Steel 已**独立复核**） |
| **C3 平台风控** | ⚠️ 中：设备指纹"新 profile"仍属新设备，但**环境（IP、时区、字体、系统）与用户日常一致** | ⛔ **更高**：数据中心 IP + 指纹与日常不一致 → "异常登录"更易触发 |
| **C4 可见性/可接管** | ✅ **天然满足**：headed 真实窗口，用户可直接接管完成登录（这是 CGAP-04 Resume 的实现前提） | ❌ 需 Provider 的 live view / 交互通道；**用户接管体验不可控** |
| **C5 本地资源** | ✅ 完整访问（本地文件、本地网络、已装软件） | ❌ 无 |
| **C6 后台长任务** | ⚠️ 依赖 Mac 唤醒；休眠/关机中断 → 需任务恢复机制 | ✅ **优势明确**：不依赖用户设备在线，可长时间后台运行 |
| **C7 成本** | ≈ $0/月 | ≈ $20/月（已核验档位） |
| **C8 合法集成** | ✅ 全部组件 License 洁净（Playwright Apache-2.0 等） | ⚠️ Provider 自带 License/条款；Browserless 自托管不可闭源用 |

### 3.1 云端会话迁移是**有损**的（首手证据）

browser-use README 原文（`evidence/08` §A.4）：
> "**Profile sync transfers cookies, not local storage, IndexedDB, or extensions. Some sites may require you to sign in again.**"

**含义**：现代平台后台普遍把登录态放在 localStorage（SPA + JWT），**云侧迁移后大概率需要重新登录**。
而"重新登录"意味着**再次触发 CGAP-04 的 Human Gate** —— 云方案的"后台无人值守"优势被自身削弱。
→ **C1 与 C6 在这里互相抵消**：云强于 C6（在线性），弱于 C1（会话迁移损失 + 材料出境）。

### 3.2 用户接管体验（C4）的进一步说明

CGAP-04 的 Resume 必须由**用户完成登录**。本地路径下这极其自然：**浏览器窗口就在用户桌面上，用户直接点进去登录**，Curis 只需轮询状态。
云端路径下，用户必须通过 Provider 的 live view / 交互通道登录——**体验、可用性、以及"用户是否真的愿意在第三方面板里输入验证码"都是未知数**。
→ C4 是 Local-first 的**第二个强论据**（仅次于 C2）。

---

## 4. 三个方案

### Option A — Local-first

```
Browser Engine      Chromium（Playwright 构建，或系统 Chrome via channel:'chrome'）
Embedded Surface    Playwright 启动的可见 headed 窗口（非嵌入式 WebView）
Automation Runtime  Playwright（Apache-2.0）
Agent Layer         Curis 自建薄层；首版 = 路线 A（纯 Playwright 确定性，无 L3 智能层）
Session/Profile     本机 profile 目录，(business_id, platform_key) 隔离
Evidence            截图 + URL + 标题 + 观测时间 + 提取数据 + Trace
Permission          仅需 Files&Folders / Local Network；**无需 TCC 无障碍与录屏**
Human Gate          Curis 自建 Stop Gate + checkpoint + Resume
```
- **优势**：C1/C2/C3/C4/C5/C8 全优；与 Curis「单机本地自用 v1」定位一致；与既有"凭据不落明文"的治理方向可收敛。
- **代价**：C6 弱（依赖 Mac 在线）；profile 目录增长；Node 运行时与浏览器体积（可部分规避）。
- **最大未解风险**：`--remote-debugging-port` 成为本机新攻击面，必须严格管控（`SESSION_AND_SECURITY_MODEL` §7.1）。

### Option B — Cloud-first

```
Remote Browser      Browserbase / Steel / 其他
Automation          Provider SDK（Playwright 兼容）
Surface             Curis 内渲染 live view（帧流或 Provider 嵌入）
```
- **优势**：C6 强；无需分发浏览器体积；并发弹性好。
- **致命问题**：**C2 品类级冲突**（已独立复核）；C1 会话材料出境；C3 风控概率上升；C4 接管体验不可控。
- **若要强行采用**：必须在接入层**显式关闭** captcha 求解 / 自动重登 / MFA 代填 / 指纹随机化 / stealth，且需逐一确认可关闭性——**Browserbase 与 Steel 的官网能力清单已明示其提供这些能力**，需确认能否按项目关闭。

### Option C — Hybrid

```
默认（个人账号 / 敏感平台 / 需要人工登录 / 需本地资源） → Local
后台长任务（用户设备不可用 / 大批量 / 无人值守）        → Cloud
```
- **优势**：保留 C6 弹性。
- **隐患（必须登记）**：
  1. **一致性风险**：同一平台在 Local 与 Cloud 两处各有一份会话 → **账号安全与风控风险叠加**（两套设备指纹、两个 IP 登录同一账号，是最典型的"异常登录"模式）。
  2. **CGAP-04 无法统一**：Local 侧可保证"遇验证即停"，Cloud 侧取决于 Provider 默认行为 → **安全合同被削弱为"取决于路径"**，用户在 UI 上无法理解差异。
  3. **状态同步复杂**：哪条路径持有"权威会话"？切换时如何保证不串号？

---

## 5. 结论候选（研究假设，非裁定）

### 5.1 对 v1（单机本地桌面自用）
**推荐 Option A（Local-first）** —— 但它不是"因为便宜"，而是：
1. **C2 决定性**：云浏览器品类的主流商业定位（规避风控）与 CGAP-04（遇验证即停）**结构性冲突**。这是本轮最强的排除性理由，且已被独立复核。
2. **C1/C4 强约束**：会话材料不出本机 + 用户可接管，是 CGAP-04 Resume 的实现前提。
3. **C3**：本地环境与用户日常一致，风控概率低于数据中心。
4. Curis v1 定位为**单机本地自用**，云端方案的收益（弹性、无人值守）在 v1 场景中价值有限。
5. **（Reconciliation 补充）场景同构性**：主场景是"读取用户**自己的**后台"，**会话与数据天然属于本机、本账号**。把这类读取送上云，既无收益又新增"材料出境"这一**纯风险项**。→ **场景修正后，Local-first 不只是更优，而是与场景定义一致的唯一选择。**

### 5.2 但必须保留 Cloud 为 Provider，且收窄其用途
**不建议**把 Cloud 作为"另一个执行位置"，而应把它定义为**受严格约束的例外通道**：
- 仅用于：**官方 API 通道不可得、且平台风控对本地新 profile 明显不友好、且用户显式授权**的浏览器路径。
- 必须：显式关闭 Provider 的规避类能力；明确告知用户"页面数据将离开本机"；登记数据保留期。
- **不建议**在 v1 实现（登记为 Later / Provider，见 `CURIS_BROWSER_CAPABILITY_RECOMMENDATION.md`）。

### 5.3 明确否定的做法
- ❌ **"敏感平台走 Local、其他走 Cloud"的 Hybrid**：会造成同账号双环境登录，**主动升高风控与账号安全风险**，且使 CGAP-04 无法统一承诺。
- ❌ 为降低风控而启用 Provider 的 stealth / 指纹随机化：**与产品原则直接冲突**。

---

## 6. 未验证 / 待补

| 项 | 状态 |
|---|---|
| Steel / Browserless / Cloudflare / AWS / Kernel / Anchor 等**当期公开报价** | `△转述`，**未独立复核** → `steel.dev/pricing` 实际返回首页，价格未取得 |
| 各 Provider 的**规避类能力是否可按项目关闭** | **未验证**（这是 Hybrid/Cloud 能否成立的关键前提） |
| 本地运行 Chromium 的**内存实测值** | 未实测（未在本轮运行浏览器） |
| 中文平台对"新 profile 首次登录"的**风控触发阈值** | 只能定性（风险升高），**不可量化** |
| Mac 休眠期间任务恢复的具体机制 | 属 CGAP-03，本轮不展开 |
