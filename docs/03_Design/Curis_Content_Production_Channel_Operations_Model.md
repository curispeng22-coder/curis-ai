# Curis · Content Production × Channel Operations 架构模型

> **状态**：CONTENT × CHANNEL ARCHITECTURE REVIEW REQUIRED
> **类型**：Reference Only · 专项架构复盘（非权威文档）
> **纪律**：不画 UI / 不改 Frozen Shell / 不改 XHS·RD Instance / 不开发 Connector / 不改 Runtime / 不改 Authority Map
> **关联文档**：`Curis_Canonical_Content_Channel_Variant_Model.md`（数据模型）、`Curis_Multi_Channel_Architecture_Review.md`（平台差异 + 7 问 + 处置）、`Curis_AiToEarn_Architecture_Review.md`（参考实现）

---

## 0. 触发与范围

前序研究（TTK Product Model、Douyin End-to-End Automation）隐含一个未被审查的前提：

> **TTK Workspace = Video Production**

本轮目标：**把这个前提拆开**。Curis 必须区分两个独立关注点：

1. **CONTENT FORMAT / PRODUCTION** —— 做什么内容、怎么生成（平台无关）
2. **CHANNEL / PLATFORM OPERATIONS** —— 在各平台怎么发、怎么互动、怎么看数据（每平台一个）

抖音（Douyin）只是"渠道"之一，不是"视频生产"的同义词。把 `Video` 绑定到 `Douyin Workspace` 是错误的根因。

---

## 1. 核心诊断：被混淆的两层

| 混淆项 | 应归属 | 错误归属 |
|---|---|---|
| 剪映/CapCut、即梦、可灵、HeyGen、Runway | **视频生产能力提供方**（Video Production Capability Provider） | 抖音 Connector ❌ |
| 抖音发布/评论/私信/数据/OAuth/Scope/Webhook | **抖音渠道能力**（Douyin Channel Capability） | 视频生产 ❌ |
| `Video` 对象 | **跨平台 Company/Business Canonical Content** | Douyin Workspace 私有对象 ❌ |

**结论**：生产工具与渠道能力必须物理隔离。一个 Canonical Video 可以进 5 个平台，但生成它的工具一个都不属于任何平台。

---

## 2. 统一内容模型（A 节综述）

建议的纵向链（平台无关 → 平台特化）：

```
Canonical Content Object（平台无关）
  → Production Result（平台无关母版/成品）
    → Channel Variant（每平台一份，平台特化）
      → Publication（每次发布一份，独立）
        → Engagement + Analytics（挂在 Publication 上）
```

用户给出的候选结构（评估见 Doc 2）：

```
Canonical Video
├ Script
├ Assets
├ Production Result
└ Channel Variants
    ├ Douyin Variant
    ├ XHS Video Variant
    ├ TikTok Variant
    ├ Bilibili Variant
    └ YouTube Variant
```

**评估结论（方向正确，需泛化）**：
- ✅ `Video` 内含 `Script / Assets / Production Result / Channel Variants` 的拆分是对的；
- ⚠️ 需泛化为 **`Canonical Content`**（子类型 `VIDEO` / `NOTE` / `IMAGE_SET`），因为 XHS 同时有 Note 与 Video；
- ⚠️ `Channel Variants` 应是 `platform × content_type` 的组合枚举，而非写死 5 个平台名；
- ⚠️ 用户候选树缺 **`Publication`** 独立层（A3 要求）——同一 Video 应能产生多个平台 Publication。

A1–A4 四问的明确答案见 Doc 2 §5。

---

## 3. 两类专业 Workspace（B 节）

### 3.1 Video Production Workspace（平台无关）

**责任链（Production Pipeline）**：
`选题 → Script → Assets → Generate/Shoot → Edit → Content Review → Canonical Video Result`

**拥有**：Canonical Content、Script、Assets、Production Result（平台无关母版）。
**能力提供方**：CapCut / 即梦 / 可灵 / HeyGen / Runway = **VIDEO PRODUCTION CAPABILITY PROVIDERS**。
**员工角色示例**：选题策划、脚本、素材、生成/拍摄、剪辑、内容审核。

### 3.2 Channel Operations Workspace（每平台一个）

**实例**：Douyin Operations / XHS Operations / TikTok Operations / Bilibili Operations / YouTube Operations。

**责任链（Channel Operations Flow）**：
`Content Intake → Platform Adaptation → Platform Review → Scheduling → Publishing → Engagement → Analytics → Feedback`

**拥有**：Channel Variant、Publication、Engagement、Analytics（均为 per-platform）。
**能力提供方**：各平台 Connector = **CHANNEL CAPABILITY PROVIDERS**（Douyin / XHS / Bilibili / YouTube …）。
**员工角色示例**：渠道运营、平台适配、社区管理/互动。

### 3.3 是否符合 Curis 架构

完全契合 **Professional Workspace + Employee Responsibility + Capability Provider**：

- 两类 Workspace 都是 **Professional Workspace**；
- 员工是**动态调用能力的岗位**（非固定 Agent）—— 生产岗调用生产工具，运营岗调用渠道 Connector；
- 能力**可替换不写死**：生产工具可从 CapCut 换剪映云；渠道可从抖音扩展到视频号/Rumble；
- 这与 `working_memory` 中产品主轴「四原则不可动摇」一致：全自动任务流是核心、能力可替换、员工=动态调用能力的岗位。

### 3.4 Target Channels 前置（B4 关键约束）

> **目标渠道必须在 Production 之前确定，并生成 Production Requirements。**
> Default Channel Set 由 Business / Workspace 记忆，不要求每条内容重复选择。

- Production Requirements 示例：需同时产出 `9:16`（Douyin+XHS+TikTok）、`16:9`（YouTube+Bilibili）；时长上限取各渠道最小值；若含 Bilibili 需预留 `copyright` 字段与原创证明；若含 YouTube 需预留 `publishAt` 调度占位。
- 这是连接两个 Workspace 的**契约点**：Channel Intent（来自 Channel Operations / Business 记忆）→ Production 消费 → 产出满足多渠道要求的 Production Result。

---

## 4. XHS 重理解（C 节）

- 当前 **Approved XHS Instance = XHS Note Publishing / Operations 首版** —— **不改**。
- 未来 XHS Channel Operations 应同时接受：
  - `Canonical Note → XHS Note Variant → Publication`
  - `Canonical Video → XHS Video Variant → Publication`
- 证据：XHS 已支持视频笔记（9:16 首选 / 3:4 / 16:9 兼容，时长最长约 15min，封面独立 3:4）。
- **结论**：当前 XHS = 首个 Content Type（Note）实现，**不是「XHS 永远=Note」**。稳定的概念是 *XHS Channel Operations Workspace*，Content Type 是其参数。

---

## 5. 本轮 Douyin Research 重归类（D 节）

| 原归类（错误） | 重归类为 |
|---|---|
| 发布 / 互动 / 数据 / OAuth / Scope / Webhook / 账号要求 | **DOUYIN CHANNEL CAPABILITIES**（归属 Douyin Operations WS / Douyin Connector） |
| CapCut / 即梦 / 可灵 / HeyGen / Runway | **VIDEO PRODUCTION CAPABILITY PROVIDERS**（归属 Video Production WS） |

**官方能力事实保留**（用户明示「官方能力研究部分保留」），仅**重新归类**其归属域，不质疑事实本身。生产工具**不得混入** Douyin Connector。

---

## 6. 默认工作面重审（E 节）

### Video Production Workspace
默认面 **保持 = Production Pipeline**。内容项在生产阶段间流动，Pipeline 是最自然的默认面。

### Douyin Operations Workspace（及其他 Channel Operations）
候选对比：

| 候选面 | 评价 |
|---|---|
| Publishing Queue（待发布/已排期） | 强，运营日常核心 |
| Channel Content Pipeline（Intake→Adapt→Review→Schedule→Publish） | 强，线性流程清晰 |
| Calendar（排期视图） | 次级视图，非默认主面 |
| Engagement Inbox（评论/私信） | 强，互动是日常循环 |
| Performance / Analytics | 强，但偏周期查阅 |
| Mixed Operations Surface | 综合最优候选 |

**推荐默认 = Mixed Operations Surface（混合操作面）**：以 `Publishing Queue + Engagement Inbox + Performance 摘要` 三区为核心，Calendar 作为排期子视图，Pipeline 视图可选切换。
**理由**：渠道运营的日常是「发 + 互动 + 看数」循环，而非纯线性管道。
**不预设最终答案** —— 留待设计阶段用真实任务验证（与 `working_memory` §12「以用户能否在浏览器完成一件真实事情」牵引一致）。

---

## 7. 自动化政策结论降级（H 节）

本轮报告中原结论：

- ❌「全自动托管 = 封禁」
- ❌「发布前人工审核永远必须」

**均降级为 → `POLICY VERIFICATION REQUIRED`**，理由：

- 不进入 Frozen Product Rule；
- 下一阶段单独核实：① 官方政策原文 ② 适用账号（个人/企业/品牌/员工号）③ 适用场景 ④「自动化」的精确定义 ⑤ 人工审核要求的边界；
- **证据闭合前，不得把「每次发布必须人工点击」写死**进任何产品规则或代码。

这意味着 Douyin Automation Research 中的政策强结论需回退为待验证项（见 Doc 3 处置）。

---

## 8. 与既有研究的衔接

- **Doc 2**：Canonical Content / Channel Variant / Publication / Engagement / Analytics 的数据模型与字段定义。
- **Doc 3**：5 平台差异矩阵（G 节）、B/E 深化、7 个必答问题、对 TTK / Douyin / XHS 三份既有研究的 KEEP/MODIFY/REINTERPRET/REJECT。
- **Doc 4**：AiToEarn 架构复盘与定位判断（F 节）。

---
*本模型为架构复盘参考，未固化进任何权威文档。下一步：建立 Video Production WS 与 Channel Operations WS 之间的 Contract 后分别设计（见 Doc 3 §7-Q7）。*
