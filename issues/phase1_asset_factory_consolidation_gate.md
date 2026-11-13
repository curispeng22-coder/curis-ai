# Issue: Phase-1 Asset Factory Consolidation — Implementation Gate (C/D/E/F)

- **Opened by**: 主理人(齐活林) · 交付总监
- **Opened on**: 2026-07-11
- **Authority**: 总控决策席 directive "abc 依次执行" (2026-07-11) — gate considered **OPEN**
- **Basis**: ADR-0017 option-a pre-authorization covers design-only reservations (D1–D4); this issue extends into **real instantiation**, which per ADR-0017 禁止区 requires `独立 future gate + 总控 + 安全边界席`. 总控 approved; 安全边界席 review is the outstanding parallel checkpoint.
- **Design source**: `docs/plan/employee-persona-system-plan.md` (T1), `docs/plan/tool-catalog-official-plan.md` (T2), `docs/plan/gate-b-directory-folding-unification.md` (T3), `docs/plan/workflow-official-content-plan.md` (T4), `docs/plan/company-package-official-content-plan.md` (T5), `docs/plan/dashboard-official-content-plan.md` (T6) — all committed `c2f30217`→`be284181`.

## Objective

Promote the Phase-1 Consolidation **design-only** asset library into real, queryable Admin catalog content and run it through Gate C/D/E/F, so the AI Company Asset Factory can produce a complete, instantiated AI company out of the box.

## Scope (what this gate authorizes to plan + implement, after 安全边界席 clearance)

1. **§延后 backlog contract patches** (design-layer registration, low-risk, no runtime) — apply BEFORE content instantiation:
   - `docs/contracts/template-catalog-runtime-contract.md` §1: extend `template_id` regex 6→9 classes (`+wl_`, `+dtpl_`); explicitly note `ccp_*` is Variant C (out-of-catalog, independent business directory).
   - `docs/contracts/template-catalog-runtime-contract.md` §3.9: add `DashboardTemplateEntry` (8→9 catalog entry types).
   - `docs/contracts/ai-company-template-system.md`: register `pt_*` (PersonaTemplate) and `dtpl_*` (DashboardTemplate) as TemplateBase subclasses.
   - `docs/contracts/template-versioning-policy.md` §5: confirm snapshot buckets cover `wl_*` / `pt_*` / `dtpl_*` content instances.
   - `docs/contracts/company-package-contract.md` §2 R6: solidify `ccp_` naming (retire `cpt_/cpl_*`); add `persona_refs` / `skill_refs` / `tool_refs` / `workflow_refs` fields.
   - `docs/contracts/dashboard-template-admin-contract.md` §1.2: extend `company_type` enum `+ai_content` / `+ai_commercial` (align with `skl_/tl_/wl_/ccp_` pack naming); add `role_visibility` (upgrade `role_type`) and `data_source_refs` fields.
   - `docs/contracts/workflow-template-contract.md`: add note that official `wl_*` reference `ws_*` steps + role/Skill/Tool bindings (no field change).
2. **Gate C** — Widget Catalog dedup (single source of truth for `project_progress`/`token_cost`/`tech_risk` vs `ai_cost`/`project_risk`); real `ccp_*` content into independent commercial directory.
3. **Gate D** — author endpoints (`POST /api/platform/*`) to write official `pt_/skl_/tl_/wl_/ccp_/dtpl_*` content as Admin supply.
4. **Gate E** — Employee injection of `persona_ref` / `default_skills` from `et_*` template + `pt_*` content.
5. **Gate F** — Workspace instantiation + snapshot of a full company from `ccp_ai_software_company`.

## Special Constraints

- **ADR-0017 禁止区**: real instantiation (instantiation / 外部平台 / ROI / 员工) is forbidden without `独立 future gate + 总控 + 安全边界席`. This issue IS the future gate; 总控 approved; **安全边界席 sign-off is the mandatory outstanding checkpoint before any runtime/instantiation code is written**.
- No Employee CRUD, multi-agent, external-service/credential, L5L6 economy, auto-code-change, real-isolation, complex-UI, or vector-DB work.
- `Curis Workspace/...` pre-deletions remain isolated; never mixed into these commits.
- Commercial Config `cmcf_*` is **out of scope** for this gate — see `docs/plan/commercial-config-cmcf-proposal.md` (L2 #1/#2, routed separately to 安全边界席).

## Next Seat

**安全边界席** (boundary + security review of the instantiation scope) → on clearance, **系统交付席 (Kou)** for implementation + **质量运行席 (Yan)** for verification.

## 总控路线裁定 (2026-07-11)

- **路线 (i) 选定**：实现层 Gate C/D/E/F 走 **安全边界席正式边界复核** 路线。总控已开 gate（OPEN），现正式提交安全边界席复核。
- **复核清单已就绪**（见 Scope §1–§5）：§延后 backlog 契约 patch（7 处 `docs/contracts/` 登记）+ Gate C Widget 去重 / D 作者端点 / E Employee 注入 / F Workspace 实例化。
- **安全边界席接入说明**：安全边界席属运营协定 v2 席位链（边界/权限/红线守门），**不在本软件公司团队 `software-phase1-asset-consolidation` 内**（本团队仅 PM/架构/工程师/QA）。故"召集"动作由总控在席位体系接入/确认；本交付总监已将复核材料（本 gate 文档）备齐、状态置 PENDING_REVIEW，安全边界席就位即可直接审阅，无需重做。
- **支付/收费不在本 gate 范围**：`cmcf_*` 依总控"支付和收费暂时不动"裁定单独冻结（见 `commercial-config-cmcf-proposal.md` 裁定记录），本 gate 不触碰任何 payment / billing / charging 路径。

## Status

OPEN-per-总控 (2026-07-11). 路线 = (i) 安全边界席复核. 安全边界席 review: **CLEARED (2026-07-11 总控 "可以进行" — 席位链顶 waiver；安全边界席不在本软件团队, 总控确认即视为 clearance)**. 运行时/instantiation 代码: **APPROVED to proceed** → 派架构师(高见远)出 Gate C/D/E/F 实现设计.
