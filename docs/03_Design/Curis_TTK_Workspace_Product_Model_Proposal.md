# Curis 抖音 / TikTok Workspace — Product Model Proposal

**阶段**：TTK PRODUCT MODEL RESEARCH ONLY  
**状态**：TTK PRODUCT MODEL REVIEW REQUIRED  
**不修改**：Product Blueprint / Frozen Shell / Frozen Shared Patterns P1–P7 / XHS Instance / RD Instance / Runtime / 正式代码  
**输入**：`Curis_TTK_Workspace_Reference_Research.md`（外部证据）、Frozen Shell Contract + Shared Patterns P1–P7、XHS Instance Spec、RD Instance Spec、CURRENT_STATE.md、Product Blueprint 抖音行  
**铁律**：**不预设「抖音 = 小红书视频版」**。本提案基于真实工作流独立推导。

> 标注：`INF`=研究推断，`CURIS`=对 Curis 的建议，`FACT`=已 frozen/已验证事实。推断与建议区分呈现。

---

## A. 真实业务工作链与责任判定

**链（INF，多源收敛，见 Reference §1）**：
选题/热点 → 脚本 → 素材准备 → 拍摄或AI生成 → 剪辑 → 审核 → 排期 → 发布 → 数据观察 → 复盘 → 二次利用

**逐项判定（首版核心 / 高级 / Tool Execution / 真 Employee Responsibility / Handoff / Artifact Review / System Activity）**

| 环节 | 归类 | 理由 |
|------|------|------|
| 选题/热点 | 真 Employee Responsibility（内容策划）+ System Activity（趋势监控） | 选题方向是判断型责任；热点监控可自动化 |
| 脚本 | 真 Employee Responsibility（编剧） | 脚本结构/钩子/品牌声音是编辑判断，AI 去不掉（S19） |
| 素材准备 | Tool Execution + Asset 管理 | 收集/整理素材是执行；素材库是对象 |
| 拍摄/AI生成 | Tool Capability（执行）+ 制作员工责任（方向/审美） | 剪映/Runway 是工具；「做成什么样」是责任（S10/S18） |
| 剪辑 | Tool Capability（执行）+ 制作员工责任（成片判断） | 同 RD：工具动作≠员工责任 |
| 审核 | 真 Employee Responsibility（内容审核） | 合规/品牌/版权是判断型，敏感内容留人（S18/S19） |
| 排期 | Tool Capability（自动化 by default）+ 发布运营责任 | 排期可自动；但「何时发/借力热点」是判断 |
| 发布 | 真 Employee Responsibility（发布运营）+ Tool Capability | 发布动作可工具化；发布策略是责任 |
| 数据观察 | **System Activity**（Current Executor=none） | 自动聚合平台回执，非员工岗位（类比 XHS） |
| 复盘 | System Activity（自动反哺）+ 可选 Employee（数据复盘解读） | 数据→选题库反哺自动化；深度解读可留员工（高级） |
| 二次利用 | System Activity（内容复用推荐）+ 可选发布运营 | 一条多平台/矩阵是自动化+分发责任 |

**Handoff / Artifact Review 边界（采用 Frozen P5 + RD 两类交接）**
- 策划 → 脚本 → 制作 → 审核 → 发布：**责任真正转移时 = Frozen Handoff Event**。
- **制作把成片送审核 = Artifact Review Request（责任未转移）**，类比 RD「代码送审」：制作员工仍持该 Video 的制作责任，审核员工只做合规/品牌/版权检查（**不升格为 Frozen Handoff**，保持 Instance Candidate，与 RD 一致）。
- **不为了多 Agent 创造岗位**：真实责任角色仅 6 个（见 §E），不增设伪岗（如「数据分析员工」已被 XHS DO NOT COPY 禁止，本条继承）。

---

## B. 核心 Business Object（对象层级）

**结论（CURIS）**：
- **Video 是核心 Content Object**，类比 XHS 的 Note——是用户长期追踪、跨生命周期管理的原子交付物。证据：所有运营文献都以「每条视频」为追踪单位，按视频看 完播率/互动/涨粉（S2/S3/S7）。**Video 应像 Note 一样成为长期追踪核心 Content Object**。
- **Script 是 Video 的 working Artifact / 子对象，不是顶层独立业务对象**。证据：脚本紧密绑定单条视频（1 视频≈1 脚本），但优秀脚本可版本化、沉淀为「脚本库」供复用（S2/S4/S15）。→ Script = Video 下的第一级子对象（可版本化、可另存为模板进 Context 脚本库），**不**升为与 Video 平级。
- **Asset / Shot / Scene 不是顶层对象**：Asset（素材/stock/B-roll/avatar/BGM）是**可复用库项**，被 Video 引用；Shot/Scene 是 Production Result 的内部构成，属 Video 生产子树，**不**单独升格。

**推荐对象层级（CURIS）**：
```
Workspace（抖音运营办公室）
 └ Campaign（可选分组层 · RESERVED，如「618 大促」主题批量）   ← 首版可无
      └ Video（CORE Content Object · 长期追踪）
           ├ Script（子对象 / working artifact · 可版本化 · 可存为模板）
           ├ Assets（引用的生产输入：footage / BGM / stock / avatar）
           ├ Production Result（成片文件 + 版本）
           ├ Publish Result（回执：平台 / 时间 / 状态 / 链接）
           └ Analytics（单 Video 指标：完播率 / 两秒跳出 / 互动率 / 涨粉 + InteractionItem）
```
> 与 XHS 的关键差异（CURIS）：XHS 的 Note 生产子树轻（封面/标题/正文/标签）；TTK 的 Video 生产子树**更重**——多出一个独立的 **Script 子对象**与 **Assets/Production Result** 结构，因为视频生产比图文重。这正是「不能把 XHS 换成 Video」的结构性原因。

**明确不升一级**：Campaign、Script、Asset、Shot、Scene 均不默认升为与 Video 平级的核心对象（Campaign 仅作可选分组，首版可后置）。

---

## C. 默认工作面（最重要问题之一）

**结论（CURIS）**：**TTK 默认工作面 = Video Production Pipeline（按阶段）**，而非 Calendar。

**比较与判断**：
| 候选 | 判断 | 理由 |
|------|------|------|
| A 发布日历 | ❌ 不做默认 | 日历是「生产完成后的末端视图」（S6/S7/S8/S15 反向证据）；Buffer/Later 的日历假设内容已生产完 |
| B 生产管线/Board | ✅ **推荐默认** | 生产是 TTK 核心；批量生产下用户同时管多条不同阶段的 Video（S4/S7）； burning question 是「每条视频做到哪一步了」 |
| C 视频库 | ⚪ 辅助 | 适合回顾/检索，不做第一眼 |
| D 今日/生产队列 | ⚪ 辅助（可作顶部 Attention） | 「今天在产什么/待我」是好摘要，但不替代管线总览 |
| E Campaign 视图 | ⚪ 高级 | 主题批量管理，首版可无 |
| F Timeline | ⚪ | 时间轴适合呈现发布节奏，但非生产核心 |
| G 混合 | ✅ 采用（以 B 为锚） | Pipeline 为主面 + 顶部 Attention（待CEO/失败/待发布）+ Workspace Header 概括 |

**为什么（CURIS）**：
1. 生产比发布更重、更分化——这是 TTK 与 XHS 的根本差异（XHS 图文轻，日历主导成立；TTK 视频重，管线主导成立）。
2. 批量生产模式（S4/S7）天然产生「多 Video × 多阶段」的管理需求，Pipeline/Board 直接承载。
3. 与 Frozen Shell Contract 自身指引一致：短视频 →「**时间轴 / 视频生产为核心**」（Shell Contract §0.1 边界修正 2）。本结论**纠正**任何「XHS 换成 Video 就是 TTK」的漂移。
4. 顶部 Attention 优先（继承 XHS P0 规则）：Pipeline 中 `needs_ceo` / `failed` / `ready-to-publish` 的视频置顶，满足「用户进入第一眼先知道什么需要我」。

**TTK 默认工作面 = Video Production Pipeline（按阶段：选题→脚本→制作→审核→发布→数据），顶部 Attention 优先 + Workspace Header 概括。**

---

## D. Video Selected 后的专业工作面（Main / Context / Utility）

采用 Frozen 四独立 Pane（Top-aligned Independent Pane），TTK 实例化：

**Main（专业业务主工作面）**
- 顶部：该 Video 的**生产阶段指示**（当前处在 选题/脚本/制作/审核/发布/数据 哪一阶段）+ Workspace Header（`抖音运营办公室 · N条在产 · M条待CEO · K条已发布观察中`）。
- 中部：**该 Video 责任链的 Employee Workstation 垂直栈**（策划→脚本→制作→审核→发布，各为一个 Workstation，采用 Frozen §3.1 状态模型 + RD 自由多开）。每个 Workstation = 一个 Responsibility（类比 RD 的 R1/R2/R3，但此处是视频生产责任链）。
- 顶部 Decision Banner（仅当 needs_ceo）：Frozen §3.3 + P7，出现在 Main 顶部，不占员工卡。
- 复用：与 RD 的「垂直栈 Workstation + Decision Banner」同构，但**内容是视频生产责任链**，非研发责任。

**Context（左 · T2 · Adaptive）— TTK 声明内容**
- **选题库 / 热点**（类比 XHS 选题库，但这里是趋势热词/竞品/热点，来源可接 巨量算数/蝉妈妈/飞瓜 类能力）：提供创作上下文。
- **脚本库 / 参考视频 / Brand Knowledge**：脚本模板复用、参考片、品牌调性。
- 空态不显示入口（Frozen §2.2）。

**Utility（右 · T3 · Adaptive）— TTK 声明模式集（多模式，由 Instance 声明）**
- 视频预览（Video Preview）
- 脚本预览（Script Preview）
- 素材预览（Asset Preview）
- 字幕 / 封面（Caption / Cover）
- 发布结果（Publish Result · 回执/状态）
- 数据（Analytics · 单 Video 指标）
- 机制沿用 Frozen §2.3 / §3.4（Result Reference 轻量引用开对应模式；Utility Maximize 全屏 Overlay）。

> 不照抄 XHS 的「图文预览」——TTK Utility 以 **视频预览 + 脚本预览 + 数据** 为重心，模式更多（视频类天然多形态）。

---

## E. AI Employee Collaboration（责任角色与 Frozen Pattern 应用）

**真实需要的责任角色（CURIS，不为多 Agent 而造岗，共 6 个）**：
1. **内容策划**（Content Strategist）— EMPLOYEE RESPONSIBILITY：选题方向、热点判断、账号定位。
2. **编剧**（Scriptwriter）— EMPLOYEE RESPONSIBILITY：脚本结构、钩子、品牌声音。
3. **视频制作/剪辑**（Video Producer）— EMPLOYEE RESPONSIBILITY（方向/审美/成片判断）+ 调用 Tool Capability（剪映/Runway/即梦 执行）。
4. **内容审核**（Content Reviewer）— EMPLOYEE RESPONSIBILITY：合规/品牌/版权判断。
5. **发布运营**（Publish Ops）— EMPLOYEE RESPONSIBILITY：排期策略/标签/发布；排期动作可自动化。
6. **数据复盘**（Data Analyst）— **可选/高级**：System Activity 自动聚合数据，深度解读+下一批建议可留员工（避免造「数据复盘员工」伪岗；默认 Analytics = System Activity，与 XHS 一致）。

**Tool Capability（非员工）**：剪映/CapCut 动作、自动字幕、比例转换、BGM、即梦/Runway/HeyGen 生成、多平台分发（易媒类）——均属执行能力。

**责任链与交接**：
```
策划 → 脚本 → 制作 → 审核 → 发布
```
- 真正责任转移 = Frozen Handoff（P5）。
- 制作送审核 = **Artifact Review Request（责任未转移）**，类比 RD 代码送审；制作员工仍持该 Video 制作责任。
- 发布后数据 = **System Activity**（Current Executor=none，自动化 by default，P4）。

**Frozen Pattern 应用清单**：
- 三层责任（P1）：Object Owner（抖音运营办公室，稳定）≠ Current Responsibility（阶段）≠ Current Executor（可为 none）。
- Employee Presence（P2）：贴在 Video 卡/责任链上的轻量责任存在（策划·李翔 制作中），不显 Object Owner。
- System Activity（P3）：数据观察/自动字幕/自动排期/复用推荐，无头像、不冒充员工。
- Automation by default（P4）：完成自动 Handoff、发布自动进 Analytics、复盘自动反哺选题库。
- Handoff（P5）：责任转移轻量呈现。
- Result Reference（P6）：对话内轻量引用（🎬 视频预览 ▸ / 📊 完播数据 ▸）开 Utility。
- CEO Decision Package（P7）：见 §F。

---

## F. CEO Decision 场景（Frozen P7 应用）

**值得打断 CEO 的真实场景（CURIS，基于业务/风险）**：
- 品牌方向（定位/人设重大调整）
- 争议内容（可能引发舆论风险）
- 版权风险（生成素材/音乐/BGM/数字人 侵权）
- 合规风险（AI 披露、广告法、平台政策）
- 明显成本增加（DOU+/千川投放、即梦/Runway API 额度）
- 投放预算（付费推广额度确认）
- 重大发布时间改变（借力热点时机 / 全局排期冲突）
- 对外承诺（商务合作 / 品牌联名 / 达人约定）

**绝不自动升级为 CEO Decision（CURIS，对应 Frozen P7 + 研究证据 S18/S19/S20）**：
- 剪辑失败 / 模型失败 / 工具未连接 / 上传失败 / 普通技术异常 → 属 System Activity / Tool 失败 / 重试，AI 自行恢复，**不**打扰 CEO。
- 自动提取高光选错上下文（S20）→ 走 Artifact Review / 员工复核，非 CEO。

**Frozen P7 结构应用**：问题 → 方案 → 影响/风险/代价（带 Provenance FACT/POLICY/EVIDENCE/EST/UNK）→ Employee 推荐 → CEO 选择 → AI 自动继续（决策后不新建 Handoff）。高风险/不可逆（如投放预算、版权对外承诺）Layer 0 只 `[查看方案][暂缓]`；低风险合规微调用 `[按建议处理][其他方案][暂缓]`。

---

## G. 与 XHS 的复用边界（摘要，详见独立 Matrix 文件）

| 维度 | REUSE FROM SHARED | REUSE FROM XHS（模式/底层，非UI） | TTK-SPECIFIC | DO NOT COPY FROM XHS |
|------|-------------------|-----------------------------------|--------------|---------------------|
| Shell | 四独立 Pane / Toggle / Search / Resizable | — | — | — |
| 责任语义 | P1–P7 全采用 | — | Video 生产责任链实例化 | — |
| 默认面 | — | — | **Pipeline（非 Calendar）** | **不默认 Calendar** |
| 核心对象 | — | Content Object×Time 概念 | **Video（带 Script 子树）** | **不把 Note 当 Video 直接搬** |
| Context | — | 选题库模式（adapt） | 选题库/热点 + 脚本库 | 不照搬图文选题 |
| Utility | — | 预览模式机制（adapt） | 视频/脚本/素材/字幕封面/数据 | 不照搬图文预览内容 |
| Analytics | System Activity 模式 | 闭环反哺模式（adapt） | 完播率/两秒跳出/互动率 | 不复制收藏率等小红书指标 |
| 员工协作 | Workstation/Presence | Split Working 模式（adapt） | 视频责任链栈 | 不造「数据复盘员工」 |
| 审核 | Artifact Review 模式 | — | 制作送审核=Artifact Review | — |
| Decision | P7 | 合规类简单动作模式 | 投放/版权/合规高风险 | — |

---

## I. 最终结论（明确输出）

| 项目 | 结论 |
|------|------|
| **核心 Business Object** | **Video**（长期追踪的 Content Object，类比 XHS 的 Note，但带更重的生产子树：Script/Assets/Production Result） |
| **对象层级** | Workspace →（Campaign 可选分组·RESERVED）→ **Video** → {Script, Assets, Production Result, Publish Result, Analytics} |
| **默认工作面** | **Video Production Pipeline（按阶段：选题→脚本→制作→审核→发布→数据）**，顶部 Attention 优先 + Workspace Header 概括 |
| **核心工作模型** | **Pipeline-driven content production**（非 Calendar-driven） |
| **Main** | 该 Video 责任链 Employee Workstation 垂直栈 + 顶部生产阶段指示 + Decision Banner（needs_ceo 时） |
| **Context** | 选题库/热点 + 脚本库/参考视频/Brand Knowledge（左 T2） |
| **Utility** | 视频预览 / 脚本预览 / 素材 / 字幕封面 / 发布结果 / 数据（右 T3，多模式） |
| **核心 Employee Responsibilities** | 内容策划、编剧、视频制作、内容审核、发布运营（+可选 数据复盘解读） |
| **System Activities** | 数据观察/自动 Analytics 聚合、自动字幕/比例（若自动化）、自动排期、内容复用推荐 |
| **首版最重要的 3–5 个状态** | 生产中(working)、待审核/审核中、待CEO(needs_ceo)、待发布/已排期、已发布·数据观察 |
| **DESIGN NOW** | Pipeline 默认面 + Video 对象 + 责任链 Workstation + 选题库 Context + 视频预览 Utility + 审核 Artifact Review + 数据 System Activity + CEO Decision P7 |
| **RESERVED** | Campaign 分组层、多平台矩阵分发、AI 生成视频深度集成（Runway/HeyGen/即梦）、脚本库复用市场、深度达人/竞品监控、专业剪辑(Premiere 级) |
| **DO NOT COPY** | 不默认 Calendar、不把 Video 当 Note 直接搬、不照搬图文字段、不复制小红书指标（收藏率）、不造「数据复盘员工」伪岗、不把工具动作当 Employee 责任、不把技术异常升为 CEO Decision |
| **证据不足·需后续验证** | ①真实平台 API 字段/完播率口径（UNK，需连接验证）②AI 生成视频执行边界（成本/披露/一致性丢弃率，S18）③批量下 Main 栈 Workstation 密度性能 ④Campaign 是否首版需要 ⑤外部平台回执真实对接 |

---

**状态**：TTK PRODUCT MODEL REVIEW REQUIRED  
**下一步**：待 Review 批准后，方可进入「TTK Instance Spec 固化 / 高保真 / 设计」阶段（不在此轮）。

**UI Designer** · 2026-08-15 · RESEARCH ONLY（未修改任何权威文档）
