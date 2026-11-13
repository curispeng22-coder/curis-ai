---
title: Curis Content Growth — Strategy Evolution Interaction（策略进化交互）
status: OPERATING STRATEGY UX TRANSLATION · APPROVED CANDIDATE（非 Frozen · 非高保真）
date: 2026-08-16
covers: Brief §11 策略进化 / §12 最近学到了什么 / §13 策略提案 vs Needs CEO
sibling_wireframe: Curis_Content_Growth_Wireframe_C_Evolution.html（场景 C 中保真结构稿）
upstream: Operating Strategy Product Handoff §1(Strategy Evolution) / §6 / §11 / §12 First Version
discipline: 三类区分清晰；策略提案≠Needs CEO；不把 Home 变审批队列；Context Isolation 非 P8
---

# 1. 必须区分的三类（Brief §11 · Handoff §6）

| 类型 | 含义 | 用户需批准？ | 留痕 |
|---|---|---|---|
| **A. AI 自主微调** | 授权范围内的微调（时段矩阵内调发布时间、选题排序、活动期临时加源/加频、低值源临时降频） | **不需要** | 须在授权边界内 · 必须留痕可查看（可回滚） |
| **B. AI 建议长期调整** | 超出当前规则的结构性变化 → 策略提案流 | 视影响层级；结构性 → Frozen P7 | 观察/证据/建议/影响/可回滚 |
| **C. CEO 主动修改** | 用户直接下命令（「以后不要扫描这个网站」） | 已是决策本身 | 直接执行，不再建一次 CEO Decision |

> **关键裁定（Handoff §6）**：CEO 主动明确下命令 = 决策执行，**不需要再创建 CEO Decision**。只有 **AI 主动提出超出既有经营策略的结构性长期变化** → 才按 Frozen P7 进入 Needs CEO。

---

# 2. A. AI 自主微调（必须在授权边界内 · 留痕可查）

- AI Autonomous Adjustment **≠** AI 自行判断什么都算「小调整」。必须存在 **Operating Boundary / Authorized Range**（用户侧**不暴露**「Policy Boundary」这类内部词）。
- 用户语言自然表达为：「允许 AI 在这个时间范围内自动优化」之类。
- 例：CEO / 初始经营规则允许「工作日 11:30–13:30 之间，AI 根据账号数据选择发布时间」→ 则 12:30→12:00 属授权范围，可自主微调；**超出授权范围不得静默改变**。
- 所有自主微调必须**同时满足**：
  1. **在已授权范围**内；
  2. **留痕**（什么被微调、原值、新值、触发依据、是否可回滚）；
  3. **可回滚**。
- 用户可在「经营方式 → 最近 AI 调整过什么」查看全部留痕（见 Doc 2 §3.2）。

> 原则：可观测、可信任、可回滚——不是黑箱，也绝不是 AI 越权。

---

# 3. B. AI 建议长期调整（Strategy Proposal）

属于策略提案，用户看到结构化信息（Handoff §11）：

| 字段 | 内容 |
|---|---|
| 观察 | AI 发现了什么（如「教程类内容播放一般，但收藏和关注转化明显更高」） |
| 证据强度 | 单次 / 重复 / 实验验证 |
| 建议 | 具体改什么（如「把教程内容占比提高」） |
| 影响 | 影响哪层策略（方向 / 账号 / 员工方法） |
| 是否可回滚 | 是 / 条件 |

- **轻量建议** → 可先「观察中」，不强迫立即决策。
- **结构性建议** → 进入 Frozen P7 Needs CEO（见 §5）。

---

# 4. C. CEO 主动修改

用户直接命令即决策，直接执行。**不再生成一次 CEO Decision**——这本身已是 CEO 的决定（Handoff §6 关键裁定）。

示例：
- 「以后不要扫描这个网站」→ 信息雷达移除该 Source，后续 Conversation / Employee Method 同步（同一份方法，见 Doc 3 §3）。
- 「这个月多做一点教程类内容」→ 直接更新对应经营方向 / 账号的临时内容策略（临时 Operating Rule）→ 留痕 → 执行（见 Doc 3 §3.1 C）。
- **歧义处理**：若语义有期限 / 范围歧义（如「这个月」vs「以后都」），Employee 可自然追问确认，但**不要求 CEO 再次批准自己的命令**。
- **边界**：只有 **AI 主动提出**超出既有经营策略的结构性长期变化 → 才按 Frozen P7（见 §5）。CEO 主动命令本身不触发 P7。

---

# 5. 「最近学到了什么」（Brief §12 · 非常重要的新产品能力）

它**不是普通 Analytics**，而是 Curis 正在形成「这个账号自己的经营方法」的证据。

## 5.1 轻量出现位置

> **示例标注（DELTA T4）**：以下条目仅为 Illustrative / Demo Evidence，用于说明「最近学到了什么」的用户面形态——**不代表真实 Analytics 已连接**。真实产品仅在 Analytics / Platform Evidence 真实可用时显示真实规律；UNAVAILABLE / UNKNOWN 时**不伪造 Learning Evidence**（「最近学到了什么」不会杜撰规律）。

Business Home 以**低存在感条目**出现（不抢 Decision/Attention）：

- 「教程类内容更容易带来关注」
- 「周二晚上的小红书收藏率更高」
- 「这个信息源最近贡献下降」
- 「用户最近频繁询问 Codex 接入」

## 5.2 进入详细 Evidence

点任一条 → 展开 Evidence（观察窗口 / 相关≠因果提示 / 防过拟合标注 / 同主题历史对照），而非一堆图表。

> 表达原则：用「我们最近发现的一条规律 + 为什么这么认为」的自然语言，而非把 Learning 做成数据看板。

---

# 6. Strategy Proposal vs Needs CEO（Brief §13 · 避免审批队列）

Home 必须区分四类，避免把 Home 重新变成审批队列：

| 类别 | Home 呈现 | 是否需 CEO |
|---|---|---|
| **建议**（轻量） | 「观察中 / 可留意」低存在感 | 否，先观察 |
| **观察中** | AI 在积累证据，未提议 | 否 |
| **已自动微调** | 留痕条目（见 §2） | 否 |
| **需要 CEO 决定** | 顶部 Decision Banner（P7） | 是，仅重大事项 |

> 核心纪律：**Strategy Proposal 不一定都需要 CEO 立刻决策**。轻量建议先观察；结构性建议才进 P7。Home 不被重新变成审批队列（对齐 I1：普通事项不逐一 Gate）。

---

# 7. 场景 C 中保真结构稿

关键新增场景「Strategy Proposal / 最近学到了什么」的中保真结构稿见独立文件：
**`Curis_Content_Growth_Wireframe_C_Evolution.html`**

该结构稿演示：Home 上「最近学到了什么」轻量条目 → 点开 Evidence；「策略建议 / 观察中 / 已自动微调 / 需要 CEO 决定」四类如何区分呈现；AI 自主微调留痕列表。套用 Frozen Shell 四 Pane 标注。

---

# 8. 状态

```text
CONTENT GROWTH OPERATING STRATEGY UX TRANSLATION APPROVED CANDIDATE
```

（本文件为 DESIGN CANDIDATE；不修改 Frozen / Blueprint / XHS·RD / Runtime / Connector；不进高保真；Context Isolation 引用正确、无 P8；提案与 CEO 决策严格区分。）
