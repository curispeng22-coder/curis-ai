# CURIS-V1-EMPLOYEE-RECRUITMENT-AVATAR-CLOSURE-001

Status: Review
Authority Class: CURRENT IMPLEMENTATION ISSUE
Date: 2026-09-01
Owner: Main Development Session

## Goal

补齐现有 canonical Employee 招聘时的可选头像：本地上传、Curis 内置卡通预设、稳定 fallback。所有已有头像投影读取同一个 `employee_instances.avatar_ref`，不建立第二套 Employee、Identity 或 Avatar 系统。

## Authority

- `docs/reviews/CURIS_AVATAR_IDENTITY_PATTERN.md`
- `docs/reviews/CURIS_V1_TALENT_CAPABILITY_PRODUCTIZATION_REVIEW.md`
- `issues/CURIS-V1-TALENT-CAPABILITY-PRODUCTIZATION-001.md`
- Current Employee / Identity implementation truth
- Current Organization Center accepted implementation
- `docs/00_Context/CURRENT_STATE.md`

## Current Gap

- `employee_instances` 没有统一 current avatar reference。
- Talent 与 Organization 只能显示首字 fallback。
- `persona_templates.image_ref_json` 是模板图像，不是 Employee instance current avatar truth。
- CEO 旧入口使用 base64 持久化；该实现不适用于 Employee，且本 Issue 明确禁止把图片二进制/base64 写入 SQLite。

## Pre-change Ownership

HEAD: `c797db840bad285d7e9f1962d06eac61aa28508b`

| Path | SHA-256 | Owned semantic hunk |
|---|---|---|
| `backend/app/database.py` | `460bc5d62911127ba7ee9c1fc5b4cf91f685c8932b73ea9e5d343097439852d5` | additive Employee avatar reference column only |
| `backend/app/employee_templates.py` | `4a4147bfaf42019eb022f5ba7584bfd1bf6a1b4d28232f350a06c97e9c5e001a` | canonical avatar validation/local asset reference methods only |
| `backend/app/main.py` | `f594ececaab79c4066629b372dd3caa1f13ae132e36a5bc5d0c91b3f74afcc0d` | recruitment avatar field + upload/content routes only |
| `backend/app/organization_projection.py` | `0189ff5a847be26e6c1d35fcebea7cd80da7a72a502837420d3cc6e0736d003d` | include canonical avatar reference in read projection only |
| `frontend/lib/api.js` | `e06a18db7f28c5408e632ec23cd4ab2c8a52141c5ff472a9093c901c01c58350` | blob response support only |
| `frontend/lib/talentMarket.js` | `9e75c127b6f558fce8501004a4db3630db1890a542de4601ad75707f4785491f` | upload call only |
| `frontend/lib/organizationProjection.js` | `ade1248498ab3c9ab53028ce996a94b78fef1bcfc055ee143dd57c3b9c9189f8` | preserve Employee avatar reference only |
| `frontend/app/ceo-office/talent-market/page.js` | `19a884020b2c774666a9826dac2a435091d688b96408ad4fa774824948f057d0` | bounded recruitment avatar chooser only |
| `frontend/app/ceo-office/organization/OrganizationCenter.js` | `e28d8401ed89058f7f04b637338990a721303cd5f141dd5984bf7121d7925975` | existing Employee/leader avatar projection only |
| `frontend/app/ceo-office/organization/organizationCenter.module.css` | `c017b06d639eb42f6964a4ed2ac70d176b1405f4676493039749d33b5c5a20ad` | image fit within existing avatar surface only |

All files are preserved mixed-source. This Issue owns only the exact semantic hunks above and will not stage, commit, reset, clean or overwrite unrelated work.

## Allowed Files

- `backend/app/database.py`
- `backend/app/employee_templates.py`
- `backend/app/main.py`
- `backend/app/organization_projection.py`
- `backend/tests/test_employee_recruitment_avatar.py`
- `frontend/lib/api.js`
- `frontend/lib/talentMarket.js`
- `frontend/lib/organizationProjection.js`
- `frontend/components/v1/EmployeeAvatar.js`
- `frontend/app/ceo-office/talent-market/page.js`
- `frontend/app/ceo-office/organization/OrganizationCenter.js`
- `frontend/app/ceo-office/organization/organizationCenter.module.css`
- `frontend/public/avatars/curis-employee/*.svg` (exact eight bundled presets)
- `frontend/tests/employeeRecruitmentAvatar.test.mjs`
- this Issue
- `docs/reviews/CURIS_V1_EMPLOYEE_RECRUITMENT_AVATAR_CLOSURE_REVIEW.md`
- bounded closure references appended to the current Talent Issue/Review

## Runtime Truth

- Resolution order: uploaded `asset:*` reference > selected `preset:*` reference > empty-reference initial fallback.
- SQLite stores only the bounded reference, never image bytes, base64 or an arbitrary filesystem path.
- Uploaded bytes live below the current isolated/packaged database data directory and are served only after tenant-scoped Employee resolution.
- Accepted MIME/signatures: PNG, JPEG, WebP; maximum 2 MiB.
- Upload failure never rolls back or blocks canonical Employee creation. A retry uses the same Employee rather than creating a duplicate.
- Preset asset failure degrades to the stable fallback.

## Acceptance

1. Employee A: upload valid local image, canonical `asset:*` reference and content persist.
2. Employee B: choose one bundled Curis preset, canonical `preset:*` persists.
3. Employee C: skip avatar, empty reference renders stable initial fallback.
4. Invalid type/oversize upload is rejected without changing the current avatar or creating another Employee.
5. Talent Company Employee and Organization Directory read the same canonical reference.
6. Existing name-only surfaces are not forced to add an avatar; no competing projection is introduced.
7. Same isolated SQLite/app-data survives complete Runtime/Desktop restart with all three identities unchanged.
8. Missing preset/upload asset renders fallback and does not block Employee use.
9. Recruitment, Employee identity, Talent and Organization regressions pass.
10. Fresh packaged Desktop proves upload/preset/fallback, Organization continuity and restart.

## Active DB Protection

Preflight:

| Path | Size | mtime | SHA-256 | integrity_check |
|---|---:|---:|---|---|
| `data/curis.sqlite` | `1232896` | `1786873339` | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` | `ok` |
| `backend/data/curis.sqlite` | `1277952` | `1786783659` | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` | `ok` |

All tests and acceptance use repository-external isolated SQLite/app-data. No active DB initialization or migration is allowed.

## Explicit Exclusions

- No new Identity/Employee/Avatar service, no profile editor, no image editor/cropper service.
- No base64/blob in SQLite/JSON, arbitrary local path, remote avatar service or runtime download.
- No Talent/Organization redesign, Figma, model/provider/connector work, release, commit or push.

## Stop Gates

- A second identity truth or unbounded file access is required.
- Current canonical Employee cannot safely carry the reference without authority conflict.
- Active DB changes, unrelated ownership collision, or destructive migration occurs.

## Implementation Result

`IMPLEMENTED / ACCEPTED CANDIDATE`

- `employee_instances.avatar_ref` is the single current Employee avatar reference.
- Recruitment supports validated local upload, eight bundled Curis presets, and optional fallback.
- Uploaded bytes remain below the current isolated/packaged data root; SQLite stores only `asset:*`, `preset:*`, or an empty fallback reference.
- Talent and Organization consume the same canonical reference. Existing name-only Employee surfaces remain unchanged.
- Browser and fresh packaged Desktop proved three independent employees, complete shutdown, restart recovery, and no duplicate/overwritten identity.
- Exact evidence and truthful boundaries are recorded in `docs/reviews/CURIS_V1_EMPLOYEE_RECRUITMENT_AVATAR_CLOSURE_REVIEW.md`.
- No commit or push was performed.
