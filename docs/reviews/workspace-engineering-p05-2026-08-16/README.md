# Workspace Engineering P0.5 Desktop Company Integration Evidence

Status: Formal Acceptance Evidence

Date: 2026-08-16

Issue: `WORKSPACE-ENGINEERING-P05-COMPANY-INTEGRATION-001`

## Build-before-Package boundary

| Artifact | mtime epoch | SHA-256 |
| --- | ---: | --- |
| `Curis.app/Contents/MacOS/curis-desktop` | `1786876489` | `1e73656fd32f3978b8a3b4b929d1ce1d25ffb694bb2a6a6ae766359328d74abf` |
| packaged `runtime/workspace/curis-workspace` | `1786876423` | `e1ca53dfcdc2de062b1e04ef8640e0b8775cb8f14c0f0263968baa273192456f` |
| external `manifest.json` | `1786876541` | `719a26991dc806bb21a803a23cdf8cf5b4624d22f047a84865937253425158e9` |
| external domain schema | `1786876541` | `f0e24085839cc4356df637bafb80f750e37c02b34b88ad338d386d0a1a53043d` |
| external surfaces | `1786876541` | `328d40d7f890aed3ca6e170bad3a005148c8c34f5abd6a00075b67ed2a626cbc` |

The external Package files were created after the app and packaged Workspace Runtime. A recursive
binary/text scan of `Curis.app` returned `0` matches for
`com.curis.sample.customer-feedback-office`, `CustomerFeedback` and `客户反馈办公室`.

Installed provenance:

- package: `com.curis.sample.customer-feedback-office@0.1.0`
- digest: `5fcc5af0c4a8010d13d64524682cc7544c0636e854b2e7e4f8a1d57138dfcd67`
- instance: `workspace-package-instance-e40cdd30-13d3-4e77-a603-046763aa3dc5`
- workspace: `workspace-package-f9ff0d18-34ed-4167-89ee-41a3dda7e94b`
- company: `company-p05-desktop`

## Real operating chain

The packaged Desktop API returned `COMPLETED`, `resolvable=true`, `reverseResolved=true` and
`TRIAGED` for:

```text
package-object-20086bd0-cc1b-4a95-bc81-5ec6eefa1453
→ role-slot-p05-feedback-triage
→ ai-employee-p05-feedback-triage
→ capability-binding-p05-feedback-triage
→ core.customer-feedback-triage
→ Task 4d76d4c7-dbf3-434c-87bc-e5f11282a491
→ Execution 1
→ artifact-3890f080-128a-403b-86b1-d5de59192d09
→ evidence-d8999ac6-0060-4bed-99a3-69629ac3e781
→ outcome-938bd8a4-a01e-4f5c-a1cb-28687dd3fada
→ CustomerFeedback TRIAGED
```

SQLite shows all Runtime entities in `selfuse / company-p05-desktop /
workspace-package-f9ff0d18-34ed-4167-89ee-41a3dda7e94b`; Package projection and Core identity share
the object ID. Core links are `HAS_CURRENT_RESPONSIBILITY`, `HAS_CURRENT_EXECUTOR`,
`USES_CAPABILITY`, `HAS_EVIDENCE` and `HAS_RESULT`.

## Failure proof

Forged Package relationship input returned `422`. A second real operation returned:

```text
object: package-object-b4331078-9211-4789-9f68-69ed7b82442d
state: NEW
task: e81ac8b5-328a-4dc0-8fbf-b4017d8d1610 / FAILED
execution: 2
error: customer_feedback_summary_insufficient
evidenceRefs/resultRefs/artifactRefs: []
```

## Full Desktop restart

The Desktop process and sidecars were stopped; the backend health port rejected connections. The
same app binary was relaunched with all three DB variables pointing to the isolated DB. Both
terminal records then resolved with the same IDs and states. The success record remained
`TRIAGED`; the failure record remained `NEW` without false result truth.

Isolated DB after restart/stop:

- path: `/tmp/curis-workspace-p05-desktop-home-20260816/Library/Application Support/com.curis.desktop/data/curis.sqlite`
- size: `1228800`
- SHA-256: `87cd2c0bb9bea7ce9a118cb615b41130b21a1a6b409f9b3bb27b4cbecb940322`
- `integrity_check=ok`; `foreign_key_check` returned no rows
- Runtime children of the two proof objects contain only `EVIDENCE` and `OUTCOME`; no Handoff,
  Decision or P7 entity was created.

## Desktop UI

- [Before restart](desktop-company-integration-before-restart.png)
- [After restart](desktop-company-integration-after-restart.png)

The after-restart screenshot shows the dynamic Package, persisted success/failure objects and the
recovered Core Responsibility, Employee, Capability Binding, Task, Execution, Evidence and Result
references.

## Repository active DB guard

Final active DB truth is unchanged from the Issue baseline:

- size `1232896`
- mtime epoch `1786873339`
- SHA-256 `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6`
- `integrity_check=ok`

All focused/regression tests explicitly set `CURIS_DB`, `CURIS_DB_PATH` and
`CURIS_WORKSPACE_DB` to the same repository-external isolated DB.

**WORKSPACE ENGINEERING P0.5 DESKTOP COMPANY INTEGRATION PROOF PASS**
