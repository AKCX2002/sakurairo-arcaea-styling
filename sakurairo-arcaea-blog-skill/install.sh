#!/usr/bin/env bash
set -euo pipefail
SKILL_NAME='sakurairo-arcaea-blog-skill'
DEST="${HERMES_HOME:-$HOME/.hermes}/skills/${SKILL_NAME}"
source_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
staging=''
cleanup() { if [ -n "$staging" ] && [ -d "$staging" ]; then rm -rf -- "$staging"; fi; }
trap cleanup EXIT
if [ ! -f "$source_dir/SKILL.md" ]; then
    staging="$(mktemp -d -t sakurairo-skill.XXXXXX)"
    git clone --quiet --depth 1 https://github.com/AKCX2002/sakurairo-arcaea-styling.git "$staging/repo"
    source_dir="$staging/repo/$SKILL_NAME"
fi
mkdir -p "$DEST"
for item in SKILL.md README.md LICENSE references scripts; do
    if [ -e "$source_dir/$item" ]; then cp -R -- "$source_dir/$item" "$DEST/"; fi
done
printf 'Installed %s to %s\n' "$SKILL_NAME" "$DEST"
