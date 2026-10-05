#!/usr/bin/env python3
"""Validate DRF-Agent-Skills repository structure without third-party dependencies."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"

FRONTMATTER_RE = re.compile(r"\A---\n(?P<body>.*?)\n---\n", re.DOTALL)
LOCAL_REF_RE = re.compile(r"`((?:references|examples)/[^`]+)`")
ROUTING_SECTIONS = (
    "## Routing contract",
    "### Use this skill when",
    "### Do not use this skill when",
    "### Inspect first",
    "### Related skills",
)


def parse_frontmatter(text: str, path: Path) -> dict[str, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError(f"{path}: missing YAML-style frontmatter")

    data: dict[str, str] = {}
    for raw_line in match.group("body").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"{path}: unsupported frontmatter line: {raw_line!r}")
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_file = skill_dir / "SKILL.md"

    if not skill_file.is_file():
        return [f"{skill_dir}: missing SKILL.md"]

    text = skill_file.read_text(encoding="utf-8")

    try:
        frontmatter = parse_frontmatter(text, skill_file)
    except ValueError as exc:
        return [str(exc)]

    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")

    if not name:
        errors.append(f"{skill_file}: frontmatter.name is required")
    elif name != skill_dir.name:
        errors.append(
            f"{skill_file}: frontmatter.name={name!r} must match directory {skill_dir.name!r}"
        )

    if not description:
        errors.append(f"{skill_file}: frontmatter.description is required")
    elif len(description) < 30:
        errors.append(f"{skill_file}: description is too short to drive reliable skill discovery")

    if "Use when" not in description:
        errors.append(f"{skill_file}: description should include a 'Use when ...' trigger clause")

    for section in ROUTING_SECTIONS:
        if section not in text:
            errors.append(f"{skill_file}: missing required routing section: {section}")

    for relative in LOCAL_REF_RE.findall(text):
        target = skill_dir / relative
        if not target.exists():
            errors.append(f"{skill_file}: local reference does not exist: {relative}")

    for folder in ("references", "examples"):
        subdir = skill_dir / folder
        if subdir.exists() and not any(subdir.iterdir()):
            errors.append(f"{subdir}: directory exists but is empty")

    return errors


def main() -> int:
    errors: list[str] = []

    if not SKILLS_DIR.is_dir():
        print("ERROR: skills directory not found", file=sys.stderr)
        return 1

    skill_dirs = sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir())

    if not skill_dirs:
        print("ERROR: no skills found", file=sys.stderr)
        return 1

    seen_names: set[str] = set()

    for skill_dir in skill_dirs:
        errors.extend(validate_skill(skill_dir))

        skill_file = skill_dir / "SKILL.md"
        if skill_file.is_file():
            try:
                name = parse_frontmatter(
                    skill_file.read_text(encoding="utf-8"), skill_file
                ).get("name")
            except ValueError:
                name = None
            if name:
                if name in seen_names:
                    errors.append(f"duplicate skill name: {name}")
                seen_names.add(name)

    if errors:
        print("Skill validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"Validated {len(skill_dirs)} skills successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
