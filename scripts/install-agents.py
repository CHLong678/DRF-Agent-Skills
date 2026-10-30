#!/usr/bin/env python3
"""Install shared Agent Skills into supported coding-agent directories.

Uses the Python standard library only. Never deletes unowned target directories.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKER = ".drf-agent-skills-install.json"
AGENTS = {
    "codex": (".codex/skills", ".codex/skills"),
    "antigravity": (".agents/skills", ".gemini/config/skills"),
    "claude-code": (".claude/skills", ".claude/skills"),
    "cursor": (".cursor/skills", ".cursor/skills"),
    "github-copilot": (".github/skills", ".copilot/skills"),
    "opencode": (".opencode/skills", ".config/opencode/skills"),
}

def destination(agent: str, scope: str, project: Path) -> Path:
    local, global_path = AGENTS[agent]
    return project.resolve() / local if scope == "project" else Path.home() / global_path

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", choices=[*AGENTS, "all"], required=True)
    parser.add_argument("--scope", choices=["project", "global"], default="project")
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--skill", action="append", default=[], help="Install only named skill (repeatable)")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true", help="Replace pre-existing unowned skill dirs")
    args = parser.parse_args()

    source_root = ROOT / "skills"
    available = {p.name: p for p in sorted(source_root.iterdir())
                 if p.is_dir() and (p / "SKILL.md").is_file()}
    missing = sorted(set(args.skill) - set(available))
    if missing:
        parser.error("Unknown skills: " + ", ".join(missing))
    selected = sorted(set(args.skill)) if args.skill else sorted(available)
    agents = sorted(AGENTS) if args.agent == "all" else [args.agent]

    if args.scope == "project" and not args.project.is_dir():
        parser.error("Project directory does not exist: " + str(args.project))

    plan = [(agent, destination(agent, args.scope, args.project), name)
            for agent in agents for name in selected]

    # Preflight all conflicts before modifying anything.
    conflicts = []
    for agent, root, name in plan:
        target = root / name
        if target.exists() or target.is_symlink():
            marker = target / MARKER if target.is_dir() and not target.is_symlink() else None
            owned = marker is not None and marker.is_file()
            if not owned and not args.force:
                conflicts.append(str(target))
    if conflicts:
        print("Refusing to replace pre-existing, unowned skill paths:", file=sys.stderr)
        for path in conflicts:
            print("  " + path, file=sys.stderr)
        print("Use --force only if replacing those paths is intentional.", file=sys.stderr)
        return 2

    for agent, root, name in plan:
        target = root / name
        action = "would install" if args.dry_run else "installed"
        if args.dry_run:
            print(f"{action}: {agent}: {name} -> {target}")
            continue
        root.mkdir(parents=True, exist_ok=True)
        staging = Path(tempfile.mkdtemp(prefix=".drf-skill-", dir=root))
        try:
            shutil.copytree(available[name], staging / name)
            candidate = staging / name
            (candidate / MARKER).write_text(
                json.dumps({"managed_by": "DRF-Agent-Skills", "skill": name, "agent": agent}) + "\n",
                encoding="utf-8",
            )
            if target.exists() or target.is_symlink():
                if target.is_symlink() or target.is_file():
                    target.unlink()
                else:
                    shutil.rmtree(target)
            candidate.rename(target)
            print(f"{action}: {agent}: {name} -> {target}")
        finally:
            shutil.rmtree(staging, ignore_errors=True)
    print(f"Completed {len(plan)} skill installations.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
