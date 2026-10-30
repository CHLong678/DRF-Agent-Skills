#!/usr/bin/env python3
"""Export a minimal Community release without copying Git history.

Fail closed: only declared skill folders and explicitly public top-level files.
Never performs remote Git operations.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "publishing" / "community.json"

def export(dest: Path) -> None:
    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    names = data["skills"]
    if len(names) != 7 or len(names) != len(set(names)):
        raise ValueError("Community allowlist must contain exactly 7 unique skills")
    if dest.exists():
        raise FileExistsError(f"Destination already exists: {dest}; choose a new, empty path")
    for name in names:
        if not isinstance(name, str) or name in {".", ".."} or "/" in name or "\\" in name:
            raise ValueError(f"Unsafe skill name: {name!r}")
        directory = ROOT / "skills" / name
        if not (directory / "SKILL.md").is_file() or directory.is_symlink():
            raise ValueError(f"Unknown or unsafe skill: {name}")

    for filename in data["root_files"]:
        if filename != "LICENSE":
            raise ValueError(f"Unapproved public root file: {filename}")

    dest.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".community-export-", dir=dest.parent) as temporary:
        stage = Path(temporary) / "release"
        (stage / "skills").mkdir(parents=True)
        for name in names:
            source = ROOT / "skills" / name
            if any(p.is_symlink() for p in source.rglob("*")):
                raise ValueError(f"Symlink in skill content: {name}")
            shutil.copytree(source, stage / "skills" / name)
        for filename in data["root_files"]:
            shutil.copy2(ROOT / filename, stage / filename)

        # Deliver one self-contained installer, never the developer tooling.
        shutil.copytree(ROOT / "publishing" / "community-installer", stage / "scripts")
        (stage / "README.md").write_text(
            "# DRF Agent Skills — Community Edition\n\n"
            "Seven free Django REST Framework agent skills for Codex, Antigravity, "
            "Claude Code, Cursor, GitHub Copilot and OpenCode.\n\n"
            "## Install\n\n"
            "From this repository, run:\n\n"
            "\x60\x60\x60bash\n"
            "python3 scripts/install-agents.py --agent all --scope project --project /path/to/django-project\n"
            "\x60\x60\x60\n\n"
            "You can also select one agent with --agent or use --scope global.\n\n"
            "This public edition contains only seven curated skills. "
            "The development repository and its history are not included.\n",
            encoding="utf-8",
        )
        (stage / "COMMUNITY_SKILLS.json").write_text(
            json.dumps({"skills": names}, indent=2) + "\n", encoding="utf-8"
        )
        stage.rename(dest)

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        export(args.output.resolve())
    except (ValueError, FileExistsError, OSError, KeyError) as error:
        print(f"Export failed: {error}", file=sys.stderr)
        return 1
    print(f"Community export created: {args.output.resolve()}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
