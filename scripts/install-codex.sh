#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${CODEX_SKILLS_DIR:-$HOME/.codex/skills}"

mkdir -p "$DEST"
for skill in "$ROOT"/skills/drf-*; do
  name="$(basename "$skill")"
  rm -rf "$DEST/$name"
  cp -R "$skill" "$DEST/$name"
  echo "installed $name -> $DEST/$name"
done
