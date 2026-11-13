---
status: Draft (Research)
authority_class: RESEARCH
disposition: 待 CEO 评审
owner: VisualStorytellingExpert
created: 2026-08-20
next_action: CEO 接收研究 → 选定视觉方向 → 委托 Trae 输出高保真竞争稿
frozen_source: 不修改 — 本文件不替代任何 Frozen Authority
---

# CURIS VISUAL DIRECTION RESEARCH
## Product Desirability × Visual Direction Research

> 本文件只定义未来所有高保真设计必须遵循的 **Visual Quality Bar**、**Visual Direction Evidence**、**Product Desirability Principles** 与 **三个候选方向**。它不是 Product Blueprint / Master Map / UI Blueprint / Design System / 高保真 UI 的替代品，也不是最终设计稿。
>
> 任何设计稿在进入 Curis 之前，都必须通过本文定义的 **Visual Quality Rubric** + **Desirability Gate**。

---

## 0. 上下文与本研究的边界

- **产品**：一人公司自动任务与工作流系统（Desktop App）
- **当前产品逻辑**：基本稳定（Blueprint v4.4 / Master Map / Frozen UI Spec 已定）
- **本研究的使命**：在不改变产品逻辑的前提下，让 Curis 成为「**第一眼精致、成熟、有说服力**」的视觉产品
- **不做什么**：
  - 不重画产品架构、不动 Blueprint / Master Map / UI Blueprint
  - 不动 Design System / Frozen `--ui-*` token / 高保真原型
  - 不产出最终 Curis 高保真页面（本轮只定义方向）
- **何时进入下一步**：CEO 明确选择「这个方向我愿意每天用」之后，才由 Trae 在同一 CEO Desk / 同一 Product Truth / 同一信息结构上出三张高保真竞争稿。

---

## 1. Executive Summary

### 1.1 核心结论（先看这一段）

1. **Curis 当前最大的视觉风险不是缺 token，而是「功能密度高但视觉权重分布错误」**。研读 Linear / Raycast / Stripe / Craft / Arc 之后反复确认一件事：高级的桌面生产力产品不是用更少元素，而是**让每个元素挣到自己的视觉权重**。
2. **「这是我的公司」不是视觉口号，是视觉结构**。CEO Desk 必须能让人一眼看到「今天公司发生了什么」——但不能变成 Dashboard。要做到这一点，必须用「注意力锚点 + 安静背景」而不是「满屏 Card + 数字」。
3. **AI 必须在 Curis 里"隐形存在"**，而不是被装饰。AI 不需要专属按钮、不需要专属色、不需要专属面板。它是「你公司里的一个员工」，和你自己的员工用同一种语言、同一种权重出现在 Home 里。
4. **Curis 的视觉气质排序（详细论证见 §15）**：
   - PRIMARY：**Calm · Precise · Executive · Trustworthy**
   - SECONDARY：**Alive · Human · Intelligent**
   - AVOID：**Playful · Decorative · "AI-futuristic" · Enterprise-busy**
5. **建议三个候选方向**（详见 §19），都已在 Frozen `--ui-*` token 范围内具有可行性；不在本研究内冻结主题或 Hex。

### 1.2 本研究的几个关键判断

- **Card 必须"挣到自己的边界"**。当前原型里 Card 用得太松：很多信息块只是「看起来像 Card」，而不是「结构上必须是 Card」。本研究给出 Card Discipline（§7）。
- **Typography 是 Curis 中文桌面 UI 精致感的最大杠杆**，不是颜色。中文字号 / 字重 / 行高 / 间距的研究比 Linear 那种英文指标多出一层颗粒度（§5）。
- **Motion 应优先 Functional > Delight > Decorative**。当前原型在 Decorative 上投入过多，会让"AI 公司正在运转"的语义被装饰噪音淹没（§9 / §10）。
- **Light / Dark 不在本研究冻结**。但三个方向里各有一种倾向：B 偏 Dark-first、A 偏 Light-first、C 偏「Light-first + 可切 Dark」。

---

## 2. Why Previous UI Attempts Likely Failed

> 旧 UI 反复迭代但总觉得「不够高级」的根本原因，不是 token 不对、不是字体不对，而是**信息架构与视觉权重之间的契约没立起来**。以下是来自参考产品反推的常见失败模式。

### 2.1 失败 #1：把「产品能力多」翻译成「屏幕上元素多」

- **表现**：每个能力都获得一个 Card / Tab / Panel / Status pill。于是首屏同时出现 8 个能力、12 个状态、5 种 pill 颜色。
- **为什么错**：用户不读能力清单，用户读「我现在该做什么」。当所有能力视觉权重相等，注意力就被稀释。
- **参考**：Stripe Dashboard 主动把首页 metric 砍到「3–5 个决策相关」，并明确说"the metrics on the home screen are the ones that change your behaviour, not the ones that are simply available"（925Studios, *Stripe Dashboard Design Breakdown*）。Linear 用同样的取舍把"工程团队注意力"作为首页唯一 metric。

### 2.2 失败 #2：把「AI」当作装饰主语

- **表现**：单独 AI 按钮 / 专属 AI 色 / AI sparkle 角标 / AI Agent 卡片墙 / "Running…" 状态横条。
- **为什么错**：用户应该感觉「公司里有一个员工叫 AI」，而不是「我在用一个 AI 后台」。AI 作为独立模块曝光，会强化"我在管理工具"而非"我在经营公司"。
- **参考**：Claude Design（Anthropic Labs, 2026）的反 AI-味设计哲学里明确："用户关心吗？推动了叙事吗？去掉之后页面还看得懂吗？有更简洁的方式吗？服务的是用户还是设计师？" 五问测试里，前两问会直接杀掉所有"装饰性 AI"。

### 2.3 失败 #3：用 Card 模拟层级，而不是用 Whitespace / Type 模拟层级

- **表现**：每个 section 用一个圆角矩形套起来，section 之间用空白；Card 内部再用空白；Card 之间再留 24px gutter。结果是"卡片墙"。
- **为什么错**：当 Card 是默认容器时，Card 就不再承担"语义边界"的责任——它只是"一个装饰"。
- **参考**：Notion / Craft 都明确区分 Card、Section、Divider、Whitespace、Surface、Popover 的使用场景。Notion 的 Sidebar 项是 List 不是 Card；Craft 的 Card 只在"对象就是一张卡片"时使用。

### 2.4 失败 #4：把「精致」等同于「颜色 + 渐变 + 圆角」

- **表现**：渐变紫、玻璃态、强对比阴影、大圆角、emoji、插画点缀。
- **为什么错**：真正的精致来自**克制的类型层级 + 严谨的间距节奏 + 一致的微观交互**，不是来自颜色。Linear 是反例——单一 indigo accent、几乎全 grayscale，但被反复评为"最精致"。
- **参考**：Linear DESIGN.md 明确写："A single accent color, one negative-tracking display family, and four surface lifts produce a marketing page that reads as software-craft documentation."

### 2.5 失败 #5：长时段使用没被设计

- **表现**：饱和色状态指示、强对比警告文字、永远在场的 Sidebar、AI 状态徽章持续闪烁、动效叠动效。
- **为什么错**：Curis 不是营销站。用户每天用 4–8 小时。Stripe / Linear / Notion 都在长时段使用上做了大量"低调"决策。
- **参考**：Raycast Compact Mode（按用户偏好隐藏所有非核心元素）直接证明"用户主动选择更少东西"是被尊重的能力。

### 2.6 失败 #6：导航、状态、徽章、标题在视觉权重上不分

- **表现**：H1 / 菜单项 / 状态徽章 / 按钮文字 同字号、同字重、同颜色。
- **为什么错**：当一切权重相等，用户不知道看哪里。Stripe 用了 6 个字号 + 3 个字重明确切层级。
- **参考**：aidesigner.ai *How to Design a Dashboard UI (2026)* — "Cards do not need shadows. A 1px border at 8% opacity reads cleaner and ages better than the standard 'soft drop shadow' most templates ship with. Linear and Vercel both ship with borders, not shadows, and their dashboards feel modern years later."

### 2.7 失败 #7：把"AI 公司正在运转"翻译成"实时数据 + 状态徽章"

- **表现**：右下角 Live 状态、AI 思考中动画、运行中 spinner、"5 个 Agent 在线"徽章。
- **为什么错**：运转感来自**结果可见 + 责任可追 + 决策可触**，不来自"屏幕在动"。
- **参考**：Craft 不展示任何"系统状态"，但每次进入应用你能立刻看到你的内容变了——这就是"运转"。

### 2.8 失败 #8：没有把 CEO 当成"真实用户"

- **表现**：CEO Desk 像管理员控制台——一堆 metric、操作按钮、状态 filter。
- **为什么错**：CEO 应该像在办公室里巡视——看到自己今天做的几个决定、几个结果、几个待定的事。不是看 dashboard，是"看到公司"。
- **参考**：Apple Notes / Bear / Things 3 这种"个人 App"用空白和节奏替代 dashboard，但让人能感受到"这是我的空间"。

### 2.9 失败 #9：把「高保真」等同于「Figma 写实」

- **表现**：花大量精力模拟真实图表、真实插画、真实图片，但交互是"按钮+跳转"。
- **为什么错**：高保真的关键是**真实可点击的真实反馈**，不是真实图片。Raycast / Superhuman 的视觉真实感来自"动作真的发生"，不是来自图片精度。
- **参考**：Raycast 官方设计原则三条："fast, simple, delightful"——视觉真实感 = 反馈真实感。

### 2.10 失败 #10：在 Frozen 之后缺乏 Visual Quality Gate

- **表现**：每次高保真迭代靠主观判断；"看起来不够高级"反复出现；没人能说清为什么不够高级。
- **为什么错**：没有 gate 就没有判据。
- **解决**：本研究 §17 / §18 输出可执行的 Rubric + Gate，作为下一轮高保真迭代的硬门槛。

---

## 3. Reference Product Matrix

> 本节给每个参考产品定义「我们想从它那里拿走什么」与「我们绝对不要照搬什么」。后续章节的所有原则都可以在这里溯源。

| 产品 | 主要借鉴原则 | 主要警惕 | 在 Curis 中的翻译 |
|---|---|---|---|
| **Linear** | 单一 accent · hairline 边界 · 4–6–12 radius · scale(0.97) press · Inter Variable 16px body · 近黑 canvas · 4px grid | 不要把 Linear 直接做成 Curis 的视觉 —— Linear 是"工程团队的工具"，不是"经营公司" | 把"克制的视觉权重"作为质量基线；用 hairline 而非 shadow 做层级 |
| **Raycast** | fast/simple/delightful 三原则 · 放大搜索条作为视觉锚 · Compact Mode（用户主动选择更少） · action bar 把快捷键教给用户 · tasteful Liquid Glass · 自有 icon set | 不要照搬"command bar + extension store"的形态 —— Curis 不是 launcher | 把"放大主交互"和"主动让用户少看东西"作为 motion / chrome discipline |
| **Craft** | block model 的克制 · 字体/间距/动画/颜色四个维度同样考虑 · 苹果生态 native feeling · "design-led" 信念 · "objects that feel polished" | 不要把 Curis 做成 Craft —— Craft 是文档工具，没有"经营"语义 | 把"中文混排精致度"和"块级对象的层级"作为质量基线 |
| **Notion** | 渐进披露 · 内容优先 · hover actions · 长期使用可承受 · sidebar 是 list 不是 card · 空白当结构 | 不要照搬 Notion 的 block-based editor —— Curis 不是编辑器 | 用"空白当结构"代替 Card 当结构；sidebar 用 list |
| **Stripe Dashboard** | jobs-to-be-done nav（不是数据模型 nav）· 6 个字号 3 个字重 · sparse density · 关键 metric 优先 · microcopy 承担信任 · 乐观 UI + skeleton · 智能 autofill · "purple = action" 单一行动色 | 不要把 Curis 做成后台数据 dashboard —— Curis 是经营仪表，不是财务后台 | 把 nav 用 jobs 命名；用 microcopy 承担"我这家公司正在运转"的信任 |
| **Superhuman** | 100ms 规则 · keyboard-first · Split Inbox · Remind/Snooze · AI 模仿用户声音 · 1:1 onboarding 教用户习惯 · "game design" 哲学 | 不要照搬"每秒都追求极致速度" —— Curis 是决策工具，不是通信工具 | 把"速度感知"作为 motion 目标；用 onboarding 把习惯交给用户 |
| **Arc** | 垂直 sidebar 用 list · Spaces 切上下文 · 主动隐藏 chrome · "frame your apps, get out of the way" · 视觉不是装饰 · little arc / easel 等 micro-product 表达产品个性 | 不要做"浏览器式 chrome" —— Curis 不是浏览器 | 用"主动隐藏 chrome"作为产品哲学；workspace 切换用 Spaces 而不是 tab |
| **Claude Design** | 五问测试 · 颜色不是默认 · AI 不暴露自身 · 主动把"可变维度"交给用户 · 不靠紫色渐变 · spacing 4/8 倍数 | 不要照搬 Claude Design 的 generative 输出 —— 那是工具产物 | 用"五问测试"作为 anti-AI-decoration 流程；spacing 严格 4/8 倍数 |
| **现代 AI 产品（ChatGPT / Claude / Cursor / Granola / Wispr Flow / Perplexity）** | AI 隐藏在对话流里 · 不暴露"我是 AI" 的徽章 · 输入框是 UI 主面 · 不需要 AI 专属色 | 不要让 Curis 看起来像"AI 前台" | AI 员工和人类员工用同一种视觉语言出现在 Home 里 |

### 3.1 关于"参考的边界"——重要原则

研读所有参考之后必须明确：**Linear 的"高级"来自其约束（dark-only, single-accent, hairline-only, no-shadow），Curis 不能直接套这套约束**。参考给我们的是"约束 → 视觉精致"的因果链，不是"约束本身"。Curis 必须找到属于自己的约束集合（见 §19 三个方向）。

---

## 4. Attention & Hierarchy Research

### 4.1 注意力结构的三个真相

1. **第一眼有 2 秒**。F-pattern / Z-pattern 都不是用户主动选择——它是认知约束。用户到任何屏幕，先扫横线，再扫竖线；扫到第一个"看起来像答案"的地方，停下来。Curis 必须把"今天真正重要的 1–3 件事"放在第一扫的横线终点附近。
2. **决策有"决策成本"**。当所有东西权重相等，用户决策成本最高（每秒钟都在问"我该看哪个？"）。Curis 要降低决策成本，必须**主动降低次要项的视觉权重**——这是克制，不是删减。
3. **注意力会被动作回拉**。用户点了一个按钮，期待 100ms 内有反馈；超过 400ms 注意力就回不来了。Curis 的 motion 必须做到"动作立刻有回应"。

### 4.2 视觉权重的 5 级阶梯（建议作为基础）

> 这不是 token，是**逻辑层级**。每张高保真稿都必须能回答："这屏上的每一项属于第几级？为什么？"

| 层级 | 视觉语言 | 内容类型 | 例 |
|---|---|---|---|
| **L1 锚点** | 最大字号 + 中粗 + 主色前景 | 今天必须看到的 1–3 件事 | 今日决策、今日营收数字、今日待办 |
| **L2 主内容** | 中字号 + 常规字重 | 默认进入后看到的列表 / 表格 | 任务列表、运行中的工作流 |
| **L3 次级** | 小一号 + 浅色 | 元数据、上下文、辅助说明 | 时间戳、负责人、状态 |
| **L4 背景** | 更浅 / 半透明 | 路径、面包屑、secondary nav | 历史归档、低优先级提醒 |
| **L5 装饰** | 几乎不可见 | divider、空状态、whitespace | section 间距、card 间隙 |

### 4.3 Curis CEO Desk 的第一扫地图（建议结构）

> CEO 打开 Curis 的第一扫应该看到什么？这是 §12 的结构骨架。

```
[0–0.5s]   → 当前身份（Curis · 我的公司）            ← Top bar
[0.5–1s]   → 今天公司最重要的事（1–3 件 L1）         ← Hero 区
[1–2s]     → 公司当前运转状态（L2，安静显示）        ← 今日活跃工作流 / 今日决策
[2–3s]     → 进入 Workspace 或切换经营方向的入口（L3 文字链 + 入口）
```

---

## 5. Typography

### 5.1 总体原则（从 Linear / Stripe / Craft / Notion 提炼）

- **字体就是产品**。在桌面 App 里，字体贡献的视觉精致度比颜色高 2–3 倍。
- **中英文字体是两套系统，必须分别管**。不能用英文 Inter 直接替换中文字符。
- **字重等级越少越高级**。3 个字重（Regular / Medium / Semibold）足够撑起一整个产品；多过 4 个就开始失控。
- **不要用软件「加粗」按钮**。必须从字体本身的字重选择。
- **行高必须有公式**。设计稿不写死行高 = 高保真失败（兰亭妙微 UI 文字规范）。

### 5.2 Curis 建议 Typography Baseline（不冻结，供参考）

> 本研究只给「Baseline」，不冻结具体 Hex。

| 用途 | 中文字体 | 英文字体 | 推荐字号 | 字重 | 行高 | 字距 |
|---|---|---|---|---|---|---|
| Display（大标题） | 苹方-中粗 / 思源黑体 Bold | Inter Tight | 28–36px | Semibold (600) | 1.15–1.20 | -0.01em |
| H1（页面标题） | 苹方-中粗 | Inter | 22–24px | Semibold (600) | 1.30 | -0.005em |
| H2（区域标题） | 苹方-中 | Inter | 17–18px | Medium (500) | 1.35 | 0 |
| Body 主文 | 苹方-常规 | Inter | 14–15px | Regular (400) | 1.55–1.60 | 0 |
| Metadata / 辅助 | 苹方-细 | Inter | 12–13px | Regular (400) | 1.50 | 0 |
| Caption / 标签 | 苹方-细 | Inter | 11–12px | Regular (400) | 1.45 | +0.02em（中文不需要） |
| Numeric 数据 | SF Mono / IBM Plex Mono | 同 | 13–14px | Medium (500) | 1.40 | tabular-nums |

### 5.3 中文字体的几个硬规则

1. **不要纯黑**。纯黑 + 纯白 对比度极端，长时段阅读视疲劳。建议主文使用 ink-muted（暖灰）或 ink-soft。
2. **不要 Light 字重做正文**。中文字体 Light 字重在 ≤14px 下识别度差，12px 下几乎糊掉。
3. **中英文混排时英文小 1–2px**。同等字号下英文视觉更小，需要补偿。
4. **中英文之间留 1/4 空格**（ideally 自动 kerning）。
5. **中文标点用全角，英文标点用半角**。混排时尤其重要。
6. **不要用 emoji 当 UI 元素**（除非是状态指示的圆点）。
7. **避免苹方 PingFang TC 与 SC 混用**——一个偏繁体字形，一个偏简体，会造成字形不齐。
8. **数字用 tabular-nums**（等宽数字）。表格、金额、计数都该用。

### 5.4 Typography 的"5 级字号阶梯"（建议）

为了让 CEO Desk 不被字号淹没，建议采用 5 级阶梯：

```
36 / 24 / 17 / 14 / 12
```

- 36 = Hero（L1）
- 24 = Section 标题（L1/L2 边界）
- 17 = 区域标题 / 列表项主文（L2）
- 14 = Body / 默认文字（L2/L3 边界）
- 12 = Metadata / 状态 / 时间（L3）

任何超出这 5 级的使用都应被 Design Review 挑战。

---

## 6. Density / Spacing

### 6.1 总体原则

- **Spacing 是结构，不是装饰**。Stripe Dashboard 用 16–24px gap + 24px card padding 来表达"section 内 / section 间"——这就是结构。
- **4px grid 是底线**。所有 spacing 必须是 4 的倍数（4 / 8 / 12 / 16 / 24 / 32 / 48 / 64）。Curis Frozen `--ui-*` 已有 6 档间距，沿用。
- **Whitespace 比 Border 更适合做层级**。Craft / Notion 大量用空白分割 section；Linear 用 1px hairline 补充。

### 6.2 推荐的 Spacing 语义

| Token | 用途 | 例 |
|---|---|---|
| 4px | icon 与文字、pill 内 padding | `padding: 4px 8px` |
| 8px | list item 内 padding、tag 之间 | 行内小间距 |
| 12px | 列表项之间、紧凑段落 | list-item 上下 |
| 16px | card 内 padding、section 间小间隔 | card padding-top |
| 24px | section 间、card 与 card | 主区段间距 |
| 32px | 区块间、hero 与主内容 | 区段间距 |
| 48px | 大区块间隔、hero 内部 | 页头与内容 |
| 64px+ | 仅在 hero / empty state 使用 | 首屏 / 空态 |

### 6.3 信息密度的取舍

- **不要"满"也不要"空"**。Stripe 是 sparse（信息少、空白多）；Datadog / AWS Console 是 dense（信息多、文字小）。Curis 应偏向 sparse——因为 Curis 是决策工具，不是监控工具。
- **第一屏最多 7 个信息块**。超出就开始违反 "low surface complexity"。
- **首屏 metric 上限 = 4**。这是 Stripe / Linear / Vercel 的收敛值。

---

## 7. Surface / Card Discipline

> **这是本研究对 Curis 当前 UI 风险最大的反推**。Curis 此前多轮设计存在 Card 过多风险。

### 7.1 Card 必须"挣到自己的边界"

> Card 不是默认容器。Card 是**当对象本身是一个独立可操作单元时**才使用的容器。

#### 7.1.1 什么时候用 Card

| 场景 | 是不是 Card | 替代方案 |
|---|---|---|
| 一张发票、一篇文章、一个订单 | ✅ 是 | — |
| 一个 metric + label + delta | ❌ 否 | 用 KPI row（数字 + 文字一行） |
| 一个任务项 | ⚠️ 看上下文 | 在 list 中是 row，在详情中是 card |
| 一段解释文字 | ❌ 否 | Section + 正文 |
| 状态徽章 / tag | ❌ 否 | Pill / Chip / Inline tag |
| 表单字段 | ❌ 否 | Field row + helper text |
| Empty state 引导 | ⚠️ 看场景 | 多为 Section + 大 CTA，不一定 Card |
| 设置项 | ❌ 否 | Setting row（label + control） |

### 7.2 CURIS CARD DISCIPLINE（八条）

1. **Card 有边界责任**——只有"对象本身就是独立可操作单元"才用 Card。
2. **Card 内必须有显眼的操作或对象名**，否则就只是视觉占位。
3. **同屏 Card 不超过 6 个**。超 6 个 = Card wall，立刻停手。
4. **Card 不能堆叠**。Card 内禁止再嵌入 Card——必须 flatten。
5. **Card 与 Section 的选择**——能用 Section + Whitespace 的，不要 Card。
6. **List > Card for 多项**。同质多项用 list（行 + divider），不要每项一个 Card。
7. **Popover > Card for 临时交互**。hover / 点击展开的临时内容用 Popover，不开新 Card。
8. **Focus View > Card for 详情**。被选中的对象展开成 Focus View（铺满），不是放大 Card。

### 7.3 Surface Ladder（建议）

> 来自 Linear DESIGN.md 的核心机制：用 surface 阶梯代替阴影做层级。

```
Canvas (背景) → Surface 1 (主区) → Surface 2 (卡片) → Surface 3 (弹层) → Surface 4 (Modal/Popover)
```

- **Canvas**：整个窗口背景。Light 时偏 warm gray，Dark 时偏 near-black（不要纯黑）。
- **Surface 1**：主内容区。比 Canvas 高一阶。
- **Surface 2**：Card / 容器。
- **Surface 3**：悬浮元素。
- **Surface 4**：Modal / 强焦点。

每一阶通过**亮度差 + 1px hairline border** 区分，**不靠 drop shadow**。这是 Linear / Vercel 的共识——"borders age better than shadows"。

---

## 8. Color

### 8.1 Color 的"职责清单"

颜色不是装饰，**颜色是有职责的**。一份合格的设计必须能让审稿人回答："这屏里的每种颜色，分别承担哪个职责？"

| 职责 | 应使用 | 应避免 |
|---|---|---|
| **Brand** | 仅 logo / 主 CTA / 启动屏 | 不要大面积铺品牌色 |
| **Selection** | 选中行 / focus ring / 当前项 | 不要把 selection 当 brand |
| **Status** | success / warning / danger / info | 不要用红绿做装饰 |
| **Risk** | danger / warning | 不要用橙黄做装饰 |
| **Decision** | 主 CTA / 关键决定按钮 | 不要超过 1 个主 CTA |
| **Interactive** | link / hover / active | 不要让所有文字都可点 |
| **Domain Identity** | workspace 区分色（最多 4–6 色） | 不要每个 workspace 换全套配色 |

### 8.2 Color Behavior（建议规则，不冻结 Hex）

1. **品牌色只承担一件事**：让用户知道"这是 Curis"，不参与决策流程。
2. **主 CTA 用品牌色或中性深色**——两者择一，不要混用。
3. **状态色三色就够**：success（绿）/ warning（琥珀）/ danger（红）。info 可省。
4. **Workspace identity 用 token，不**（饱和度高的纯色）。
5. **永远不要用纯黑 `#000` 或纯白 `#FFF`**——前者太重，后者太硬。用 `#0a0a0a` / `#fafafa` 这种 near-black / off-white。
6. **长时段使用面避免高饱和**。所有前景色饱和度 ≤ 60%。
7. **decorative gradient 默认禁用**——除非用于 hero / empty state 的明确场景。
8. **同一语义在所有页面用同一种颜色**。例如 danger 永远是同一种红。

### 8.3 不应该用颜色的地方

- 元数据（用字号 + 字重 + 透明度表达层级）
- 时间戳
- 操作历史 / log
- 数字（用 tabular-nums + 字重，不要用颜色）
- 状态描述文字（用 icon + 字重）

---

## 9. Motion

### 9.1 Motion 的三类

> 研读 Raycast / Linear / Superhuman / Craft 后必须区分清楚。

1. **Functional Motion（功能性动效）**：click feedback、pane open/close、focus、loading、state change。这类动效**必须存在**——没有它们产品感觉"卡"。
2. **Delight Motion（愉悦性动效）**：hover 微动、入场 stagger、cursor effect、AI 思考时的小动画。这类动效**偶尔使用**——用多了就疲劳。
3. **Decorative Motion（装饰性动效）**：永久背景动画、闪烁光斑、AI sparkle、AI agent 卡片浮动。**Curis 应禁用**。

### 9.2 Curis 的 Motion 优先级

> **Functional > Delight > Decorative**

### 9.3 具体 Motion 规则

| 场景 | 动效 | 时长 | 缓动 |
|---|---|---|---|
| Button press | scale 0.97 | 80–120ms | ease-out |
| Hover（surface） | bg-shift / border-darken | 120–180ms | ease-out |
| Pane open/close | translate + opacity | 200–280ms | cubic-bezier(0.2, 0, 0, 1) |
| Modal open | scale 0.96 → 1, opacity | 220ms | ease-out |
| Result arrival | opacity + translate 4px → 0 | 180ms | ease-out |
| Loading（异步） | skeleton shimmer（仅在 >300ms 时） | 1200ms loop | linear |
| State change | crossfade | 150ms | ease-out |
| 永久状态 | 不要动画 | — | — |
| AI 思考 | 单点 pulse（不闪烁） | 1200ms loop | ease-in-out |
| 空状态切换 | fade in | 240ms | ease-out |

### 9.4 必须避免的 Motion

- 任何在桌面 App 里**持续闪烁**的元素
- 任何会让人**视线跟踪不到**的动效（parallax / 慢速 zoom / 漂浮）
- 任何**装饰性渐变背景动画**
- 任何 **scale > 1.05 的弹动**——会让"专业"感消失
- 任何 **> 400ms 的 transition**——除非 modal 全屏切换

---

## 10. Micro-interaction

> 真正让成熟 App 和"看起来差不多的 App"差开的，是这些细节。下一轮 Visual Quality Gate 必须包含这些维度。

### 10.1 必须存在的 micro-interaction 清单

| 场景 | 必须做到 |
|---|---|
| **Hover** | 背景透明度或颜色变化 ≤ 80ms 完成；无 hover 闪烁 |
| **Press** | scale 0.97 + bg-shift 同时；即时反馈 |
| **Focus** | 1px focus ring（区别于 hover），键盘可达 |
| **Selection** | 选中态与 hover 态**视觉不同**；选中后保留 selection tint |
| **Loading** | >300ms 才显示 skeleton；<100ms 直接结果；<300ms 用 opacity |
| **Empty state** | 有图示 + 一句话引导 + 一个明确动作 |
| **Success** | 短暂绿色脉冲 + toast，自动消失 ≤3s |
| **Failure** | 红色 inline + 修复建议 + retry；toast 不自动消失 |
| **Drag** | drag target 提升阴影 / tint，drop zone 高亮，cancel 时复位 |
| **Resize** | 拖拽实时反馈，松开后有 settle animation（100–150ms） |
| **Collapse** | 高度 + opacity 同步；200–240ms |
| **Keyboard shortcut** | 提示文字始终可见（如 ⌘K），不要隐藏 |
| **Context menu** | 右键 / 长按 一致；菜单 fade in 80ms |
| **Transition** | pane 间用 crossfade 或 slide；不要 scale |
| **Scroll** | 滚动有 momentum；header 在滚动时可选择性 retract |
| **Notification** | 顶部 slide-down；用户主动 dismiss 后下次仍会出现 |

### 10.2 必须**禁用**的 micro-interaction

- bounce / spring 默认开启
- 默认 cursor 动画
- 自动播放视频或音频
- AI agent 卡片自动闪烁
- hover 时改变布局（layout shift）

---

## 11. Desktop / Long-duration Use

> 这是把"截图漂亮"和"工作 4 小时不累"区分开的章节。

### 11.1 视疲劳来源（按严重度排序）

1. **纯黑 + 纯白的高对比边缘**（解决：用 `#0a0a0a` ↔ `#fafafa` 这种近黑/近白）
2. **饱和色状态徽章**（解决：状态色降饱和度）
3. **永久在场的辅助元素**（解决：默认隐藏，按需出现）
4. **字号过小 + 行高过紧**（解决：14–15px body，行高 1.55–1.60）
5. **持续动效 / 闪烁**（解决：见 §9）
7. **section 之间没有 whitespace 节奏**（解决：见 §6 spacing 语义）

### 11.2 长时段使用的 8 条规则

1. **正文用 ink-muted（暖灰）或 ink-soft，禁用 ink-pure（纯黑）**。
2. **行高 ≥ 1.55**（中文）/ 1.50（英文）。
3. **status color 用于"必要告警"，不用于"日常状态"**。
4. **侧栏可收起，默认收起 30% 内容**。
5. **动效停止条件：viewport 不在主交互区**（用 IntersectionObserver）。
6. **永远不要让 viewport 内的元素跑 loop 动画超过 3 秒**。
7. **状态徽章用 dot（点）而不是 pill（药丸）**——点占用空间小、视觉噪音低。
8. **空状态不要用插画动画**。

### 11.3 屏幕密度与窗口尺寸

- **目标窗口尺寸**：1280×800 起，向上扩展到 1920×1080。Curis 不是 mobile-first。
- **内容宽度上限**：表格 ≤ 1280px；阅读内容 ≤ 720px（中文字符约 35–45 字）。
- **Sidebar 收起宽度**：48px（icon only）；展开宽度：220–260px。
- **Top bar 高度**：48–52px。
- **Main content padding**：24–32px。

---

## 12. CEO Desk Research

> CEO Desk 是 Curis 第一张视觉母版。本节定义它必须满足的注意力结构。

### 12.1 CEO Desk 不能是的东西

- ❌ Admin Console（不要有 metric 墙）
- ❌ Task List（不要把所有任务平铺）
- ❌ Chat 首页（不要以对话开场）
- ❌ Empty void（不要只有"开始经营公司"）
- ❌ Workspace Switcher（不要让用户先选业务）

### 12.2 CEO Desk 必须做到的五件事

1. **让用户第一眼感觉"这是我的公司"**——而不是"我在用工具"。
2. **让用户第一眼看到"今天最重要的事"**——1–3 件 L1 锚点。
3. **让用户第一眼感受到"公司正在运转"**——但不是"系统在跑"。
4. **让用户第一眼能看到"我的 Workspace 入口"**——但不是把它们做成 Card 墙。
5. **让用户第一眼没有"开始经营"按钮**——首次进入的"创办"流单独放在 first-run gate，不挤占日常 Home。

### 12.3 CEO Desk 的建议信息结构（中保真骨架，§19 三个方向各自落地）

```
[Top Bar]
  公司名 · 当前经营方向 · 用户头像 · 通知点

[Hero — L1 锚点]
  今日 1–3 件最重要的事
  - 每件事：标题 + 一行解释 + 当前状态（安静 dot）+ 进入链接

[Today — L2 主内容]
  今日决策 / 今日进行中 / 今日完成
  列表形式，不是 Card 墙

[Workspace 入口 — L3 文字链]
  你的经营方向 · 进入 →
  （不是大色块）

[Footer — L4 安静提示]
  本周运转摘要：完成 12 / 决策 3 / 阻塞 1（最文字数字 + dot）
```

### 12.4 "AI 公司正在运转"的视觉表达（不靠状态徽章）

研究 Craft / Notion / Apple Notes 后确认：**运转感来自"内容在变"，不来自"状态在闪"**。

建议在 CEO Desk 用以下机制表达"公司正在运转"：

- **Hero 区有"最近一次决策"的时间戳**（"2 小时前 · 你批准了 X"）——比"AI 正在思考"更可信。
- **Today 区的"完成项"是真实任务，不是占位**——必须能点击回到对象。
- **Footer 用一句话总结本周**：而不是用 4 个 KPI 数字。
- **不用 badge 表达"agent 在线"**——如果必须，用 1px dot，最多 3 个。

### 12.5 第一屏 7 项硬上限

> 第一屏（不开滚动）**最多 7 个信息块**。超 7 = 违反 "low surface complexity"。

建议 7 项分配：

1. 公司名 + 经营方向（Top Bar，1 块）
2. 今日最重要（Hero，1 块）
3. 今日决策（Today，1 块）
4. 今日进行中（Today，1 块）
5. 今日完成（Today，1 块）
6. Workspace 入口（Footer，1 块）
7. 运转摘要（Footer，1 块）

---

## 13. Professional Workspace Research

### 13.1 共享 Shell + Domain Identity 是关键

> 第二个验证对象是 Professional Workspace。它必须明显属于 Curis，但每个 workspace 必须有非常强的 domain identity。

#### 13.1.1 共享 Shell（Same DNA）

| 元素 | 所有 Workspace 必须一致 |
|---|---|
| Top bar 高度、字号、布局 | 48px，左 logo + 中标题 + 右用户区 |
| Sidebar 收起/展开机制 | 48px / 240px，左侧固定 |
| 主内容 padding | 24–32px |
| Spacing token | 4/8/12/16/24/32/48 |
| Typography 5 级阶梯 | 36/24/17/14/12 |
| Motion 时长 | 80–280ms 区间 |
| Surface ladder | 5 阶 |
| 主操作按钮 | 同一种 |
| 错误反馈 / 空状态 | 同一种风格 |

#### 13.1.2 Domain Identity（必须不同）

每个 workspace 可以有自己的：

- **主色 token**（不超过 1 个 accent）
- **Hero 区的 hero pattern**（研发 = 代码态、内容经营 = 文档态、未来业务 = 探索态）
- **Domain object 的视觉呈现**（研发 = issue/code、内容经营 = article/draft、未来业务 = decision）
- **Status color 的语义**（研发 = build/test 状态、内容经营 = draft/published、未来业务 = open/done）

### 13.2 三个具体 Workspace 的 Domain Identity 草案

| Workspace | 主色 token | Hero 元素 | 主要对象 | 状态语义 |
|---|---|---|---|---|
| **研发** | 冷色（slate / steel） | 最近 commit + 最近 issue | code / issue / test | build/test pass |
| **内容经营** | 暖色（warm beige） | 最近发布的文章 + 数据 | draft / article / channel | draft / scheduled / published |
| **未来业务** | 中性（muted gray） | 当前在跑的实验 | experiment / decision / hypothesis | open / running / decided |

### 13.3 Workspace 切换的视觉处理

- **不要做"变色"**——用户进入不同 workspace 应该感觉"换了一间办公室"，不是"换了一个网站"。
- **Workspace 切换时主区 fade 200ms + 内容 slide 8px**。
- **Sidebar 内容根据 workspace 完全替换**，不保留"跨 workspace 通用"项目。
- **Workspace 切换的过渡态**：可以用一张 200ms 的 placeholder skeleton，而不是 spinner。

---

## 14. AI Presence Without AI Decoration

> 研读 ChatGPT / Claude / Cursor / Granola / Wispr Flow / Perplexity 之后的共识：**AI 必须隐形存在**。

### 14.1 AI 不应该出现的东西

- ❌ AI 按钮（独立按钮比"开始对话"更显眼）
- ❌ AI 专属色（"AI purple" 是反例）
- ❌ AI agent 卡片墙
- ❌ "AI 正在思考" 旋转动画（超过 2 秒后停止）
- ❌ AI sparkle / 闪光图标
- ❌ "Running…" 状态徽章（除非真有后台任务）
- ❌ AI model selector 暴露在 UI（藏在 settings）

### 14.2 AI 应该如何"存在"

- **AI 员工和人类员工用同一种视觉语言**：同样的头像框、同样的状态 dot、同样的 list item 样式。
- **AI 的"输出"用普通 result 样式**：ChatGPT 的对话气泡、Claude 的回答块、Cursor 的 diff 高亮——都是 result，不是 AI 装饰。
- **AI 的"运行"用普通 loading 样式**：和系统其他 loading 一致。
- **AI 的"权限"用普通 setting row**：和人类员工的权限 UI 一致。
- **AI 不需要专门"被介绍"**——它应该和你的 CTO、CMO 一样出现在公司通讯录里。

### 14.3 Claude Design 的"五问测试"（必须复用到 Curis）

> 来源：Anthropic Labs, Claude Design 系统提示词。每当 Curis 想加一个 AI 装饰元素，先过五问：

1. **用户关心吗？**（如果去掉它用户会困惑吗？）
2. **它推动了叙事吗？**（它帮用户理解"我的公司"吗？）
3. **去掉之后页面还看得懂吗？**（它是结构还是装饰？）
4. **有更简洁的方式吗？**（能不能用一个 dot / 文字 / 状态？）
5. **它服务的是用户还是设计师？**（设计师想 show off 就删掉）

5 问全过才允许加。

---

## 15. Curis Visual Personality

> Curis 必须从以下 13 个维度里**选优先级**，不能全选。

### 15.1 维度评估矩阵

| 维度 | 必要性 | 是否进入 PRIMARY | 理由 |
|---|---|---|---|
| **Calm（安静）** | 极高 | ✅ PRIMARY | 长时段使用 + 一人公司的精神状态需要 |
| **Precise（精确）** | 极高 | ✅ PRIMARY | 让 CEO 信任"这家公司被精确管理" |
| **Executive（高管感）** | 极高 | ✅ PRIMARY | CEO 是真实用户，他需要感觉自己在经营，不是被伺候 |
| **Trustworthy（可信）** | 极高 | ✅ PRIMARY | 一人公司 = 责任集中，信任是底层 |
| **Alive（有生命感）** | 高 | ✅ SECONDARY | "公司正在运转" 必须有，但要安静地表达 |
| **Human（人性化）** | 高 | ✅ SECONDARY | AI 公司 = 人 + AI，必须有人的温度 |
| **Intelligent（智能）** | 高 | ✅ SECONDARY | AI 能力要可被感知，但不能炫耀 |
| **Focused（聚焦）** | 高 | ✅ SECONDARY | "low surface complexity" 的结果 |
| **Premium（精致）** | 中 | ✅ SECONDARY | 让人愿意每天打开，但不主导 |
| **Professional（专业）** | 中 | ✅ SECONDARY | 信任来自专业，但不要"企业感" |
| **Technical（技术感）** | 低 | ❌ AVOID | Curis 不是 IDE，过度技术感会让非技术 CEO 焦虑 |
| **Creative（创意感）** | 低 | ❌ AVOID | Curis 是决策工具，不是创意工具 |
| **Playful（玩趣）** | 低 | ❌ AVOID | 与"Executive / Trustworthy" 直接冲突 |
| **Warm / Cold 倾向** | 情境 | 维度决定 | 由 §19 三个方向分别落地 |

### 15.2 优先级总结

```
PRIMARY    : Calm · Precise · Executive · Trustworthy
SECONDARY  : Alive · Human · Intelligent · Focused · Premium · Professional
AVOID    : Technical-only · Creative · Playful · Enterprise-busy · AI-decorative
```

### 15.3 这个优先级对设计的影响

- **Calm + Precise** → 少颜色 + 多空白 + hairline border + 慢 motion
- **Executive + Trustworthy** → 类型层级严谨 + 无装饰 + 真实数据 + microcopy 准确
- **Alive + Human** → "今天发生的" 时间戳 + 真实对象 + 安静的运转痕迹
- **Intelligent** → AI 隐形存在 + 输出精致 + 错误有解释
- **Focused** → 第一屏 ≤ 7 信息块 + Card ≤ 6 + List 优先
- **Premium** → 字体精致 + 中文混排 + spacing 节奏
- **Professional** → 不卖萌 + 不浮夸 + 错误有解

---

## 16. Anti-patterns

> 研读大量 AI SaaS / Agent Platform / Enterprise Dashboard 之后，归纳出至少 12 种视觉反模式。**任何在 Curis 中出现一种 = Visual Review FAIL**。

### 16.1 反模式清单

| # | 名称 | 表现 | 后果 |
|---|---|---|---|
| 1 | **Card Wall** | 首屏 6+ Card，没有 hierarchy，没有呼吸 | 用户立刻关掉 |
| 2 | **KPI Wall** | 8+ 数字 + 4 种 delta 颜色 | 像 BI 后台，不像经营工具 |
| 3 | **Excessive Pills** | 每个状态都套 pill，pill 颜色饱和 | 视觉噪音 |
| 4 | **Excessive Borders** | 每个 section 都用 1px border 圈起来 | 边框重于内容 |
| 5 | **Every Section Same Weight** | 所有 section 同字号同字重 | 没有 anchor，眼睛无处落脚 |
| 6 | **Permanent Panels** | Sidebar / Inspector 永远展开 | 桌面空间被吃掉 |
| 7 | **Over-labelled UI** | 每个 icon 都有 tooltip、每个按钮都有提示文字 | 信息密度爆炸 |
| 8 | **Tiny Dense Text Everywhere** | 11px / 12px 当默认正文 | 长时段使用必累 |
| 9 | **Decorative Gradients** | 紫色 / 蓝色 radial gradient 当背景 | 立刻显 AI 味 |
| 10 | **Fake AI Futuristic Styling** | 粒子背景 / 发光边框 / 大写 mono | 假高科技 |
| 11 | **Too Many Primary Buttons** | 一屏 3+ 个同色主 CTA | 用户不知道点哪个 |
| 12 | **Dashboard Syndrome** | 第一屏像 dashboard，不像工作入口 | "我被伺候"而不是"我在经营" |
| 13 | **AI Sparkle Pollution** | 多处 sparkle / star / magic 图标 | AI 装饰病毒 |
| 14 | **Status-as-Promotion** | 把系统状态当作"功能"展示（"AI 思考中"当 feature） | 让产品自恋 |
| 15 | **Mode-as-Promo** | 把 dark/light mode 当卖点展示 | 用户不需要被教育模式 |
| 16 | **Glassmorphism Overuse** | 所有 surface 都半透明 + 模糊 | 注意力被分散 |
| 17 | **Sticky Everything** | 多处 sticky / pinned / 悬浮 | 屏幕混乱 |
| 18 | **Empty Hero** | 第一屏只有一个空状态 | 用户立刻关掉 |

### 16.2 Anti-pattern 自检流程

每次高保真提交前必须用这张表自检：

- [ ] 第一屏 Card ≤ 6？
- [ ] 第一屏 metric ≤ 4？
- [ ] 主色出现在 ≤ 3 个区域？
- [ ] 没有任何持续闪烁的元素？
- [ ] 没有任何 emoji 出现在 UI（除非状态 dot）？
- [ ] 没有任何 decorative gradient？
- [ ] AI 元素和人类员工用同一种样式？
- [ ] 正文 ≥ 14px（中文）/ 行高 ≥ 1.55？
- [ ] 没有默认 cursor 动画？
- [ ] 没有 spring / bounce 默认开启？

---

## 17. Visual Quality Rubric

> 这是本研究最重要的可交付之一。**未来所有高保真页面必须过这个 Rubric**，任一项 FAIL 即打回。

### 17.1 Rubric — 15 维度 × 3 等级

| # | 维度 | FAIL | ACCEPTABLE | EXCELLENT |
|---|---|---|---|---|
| **1** | **First Impression（第一眼）** | 像 Dashboard / 像 ChatGPT Clone / 像 Agent 后台 / 像 ERP | 看起来"像个 App"但说不出高级在哪 | 第一次打开就让人觉得"这是个成熟产品" |
| **2** | **Hierarchy（层级）** | 所有 section 同权重；字号 / 字重 / 颜色都是默认 | 有层级但仍有一两处权重平了 | 1–2 秒能定位锚点；不需要思考"看哪里" |
| **3** | **Focus（聚焦）** | 第一屏 ≥ 10 个信息块；多个 primary CTA | 7–9 个信息块，主次稍清 | ≤ 7 个信息块，1 个 L1 锚点明确 |
| **4** | **Density（密度）** | 文字过密 / 留白失控 / dashboard syndrome | 节奏大致对，但有 1–2 处拥挤或空旷 | 节奏贯穿整屏；密度有变化 |
| **5** | **Typography（排版）** | 中文 < 14px / 行高 < 1.5 / 字号等级混乱 | 排版大致对，但混排或中文特殊字符有问题 | 中文精致；5 级字号；中英文 kerning 正确 |
| **6** | **Spacing（间距）** | spacing 不在 4 倍数；section 之间没节奏 | 4 倍数但节奏单调 | 4 倍数 + 节奏有变化（紧凑 / 呼吸） |
| **7** | **Surface Discipline（surface 规范）** | Card Wall / shadow 代替 hairline / 用渐变背景 | 有 surface 阶梯，但 Card 用得过松 | 5 阶 surface ladder 严格；Card Discipline 8 条全过 |
| **8** | **Color Discipline（色彩规范）** | 品牌色乱铺 / 状态色饱和 / 颜色无职责分工 | 颜色克制，但有 1–2 处"色彩污染" | 颜色职责清单 100% 落实；status color 仅用于告警 |
| **9** | **Interaction Quality（交互质量）** | hover 无反馈 / press 无变化 / 加载用 spinner | 基础反馈齐，但精细度不一致 | §10 16 项 micro-interaction 全部到位 |
| **10** | **Motion（动效）** | 装饰性动效 > 动效总量 30% / 永久闪烁 | Functional 动效齐全，Delight 偶用 | Functional > Delight > Decorative 严格排序 |
| **11** | **Domain Identity（领域识别）** | 所有 workspace 看起来一样 | workspace 之间有颜色区分，但视觉一致 | workspace 有自己的 hero pattern / object 视觉；共享 shell 严格 |
| **12** | **Product Consistency（产品一致性）** | 同一组件在不同页面样式不同 | 大致一致但有 1–2 处偏差 | 跨页组件严格一致；token 100% 覆盖 |
| **13** | **Long-duration Comfort（长时段舒适）** | 纯黑纯白 / 持续闪烁 / 12px 主文 | 大部分 OK，但有一两处疲劳源 | §11 八条规则 100% 通过 |
| **14** | **Trust / Professionalism（信任 / 专业）** | microcopy 含糊 / 错误无解释 / 时间戳缺失 | 基础可读，但缺少"经营感" | 微文案承担信任；时间戳清晰；运转痕迹真实 |
| **15** | **Desirability（使用欲望）** | 看起来像 AI 生成的 demo / 像 Dribbble 概念稿 | 看起来"还不错"但不会想分享 | 第一眼就让人想分享 / 想每天打开 |

### 17.2 Rubric 怎么用

- **提交高保真稿前**：作者用 Rubric 自评；FAIL 项必须返工。
- **Review 会议**：以 Rubric 为讨论框架；不接受"我觉得不够高级"这种主观结论——必须对应到具体维度。
- **每个新页面**都过完整 15 项；任何新组件进入系统也按对应维度评估。

---

## 18. Desirability Gate

> 在 Rubric 之外，加一个**CEO 视角的体验质量门**——它不是技术指标，是"愿不愿意每天用、愿不愿意分享"的判断。

### 18.1 Desirability Gate 的 6 个问题（必须每个都能回答 "是"）

每次高保真稿必须能让 CEO 在不查任何文档的情况下，对以下每个问题都答 "是"：

| # | 问题 | 如果答案是 "否"，应该改什么 |
|---|---|---|
| **D1** | **我愿不愿意每天打开它？** | 视觉太"忙"或太"空"——必须找到节奏 |
| **D2** | **它看起来像一个值得付费的软件吗？** | 有 demo 感 / AI 味 / Dribbble 味——必须去掉所有装饰 |
| **D3** | **第一次看到它，我会不会想继续点进去？** | Hero 不够明确 / 第一屏 ≤ 7 信息块没做到 |
| **D4** | **截图发给别人，我会不会觉得产品有说服力？** | 视觉太轻 / 太密 / 太花 |
| **D5** | **它是否看起来已经接近成熟商业产品，而不是 AI 生成的 Demo？** | 任何 §16 反模式出现 = FAIL |
| **D6** | **它有没有让我感觉"这是我的公司"？** | 用了 dashboard 范式 / 没体现运转 / 太工具感 |

### 18.2 Desirability Gate 的"截图测试"

具体执行步骤：

1. 把高保真稿导出为 1 张截图（CEO Desk 默认状态）。
2. 把这张截图发给一个**不知道 Curis 是什么**的人，问："这是什么？"
3. 如果回答不是"你的公司"或"一个帮你经营公司的工具"——**D6 FAIL**。
4. 同样的截图，问："你会想用吗？为什么？"——如果对方犹豫 > 5 秒——**D1 FAIL**。

### 18.3 Desirability Gate 的"30 分钟测试"

具体执行步骤：

1. 让一位用户连续使用高保真稿 30 分钟（模拟日常操作）。
3. 30 分钟后问："眼睛累吗？"
4. 如果答 "累"——**Long-duration FAIL**（§11 必须返工）。
5. 如果答 "还好但有点花"——**Decorative FAIL**（§9 必须返工）。

---

## 19. Three Visual Directions

> 三个真正不同的方向。它们不是 A=深色 / B=浅色 / C=蓝色 这种假差异。
>
> 它们是**三个不同的产品气质**、三个不同的**注意力策略**、三个不同的**空间语言**、三个不同的**信息密度**、三个不同的**交互感觉**。
>
> 三个方向**都在 Frozen `--ui-*` token 范围内**具有可行性——研究不冻结具体 Hex，但 Frozen token 提供了三个方向都能落地的底座。

---

### 19.1 方向 A：**「我的公司」**（My Office）

> 关键词：**温暖 · 安静 · 个人化 · 像走进办公室**

| 项目 | 定义 |
|---|---|
| **名字** | "My Office / 我的公司" |
| **Emotional target** | 用户打开 Curis 像打开自己的办公桌：安静、熟悉、有自己经营痕迹 |
| **Visual philosophy** | 内容优先 + 空白优先 + 真实感优先 |
| **Typography** | 苹方 + Inter Tight；正文 15px；行高 1.60；warm gray ink |
| **Density** | Sparse。第一屏 ≤ 7 信息块。Card ≤ 4。 |
| **Surface** | Light-first（warm off-white + soft shadow + hairline border），可切 Dark |
| **Color** | 单一暖灰中性 + 单一品牌色（推荐冷暖中性偏一种，但**不锁定**） |
| **Motion** | Functional > Delight。Motion 偏慢（240–320ms）。无装饰动效。 |
| **Navigation** | 极简：顶栏 + 单 Sidebar（240px，可收 56px）。无 bottom bar。 |
| **Workspace** | Domain identity 用 hero pattern 区分；不靠主色 |
| **Strength** | 最适合一人公司 + 长时段使用；视觉接近 Apple Notes / Things 3 / Bear；让人想每天打开 |
| **Risk** | 容易被认为"不像生产力工具"；开发同事会嫌"不够工程感" |
| **Suitable references** | Notion · Things 3 · Apple Notes · Bear · Linear Light mode · Arc Light |
| **What NOT to copy** | ❌ Notion 的 block editor；❌ Things 的"今日 + 今日 + 今日"重复结构；❌ Apple Notes 的极度轻 |

---

### 19.2 方向 B：**「精密机房」**（Precision Room）

> 关键词：**冷峻 · 精确 · 工程化 · 像控制中心**

| 项目 | 定义 |
|---|---|
| **名字** | "Precision Room / 精密机房" |
| **Emotional target** | 用户打开 Curis 像进入精密控制室：精确、严谨、每个细节都到位 |
| **Visual philosophy** | Surface ladder 优先 + hairline border + 单一 accent；信息密度中等偏密 |
| **Typography** | Inter Variable；正文 14px；行高 1.55；near-black ink |
| **Density** | Medium。第一屏 ≤ 7 信息块，但每个信息块密度更高 |
| **Surface** | Dark-first（near-black `#0a0a0a` + 5 阶 surface ladder），可切 Light |
| **Color** | 单一 indigo / steel accent；所有颜色承担明确职责 |
| **Motion** | Functional 严格；fast（120–200ms）；scale(0.97) press |
| **Navigation** | 中等：顶栏 + Sidebar（220px，可收 48px）+ 可选 Inspector |
| **Workspace** | Domain identity 用主色区分 + 状态语义区分 |
| **Strength** | 视觉接近 Linear / Raycast / Stripe；"工程感"足够；让技术用户最满意 |
| **Risk** | 容易"看起来太工程"；CEO（非技术）可能觉得冷；与 Curis "Executive" 维度稍冲突 |
| **Suitable references** | Linear · Raycast · Superhuman · Stripe Dashboard · Vercel |
| **What NOT to copy** | ❌ Linear 的纯 dark-only；❌ Raycast 的 command bar；❌ Stripe 的 jobs-to-be-done 财务后台 |

---

### 19.3 方向 C：**「经营室」**（Operating Studio）

> 关键词：**温度 · 生命 · 中性 + 暖色 + 一点点动 · 像公司总部**

| 项目 | 定义 |
|---|---|
| **名字** | "Operating Studio / 经营室" |
| **Emotional target** | 用户打开 Curis 像走进公司总部：能感觉到"公司正在运转"，有温度、有空间感 |
| **Visual philosophy** | Surface + section + 节奏；用 whitespace 节奏替代 card 节奏 |
| **Typography** | 苹方 + Inter Display；正文 15px；行高 1.55–1.60 |
| **Density** | Medium-sparse。第一屏 5–7 信息块，但每个 block 内部节奏强 |
| **Surface** | Light-first with subtle warm tint（off-white 偏米黄或 cream）；Dark 模式为同色板对应暗版 |
| **Color** | 中性 + 1 个品牌色 + 1 个 workspace accent（每个 workspace 一个） |
| **Motion** | Functional + 极少量 Delight（结果到达 / 状态变化时 240ms 慢呼吸）；无 Decorative |
| **Navigation** | 中等：顶栏 + Sidebar（240px）+ workspace switcher 在顶栏 |
| **Workspace** | Domain identity 最强——每个 workspace 有自己的 hero、自己的 accent、自己的状态色 |
| **Strength** | "Executive + Human + Alive" 三者最平衡；最像"我的公司"；最适合一人公司 |
| **Risk** | 设计难度最高（surface 节奏 + 多 workspace identity 都要对）；工期最长 |
| **Suitable references** | Arc · Craft · Notion · Things 3 · Granola · 一个被精心设计过的"个人 App" |
| **What NOT to copy** | ❌ Arc 的浏览器式 chrome；❌ Craft 的文档 editor；❌ Notion 的 block 编辑器；❌ 任何 generative gradient |

---

### 19.4 三个方向的并排对比

| 维度 | A 我的公司 | B 精密机房 | C 经营室 |
|---|---|---|---|
| 主调 | 安静 + 个人 | 精确 + 工程 | 温暖 + 经营 |
| 默认主题 | Light | Dark | Light |
| 信息密度 | Sparse | Medium | Medium-sparse |
| 装饰动效 | 几乎无 | 无 | 极少 |
| Workspace 区分度 | 弱 | 中 | 强 |
| 长时段舒适 | 极高 | 高 | 高 |
| 第一眼印象 | "私人空间" | "控制中心" | "公司总部" |
| "这是我的公司" 强度 | 高 | 中 | 极高 |
| 工程化信任度 | 中 | 极高 | 高 |
| 设计难度 | 中 | 低（已有 Linear 路径） | 高 |
| 风险 | 偏柔 | 偏冷 | 偏散 |

---

### 19.5 三个方向必须都做到的几件事（硬性）

> **三个方向都必须满足的最低标准**——这保证 CEO 不管选哪个方向都不会踩到 §16 反模式。

1. 第一屏 ≤ 7 信息块
2. Card ≤ 6（第一屏）
3. 主色 ≤ 1
4. 装饰动效 = 0
5. AI 不暴露自身
6. 中文精致（§5 规则全部满足）
7. 长时段使用 8 条规则（§11）全部满足
8. §10 micro-interaction 至少 12 项达标
9. §17 Rubric 至少 13/15 维度达到 ACCEPTABLE
10. §18 Desirability Gate 6 项全部能答 "是"

---

## 20. Recommendation

> 本研究不给唯一推荐（因为"哪个高级"是主观判断，且这是 CEO 的决策）。但给**决策框架**。

### 20.1 决策框架（建议 CEO 用这三个问题拍板）

| # | 决策问题 | 倾向 A | 倾向 B | 倾向 C |
|---|---|---|---|---|
| **Q1** | 你希望 Curis 看起来更像"私人空间"还是"控制中心"还是"公司总部"？ | 私人空间 | 控制中心 | 公司总部 |
| **Q2** | 你最看重哪种气质：温暖 / 精确 / 经营感？ | 温暖 | 精确 | 经营感 |
| **Q3** | 你最想避免哪种气质：太轻 / 太冷 / 太散？ | 偏轻 | 偏冷 | 偏散 |

**Q1 决定主调** → 决定方向
**Q2 + Q3 决定细节** → 决定设计语言细节

### 20.2 风险与建议

- **如果选择 A**：建议保留 B 的工程化组件（状态徽章、loading、focus ring），避免"看起来不像工具"。
- **如果选择 B**：建议引入 A 的"温暖元素"（warm off-white 可选、microcopy 拟人化、状态色降饱和），避免"过冷"。
- **如果选择 C**：建议先把 CEO Desk 和 一个 Workspace（如内容经营）做出来再扩展，避免"workspace identity 失衡"。

### 20.3 给 Trae 的下一轮交付建议

1. **同一个 CEO Desk 信息结构**（§12.3）。
2. **同一个 Product Truth**（Blueprint v4.4）。
3. **同一套设计系统底座**（Frozen `--ui-*` token）。
4. **三个方向各出一张 CEO Desk 高保真稿**。
5. **三张稿必须用 §17 Rubric 全部打到 ACCEPTABLE 以上**。
6. **三张稿必须用 §18 Desirability Gate 全部答 "是"**。

---

## 21. Open Questions for CEO

> 本研究里我无法替 CEO 决定的几个问题，列出等评审。

| # | 问题 | 影响 |
|---|---|---|
| **OQ1** | Curis 默认主题倾向 Light-first、Dark-first、还是可切换？ | 决定 §19 哪个方向更适合 |
| **OQ2** | 是否需要"AI 是不是 AI"在视觉上暗示，还是完全透明？ | 决定 §14 AI 隐形策略的边界 |
| **OQ3** | 三个 Workspace 同时上线，还是先 1 + 1 + 1 渐进？ | 决定 §13 Domain Identity 推进节奏 |
| **OQ4** | "运转感"的强度——是"轻微可见"还是"明确展示"？ | 决定 §12.4 表达机制的选择 |
| **OQ5** | 是否允许装饰性插画（如空状态、错误页）？ | 决定 §16 反模式 #1 / #10 的边界 |
| **OQ6** | 中文 vs 英文优先级——是否需要中英双语界面？ | 决定 §5 字体与字距细节 |
| **OQ7** | 是否引入"季节性主题"（如节日皮肤）？ | 决定品牌色的可变性 |
| **OQ8** | CEO Desk 在首次进入（无公司）时应如何呈现？ | 决定 first-run gate 与 home 的边界 |

---

## 22. STOP — 待 CEO 评审

> 本研究在此停止。**禁止扩展整套产品页面**。
>
> 下一步：
>
> 1. **CEO 接收研究**——看 §17 Rubric、§18 Desirability Gate、§19 三个方向、§20 决策框架。
> 2. **CEO 用 §21 决策框架拍板**（A / B / C，或推翻本研究的三个方向、提出新的）。
> 3. **CEO 明确选择方向后**，才把研究结果交给 Trae——同一 CEO Desk / 同一 Product Truth / 同一信息结构，输出 Visual Direction A / B / C 三张高保真竞争稿。
> 4. **CEO 明确选择"这个方向我愿意每天用"**之前，禁止扩展任何 Curis 页面。

---

## 附录 A：本研究未做的事（明确边界）

1. **没有冻结具体 Hex / token 值**——本研究只定义 Color Behavior（§8）。
2. **没有出任何高保真稿**——下一轮才出。
3. **没有修改 Blueprint / Master Map / UI Blueprint / Design System / Frozen token**。
4. **没有引入新 Primitive**——所有方向都在 Frozen `--ui-*` token 范围内可行。
5. **没有写生产代码**。
6. **没有触及 XHS Workspace / RD Workspace 的具体设计**——本研究的 §13 是通用规则。

## 附录 B：本研究的主要参考来源

- Linear：linear.app 官方 + designmd.cc + shadcn.io/design/linear + opendesign.cc（dark canvas / 单一 accent / surface ladder / Inter Variable / 4px grid / hairline border）
- Raycast：raycast.com/blog/a-fresh-look-and-feel + raycast.com/blog/the-new-raycast（fast / simple / delightful 三原则 / Compact Mode / 放大主交互 / 自有 icon set / tasteful native）
- Stripe：925studios.co/blog/stripe-dashboard-design-breakdown + illustration.app/blog/stripe-payment-ux-gold-standard + opendoordigital.dev/blog/dashboard-design-patterns-saas + aidesigner.ai/blog/how-to-design-a-dashboard-ui-2026（jobs-to-be-done nav / 6 type sizes / sparse density / microcopy 承担信任 / 单一 purple = action / "show what you need to act, not everything that exists"）
- Superhuman：blog.superhuman.com/superhuman-is-built-for-speed + techvernia.com/pages/reviews/productivity/superhuman + dynalord.com/blog/superhuman-review（100ms 规则 / keyboard-first / Split Inbox / AI 模仿用户声音 / game design 哲学）
- Craft：aiindigo.com/tool/craft + thesunrisedigest.com/focus/craft-review-2026 + saner.ai/blogs/craft-review + thetechverdict.com/apps/craft-docs-review + support.craft.do/en/write-and-edit/styling（block model 克制 / typography / spacing / animation / color 四维度同样考虑 / Apple 生态 native feeling / design-led 信念）
- Arc：positioniseverything.net/arc-browser-review + techbloat.com/arc-is-the-best-new-browser-for-windows + au.lifehacker.com/apple/26450/news/why-the-new-arc-browser-is-better-than-chrome（垂直 sidebar / Spaces / "frame your apps, get out of the way" / 主动隐藏 chrome）
- Claude Design：news.qq.com/rain/a/20260420A07BUY00 + sohu.com/a/1046822018_122014422 + 163.com/dy/article/K2ES97SB0556CSY5.html + 163.com/dy/article/KQOVDI6Q0556C3J2.html + news.qq.com/rain/a/20260619A03H5L00（五问测试 / 不默认暖色调 / AI 不暴露 / 不靠紫色渐变 / "用户关心吗？推动了叙事吗？"）
- 中文排版：uisdc.com/ui-design-font-typesetting + lanlanwork.com/blog?post=14526 + zcool.com.cn/article/ZMTE3MjI3Ng + kingdee.design/rule/base/font + fonthubs.com/zh-TW/knowledge/ui-typography（苹方 / 思源黑体 / Roboto / 字号 14–18px / 行高 1.4–1.6 / 字重 Regular 正文 / 不要纯黑 / 数字 tabular-nums）

## 附录 C：本研究的中文精炼版（一段话给 CEO）

> Curis 想成为"第一眼精致、成熟、让人想每天打开"的桌面产品，关键不在颜色也不在字体，而在**视觉权重的克制**——把"今天最重要的事"做成 L1 锚点、把 AI 隐形存在、把 Card 收紧到真正必要的对象、把所有装饰动效删干净、把中文排版精致做到位。三个候选方向："我的公司"（温暖、私人）、"精密机房"（冷峻、工程）、"经营室"（温暖 + 经营感 + workspace identity 最强）。三个方向都用 §17 Rubric + §18 Desirability Gate 严格打勾。本研究不冻结任何 Hex、不出任何高保真稿、不动任何 Frozen 源——只把"未来高保真稿必须满足什么"立成规矩。