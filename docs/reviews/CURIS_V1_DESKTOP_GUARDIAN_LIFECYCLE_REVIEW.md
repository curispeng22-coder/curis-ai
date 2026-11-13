# Guardian parent lifecycle bounded implementation review

Task ID: CURIS-V1-DESKTOP-GUARDIAN-LIFECYCLE-001
Authority Class: REVIEW
Status: Review
Disposition: REVIEW_REQUIRED
Owner: Curis V1 Delivery Owner
Verdict: READY_FOR_INDEPENDENT_BOUNDED_QA / NOT_ACCEPTED

Problem: instrumented historical supervisor created target then /bin/ps query PermissionError stopped it. Permission origin remains UNKNOWN. This fix uses the spawner-created stdin pipe lifetime, not a replacement process-query tool. Rust Child retains the sole write end, checks CLOEXEC and sends finite PID handshake. Guardian checks FIFO/64byte/3second handshake before spawn, reads lifecycle loss, gives target DEVNULL stdin, and performs TERM→3s→KILL→wait. Rust closes pipe then gives guardian4s. Startup rollback uses same cleanup. No business/identity/env/ports/readiness/package-script or Product Authority change.

Owner review found inherited signal mask [2,15] in the first attempt. That failed implementation and probe are retained. Current pending_stop defers during Popen without masking target signals; after assignment it stops the owned target. Normal targets have empty blocked mask and write TERM flush receipt, rather than forced-kill. Tests do not unblock signals in the target.

Evidence: source16 PASS /10.387s and actual onefile16 PASS /45.781s, each13 live-process cases plus3 module checks (IO exception/mock query dependency/deterministic spawn-signal unit). Harmless parent alive, EOF, normal and foreign/missing/oversize/timeout/extra channel rejection, TERM/INT, target natural status7, ignoreTERM escalation, parentSIGKILL with intermediary reader verified. Five actual Rust caller cases PASS: closed-read-end writefail cleans already-spawned process+wait; missingpipe cleanup; both actual targets rollback and flush; unrelated exec remains alive after parent/guardian/target gone proving write-end noninheritance; ignoreTERM cleanup3.039s<4s. Exact production attach/kill source functions compile in standalone Rust fixture; full Tauri cargo check NOT_RUN (offline isolated cache lacks libc), no network/install retry. Native App NOT_RUN.

Failures retained: first guard source15 failed7/errors1 due DEVNULL denied by added stricter write guard; specific trace retained. Owner approved DEVICE_SINK_ONLY literal /dev/null exception; newguard diff/hash retained, oldv2 untouched. Initial source-wrapper Rustfixture Os13 PermissionDenied with whitespace shebang retained; not retried, actual previously approved packaged checks used. Exact OS cause not generalized. All normal/failed fixtures bounded and closed. Current owned PID receipts all gone; external unused.sqlite absent. No protected DB open/stat/hash/revalidation; prior fingerprints historical only. No App, business Runtime import, Keychain, Provider, HTTP or network connection run by task.

Approval/problem/basis/impact/risk recorded in Issue and APPROVAL_LEDGER. Scope is direct sidecar only; no guarantee for arbitrary descendants or forced guardianSIGKILL, no durable data/native shutdown acceptance. Source two files/preimages/diff/seal precise; no unknown source hunks or Git operations. Outputs retained REVIEW_REQUIRED; no PROMOTE/ARCHIVE/DELETE.

Next Gate: Owner independent QA exact sealed source and onefile identity/lifecycle/ownership cases plus full Tauri compilation in an authorized offline build scope. Only after QA passes may separately approved fresh native lifecycle/product acceptance proceed. Owner owns final acceptance; this self-review cannot promote Product or implementation authority.

Task Output Manifest: Issue; this Review; task scope/preimages/source snapshots/owned diff/approval ledger/check results/HANDOFF/SOURCE_SEAL/OUTPUT_MANIFEST; external source/config/tests/logs/evidence/build/tmp retained. All are REVIEW_REQUIRED. Output manifest excludes itself and seals Task+external regular files. No canonical Pointer/CURRENT_STATE/ChangeLog write was granted or performed.
