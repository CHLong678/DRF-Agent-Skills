#!/usr/bin/env python3
"""Integration smoke tests for unified multi-agent installer."""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts/install-agents.py"
AGENTS = {
    "codex": (".codex/skills", ".codex/skills"),
    "antigravity": (".agents/skills", ".gemini/config/skills"),
    "claude-code": (".claude/skills", ".claude/skills"),
    "cursor": (".cursor/skills", ".cursor/skills"),
    "github-copilot": (".github/skills", ".copilot/skills"),
    "opencode": (".opencode/skills", ".config/opencode/skills"),
}

def run(*args: str, env: dict[str, str], expect: int = 0) -> subprocess.CompletedProcess[str]:
    result = subprocess.run([sys.executable, str(INSTALLER), *args],
                            text=True, capture_output=True, env=env)
    if result.returncode != expect:
        raise AssertionError(
            f"exit {result.returncode} != {expect}: {result.stdout} {result.stderr}"
        )
    return result

def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        home = base / "home"
        home.mkdir()
        project = base / "project"
        project.mkdir()
        env = {**os.environ, "HOME": str(home)}
        # Path.home() uses HOME on Unix CI.
        for agent, (project_path, global_path) in AGENTS.items():
            for scope, target_root in (
                ("project", project / project_path),
                ("global", home / global_path),
            ):
                args = ["--agent", agent, "--scope", scope,
                        "--project", str(project), "--skill", "drf-celery"]
                run(*args, "--dry-run", env=env)
                assert not (target_root / "drf-celery").exists()
                run(*args, env=env)
                target = target_root / "drf-celery"
                assert (target / "SKILL.md").is_file()
                assert (target / "agents/openai.yaml").is_file()
                assert (target / ".drf-agent-skills-install.json").is_file()
                run(*args, env=env)  # idempotent owned update

        cli_args = ["--agent", "antigravity", "--scope", "cli-global", "--skill", "drf-celery"]
        run(*cli_args, env=env)
        assert (home / ".gemini/antigravity-cli/skills/drf-celery/SKILL.md").is_file()
        run("--agent", "cursor", "--scope", "cli-global", env=env, expect=2)

        unowned = project / ".cursor/skills/drf-testing"
        unowned.mkdir(parents=True)
        (unowned / "user.txt").write_text("preserve", encoding="utf-8")
        args = ["--agent", "cursor", "--scope", "project", "--project", str(project),
                "--skill", "drf-testing"]
        run(*args, env=env, expect=2)
        assert (unowned / "user.txt").read_text() == "preserve"
        run(*args, "--force", env=env)
        assert (unowned / "SKILL.md").exists()
        assert not (unowned / "user.txt").exists()

        run("--agent", "all", "--scope", "project", "--project", str(project),
            "--skill", "drf-orm-performance", env=env)
        for agent, (project_path, _) in AGENTS.items():
            assert (project / project_path / "drf-orm-performance/SKILL.md").is_file(), agent
    print("Unified installer tests passed for six agents plus Antigravity CLI.")

if __name__ == "__main__":
    main()
