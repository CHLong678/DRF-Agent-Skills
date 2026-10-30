#!/usr/bin/env python3
"""Validate that Community export is allowlisted and contains no repository history."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "publishing/community.json"

def main() -> None:
    expected = set(json.loads(CONFIG.read_text(encoding="utf-8"))["skills"])
    assert len(expected) == 7

    with tempfile.TemporaryDirectory() as tmp:
        output = Path(tmp) / "community"
        subprocess.run(
            [sys.executable, str(ROOT / "scripts/export-community.py"), "--output", str(output)],
            check=True, capture_output=True, text=True,
        )
        actual = {p.name for p in (output / "skills").iterdir()}
        assert actual == expected, (actual, expected)

        allowed_root = {"README.md", "LICENSE", "COMMUNITY_SKILLS.json", "skills", "scripts"}
        root_names = {p.name for p in output.iterdir()}
        assert root_names == allowed_root, root_names

        allowed_scripts = {"install-agents.py"}
        assert {p.name for p in (output / "scripts").iterdir()} == allowed_scripts

        for path in output.rglob("*"):
            assert not path.is_symlink(), path
            assert ".git" not in path.parts, path
            assert "evaluations" not in path.parts, path
            assert "metadata" not in path.parts, path
            assert "publishing" not in path.parts, path

        for name in expected:
            assert (output / "skills" / name / "SKILL.md").is_file()
            assert (output / "skills" / name / "agents" / "openai.yaml").is_file()

        project = Path(tmp) / "consumer"
        project.mkdir()
        subprocess.run(
            [sys.executable, str(output / "scripts/install-agents.py"),
             "--agent", "all", "--scope", "project", "--project", str(project)],
            check=True, capture_output=True, text=True,
        )
        for agent_dir in (
            ".codex/skills", ".agents/skills", ".claude/skills",
            ".cursor/skills", ".github/skills", ".opencode/skills"
        ):
            installed = {p.name for p in (project / agent_dir).iterdir()}
            assert installed == expected, (agent_dir, installed)
    print("Community export and six-agent installation passed (7 public skills only).")

if __name__ == "__main__":
    main()
