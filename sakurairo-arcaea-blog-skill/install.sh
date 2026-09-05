#!/usr/bin/env bash
set -euo pipefail

SKILL_NAME="sakurairo-arcaea-blog-skill"
REPO="AKCX2002/${SKILL_NAME}"
DEST="${HERMES_HOME:-$HOME/.hermes}/skills/${SKILL_NAME}"

echo "📦 Installing ${SKILL_NAME}..."

# Ensure target dir exists
mkdir -p "$DEST"

# Download via curl or git clone
if command -v git &>/dev/null; then
  echo " → Cloning from GitHub..."
  git clone --depth 1 "https://github.com/${REPO}.git" /tmp/${SKILL_NAME} 2>/dev/null
  cp /tmp/${SKILL_NAME}/SKILL.md "$DEST/"
  cp /tmp/${SKILL_NAME}/README.md "$DEST/" 2>/dev/null || true
  rm -rf /tmp/${SKILL_NAME}
else
  echo " → Downloading release zip..."
  curl -sL "https://github.com/${REPO}/releases/latest/download/${SKILL_NAME}.zip" \
    -o /tmp/${SKILL_NAME}.zip
  unzip -o /tmp/${SKILL_NAME}.zip -d "$DEST/" >/dev/null 2>&1
  rm -f /tmp/${SKILL_NAME}.zip
fi

echo "✅ Installed to: ${DEST}/SKILL.md"
echo ""
echo "📖 To use, load the skill in Hermes:"
echo "   skill_view(name=\"${SKILL_NAME}\")"
