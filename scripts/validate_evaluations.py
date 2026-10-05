#!/usr/bin/env python3
"""Validate routing evaluations and real-world scenarios."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
EVAL_FILE = ROOT / "evaluations" / "routing-cases.json"
SCENARIOS_DIR = ROOT / "scenarios"
TAXONOMY_FILE = ROOT / "evaluations" / "model" / "reasoning-taxonomy.json"

SKILL_NAME_RE = re.compile(r"skills/([^/]+)/SKILL\.md$")


def skill_names() -> set[str]:
    names: set[str] = set()
    for path in SKILLS_DIR.glob("*/SKILL.md"):
        names.add(path.parent.name)
    return names


def validate_routing_cases(skills: set[str]) -> list[str]:
    errors: list[str] = []

    if not EVAL_FILE.is_file():
        return [f"{EVAL_FILE}: missing"]

    try:
        cases = json.loads(EVAL_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{EVAL_FILE}: invalid JSON: {exc}"]

    if not isinstance(cases, list) or not cases:
        return [f"{EVAL_FILE}: expected non-empty JSON array"]

    seen_ids: set[str] = set()

    required = {
        "id",
        "prompt",
        "expected_primary",
        "allowed_secondary",
        "forbidden_primary",
        "rationale",
        "required_reasoning_tags",
    }

    for index, case in enumerate(cases):
        label = f"{EVAL_FILE}[{index}]"

        if not isinstance(case, dict):
            errors.append(f"{label}: expected object")
            continue

        missing = required - case.keys()
        if missing:
            errors.append(f"{label}: missing fields: {sorted(missing)}")
            continue

        case_id = case["id"]
        if not isinstance(case_id, str) or not case_id.strip():
            errors.append(f"{label}: id must be non-empty string")
        elif case_id in seen_ids:
            errors.append(f"{label}: duplicate id: {case_id}")
        else:
            seen_ids.add(case_id)

        for field in ("prompt", "rationale"):
            if not isinstance(case[field], str) or len(case[field].strip()) < 20:
                errors.append(f"{label}: {field} is too short")

        primary = case["expected_primary"]
        if primary not in skills:
            errors.append(f"{label}: unknown expected_primary: {primary}")

        for field in ("allowed_secondary", "forbidden_primary"):
            value = case[field]
            if not isinstance(value, list):
                errors.append(f"{label}: {field} must be a list")
                continue
            if len(value) != len(set(value)):
                errors.append(f"{label}: duplicate skills in {field}")
            for skill in value:
                if skill not in skills:
                    errors.append(f"{label}: unknown skill in {field}: {skill}")

        if primary in case.get("allowed_secondary", []):
            errors.append(f"{label}: expected_primary cannot also be allowed_secondary")

        if primary in case.get("forbidden_primary", []):
            errors.append(f"{label}: expected_primary cannot also be forbidden_primary")

        overlap = set(case.get("allowed_secondary", [])) & set(case.get("forbidden_primary", []))
        if overlap:
            errors.append(f"{label}: skill appears in both allowed_secondary and forbidden_primary: {sorted(overlap)}")

        required_tags = case.get("required_reasoning_tags", [])
        if not isinstance(required_tags, list):
            errors.append(f"{label}: required_reasoning_tags must be a list")
        else:
            taxonomy = set(load_taxonomy())
            unknown_tags = set(required_tags) - taxonomy
            if unknown_tags:
                errors.append(f"{label}: unknown reasoning tags: {sorted(unknown_tags)}")

    return errors


def extract_named_skills(text: str) -> set[str]:
    found: set[str] = set()
    for match in re.findall(r"`([a-z0-9][a-z0-9-]+)`", text):
        if match.startswith("drf-") or match.startswith("django-") or match == "postgresql-for-django":
            found.add(match)
    return found


def load_taxonomy() -> list[str]:
    if not TAXONOMY_FILE.is_file():
        return []
    data = json.loads(TAXONOMY_FILE.read_text(encoding="utf-8"))
    return data.get("tags", [])


def validate_scenarios(skills: set[str]) -> list[str]:
    errors: list[str] = []

    if not SCENARIOS_DIR.is_dir():
        return [f"{SCENARIOS_DIR}: missing"]

    scenario_files = sorted(SCENARIOS_DIR.glob("*/README.md"))
    if not scenario_files:
        return [f"{SCENARIOS_DIR}: no scenario README files found"]

    required_sections = (
        "# Scenario:",
        "## Symptom",
        "## Expected reasoning",
        "## Primary skill",
    )

    for path in scenario_files:
        text = path.read_text(encoding="utf-8")

        for section in required_sections:
            if section not in text:
                errors.append(f"{path}: missing section marker: {section}")

        named = extract_named_skills(text)
        for skill in named:
            if skill not in skills:
                errors.append(f"{path}: references unknown skill: {skill}")

    return errors


def main() -> int:
    skills = skill_names()
    errors = validate_routing_cases(skills)
    errors.extend(validate_scenarios(skills))

    if errors:
        print("Evaluation validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    case_count = len(json.loads(EVAL_FILE.read_text(encoding="utf-8")))
    scenario_count = len(list(SCENARIOS_DIR.glob("*/README.md")))
    print(
        f"Validated {case_count} routing cases and "
        f"{scenario_count} real-world scenarios successfully."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
