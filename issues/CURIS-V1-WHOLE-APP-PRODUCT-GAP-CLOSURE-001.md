# CURIS-V1-WHOLE-APP-PRODUCT-GAP-CLOSURE-001

Status: Implemented / Accepted with Recorded P1

Authority Class: CURRENT / IMPLEMENTATION ISSUE

Owner: Main Development Session

## Goal

Close the two product seams proven by the packaged whole-app acceptance without creating a second
Team, Responsibility, Capability, Conversation or execution system:

`recruited Employee → General Workspace Responsibility → legal Work → real execution → Result/Evidence/P7 → restart`

and:

`CEO Assistant Composer → selected/default verified model → real response → same Assistant persistence`.

## Product gaps

1. A recruited Company Employee cannot be assigned to the current General Workspace through UI.
2. CEO Desk renders the canonical CEO Assistant but its Conversation composer has no submit path.

## Allowed Files

- `backend/app/runtime/general_workspace_delivery.py`
- `backend/app/api/shared_workspace_router.py`
- `backend/app/api/team_operating_router.py` — resume an existing failed/rejected Employee result through the existing CONTINUE signal
- `backend/app/api/frontend_v1_router.py`
- `backend/app/main.py` — router dependency injection only
- `backend/app/employee_execution_identity.py` — accept existing verified model-call evidence for model-bound Employee callbacks
- `backend/app/ai_usage.py` — resolve canonical execution provenance by the current Task/Execution rather than requiring one Task per Work
- `backend/tests/test_employee_execution_identity.py`
- `backend/tests/test_canonical_usage_attribution.py`
- `backend/tests/test_v1_general_workspace_p1_operating_closure.py`
- `backend/tests/test_v1_frontend_batch1.py`
- `frontend/components/v1/GeneralWorkspaceOperating.js`
- `frontend/components/v1/CeoDeskOperating.js`
- `frontend/components/v1/SharedConversation.js` — selected model handoff only
- `frontend/lib/runtimeApi.js`
- `frontend/lib/v1FrontendApi.js`
- `frontend/tests/v1GeneralWorkspaceOperating.test.mjs`
- `frontend/tests/v1FrontendBatch1.test.mjs`
- this Issue and the two bounded Reviews named below

Any additional source file requires an Issue amendment before modification.

## Runtime/API seams

- Reuse `AI_EMPLOYEE`, `ROLE_SLOT`, `RESPONSIBILITY_ASSIGNMENT`,
  `RESPONSIBILITY_WORKFLOW`, `EmployeeExecutionIdentity` and the current verified tenant model.
- A user explicitly chooses a recruited Employee and states the responsibility. No role or Employee
  is inferred silently.
- The current verified default model may be attached as that Employee's execution capability; no
  per-Employee Provider form is added.
- Persist bounded CEO/Assistant messages on the one canonical `CEO_ASSISTANT` Runtime entity.
- Reuse the accepted Model Preference, native credential recovery and model adapter. Provider errors
  remain errors; no local answer is substituted.

## Test matrix

1. Candidate list is Company/Workspace scoped.
2. Assignment requires a real Employee, explicit responsibility and eligible default model.
3. Assignment creates one canonical Role, Employee bridge, Responsibility and Workflow.
4. Retry/restart returns the same objects and creates no duplicates.
5. Conflicting Employee/Workspace/capability truth fails closed.
6. Legal Work can execute through the existing Team Operating chain.
7. Result/Evidence/P7 continue to reference existing canonical objects.
8. CEO Assistant submit uses one canonical Assistant and one eligible model.
9. Assistant messages survive restart; Provider failure creates no fabricated reply.
10. Existing General Workspace, RD, XHS, usage attribution, Keychain and DB-safety regressions pass.

## Database safety

All tests and acceptance writes use repository-external SQLite selected by all three variables:
`CURIS_DB`, `CURIS_DB_PATH`, `CURIS_WORKSPACE_DB`. Repository active databases are fingerprinted
before and after and must remain byte-identical with `integrity_check=ok`.

## Stop gates

- a new schema or shared Runtime primitive is required;
- Product/Frozen Authority conflict;
- active database mutation;
- unresolvable mixed-source ownership collision;
- a fake Employee, capability, Provider response, Result, Evidence or Decision would be required.

## Explicit exclusions

No Provider/Keychain redesign, Team Builder, Chat V2, Memory V2, professional matcher, RD/XHS/TTK
domain change, release signing/notarization, commit or push.

## Acceptance path

Fresh packaged UI: recruit Employee → assign responsibility → create/execute Work → Result/Evidence
→ legitimate P7 round-trip → CEO Desk → full restart → CEO Assistant and Workspace post-restart real
AI action. Secret scans must remain zero and active databases unchanged.

## Closure

Accepted on 2026-08-30 against the packaged app at:

`/Users/yy/Documents/Curis AI Workspace/desktop/target/release/bundle/macos/Curis.app`

The bounded chain is proven with a real DeepSeek model, one canonical recruited Employee, one
Workspace-scoped Responsibility, real Work retries, Result/Evidence/Artifact references, one
high-risk P7 Decision Packet, automatic continuation, full process restart and post-restart model
recovery. The formal acceptance record is:

`docs/reviews/CURIS_V1_WHOLE_APP_PRODUCT_GAP_CLOSURE_REVIEW.md`

Recorded P1 items are limited to presentation/release quality: CEO Desk still exposes some internal
IDs/status enums, APPLIED decisions remain in the low-rank continuous-attention list, and ad-hoc
rebuilt packages have unstable macOS code identity until distribution signing/notarization. These do
not invalidate the scoped operating chain. No commit or push was created.
