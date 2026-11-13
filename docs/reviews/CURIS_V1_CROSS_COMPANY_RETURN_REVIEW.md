# Cross-company business return bounded implementation review

Task ID: CURIS-V1-CROSS-COMPANY-RETURN-001
Authority Class: REVIEW
Status: Review
Disposition: REVIEW_REQUIRED
Owner: Curis V1 Delivery Owner
Verdict: READY_FOR_INDEPENDENT_BOUNDED_QA / NOT_ACCEPTED

Employee and ModelManagement now resolve source Company from existing installed workspace metadata, then run unchanged authenticated CG/Music/Writing collection/object/attempt validators. Metadata alone does not authorize: original business request must succeed, tenant context/workspace/package/active instance consistency must hold, employee Company must match. No URL Company authority or default Company override/fallback. Imported identity headers are never overridden. CG/Music scopes have no instance field; Writing same-instance check retained; no fabricated fields.

Two consumer return effects use current Next search params and cancel stale Promises. Query-bound success stamps suppress prior links synchronously on changed query. Employee conversation return follows the same query; original employee/editor/model provider/connection/shared conversation and business input caches remain unchanged. Same-file Suspense boundary compiles without extra files/navigation.

43 tests PASS (14 new finite/fake-request cases plus29 CG/Music/Writing regressions); scoped lint PASS; actual offline webpack build PASS47/47routes with final source. Negative cases include backend403/404, Company/tenant/workspace/package/instance/read-only conflict, employee mismatch, absent version/original attempt and malformed/duplicate/unknown/external/cross-kind Company injection. Actual backend calls/DB/services/Provider/Browser/native are NOT_RUN. Cache regression is the existing scoped input test, not a new live A-B-A acceptance. Query continuity is source/compiler evidence only; no actual React DOM test runner is present and no install was authorized. Independent QA must operate same mounted consumer changing query and resolve older async last, plus real A-B-A employee/model/cache/API rejection.

Tool/input failures remain in exact logs: Node ENOENT, unsupported flag, wrong Writing parser import, absent workspace node_modules. Final existing toolchain/path corrected; no installs or permission bypass. Current Node typeless-package warnings are retained. Pure source export excludes backend/history/data/credentials and uses old dependencies read-only; no mixed old physical backend export is reused. Build output manifest is independent and no scripts were loaded by Browser.

Old Music151 and guardian240 exact outputs0drift; original source snapshots/seals untouched. Four owned source files (two new) and precise preimages/diff/seals. No Git operation, protected DB read, Provider fee, Keychain or App launch. No canonical Pointer/CurrentState/ChangeLog grant/promotion.

Owner approval/problem/basis/impact/risk/next iteration are in Issue/APPROVAL_LEDGER. Task Output Manifest: Issue, Review, task scope/preimages/source snapshots/owned diff/ledger/checks/HANDOFF/source/build/output seals, exact external frontend/config/log/evidence/build retained REVIEW_REQUIRED; no PROMOTE/ARCHIVE/DELETE. Next Gate: Owner independent QA exact new four source files and final build; full real user navigation/identity proof separately authorized.

Physical export clarification: the frontend source input seal lists237 inputs, generated .next seal1516 files; Next also copied27 traced public dependency files under an external source sibling and Node created2368 external temporary compile-cache entries. All are retained and covered by the final output inventory; copied dependency paths are additionally in BUILD_OUTPUT_SEAL. Only the actual readonly dependency symlink is excluded. This physical inventory is not a portable native package or clean-source promotion. An interim overbroad node_modules exclusion was corrected before handoff; the draft manifest is preserved for provenance.
