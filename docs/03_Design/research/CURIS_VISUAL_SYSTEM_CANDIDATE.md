# CURIS VISUAL SYSTEM CANDIDATE

Status: Review
Authority Class: RESEARCH
Disposition: SHARED VISUAL SYSTEM CANDIDATE / CEO REVIEW REQUIRED
Owner: Product / Design
Updated: 2026-08-23
Baseline: main @ c797db840bad285d7e9f1962d06eac61aa28508b

> 本文是候选，不是 Frozen Design System，不修改现有权威或实现。

## 1. Philosophy

**Calm Surface / Strong Focus / Rich Work**。

- Calm Surface：中性、低噪音、可长时间阅读。
- Strong Focus：每个视口默认一个 L1，主行动默认一个。
- Rich Work：保留经营对象和证据，通过层级与披露管理复杂度。

## 2. Focus and attention

| Level | Candidate meaning |
|---|---|
| L1 | 当前 Decision、Work、Insight、Conversation、Critical Change 或 Business Object |
| L2 | Current Employee、Surface、Cycle、Work state |
| L3 | Result、Handoff、Evidence、Plan、related objects、supporting metrics |
| L4 | Time、Source、History、File、technical metadata |

默认预算：1 L1、≤2 明显 accent areas、≤1 Primary CTA、Raised surface 稀缺、其余主动后退。

## 3. Typography

候选层级：Display/Focus 28–36/600；Page Title 22–24/600；Section 17–18/500–600；Object 15–17/500；Body 14–15/400；Supporting 13–14/400；Metadata/Label 11–12/400–500；Numeric 13–18/500–600 tabular-nums。中文优先，正文不用 Light，具体字体和最终值待 benchmark。

## 4. Spacing and content width

候选节奏：4/8 micro，12/16 component，24 section，32/48 page，64+ 仅 hero/empty。候选 content modes：Reading 640–760px；Work 720–1040px；Operating 920–1200px；Dense Data 可扩展但保留 context anchor。不要全站一个 max-width。

## 5. Color roles

使用 semantic roles，不直接向页面分发 Hex：`brand.primary`、`focus.primary/soft`、`action.primary/secondary`、`surface.canvas/default/subtle/focus`、`text.primary/secondary/tertiary/on-brand`、`border.default/subtle/focus`、`attention.pending/warning/critical`、`success/error`、`employee.active/blocked`。

Deep Green：候选保留，降频使用；品牌锚点、主行动、少量 focus 可以用，大面积皮肤、所有 active、所有链接不使用。颜色不能独立承载状态。

## 6. Brand and domain accent

Curis signature = 中性表面 + 受控 Deep Green + 中文排版 + Employee presence + Work/Result/Evidence reference + 稳定节奏 + 克制 motion。Professional accent 只在图表、Calendar/Content 类型、Domain Object、专用可视化和领域状态中出现；不能改变壳层、导航、Composer、通用文字和基础焦点语义。

## 7. Surface, elevation, card, border, radius, shadow

层级：Canvas → Default → Focus/Raised → Overlay。Typography → Spacing → Alignment → Divider/Subtle Surface → Card。Must Card 仅为独立对象、selected/focus object、action group、overlay；禁止消息、metadata、每个 KPI、每个 section、每个 Employee 默认 Card。Raised/Shadow 只为真实 elevation；radius 以 4/6/8 为主，10/12 仅大型 focus/overlay，均待验证。

## 8. Employee

统一身份组：Avatar、Name、Role、Scope、Status、Current Work、Conversation affordance。三入口共享身份但改变 L1：Direct Conversation = Communication；Current Work = Work Collaboration；Employee Profile = Employee Identity。禁止在线墙、Agent monitoring wall、三套独立 Employee 卡片皮肤。

## 9. Conversation and Composer

Conversation 是阅读流，不是气泡墙；正文列 640–760px 候选；长回答用标题/段落/列表/折叠；Work、Result、Handoff、Evidence 用 inline reference 或单一 focus surface。Composer 保持 Input + 目标/路由 + Auto + Voice + Send；低频能力渐进披露；主行动清楚，技术能力退后。

## 10. Current Work and object semantics

Current Work 首先显示 Goal、Current Activity、Important Judgment、Result、Handoff；使用 timeline、rows、disclosure，不使用 Dashboard Card Grid。Result = 产出；Evidence = 依据/追溯；Decision = 选择/责任/行动。三者靠结构、文案、来源和行动关系区分，不靠三种大彩色卡片。

## 11. Dense data and modes

Table/List/Calendar/Metrics 共享文字、状态、focus、divider 语义；指标不逐个卡片化。Comfortable 为默认；Compact 仅减少 chrome/间距，不牺牲正文可读性。Responsive priority：1440 完整，1280 Utility 可收窄，1024 Context/Utility 折叠，L1 不丢。

## 12. Accessibility and motion

对比度、键盘 focus、target size、字体放大、色彩独立性、状态文字、屏幕阅读器命名属于必验项。Focus 不只靠颜色。Motion 只服务 pane transition、utility open、focus change、employee response、work update、decision arrival；短、可打断、可减少。

## 13. Anti-patterns

禁止或强烈挑战：Card Wall、Dashboard Wall、Pill Everywhere、Gray-on-Gray、Color Everywhere、No Visual Focus、Everything Bold/Equal、Huge Empty Space、Over-compressed Density、Agent Monitoring Wall、File Manager Feel、Chat Bubble Wall、Engineering Console、Gradient AI SaaS、Excessive Radius、Excessive Shadow。

## 14. Acceptance questions

1. 2 秒首扫是否找到一个 L1？
2. 删除所有颜色后层级是否仍成立？
3. 是否只有一个 Primary CTA？
4. Employee 三入口是否同一身份、不同任务？
5. Rich Work 是否保留 Goal/Result/Evidence/Decision 而没有卡片墙？
6. XHS、RD、CEO Desk、Business、Commerce 是否都能复用规则，只改变 layout/domain annotation？
7. Light/Dark、中文长文、Compact、1024 宽度是否仍可读？

