# Curis Documentation Governance Phase 3-C2 Asset Review

Status: Review

Baseline:
main @ 19c4a3a6fcff7d67c794766a905325a59b3e7dbe

Updated:
2026-07-30

---

## 1. Review Conclusion

Phase 3-C2 completed classification analysis only. No asset was moved or deleted,
and no business code, configuration or product logic was modified.

| Scope | Count | Result |
| --- | ---: | --- |
| Phase 3-B2 Human Confirmation Required | 218 | Reconciled against the authoritative Asset Report |
| Delete Candidate excluded by instruction | 41 | Not reviewed or reclassified in this phase |
| Phase 3-C2 assets reviewed | 177 | Classified item by item below |
| Keep | 0 | No in-scope item met Keep more strongly than Archive or Protected |
| Archive | 160 | Historical or completed assets suitable for a later referenced package migration |
| Protected | 17 | WorkBuddy tool state or referenced ignored release state |

The apparent 218-versus-177 difference is intentional: the Phase 3-B2 manual
confirmation gate contains 41 Delete Candidates. The current instruction explicitly
excludes those records, so Keep + Archive + Protected equals 177, not 218.

## 2. Method And Decision Rules

Evidence used:

1. the 218 rows marked 需要人工确认 in the Phase 3-B2 Asset Report;
2. the Phase 3-B2 type, source, current-use and M/S/A/I reference evidence;
3. a current exact-path scan of Git-tracked and visible untracked text files at the
   declared baseline, excluding governance inventories and reports as consumers;
4. current filesystem existence checks for every reviewed path;
5. Frozen Current State and Design rules, which explicitly treat old UI sources as
   historical and not current design authority.

Recommendation precedence:

- Protected: external tool-state consumption, script/config consumption, ignored
  runtime/release state or another boundary that makes migration unsafe.
- Keep: current design authority, formal acceptance evidence or indispensable
  product-decision provenance that should remain at its current governed location.
- Archive: historical design, prototype, completed demo or superseded handoff that
  should be retained but can later move as a coherent package with references updated.

A detected reference does not automatically convert a historical asset into current
authority. For Archive rows, it means any future move must update all named, relative
and package-internal references in the same change.

## 3. Keep

Keep count: 0.

No reviewed item is a current Frozen design source or formal Release Evidence.
Completed demo assets retain historical value but are better classified Archive; the
formal Release Evidence that cites them remains protected outside this 177-row scope.

## 4. Archive

Archive count: 160.

| Path | Type | Source | Current Use | Still Referenced | Recommended Status |
| --- | --- | --- | --- | --- | --- |
| `diagrams/curis-architecture-diagrams.html` | HTML Prototype | Historical diagram/prototype | Historical interactive prototype | 是（M1 / S0 / A0 / I1；当前精确引用 1 个文件） | Archive |
| `diagrams/ui-databi.html` | HTML Prototype | Historical diagram/prototype | Historical interactive prototype | 是（M0 / S0 / A0 / I1；当前精确引用 1 个文件） | Archive |
| `diagrams/ui-department.html` | HTML Prototype | Historical diagram/prototype | Historical interactive prototype | 是（M0 / S0 / A0 / I1；当前精确引用 1 个文件） | Archive |
| `diagrams/ui-employee.html` | HTML Prototype | Historical diagram/prototype | Historical interactive prototype | 是（M0 / S0 / A0 / I1；当前精确引用 1 个文件） | Archive |
| `diagrams/ui-homepage-teal-v2.html` | HTML Prototype | Historical diagram/prototype | Historical interactive prototype | 是（M0 / S0 / A0 / I1；当前精确引用 1 个文件） | Archive |
| `diagrams/ui-homepage-variants.html` | HTML Prototype | Historical diagram/prototype | Historical interactive prototype | 是（M1 / S0 / A0 / I1；当前精确引用 2 个文件） | Archive |
| `diagrams/ui-login.html` | HTML Prototype | Historical diagram/prototype | Historical interactive prototype | 是（M0 / S0 / A0 / I1；当前精确引用 1 个文件） | Archive |
| `diagrams/ui-settings.html` | HTML Prototype | Historical diagram/prototype | Historical interactive prototype | 是（M0 / S0 / A0 / I1；当前精确引用 1 个文件） | Archive |
| `diagrams/ui-task-console.html` | HTML Prototype | Historical diagram/prototype | Historical interactive prototype | 是（M0 / S0 / A0 / I1；当前精确引用 1 个文件） | Archive |
| `docs/demo/phase3-demo-script.md` | Demo Document | Historical demo | Completed demo material | 是（M0 / S0 / A0 / I1；当前精确引用 1 个文件） | Archive |
| `docs/demo/phase4-ai-employee-demo-script.md` | Demo Document | Historical demo | Completed demo material | 是（M1 / S0 / A0 / I1；当前精确引用 2 个文件） | Archive |
| `docs/demo/phase5-g2-credential-vault-demo-script.md` | Demo Document | Historical demo | Completed demo material | 是（M1 / S0 / A0 / I1；当前精确引用 2 个文件） | Archive |
| `docs/demo/phase6-workflow-mvp-demo-script.md` | Demo Document | Historical demo | Completed demo material | 是（M1 / S0 / A0 / I2；当前精确引用 3 个文件） | Archive |
| `docs/demo/phase7-demo-seed.json` | JSON Demo/Support | Historical demo | Completed demo material | 是（M1 / S0 / A0 / I2；当前精确引用 3 个文件） | Archive |
| `docs/demo/phase7-stable-demo-script.md` | Demo Document | Historical demo | Completed demo material | 是（M1 / S0 / A0 / I1；当前精确引用 2 个文件） | Archive |
| `docs/pmo/20260719_quota_handoff_plan.md` | Handoff Document | Historical handoff/governance | Completed or superseded handoff | 是（M4 / S0 / A0 / I0；当前精确引用 4 个文件） | Archive |
| `docs/prototypes/curis-full-system-high-fidelity-prototype.html` | HTML Prototype | Static prototype | Historical interactive prototype | 是（M2 / S0 / A0 / I0；当前精确引用 2 个文件） | Archive |
| `frontend/design-spec/ceo-office/_samples/analytics-sample.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M1 / S0 / A0 / I0；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/_samples/brainstorm-sample.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M1 / S0 / A0 / I0；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/_samples/capability-center-sample.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M1 / S0 / A0 / I0；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/_samples/ceo-home-sample.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M1 / S0 / A0 / I0；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/_samples/department-detail-sample.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M1 / S0 / A0 / I0；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/_samples/execution-sample.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M1 / S0 / A0 / I0；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/_samples/knowledge-sample.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M1 / S0 / A0 / I0；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/_samples/org-center-sample.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M1 / S0 / A0 / I0；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/_samples/project-center-sample.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M1 / S0 / A0 / I0；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/_samples/project-detail-sample.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M1 / S0 / A0 / I0；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/_samples/report-detail-sample.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M1 / S0 / A0 / I0；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/_samples/skill-detail-sample.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M1 / S0 / A0 / I0；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/_samples/task-detail-sample.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M1 / S0 / A0 / I0；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/analytics-org.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M3 / S0 / A0 / I3；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/analytics-project.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M3 / S0 / A0 / I3；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/analytics-workflow.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M3 / S0 / A0 / I3；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/analytics.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M3 / S0 / A0 / I3；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/brainstorm-active.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M3 / S0 / A0 / I4；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/brainstorm-result-detail.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M1 / S0 / A0 / I0；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/brainstorm-results.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M3 / S0 / A0 / I4；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/brainstorm-session-detail.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M3 / S0 / A0 / I0；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/brainstorm.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M2 / S0 / A0 / I2；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/capability-agent-list.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M2 / S0 / A0 / I6；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/capability-center.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M4 / S0 / A0 / I5；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/capability-model-list.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M2 / S0 / A0 / I6；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/capability-skill-list.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M2 / S0 / A0 / I6；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/capability-tool-list.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M2 / S0 / A0 / I6；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/capability-workflow-list.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M2 / S0 / A0 / I6；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/ceo-home.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M3 / S0 / A0 / I4；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/company-runtime.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M2 / S0 / A0 / I1；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/decision-center.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M2 / S0 / A0 / I5；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/department-detail.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M2 / S0 / A0 / I0；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/employee-detail.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M3 / S0 / A0 / I0；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/execution-runs.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M3 / S0 / A0 / I4；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/execution-tasks.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M3 / S0 / A0 / I4；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/execution.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M3 / S0 / A0 / I3；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/handoff/capability-center/capability-center.hifi.html` | HTML Prototype | CEO Office historical design | Completed or superseded handoff | 是（M0 / S0 / A0 / I1；当前精确引用 1 个文件） | Archive |
| `frontend/design-spec/ceo-office/knowledge-company.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M3 / S0 / A0 / I4；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/knowledge-dept.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M3 / S0 / A0 / I4；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/knowledge-entry-detail.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M3 / S0 / A0 / I0；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/knowledge-project.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M3 / S0 / A0 / I4；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/knowledge.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M2 / S0 / A0 / I3；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/org-center.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M4 / S0 / A0 / I3；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/org-dept.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M5 / S0 / A0 / I4；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/org-employees.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M4 / S0 / A0 / I4；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/project-center.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M3 / S0 / A0 / I2；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/project-dept.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M4 / S0 / A0 / I2；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/project-detail.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M2 / S0 / A0 / I0；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/report-detail.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M2 / S0 / A0 / I0；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/reports.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M2 / S0 / A0 / I5；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/run-detail.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M3 / S0 / A0 / I0；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/settings-brand.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M3 / S0 / A0 / I3；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/settings-notify.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M3 / S0 / A0 / I3；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/settings-profile.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M3 / S0 / A0 / I3；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/settings.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M2 / S0 / A0 / I3；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/skill-detail.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M3 / S0 / A0 / I1；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/strategy-room.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M2 / S0 / A0 / I5；相对或包内引用） | Archive |
| `frontend/design-spec/ceo-office/task-detail.html` | HTML Prototype | CEO Office historical design | Historical interactive prototype | 是（M2 / S0 / A0 / I0；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/assets/create-flow.css` | Prototype CSS | Deprecated UI V2 | Historical package support | 是（M0 / S0 / A0 / I2；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/assets/create-flow.js` | Prototype Script | Deprecated UI V2 | Historical package support | 是（M0 / S0 / A0 / I2；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/assets/navigation-ia.css` | Prototype CSS | Deprecated UI V2 | Historical package support | 是（M0 / S0 / A0 / I48；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/assets/navigation-ia.js` | Prototype Script | Deprecated UI V2 | Historical package support | 是（M0 / S0 / A0 / I47；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/assets/project-dept-ia.js` | Prototype Script | Deprecated UI V2 | Historical package support | 是（M0 / S0 / A0 / I1；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/assets/project-detail-prototype.css` | Prototype CSS | Deprecated UI V2 | Historical package support | 是（M0 / S0 / A0 / I2；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/assets/project-detail-prototype.js` | Prototype Script | Deprecated UI V2 | Historical package support | 是（M0 / S0 / A0 / I2；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/audit-evidence/01-ceo-home-1440-viewport.png` | PNG Design Export | Deprecated UI V2 | Historical visual reference | 是（M1 / S0 / A0 / I0；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/audit-evidence/2026-07-27-capability-center-1440.png` | PNG Design Export | Deprecated UI V2 | Historical visual reference | 是（M1 / S0 / A0 / I0；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/audit-evidence/2026-07-27-org-center-1440.png` | PNG Design Export | Deprecated UI V2 | Historical visual reference | 是（M1 / S0 / A0 / I0；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/audit-evidence/2026-07-27-project-center-1440.png` | PNG Design Export | Deprecated UI V2 | Historical visual reference | 是（M1 / S0 / A0 / I0；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/audit-evidence/analytics-1440.png` | PNG Design Export | Deprecated UI V2 | Historical visual reference | 是（M1 / S0 / A0 / I0；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/audit-evidence/analytics-390.png` | PNG Design Export | Deprecated UI V2 | Historical visual reference | 是（M1 / S0 / A0 / I0；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/audit-evidence/capability-center-1440.png` | PNG Design Export | Deprecated UI V2 | Historical visual reference | 是（M1 / S0 / A0 / I0；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/audit-evidence/capability-center-390.png` | PNG Design Export | Deprecated UI V2 | Historical visual reference | 是（M1 / S0 / A0 / I0；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/audit-evidence/ceo-home-390.png` | PNG Design Export | Deprecated UI V2 | Historical visual reference | 是（M1 / S0 / A0 / I0；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/audit-evidence/org-center-1440.png` | PNG Design Export | Deprecated UI V2 | Historical visual reference | 是（M1 / S0 / A0 / I0；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/audit-evidence/org-center-390.png` | PNG Design Export | Deprecated UI V2 | Historical visual reference | 是（M1 / S0 / A0 / I0；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/audit-evidence/project-center-1440.png` | PNG Design Export | Deprecated UI V2 | Historical visual reference | 是（M1 / S0 / A0 / I0；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/audit-evidence/project-center-390.png` | PNG Design Export | Deprecated UI V2 | Historical visual reference | 是（M1 / S0 / A0 / I0；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/colors_and_type.css` | Prototype CSS | Deprecated UI V2 | Historical package support | 是（M0 / S0 / A0 / I6；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/curis-ceo-office.design` | Design Source | Deprecated UI V2 | Historical package support | 是（M1 / S0 / A0 / I1；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/docs/ui/curis-ui-state-catalog.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M1 / S0 / A0 / I2；当前精确引用 1 个文件） | Archive |
| `frontend/design-spec/curis-ui-v2/docs/ui/curis-ui-v2-data-map.json` | JSON Demo/Support | Deprecated UI V2 | Historical package support | 是（M1 / S0 / A0 / I4；当前精确引用 1 个文件） | Archive |
| `frontend/design-spec/curis-ui-v2/docs/ui/curis-ui-v2-handoff.md` | Handoff Document | Deprecated UI V2 | Completed or superseded handoff | 是（M1 / S0 / A0 / I2；当前精确引用 1 个文件） | Archive |
| `frontend/design-spec/curis-ui-v2/docs/ui/curis-ui-v2-secondary-page-contracts.json` | JSON Demo/Support | Deprecated UI V2 | Historical package support | 是（M1 / S0 / A0 / I3；当前精确引用 1 个文件） | Archive |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/ceo-home.png` | PNG Design Export | Deprecated UI V2 | Historical visual reference | 是（M0 / S0 / A0 / I1；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/ceo-home.png` | PNG Design Export | Deprecated UI V2 | Historical visual reference | 是（M0 / S0 / A0 / I1；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/ceo-home.png` | PNG Design Export | Deprecated UI V2 | Historical visual reference | 是（M0 / S0 / A0 / I1；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/manifest.json` | Export Manifest/Support | Deprecated UI V2 | Historical package support | 是（M0 / S0 / A0 / I1；当前精确引用 1 个文件） | Archive |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/curis-ui-v2.all-pages.json` | JSON Demo/Support | Deprecated UI V2 | Historical package support | 是（M2 / S0 / A0 / I4；当前精确引用 1 个文件） | Archive |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/curis-ui-v2.frames.json` | JSON Demo/Support | Deprecated UI V2 | Historical package support | 是（M1 / S0 / A0 / I2；当前精确引用 1 个文件） | Archive |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/curis-ui-v2.interactions.json` | JSON Demo/Support | Deprecated UI V2 | Historical package support | 是（M2 / S0 / A0 / I2；当前精确引用 1 个文件） | Archive |
| `frontend/design-spec/curis-ui-v2/docs/ui/figma/curis-ui-v2.tokens.json` | JSON Demo/Support | Deprecated UI V2 | Historical package support | 是（M2 / S0 / A0 / I2；当前精确引用 1 个文件） | Archive |
| `frontend/design-spec/curis-ui-v2/docs/ui/index.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M1 / S0 / A0 / I0；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/analytics-org.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M0 / S0 / A0 / I42；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/analytics-project.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M0 / S0 / A0 / I42；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/analytics-workflow.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M0 / S0 / A0 / I42；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/analytics.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M1 / S0 / A0 / I42；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/brainstorm-active.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M0 / S0 / A0 / I42；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/brainstorm-results.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M0 / S0 / A0 / I42；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/brainstorm-session-detail.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M0 / S0 / A0 / I1；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/brainstorm.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M0 / S0 / A0 / I42；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/capability-agent-list.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M0 / S0 / A0 / I2；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/capability-center.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M1 / S0 / A0 / I45；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/capability-model-list.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M0 / S0 / A0 / I2；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/capability-skill-list.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M0 / S0 / A0 / I42；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/capability-tool-list.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M0 / S0 / A0 / I42；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/capability-workflow-list.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M0 / S0 / A0 / I42；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/ceo-home.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M1 / S0 / A0 / I46；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/company-runtime.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M1 / S0 / A0 / I2；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/decision-center.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M0 / S0 / A0 / I42；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/department-create.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M0 / S0 / A0 / I1；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/department-detail.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M0 / S0 / A0 / I2；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/employee-create.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M0 / S0 / A0 / I1；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/employee-detail.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M1 / S0 / A0 / I1；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/execution-runs.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M0 / S0 / A0 / I42；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/execution-tasks.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M0 / S0 / A0 / I42；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/execution.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M1 / S0 / A0 / I44；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/knowledge-company.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M0 / S0 / A0 / I42；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/knowledge-dept.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M0 / S0 / A0 / I42；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/knowledge-entry-detail.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M0 / S0 / A0 / I1；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/knowledge-project.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M0 / S0 / A0 / I42；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/knowledge.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M0 / S0 / A0 / I44；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/org-center.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M1 / S0 / A0 / I46；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/org-dept.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M0 / S0 / A0 / I1；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/org-employees.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M0 / S0 / A0 / I4；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/project-center.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M1 / S0 / A0 / I44；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/project-dept.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M0 / S0 / A0 / I1；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/project-detail.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M0 / S0 / A0 / I3；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/project-miniapp-detail.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M0 / S0 / A0 / I2；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/project-xhs-workflow-detail.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M0 / S0 / A0 / I2；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/report-detail.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M0 / S0 / A0 / I1；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/reports.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M0 / S0 / A0 / I42；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/run-detail.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M0 / S0 / A0 / I1；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/settings-brand.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M0 / S0 / A0 / I42；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/settings-notify.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M0 / S0 / A0 / I42；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/settings-profile.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M0 / S0 / A0 / I42；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/settings.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M1 / S0 / A0 / I42；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/skill-detail.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M0 / S0 / A0 / I1；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/strategy-room.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M0 / S0 / A0 / I42；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/pages/task-detail.html` | HTML Prototype | Deprecated UI V2 | Historical interactive prototype | 是（M0 / S0 / A0 / I1；相对或包内引用） | Archive |
| `frontend/design-spec/curis-ui-v2/runtime-orchestration-summary.json` | JSON Demo/Support | Deprecated UI V2 | Historical package support | 是（M0 / S0 / A0 / I1；相对或包内引用） | Archive |
| `PROJECT_HANDOFF.md` | Handoff Document | Historical handoff/governance | Completed or superseded handoff | 是（M9 / S0 / A0 / I1；当前精确引用 10 个文件） | Archive |
| `shared/prototypes/curis-full-system-high-fidelity-prototype.html` | HTML Prototype | Static prototype | Historical interactive prototype | 是（M1 / S0 / A0 / I1；当前精确引用 2 个文件） | Archive |

## 5. Protected

Protected count: 17.

| Path | Type | Source | Current Use | Still Referenced | Recommended Status |
| --- | --- | --- | --- | --- | --- |
| `.workbuddy/automations/automation-1783450520356/memory.md` | WorkBuddy Memory | WorkBuddy tool memory | Historical Agent/tool context | 否（未检测到静态仓库引用；外部工具消费未知） | Protected |
| `.workbuddy/automations/automation-1784564820520/memory.md` | WorkBuddy Memory | WorkBuddy tool memory | Historical Agent/tool context | 否（未检测到静态仓库引用；外部工具消费未知） | Protected |
| `.workbuddy/memory/2026-07-07.md` | WorkBuddy Memory | WorkBuddy tool memory | Historical Agent/tool context | 否（未检测到静态仓库引用；外部工具消费未知） | Protected |
| `.workbuddy/memory/2026-07-08.md` | WorkBuddy Memory | WorkBuddy tool memory | Historical Agent/tool context | 是（M1 / S0 / A0 / I1；当前精确引用 2 个文件） | Protected |
| `.workbuddy/memory/2026-07-09.md` | WorkBuddy Memory | WorkBuddy tool memory | Historical Agent/tool context | 否（未检测到静态仓库引用；外部工具消费未知） | Protected |
| `.workbuddy/memory/2026-07-10.md` | WorkBuddy Memory | WorkBuddy tool memory | Historical Agent/tool context | 否（未检测到静态仓库引用；外部工具消费未知） | Protected |
| `.workbuddy/memory/2026-07-11.md` | WorkBuddy Memory | WorkBuddy tool memory | Historical Agent/tool context | 否（未检测到静态仓库引用；外部工具消费未知） | Protected |
| `.workbuddy/memory/2026-07-12.md` | WorkBuddy Memory | WorkBuddy tool memory | Historical Agent/tool context | 是（M1 / S0 / A0 / I1；当前精确引用 2 个文件） | Protected |
| `.workbuddy/memory/2026-07-13.md` | WorkBuddy Memory | WorkBuddy tool memory | Historical Agent/tool context | 是（M1 / S0 / A0 / I0；当前精确引用 1 个文件） | Protected |
| `.workbuddy/memory/2026-07-17.md` | WorkBuddy Memory | WorkBuddy tool memory | Historical Agent/tool context | 是（M1 / S0 / A0 / I1；当前精确引用 2 个文件） | Protected |
| `.workbuddy/memory/2026-07-18.md` | WorkBuddy Memory | WorkBuddy tool memory | Historical Agent/tool context | 否（未检测到静态仓库引用；外部工具消费未知） | Protected |
| `.workbuddy/memory/2026-07-19.md` | WorkBuddy Memory | WorkBuddy tool memory | Historical Agent/tool context | 否（未检测到静态仓库引用；外部工具消费未知） | Protected |
| `.workbuddy/memory/2026-07-20.md` | WorkBuddy Memory | WorkBuddy tool memory | Historical Agent/tool context | 否（未检测到静态仓库引用；外部工具消费未知） | Protected |
| `.workbuddy/memory/2026-07-21.md` | WorkBuddy Memory | WorkBuddy tool memory | Historical Agent/tool context | 否（未检测到静态仓库引用；外部工具消费未知） | Protected |
| `.workbuddy/memory/2026-07-22.md` | WorkBuddy Memory | WorkBuddy tool memory | Historical Agent/tool context | 否（未检测到静态仓库引用；外部工具消费未知） | Protected |
| `.workbuddy/memory/MEMORY.md` | WorkBuddy Memory | WorkBuddy tool memory | Historical Agent/tool context | 是（M5 / S0 / A0 / I4；当前精确引用 6 个文件） | Protected |
| `deploy/curis/releases/` | Ignored Directory | Ignored workspace state | Historical local release bundle | 是（M0/S2/A0；当前精确引用 2 个文件） | Protected |

## 6. Focused Review

### 6.1 WorkBuddy Memory

- Reviewed: 16 tracked memory records.
- Recommendation: Protected for all 16.
- Historical value: they contain tool/Agent context and decision breadcrumbs that may
  help provenance review.
- Movement decision: do not move them through Documentation Governance while WorkBuddy
  may resolve memory by its original path. Zero repository-text references do not prove
  that an external tool has no path-level dependency.
- Archive condition: only after the WorkBuddy owner confirms the tool is retired or
  provides an export/import path, with a verified replacement index.

### 6.2 Release Evidence

- The 29 formal Release Evidence files in Phase 3-B2 are Forbidden Move records, not
  part of the 218 Human Confirmation Required cohort. They remain protected and were
  not reclassified here.
- The six in-scope demo assets support completed demonstrations but are not themselves
  the formal acceptance authority. They are classified Archive; their Release Evidence
  links must be updated atomically if a future move is approved.
- The ignored `deploy/curis/releases/` bundle is Protected because it is
  outside Git tracking and has two script/config reference signals.

### 6.3 Design Assets

- Reviewed design/prototype cohort: 152 assets from Deprecated UI V2, CEO Office
  historical design, historical diagrams and static prototypes.
- Recommendation: Archive for all 152.
- Current authority: none of these files is a current Frozen design input. The Frozen
  Design System explicitly lists the old UI sources as Deprecated exclusion-only
  material.
- Future value: retain them as historical comparison, rejected-direction evidence and
  possible inspiration, but never use them to override the current Terra design rules.
- Movement condition: move by coherent package, not individual child files, because
  HTML, CSS, JavaScript, JSON and image assets contain dense relative references.

## 7. Risks

- The Phase 3-B2 label Human Confirmation Required includes 41 Delete Candidates;
  treating all 218 as archive candidates would violate the current instruction.
- Static repository search cannot prove whether WorkBuddy consumes memory paths outside
  Git-visible files.
- The UI V2 and CEO Office historical packages have internal and Markdown references;
  partial movement can break navigation, assets or historical evidence.
- The ignored local release bundle is not protected by Git history and has script/config
  references. It needs a release-owner decision and a recoverable manifest before any
  future handling.
- Formal Release Evidence must remain searchable even if its supporting demo paths later
  change.
- Dynamic paths assembled at runtime cannot be fully proven by static scanning.

## 8. Recommended Next Actions

1. Approve or reject the 160-row Archive recommendation without moving files in this
   review commit.
2. If approved, migrate one coherent package per later phase in this order:
   Deprecated UI V2, CEO Office historical design, diagrams/static prototypes,
   completed demos, then superseded handoffs.
3. For every migration batch, rerun exact, relative, Markdown, script/config and Agent
   reference checks and update all referrers atomically.
4. Keep all 16 WorkBuddy Memory records Protected until the WorkBuddy owner confirms
   path-independent retention or a verified export.
5. Keep `deploy/curis/releases/` Protected until release scripts, bundle
   contents and recovery requirements are reviewed.
6. Handle the 41 Delete Candidates only in a separately authorized deletion review.

## 9. Boundary Confirmation

- Files moved: 0
- Files deleted: 0
- Code modified: 0
- Configuration modified: 0
- Reviewed asset paths present: 177 / 177
- Delete Candidates processed: 0 / 41

Phase 3-C2 stops at analysis and classification.
