# CURIS BROWSER USE CASE RECONCILIATION

**主场景纠正记录 — Authorized Web Console Operation**

Authority Class: **RESEARCH — RECONCILIATION**
Status: **Draft — Ready for CEO Review**
Date: 2026-09-18（Reconciliation 轮）
Supersedes（仅限 Problem Definition 部分）: `CURIS_BUILT_IN_BROWSER_CAPABILITY_STUDY.md` §8 的风险定性、§11 第 1/2/18 问
Retains: 上一轮全部技术结论（见 §4）

> 本轮**只**纠正 Problem Definition / Primary Use Case / Risk Interpretation / MVP。
> **未重做技术研究**，**未推翻** Playwright / Local-first / Profile / Stop Gate 等有效结论，**未开发**，**未修改** Curis Authority / Runtime / UI。
>
> ➡️ **后续轮次（第 3 轮 Addendum，2026-09-20）**：已就**新增候选**（`Tencent/BrowserSkill`、`browser-use/jev-ultrafast`）完成**源码级核验**，并**细化 R7 的适用范围**（Chrome 136 限 **CDP/Playwright 路线**；**扩展路径不受限**）。
> 见 `CURIS_BROWSER_ADDENDUM_2026-09-20_BROWSERSKILL_AND_JEV.md` 与 `evidence/10`。**本文（第 2 轮）的结论不受影响。**

---

## 1. 原误区是什么

上一轮研究（含我的报告）在**风险章节**把主场景表述为：

> ❌ "平台没有 API → Curis 用 AI Browser 去**抓取**平台/APP 信息"

这个表述在**技术上不错、在产品语义上错**。它造成三个连锁偏差：

| # | 偏差 | 后果 |
|---|---|---|
| **D1** | 把 Curis 的定位说成"**数据获取**"（获取行为），而非"**代为操作已授权界面**"（操作行为） | 团队会把它理解成一个**采集器**，进而讨论"反爬""覆盖度""抓取量" |
| **D2** | 把平台协议风险简单套用**"抓取公开/第三方内容"（A 类）**的结论 | 风险被**过度扩大**，可能直接否掉一个平台本身承认的产品目的 |
| **D3** | 没看到"**用户读自己后台**"是**平台自己就提供官方通道与官方导出功能**的场景 | 丢失了**API-first 的强论据**，也丢失了"官方导出 + Import"这条更干净的路 |

**根因**：上一轮把"外部平台执行"当成**单一场景**处理，没有区分
**"获取不属于我的数据"** 与 **"读取本来就展示给我的数据"**。
（`CURIS_BUILT_IN_BROWSER_CAPABILITY_STUDY.md` §8 的措辞与 §11 第 1/2 问需要被本节取代。）

---

## 2. 新主场景是什么

### 2.1 正式定义

> **Authorized Web Console Operation**
> 用户本人拥有平台账号 → 用户已正常登录对应创作者/经营后台 → 平台本身已提供经营数据中心 → **AI Employee 只是进入用户自己的后台**，导航到数据页面、选择账号/内容/时间范围、**读取平台已经整理好的指标**、必要时截图留 Evidence、结构化写入 Curis → 分析 → Learning → Next Cycle。

### 2.2 典型实例
抖音创作者中心（`creator.douyin.com`）｜汽水音乐创作者后台｜微信公众号后台｜其它 Creator Center / Seller Center / Analytics Dashboard / SaaS Console。

### 2.3 明确不是
通用爬虫｜公开页面批量抓取器｜反爬工具｜Stealth Browser｜CAPTCHA Solver｜风控绕过工具｜未授权数据采集器。

### 2.4 产品定义（建议正式采用）

```
Curis Browser Capability =
AI Employee 对【用户本人已授权】的 Web Workspace / Console 的操作能力
```

> **注意**：这里的"授权"，指的是**用户拥有该账号并已登录**，而**不是**指 OAuth Token。
> （OAuth 授权是另一条通道，见 §6 优先级；两者是不同层次的东西。）

---

## 3. 为什么这个纠正**强化**而非削弱了研究

这是本轮最重要的一点。修正后的场景**恰好被官方证据支撑**（`evidence/09`）：

**抖音官方文档原文**（`open.douyin.com/.../video-data-solution`）：
> "抖音帐号运营者或普通用户**完成授权后，可直接在第三方系统或应用内查看自己发布的抖音视频在一段时间内的统计数据**"
> "**唯一官方认证的对外开放的抖音数据，数据真实性高**"

→ **"用户在自己的授权下、通过工具查看自己的经营数据"这一产品目的，平台是官方承认并支持的。**

同时，官方通道的门槛是：
> **"仅限企业开发者，个人开发者无法调用"**（第三方技术解读，需官方复核）

**因此正确的因果链是**：

| 旧（不准确） | 新（准确，有证据） |
|---|---|
| 平台没有 API → 所以抓取 | **官方通道存在且被平台承认 → 但资质门槛（企业开发者）把个人主体系统性地排除在外 → 而用户本人的 Web Console 对其完全开放 → 所以操作 Console** |

→ **Browser Capability 的正当理由不是"绕过平台"，而是"使用用户实际拥有的那一个入口"。**
→ 这与既有 **PHASE 2 Provider Feasibility** 结论（"国内电商对个人主体系统性排除"）**相互印证**。

---

## 4. 哪些结论**保留**（完全有效，不因场景修正而改变）

| # | 结论 | 为何不受影响 |
|---|---|---|
| R1 | **不自建 Browser Engine**（Chromium 系） | 与场景无关，纯工程判断 |
| R2 | **Chromium 系**（系统 Chrome / Chrome for Testing） | 同上；Google 官方对自动化的推荐路径 |
| R3 | **Playwright 作为 L2 主候选**（Apache-2.0）；`agent-browser` 为 R1.5 备选 | 同上；能力覆盖面不变 |
| R4 | **Local-first**（v1） | **场景修正后更强**：自有后台读取天然是"用户本机+本机登录态" |
| R5 | **headed 浏览器，用户可见可接管** | **更强**：官方导出/正常人工访问都以"用户在后台"为前提 |
| R6 | **Curis 专用 persistent profile**（`(business_id, platform_key)` 隔离） | 不变 |
| R7 | **Chrome 136 政策**：不能复用用户日常 Chrome 默认 profile | 不变（官方级约束） |
| R8 | **Authentication Stop Gate**（含全部禁止项） | 不变（见 §7） |
| R9 | **Evidence** 最小集合（structured data + URL + title + observed time + selected date range + screenshot + trace 按需） | 不变 |
| R10 | **Browser 与 Computer Use 并列**，共享 Stop Gate 与 Evidence 契约 | 不变 |
| R11 | **License 阻断项**（AGPL-3.0 / GPL-3.0 / SSPL 等） | 不变 |
| R12 | **云浏览器与 CGAP-04 品类级冲突**（Browserbase/Steel/Anchor 等以规避风控为卖点） | 不变 |
| R13 | **成本不是判据** | 不变 |
| R14 | **`--remote-debugging-port` 是本机最大攻击面** | 不变 |
| R15 | **SingletonLock**：同 profile 不可并发 | 不变 |

---

## 5. 哪些结论**修改 / 降级 / 撤回**

| # | 原结论（位置） | 处理 | 新表述 |
|---|---|---|---|
| **M1** | 主场景 = "平台无 API → 抓取"（STUDY §8、§11 第 1/2 问） | **撤回** | 主场景 = **Authorized Web Console Operation**（§2） |
| **M2** | 抖音 5.1 被作为"产品可行性硬约束"，实质否定场景 | **降级为 UNKNOWN + 待法务/官方确认** | U1/U3：条款**无"自用豁免"表述**，但**亦无官方材料明确适用于"读自己后台"** → **不得断言禁止，亦不得断言允许**（`evidence/09` §6） |
| **M3** | "平台合规是产品可行性前置约束"（表述过重） | **修正** | 平台合规是**风险登记项**（须裁定是否接受），**其中"产品目的"层面的合法性已被官方证据支持**；**仅"自动化机制"层面存在 UNKNOWN** |
| **M4** | 平台协议风险列为 **P0（可能使场景不成立）** | **降级为 P1** | 产品目的不再存疑；剩余风险集中在"自动化机制"与"资质"两点，且**存在更干净替代路径**（官方导出 + Import，`evidence/09` §5） |
| **M5** | 外部平台优先级：API → Browser → Computer Use → Import/Manual（用户 §3） | **建议细化（需 CEO 裁定）** | 建议在 API 与 Browser 之间**显式插入一档**：**"平台官方导出文件 + Curis Import"**（见 §6.2） |
| **M6** | §11 第 1 问答案："不需要自建渲染表面，需要 Curis 启动的可见浏览器窗口" | **保留，但补充命名澄清** | 结论不变；**须同时明确"Built-in Browser"只是产品能力名称**，**不蕴含技术上把渲染器嵌进 Curis 窗口**（用户 §8） |
| **M7** | §11 第 18 问 MVP | **重写** | 见 §8 |
| **M8** | Agent Layer 倾向"确定性优先 + 智能兜底"（表意正确但未定首版） | **收紧并定版** | **首版 = 路线 A（纯 Playwright 确定性）**；Stagehand/Agent 一律降为**后续可选**（见 §7） |

---

## 6. 外部平台执行优先级（正式采用 + 一处建议细化）

### 6.1 用户给定（正式采用）

```
1. Official API available?                        → API first
2. No API / API insufficient
   but user has authorized Web Console?           → Browser Capability
3. No usable Web Console
   but requires local App / Desktop GUI?          → Computer Use
4. Otherwise                                      → Import / Manual Entry
```

### 6.2 ⚠️ 建议细化（**需 CEO 裁定**，不擅自变更）

证据（`evidence/09` §5）显示：**平台自身提供"导出 Excel/CSV"的官方功能**（抖音创作服务平台「导出数据」、App 数据中心「导出数据」支持 7/30/90 天或自定义、抖店后台「批量导出」CSV）。

→ 因此实际存在一个**未被显式列出**的中间档。建议明确为：

```
1. Official API（含用户授权型 open_api）
2. ★ 平台官方导出文件 + Curis Import   ← 建议新增档（更少协议张力：用户只是点平台自己的按钮）
3. Browser Capability（Authorized Web Console Operation）
4. Computer Use（Desktop GUI）
5. Manual Entry
```

**取舍（必须由 CEO 决定，本报告不裁定）**：

| 选 2（官方导出） | 选 3（Browser） |
|---|---|
| ✅ 协议张力最低（用户在用平台自己的功能） | ✅ **可定时自动触发**（用户 §11 的核心诉求） |
| ✅ 零自动化风险 | ✅ 可批量、可回溯、时间范围可控 |
| ❌ **需人点按钮**，无法无人值守 | ⚠️ "自动化机制"层面存在 U1/U3 UNKNOWN |
| ❌ 跨平台字段名不统一，需逐平台映射 | ⚠️ 页面改版需维护 |
| ❌ 历史回溯差 | — |

**研究建议（非裁定）**：**两者并非互斥**。可行形态是 **2 作为默认、3 作为自动化增强**，并在 UI 上如实告知用户当前走的是哪条路径。**在 CEO 裁定前，MVP 应按 §8 定义的"3"实现**，因为 MVP 的目的正是验证 Browser 路径本身。

---

## 7. Agent Layer 复杂度：重新评估 → **首版选路线 A**

用户 §7 要求重新判断"是否真的需要重 Agent Browser"。结论如下。

### 7.1 三路线对比

| 路线 | 构成 | 适用条件 | 首版判定 |
|---|---|---|---|
| **A** | **Playwright + 确定性页面路径 + 结构化 selector / a11y + 少量智能恢复** | 稳定后台、已知导航路径、确定性数据页面 | ✅ **首版采用** |
| **B** | Playwright + Stagehand 等 AI 抽象 | 页面频繁改版、需自然语言适配 | ⏸ 后续可选（**仅作降级路径**） |
| **C** | 完整 browser-use 式 Agent | 未知站点、开放式任务 | ❌ **首版不采用** |

### 7.2 为什么路线 A 就够了（而非"更简单"）

**主场景的三个特征**恰好是"确定性路径"的**最佳适用条件**：

1. **稳定后台** —— 创作者/经营后台是**平台的核心产品资产**，其数据页面布局相对稳定（不是营销页/长尾页）。
2. **已知导航路径** —— 入口、菜单层级、数据页是**有限且可枚举**的（如 `creator.douyin.com` → 视频数据 → 作品分析）。
3. **确定性数据页面** —— 目标是**读取表格化指标**，而非"理解页面语义"。

**新增论据（本轮）**：**平台自身提供「导出数据」说明其后台数据是"结构化、可导出"的**（`evidence/09` §5）——这进一步说明页面上的数据是**规整的**，用确定性选择器读取是**恰当**的。

### 7.3 原则（正式采用）

```
Deterministic First
AI Recovery Second
```

**并明确**：**不为"AI Browser"这一标签引入第二套复杂编排器。**
理由（与 Curis 四原则一致）：Curis 的 Employee 是"调用能力的岗位"；引入 browser-use 式 Agent 会形成**两个规划者**，违背"能力可替换不写死"与"任何开发须让'目标→执行→验收→返工→完成'更自动"的取向。

### 7.4 智能恢复的**准入条件**（防滥用）
仅当**同时**满足以下两条才允许走 B 路线：
1. **确定性路径失败**（选择器失配、结构变更）已连续发生且被记录；
2. 该次采集在 Evidence 中被**显式标记为"自愈路径"**。
→ 保证经营数据的**可复现性**不被静默破坏（沿用 `CURIS_BROWSER_AUTOMATION_AND_AGENT_LAYER.md` §3 的结论）。

---

## 8. MVP 重写

### 8.1 目标
> **验证"AI Employee 可以读取用户自己 Web 后台中的真实经营数据并写回 Curis"。**

**验收重点不是"抓到网页"，而是**：
**找对账号 → 找对对象 → 找对日期 → 找对指标 → 写对 Result → 遇认证问题正确停止。**

### 8.2 范围（最小化）
单 Business ＋ 单 Platform ＋ 单账号 ＋ 单数据页 ＋ **单确定性路径**。

### 8.3 流程（14 步）

| # | 步骤 |
|---|---|
| 1 | 用户在 **Curis Browser Profile** 中手动登录（headed 可见窗口） |
| 2 | Curis 保存 **Profile 映射**，**不读取凭据** |
| 3 | 触发一次数据采集 Work |
| 4 | Browser 打开创作者/经营后台 |
| 5 | 导航到目标数据页 |
| 6 | 选择**固定时间范围** |
| 7 | 读取 **3~5 个关键指标** |
| 8 | 保存**关键 Screenshot Evidence** |
| 9 | 输出**结构化 JSON** |
| 10 | 写回 Result Intake |
| 11 | **制造一次 Session 失效** |
| 12 | **系统必须 STOP 并创建 Human Gate** |
| 13 | 用户重新正常登录 |
| 14 | **Resume 并完成原 Work** |

### 8.4 与上一轮 MVP 的差异

| 项 | 上一轮 | 本轮 |
|---|---|---|
| 首选平台 | "优先微信公众号 datacube 官方 API；若必须走浏览器选稳定平台" | **直接选一个用户实际拥有后台的平台**（官方 API 对个人主体不可得，故 API 路径不构成 MVP 主体） |
| Agent 层 | 未定版 | **明确路线 A（无 L3 智能层）** |
| 平台风险表述 | P0，可能使场景不成立 | **P1**；产品目的已被官方证据支持，剩余为机制层 UNKNOWN |
| 路径类型 | 确定性步骤脚本 | **不变**，但明确**禁止**引入自愈作为主路径 |
| Stop Gate | 必做 | **不变**，且第 11–14 步为**强制性验收项** |
| 追加 | — | **新增第 11–14 步为"必过"环节**（原 MVP 已有，但本轮明确其为首要验收内容） |

### 8.5 明确不做
❌ Cloud ❌ 并发 ❌ stealth ❌ CAPTCHA solving ❌ L3 智能规划 ❌ Computer Use ❌ 多平台 ❌ 端到端无人发布

---

## 9. 平台协议风险重新定性（A vs B）

### 9.1 两类行为必须分开

| | **A 类**：抓取公开/第三方内容 | **B 类**：用户在自己账号授权范围内、经自己的后台读取自己的经营数据 |
|---|---|---|
| 对象 | 他人的、或平台未向该用户展示的数据 | **平台已向该用户展示的数据** |
| 官方态度 | **明确禁止**（抖音 5.1 明文，`evidence/05`） | **产品目的被官方承认**（`evidence/09` §1）；**机制层面 UNKNOWN** |
| 风险等级 | 高（含民事、刑事、封号风险） | **中（且存在更干净的替代路径）** |
| Curis 是否采用 | ❌ **不采用** | ⚠️ **本轮主场景** |

**上一轮的错误**：把 A 类的风险结论**未经分析直接等同于 B**。本轮纠正。

### 9.2 B 类的逐项核验（用户 §9 要求）

| # | 待核验问题 | 结论 | 依据 |
|---|---|---|---|
| 1 | 平台条款是否**明确禁止** | **UNKNOWN** | 抖音 5.1 原文**无自用豁免**表述，但**亦无官方材料明确适用于"读自己后台"** → **不断言禁止、不断言允许**（U1） |
| 2 | 是否允许**正常人工后台访问** | ✅ **是** | 平台自身提供后台、提供**官方导出功能**（`evidence/09` §5） |
| 3 | Browser Automation 是否有**明确限制** | **UNKNOWN** | 未找到官方文件就"后台自动化"作出明确规定（U1） |
| 4 | 是否需要**产品层接受风险** | ✅ **是** | 建议由总控决策席显式登记"机制层 UNKNOWN 已接受" |
| 5 | 是否应**限制为用户自己账号** | ✅ **是（强制）** | Profile 与 Business 强绑定；禁止运行时切号 |
| 6 | 是否应**限制执行频率** | ✅ **是（建议低频）** | 平台风控为设备指纹+行为分析；低频更安全。**阈值 UNKNOWN，不可量化**（U6） |
| 7 | 是否应要求**可见 headed 模式** | ✅ **是** | 用户可见可接管是 CGAP-04 Resume 的实现前提，也降低"隐蔽自动化"的语义风险 |
| 8 | 是否应**默认低频 / 事件驱动** | ✅ **是（建议）** | 默认低频或事件驱动（如发布后 24h 一次）；高频采集须显式授权 |
| 9 | "向第三方共享账号"是否被触及 | ❌ **不触及** | Curis 不接收/不代填/不导出密码或 Cookie；用户在本机自行登录（`evidence/09` §4.1） |
| 10 | "协助第三方采集非公开数据"是否被触及 | **UNKNOWN** | 取决于"用户自己后台已展示的数据"是否构成"平台非公开数据"（U3） |

### 9.3 明确不做什么（不扩大、不弱化）
- ❌ **不**因为"自有数据"就宣称完全合规（机制层仍是 UNKNOWN，须法务/官方确认）。
- ❌ **不**因为抖音 5.1 字面宽泛就宣称场景不成立（官方证据支持该产品目的）。
- ✅ **登记 UNKNOWN，交由法务或官方渠道闭环**，不由本研究自行裁定。

---

## 10. Session 模型重新理解

### 10.1 正确描述
用户**提前**在 **Curis 管理的专用 Browser Profile** 中**正常登录**；此后 Employee **复用这个正常 Session**。

### 10.2 禁止的描述（上一轮若出现，一并纠正）
❌ "自动获取登录态" ❌ "迁移用户 Cookie" ❌ "自动登录"

### 10.3 Curis 的责任边界

| Curis **只**管理 | Curis **不**知道 / **不**处理 |
|---|---|
| Profile identity（哪个 profile 属于哪个 Business×Platform） | 用户的**密码** |
| Session availability（会话当前是否可用） | **Cookie** 内容 |
| Auth state signal（已登录/未登录/需验证的信号判断） | **Token** 内容 |
| Business / Platform mapping | 任何凭据的**导出或解析** |

> **要点**：Curis **不需要知道密码**，**也不应该导出/解析 Password / Cookie / Token**。
> 这与 Curis 既有硬约束（凭据不落盘明文）方向一致，并使 §9.2 第 9 项（"向第三方共享账号"）**不成立**。

---

## 11. 自动触发场景（CGAP-03 的 Capability Requirement，**不设计 Automation Runtime**）

典型流程：
- **事件驱动**：Song 发布后 24h → 触发 Analytics Work → 启动 Browser → 使用已有 Session → 进入目标后台 → 读取目标数据 → 写回 → 分析。
- **定时驱动**：每天 09:00 → 检查 Content Growth 各账号昨日表现。

### 11.1 必须记录的 Capability Requirement（不设计实现）

| # | 问题 | Requirement（本轮只登记） |
|---|---|---|
| Q1 | 浏览器未运行时如何启动 | 需"按需启动 Chrome + 专用 profile + headed"的能力；**须由 Capability 层封装** |
| Q2 | Session 如何恢复 | 依赖 persistent profile；**须有"会话可用性检测"**（不假设必然有效） |
| Q3 | Mac 休眠怎么办 | **须登记为已知限制**：休眠中断任务 → 需"任务可恢复"语义（CGAP-03 范畴） |
| Q4 | 同 Profile 是否串行 | **强制串行**（SingletonLock 硬约束：同 user data dir 不可双实例） |
| Q5 | 任务失败如何恢复 | 需 checkpoint + 幂等重入（与 Stop Gate 共用机制） |
| Q6 | 页面结构变化如何处理 | **首版**：失败即上报，**不自愈**；**后续**：按 §7.4 准入条件启用 B 路线 |
| Q7 | 写回如何保证目标账号/目标内容不串 | **必须做三元组校验**：`(business_id, platform_key, profile_ref)` + **采集对象 ID**（作品/歌曲/账号 ID）双校验，写入前校验，写入后回读 |

> **Q7 是本轮新增的关键 Requirement** —— 用户 §12 的 Evidence 最小集合中包含 **Account / Content ID**，正是为防串号而设。**这是"找对账号、找对对象"的落地保障。**

---

## 12. Evidence 重新收敛

**主产物 = Structured Result。Evidence 只用于证明来源。**

### 12.1 最小必存字段（用户 §12 给定，正式采用）

| 字段 | 说明 |
|---|---|
| Platform | 平台标识 |
| Account | 账号标识 |
| **Content / Song ID** | **采集对象 ID**（防串号核心字段） |
| Page / Section | 页面/区块（证明"从哪个页面读的"） |
| **Selected Date Range** | 采集所设时间范围（经营数据关键维度） |
| Observed At | 观测时间（**含时区**） |
| Metric | 指标名 |
| Value | 指标值 |
| Source URL | 来源 URL |
| **Screenshot** | **关键步骤 / 关键结果**截图 |
| **Collection Method = BROWSER** | 采集方式标识 |

**另建议增加一项**（延续既有结论）：`Path Type = DETERMINISTIC | SELF_HEALED`。

### 12.2 明确不做
❌ **默认不保存整页 DOM**。（与上一轮结论一致，本轮维持。）

---

## 13. 命名建议（**不改正式名称**）

用户 §14 要求避免团队误解成"Curis 要做浏览器"或"Curis 要做爬虫"。

| 候选名称 | 优点 | 缺点 | 评价 |
|---|---|---|---|
| **Authorized Web Console Capability** | **最准确**：点出"已授权"与"Web Console"两个要点 | 稍长 | ✅ **首选** |
| **Browser Workspace Capability** | 简洁，与 Curis 的"Workspace"词汇体系一致 | "Browser"仍可能被读成"浏览器产品" | ✅ 次选 |
| **Console Operation Capability** | 最短 | 丢失"Web"与"授权"语义 | ⚠️ 可用 |
| Web Console Operation Capability | 准确 | 长 | ✅ 可用 |

**建议**：正式名称 **`Authorized Web Console Capability`**（**CGAP-01 编号不变**），并在所有文档首次出现处加一句消歧：

> "本能力指 **AI Employee 对用户本人已授权的 Web 后台（Console）的操作**，**不是**浏览器产品，**不是**爬虫，**不涉及**公开内容采集。"

**同时明确保留用户 §8 的澄清**：
> **"Built-in Browser"是产品能力名称，不意味着技术上必须把浏览器渲染器嵌进 Curis 窗口。**

---

## 14. 是否影响技术选型？——**不影响**

| 层 | 上一轮结论 | 本轮是否变更 |
|---|---|---|
| L0 Browser Engine | Chromium（系统 Chrome / CfT） | **不变** |
| L1 Embedded Surface | 可见 headed 真实浏览器窗口（非嵌入式 WebView） | **不变**（且澄清命名） |
| L2 Automation Runtime | Playwright（主）/ agent-browser（备选） | **不变** |
| L3 Agent Layer | Curis 自建薄层 | **收紧**：首版 **Route A**，B/C 延后 |
| L4 Session/Profile | Curis 自建（二维隔离） | **不变**（责任边界更明确） |
| L4 Stop Gate | Curis 自建 | **不变** |
| L5 Cloud | Later / Provider | **不变**（且场景修正后更不需要） |

**一句话**：**变的是"我们为什么做"和"首版做到哪一步"，不是"用什么做"。**

**唯一实质性的选型层影响**：**Agent Layer 的复杂度被显著压低**——从"待评估是否引入 Stagehand/Agent"变为"**首版明确不用**"。这降低了复杂度、成本与不确定性。

---

## 15. 十五问逐条回答

| # | 问题 | 回答 |
|---|---|---|
| **1** | Browser Capability 真正服务的第一场景是什么？ | **Authorized Web Console Operation**：AI Employee 进入**用户本人已登录**的创作者/经营后台，**读取平台已向该用户展示的经营指标**，结构化写回 Curis（§2）。 |
| **2** | 它是不是"数据抓取器"？ | **不是。** 不是爬虫、不是公开页面批量抓取、不是反爬/stealth/CAPTCHA/风控绕过工具（§2.3）。上一轮用"抓取"作主叙事是**表述错误**，已撤回（M1）。 |
| **3** | 为什么 Web Console 操作优先于 Computer Use？ | 三条：① **官方 API 对个人主体不可得**，而用户的 Web Console 对其开放（`evidence/09` §2）；② macOS 上 Browser 自动化**无需 TCC 无障碍/录屏**，Computer Use **需三项手动授权且会周期性失效** —— **权限成本差一个量级**；③ 目标是**结构化表格数据**，Web 层读取是**恰当工具**，GUI 坐标级操作是**过度工程**。 |
| **4** | API / Browser / Computer Use / Import / Manual 优先级？ | 正式采用用户给定的 **API → Browser → Computer Use → Import/Manual**。**建议细化（需 CEO 裁定）**：在 API 与 Browser 之间显式插入 **"平台官方导出文件 + Curis Import"**（§6.2，证据 `evidence/09` §5）。 |
| **5** | Playwright 结论是否仍成立？ | **完全成立，且更强。** 主场景（稳定后台 + 已知路径 + 确定性数据页）**正是 Playwright 的最佳适用条件**；Playwright 的短板（登录态获取、Stop Gate、Pause/Resume）**仍是 Curis 必须自建的部分**，与场景无关（R3、§7.2）。 |
| **6** | 是否还需要重 Agent Browser？ | **首版不需要。** 采纳 **Deterministic First / AI Recovery Second**（§7.3）。**首版 = 路线 A（纯 Playwright 确定性）**；路线 B（Stagehand 类）降为**有准入条件的后续可选**；路线 C（browser-use 式完整 Agent）**不采用**（会引入第二个规划者）。 |
| **7** | 用户如何建立正常登录 Session？ | 用户在 **Curis 管理的专用 Browser Profile** 中、**在可见 headed 窗口内自行登录一次**。Curis **不做**自动登录、**不代填**、**不导出**（§10）。**注意**：不能复用用户日常 Chrome 默认 profile（Chrome 136 政策，R7）。 |
| **8** | Curis 需要保存什么，不保存什么？ | **保存**：Profile identity、Session availability、Auth state signal、Business/Platform mapping。**不保存/不处理**：Password、Cookie、Token（**不导出、不解析**）（§10.3）。**另需 CEO 裁定**：profile 目录内**必然落盘的会话材料**是否纳入既有凭据治理（上一轮已提出的裁定项，本轮不变）。 |
| **9** | 平台协议风险在"自有后台数据读取"场景下应如何解释？ | **必须区分 A（抓取公开/第三方内容）与 B（自有后台读取）**，不得把 A 的结论套用到 B（§9.1）。**B 的产品目的被官方承认**（抖音官方文档明示支持"用户授权后在第三方系统查看自己数据"）；**机制层为 UNKNOWN**（5.1 无自用豁免表述，亦无明确适用）→ **登记 UNKNOWN 交法务/官方闭环**，**不扩大、不弱化**（§9.2、§9.3）。 |
| **10** | Authentication Stop Gate 是否变化？ | **完全不变**（R8）。信号集合、STOP→checkpoint→Gate→通知、全部禁止项、Resume 重校验，均维持。**并且**：`evidence/09` §4.1 显示 Curis"不共享账号"的架构**恰好让它避开了平台明确禁止的模式** —— 这是 Stop Gate 原则的**额外收益**。 |
| **11** | 自动触发数据回收如何工作？ | 本轮**只登记 Capability Requirement**（Q1–Q7，§11），**不设计 Automation Runtime**。关键硬约束：**同 Profile 强制串行**（SingletonLock）；**Mac 休眠为已知限制**；**写回必须做三元组 + 采集对象 ID 双校验**（防串号）。 |
| **12** | 最小 MVP 应该验证什么？ | 验证 **"能读取用户自己 Web 后台的真实经营数据并写回 Curis"**，验收重点是 **找对账号 / 找对对象 / 找对日期 / 找对指标 / 写对 Result / 遇认证问题正确停止**（14 步流程，§8.3）。 |
| **13** | 哪些原报告结论因误解场景需要撤回或降级？ | **撤回**：M1（主场景=抓取）、M2（抖音 5.1 作为否定性硬约束→降为 UNKNOWN）。**降级**：M4（平台风险 P0→**P1**）。**修正**：M3（"可行性前置约束"→风险登记项）。**重写**：M7（MVP）。**定版**：M8（Agent 层 Routes A）。**建议细化**：M5（优先级新增官方导出一档）。**补充**：M6（命名澄清）（§5）。 |
| **14** | 哪些结论仍然完全有效？ | **R1–R15 全部有效**（§4）：不自建引擎、Chromium、Playwright 主选、Local-first、headed 可见可接管、专用 persistent profile、Chrome 136 约束、Stop Gate、Evidence 最小集、Browser 与 Computer Use 并列、License 阻断项、云浏览器与 CGAP-04 冲突、成本非判据、调试端口攻击面、SingletonLock 串行。 |
| **15** | 是否足够登记为 Capability Solution Candidate？ | **更接近了，但仍未足够。** 场景修正**消除了最大的概念性障碍**（产品目的已被官方证据支持），但登记前仍需闭环：① **U1/U3 法务或官方确认**（自动化机制在自有后台场景的定性）；② **会话材料凭据治理裁定**；③ **"官方导出 vs Browser"优先级的 CEO 裁定**；④ **MVP（§8）验收通过**；⑤ 命名正式变更需走文档流程。**当前状态：READY FOR CEO REVIEW，未登记。** |

---

## 16. 本轮边界遵守声明

| 允许 | 执行情况 |
|---|---|
| RECONCILE | ✅ 完成（本文件） |
| VERIFY | ✅ 完成（定向核验 2 次，`evidence/09`；**未做泛搜**） |
| DOCUMENT UPDATE | ✅ 完成（见下） |

| 禁止 | 执行情况 |
|---|---|
| 重新泛搜所有 Browser 项目 | ✅ 未做（仅 2 次定向核验，针对 B 场景的官方通道与导出功能） |
| 开发 | ✅ 未做 |
| 修改 Curis Runtime / Authority / UI | ✅ 未做 |
| HTML / Figma | ✅ 未做 |
| commit / push | ✅ 未做 |

**同步更新的文件**（见各文件内新增的 Reconciliation 段落）：

| # | 文件 | 更新内容 |
|---|---|---|
| 1 | `CURIS_BUILT_IN_BROWSER_CAPABILITY_STUDY.md` | 文首 RECONCILIATION 声明 + §0 第 8/9 条修正 + §8 定性降级 + §11 第 1/2/6/17/18/20 问修正 + §13 交付状态 |
| 2 | `CURIS_BROWSER_CAPABILITY_RECOMMENDATION.md` | 文首声明 + §0 L3/风险行 + §6 MVP 重写指针 + §7 P0→P1 + §8 待裁定 #1 + §10 登记判定 |
| 3 | `CURIS_BROWSER_TECHNOLOGY_MATRIX.md` | 文首声明 + §4 L3 行收紧 + §6.1 补充 + §7 汇总 L3 行 |
| 4 | `CURIS_BROWSER_LOCAL_CLOUD_HYBRID_OPTIONS.md` | 文首声明 + §5.1 新增第 5 条论据 |
| 5 | `CURIS_BROWSER_AUTOMATION_AND_AGENT_LAYER.md` | 文首声明 + **新增 §3.0 首版定版（路线 A）** + §5 结论行收紧 |
| 6 | `CURIS_BROWSER_OPEN_SOURCE_DEEP_DIVE.md` | 文首声明 + §6.1 R2 行收紧 |
| 7 | `CURIS_BROWSER_SESSION_AND_SECURITY_MODEL.md` | 文首声明 + §10 语义澄清（Session 描述与责任边界） |
| 8 | `RESEARCH_JOURNAL.md` | 状态行 + E3 修正 + H6 更新 + **新增 §6 Reconciliation 轮** |
| 9 | `evidence/01_SOURCES_INDEX.md` | 采集日期 + §A 新增 09 + §B.5 新增来源 + §C 独立核验 11–13 + **新增 §D.5 Reconciliation 审计** |
| 10 | **新增** `evidence/09_AUTHORIZED_CONSOLE_AND_API_GATING.md` | 官方通道 / API 资质门槛 / 官方导出 / A-B 风险区分 / U1–U6 |

**未修改**：`docs/` 下任何文件、Curis Runtime / Frontend / Backend / Authority / UI / HTML Exploration / Figma。**未 commit、未 push。**

---

```
BROWSER CAPABILITY USE CASE RECONCILED — READY FOR CEO REVIEW
```
