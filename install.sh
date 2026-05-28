#!/usr/bin/env bash
set -euo pipefail

SKILL_NAME="sakurairo-theme"
REPO="AKCX2002/${SKILL_NAME}"
DEST="${CODEKX_HOME:-$HOME/.agents}/skills/${SKILL_NAME}"

echo "📦 Installing ${SKILL_NAME}..."

mkdir -p "$DEST"

if command -v git &>/dev/null; then
  echo " → Cloning from GitHub..."
  git clone --depth 1 "https://github.com/${REPO}.git" /tmp/${SKILL_NAME}
  cp -r /tmp/${SKILL_NAME}/* "$DEST/"
  rm -rf /tmp/${SKILL_NAME}
else
  echo " → Downloading tarball..."
  curl -sL "https://github.com/${REPO}/releases/latest/download/${SKILL_NAME}.tar.gz" \
    -o /tmp/${SKILL_NAME}.tar.gz
  tar xzf /tmp/${SKILL_NAME}.tar.gz -C "$DEST/"
  rm -f /tmp/${SKILL_NAME}.tar.gz
fi

echo "✅ Installed to: ${DEST}/SKILL.md"
echo ""
echo "📖 To use:"
echo "   skill_view(name=\"${SKILL_NAME}\")"
