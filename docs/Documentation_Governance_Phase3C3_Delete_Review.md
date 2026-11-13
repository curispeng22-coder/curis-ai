# Curis Documentation Governance Phase 3-C3 Delete Review

Status: Review

Baseline:
main @ e86c9a54e51d0b4a13b259f20024ee3676dcb364

Updated:
2026-07-30

---

## 1. Conclusion

Phase 3-C3 reviewed all 41 Delete Candidate records from the Phase 3-B2
Asset Report. This phase performed analysis only.

| Result | Count | Disposition |
| --- | ---: | --- |
| Safe Delete | 35 | Eligible for a separately authorized deletion batch after final pre-delete checks |
| Keep | 0 | No candidate contains unique historical, technical or design value |
| Protected | 6 | Retain because a current or implicit build/runtime dependency exists |
| Total | 41 | Complete Phase 3-B2 Delete Candidate cohort |

- Tracked candidates: 8
- Ignored candidates: 33
- Files or directories deleted: 0
- Files or directories moved: 0
- Code or configuration modified: 0

Safe Delete is a recommendation, not deletion authorization.

## 2. Audit Method

For each candidate the review checked:

1. current Git tracked or ignored state;
2. exact repository-relative references from Markdown, scripts/configuration and
   Agent instruction files, excluding governance inventories/reports as consumers;
3. build and deployment consumption, including implicit package/runtime dependencies;
4. current filesystem presence;
5. regeneration or retained-copy evidence;
6. historical decision, validation and design-reference value.

Current runtime inspection found an active Next development process using
`frontend/node_modules/` and `frontend/.next/`. These paths therefore remain
Protected even though they are reproducible.

Mentions in ignore rules, cleanup documentation or historical reviews are reported but
are not treated as consumers when the referenced residue itself has no retained value.

## 3. Complete 41-Item Review

| Path | Type | Git State | Markdown Audit | Script/Config Audit | Agent Audit | Build/Deploy Audit | Value Assessment | Recommendation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `.DS_Store` | Ignored File | Ignored | 7 项提及/ignore，不消费 | 1 项提及/ignore，不消费 | 0 | 无消费；仅历史提及或 ignore 规则 | 无历史价值；Finder 元数据 | Safe Delete |
| `.pytest_cache/` | Ignored Directory | Ignored | 2 项提及/ignore，不消费 | 2 项提及/ignore，不消费 | 0 | 无消费；仅 ignore/缓存规则 | 无历史价值；pytest 可重建缓存 | Safe Delete |
| `.tmp-ui-handoff/` | Ignored Directory | Ignored | 0 | 0 | 0 | 未检测到构建/部署消费 | 无历史价值；目录内仅含两个 .DS_Store 文件 | Safe Delete |
| `.venv/` | Ignored Directory | Ignored | 173 项 | 25 项 | 0 | 是：官方 Workspace backend launcher 及测试链引用 | 环境可重建，但当前启动/测试文档和脚本依赖原路径 | Protected |
| `backend/__pycache__/` | Ignored Directory | Ignored | 0 | 0 | 0 | 无消费；仅 ignore/缓存规则 | 无历史价值；Python 字节码缓存 | Safe Delete |
| `backend/.pytest_cache/` | Ignored Directory | Ignored | 0 | 1 项提及/ignore，不消费 | 0 | 无消费；仅 ignore/缓存规则 | 无历史价值；pytest 可重建缓存 | Safe Delete |
| `backend/.venv/` | Ignored Directory | Ignored | 66 项 | 17 项 | 0 | 是：后端测试/工具链引用 | 环境可重建，但大量测试和工具引用原路径 | Protected |
| `backend/app/__pycache__/` | Ignored Directory | Ignored | 0 | 0 | 0 | 无消费；仅 ignore/缓存规则 | 无历史价值；Python 字节码缓存 | Safe Delete |
| `backend/app/agent_conversion/__pycache__/` | Ignored Directory | Ignored | 0 | 0 | 0 | 无消费；仅 ignore/缓存规则 | 无历史价值；Python 字节码缓存 | Safe Delete |
| `backend/app/connectors/__pycache__/` | Ignored Directory | Ignored | 0 | 0 | 0 | 无消费；仅 ignore/缓存规则 | 无历史价值；Python 字节码缓存 | Safe Delete |
| `backend/app/models/__pycache__/` | Ignored Directory | Ignored | 0 | 0 | 0 | 无消费；仅 ignore/缓存规则 | 无历史价值；Python 字节码缓存 | Safe Delete |
| `backend/app/routers/__pycache__/` | Ignored Directory | Ignored | 0 | 0 | 0 | 无消费；仅 ignore/缓存规则 | 无历史价值；Python 字节码缓存 | Safe Delete |
| `backend/scripts/__pycache__/` | Ignored Directory | Ignored | 0 | 0 | 0 | 无消费；仅 ignore/缓存规则 | 无历史价值；Python 字节码缓存 | Safe Delete |
| `backend/selfuse.log` | Ignored File | Ignored | 0 | 0 | 0 | 未检测到构建/部署消费 | 未作为验收证据引用；当前无进程打开该日志 | Safe Delete |
| `backend/tests/__pycache__/` | Ignored Directory | Ignored | 0 | 0 | 0 | 无消费；仅 ignore/缓存规则 | 无历史价值；Python 字节码缓存 | Safe Delete |
| `backend/tests/real_run/__pycache__/` | Ignored Directory | Ignored | 0 | 0 | 0 | 无消费；仅 ignore/缓存规则 | 无历史价值；Python 字节码缓存 | Safe Delete |
| `deploy/.DS_Store` | Ignored File | Ignored | 0 | 0 | 0 | 无消费；仅历史提及或 ignore 规则 | 无历史价值；Finder 元数据 | Safe Delete |
| `deploy/curis/.DS_Store` | Ignored File | Ignored | 0 | 0 | 0 | 无消费；仅历史提及或 ignore 规则 | 无历史价值；Finder 元数据 | Safe Delete |
| `docs/.DS_Store` | Ignored File | Ignored | 0 | 0 | 0 | 无消费；仅历史提及或 ignore 规则 | 无历史价值；Finder 元数据 | Safe Delete |
| `docs/product/.DS_Store` | Ignored File | Ignored | 0 | 0 | 0 | 无消费；仅历史提及或 ignore 规则 | 无历史价值；Finder 元数据 | Safe Delete |
| `frontend/.DS_Store` | Ignored File | Ignored | 1 项提及/ignore，不消费 | 0 | 0 | 无消费；仅历史提及或 ignore 规则 | 无历史价值；Finder 元数据 | Safe Delete |
| `frontend/.next/` | Ignored Directory | Ignored | 1 项 | 1 项 | 0 | 是：当前 Next 运行时正在使用 | 构建缓存可重建，但当前 Next 开发运行时正在使用 | Protected |
| `frontend/ceo-evidence/dist/assets/` | Ignored Directory | Ignored | 0 | 0 | 0 | 是：dist/index.html 引用 /assets bundle | 构建产物可重建，但 tracked dist/index.html 当前引用该 bundle | Protected |
| `frontend/ceo-evidence/dist/index.html` | HTML Prototype | Tracked | 0 | 0 | 0 | 无外部消费；package.json 可重建 | 无独立价值；由 tsc -b && vite build 重新生成 | Safe Delete |
| `frontend/ceo-evidence/node_modules/` | Ignored Directory | Ignored | 0 | 0 | 0 | 是：CEO Evidence npm/Vite 构建依赖 | 依赖可重装，但 CEO Evidence 构建链隐式依赖 | Protected |
| `frontend/ceo-evidence/tsconfig.tsbuildinfo` | Generated Build Metadata | Tracked | 0 | 0 | 0 | 无消费；TypeScript build 可重建 | 无独立价值；TypeScript 可重新生成缓存 | Safe Delete |
| `frontend/design-spec/.DS_Store` | Ignored File | Ignored | 0 | 0 | 0 | 无消费；仅历史提及或 ignore 规则 | 无历史价值；Finder 元数据 | Safe Delete |
| `frontend/design-spec/ceo-office/.DS_Store` | Ignored File | Ignored | 0 | 0 | 0 | 无消费；仅历史提及或 ignore 规则 | 无历史价值；Finder 元数据 | Safe Delete |
| `frontend/design-spec/curis-ui-v2/docs/.DS_Store` | Ignored File | Ignored | 0 | 0 | 0 | 无消费；仅历史提及或 ignore 规则 | 无历史价值；Finder 元数据 | Safe Delete |
| `frontend/design-spec/curis-ui-v2/docs/ui/.DS_Store` | Ignored File | Ignored | 0 | 0 | 0 | 无消费；仅历史提及或 ignore 规则 | 无历史价值；Finder 元数据 | Safe Delete |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/project-miniapp-detail.png` | PNG Design Export | Tracked | 0 | 0 | 0 | 未检测到构建/部署消费 | 无独立价值；与已归档保留副本 SHA-256 完全一致 | Safe Delete |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/project-xhs-workflow-detail.png` | PNG Design Export | Tracked | 0 | 0 | 0 | 未检测到构建/部署消费 | 无独立价值；与已归档保留副本 SHA-256 完全一致 | Safe Delete |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/project-miniapp-detail.png` | PNG Design Export | Tracked | 0 | 0 | 0 | 未检测到构建/部署消费 | 无独立价值；与已归档保留副本 SHA-256 完全一致 | Safe Delete |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/project-xhs-workflow-detail.png` | PNG Design Export | Tracked | 0 | 0 | 0 | 未检测到构建/部署消费 | 无独立价值；与已归档保留副本 SHA-256 完全一致 | Safe Delete |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/project-miniapp-detail.png` | PNG Design Export | Tracked | 0 | 0 | 0 | 未检测到构建/部署消费 | 无独立价值；与已归档保留副本 SHA-256 完全一致 | Safe Delete |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/project-xhs-workflow-detail.png` | PNG Design Export | Tracked | 0 | 0 | 0 | 未检测到构建/部署消费 | 无独立价值；与已归档保留副本 SHA-256 完全一致 | Safe Delete |
| `frontend/design-spec/prototypes/` | Ignored Directory | Ignored | 0 | 0 | 0 | 未检测到构建/部署消费 | 无历史价值；目录内仅含 .DS_Store | Safe Delete |
| `frontend/node_modules/` | Ignored Directory | Ignored | 4 项 | 1 项 | 0 | 是：当前 Next 运行时正在使用 | 依赖可重装，但当前 Next 开发运行时正在使用 | Protected |
| `issues/.DS_Store` | Ignored File | Ignored | 0 | 0 | 0 | 无消费；仅历史提及或 ignore 规则 | 无历史价值；Finder 元数据 | Safe Delete |
| `tools/migrations/__pycache__/` | Ignored Directory | Ignored | 0 | 0 | 0 | 无消费；仅 ignore/缓存规则 | 无历史价值；Python 字节码缓存 | Safe Delete |
| `tools/real_rd_fixture/__pycache__/` | Ignored Directory | Ignored | 0 | 0 | 0 | 无消费；仅 ignore/缓存规则 | 无历史价值；Python 字节码缓存 | Safe Delete |

## 4. Safe Delete

Safe Delete count: 35.

This group contains:

- 8 tracked generated or byte-identical redundant assets;
- 11 Finder `.DS_Store` residue records;
- 13 pytest/Python cache records;
- 2 temporary delivery directories containing only `.DS_Store` files;
- 1 unreferenced and currently unopened runtime log.

The tracked records must use a future Git-aware deletion so their history remains
recoverable. Ignored records require no Git removal but still require explicit deletion
authorization.

## 5. Keep

Keep count: 0.

No candidate is a formal acceptance record, product decision, unique design source or
non-reproducible technical artifact. Six duplicate PNG exports have byte-identical
retained copies under `docs/99_Archive/`.

## 6. Protected

Protected count: 6.

| Path | Protection Reason | Release Condition |
| --- | --- | --- |
| `.venv/` | Official backend launcher and test history reference the environment path | Recreate and verify the official backend chain without relying on this environment |
| `backend/.venv/` | Backend tests and tools reference the environment path | Confirm replacement environment and rerun backend checks |
| `frontend/.next/` | Active Next development runtime currently uses this build state | Stop runtime and verify a clean rebuild before reconsideration |
| `frontend/node_modules/` | Active Next development runtime currently resolves dependencies here | Stop runtime and verify deterministic reinstall before reconsideration |
| `frontend/ceo-evidence/node_modules/` | CEO Evidence npm/Vite build implicitly depends on installed packages | Confirm the legacy evidence app no longer needs local build or verify reinstall |
| `frontend/ceo-evidence/dist/assets/` | Tracked `frontend/ceo-evidence/dist/index.html` references the generated bundle | Delete only as one separately approved generated-build cohort after rebuilding or retiring the app |

## 7. Duplicate Verification

All six tracked PNG Delete Candidates still match the retained Phase 3-C1 archive
copy byte for byte.

| Delete Candidate | Retained Copy | SHA-256 |
| --- | --- | --- |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/project-miniapp-detail.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/project-miniapp.png` | `ee516e9be227c2200db5dbaf4d76271036058167820281f2a86df9df792c780f` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/project-xhs-workflow-detail.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/project-xhs.png` | `0afd0b2d2f473c409d5ef20b193d9681327e85054bea3c5c2a5fa418a573c57b` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/project-miniapp-detail.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/project-miniapp.png` | `162dd8ddbe012230ef9d44a5a4d94543835e6430df8727dbc77bce058044f80a` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/project-xhs-workflow-detail.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/project-xhs.png` | `0475158ce59d431b090936be83abb798eb027bcb4d7a1f4559be9b76757dc27b` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/project-miniapp-detail.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/project-miniapp.png` | `67cc00942629d00d33d25d85cc5cbe27fa32f13fa76c0106bf70c7a50d0afbfd` |
| `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/project-xhs-workflow-detail.png` | `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/project-xhs.png` | `d44acb7e378aa4434d878c91673375f396dfb5ae10a314b3c45f5ef8595df3a1` |

## 8. Deletion Risks

- Deleting `frontend/.next/` or `frontend/node_modules/` while the
  current Next runtime is active would break the running frontend.
- Python environments are reproducible but are referenced by launch, test and
  diagnostic workflows; deletion without replacement validation can block recovery.
- `frontend/ceo-evidence/dist/assets/` is consumed by the tracked generated
  index. Treating the directory alone as safe would leave a broken evidence bundle.
- Ignored files are not recoverable from Git. A future deletion batch needs either a
  regeneration command, a content-free proof or a recoverable local backup.
- Runtime logs may contain the only copy of transient diagnostics even when they are not
  formal evidence. The current log is unopened and unreferenced, but final deletion
  should occur only after confirming no incident investigation is active.
- Static scans do not prove the absence of dynamically constructed paths.

## 9. Recommended Next Action

1. Commit this review only; do not delete candidates in the review commit.
2. If deletion is approved, open a separate deletion phase with exact targets and a
   recoverability record.
3. Process the 35 Safe Delete items in bounded cohorts: tracked generated assets,
   duplicate PNG exports, ignored metadata/caches, temporary directories, then log.
4. Stop Curis Runtime before any future cleanup that could touch runtime-generated
   locations.
5. Keep the six Protected paths unchanged until their release conditions are met.
6. Rerun Git, Markdown, script/config, Agent and build/deploy reference checks
   immediately before deletion.
7. Run product startup and focused build/test verification after any future deletion
   batch that affects generated or dependency state.

## 10. Boundary Confirmation

- Reviewed candidates present: 41 / 41
- Delete Candidates classified: 41 / 41
- Deletions executed: 0
- Moves executed: 0
- Business-code changes: 0
- Configuration changes: 0

Phase 3-C3 stops at disposition analysis and waits for explicit deletion authority.
