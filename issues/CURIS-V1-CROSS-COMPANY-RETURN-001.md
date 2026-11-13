# CURIS-V1-CROSS-COMPANY-RETURN-001

Status: Review
Authority Class: REVIEW / IMPLEMENTATION ISSUE
Disposition: REVIEW_REQUIRED
Owner: Curis V1 Delivery Owner
Objective: allow verified source Company business return through employee/model pages while preserving defaultCompany and backend tenant/company authority.

CEO delegated ordinary bounded decisions; Owner explicitly approved exact proposal after guardian self-seal, which is complete. Required flow: scoped Issue/preimages→bounded implementation/self-check→Owner independent QA.

Allowed Files: frontend/app/ceo-office/organization/employees/[id]/page.js; frontend/components/v1/ModelManagement.js; new frontend/lib/businessReturnApi.js; new frontend/tests/businessReturnApi.test.mjs; this Issue; docs/reviews/CURIS_V1_CROSS_COMPANY_RETURN_REVIEW.md; artifacts/tasks/CURIS-V1-CROSS-COMPANY-RETURN-001/**. Allowed Directories: existing exact-file parents only, granted Task directory, /private/tmp/curis-cross-company-return-20261005-01/{source,config,tests,logs,evidence,build,data,store,tmp}/**. No real DB/data/store fixture or service is authorized; unused directories not created.

Problem: Employee and ModelManagement effects/display bind source return to default runtime.companyId, preventing legal B return while default A remains. Backend collection/Object authorization is retained. Source metadata is location, never authorization.

Owned hunks: two consumer imports/return effects/display guards only, common helper finite target parsing and existing validator dispatch, new tests. No RuntimeProvider/default Company/model provider/forms/employee editor/sharedbar/composer/businessruntime or old sealed outputs changed. Preimages exact hashes recorded. Unknown concurrent hunks stop.

Source semantics: existing authenticated getInstalledWorkspace returns instance Company/workspace/id/package/status, but does not return tenant in instance DTO. Do not fabricate it: tenant comes from actual authorized business collection scope, bound to existing workspaceFetch tenant context. Resolve source instance then require entire original CG/Music/Writing collection/object/attempt validation, exact installed package consistency, expected employee Company if present. Writing additionally validates same instance/chapter; CG/Music retain original validators/source semantics. Reject missing/conflicting/forbidden scope; no URLcompany authority, fallback defaultCompany, extra navigation or persisted authorization truth. Async cancellation prevents stale links.

Inputs: actual two consumers, existing package getter and three finite parsers/validators; existing source identity/scopes are input, not new design. Output: source diff/seals, fake-request negative/positive tests+legacy regression, bounded lint/offline frontend build if legal. Tests are scoped unit fixtures, not real authorization/UI acceptance.

Permission boundary: no new real DB, fixture/service/HTTP/Provider/App/native/userfiles/Keychain/protectedDB access or Git operations. Temporary files only granted roots. Offline tool dependencies only, network denied; runtime proof next needs separately approved QA. Source cache input remains isolated by existing business ownership keys, never changed by this fix.

Acceptance checks: default A, verified B returns for employee/model; A-B-A scoped cache tests unchanged; employee-source mismatch, server403/404, invalid tenant/workspace/package/instance, nonexistent original version/attempt, dangerous/duplicate/unknown or mixed query rejected; legacyWriting/Music Song+Operating return preserved. Component bounded lint/prod build, no unexpected diff.

Approval impact/risk: front return resolution only; default context unchanged; extra metadata request; broad backend changes forbidden. Next iteration/gate: independent QA actual permitted same isolated DB A→B→A return/cache and foreign API rejection, then native only separate grant. Verdict pending / NOT_ACCEPTED. All outputs REVIEW_REQUIRED, no canonical Authority/Pointer/CurrentState/ChangeLog promotion authorized.

Self-validation:43tests/scopedlint/offlinewebpack47routes PASS; query continuity source+compile only, actual Browser/React DOM/API/DB/fixture/native NOT_RUN. IndependentQA pending; NOT_ACCEPTED.
