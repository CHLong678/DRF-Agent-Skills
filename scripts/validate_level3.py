#!/usr/bin/env python3
"""Validate Level-3 executable evaluation fixtures."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "evaluations" / "level3" / "fixtures"
SKILLS = {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}


def main() -> int:
    errors: list[str] = []

    if not FIXTURES.is_dir():
        print("Level-3 fixtures directory is missing", file=sys.stderr)
        return 1

    seen: set[str] = set()
    manifests = sorted(FIXTURES.glob("*/manifest.json"))

    if not manifests:
        print("No Level-3 fixtures found", file=sys.stderr)
        return 1

    for manifest_path in manifests:
        label = str(manifest_path)
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{label}: invalid JSON: {exc}")
            continue

        required = {
            "id",
            "title",
            "primary_skill",
            "task_file",
            "requirements_file",
            "verify_command",
        }
        missing = required - data.keys()
        if missing:
            errors.append(f"{label}: missing fields: {sorted(missing)}")
            continue

        fixture_id = data["id"]
        if fixture_id != manifest_path.parent.name:
            errors.append(
                f"{label}: id {fixture_id!r} must match directory {manifest_path.parent.name!r}"
            )
        if fixture_id in seen:
            errors.append(f"{label}: duplicate fixture id {fixture_id!r}")
        seen.add(fixture_id)

        if data["primary_skill"] not in SKILLS:
            errors.append(f"{label}: unknown primary_skill {data['primary_skill']!r}")

        for field in ("task_file", "requirements_file"):
            value = data[field]
            if not isinstance(value, str) or not value:
                errors.append(f"{label}: {field} must be a non-empty string")
                continue
            if not (manifest_path.parent / value).is_file():
                errors.append(f"{label}: missing {field}: {value}")

        command = data["verify_command"]
        if (
            not isinstance(command, list)
            or not command
            or not all(isinstance(part, str) and part for part in command)
        ):
            errors.append(f"{label}: verify_command must be a non-empty string list")

        task_path = manifest_path.parent / data["task_file"]
        if task_path.is_file() and len(task_path.read_text(encoding="utf-8").strip()) < 80:
            errors.append(f"{task_path}: task is too shallow")

    if errors:
        print("Level-3 validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"Validated {len(manifests)} Level-3 fixtures successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
