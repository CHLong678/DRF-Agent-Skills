#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODE="${1:-}"

case "$MODE" in
  --project)
    PROJECT="${2:-.}"
    DEST="$(cd "$PROJECT" && pwd)/.agents/skills"
    ;;
  --global)
    DEST="${ANTIGRAVITY_SKILLS_DIR:-$HOME/.gemini/config/skills}"
    ;;
  --cli-global)
    DEST="${ANTIGRAVITY_CLI_SKILLS_DIR:-$HOME/.gemini/antigravity-cli/skills}"
    ;;
  *)
    echo "Usage: $0 --project <project-path> | --global | --cli-global" >&2
    exit 2
    ;;
esac

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
