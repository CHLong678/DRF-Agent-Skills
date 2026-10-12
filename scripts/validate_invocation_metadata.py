#!/usr/bin/env python3
"""Validate skill invocation metadata and Codex UI metadata."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"

FRONTMATTER_RE = re.compile(r"\A---\n(?P<body>.*?)\n---\n", re.DOTALL)

EXPECTED_USER_INVOKED = {
    "backend-agent-retro",
    "drf-skill-router",
}


def parse_frontmatter(text: str, path: Path) -> dict[str, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError(f"{path}: missing frontmatter")

    data: dict[str, str] = {}
    for raw in match.group("body").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"{path}: unsupported frontmatter line: {raw!r}")
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def parse_openai_yaml(text: str) -> dict[str, object]:
    result: dict[str, object] = {}
    section: str | None = None

    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue

        indent = len(raw) - len(raw.lstrip())
        line = raw.strip()

        if indent == 0 and line.endswith(":"):
            section = line[:-1]
            result.setdefault(section, {})
            continue

        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        value = value.strip().strip('"').strip("'")

        if section and indent > 0:
            child = result.setdefault(section, {})
            if isinstance(child, dict):
                child[key.strip()] = value
        else:
            result[key.strip()] = value

    return result


def main() -> int:
    errors: list[str] = []
    skill_dirs = sorted(path for path in SKILLS.iterdir() if path.is_dir())

    actual_user_invoked: set[str] = set()

    for skill_dir in skill_dirs:
        skill_file = skill_dir / "SKILL.md"
        metadata_file = skill_dir / "agents" / "openai.yaml"

        if not skill_file.is_file():
            continue

        try:
            fm = parse_frontmatter(skill_file.read_text(encoding="utf-8"), skill_file)
        except ValueError as exc:
            errors.append(str(exc))
            continue

        user_invoked = fm.get("disable-model-invocation", "").lower() == "true"
        if user_invoked:
            actual_user_invoked.add(skill_dir.name)

        if not metadata_file.is_file():
            errors.append(f"{metadata_file}: missing")
            continue

        metadata = parse_openai_yaml(metadata_file.read_text(encoding="utf-8"))
        interface = metadata.get("interface")

        if not isinstance(interface, dict):
            errors.append(f"{metadata_file}: missing interface section")
        else:
            display = str(interface.get("display_name", "")).strip()
            short = str(interface.get("short_description", "")).strip()
            if not display:
                errors.append(f"{metadata_file}: interface.display_name is required")
            if not short:
                errors.append(f"{metadata_file}: interface.short_description is required")
            elif len(short) > 100:
                errors.append(f"{metadata_file}: short_description should stay concise")

        policy = metadata.get("policy")
        implicit_disabled = (
            isinstance(policy, dict)
            and str(policy.get("allow_implicit_invocation", "")).lower() == "false"
        )

        if user_invoked and not implicit_disabled:
            errors.append(
                f"{metadata_file}: user-invoked skill must set "
                "policy.allow_implicit_invocation: false"
            )
        if not user_invoked and implicit_disabled:
            errors.append(
                f"{metadata_file}: model-invoked skill must not disable implicit invocation"
            )

        description = fm.get("description", "")
        if user_invoked and "Use when" in description:
            errors.append(
                f"{skill_file}: user-invoked description should be human-facing, "
                "not contain model trigger wording"
            )

    if actual_user_invoked != EXPECTED_USER_INVOKED:
        errors.append(
            "user-invoked skill registry mismatch: "
            f"expected={sorted(EXPECTED_USER_INVOKED)}, "
            f"actual={sorted(actual_user_invoked)}"
        )

    if errors:
        print("Invocation metadata validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(
        f"Validated invocation metadata for {len(skill_dirs)} skills "
        f"({len(actual_user_invoked)} user-invoked)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
