#!/usr/bin/env bash
set -euo pipefail

version="${1:?用法: $0 <备份版本目录> }"
root="$(cd "$(dirname "$0")/../.." && pwd)"
backup="$root/deploy/curis/releases/$version"

[ -d "$backup" ] || { echo "找不到发布备份: $backup" >&2; exit 1; }
printf '可回滚发布包: %s\n' "$backup"
printf '数据库回滚需从 data/migration-backups/ 或指定快照恢复；本脚本不覆盖活动数据库。\n'
