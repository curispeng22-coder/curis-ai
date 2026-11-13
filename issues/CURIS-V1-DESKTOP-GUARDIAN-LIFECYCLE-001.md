# CURIS-V1-DESKTOP-GUARDIAN-LIFECYCLE-001

Status: Review
Authority Class: REVIEW / IMPLEMENTATION ISSUE
Disposition: REVIEW_REQUIRED
Owner: Curis V1 Delivery Owner
Objective: replace permission-sensitive ancestry queries with a parent-owned anonymous pipe lifecycle while preserving fail-safe direct-sidecar supervision.

Approval: CEO delegated ordinary bounded fixes to Delivery Owner; Owner explicitly approved this exact proposal and withdrew its generalized protected-DB reread requirement, retaining stricter NO protected DB reads. This is implementation authorization, not Product/Frozen promotion or native acceptance.

Problem/evidence: instrumentation diagnostic created target then parent-query PermissionError caused false-ancestor safe-stop. Permission origin/errno remains UNKNOWN. No alternate query tool or guard widening is authorized.

Allowed Files: desktop/runtime/guardian.py; desktop/src/lib.rs; this Issue; docs/reviews/CURIS_V1_DESKTOP_GUARDIAN_LIFECYCLE_REVIEW.md; artifacts/tasks/CURIS-V1-DESKTOP-GUARDIAN-LIFECYCLE-001/**. Allowed Directories: existing exact-file parents only, granted task directory, /private/tmp/curis-guardian-lifecycle-20261005-01/{source,config,tests,logs,evidence,build,tmp}/**. No other canonical writes.

Owned hunks: guardian imports/ancestry supervision/main lifecycle only; Rust spawn_guarded stdin ownership/handshake/fail-safe cleanup, kill_child cleanup timing and startup rollback branches. Child already owns ChildStdin so retain standard Child ownership rather than introduce a redundant wrapper; no change in scope or security model. No business, identity, DB, env, port, readiness, native resource or packaging-script changes. Preimages exact hashes in task/PREIMAGES.json.

Lifecycle design: parent creates pipe, holds CLOEXEC write end in Child.stdin, sends finite parent-pid handshake. Guardian checks pipe and bounded handshake before spawning; target stdin DEVNULL; parent close/death EOF, invalid bytes/read failures stop direct sidecar. TERM/3s/KILL/wait, Rust4s grace. No broad PID queries/network/permission changes. Handshake consistency does not authorize arbitrary PID or URL.

Inputs: current guardian.py/lib.rs; current navigation/Implementation route; instrumented Review REPORT+observed branch. History is diagnostic evidence only. Output: bounded source diff, stdlib process tests, isolated offline onefile build/probe if legitimate, Rust compile/check if offline permitted, process closure and seals, formal Review/HANDOFF.

Acceptance evidence: valid parent-live lifetime; natural target status; parent close/death; invalid/missing/oversize/timed-out handshake before target creation; intermediary parent compatible; no write-end leaks on unrelated exec; TERM/INT and ignore-TERM escalation; Rust4s coordinates guardian3s; startup rollback cleanup. Tests only harmless fixtures in external root. No Curis imports/DB/Provider/HTTP/App/Keychain. Old protected fingerprints may be referenced only as historical baseline, not current revalidation.

Build boundary: existing offline tools only, outputs/cache/spec/tmp/dist confined root. Default PyInstaller internal adhoc identity permitted for new test binary only; no standalone codesign/certificate/Keychain/entitlements or old bundle changes. Guard or offline compile blockers are NOT_RUN; no install or permission workaround. Native acceptance requires independent QA, not self-tests.

Approved effect/risk: changes packaged supervisor lifecycle only; stdin dedicated to lifecycle, original targets no interactive stdin. Direct sidecar scope only; forced supervisor SIGKILL cannot promise full descendant-group cleanup. Follow-up: independent QA actual sealed onefile, then separately approved fresh native acceptance. NO Git mutation, protected DB reads, default App or Provider execution.

Next Gate: implement/self-test/seal → Owner independent QA; verdict pending. All durable outputs REVIEW_REQUIRED.

Self-validation completed: 16 source +16 packaged checks, five Rust caller cases PASS. Full Tauri compile NOT_RUN missing offline dependency, native NOT_RUN. Initial failure/mask/DEVICE_SINK_ONLY approval retained. Next independent QA; NOT_ACCEPTED. Review: /Users/yy/Documents/Curis AI Workspace/docs/reviews/CURIS_V1_DESKTOP_GUARDIAN_LIFECYCLE_REVIEW.md
