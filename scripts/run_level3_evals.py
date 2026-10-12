#!/usr/bin/env python3
"""Run executable Django/DRF fixtures against Codex or Antigravity."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURES_ROOT = ROOT / "evaluations" / "level3" / "fixtures"
RESULTS_ROOT = ROOT / "evaluations" / "results" / "level3"

GUIDANCE_FILES = (
    "AGENTS.md",
    "ROUTING.md",
    "CODEBASE_INSPECTION.md",
    "CHANGE_RISK.md",
    "SKILL_COMPOSITION.md",
    "OUTPUT_CONTRACTS.md",
)


def load_manifest(fixture_dir: Path) -> dict[str, Any]:
    return json.loads((fixture_dir / "manifest.json").read_text(encoding="utf-8"))


def fixture_dirs(selected: list[str]) -> list[Path]:
    all_dirs = sorted(path.parent for path in FIXTURES_ROOT.glob("*/manifest.json"))
    if not selected:
        return all_dirs

    wanted = set(selected)
    chosen = [path for path in all_dirs if path.name in wanted]
    missing = wanted - {path.name for path in chosen}
    if missing:
        raise ValueError(f"Unknown fixtures: {sorted(missing)}")
    return chosen


def copy_guidance(workdir: Path) -> None:
    target = workdir / ".eval-guidance"
    target.mkdir(parents=True, exist_ok=True)
    for name in GUIDANCE_FILES:
        source = ROOT / name
        if source.is_file():
            shutil.copy2(source, target / name)


def build_prompt(workdir: Path, manifest: dict[str, Any]) -> str:
    task = (workdir / manifest["task_file"]).read_text(encoding="utf-8")
    return f"""You are running an executable backend engineering evaluation.

Work only inside this fixture workspace.

Before editing:
1. Read .eval-guidance/AGENTS.md.
2. Read .eval-guidance/CODEBASE_INSPECTION.md.
3. Read .eval-guidance/CHANGE_RISK.md.
4. Read .eval-guidance/ROUTING.md as needed.
5. Inspect the fixture code and tests.

Expected primary skill: {manifest["primary_skill"]}

Task:
{task}

Requirements:
- Fix the actual implementation; do not weaken/delete tests.
- Keep the change minimal.
- Preserve public behavior unless the task explicitly requires a change.
- Run the fixture verification tests if possible.
- Do not modify files outside this workspace.
"""


def setup_venv(workdir: Path, requirements_file: str) -> Path:
    venv = workdir / ".venv"
    subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True)
    python = venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    subprocess.run(
        [str(python), "-m", "pip", "install", "-q", "-r", requirements_file],
        cwd=workdir,
        check=True,
    )
    return python


def run_codex(workdir: Path, prompt: str, model: str | None, timeout: int) -> subprocess.CompletedProcess[str]:
    args = [
        "codex",
        "exec",
        "--sandbox",
        "workspace-write",
        "--ask-for-approval",
        "never",
    ]
    if model:
        args.extend(["--model", model])
    args.append("-")
    return subprocess.run(
        args,
        input=prompt,
        cwd=workdir,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )


def run_antigravity(workdir: Path, prompt: str, model: str | None, timeout: int) -> subprocess.CompletedProcess[str]:
    args = ["agy", "-p", prompt]
    if model:
        args.extend(["--model", model])
    return subprocess.run(
        args,
        cwd=workdir,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )


def verification_command(
    manifest: dict[str, Any],
    python: Path | None,
) -> list[str]:
    command = list(manifest["verify_command"])
    if python is not None and command and command[0] == "python":
        command[0] = str(python)
    return command


def run_one(
    source: Path,
    provider: str,
    model: str | None,
    timeout: int,
    setup: bool,
    dry_run: bool,
    keep_workdir: bool,
) -> dict[str, Any]:
    manifest = load_manifest(source)

    if dry_run:
        return {
            "id": manifest["id"],
            "primary_skill": manifest["primary_skill"],
            "dry_run": True,
            "verify_command": manifest["verify_command"],
        }

    base = Path(tempfile.mkdtemp(prefix=f"drf-agent-eval-{manifest['id']}-"))
    workdir = base / manifest["id"]
    shutil.copytree(source, workdir)
    copy_guidance(workdir)

    python: Path | None = None
    setup_error: str | None = None
    agent_result: subprocess.CompletedProcess[str] | None = None
    verify_result: subprocess.CompletedProcess[str] | None = None

    try:
        if setup:
            try:
                python = setup_venv(workdir, manifest["requirements_file"])
            except Exception as exc:
                setup_error = str(exc)

        if setup_error is None:
            prompt = build_prompt(workdir, manifest)
            if provider == "codex":
                agent_result = run_codex(workdir, prompt, model, timeout)
            else:
                agent_result = run_antigravity(workdir, prompt, model, timeout)

            command = verification_command(manifest, python)
            verify_result = subprocess.run(
                command,
                cwd=workdir,
                text=True,
                capture_output=True,
                timeout=timeout,
                check=False,
            )

        passed = (
            setup_error is None
            and agent_result is not None
            and agent_result.returncode == 0
            and verify_result is not None
            and verify_result.returncode == 0
        )

        return {
            "id": manifest["id"],
            "primary_skill": manifest["primary_skill"],
            "pass": passed,
            "workdir": str(workdir) if keep_workdir else None,
            "setup_error": setup_error,
            "agent_returncode": None if agent_result is None else agent_result.returncode,
            "agent_stdout": "" if agent_result is None else agent_result.stdout[-12000:],
            "agent_stderr": "" if agent_result is None else agent_result.stderr[-12000:],
            "verify_returncode": None if verify_result is None else verify_result.returncode,
            "verify_stdout": "" if verify_result is None else verify_result.stdout[-12000:],
            "verify_stderr": "" if verify_result is None else verify_result.stderr[-12000:],
        }
    finally:
        if not keep_workdir:
            shutil.rmtree(base, ignore_errors=True)


def write_report(provider: str, model: str | None, results: list[dict[str, Any]]) -> tuple[Path, Path]:
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = RESULTS_ROOT / provider
    out_dir.mkdir(parents=True, exist_ok=True)

    payload = {
        "provider": provider,
        "model": model,
        "generated_at": timestamp,
        "summary": {
            "fixtures": len(results),
            "passed": sum(1 for result in results if result.get("pass")),
        },
        "results": results,
    }

    json_path = out_dir / f"{timestamp}.json"
    md_path = out_dir / f"{timestamp}.md"

    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    lines = [
        f"# Level-3 Eval: {provider}",
        "",
        f"- Model: {model or 'CLI default'}",
        f"- Fixtures: {len(results)}",
        f"- Passed: {payload['summary']['passed']}",
        "",
        "| Fixture | Primary skill | Result |",
        "|---|---|---|",
    ]
    for result in results:
        status = "PASS" if result.get("pass") else "FAIL"
        lines.append(f"| {result['id']} | {result['primary_skill']} | {status} |")
    lines.append("")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, md_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", choices=("codex", "antigravity"), required=True)
    parser.add_argument("--model")
    parser.add_argument("--fixture", action="append", default=[])
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--setup", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--keep-workdir", action="store_true")
    args = parser.parse_args()

    selected = fixture_dirs(args.fixture)
    results = [
        run_one(
            fixture,
            args.provider,
            args.model,
            args.timeout,
            args.setup,
            args.dry_run,
            args.keep_workdir,
        )
        for fixture in selected
    ]

    if args.dry_run:
        for result in results:
            print(
                f"{result['id']}: primary={result['primary_skill']} "
                f"verify={' '.join(result['verify_command'])}"
            )
        return 0

    json_path, md_path = write_report(args.provider, args.model, results)
    print(f"JSON report: {json_path}")
    print(f"Markdown report: {md_path}")

    return 0 if all(result.get("pass") for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
