# Commercial Configuration (`cmcf_*`) — Proposal & L2 Escalation

- **Prepared by**: 主理人(齐活林) · 交付总监
- **Date**: 2026-07-11
- **Trigger**: 总控决策席 directive "abc 依次执行" — step (b): 单独裁定 Commercial Config `cmcf_*`
- **Classification**: **L2 Gate #1 (商业模式变化) + #2 (收费规则变化)** — mandatory escalation

## 1. What `cmcf_*` Is

`cmcf_*` is the **Commercial Configuration** asset class — the 10th and final asset type in the AI Company Asset Factory taxonomy, sitting in **Gate B Variant D** (out-of-catalog, independent commercial directory), sibling to `ccp_*` (Company Package, also Variant C/D out-of-catalog).

It governs commercial behavior of an AI company: pricing policy, billing rules, commercial package configuration, revenue-share / tenant-commercial settings.

## 2. Why It Is Gated (L2 #1 / #2)

- **L2 #1 商业模式变化**: any `cmcf_*` content defines *how the product makes money* — pricing model, packaging, monetization. This is a business-model decision, not an asset-fill decision.
- **L2 #2 收费规则变化**: billing rules, usage-based charging, package tiers, and cost recovery directly alter the charging logic.
- Per 运营协定 v2, both are **must-trigger 总控** events: route `安全边界席 → 飞书升级 → 等总控决策`. The 总控 has now pre-approved exploration, but the **安全边界席 boundary review remains mandatory** before any `cmcf_*` content or charging logic is authored.

## 3. Proposed Content Shape (design-only sketch, NOT to be filled without clearance)

```
cmcf_{pack}_{config_name}      # pack ∈ {ai_rd, ai_content, ai_commercial}
  ├─ version / status / source / description        # TemplateBase
  ├─ commercial_family: "pricing" | "billing" | "package" | "revenue"
  ├─ pricing_model: { type, currency, tiers[] }
  ├─ billing_rule: { cycle, metered_fields[], free_quota }
  ├─ package_refs: [ccp_*]                           # links to company packages
  └─ attribution: { owner_seat, approved_by, effective_date }
```

Minimal first candidates (design-only, for 总控 review only):
- `cmcf_ai_commercial_software_subscription` — SaaS subscription tier config
- `cmcf_ai_commercial_usage_metering` — token/run metered billing rule
- `cmcf_ai_content_creator_revenue_share` — creator revenue-share policy

## 4. Hard Constraints

- **NOT autonomously planned or instantiated.** Content must be approved by 总控 after 安全边界席 boundary review.
- Must not touch `payment/` / `invoice/` / real charging paths without an independent gate (per Git 基线纪律 红线).
- No real credential, no real money movement, no external billing provider integration at this stage.

## 5. Route

`安全边界席` (boundary + security review of commercial-scope exposure) → `飞书升级 (群 Curis 开发通知)` → `总控决策席` final decision.

## 6. Decision Asked of 总控

- (i) Keep `cmcf_*` **design-only + deferred** (current posture), or
- (ii) Authorize a bounded `cmcf_*` first-slice (e.g., pricing-policy metadata only, no charging logic) under a dedicated future gate + 安全边界席.

## 总控裁定 (2026-07-11)

- **裁定**：**支付和收费暂时不动** → 选 (i) **Keep `cmcf_*` design-only + deferred**（维持延后）。
- **含义**：`cmcf_*` 不解锁、不进入安全边界席实质评估、不填内容、不碰任何 payment / invoice / charging 路径。本提案仅作存档，留作 future gate。
- **与安全边界席关系**：因直接冻结，(b) 不触发安全边界席复核流程（区别于 (a) 实现层 gate 的 (i) 路线）。如需未来重启，须重新触发 L2 #1/#2 升级并由总控开放。

## Status

PROPOSAL + L2 ESCALATION (ARCHIVED). 总控 decision: DEFERRED (2026-07-11 "支付和收费暂时不动"). 安全边界席 review: NOT INITIATED (frozen). 内容填充: BLOCKED.
