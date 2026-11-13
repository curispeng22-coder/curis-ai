# CURIS V1 — Employee Recruitment Avatar Closure Review

Status: Review
Authority Class: EVIDENCE
Date: 2026-09-01
Issue: `CURIS-V1-EMPLOYEE-RECRUITMENT-AVATAR-CLOSURE-001`
Owner: Main Development Session

## 1. Upload

Recruitment accepts PNG, JPEG and WebP up to 2 MiB. MIME and file signature are both checked before persistence. A valid image is written below the current database data root and the Employee stores only `asset:<sha256>.<extension>`.

Browser and fresh packaged Desktop each recruited an Employee through the visible upload control and native file picker. The final packaged proof used `desktop/icons/64x64.png`; the resulting canonical reference was `asset:e5e51a25b6a047328ea592f29353f67782c6aaae1bf8e68594394cdbab4e7677.png`.

Invalid MIME and oversize payloads return a bounded validation error, preserve the prior selection/reference, and do not create a second Employee.

## 2. Preset

Eight local Curis Cartoon Avatar Set assets ship under `frontend/public/avatars/curis-employee/`:

`iris`, `sage`, `coral`, `amber`, `sky`, `plum`, `mint`, `slate`.

No runtime network download or remote avatar service is used. Browser and packaged Desktop selected `青禾`; the canonical Employee reference persisted as `preset:sage`.

## 3. Fallback

Avatar remains optional. Skipping stores an empty canonical reference and renders the stable Employee-name initial fallback. Missing local preset/upload content also degrades to the same fallback and never blocks Employee creation or use.

Resolution order is:

`uploaded asset > selected preset > fallback`.

## 4. Persistence truth

Employee current avatar truth is `employee_instances.avatar_ref`. This is an additive field on the existing canonical Employee instance, not a new identity/avatar store.

The final isolated packaged database contained exactly:

- `最终上传头像员工` → `asset:e5e51a25...7677.png`
- `最终预设头像员工` → `preset:sage`
- `最终默认头像员工` → empty reference

SQLite scan found `0` data-URI or absolute-path avatar references. Uploaded bytes existed only under the isolated app-data asset directory. `integrity_check=ok`.

## 5. Organization continuity

Talent Company Employee and Organization Center Employee Directory both consume the same canonical `avatar_ref`; Organization does not copy image data or create `organization_avatar` state.

Browser and packaged Desktop each showed the same three Employee identities in Organization after recruitment. Multiple employees kept independent references and did not overwrite one another.

## 6. Employee surfaces

The shared `EmployeeAvatar` projection is used on existing Talent and Organization avatar surfaces. It resolves canonical upload/preset/fallback truth and fetches uploaded content through the tenant-scoped Employee endpoint.

Employee Detail, Conversation and Responsibility surfaces that currently show names only were not expanded; this matches the bounded contract and avoids introducing a competing avatar projection.

## 7. Restart

Browser proof used one repository-external SQLite, stopped the backend, restarted it on the same database, reloaded Organization, and recovered all three references.

Packaged proof used:

- app: `/Users/yy/Documents/Curis AI Workspace/desktop/target/release/bundle/macos/Curis.app`
- app-data: `/tmp/curis-avatar-desktop-final.uJrXWw`
- desktop binary SHA-256: `cabc9d9be89ec65af2511c3670ace505a6668979d542ca7c062d0b2c943c5f5a`
- packaged Workspace sidecar SHA-256: `8b0ea8a206a73423edff12c8f2c313512acf5af5a31554532d8b3495d9162445`

The app was fully closed; `curis-desktop`, Workspace, Gateway, Guardian and frontend process count reached zero. Reopening with the same isolated app-data restored the same Company, three Employees and three avatar modes in Organization.

Evidence:

- `/tmp/curis-avatar-browser-talent.png`
- `/tmp/curis-avatar-browser-organization.png`
- `/tmp/curis-avatar-desktop-final-organization.png`
- `/tmp/curis-avatar-desktop-final-restart.png`

## 8. Security

- No image bytes/base64 are stored in SQLite or JSON.
- No arbitrary user filesystem path is persisted or served.
- Asset lookup derives a tenant-hash/Employee-hash directory and accepts only the bounded `asset:<sha256>.<extension>` reference.
- GET content first resolves the tenant-scoped Employee.
- Upload validates declared MIME, magic bytes and 2 MiB limit.
- Local preset assets are bundled and traceable; no remote service exists.
- Upload failure does not roll back the canonical Employee. Retry targets the same Employee.

## 9. Tests and build

- Backend focused/no-regression: `23 passed`.
- Frontend focused/no-regression: `17 passed`.
- Python compile: pass.
- Scoped ESLint: pass.
- Frontend production build: pass.
- Fresh Workspace/Gateway/Guardian/Recovery sidecars: pass.
- Fresh Tauri `Curis.app`: pass.
- Scoped `git diff --check`: pass.
- Browser fresh-tab console errors: `0`.

Coverage includes upload, preset, fallback, invalid file, oversize, multiple Employees, cross-tenant denial, Organization projection, restart, recruitment, Talent, Employee execution identity, shared Workspace projection and V1 frontend navigation.

## 10. Active DB safety

Both repository active SQLite files are byte-identical to preflight and pass integrity:

| Path | Size | mtime | SHA-256 | integrity_check |
|---|---:|---:|---|---|
| `data/curis.sqlite` | `1232896` | `1786873339` | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` | `ok` |
| `backend/data/curis.sqlite` | `1277952` | `1786783659` | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` | `ok` |

All tests, Browser and Desktop evidence used repository-external isolated SQLite/app-data.

## 11. Employee Avatar verdict

`EMPLOYEE AVATAR: IMPLEMENTED / ACCEPTED CANDIDATE`

Upload, bundled preset, fallback, shared canonical identity, cross-surface continuity and complete restart recovery are all implemented and evidenced. No new Identity/Employee/Avatar system was created. No commit or push was performed.

## 12. Recommended Talent & Capability status

`TALENT & CAPABILITY: IMPLEMENTED / ACCEPTED`

This recommendation closes the final explicit P1 avatar gap. Existing truthful boundaries remain: real external Connector authorization/health/execution and unsupported external catalog items are not promoted to connected capability.

STOP FOR CEO / CHATGPT EMPLOYEE AVATAR REVIEW.
