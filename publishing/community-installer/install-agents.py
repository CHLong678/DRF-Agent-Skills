#!/usr/bin/env python3
"""Install public DRF Agent Skills into supported AI coding agents."""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
PATHS = {
    "codex": (".codex/skills", ".codex/skills"),
    "antigravity": (".agents/skills", ".gemini/config/skills"),
    "claude-code": (".claude/skills", ".claude/skills"),
    "cursor": (".cursor/skills", ".cursor/skills"),
    "github-copilot": (".github/skills", ".copilot/skills"),
    "opencode": (".opencode/skills", ".config/opencode/skills"),
}

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", choices=[*PATHS, "all"], required=True)
    parser.add_argument("--scope", choices=["project", "global"], default="project")
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    skills = sorted(p for p in (BASE / "skills").iterdir() if (p / "SKILL.md").is_file())
    agents = PATHS if args.agent == "all" else [args.agent]
    for agent in agents:
        project_dir, global_dir = PATHS[agent]
        dest = (
            args.project.resolve() / project_dir
            if args.scope == "project" else Path.home() / global_dir
        )
        for source in skills:
            target = dest / source.name
            if target.exists():
                print(f"Refusing to overwrite existing path: {target}", file=sys.stderr)
                return 2
    for agent in agents:
        project_dir, global_dir = PATHS[agent]
        dest = (
            args.project.resolve() / project_dir
            if args.scope == "project" else Path.home() / global_dir
        )
        for source in skills:
            target = dest / source.name
            print(f"{'Would install' if args.dry_run else 'Installing'} {source.name} -> {target}")
            if not args.dry_run:
                dest.mkdir(parents=True, exist_ok=True)
                shutil.copytree(source, target)
    return 0

if __name__ == "__main__":
    sys.exit(main())
