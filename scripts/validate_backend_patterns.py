#!/usr/bin/env python3
"""Validate the framework-neutral backend-pattern knowledge layer."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = ROOT / "backend-patterns"

REQUIRED_FILES = {
    "README.md",
    "SOURCES.md",
    "resilience.md",
    "event-driven-consistency.md",
    "capacity-scaling.md",
    "service-module-boundaries.md",
    "production-runtime.md",
}

REQUIRED_TITLES = {
    "resilience.md": "# Resilience Patterns",
    "event-driven-consistency.md": "# Event-driven Consistency Patterns",
    "capacity-scaling.md": "# Capacity and Scaling Patterns",
    "service-module-boundaries.md": "# Service and Module Boundaries",
    "production-runtime.md": "# Production Runtime Patterns",
}


def main() -> int:
    errors: list[str] = []

    if not PATTERNS.is_dir():
        print("backend-patterns directory is missing", file=sys.stderr)
        return 1

    actual = {path.name for path in PATTERNS.iterdir() if path.is_file()}
    missing = REQUIRED_FILES - actual
    if missing:
        errors.append(f"missing backend pattern files: {sorted(missing)}")

    for filename, title in REQUIRED_TITLES.items():
        path = PATTERNS / filename
        if not path.is_file():
            continue

        text = path.read_text(encoding="utf-8")

        if title not in text:
            errors.append(f"{path}: missing title {title!r}")

        if len(text.strip()) < 500:
            errors.append(f"{path}: pattern document is too shallow")

    sources = PATTERNS / "SOURCES.md"
    if sources.is_file():
        text = sources.read_text(encoding="utf-8")
        for source in (
            "donnemartin/system-design-primer",
            "ByteByteGoHq/system-design-101",
            "binhnguyennus/awesome-scalability",
            "HackSoftware/Django-Styleguide",
            "Sairyss/domain-driven-hexagon",
            "cookiecutter/cookiecutter-django",
        ):
            if source not in text:
                errors.append(f"{sources}: missing source/adaptation note for {source}")

    if errors:
        print("Backend-pattern validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"Validated {len(REQUIRED_TITLES)} backend pattern documents successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
