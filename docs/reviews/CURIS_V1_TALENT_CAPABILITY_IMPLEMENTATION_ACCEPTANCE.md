# CURIS V1 — TALENT & CAPABILITY IMPLEMENTATION ACCEPTANCE

Status: Frozen
Authority Class: CURRENT IMPLEMENTATION TRUTH / ACCEPTANCE REGISTRATION
Date: 2026-09-01
Disposition: IMPLEMENTED / ACCEPTED

## Accepted current truth

- **Talent & Capability Product:** ACCEPTED
- **Talent & Capability Implementation:** IMPLEMENTED / ACCEPTED
- **Expert Recruitment:** IMPLEMENTED / ACCEPTED
- **Company Employee:** IMPLEMENTED / ACCEPTED
- **Skill Installation:** IMPLEMENTED / ACCEPTED
- **Employee Capability Binding:** IMPLEMENTED / ACCEPTED
- **Connector state truth:** VERIFIED; current definitions remain `未连接 / 需要授权` unless real authorization and health exist
- **Employee Avatar:** IMPLEMENTED / ACCEPTED
- **Shared Employee Avatar truth:** VERIFIED
- **Packaged Desktop:** VERIFIED
- **Restart / Persistence:** VERIFIED
- **Active DB safety:** PASS

## Avatar closure

Employee Avatar uses the canonical `employee_instances.avatar_ref` projection consumed by Talent and Organization Center. The shared pattern is:

`uploaded asset > Curis Cartoon Avatar Set preset > fallback`

The current package contains eight local presets. Avatar is optional and never blocks Employee creation, responsibility, capability, or execution. Upload bytes are stored under the isolated app-data asset boundary; SQLite stores no image bytes, base64 data or arbitrary filesystem path. Browser and packaged restart evidence recovered the same Employee avatar references.

## Boundaries retained

Talent is not Employee; catalog entries do not become Company Employees without recruitment. Capability presence is not Employee ownership: the accepted chain remains `Capability → install / enable → explicit binding → execution availability`. Connector definitions are not connected or executable without real authorization and health. External talent candidates and unsupported catalog Skill types remain unavailable or conditional. Model / Provider management remains outside Talent and continues through the existing CEO settings / AI capability surface.

No parallel Organization, Employee, Avatar or Connector truth was created. Organization Center, Employee Detail, Responsibility and Business / Workspace relationships continue to consume canonical Employee truth.

## Evidence and remaining gaps

Evidence is recorded in `CURIS_V1_TALENT_CAPABILITY_PRODUCTIZATION_REVIEW.md` and `CURIS_V1_EMPLOYEE_RECRUITMENT_AVATAR_CLOSURE_REVIEW.md`: Browser, fresh packaged Desktop, failure/retry, restart/persistence, scoped tests/build and active SQLite integrity passed. Remaining bounded gaps are real external Connector authorization / execution, external Talent Providers, unsupported catalog Skill alignment, later avatar editing experience and specific Talent visual closure. These do not block this bounded acceptance registration.

Next Product Completion gate: `KNOWLEDGE LIBRARY DIRECTION D VISUAL CLOSURE`.

No code, Frontend, Backend, Runtime, Schema, DB, Figma, release, commit or push was performed by this registration.
