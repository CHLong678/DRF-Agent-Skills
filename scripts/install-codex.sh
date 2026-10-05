#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${CODEX_SKILLS_DIR:-$HOME/.codex/skills}"

mkdir -p "$DEST"

found=0
for skill in "$ROOT"/skills/*; do
  [ -d "$skill" ] || continue
  [ -f "$skill/SKILL.md" ] || continue

  found=1
  name="$(basename "$skill")"
  rm -rf "$DEST/$name"
  cp -R "$skill" "$DEST/$name"
  echo "installed $name -> $DEST/$name"
done

if [ "$found" -eq 0 ]; then
  echo "No skills with SKILL.md found under $ROOT/skills" >&2
  exit 1
fi
