---
title: Curis Content Growth — Operating Strategy UX Translation（运营策略 → 产品体验翻译）
status: OPERATING STRATEGY UX TRANSLATION · DESIGN CANDIDATE（非 Frozen · 非高保真 · 非前端代码 · 非 Runtime/Connector）
date: 2026-08-16
purpose: 把《Operating Strategy Product Handoff》定义的「真实经营方法」翻译成「普通用户能理解、查看、修改、管理的 Curis 产品体验」。不重新解释 7 份运营研究；不把运营框架机械画给用户；不进入最终高保真。
source: docs/Content_Growth_Research/Curis_Content_Growth_Operating_Strategy_Product_Handoff.md（PRODUCT DESIGN HANDOFF FINAL · 唯一运营专业输入）
upstream_frozen:
  - Curis_Company_OS_Shared_Authority.md（Frozen · ⑥⑧⑦ + Context Isolation Truth Boundary）
  - Curis_Content_Growth_Domain_Authority.md（Frozen · ①②③④⑤ + Distribution Execution Policy + Capability Truth）
  - Curis_Workspace_Shell_Contract_And_Shared_Patterns.md（Frozen · P1–P7 · 四独立 Pane）
siblings:
  - Curis_Content_Growth_Strategy_Experience_Model.md（Doc 2 · Home/节奏/方向/账号/机会/社区/首启）
  - Curis_Content_Growth_Employee_Method_Experience.md（Doc 3 · 员工方式/对话驱动/来源组合/Token）
  - Curis_Content_Growth_Strategy_Evolution_Interaction.md（Doc 4 · 进化/学到的/提案 vs CEO）
  - Curis_Content_Growth_Core_Interaction_Spec.md（已 APPROVED CANDIDATE · 本轮标记 OPERATING STRATEGY INTEGRATION CANDIDATE）
---

# 0. 阅读指引

> 2026-09-15 Disposition: **CONSUMED SUBSET / PROVENANCE — NOT DEFAULT CURRENT INPUT**。账号经营与信息责任的已接受子集已写入[Content Growth Domain Authority §5.4](Curis_Content_Growth_Domain_Authority.md)及Current Master Map/UI Blueprint。下文保持原候选/研究/历史设计状态；不整体冻结8状态、4桶、Tabs或页面布局。后续普通设计不需重读研究来补产品。

- 本文件是**运营策略 → 产品体验的翻译总纲**。唯一运营专业输入是《Operating Strategy Product Handoff》；7 份运营 Research + Review + Overview 仅作 Reference，本文件不再自行解释整套运营研究。
- 本文件**定义翻译原则与映射**，不定义页面、字段、前端实现；落地细节在 Doc 2 / Doc 3 / Doc 4，三场景结构稿在 `Curis_Content_Growth_Wireframe_A/B/C_*.html`。
- 严格遵守《DOCUMENT CONSISTENCY CLEANUP》纪律：不制造不存在的 P8；Platform Facts 四态（VERIFIED/CONDITIONAL/UNKNOWN/UNAVAILABLE）而非写死数字；内部术语全隐藏。

---

# 1. 第一原则：不要把运营框架画出来

运营专家的内部视角是**经营逻辑**，不是产品界面要求：

- **八步飞轮**（Goal → Intelligence → Strategy → Operating Rules → Execution → Feedback → Learning → Strategy Evolution）是「经营如何闭环」的分析视角；
- **五层策略归属**（经营方向 / Account / Employee Method / Platform Facts / Operating Rules）是「策略如何归属」的分析视角。

**产品绝不能**把这两套内部架构机械呈现为用户要学习的对象：

| 不要做的事 | 为什么 |
|---|---|
| 画「八步飞轮流程图」给用户看 | 用户不需要理解经营架构；他只需要知道「现在在做什么、为什么、要不要改」 |
| 画「五层策略配置树」给用户配 | 归属是内部责任划分，不是用户侧的 5 层设置表单 |
| 把员工工作方式做成「工程配置后台」 | Employee Method ≠ 逐项配置的复杂面板 |
| 把 Token / 贡献度 / 权重公式暴露给用户 | 这些是内部逻辑层，普通用户无需也不应管理 |

**正确的翻译目标**：复杂的经营逻辑在底层**真实存在、真实运行**，但普通用户看到的是一组自然语言问题——

> 「现在公司怎么经营」
> 「AI 正在做什么」
> 「为什么这样做」
> 「最近学到了什么」
> 「哪里值得调整」
> 「我想改的时候怎么改」

设计者要做的，是把运营 Handoff 的每一段「能力 / 边界」翻译成上述用户语言下的**界面能力**，而不是把架构图搬上屏幕。

---

# 2. 翻译视角：运营概念 → 用户面问题

下表是总映射。每一行左侧是 Handoff 的内部概念，右侧是用户实际看到/能做的东西。详细落地见 Doc 2 / 3 / 4。

## 2.1 八步飞轮 → 用户感知（不画流程图）

| 飞轮步骤（内部） | 用户面呈现（自然语言 + 能力） | 落在哪个体验面 |
|---|---|---|
| Goal 目标 | 「这个方向为什么存在 / 最希望帮你做到什么」——首启问一个 Goal；经营方向页显示主/次目标 | Doc 2 §4 / §15 |
| Intelligence 情报 | 「重要平台机会 / 重要用户信号 / 信息雷达里最近加了什么源」 | Doc 2 §9–§10 / Doc 3 §8 |
| Strategy 策略 | 「当前策略摘要 / 当前策略提案 / 内容大致 Mix」 | Doc 2 §4–§5 |
| Operating Rules 规则 | 「当前经营节奏 / 为什么这样经营 / 今天怎么运行」 | Doc 2 §3 |
| Execution 执行 | 「正在生产什么 / 即将自动发布什么 / AI 在做什么」 | Doc 2 §2（Home） |
| Feedback 反馈 | 「最近用户在反馈什么 / 哪些需求在增长 / 账号异常」 | Doc 2 §10 |
| Learning 学习 | 「最近学到了什么」——轻量增量，可进 Evidence | Doc 4 §12 |
| Strategy Evolution 进化 | 「建议 / 观察中 / 已自动微调 / 需要 CEO 决定」四类区分 | Doc 4 §11 / §13 |

> **关键**：Home 不显示「飞轮第 N 步」，而是把各步的「用户感知」自然分布到信息层级中（见 Doc 2 §2）。只有「需要 CEO 决定」才上升到 P7 Decision Banner。

## 2.2 五层策略归属 → 体验面（不画配置树）

| 归属层（内部） | 用户面载体 | 用户怎么理解 |
|---|---|---|
| A. 经营方向 | 经营方向 Strategy Experience（Doc 2 §4） | 「这是这块业务现在的经营方法」 |
| B. Account | 账号 Strategy Experience（Doc 2 §5） | 「这个账号自己的目标/定位/节奏/最近表现」 |
| C. Employee Method | 员工方式查看 + 对话驱动（Doc 3 §6–§7） | 「他现在是怎么工作的」+「我想改就改」 |
| D. Platform Facts | 动态四态能力（不写死数字） | 「平台当前真实规则/活动，带 VERIFIED 等状态」 |
| E. Operating Rules | 当前经营节奏入口（Doc 2 §3） | 「今天怎么运行 / 哪些账号有自己的特殊规则」 |

> 归属是内部责任边界；用户侧**不出现**「Policy inheritance / Override hierarchy / Account Pool / Target Account Set」等词。用户只自然说「默认这样运行 / 这个账号单独设置 / 这一次例外」。

## 2.3 Source Strategy → 信息雷达（Doc 3 §8）

来源组合、分层、扫描频率、暂停、贡献/质量趋势、AI 建议加入/降频/删除 —— 全部翻译为「信息收集员工的信息雷达」体验；**贡献度公式 / 阈值 / 权重不进首版**。

## 2.4 Topic / Content / Audience / Publishing / Analytics

- 机会面（Doc 2 §9）：为什么值得做 / 来自哪里 / 服务哪个目标 / 适合哪些账号 / 时效性。
- 社区闭环（Doc 2 §10）：评论 → User Signal → 用户洞察 → Content Opportunity，在 Home / Employee / Journey / Utility 各自不同深度出现。
- 发布演化（Doc 2 §5 / Handoff §10）：用户能区分「平台通用建议」vs「本账号数据学到的建议」。
- 分析（Doc 4 §12 / Handoff §11）：指标跟经营目标挂钩，**默认不把播放量当成功**；每条策略建议可见 观察/证据强度/建议/影响/可回滚。

---

# 3. 跨切面纪律（贯穿所有文档）

| 纪律 | 要求 |
|---|---|
| 第一原则 | 不画八步飞轮流程图、不画五层配置树、不做工程配置后台 |
| Platform Facts | 只消费 VERIFIED/CONDITIONAL/UNKNOWN/UNAVAILABLE 四态；**禁止写死任何研究数字**（权重/频率/最佳时间/流量池/算法数值一律 REFERENCE/NEEDS VERIFICATION） |
| Context Isolation | 引用统一用「Context Isolation Truth Boundary」（来自 Company OS Shared Authority）；**无正式 P8 Authority，不得制造 P8** |
| 内部术语隐藏 | 用户产品身份只使用 Workspace；legacy Office / OfficeAccountBinding 仅作 implementation / migration provenance，不在 Current UI 显示。禁词：Account Pool / Target Account Set / HIGH_REUSE / FULL_DIVERGENCE / Variant / reuse_mode / Queue·Bottleneck（⑨ VISION/RESERVED）/ Policy inheritance / Routing·Assignment·Capacity / Token 计数·贡献度原始分·w1–w8 公式 |
| 员工数量 | **不固定创建 5 个 Employee**；一个员工可承担多职责，未来业务增长再拆；不破坏 Company OS Frozen Organization 语义 |
| Token / 成本 | 不设计 Token Budget Slider / Context Window / Embedding / RAG 配置作为首版 UI；表达为「重点关注 N 个固定来源 + 平台热点 + 用户评论」而非「全网实时扫描」 |
| 两套配置禁止 | 对话驱动（Conversation）与直接编辑（Direct Edit）**修改同一份长期经营方法**，不允许两套独立存储 |
| 未越界 | 不修改 Frozen Authority / Blueprint / XHS·RD / Runtime / Connector / 代码 / UI；不进最终高保真；不新建业务 Primitive |

---

# 4. 子文档索引与本轮范围

| 文档 | 覆盖 Brief 章节 | 关键新增 |
|---|---|---|
| **Doc 2 Strategy Experience Model** | §2 Home IA / §3 经营节奏 / §4 方向 / §5 账号 / §9 机会 / §10 社区 / §15 首启 | 新 Home 8 问信息层级；经营节奏渐进披露；方向/账号策略体验；机会解释维度；社区四度分布；Goal 首启 |
| **Doc 3 Employee Method Experience** | §6 员工方式 / §7 对话驱动 / §8 来源组合 / §14 Token / §16 不固定5员工 | 「他现在怎么工作」；3 个对话场景→同一份方法；信息雷达；Token 用户语言 |
| **Doc 4 Strategy Evolution Interaction** | §11 进化三类 / §12 学到的 / §13 提案 vs CEO | AI 自主微调留痕 / 策略提案 / CEO 主动改；最近学到了什么轻量出现；四类区分 |
| **Core Interaction Spec（更新）** | — | 标记 OPERATING STRATEGY INTEGRATION CANDIDATE；指向本批文档；三场景保持 APPROVED CANDIDATE 不动 |
| **Wireframe A/B/C（中保真）** | §17 关键新增场景 | A 经营策略/当前经营方式 · B 员工方式/来源组合 · C 策略提案/最近学到了什么 |

> 本轮**不重新画** First-Run / Home / Journey 全套结构稿（已 APPROVED CANDIDATE）；仅对 A/B/C 三类**关键新增场景**补中保真结构稿。

---

# 5. 状态（Translation Closure）

```text
CONTENT GROWTH OPERATING STRATEGY UX TRANSLATION
APPROVED CANDIDATE
```

## 5.1 Translation Closure：APPROVED WITH 5 DELTAS（T1–T5 · 就地修正，未新增文档）

| DELTA | 修正点 | 落到 |
|---|---|---|
| **T1** 经营方式 = 聚合入口 | 经营方式只是 SUMMARY/ENTRY SURFACE，不拥有全部策略；真实策略仍归属 经营方向 / Account / Employee Method / Operating Rules / Platform Facts；只聚合+下钻，不演化成 Strategy Settings Center | Doc 2 §3.3 |
| **T2** CEO 主动命令不得再次 P7 | CEO 明确指令 = 已决策 → 直接更新策略/临时 Operating Rule → 留痕 → 执行；歧义仅自然追问，不二次批准；仅 AI 主动提结构性长期变化才进 P7 | Doc 3 §3.1 C · Doc 4 §4 C |
| **T3** AI 自主微调须在授权边界内 | 须有 Operating Boundary/Authorized Range；不在授权范围不得静默改；用户语言不暴露 Policy Boundary；三要件：授权范围 / 留痕 / 可回滚 | Doc 4 §1 表 · §2 A |
| **T4** Demo Evidence 明确标识 | 所有结构稿示例数字标 Illustrative/Demo；不误认真实 Analytics；UNAVAILABLE/UNKNOWN 不伪造 Learning Evidence | A/B/C 结构稿 + Doc 4 §5.1 |
| **T5** Employee Detail 必须保持 Shared 一致 | Employee 是 Company OS Shared Employee；CG 只在 Shared Employee Detail 内加「工作方式」扩展 Section（职责决定内容），沿用 Shared 露出方式（点员工→右侧详情），不改成 Main 独立页 / 不新建 Employee Method Workspace / 不改全局露出；Shared≠Shared Context | Doc 3 §1.1（含 §1.1.6 若 Shared 权威不足仅记 `SHARED EMPLOYEE DETAIL DELTA CANDIDATE`）· Wireframe B 重写 |

**KEEP 全部保持**：总体翻译模型 / Home 8 问 / 「经营方式」用户词 / 方向·账号 Strategy Experience / First-Run 只问一个 Goal / Employee Method / Conversation+Direct Edit 同一份方法 / Source Portfolio / Token 隐藏 / Opportunity 解释 / 评论→User Signal→Opportunity / 最近学到了什么 / 提案≠Needs CEO / 进化三类 / Platform Facts 四态 / 不固定 5 员工。

```text
CONTENT GROWTH OPERATING STRATEGY UX TRANSLATION CLOSED
VISUAL DESIGN DEFERRED
WAITING FOR WORKSPACE ENGINEERING REVIEW
```

（**不进入最终高保真**。`READY FOR VISUAL DESIGN PLANNING` 易误读为可立即启动，故改为 VISUAL DESIGN DEFERRED：当前 Workspace Engineering Methodology 与 Workspace Runtime / Extensibility Audit 正在进行，在确认未来 Workspace 如何被搭建、如何动态加载、Declarative / Extension 边界之前，不启动最终高保真。未改任何 Frozen / Blueprint / Shell / P1–P7 / XHS·RD / Runtime / Connector / 代码 / UI；内部术语全隐藏；无 P8。）
