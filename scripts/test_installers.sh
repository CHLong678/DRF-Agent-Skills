#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EXPECTED="$(find "$ROOT/skills" -mindepth 1 -maxdepth 1 -type d -exec test -f '{}/SKILL.md' ';' -print | wc -l | tr -d ' ')"

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

CODEX_SKILLS_DIR="$tmp/codex" "$ROOT/scripts/install-codex.sh" >/dev/null
ANTIGRAVITY_SKILLS_DIR="$tmp/antigravity" "$ROOT/scripts/install-antigravity.sh" --global >/dev/null
ANTIGRAVITY_CLI_SKILLS_DIR="$tmp/antigravity-cli" "$ROOT/scripts/install-antigravity.sh" --cli-global >/dev/null

for dest in "$tmp/codex" "$tmp/antigravity" "$tmp/antigravity-cli"; do
  actual="$(find "$dest" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')"
  if [ "$actual" != "$EXPECTED" ]; then
    echo "Expected $EXPECTED installed skills in $dest, found $actual" >&2
    exit 1
  fi

  while IFS= read -r source_skill; do
    name="$(basename "$source_skill")"

    [ -f "$dest/$name/SKILL.md" ] || {
      echo "Missing installed SKILL.md for $name in $dest" >&2
      exit 1
    }

    if [ -d "$source_skill/references" ]; then
      [ -d "$dest/$name/references" ] || {
        echo "references/ not copied for $name" >&2
        exit 1
      }
    fi

    if [ -d "$source_skill/examples" ]; then
      [ -d "$dest/$name/examples" ] || {
        echo "examples/ not copied for $name" >&2
        exit 1
      }
    fi
  done < <(find "$ROOT/skills" -mindepth 1 -maxdepth 1 -type d -exec test -f '{}/SKILL.md' ';' -print | sort)
done

echo "Installer tests passed for $EXPECTED skills."
