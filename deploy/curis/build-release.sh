#!/usr/bin/env bash
set -euo pipefail

version="${1:?用法: $0 <版本号> }"
root="$(cd "$(dirname "$0")/../.." && pwd)"
out="$root/deploy/curis/releases/$version"

rm -rf "$out"
mkdir -p "$out/workspace" "$out/backend"

(cd "$root/frontend" && pnpm build)

cp -R "$root/frontend/.next" "$out/workspace/"
cp "$root/frontend/package.json" "$root/frontend/pnpm-lock.yaml" "$out/workspace/"
cp -R "$root/backend/app" "$out/backend/"
cp "$root/deploy/curis/workspace.env.example" "$out/workspace.env.example"
cp "$root/deploy/curis/run-workspace-backend.sh" "$out/backend/"

printf '发布包已生成: %s\n' "$out"
