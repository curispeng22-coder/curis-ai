# CURIS V1 — OPERATING INTELLIGENCE UI ACCEPTANCE

**Authority Class**：CURRENT UI IMPLEMENTATION INPUT / ACCEPTANCE REGISTRATION
**Status**：Frozen
**Date**：2026-08-31
**Disposition**：PRODUCT ACCEPTED / UX ACCEPTED / UI ACCEPTED

## Accepted result

- **Operating Intelligence Product**：ACCEPTED
- **Operating Intelligence UX**：ACCEPTED
- **Operating Intelligence UI**：UI ACCEPTED
- **Current Figma Design Baseline**：`172:3` / `172:277` / `172:551` / `172:825`（1440 × 900 Light）
- **Remaining P1**：NONE
- **Remaining P2**：Prototype wiring、Dark、1024、accessibility / keyboard、real Runtime data-density verification
- **Implementation**：FRONTEND PRODUCTIZATION REQUIRED
- **Runtime / Data**：PARTIAL

## Product boundary

Operating Intelligence 负责趋势、比较、归因、经营评价、分析报告与专项分析；CEO Desk 负责当前注意事项、异常、结果和需要 CEO 决定的 Matter。Operating Intelligence 只消费 canonical Company / Business / Workspace / Employee / Result / Execution / Usage / Cost / Feedback / Review truth，不创建第二套 Metric Truth、Result Truth、Analytics Runtime 或 Decision。

## Accepted UX baseline

- `172:3`：Overview，Analyst-first / conclusion-first，支持趋势、Unknown、Recommendation、Evidence / Data Trust。
- `172:277`：Scoped Business Analysis，分离 baseline trend、attribution、cost / speed / quality / failure，并保留 Evidence / Unknown / Recommendation。
- `172:551`：Explore / Benchmark，明确 scope、time、definition、sample、data availability，不生成 synthetic ranking。
- `172:825`：Report / Decision Continuity，Fact / Analysis / Unknown / Recommendation / Evidence 回到既有 canonical Decision。

Hybrid capability envelope、Analyst-first skeleton 与 progressive Explore / Benchmark 已统一为当前 UX 基线；历史 Variant A/B/C 不再作为并列方案。

## Data truth boundary

无真实来源不得用 0、健康分数或合成排名替代未知。指标保留 source、更新时间、验证状态、缺失、来源不一致 / 需要核实与人工数据；成本、速度、质量、失败、验收和外部业务结果保持可解释分离。设计中的“司衡”“苏禾”仅为 Fixture，Frontend 必须消费真实 Employee / Analyst identity。

## Implementation boundary

本登记仅升级当前 UI / Product Completion 状态，不代表 Frontend、Metric Registry、Report Runtime、外部数据源或图表运行时已交付。下一 Gate：`OPERATING INTELLIGENCE PRODUCTIZATION CLOSURE`，范围为 Accepted Figma → Frontend → canonical analytics projection → real data truth → Report / Decision continuity → Browser / Desktop acceptance。

不修改代码、Backend、Runtime、Schema、DB、Figma 或高保真设计；不进行 commit / push。

## Next Product Completion area

`TALENT & CAPABILITY PRODUCTIZATION CLOSURE`。
