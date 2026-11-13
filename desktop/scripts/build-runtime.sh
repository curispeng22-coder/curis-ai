#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")/../.." && pwd)"
out="$root/desktop/.runtime"
runtime="$out/runtime"
bsk_sha256="900c85d168a4a23f19767aa918b4de4c2ae0097cd298fca3691b89843935bb58"
bsk_runtime="$runtime/workspace/_internal/vendor/browser-skill/bsk"
verify_bsk() {
  [ -f "$1" ] && [ ! -L "$1" ] && [ -x "$1" ] &&
    [ "$(/usr/bin/shasum -a 256 "$1" | /usr/bin/cut -d ' ' -f 1)" = "$bsk_sha256" ] || {
      echo "BrowserSkill v0.3.3 CLI missing or changed; provide the reviewed CURIS_BROWSER_SKILL_BINARY (no automatic download)" >&2
      exit 1
    }
}

if [[ "${CURIS_SKIP_RUNTIME_BUILD:-0}" == "1" ]]; then
  test -x "$runtime/node" && test -x "$runtime/workspace/curis-workspace" && \
    test -x "$runtime/gateway/curis-gateway" && test -x "$runtime/guardian/curis-guardian" && \
    test -x "$runtime/recovery/curis-recovery" || {
      echo "runtime output missing; cannot skip build" >&2
      exit 1
    }
  verify_bsk "$bsk_runtime"
  echo "runtime build skipped (CURIS_SKIP_RUNTIME_BUILD=1)"
  exit 0
fi
# This is a fixed build input, never a global install or remote setup command.
bsk_source="${CURIS_BROWSER_SKILL_BINARY:-$root/artifacts/tasks/CURIS-V1-EMPLOYEE-EXECUTION-CAPABILITIES-20261029/tools/browser-skill/bsk}"
verify_bsk "$bsk_source"
build_tools="${CURIS_BUILD_TOOLS:-$out/build-tools}"
python_bin="${CURIS_BUILD_PYTHON:-$root/backend/.venv/bin/python}"
[ -x "$python_bin" ] || python_bin="python3"

rm -rf "$runtime" "$out/workspace-dist" "$out/workspace-build" \
  "$out/gateway-dist" "$out/gateway-build" "$out/guardian-dist" "$out/guardian-build" \
  "$out/recovery-dist" "$out/recovery-build"
mkdir -p "$runtime/frontend" "$runtime/gateway" "$runtime/workspace" "$runtime/guardian" \
  "$runtime/recovery" "$build_tools"

echo "[1/4] build production frontend"
case "${CURIS_FRONTEND_BUNDLER:-}" in
  "") (cd "$root/frontend" && NEXT_PUBLIC_API_BASE="http://127.0.0.1:8080" pnpm build) ;;
  webpack) (cd "$root/frontend" && NEXT_PUBLIC_API_BASE="http://127.0.0.1:8080" pnpm build --webpack) ;;
  *) echo "unknown CURIS_FRONTEND_BUNDLER; use webpack or leave empty" >&2; exit 1 ;;
esac
# pnpm's standalone tree can contain dangling workspace convenience links. They
# are not runtime dependencies and would make Tauri reject the resource tree.
find "$root/frontend/.next/standalone" -type l ! -exec test -e {} \; -print -delete
cp -RL "$root/frontend/.next/standalone/." "$runtime/frontend/"
mkdir -p "$runtime/frontend/.next/static"
cp -RL "$root/frontend/.next/static/." "$runtime/frontend/.next/static/"
if [ -d "$root/frontend/public" ]; then
  cp -RL "$root/frontend/public" "$runtime/frontend/"
fi
# Keep already materialized npm dependencies. Only inspect a real pnpm store.
if [ ! -f "$runtime/frontend/node_modules/@swc/helpers/package.json" ]; then
  swc_helpers=""
  if [ -d "$runtime/frontend/node_modules/.pnpm" ]; then
    swc_helpers="$(find "$runtime/frontend/node_modules/.pnpm" -type d -path '*/@swc+helpers@*/node_modules/@swc/helpers' -print -quit)"
  fi
  if [ -n "$swc_helpers" ]; then
    mkdir -p "$runtime/frontend/node_modules/@swc"
    rm -f "$runtime/frontend/node_modules/@swc/helpers"
    cp -RL "$swc_helpers" "$runtime/frontend/node_modules/@swc/helpers"
  fi
fi
# Copy the virtual-store namespace only when it exists. An npm standalone
# already has its root runtime packages and needs no alternate namespace.
if [ -d "$runtime/frontend/node_modules/.pnpm/node_modules" ]; then
  for dependency in "$runtime/frontend/node_modules/.pnpm/node_modules/"*; do
    [ -e "$dependency" ] || continue
    dependency_name="$(basename "$dependency")"
    if [[ "$dependency_name" == @* ]]; then
      mkdir -p "$runtime/frontend/node_modules/$dependency_name"
      for scoped_dependency in "$dependency/"*; do
        [ -e "$scoped_dependency" ] || continue
        destination="$runtime/frontend/node_modules/$dependency_name/$(basename "$scoped_dependency")"
        if [ ! -e "$destination" ]; then
          cp -RL "$scoped_dependency" "$destination"
        fi
      done
    elif [ ! -e "$runtime/frontend/node_modules/$dependency_name" ]; then
      cp -RL "$dependency" "$runtime/frontend/node_modules/$dependency_name"
    fi
  done
fi
# Missing dependencies are a packaging failure, not a successful layout fix.
for required_package in next react react-dom @swc/helpers; do
  if [ ! -f "$runtime/frontend/node_modules/$required_package/package.json" ]; then
    echo "standalone runtime dependency missing: $required_package" >&2
    exit 1
  fi
done

node_bin="$(cd "$root/frontend" && pnpm exec node -p 'process.execPath')"
cp "$node_bin" "$runtime/node"
chmod 755 "$runtime/node"

echo "[2/4] build relocatable Workspace sidecar"
if ! PYTHONPATH="$build_tools" "$python_bin" -c 'import PyInstaller' >/dev/null 2>&1; then
  if [[ "${CURIS_ALLOW_BUILD_NETWORK:-0}" != "1" ]]; then
    echo "PyInstaller 6.15.0 is unavailable in CURIS_BUILD_TOOLS; refusing an implicit network install" >&2
    echo "Bootstrap explicitly with CURIS_ALLOW_BUILD_NETWORK=1, then reuse the local build-tools cache" >&2
    exit 1
  fi
  "$python_bin" -m pip install --quiet --disable-pip-version-check \
    --target "$build_tools" "pyinstaller==6.15.0"
fi
PYTHONPATH="$build_tools:$root" "$python_bin" -m PyInstaller \
  --noconfirm --clean --onedir \
  --name curis-workspace \
  --distpath "$out/workspace-dist" \
  --workpath "$out/workspace-build" \
  --specpath "$out" \
  --paths "$root" \
  --collect-submodules backend.app \
  --add-binary "$bsk_source:vendor/browser-skill" \
  --add-data "$root/backend/app/reader_runtime_lock.json:backend/app" \
  --add-data "$root/backend/app/reader_seccomp.json:backend/app" \
  --add-data "$root/backend/app/bundled_workspace_packages/writing_authoring:backend/app/bundled_workspace_packages/writing_authoring" \
  --add-data "$root/backend/app/bundled_workspace_packages/writing_authoring_release.json:backend/app/bundled_workspace_packages" \
  --add-data "$root/backend/app/bundled_workspace_packages/content_growth:backend/app/bundled_workspace_packages/content_growth" \
  --add-data "$root/backend/app/bundled_workspace_packages/content_growth_release.json:backend/app/bundled_workspace_packages" \
  --add-data "$root/backend/app/bundled_workspace_packages/music:backend/app/bundled_workspace_packages/music" \
  --add-data "$root/backend/app/bundled_workspace_packages/music_release.json:backend/app/bundled_workspace_packages" \
  --add-data "$root/docs/reviews/CURIS_LOCAL_USE_BETA_DEFINITION_ADMISSION_20261018.md:docs/reviews" \
  --add-data "$root/backend/app/bundled_workspace_packages/content_growth_v02:backend/app/bundled_workspace_packages/content_growth_v02" \
  --add-data "$root/backend/app/bundled_workspace_packages/content_growth_v02_release.json:backend/app/bundled_workspace_packages" \
  --add-data "$root/backend/app/budget_guard_config.json:backend/app" \
  --add-data "$root/backend/app/runtime_governance_config.json:backend/app" \
  --add-data "$root/backend/app/agent_execution_kernel_config.json:backend/app" \
  --add-data "$root/backend/app/ceo_evidence_api_config.json:backend/app" \
  --add-data "$root/backend/app/agent_conversion/sources:backend/app/agent_conversion/sources" \
  --hidden-import pydantic_core._pydantic_core \
  --collect-all fastapi \
  --collect-all uvicorn \
  "$root/desktop/runtime/backend_entry.py"
cp -RL "$out/workspace-dist/curis-workspace/." "$runtime/workspace/"
# PyInstaller may rewrite/sign --add-binary Mach-O inputs. This standalone tool
# must retain the reviewed official bytes required by managed_browser_tool.
[ -f "$bsk_runtime" ] && [ ! -L "$bsk_runtime" ] || {
  echo "Packaged BrowserSkill target missing or unsafe" >&2
  exit 1
}
cp "$bsk_source" "$bsk_runtime"
chmod 755 "$bsk_runtime"
verify_bsk "$bsk_runtime"

echo "[3/4] install fixed Gateway source"
PYTHONPATH="$build_tools:$root" "$python_bin" -m PyInstaller \
  --noconfirm --clean --onefile \
  --name curis-gateway \
  --distpath "$out/gateway-dist" \
  --workpath "$out/gateway-build" \
  --specpath "$out" \
  "$root/desktop/runtime/gateway.py"
cp "$out/gateway-dist/curis-gateway" "$runtime/gateway/curis-gateway"
chmod 755 "$runtime/gateway/curis-gateway"
PYTHONPATH="$build_tools:$root" "$python_bin" -m PyInstaller \
  --noconfirm --clean --onefile \
  --name curis-guardian \
  --distpath "$out/guardian-dist" \
  --workpath "$out/guardian-build" \
  --specpath "$out" \
  "$root/desktop/runtime/guardian.py"
cp "$out/guardian-dist/curis-guardian" "$runtime/guardian/curis-guardian"
chmod 755 "$runtime/guardian/curis-guardian"
PYTHONPATH="$build_tools:$root" "$python_bin" -m PyInstaller \
  --noconfirm --clean --onefile \
  --name curis-recovery \
  --distpath "$out/recovery-dist" \
  --workpath "$out/recovery-build" \
  --specpath "$out" \
  "$root/desktop/runtime/recovery.py"
cp "$out/recovery-dist/curis-recovery" "$runtime/recovery/curis-recovery"
chmod 755 "$runtime/recovery/curis-recovery"

echo "[4/4] write reproducibility manifest"
git_sha="$(git -C "$root" rev-parse HEAD 2>/dev/null || printf unknown)"
build_time="$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
cat > "$runtime/BUILD-MANIFEST.json" <<EOF
{
  "product": "Curis",
  "frontendApiBase": "http://127.0.0.1:8080",
  "frontendPort": 3010,
  "workspacePort": 8002,
  "gatewayPort": 8080,
  "browserSkillVersion": "0.3.3",
  "browserSkillBinarySha256": "$bsk_sha256",
  "gitSha": "$git_sha",
  "builtAt": "$build_time",
  "databaseRelativePath": "data/curis.sqlite"
}
EOF

echo "runtime ready: $runtime"
