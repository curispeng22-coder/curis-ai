# Curis XHS Workspace Reference Research

**Status**: Review — **XHS READY FOR DESIGN**  
**阶段**: 第八轮专项 · XHS Workspace（小红书运营办公室）· Reference Research 阶段  
**研究日期**: 2026-08-15  
**上位依据**（按权威顺序）:
1. `docs/01_Product/Curis_Product_Blueprint.html`（v5.1 · Single Current · Status: Review）
2. `docs/03_Design/Curis_UI_Frozen_Spec_2026-08-04.md` + `_system/tokens.css`（Frozen 视觉唯一真源）
3. `docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`（Shell Contract + Shared Patterns · A 阶段）
4. `docs/01_Product/Curis_RD_Workspace_Instance_Spec_v1.md`（RD 实例 · **APPROVED CANDIDATE**，仅作"第一个实例"参照，不作模板）

**本阶段产出边界**: 仅做 Reference Research + Design Brief，**不画页面、不改代码、不修改 Shell Contract / Blueprint / Frozen 令牌**。  
**关键禁令**: RD Workspace 只是第一个 Professional Workspace Instance（研发专业实现），**不是小红书页面模板**。禁止把研发的 Conversation / 文件树 / Diff 布局换皮成小红书。

---

## 0. 研究定位与边界（最高优先级）

本研究的唯一目的：回答"小红书运营办公室在 Curis 里真正应该怎样工作"，而不是"把研发 Workspace 改个皮肤"。

> **核心认知**：研发 Workspace 的主工作区是"垂直栈 Employee Workstation + Conversation"，因为研发的责任载体是**代码与对话**；小红书运营的责任载体是**内容（笔记）与时间（日历/发布队列）**。两者的 Main 内核本质不同。把研发的 Conversation 内核直接换成"小红书对话"是换皮，不是设计。

研究方法：研究**成熟产品的真实功能形态**（小红书官方工具、第三方数据工具、跨平台社媒管理产品），据此归纳小红书运营办公室应有的工作结构与 Surface 分配，而非从直觉假设。

---

## 1. 参考产品调研（真实功能证据）

### 1.1 小红书官方创作 / 专业工具

**创作服务平台（creator.xiaohongshu.com）** —— 个人与品牌创作者的官方工作台：
- **内容发布**：图文 / 短视频发布，支持**定时发布**与**草稿箱**；
- **创作辅助**：话题推荐、AI 文案润色、违禁词 / 敏感词检测；
- **数据洞察**：单篇笔记数据、账号趋势、粉丝画像；
- **商业合作入口**：蒲公英（pgy.xiaohongshu.com）的任务承接。

**蒲公英（pgy.xiaohongshu.com）** —— 品牌商业合作平台（专业号 / 企业号）：
- **合作任务**：品牌方下单、创作者接单、内容 brief；
- **数据看板**：合作笔记表现、转化；
- **多账号 / 矩阵管理**：品牌多账号视角；
- **财务管理**：结算、佣金；
- **API**：对外数据接口。

> 关键启示：官方工具本身**没有把"对话"作为主界面**。它的主界面是"发布 / 草稿 / 数据 / 合作"四类业务能力，Conversation 不是中枢。

### 1.2 第三方数据分析工具（行业范式）

- **千瓜数据**：内容深度分析、CES 评分拆解、爆款笔记拆解、达人深度画像。定位"内容深度 + 达人"。
- **灰豚数据**：投放分析、爆文复用追踪、商品榜单。定位"投放 + 商品"。
- **新红数据**：行业研究、周 / 月榜单、选题灵感库。定位"行业 + 选题"。
- **官方创作者中心**提供免费基础数据，第三方工具提供深度与跨账号视角。

> 关键启示：数据分析工具的核心对象是**内容（笔记）× 指标（CES 维度）**，且强调"爆款拆解 / 选题灵感"——即内容对象的可复用性，而非会话流。

### 1.3 跨平台社媒管理成熟产品（Later）

**Later**（社媒日历 / 多账号 / 分析标杆）的功能形态：
- **Visual Calendar（可视化日历）**：拖拽规划内容，所见即所得；
- **Multi-Profile Scheduling**：多账号 / 多身份定时；
- **Draft Posts / Auto Publish**：草稿、自动发布；
- **Best Time to Post**：基于数据的发布时机建议；
- **Hashtag Suggestions**：标签建议；
- **Analytics**：互动类指标（近似 CES 维度：保存 / 评论 / 分享 / 点击）；
- **Link in Bio / AI Caption Writer / 团队审批流 / 社媒监听**。

> 关键启示：Later 的 Main 内核是**日历（时间轴）+ 内容卡片**，Utility 是**预览 / 分析 / 审批**，而不是对话。这印证了"内容运营主工作区 ≠ Conversation"。

### 1.4 内容运营团队与真实 SOP

成熟内容运营完整工作流（来自行业 SOP 研究，非假设）：
1. **账号基建**：定位、人设、视觉风格统一；
2. **选题策划**：建立**选题库**（配比约 7:2:1 = 7 成已验证方向 / 2 成延伸 / 1 成测试）；来源 = 搜索下拉词、评论区提问、热门话题；
3. **单篇制作**：3:4 竖版封面 → 标题公式（数字 / 痛点 / 身份）→ 正文三段式 → 标签（1–3 个大词 + 3–5 个长尾）；
4. **发布冷启动**：定时发布 + 5/30/60 分钟"赛马"观察，早期互动决定流量池；
5. **数据复盘**：CES 评分维度 —— 点击率 → 完读率 → 收藏率（健康 >5%）→ 评论 → 转粉；
6. **爆文放大 / 复用**：拆解爆款结构，复制选题与表达；
7. **风险避坑**：违禁词、过度营销、人设漂移。
团队典型 6 岗：内容策划、设计 / 摄影、数据分析、审核、发布运营、复盘。

> **数字降级声明（本轮修正 2 / 3）**：上述 **7:2:1 选题配比、5/30/60 冷启动赛马、收藏率 >5%、CES 评分维度** 均为 **Expert Knowledge / Strategy Template 示例**，属于可配置的运营知识，**不属于固定 UI / Product Contract**。Curis UI 只提供可配置能力：策略模板、观察阶段、指标与阈值；具体数值由用户 / 专家知识设定，CES 仅是默认 Analytics Template 之一，非不可变指标体系。

> 关键启示：工作流是**"选题 → 策划 → 制作 → 审核 → 发布 → 数据 → 复盘"的环状**，内容对象（笔记）在环中流转并积累数据；Conversation 只在"策划讨论 / 审核沟通"节点出现，不是贯穿全程的主轴。

---

## 2. 研究必须回答的 8 个问题

### Q1. XHS Main Workspace 应以什么为核心？（不要默认 Conversation）

**结论：Main 核心 = 内容对象（Note / 笔记）× 时间（Content Calendar / 发布队列），而不是 Conversation。**

论证：
- 官方创作服务平台、Later、千瓜的共同主界面都是"日历 + 内容卡片 + 数据"，没有一家以对话为主轴；
- 内容运营的责任载体是**可复用、可复盘、带数据的笔记对象**，而非一段对话；
- Conversation 在研发里是核心，是因为代码生成依赖 Agent 对话上下文；小红书内容生产可以由 AI 员工执行，但**产出物是笔记，不是对话记录**。

**冻结的语义契约（本轮修正 1）**：Main 的核心必须是 **"内容对象（Note）× 时间（Calendar / 发布节奏）"双主轴语义**——即主工作区必须同时承载"一篇内容"与"它在时间线上的位置"。这一语义契约**冻结**，不可动摇。

**不冻结的几何布局（本轮修正 1）**：具体的空间几何——如"左 Calendar + 右 Note""上日历下笔记""笔记为主、日历为覆盖层"——**不冻结**。Design 阶段可自由探索 Calendar-Dominant / Split Dual-Pane / Object-First(Focus) 等方案（见 Design Exploration Round 1）。

> 注意：本 Research 强烈建议**不以 Conversation 为默认 Main 核心**；双主轴语义是底线，几何是 Design 的探索空间。

### Q2. 哪些信息需持续浏览，适合 Context Surface（左 · Adaptive）？

适合 Context Surface 的"持续浏览型"信息（与主工作区当前操作相关、但不应挤占主区）：
- **选题库 / 信号监测（Topic & Signal Library）**：搜索下拉词、评论区提问、热门话题、竞品爆款选题；创作时持续参考；
- **账号 / 品牌基准**：当前运营账号定位、人设、视觉规范、违禁词表；
- **责任上下文**：当前 Workspace、当前运营目标（如"本月涨粉 3000"）、相关素材目录；
- **粉丝 / 行业信号**：新红行业榜、千瓜达人动态（轻量订阅）。

> 与 Shell Contract §2.2 一致：Context 内容由 XHS Instance 声明（选题库 / 信号），默认收起，按需出现，不预设全产品统一内容。

### Q3. 哪些辅助专业工作适合 Utility Surface（右 · Adaptive）？

适合 Utility Surface 的"专业工具面"（沉浸、按需、可返回）：
- **图文预览（Note Preview）**：3:4 封面 + 标题 + 正文 + 标签的完整还原预览；
- **数据看板（Analytics）**：单篇 CES 维度、账号趋势、粉丝画像；
- **素材 / 资料（Asset / Reference）**：图片库、参考笔记、品牌视觉规范文档；
- **审核详情（Review Detail）**：违禁词报告、人设一致性检查、Handoff 上下文包；
- **发布队列（Publishing Queue）**：定时列表、赛马状态（可选在 Utility 或 Main 旁开）。

> 与 Shell Contract §2.3 一致：Utility **模式完全由 XHS Instance 声明**（图文预览 / 数据看板 / 素材 / 审核），Shell 只提供容器与开合机制。专注模式用更深背景制造"沉浸工具"感。

### Q4. Employee Workstation 在内容运营中何时出现？（不要为复用而强行展示）

**结论：Employee Workstation 仅在"需要 CEO 看到某个 AI 员工正在做 / 卡在某件事"的节点出现，而不是常驻主区。**

适用出现时机：
- **创作执行中**：AI 员工正在生成封面 / 文案，作为"内容生产中"的责任状态呈现；
- **审核阻塞（needs_ceo）**：品牌 / 敏感表达需 CEO 确认，员工卡进入 `needs_ceo` 责任状态；
- **Handoff**：策划员工 → 审核员工的责任交接；
- **失败 / 恢复**：生成失败需重试边界。

**不应出现的时机**：
- 日常浏览日历、看数据、看预览时，**不应**强制展开员工卡；
- 不要把"员工列表"放成常驻侧栏或顶部 tab（违反 Shared Pattern §3.1 Correction + RD Brief §14）。

> 与矩阵一致（Shell Contract §4）：Employee Workstation 对小红书为 **⚪ 可选采用**，非 Required。内容对象是主，员工是"在需要时浮现的责任状态"。

### Q5. 内容运营真实工作流是什么？（根据研究修正）

研究修正后的真实环状工作流：

```text
选题库 / 信号监测
   ↓ （选题策划：7:2:1 配比）
单篇制作（封面 3:4 → 标题 → 正文三段式 → 标签）
   ↓
审核（违禁词 / 人设一致性 / 品牌确认）
   ↓
定时发布 / 发布队列（冷启动 5/30/60 赛马）
   ↓
数据复盘（CES：点击→完读→收藏>5%→评论→转粉）
   ↓
爆文放大 / 复用（拆解结构 → 复制选题）
   ↺ 回到选题库（数据驱动下一轮选题）
```

**关键修正**：
- 不是线性的"策划→发布→结束"，而是**数据驱动的环**；
- **审核**是独立、不可省略的节点（对应 Handoff / Needs CEO Pattern）；
- **复盘直接反哺选题库**（Content Object 的数据沉淀回写 Topic Library），这是 XHS 自有 Pattern 闭环，研发没有对应物。
- **数字非契约（本轮修正 2 / 3）**：7:2:1 / 5/30/60 / 收藏率>5% / CES 均为 Strategy Template / Expert Knowledge 示例；UI 以可配置策略、观察阶段、指标阈值、Analytics Template 承载，不写死。

### Q6. Shared Patterns 如何自然复用？（只按需要采用，不要求全部）

| Shared Pattern | XHS 复用方式 | 采用度 |
|---|---|---|
| Employee Workstation | 创作执行 / 审核阻塞 / Handoff 时浮现，非常驻 | ⚪ 可选 |
| Handoff Event | 策划 → 审核责任交接，轻量呈现 | ⚪ 可选 |
| Needs CEO / Decision | 品牌 / 敏感表达确认，橙色 Decision Banner | ✅ 典型 |
| Result Reference | `📊 数据看板 ▸` / `✅ 笔记已发布 ▸` 轻量引用 | ✅ 典型 |
| Composer | 仅在某员工展开 Conversation 时出现（如审核沟通） | ⚪ 可选 |
| Context Surface | 声明为选题库 / 信号监测 | ✅ 典型 |
| Utility Surface | 声明为图文预览 / 数据看板 / 素材 / 审核 | ✅ 典型 |

**原则**：Pattern 是能力不是布局。XHS 自然采用 Context / Utility / Result Reference / Needs CEO，Employee Workstation 与 Composer 仅在节点浮现。绝不为了"复用而强行展示员工"。

### Q7. 哪些是小红书自己的 Professional Patterns？（先研究不假设）

研究归纳出的 XHS 自有（非复用自研发）Professional Patterns：

1. **Content Calendar（内容日历）**：周 / 月视图，拖拽规划，发布节奏可视化。XHS 主轴的左半。
2. **Content Object / Note（内容对象）**：单篇笔记作为一等公民对象，含封面 / 标题 / 正文 / 标签 / 状态 / 数据快照，可复用、可复盘、可进入发布队列。XHS 主轴的右半。
3. **Publishing Queue（发布队列）**：定时列表 + 冷启动赛马状态（5/30/60 观察），多账号发布管理。
4. **Analytics（数据分析）**：默认 Analytics Template，指标与阈值**可配置**；CES 维度（点击 / 完读 / 收藏 / 评论 / 转粉）仅是示例模板之一，**非不可变 Curis 指标体系**（本轮修正 3）。
5. **Topic & Signal Library（选题 / 信号库）**：选题沉淀 + 信号监测（搜索词 / 评论 / 热门 / 竞品），并接收复盘反哺。
6. **Review Gate（审核闸）**：违禁词 / 人设一致性 / 品牌确认，产出审核详情并可升级 Needs CEO。
7. **Content Reuse Loop（内容复用环）**：爆文拆解 → 结构复制 → 选题库更新，数据驱动的闭环（研发无对应物）。

> 这些 Pattern 属于 Layer 4（XHS Instance 级），不进入 Shell Contract / Shared Pattern（Layer 1–3），保持 Contract 通用、Instance 专业。

### Q8. 特别遵循 Low Surface Complexity, High Functional Density

落点原则：
- **第一眼简单**：默认 Main 只显示 Content Calendar + 当前选中笔记概要；Context / Utility 默认收起（Adaptive Surface 默认不占空间，Shell §2.1）。
- **需要时功能自然出现**：点笔记 → 右开图文预览 / 数据看板；点选题 → 左开选题库；审核阻塞 → 橙色 Decision Banner + 员工 `needs_ceo` 浮现。
- **高密度不靠常驻墙**：不在主区铺满工具图标墙；专业工具走 Utility Surface 按需进入，返回锚点保留。
- **禁止平行堆砌**：不把 7 个 XHS 自有 Pattern 同时展开；一次聚焦一个对象（笔记 / 日历日 / 选题）。

---

## 3. XHS 自有 Professional Patterns 详列（Instance 级）

| Pattern | 主区 / Surface | 触发 | 复用 Shared |
|---|---|---|---|
| Content Calendar | Main（时间轴） | 默认 | Context 可开选题库 |
| Content Object / Note | Main（内容对象） | 选中时间项 / 新建 | Utility 开预览 / 数据 |
| Publishing Queue | Main 旁 / Utility | 定时发布（观察阶段如 5/30/60 为可配置示例） | Result Reference |
| Analytics（默认 Template，可配置指标/阈值） | Utility | 点数据引用 / 选中笔记 | Result Reference |
| Topic & Signal Library | Context（左） | 创作 / 选题时 | Context Surface |
| Review Gate | Utility / Handoff | 审核节点 | Handoff + Needs CEO |
| Content Reuse Loop | 跨对象数据流 | 复盘结论 | Result Reference |

---

## 4. 与 Shell Contract 的适配性评估（Delta Candidate，不修改）

### 4.1 现有 Workspace Shell Contract 是否适合 XHS？

**结论：基本适合，无需推翻。** Shell Contract 的"Main 必有 + Context/Utility 为 Adaptive Surface + 六区导航 + Shared Pattern 矩阵"对 XHS 完全成立：
- Main 由 XHS 声明为"日历 + 内容对象"，符合 §0.1 边界修正 2（Main 布局由 Workspace 决定）；
- Context = 选题库、Utility = 预览/数据，符合 §2.2/§2.3 的"内容由 Instance 声明"；
- 六区导航不变，XHS 作为"业务空间"子项出现。

### 4.2 可直接复用的 Shared Patterns

✅ 直接复用（不改）：Context Surface、Utility Surface、Result Reference、Needs CEO / Decision、Handoff Event。
⚪ 按需复用（不强制）：Employee Workstation、Composer（仅在节点浮现）。

### 4.3 暴露出的 Shell Contract 不足（**已裁决 · 2026-08-15 XHS Review**）

XHS Research 方向已通过。以下 4 个 Delta Candidate 经 CEO / 设计负责人裁决：

| # | 裁决 | 理由 / 动作 |
|---|---|---|
| **Delta-X1** | **不采纳** | Main 布局本就由各 Instance 决定（Shell Contract §0.1 边界修正 2 已明确），无需再显式区分"单核 / 双核"。双主轴语义在 XHS 内冻结，不影响 Contract 通用性。 |
| **Delta-X2** | **采纳 · 已回写 Shell Contract §4 / §3.1** | 将 XHS 正式补为第二个 Context / Utility 实例示例（Context = 选题库（信号/素材）；Utility = 图文预览 / 数据看板 / 审核）。见 Shell Contract 文档对应更新。 |
| **Delta-X3** | **暂不采纳** | 不创建独立的 "Business Object Surface" 抽象；业务对象（Note 等）由 Instance 在 Main 内自行表达即可，保持 Contract 精简。 |
| **Delta-X4** | **不升 Shared Pattern** | 不修改 Shared Employee Workstation 状态模型；创作类进度直接用现有 `Current Work / Progress` 字段表达（如"封面生成中"），无需新增子状态。 |

> 结论：仅 X2 落地（已回写 Shell Contract §3.1 / §4），X1 / X3 / X4 驳回。Shell Contract 未做其他改动，遵循"变更顺序 = Blueprint → Design → Code"。

---

## 5. 参考产品映射表

| 设计关注点 | 主要参考 | 次要参考 | 边界 |
|---|---|---|---|
| 内容日历 / 规划 | Later Visual Calendar | 小红书创作服务定时发布 | 采用日历 + 拖拽，不抄 Later 社媒品牌视觉 |
| 内容对象 / 笔记 | 小红书创作服务平台 | Later Draft Posts | Note 为 Curis 业务对象，非聊天记录 |
| 图文预览 | 小红书 App 笔记详情 | Later Preview | 3:4 还原，不抄平台 UI |
| 数据分析 / CES | 千瓜 / 灰豚 / 新红 | Later Analytics | 采用 CES 维度，不抄第三方仪表盘视觉 |
| 选题 / 信号 | 新红选题灵感 | 千瓜爆款拆解 | Topic Library 为 Curis 自有沉淀 |
| 审核闸 | 小红书违禁词检测 | 蒲公英内容规范 | Review Gate 复用 Handoff + Needs CEO |
| 多账号 / 发布队列 | Later Multi-Profile | 蒲公英矩阵 | Publishing Queue 为 XHS 自有 Pattern |
| 员工 / 责任 | Curis Shared Pattern | — | Curis 组织层专属，不抄任何外部产品 |

---

## 6. 禁止项（防换皮 / 防 RD 复制）

- ❌ 把研发的 Conversation 内核换皮成"小红书对话"，以对话为主轴；
- ❌ 把研发的文件树 / Diff 布局平移成"素材树 / 数据 Diff"；
- ❌ 常驻员工列表侧栏 / 员工顶部 tab；
- ❌ 把 7 个 XHS 自有 Pattern 同时铺满主区；
- ❌ 在对话内嵌入完整数据表 / 长图文（应走 Result Reference → Utility）；
- ❌ 把 Shell Contract 当成"四栏固定"（Context/Utility 是 Adaptive，默认收起）。

---

## 7. Research Review Gate

进入 Design 阶段前，须确认：
1. "内容对象 × 时间"双主轴语义已冻结（非 Conversation）；具体几何布局（左日历+右笔记等）明确不冻结，交由 Design 探索；
2. Context = 选题库 / 信号、Utility = 图文预览 / 数据 / 审核 已声明；
3. Employee Workstation 仅在节点浮现，非常驻；
4. 真实环状工作流（含审核闸、复盘反哺选题）已被采纳；
5. Shared Pattern 复用矩阵已落定（XHS 列补实）；
6. 4 个 Delta Candidate 已记录待 Review，未擅自修改 Shell Contract。

**本阶段结论**：XHS RESEARCH REVIEW REQUIRED → 已裁决通过，状态升为 **XHS READY FOR DESIGN**。4 点修正已落地（双主轴语义冻结 / 几何不冻结 / 数字降级为 Strategy Template / Shell Delta 裁决），可进入 XHS Design Exploration。

---

**UI Designer**: UI Designer  
**文档日期**: 2026-08-15  
**阶段**: XHS 专项 · Reference Research（不画页面、不改代码、不修改 Contract）
