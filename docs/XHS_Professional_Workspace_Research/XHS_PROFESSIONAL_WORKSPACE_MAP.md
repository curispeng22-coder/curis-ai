---
title: XHS Professional Workspace Map
status: RESEARCH / EXPERT RECOMMENDATION
date: 2026-08-21
purpose: 只用结构图表达 XHS Workspace → Domain Navigation → Professional Surfaces → Core Objects → Detail Views → Capability/Truth Sources。非高保真 UI。
source: 本研究 §A–§W 的收敛；详见 CURIS_XHS_PROFESSIONAL_WORKSPACE_DOMAIN_RESEARCH.md
---

# XHS Professional Workspace Map

> 表达「Workspace 作为 Embedded Domain Application / Professional Operating Environment」的结构，不画页面、不定义几何。

## 1. 顶层结构（Workspace → Navigation → Surfaces → Objects）

```
XHS Workspace（小红书运营办公室 · Curis Company OS 的一个 Instance）
│
├─ DOMAIN NAVIGATION（六区导航下的 L1/L2/Detail/Scoped/Optional）
│
├─ PROFESSIONAL SURFACES（专业工作面）
│   ├─ L1: Operating Overview          （默认·语境恢复）
│   ├─ L1: Research & Insight          （研究洞察）
│   ├─ L1: Content Operating           （内容运营 = 生产 + 计划/日历 + 发布）
│   ├─ L1: Performance & Growth        （数据增长）
│   ├─ L1: Commercialization           （可选模块·成熟账号启用）
│   ├─ L2: Feedback Inbox              （用户反馈，轻 Surface）
│   ├─ L2: Team                        （Curis Employee 投影·Scoped）
│   └─ L2: Knowledge                   （Curis Global Knowledge 视图·Scoped）
│
├─ CORE OBJECTS（Domain canonical）
│   Account · Brand Brief · Topic · Experiment · Note · Brand Deal(optional)
│
├─ DETAIL VIEWS（对象展开）
│   Note detail · Competitor detail · Brand Deal detail · Experiment detail
│
└─ CAPABILITY / TRUTH SOURCES（能力/真相源）
    Research(外部源+AI) · Production(AI文案/配图+违禁词API)
    Publishing(开放平台+队列) · Analytics(蒲公英/千帆/灵犀/开放API)
    Feedback(官方/合规通道) · External Provider Boundary(动态 Platform Facts)
```

## 2. Domain Navigation 分级

```
L1（长期一级入口 · 建议 5）
 ├─ Operating Overview        ← 默认进入
 ├─ Research & Insight
 ├─ Content Operating
 ├─ Performance & Growth
 └─ Commercialization         （Optional Module·小账号隐藏）

L2（属于某 Surface）
 ├─ Topics / Experiment       （Content Strategy 内）
 ├─ Publishing Queue          （Content Operating 内）
 ├─ Feedback Inbox            （独立轻 Surface 或入 Insight）
 ├─ Team                      （Overview 或独立·Scoped 投影）
 └─ Knowledge                 （Overview 或独立·Scoped 投影）

Detail（对象展开时出现）
 ├─ Note detail · Competitor detail · Brand Deal detail · Experiment detail

Scoped View（复用 Company OS / Knowledge / Artifact）
 ├─ Team      = Curis Employee / Responsibility 投影
 ├─ Knowledge = Curis Global Knowledge 视图
 └─ Asset     = Curis Global Artifact

Optional Module（仅特定阶段启用）
 ├─ Commercialization（小账号隐藏）
 └─ Multi-account Matrix（Reserved）
```

## 3. Professional Surfaces × Core Objects 矩阵

| Surface | 主对象 | 关键能力 | 来源/真相 |
|---|---|---|---|
| Operating Overview | Account/Brand Brief/Goal/Stage | 阶段/目标/策略/注意力/下一步 | Curis 自治运营状态 |
| Research & Insight | Competitor/Trend/Keyword/Audience(evidence) | 外部采集、洞察、信号→选题 | 外部 Provider + AI |
| Content Operating | Note + Calendar View + Publishing Queue | 生产/计划/发布/赛马 | Production + 开放平台 |
| Performance & Growth | Performance Record/Audience(evidence) | 指标/趋势/受众/搜索/转化/归因 | 蒲公英/千帆/灵犀/开放API |
| Commercialization* | Brand Deal/Commercial Lead | 合作/报价/交付/回款 | 蒲公英/聚光/千帆 |
| Feedback Inbox | Comment/DM/User Question | 分类/线索/洞察回写 | 官方/合规通道 |
| Team* | Curis Employee/Responsibility | 责任视图/Handoff/Needs CEO | Curis 组织层 |
| Knowledge* | Curis Global Knowledge/Artifact | 品牌资料/规范/素材/研究 | Curis Global |

`*` = 可选模块 / Scoped 投影。

## 4. 对象分类（避免重造系统）

```
Domain canonical（持久业务对象）
 ├─ Account · Brand Brief · Topic · Experiment · Note · Brand Deal(optional)

View / Projection（非独立对象）
 ├─ Audience（Performance 投影）· Calendar Entry（Note+排期）· Publishing Queue Item（Note+状态）
 └─ Competitor / Trend / Keyword（Research 视图·外部源）

Artifact（复用 Curis Global）
 └─ Asset / Material

Evidence / Result
 ├─ Performance Record · Comment Insight · Growth Signal
 └─ Review · Operating Decision（Needs CEO / Handoff / 策略调整）

External provider object
 └─ Competitor 原始数据 · 平台原始数据
```

## 5. Autonomous Operating 映射（人类可见面）

```
Curis 自治运营                 XHS 人类可见 Surface
─────────────────────────────────────────────────
Goal                      →   Operating Overview（目标/阶段）
Strategy                  →   Content Strategy / Research & Insight
Operating Series/Cycle   →   Content Operating（生产→发布→数据→复盘）
Work                      →   Note / Experiment / Publishing Queue
Result                    →   已发布 Result / Performance Record
Evidence                  →   Comment Insight / Growth Signal
Evaluation                →   Performance & Growth（有效/无效·证据强度）
Leader Review             →   CEO（Needs CEO / 策略提案）
Next-cycle Decision       →   策略调整 / 新实验 / 商业化启用
```

> 不另造 Autonomous UI System：XHS Surface 即自治运营的人类可见专业界面；AI 员工在背后按规则推进，责任以 Employee Presence / System Activity 表达。

## 6. Calendar 的正确位置（一句话）

**Calendar = Content Operating Surface 内部的一等视图（承载 Note × Time 双主轴），不是 Workspace 默认入口。默认入口 = Operating Overview。**

---

*结构图仅表达关系，不定义像素/布局。几何由后续 Design Exploration 决定（Shell Contract 已支持 Instance 声明 Main/Context/Utility）。*
