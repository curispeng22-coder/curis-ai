#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
version="${VERSION:-0.1.0}"
app="${1:-$root/target/release/bundle/macos/Curis.app}"
output="${2:-$root/target/release/bundle/dmg/Curis_${version}_manual_aarch64.dmg}"
test -d "$app" || { echo "app not found: $app" >&2; exit 1; }
mkdir -p "$(dirname "$output")"
stage="$(mktemp -d /tmp/curis-dmg-stage.XXXX)"
trap 'rm -rf "$stage"' EXIT
cp -R "$app" "$stage/Curis.app"
hdiutil create -volname Curis -srcfolder "$stage" -ov -format UDZO "$output"
shasum -a 256 "$output"
