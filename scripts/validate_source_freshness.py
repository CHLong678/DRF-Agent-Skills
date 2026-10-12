#!/usr/bin/env python3
"""Validate compatibility/source metadata and review freshness."""

from __future__ import annotations

import datetime as dt
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "metadata" / "compatibility-sources.json"
SKILLS = {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}
MONTH_RE = re.compile(r"^(\d{4})-(0[1-9]|1[0-2])$")


def month_age(reviewed: str, today: dt.date) -> int:
    year, month = map(int, reviewed.split("-"))
    return (today.year - year) * 12 + (today.month - month)


def main() -> int:
    errors: list[str] = []

    try:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Source registry error: {exc}", file=sys.stderr)
        return 1

    stale_after = int(data.get("review_policy", {}).get("stale_after_months", 12))
    today = dt.datetime.now(dt.timezone.utc).date()

    skills = data.get("skills", {})
    if not isinstance(skills, dict):
        errors.append("registry.skills must be an object")
        skills = {}

    for skill, meta in skills.items():
        if skill not in SKILLS:
            errors.append(f"unknown skill in source registry: {skill}")
            continue

        sources = meta.get("sources", [])
        if not isinstance(sources, list) or not sources:
            errors.append(f"{skill}: sources must be a non-empty list")
            continue

        for index, source in enumerate(sources):
            label = f"{skill}.sources[{index}]"
            if not isinstance(source, dict):
                errors.append(f"{label}: source must be an object")
                continue

            for field in ("name", "authority", "reviewed"):
                if not str(source.get(field, "")).strip():
                    errors.append(f"{label}: missing {field}")

            reviewed = str(source.get("reviewed", ""))
            if reviewed and not MONTH_RE.match(reviewed):
                errors.append(f"{label}: reviewed must be YYYY-MM")
            elif reviewed and month_age(reviewed, today) > stale_after:
                errors.append(
                    f"{label}: source review is stale ({reviewed}); "
                    f"refresh required after {stale_after} months"
                )

    if errors:
        print("Source freshness validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(
        f"Validated source freshness for {len(skills)} version-sensitive skills "
        f"(stale after {stale_after} months)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
