# CURIS BROWSER SESSION AND SECURITY MODEL

Authority Class: RESEARCH（架构候选，非裁定）
Status: Draft（已过 Reconciliation 轮 + **Addendum 轮**）
Owner: 研究执行
Related: CGAP-01 / CGAP-04
Evidence: `evidence/03`、`evidence/04`、`evidence/05`、`evidence/06`、**`evidence/09`、`evidence/10`**

> 本文只回答"会话与安全应该长什么样"，不修改 Curis 现有模型。

> ⚠️ **RECONCILIATION 声明（第 2 轮）**：本文**全部结论不变**（R6 专用 persistent profile、R7 Chrome 136 约束、R8 Stop Gate、R2 可见 headed、R14 调试端口攻击面、R15 SingletonLock）。
> 两处**语义澄清**（来自 Reconciliation，非技术变更）：
> ① **Session 的正确描述**是"用户**提前**在 Curis 管理的专用 profile 中**正常登录**，Employee **复用**该 Session"；**禁止**表述为"自动获取登录态 / 迁移 Cookie / 自动登录"（RECONCILIATION §10）。
> ② **责任边界更明确**：Curis 只管理 Profile identity / Session availability / Auth state signal / Business-Platform mapping；**不知道、不处理、不导出、不解析** Password / Cookie / Token（RECONCILIATION §10.3）。
> ③ **（Addendum 轮，2026-09-20）R7 适用范围细化**：Chrome 136 关闭的是 **CDP / Playwright 路线**；**扩展（`chrome.debugger`）路径不受该政策约束**。Curis **仍须专用 profile**，但理由由"官方禁止"改为 **"需要凭据罐级隔离"**。**新增 §2.1「接入路径 P1 / P2 / P3」**。

---

## 1. 问题的真实形态：先纠正三个直觉

### 直觉 1（错误）：Curis 可以直接接管用户日常 Chrome 的登录态
**否定证据（E1）**：Chrome 136 起（2025-03-17 政策），`--remote-debugging-port` / `--remote-debugging-pipe`
**在默认 data dir 上不再被尊重**，必须配合 non-standard `--user-data-dir`。Google 官方建议自动化场景改用 **Chrome for Testing**。

→ 因此**在 CDP / Playwright 路线上**，"复用用户日常 profile"这条路**已被官方关闭**，且**不应**试图绕过（绕过即等于攻击 App-Bound Encryption 的同一手法）。

> ⚠️ **R7 适用范围细化（Addendum 轮，2026-09-20；`evidence/10` §4）**
> Chrome 136 关闭的是 **`--remote-debugging-port` 在默认 data dir 上的使用**，即 **CDP / Playwright 路线**。
> **浏览器扩展（`chrome.debugger`）是另一条通道，不受该政策约束**——`Tencent/BrowserSkill`（MIT）为现成证明：对其 `README.md` / `docs/architecture.md` / `docs/remote-extension-connection.md` / `skill/SKILL.md` 四份原文穷举 grep，**`--remote-debugging-port` 与 `--user-data-dir` 零命中**；其控制面为扩展内 `chrome.debugger`（`architecture.md` 系统图 = `Ext -->|CDP + WebExt| Tabs`）。
> **但这不改变本文结论**：Curis **仍须自持专用 profile**，理由由"官方禁止"改为 **"Curis 需要凭据罐级（per-Business）隔离，而扩展路径的隔离是窗口级"**（见 §2.1）。
> **不得**将扩展路径表述为"绕过官方限制"——它是**官方支持的正常机制**。

### 直觉 2（错误）：会话复用 = 读用户的 Cookie
**纠正**：Curis 不应**读取、导出、解析**Cookie/Token。正确形态是 **profile 目录整体托管**——Curis 只管理"哪个目录属于哪个 Business"，从不解析目录内的会话材料内容。这与"禁止设计读取/导出用户密码、Cookie、Token"的要求一致。

### 直觉 3（错误）：登录态是"一次配置、长期有效"
**纠正**：Playwright 官方文档明确 **不负责会话过期管理**（`evidence/06` §4）。过期检测、失效识别、重新登录触发**全部是 Curis 的责任**。这正是 CGAP-04 存在的理由。

---

## 2. 会话持久化：三种形态对比

| 形态 | 机制 | 覆盖内容 | 用户可见 | 隔离粒度 | 安全等级 | Curis 适配度 |
|---|---|---|---|---|---|---|
| **S1. storageState 文件** | `context.storageState({path})` → JSON | cookies + localStorage + IndexedDB + passkey | 否 | 每 Business 一个 JSON | ⚠️ **低**（官方原文：可直接冒用身份） | 不推荐作主方案 |
| **S2. Persistent Context** | `launchPersistentContext(userDataDir)` | 整个 profile：cookies、storage、**SW、cache、扩展、站点权限** | 可（headed） | 每 profile 一个目录 | 中 | **推荐（主方案）** |
| **S3. 远程会话（Cloud）** | Provider 侧持久 profile / context | 由 Provider 定义 | 视 Provider | Provider 侧 | 低（会话材料离开本机） | v1 不作默认 |

### 推荐：S2 为主、S1 为辅
- **S2** 作为登录态的**唯一持久载体**：用户在一个 Curis 托管的真实浏览器窗口里正常登录一次，会话随目录存活。
- **S1** 仅用于**跨设备/跨运行时迁移**或**只读快照**场景，且必须加密（见 §4）。
- 理由：S2 是 Google 明确推荐的形态（non-default user-data-dir）；S2 保留了 Service Worker 与站点权限，对现代后台（SPA + 长连接）登录态保真度显著高于 S1；且 S2 **天然按目录隔离**，服务 CGAP-04 的 Profile 隔离需求。

### 2.1 接入路径 P1 / P2 / P3（Addendum 轮细化，2026-09-20）

> 原表述（"P1 默认；P2 为显式例外；P3 不推荐"）**不变**；本轮补足 **P2 的可行性与其被否决的真实理由**。

| 档 | 形态 | Chrome 136 之后 | 参考实现 | Curis v1 |
|---|---|---|---|---|
| **P1** | Curis **自启专用 profile**（Playwright `launchPersistentContext`） | ✅ 可行（正是政策要求的形态） | Playwright | ✅ **默认** |
| **P2** | **浏览器扩展**附加到**用户已有浏览器**（`chrome.debugger`） | ✅ **可行**（⚠️ **不受**调试端口政策约束） | **`Tencent/BrowserSkill`（MIT）** | ⚠️ **仍为显式例外，v1 不开放** |
| **P3** | 经**外部 CDP 端点**接入（`connectOverCDP`） | ⚠️ 若指向默认 data dir 则不可行 | Playwright `connect_over_cdp` | ❌ 不推荐 |

**P2 被否决的**真实理由（**不是**"被 Chrome 禁止"）：

| 维度 | P1（默认） | P2（扩展附加真实浏览器） |
|---|---|---|
| **隔离粒度** | ✅ **凭据罐级**（每 Business × Platform 独立 profile） | ❌ **窗口级**（多 Agent Window **共享同一 cookie 罐**） |
| **多 Business** | ✅ 支持 | ❌ **不支持**（同平台多账号会**互相覆盖登录态**） |
| 浏览器二进制 | 需自带（281MB）或复用系统 Chrome | **零**（复用用户已装 Chrome / Edge） |
| 登录态获取 | 用户需在 Curis profile 内**重登一次** | **直接复用用户已有登录态** |
| 权限域 | CDP 全量（任意 JS / 任意网络 / 完整 Cookie 访问） | **21 个类型化 tool handler**（能力域化，**更窄**） |
| 新增攻击面 | CDP 调试端口（须严格管控，R14） | loopback WS 监听（默认 52800）+ 扩展 origin 白名单 + 可选远程 WSS |

→ **结论**：**P1 仍为默认**；P2 的价值（零分发体积 + 复用已登录态）**与 Curis 的多 Business 前提冲突**。
→ **建议**：P2 保留为 **v1.5+ 增强档**；届时须先定义 **"P2 下如何保证 Business 级凭据隔离"**（`CURIS_BROWSER_ADDENDUM_2026-09-20_BROWSERSKILL_AND_JEV.md` §4、§11）。
→ ⚠️ **禁止**：把 BrowserSkill 的"**跨 session 并行**"直接移植到多 Business 场景——并行窗口共享 cookie 罐 ⇒ **串号**。

---

## 3. Profile 隔离粒度：建议"每 Business × 每平台"二维独立

### 3.1 为什么不能共享一个 Profile
1. **平台风控**：同一浏览器 profile 同时承载"抖音"与"小红书"账号，Cookie 域虽隔离，但**指纹、UA、时区、缓存行为、扩展**同源。平台风控模型已普遍使用**设备指纹 + 行为分析**（`evidence/05` §2）。跨平台共用一个 profile 会**提高关联识别概率**。
2. **Curis 自身的 Business 隔离原则**：Curis 的 Business 是隔离单元（Office ⊥ Organization，见既有裁定）。会话材料若跨 Business 共享，等于**跨租户泄漏路径**（即便是单机自用，也破坏"Business 是隔离单元"的模型一致性）。
3. **失效爆炸半径**：一个平台触发风控 → 若 Profile 共享，可能连带影响其他平台的会话。

### 3.2 建议模型

```
BrowserProfileKey = (business_id, platform_key)
    e.g. ("content-growth", "xiaohongshu")
存储位置（建议，不落 docs/）：
    ~/Library/Application Support/Curis/browser-profiles/<business_id>/<platform_key>/
```

- **同一 Business 的同一平台** → 复用同一 profile（会话延续）。
- **不同 Business** → **必须独立**。
- **同一 Business 不同平台** → **建议独立**（理由 §3.1.1）。
- 代价（须登记）：profile 数量增长 → 磁盘占用与维护成本。建议设置**闲置回收策略**（如 N 天未使用则归档/清理，需用户确认）。

### 3.3 与 Curis 现有凭据体系的关系（新问题，需裁定）

Curis 既有硬约束：**凭据不可能明文落盘**（`LocalDevCredentialBackend` 仅存进程内存；DB 只存 `credential_ref` + `secret_digest`）。

而 profile 目录内的**会话材料天然落盘**。→ **必须新增裁定**：

| 待裁定项 | 候选答案 |
|---|---|
| 会话材料是否纳入凭据治理？ | 建议纳入，赋予独立 `profile_ref`，类比 `credential_ref` |
| 落盘形态？ | 候选：(a) 依赖 Chromium 内建加密（App-Bound Encryption 仅 Windows；macOS 依赖钥匙串） (b) Curis 额外包裹（OS Keychain 保管密钥 + 加密 profile 归档） (c) 仅依赖 macOS 全盘加密（FileVault） |
| 是否允许离开本机？ | 建议：v1 **默认禁止**；Cloud 路径需显式用户授权并单独登记 |
| 删除语义？ | 建议：删除 Business → 连带销毁 profile 目录，并明确告知用户"该 Business 的所有平台需重新登录" |

---

## 4. 凭据边界（硬约束的落地形态）

**允许**：
- Curis 持有"profile 目录 → Business"的**映射元数据**（不含会话内容）。
- Curis 检查**登录态是否有效的信号**（URL、页面元素、HTTP 状态），据此判断"已登录/未登录"。
- 用户在 Curis 窗口内**手工输入**账号密码（输入直接进入浏览器，Curis 不截获）。

**禁止**（与既有硬约束及本轮要求一致）：
- 读取/导出/解析 Cookie、localStorage、Token 明文。
- 存储或代填用户密码。
- 解析 `userDataDir` 内部会话文件。

---

## 5. Authentication Stop Gate（CGAP-04）实现设计

### 5.1 必须 STOP 的信号集合（用户给定 + 建议补充）

| 类别 | 具体信号 | 检测手段（候选） |
|---|---|---|
| 登出 | Logged out / Login required | URL 匹配登录路径；出现登录表单元素（role/name 选择器） |
| 会话失效 | Session expired | 关键 API 返回 401/403；跳转登录页；页面出现"登录已过期"文案 |
| 人机校验 | CAPTCHA / 滑块 / 点选 | 出现验证码容器元素；iframe 域匹配 `captcha`/`verify`/`geetest`/`hcaptcha`/`recaptcha` |
| 二次验证 | MFA / SMS / 邮箱验证码 | 出现验证码输入框、`验证码`/`动态码` 文案 |
| 设备校验 | Device verification | 出现"新设备"、"异地登录"、"设备确认"文案 |
| 风控 | Risk-control prompt | 出现"操作过于频繁"、"账号异常"、"环境异常"文案 |
| 锁定 | Account lock | 出现"账号已被限制/封禁"文案 |

> 实现要求：信号集合应**可配置、可扩展**，并**fail-closed**——**无法判定状态时，按"需要人工"处理，而非继续执行**。

### 5.2 STOP 的动作序列（用户给定，逐条落地）

```
1. STOP            → 立即中止当前动作循环，不再发起任何 page 操作
2. 保存执行位置     → 落盘 checkpoint：{run_id, plan_step_index, url, page_title,
                      observed_at, business_id, platform_key, profile_ref,
                      已完成步骤、待执行步骤、已采集数据（若有）}
3. 创建 Human Gate  → 生成 Gate 记录（类型=AuthRequired，原因=命中的信号）
4. 通知用户         → 在 Curis 内显式呈现（非静默）；不使用飞书（飞书仅升级事件）
```

**明确禁止**（用户给定，逐条对应实现约束）：
- 重复尝试登录 → 实现上：**Gate 创建后不得再发起任何导航/提交**，循环必须 break 而非 continue
- 猜密码 → 无任何凭据猜测代码路径
- 循环提交凭证 → 同上
- 绕 CAPTCHA → **不集成任何 captcha-solving**（含第三方打码服务）
- 绕 MFA → 不模拟短信/OTP
- 切账号试探 → profile 与 Business 强绑定，不允许运行时切换
- 规避平台风控 → **不使用 stealth/指纹伪装**（见 §6）

### 5.3 Resume from safe checkpoint

```
用户完成登录 → Curis 检测登录态恢复 → 从 checkpoint 恢复
恢复时要求：
  a. 重新校验 (business_id, platform_key, profile_ref) 三元组一致 → 防串号
  b. 重新校验登录态有效（不假设"用户说登好了"就是好了）
  c. 从 plan_step_index 继续，不重放已完成的写操作（幂等性由 Capability 定义）
  d. 记录 resume 事件到 Evidence
```

**技术可行性判定**：Playwright/Puppeteer **均无内置的"人工介入后恢复"原语**。它们提供的是**可中断的异步 API** + 可持久化状态。因此 **Pause/Resume 必须由 Curis 自己实现**（编排层持有 plan、step index、checkpoint 存储）。

关键有利事实：**headed 模式下浏览器进程本就可被人类同时操作**。人类在窗口中登录，Playwright 只需轮询状态即可继续——这是"Human-in-the-loop 登录"最容易实现的形态，**不需要**任何框架级 HITL 支持。

→ 结论：**CGAP-04 是 Curis 自建能力，不能外包给现有框架。**

---

## 6. 关于 stealth / 反检测（必须明确拒绝）

| 工具 | 声称能力 | License | Curis 判定 |
|---|---|---|---|
| patchright | "Undetected version of Playwright" | Apache-2.0 | **不采用** |
| SeleniumBase CDP Mode | "bypasses bot-detection systems" | MIT | **不采用** |
| undetected-chromedriver | "Passes ALL bot mitigation systems" | **GPL-3.0** | **不采用**（且 License 亦不合） |
| rebrowser-patches | 修补 CDP 泄漏指纹 | — | **不采用** |

**理由（产品原则层面，非技术层面）**：CGAP-04 的核心承诺是"遇风控即停、绝不规避"。**集成反检测工具与该承诺直接矛盾**——它把产品定义为"能绕过风控的东西"，一旦平台升级检测，产品行为从"停止"变为"隐蔽对抗"，法律与账号风险同步升级（`evidence/05`）。

**正确做法**：在**用户本人的正常环境中、以用户本人可见的方式、低速、非并发**地操作；把"被风控"视为**预期的、必须上报给用户**的合法结果，而非需要规避的障碍。

---

## 7. 其他安全域（逐项登记）

| 域 | 风险 | 建议默认策略 |
|---|---|---|
| **Downloads** | 恶意文件；落盘路径逃逸 | 默认禁用；启用时限定到 Business 沙箱目录；下载后不自动打开 |
| **Uploads** | 把用户敏感文件上传到外部平台 | 白名单允许的 Business 目录；上传前需在 UI 明示目标域名与文件名 |
| **Clipboard** | 读取剪贴板中的密码/密钥 | 默认禁用读写；`grantPermissions` 不授予 clipboard-read |
| **Local Files** | 页面通过 file:// 或 File System Access API 读取本地文件 | 禁用 `--allow-file-access-from-files`；不授予 File System Access |
| **Camera / Mic** | 静默采集 | 默认拒绝；`context.grantPermissions` 显式不包含 |
| **Notifications** | 骚扰 + 信息泄漏 | 默认拒绝 |
| **Popup / 新窗口** | 弹窗钓鱼；页面逃逸 | 全部捕获为 Page 对象并**登记**，不自动交互 |
| **External Protocol** | `mailto:` / 自定义协议唤起本机 App | 默认拦截；**不**允许页面唤起本机程序 |
| **Local Network** | 页面探测本机服务 | 不使用；不把 Curis 本地端口暴露给被自动化页面 |
| **调试端口暴露** | `--remote-debugging-port` 是一个**完整的浏览器控制通道** | **必须只绑定 127.0.0.1**；端口随机化；会话结束立即关闭；**绝不暴露到 LAN** |
| **页面内容注入** | 被自动化页面含 prompt injection（诱导 AI Employee 越权） | 页面内容**一律视为不可信输入**；Employee 的计划不得因页面文本而扩张权限（沿用既有的 prompt injection 认知） |

### 7.1 一条必须写进设计的推论

**`--remote-debugging-port` 本身是本产品最大的攻击面。**
它提供的能力等价于"任意 JS 执行 + 任意网络请求 + 完整 Cookie 访问"。本轮已确立（E1）它**不能用默认 profile**，因此 Curis 必然开启一个带调试端口的浏览器。→ 必须把"调试通道仅本机、短生命周期、随机端口、与 Business 绑定"作为**硬性实现要求**，而非优化项。

---

## 8. 小结（研究假设）

| 项 | 结论候选 |
|---|---|
| 会话载体 | Persistent Context（profile 目录）为主；storageState 仅作加密迁移 |
| 隔离粒度 | **(business_id, platform_key) 二维独立** |
| 凭据边界 | Curis **不解析**会话内容；只持映射与有效性信号 |
| 落盘形态 | **需新增裁定**（现有凭据体系未覆盖"浏览器会话材料"这一类） |
| Stop Gate | **Curis 自建**（框架无 HITL 原语）；信号集合可配置；**fail-closed** |
| Pause/Resume | Curis 编排层持有 plan + checkpoint；利用 headed 模式的人类可操作窗口 |
| 反检测 | **明确不采用**（与产品承诺冲突，且部分 License 不合） |
| 最大技术风险 | 调试端口暴露 + 平台风控误伤（新 profile 首次登录为"新设备"） |
