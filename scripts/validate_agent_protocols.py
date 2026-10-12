#!/usr/bin/env python3
"""Validate repository-level agent operating protocols."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = {
    "CODEBASE_INSPECTION.md": (
        "# Codebase Inspection Protocol",
        "## 1. Establish runtime and compatibility",
        "## 3. Search all callers before moving logic",
        "## 4. Identify invariants and contracts",
        "## 8. Verify blast radius after editing",
    ),
    "CHANGE_RISK.md": (
        "# Backend Change Risk Classification",
        "## LOW",
        "## MEDIUM",
        "## HIGH",
        "## CRITICAL",
        "## Risk multipliers",
    ),
    "SKILL_COMPOSITION.md": (
        "# Skill Composition",
        "## Production async export",
        "## Cross-system write + event",
        "## Tenant-safe cached list API",
        "## Composition stop rule",
    ),
}


def main() -> int:
    errors: list[str] = []

    for filename, markers in REQUIRED.items():
        path = ROOT / filename
        if not path.is_file():
            errors.append(f"{filename}: missing")
            continue

        text = path.read_text(encoding="utf-8")
        if len(text.strip()) < 1000:
            errors.append(f"{filename}: document is too shallow")

        for marker in markers:
            if marker not in text:
                errors.append(f"{filename}: missing required section {marker!r}")

    if errors:
        print("Agent protocol validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"Validated {len(REQUIRED)} agent operating protocols successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
