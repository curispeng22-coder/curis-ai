# Curis TTK vs XHS — Reuse Boundary Matrix（复用边界矩阵）

**阶段**：TTK PRODUCT MODEL RESEARCH ONLY  
**状态**：TTK PRODUCT MODEL REVIEW REQUIRED  
**目的**：明确「抖音办公室」能从 Shared / XHS 借什么、只能复用底层能力不能照搬 UI、绝不能抄什么。  
**铁律**：禁止出现「XHS 换成 Video 就是 TTK」。

> 图例：
> - 🟢 **REUSE FROM SHARED** — 直接采用 Frozen Shell / Shared Pattern（全局共享，不属 XHS）
> - 🔵 **REUSE FROM XHS（模式/底层）** — 复用 XHS 的「模式」或「底层能力」，但 TTK 自行实例化，不搬 UI
> - 🟡 **TTK-SPECIFIC** — TTK 独有，XHS 没有
> - 🔴 **DO NOT COPY FROM XHS** — XHS 的 Instance 专业能力，TTK 绝不照搬

---

## 矩阵主体

| # | 维度 | 🟢 REUSE FROM SHARED | 🔵 REUSE FROM XHS（模式/底层） | 🟡 TTK-SPECIFIC | 🔴 DO NOT COPY FROM XHS |
|---|------|---------------------|-------------------------------|----------------|------------------------|
| 1 | **Shell 结构** | 四独立 Pane / T1–T3 Toggle / Company-wide Object Search / Resizable / Utility Maximize（Frozen §1） | — | — | — |
| 2 | **责任语义** | P1 三层责任 / P2 Presence / P3 System Activity / P4 Automation / P5 Handoff / P6 Result Reference / P7 CEO Decision（全采用） | — | Video 生产责任链实例化（策划→脚本→制作→审核→发布） | — |
| 3 | **默认工作面** | — | — | **Video Production Pipeline（按阶段）**，顶部 Attention 优先 | **❌ 不默认 Calendar**（XHS Calendar-dominant 是 Instance 专业，不升格） |
| 4 | **核心业务对象** | — | Content Object × Time「概念」可借鉴（对象长期追踪） | **Video**（带 Script/Assets/Production Result 重子树） | **❌ 不把 Note 当 Video 直接搬**（Note 生产子树轻，Video 重） |
| 5 | **Context Surface** | Adaptive Surface 机制（Frozen §2.2） | 选题库「模式」（信号/素材 Context） | 选题库/热点 + 脚本库/参考视频/Brand Knowledge | 不照搬图文选题语义 |
| 6 | **Utility Surface** | Adaptive Surface 机制 + 多模式声明（Frozen §2.3） | 预览「模式机制」（轻量引用开模式） | 视频预览/脚本预览/素材/字幕封面/发布结果/数据（模式更多） | 不照搬「图文预览」内容（封面+标题+正文+标签） |
| 7 | **Analytics 闭环** | System Activity 模式（P3）+ 自动反哺（P4） | 发布→自动 Analytics→反哺闭环「模式」 | 北极星=**完播率/两秒跳出/互动率/涨粉** | **❌ 不复制小红书指标**（收藏率等） |
| 8 | **Employee 协作** | Employee Workstation（§3.1）+ Presence（P2） | Calendar→Note Split / 责任链栈「模式」（adapt） | 视频责任链垂直栈（不同责任内容） | **❌ 不造「数据复盘员工」伪岗**（继承 XHS DO NOT COPY） |
| 9 | **审核交接** | Artifact Review「模式」（RD Candidate，责任未转移） | — | 制作送审核=Artifact Review Request | — |
| 10 | **CEO Decision** | P7（8要素/分层/Provenance/复杂度动作） | 合规类「简单动作」模式（[按建议处理][其他方案][暂缓]） | 投放预算/版权/合规「高风险」动作（[查看方案][暂缓]） | — |
| 11 | **发布日历** | — | Calendar 作为「末端排期视图」可后续复用（非默认） | Pipeline 之上的可选「排期视图」（RESERVED） | **❌ 不作为默认进入面** |
| 12 | **内容复用** | Automation by default（P4） | 内容复用反哺选题库「模式」 | 一条多平台/矩阵二次利用（RESERVED 高级） | — |

---

## 关键边界裁决（CURIS 建议）

1. **Calendar 不作默认**：XHS 的 Calendar-dominant 成立是因为图文轻、发布节奏是核心；TTK 视频重、生产是核心 → Pipeline-dominant。Calendar 仅可作 Pipeline 之上的「排期视图」（RESERVED）。
2. **Video ≠ Note 直接搬运**：Video 多一个独立 **Script 子对象**与 **Assets/Production Result** 结构，这是结构性差异，不是皮肤差异。
3. **指标不照抄**：XHS 北极星=收藏率；TTK 北极星=完播率/两秒跳出。Analytics 闭环「模式」可复用，具体指标必须重写。
4. **伪岗不继承**：XHS 已禁止「数据分析员工」「运营复盘员工」伪岗；TTK 同样——Analytics 默认 System Activity，深度解读可选员工（高级）。
5. **工具≠责任**：剪映/CapCut/Runway/即梦 是 Tool Capability，制作员工的「责任」是方向/审美/成片判断，不随工具升格为员工。
6. **审核=Artifact Review（非 Handoff）**：与 RD 一致，制作送审核不转移责任，保持 Instance Candidate，不升格 Frozen P5。

---

**状态**：TTK PRODUCT MODEL REVIEW REQUIRED  
**关联**：`Curis_TTK_Workspace_Product_Model_Proposal.md`（G 节摘要 + A–I 全案）、`Curis_TTK_Workspace_Reference_Research.md`（外部证据）

**UI Designer** · 2026-08-15 · RESEARCH ONLY
