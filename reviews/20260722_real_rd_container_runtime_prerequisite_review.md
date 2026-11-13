# RealRD Container Runtime Prerequisite Review

- Issue: `issues/20260722_real_rd_container_runtime_prerequisite.md`
- Delivery SHA: `8ca63ce7a9676e0091eca3c4f121c4e99fc31414`
- Image: `sha256:a2cf1625d09024946338f6d57f8240885cfc273275dff56fa579b8351f59d066`
- Verdict: `PASS_WITH_NOTE`

## Initial verification at `900e90b5`

- Commit scope is exactly `deploy/curis/gateway/Dockerfile.workspace` and `backend/app/real_rd_executor.py`; `git diff-tree --check` passed.
- Image inspection confirms Python `3.14.6`, Git `2.47.3`, and registered argv prefix `/usr/local/bin/python`.
- Image history confirms the sole added APT source is `snapshot.debian.org/archive/debian/20260713T000000Z`, suite `trixie`, component `main`, with Git pinned to `1:2.47.3-0+deb13u1`.
- Comparing the pinned base image and rebuilt image produced exactly 31 added dpkg packages; canonical SHA-256 is `62effd872607d28da1240d1e59279f81620b52675db8c23c8ff573fbe64d7bce`.
- Delivery SBOM evidence reports 145 components and SHA-256 `8c7ac86d…9344`.
- The fixed command was independently rerun with `--network none`: `2 failed in 0.04s`, exit `1`. Both failures have the same cause: `/srv/curis/tools/real_rd_fixture/target_b.py` is absent.
- Compose build context is exactly `../../../backend`; the image contains the fixed test file under `/srv/curis/backend/tests/` but cannot contain the repository-root `tools/` fixture without a separately approved build-context or copy-boundary change.

## Historical conclusion at `900e90b5`

The runtime pin and controlled rebuild evidence pass. The Issue remains `BLOCKED` because its required original registered command cannot run in the rebuilt image.

Unique blocker: the approved backend-only build context excludes `tools/real_rd_fixture/target_b.py`, while host mounting is forbidden.

## Follow-up: named-context attempt

- Delivery reported that standalone Docker Compose `5.3.1` parsed `additional_contexts`, but execution stopped before build because the Docker `buildx` plugin is unavailable; classic builder cannot consume the named context.
- Quality confirmed HEAD remains `900e90b5e676af39698bfcc0d6cef2c396e71f36`, image remains `sha256:c33cdfbdb32d21dc2829e342142b1a33f4982dc2d71492b2b0bc91e21e70c919`, `docker-compose` is `5.3.1`, and `docker buildx` is unavailable.
- No rebuild or commit occurred and the attempted changes were reverted. The existing missing-target blocker is unchanged; resolving the buildx/build-context boundary requires 总控裁决.

## Final classic-builder verification at `8ca63ce7`

- Commit scope is exactly `.dockerignore`, `deploy/curis/gateway/Dockerfile.workspace`, and `deploy/curis/gateway/docker-compose.yml`; diff-check passed.
- The deny-all context independently enumerates 242 files and 2,974,324 bytes: 238 backend files, two fixture files, and two control files. No symlink, socket, hidden backend file, credential suffix, environment file, SQLite file, or `.git` entry is admitted.
- Image root contains only `.git`, `backend`, and `tools`. Host and image independently produced the same 240-source content manifest hash; no unrelated repository-root content is present.
- Fixture SHA-256 values are `1aaa9920392fb936b5395ac7aa0d493681e3dc1058291568976c14617f85bfe6` and `be64fef6f130c4d7a5b415499ef9ac22f8862a4a315644fdd517e0d335761e03`; the Gate manifest remains `1bf4f2e722b6ac0cfd1b5f49aa75c72138109cdc7315713b72876ad45224c3b9`.
- Git root is `/srv/curis`; tree `108a076d183918526dc2416b8dbc84fd26a6687e`, commit `4aaf1acbea7f4e91bdb76270f99c4af6983ab385`, deterministic author/committer and timestamp match, and only the two fixture files are tracked.
- Python `3.14.6`, Git `2.47.3`, and fixed argv `/usr/local/bin/python -m pytest -q backend/tests/test_real_rd_fixture_b.py` match.
- The fixed command was independently run with `--network none`: exit `1`, two expected assertion failures, and no `FileNotFoundError`, `ModuleNotFoundError`, or `PermissionError`. The missing-target blocker is resolved while the intentionally failing fixture pre-state is preserved.
- Delivery SBOM evidence reports 145 components and SHA-256 `8c7ac86d0cb9117bb6f566dc2eb4a1cd4b4338cd694a41e6754efdac94c09344`.

### Note

`git status --porcelain` reports the copied `backend/` directory as untracked, so the delivery word `clean` is accurate only for the tracked fixture diff/index, not for the entire repository status. This does not affect the current RealRD path because git diff and diff-check are restricted to the approved fixture paths.

## Final conclusion

The classic-builder deny-all image resolves the only runtime blocker. This prerequisite Issue passes with the Git-status wording correction above; no execution blocker remains in this Issue.

No Key, model call, service startup, RealRD write, or runtime network access was used during Quality verification.

Next Seat: 产品规划席（返回既有 RealRD 单次取证 Gate）。

Handoff: sent to 产品规划席
