---
title: Curis Content Growth — Employee Method Experience（员工工作方式体验）
status: OPERATING STRATEGY UX TRANSLATION · DESIGN CANDIDATE（非 Frozen · 非高保真）
date: 2026-08-16
covers: Brief §6 员工方式 / §7 对话驱动 / §8 来源组合 / §14 Token / §16 不固定5员工
sibling_wireframe: Curis_Content_Growth_Wireframe_B_Employee.html（场景 B 中保真结构稿）
upstream: Operating Strategy Product Handoff §2(C) / §3 / §5 / §7 / §12 First Version
discipline: Employee Method ≠ 工程配置后台；对话与直接编辑同一份方法；不固定5员工；Token 不进首版 UI
---

# 1. 核心定位：Employee Method ≠ 员工设置后台

Handoff §2(C) 明确：**Employee Method 是职责归属，不是「固定创建 5 个 Employee」，也不是复杂员工设置后台**。

正确产品形态：用户点某个 Employee → 看「他现在是怎么工作的」→ 想改就改（对话或直接编辑），且**两处改动同一份长期工作方法、互相可见一致**。

> 不要把员工工作方式呈现为需要逐项配置的复杂后台面板。

---

## 1.1 DELTA T5 — Employee Detail 必须保持 Shared 一致（不重定义 UI）

Employee 始终是 **Company OS Shared Employee**。Content Growth 可以增加「这个员工有哪些业务工作信息」，但**不能重新定义「用户怎么查看这个员工」**。

### 1.1.1 沿用 Shared Employee Detail 露出方式
若当前 Curis Shared Employee Detail 的既有交互是「点击 Employee → 右侧详情 / 折叠空间展开」，Content Growth **必须继续沿用**。不得因为单个业务：
- 把 Employee Detail 改成 Main 独立页面；
- 新建 Employee Method Workspace；
- 新建另一套 Employee Detail 交互；
- 改变全局 Employee 的露出方式。

### 1.1.2 Employee Detail 信息组成
Shared Employee Detail 原有内容继续保持（姓名 / 头像 / 岗位·Role / Organization / Agent·Model / Skills / Tools·Capability / Computer Access / Responsibility / Current Executor / Status）。Content Growth **只增加一个业务扩展 Section：「工作方式」**（如信息收集职责下：当前关注 / 工作节奏 / 信息雷达 / 最近变化 / AI 优化建议）。这些仍属 **Employee Information / Employee Detail**，不是新 Workspace Primitive。

### 1.1.3 职责决定扩展内容（Shared 容器 / Domain 扩展）
Employee Detail 容器保持 Shared；业务 / 职责只决定「工作方式」里展示什么：
- 信息收集 → Source Portfolio / 扫描方式
- 选题 → 选题重点 / Content Mix / 栏目
- 平台运营 → 发布节奏 / 平台关注
- 社区 → 评论关注 / 回复方式 / 用户问题提炼
- 数据分析 → 指标 / 观察方式 / 策略提案

未来 RD / Sales / Support 也可增加各自 Employee Method Extension，但**不能每个业务重新设计 Employee Detail**。原则：**Shared 定义「Employee 是谁、怎么查看」；Domain 定义「Employee 在这里怎么工作」**。

### 1.1.4 Context Isolation（Shared Employee ≠ Shared Context）
同一 Employee 可服务多个经营方向；无论从哪个 Workspace / Office 点击她，仍打开**同一个 Shared Employee Detail**；业务扩展内容按**当前 Context** 显示（如当前经营方向 = Curis AI → 只加载该 Responsibility / Office / Business Context 相关的 Employee Method）。**不得因员工服务多 Office 而自动显示 / 加载全部 Office Knowledge / Method Context**。保持 Shared Employee ≠ Shared Context。

### 1.1.5 Conversation + Direct Edit（KEEP 原设计）
原设计继续 KEEP：CEO 对员工说「这个网站以后每天也看看」→ 修改该 Employee **在当前 Context 下**的长期工作方法 → Shared Employee Detail「工作方式 / 信息雷达」同步出现该 Source；反向 GUI 删除 Source → Conversation / 后续执行使用更新后的同一份方法。仍只有一份长期经营方法。

### 1.1.6 若 Shared 权威不足 → 仅记录 DELTA CANDIDATE
如验证发现现有 Shared Employee Detail 权威不足以承载业务扩展 Section，**只记录 `SHARED EMPLOYEE DETAIL DELTA CANDIDATE`**，由 Shared 侧统一处理；Content Growth 不自行修改 Shared Pattern。

---

# 2. 「他现在是怎么工作的」（Brief §6 · 即 Shared Employee Detail 内「工作方式」扩展 Section 的内容）

以信息收集员工为例，用户查看的是**行为化描述**，不是参数表：

| 用户看到的 | 表达方式 | 不展示（进高级/设置） |
|---|---|---|
| 目前关注 | 官方动态 / 行业网站 / 平台热点 / 对标账号 / 用户评论（自然语言清单） | 扫描间隔秒数 |
| 工作节奏 | 「每天若干轮」 | Token 计数 |
| 最近变化 | 新增了什么源 / 降低了什么源频率 / 哪些来源质量下降 | 贡献度原始分 |
| 可操作 | 添加来源 / 暂停 / 删除 / 调整频率 | 权重公式 |

技术细节（扫描秒数、Token、贡献度原始分）只进「高级 / 设置」层级，避免吓到普通用户（Handoff §5）。

---

# 3. 对话驱动策略：改的是同一份方法（Brief §7 · Handoff §3）

**硬约束**：Conversation-driven 与 Inspectable/Direct Edit **修改同一套底层长期经营方法**，不允许「聊天一套 / GUI 一套」两套独立存储。任一处修改，另一处可见且一致。

## 3.1 三个对话场景（至少设计）

### A. 新增长期信息源
- CEO 对信息员工说：「这个网站不错，以后每天也看看。」
- Employee 回复：「已经加入日常信息来源。」
- **同步要求**：Employee Method GUI 的「信息雷达」必须立即出现这个 Source。

### B. 修改发布节奏
- CEO：「以后小红书晚上 9 点发。」
- **判定**：这是明确的 CEO 主动命令 → 直接执行，**不需要再创建一次 CEO Decision**（Handoff §6 关键裁定）。
- **同步要求**：该账号的「经营方式 / 发布规则」GUI 同步更新为「小红书 21:00」。

### C. 修改内容策略（CEO 主动命令 = 已决策，不再 P7）
- CEO：「这个月多做一点教程类内容。」
- **判定**：CEO 明确指令 = **决策已经发生** → 直接更新相应的策略 / 临时 Operating Rule → **留痕** → 执行。**不再创建一次 CEO Decision**（Handoff §6 关键裁定；与 Doc 4 §4 统一）。
- **歧义处理**：若语义存在期限 / 范围歧义（如「这个月」vs「以后都」），Employee 可自然追问：「只调整这个月，还是以后都提高教程占比？」——但**不能要求 CEO 再次批准自己的命令**。
- **同步要求**：经营方向 / 账号的「内容策略」GUI 同步反映新 Mix 倾向（同一份方法）。
- **边界**：只有 **AI 主动提出**超出既有经营策略的结构性长期变化 → 才按 Frozen P7（见 Doc 4 §5）。CEO 主动命令本身不触发 P7。

## 3.2 反向一致性

用户在 GUI 删除某 Source → 后续 Conversation / Employee Method 都使用新的同一策略（无第二份配置）。

> 原则落地：**Conversation + Direct Edit = 同一份长期经营方法**。这是 Brief §7 与 Handoff §3 共同的头号约束。

---

# 4. Source Portfolio / 信息雷达 Experience（Brief §8 · Handoff §7）

运营专家明确 Source Strategy 是核心能力。用户查看「信息收集员工当前的信息雷达」：

| 能力 | 用户面表达 | 备注 |
|---|---|---|
| 来源类别 | 官方 / 媒体 / 垂直 / 热点 / 对标 / 用户 / 内部 / 临时 | 分层，非配置树 |
| 来源 | 来源名 + 关注主题 | 自然语言 |
| 扫描频率 | 大致频率（每天 / 每 4 小时 / 实时热点） | 分级，非秒数 |
| 暂停状态 | 暂停 / 启用标签 | 可直接切 |
| 最近贡献/质量趋势 | 「这个源最近贡献在上升/下降」轻量趋势 | 不展示贡献度公式 |
| AI 建议 | 建议加入 / 建议降频 / 建议删除 | 建议可采纳/忽略 |

## 4.1 重点设计两个问题

- **「为什么这个 Source 还值得看？」** → 轻量说明：它最近贡献了哪些有效信号 / 有效选题。
- **「为什么 AI 建议少看 / 不看？」** → 轻量说明：质量下降 / 重复 / 低价值，附趋势。

> **禁止**：贡献度公式 / 阈值 / 权重展示给普通用户（Handoff §7 Reference Only）。仅呈现「值得看 / 建议少看」的结论与可理解理由。

---

# 5. Token / 成本体验（Brief §14）

用户**不需要管理 Token 工程参数**。但应理解「信息收集不是无限全网搜索」：

- 员工方式可表达：「重点关注 18 个固定来源 + 平台热点 + 用户评论」，而非「全网实时扫描」。
- 高级用户可见：扫描范围 / 频率 / 暂停来源（行为化，非工程参数）。
- **首版普通 UI 不设计**：Token Budget Slider / Context Window / Embedding / RAG 配置。

> 表达原则：用「关注什么、多久看一次、哪些暂停」的自然语言，替代一切内部 Token/检索工程参数。

---

# 6. 不固定 5 个员工（Brief §16 · Handoff §2(C)）

运营专家的「信息收集 / 选题 / 平台运营 / 社区 / 数据分析」是**职责归属**，不是「首版必须创建 5 个 Employee」。

设计要求：

- 一个 Employee **可承担多个职责**（如早期「内容运营员工」兼顾选题+发布+社区基础）。
- 未来业务增长后，职责再**拆成多个 Employee**（如视频常卡字幕 → 建议加字幕员工）。
- **不破坏 Company OS Frozen Organization 语义**：员工是动态调用能力的岗位，非固定 Agent 清单。

> 产品呈现上，用户看到的是「谁在负责什么」的**职责与行为**，不是「5 个固定员工卡片」。增员是未来候选（VISION 探索），本轮仅留入口形态。

---

# 7. 场景 B 中保真结构稿

关键场景「Employee Method / Source Portfolio」的中保真结构稿见独立文件：
**`Curis_Content_Growth_Wireframe_B_Employee.html`**

该结构稿演示（DELTA T5 修正后）：正常 Content Growth 工作面上点某 Employee → **沿用 Shared Employee Detail 露出方式**（右侧详情空间展开）→ 其中出现 Content Growth 业务扩展 Section「工作方式」→ 信息雷达可在该详情内继续下钻；并示意「对话改 Source → Shared Employee Detail 信息雷达同步」的一致性。验证的是「Domain 扩展 Employee 信息」，而非「Domain 重定义 Employee UI」。套用 Frozen Shell 四 Pane 标注。

---

# 8. 状态

```text
CONTENT GROWTH OPERATING STRATEGY UX TRANSLATION APPROVED CANDIDATE
```

（本文件为 APPROVED CANDIDATE；不修改 Frozen / Blueprint / XHS·RD / Runtime / Connector；不进高保真；禁词全落实：无 Policy inheritance / 无 Token 计数暴露 / 无 5 员工固定假设。已就地应用 DELTA T2 / T5。）
