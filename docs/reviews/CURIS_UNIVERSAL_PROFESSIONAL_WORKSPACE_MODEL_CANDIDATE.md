# CURIS UNIVERSAL PROFESSIONAL WORKSPACE MODEL
## CANDIDATE ARCHITECTURE

**Authority Class:** REVIEW  
**Status:** Review  
**Disposition:** CANDIDATE / READY FOR CEO REVIEW  
**Date:** 2026-08-21  
**Implementation:** Not authorized  
**External validation:** `PENDING EXTERNAL SYNTHESIS`

> 本文只表达 Candidate Architecture。它不修改 Current Product Truth，不新增 Runtime、Schema、DB、Frontend、Route 或 Prototype。

## 1. Model

```text
Company Shell
└── canonical Workspace
    ├── Workspace Current Operating (one shared projection)
    ├── package-declared Domain Navigation
    │   ├── Professional Surface A
    │   │   ├── Object Views
    │   │   └── on-demand Detail / Work / Utility
    │   ├── Professional Surface B
    │   └── Scoped Team / Knowledge / Result / Evidence Views
    ├── Shared Work Area / Employee Workstations
    └── Capability / Team Operating / Operating Lifecycle Runtime Truth
```

## 2. Definitions

### Workspace

一个 canonical、持久、受 Business 管辖的独立经营范围：拥有 Workspace Goal / Strategy scope、Leader、Operating Team、Operating Series、权限与数据边界、Package version 和 lifecycle。

`Workspace ≠ Page`。切换页面、Surface、Object View、Detail 或 Utility 不产生新 Workspace。

### Professional Surface

同一 Workspace 内围绕一个稳定专业问题组织对象、动作、工具和结果的主要工作面。它有 Package-local stable key 和 route，但没有独立 Workspace identity、Team 或 Operating Series。

### Object View

同一 Surface 对业务对象的列表、日历、看板、图表、队列或筛选投影。

### Detail / Work View

围绕一个 selected object 的检查、编辑、预览、证据或专业工具视图；按需进入 Utility、Drawer、Focus 或 Main split。

### Scoped View

Team、Knowledge、Artifact、Result、Evidence 等共享 Truth 按当前 Workspace / Surface scope 的 projection；不得重建 Domain-specific shared system。

## 3. Ownership

| Layer | Owns | Must not own |
|---|---|---|
| Core | canonical identity、Shell、route validation、finite renderer、permissions、shared Runtime truth、failure states | XHS/RD/e-commerce 菜单和业务语义 |
| Workspace Package | Domain Navigation、Surface Registry、Domain schemas、object/detail mappings、capability requirements、availability rules | credentials、instance data、parallel Runtime、pre-authorized grants |
| Workspace Instance | pinned package/version、enabled optional Surfaces、canonical scope、instance-owned domain data | arbitrary new Surface definition or Core menu |
| View / User preference | selected Surface、last active、pane state、width、sort/filter | Goal、Strategy、Result、Evidence、Assignment truth |

## 4. Pane responsibilities

| Responsibility | Candidate use |
|---|---|
| Global Navigation | Company-level location and Workspace entry |
| Context | Workspace-local Domain Navigation + current Surface context |
| Main | selected Professional Surface + Shared Work Area |
| Utility | selected Object Detail / editor / preview / evidence |
| CEO Assistant | one global Company employee with current scoped context; not a fifth Pane |

Pane responsibility does not equal visible column count. Main must remain usable when Context and Utility are closed.

## 5. Navigation contract

Domain Navigation is:

- produced by Workspace Engineering + Domain Expert + Product Expert;
- declared and versioned by Workspace Package;
- validated, resolved and rendered by Core;
- stable in position even when availability changes;
- never hardcoded in Core for XHS, RD or e-commerce.

Candidate entry priority:

```text
explicit deep link
→ valid last active Surface
→ Package default
→ Package fallback
→ honest blocked state
```

Runtime may recommend or mark attention. It must not auto-jump an active user between Surfaces.

## 6. Operating truth

One Workspace owns one Current Operating projection:

```text
经营状态 / 本轮重点 / 最新判断 / 下一步
```

All Surfaces consume it. Goal、Strategy、Cycle、Work、Result、Evidence、Review、Learning 和 Next-cycle Decision remain in existing shared truth. No Surface stores a duplicate operating state and no Autonomous UI Runtime is created.

## 7. Object rule

Use the highest existing owner that holds:

1. existing Core object;
2. external Provider object + Curis reference/provenance;
3. Domain Package object only when domain persistence/lifecycle is real;
4. Artifact / Evidence / Result for outputs and proof;
5. projection for recomputable views;
6. UI-only state for selection and layout.

UI need alone never justifies a new persisted entity.

## 8. Package implication

Current Package semantics are sufficient for one Workspace navigation entry and one Main/Context/Utility composition. Multi-surface needs a minimal extension of that same contract:

```text
Surface Registry
├── stable surfaceKey / routeSegment / label / order
├── default / fallback
├── role and objectViews
├── detailMappings
├── required / optional / conditional availability
├── capability requirements
└── scoped shared projections
```

No Sub-Workspace, second renderer, new workflow engine, microservice split or Package dependency solver is proposed.

## 9. Domain checks

| Domain | Candidate mapping | Result |
|---|---|---|
| XHS | Research / Content-Publishing / Growth / Commercial candidates + Calendar/Object/Detail + scoped Team/Knowledge | Architecture fits; exact set `PENDING EXTERNAL SYNTHESIS` |
| RD | Issue-Development / Build-Test / Release / Architecture + Diff/Source/Preview details | Fits without XHS semantics |
| E-commerce | Market / Product / Inventory / Order / Marketing / Service / Finance / Supply Chain grouped as Surfaces and object views | Stress test passes; no e-commerce product design claimed |
| Unknown Domain | Intent → Research → Semantic Model → IA/Navigation/Surfaces → Team → Package → Validation | Fits without user-authored navigation/workflow |

## 10. Identity boundary

Create a sibling Workspace under the same Business only when the scope requires an independent Goal, Leader/Team, Operating Series, permissions/data boundary and lifecycle. Otherwise use a Surface, Object View, Detail or filter.

Candidate route:

```text
/ceo-office/workspace/{workspaceId}/{surfaceKey}
```

`workspaceId` remains canonical. `surfaceKey` is Package-local and versioned; it never becomes a second Workspace identity.

## 11. Decision required

CEO acceptance is required for:

1. Workspace as a canonical Professional Operating Environment;
2. multiple Professional Surfaces inside one Workspace;
3. Package-declared Domain Navigation and Surface Registry;
4. Context = Domain Navigation/context, Main = selected Surface, Utility = on-demand detail;
5. deterministic default + last active + no runtime auto-jump;
6. Universal model first, XHS exact Surface set only after external synthesis.

```text
CANDIDATE ONLY
NO AUTHORITY CHANGE
NO IMPLEMENTATION
STOP FOR CEO REVIEW
```
