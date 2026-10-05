#!/usr/bin/env python3
"""Run routing cases against Codex CLI or Antigravity CLI."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CASES_FILE = ROOT / "evaluations" / "routing-cases.json"
SCHEMA_FILE = ROOT / "evaluations" / "model" / "response.schema.json"
TAXONOMY_FILE = ROOT / "evaluations" / "model" / "reasoning-taxonomy.json"
RESULTS_DIR = ROOT / "evaluations" / "results"

PROVIDERS = {"codex", "antigravity"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def build_prompt(case: dict[str, Any], taxonomy: list[str]) -> str:
    taxonomy_text = ", ".join(taxonomy)
    return f"""You are evaluating DRF-Agent-Skills routing behavior.

Repository instructions:
- Read AGENTS.md and ROUTING.md.
- Read only the minimum SKILL.md/reference files needed to route this task.
- Do not edit files.
- Do not run destructive or write commands.
- Choose exactly one primary skill.
- Secondary skills are optional and must be materially relevant.
- Separate observed task facts from assumptions.
- Do not reveal private chain-of-thought. Return only concise decision artifacts.

Task:
{case["prompt"]}

Return one JSON object with exactly these fields:
- primary_skill: string
- secondary_skills: array of skill names
- inspect_first: array of concrete things the agent should inspect before changing code
- decision_summary: short explanation of why the primary skill owns the task
- reasoning_tags: zero or more tags chosen only from this taxonomy: {taxonomy_text}
- compatibility_notes: array of version/runtime checks relevant to this task
- verification: array of concrete checks that would verify the eventual recommendation

Return JSON only, with no markdown fence and no prose before or after it.
"""


def extract_json_object(text: str) -> dict[str, Any]:
    stripped = text.strip()
    try:
        value = json.loads(stripped)
        if isinstance(value, dict):
            return value
    except json.JSONDecodeError:
        pass

    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", stripped, re.DOTALL)
    if fenced:
        return json.loads(fenced.group(1))

    start = stripped.find("{")
    end = stripped.rfind("}")
    if start >= 0 and end > start:
        value = json.loads(stripped[start : end + 1])
        if isinstance(value, dict):
            return value

    raise ValueError("Could not extract a JSON object from model output")


def run_codex(prompt: str, model: str | None, timeout: int, work_dir: Path) -> tuple[dict[str, Any], str]:
    answer_file = work_dir / "codex-answer.json"
    args = [
        "codex",
        "exec",
        "--sandbox",
        "read-only",
        "--ask-for-approval",
        "never",
        "--output-schema",
        str(SCHEMA_FILE),
        "--output-last-message",
        str(answer_file),
    ]
    if model:
        args.extend(["--model", model])
    args.append("-")

    result = subprocess.run(
        args,
        input=prompt,
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )

    raw = answer_file.read_text(encoding="utf-8") if answer_file.exists() else result.stdout
    if result.returncode != 0:
        raise RuntimeError(
            f"codex exited {result.returncode}: {result.stderr.strip() or result.stdout.strip()}"
        )
    return extract_json_object(raw), result.stderr


def run_antigravity(prompt: str, model: str | None, timeout: int) -> tuple[dict[str, Any], str]:
    args = ["agy", "-p", prompt]
    if model:
        args.extend(["--model", model])

    result = subprocess.run(
        args,
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"agy exited {result.returncode}: {result.stderr.strip() or result.stdout.strip()}"
        )
    return extract_json_object(result.stdout), result.stderr


def validate_response_shape(response: dict[str, Any], known_skills: set[str], taxonomy: set[str]) -> list[str]:
    errors: list[str] = []
    required = {
        "primary_skill": str,
        "secondary_skills": list,
        "inspect_first": list,
        "decision_summary": str,
        "reasoning_tags": list,
        "compatibility_notes": list,
        "verification": list,
    }
    for field, expected_type in required.items():
        if field not in response:
            errors.append(f"missing field: {field}")
        elif not isinstance(response[field], expected_type):
            errors.append(f"{field} must be {expected_type.__name__}")

    primary = response.get("primary_skill")
    if isinstance(primary, str) and primary not in known_skills:
        errors.append(f"unknown primary skill: {primary}")

    for skill in response.get("secondary_skills", []):
        if skill not in known_skills:
            errors.append(f"unknown secondary skill: {skill}")

    for tag in response.get("reasoning_tags", []):
        if tag not in taxonomy:
            errors.append(f"unknown reasoning tag: {tag}")

    return errors


def grade(case: dict[str, Any], response: dict[str, Any], shape_errors: list[str]) -> dict[str, Any]:
    primary = response.get("primary_skill")
    secondary = response.get("secondary_skills", [])
    tags = set(response.get("reasoning_tags", []))

    expected_primary = case["expected_primary"]
    allowed_secondary = set(case.get("allowed_secondary", []))
    forbidden_primary = set(case.get("forbidden_primary", []))
    required_tags = set(case.get("required_reasoning_tags", []))

    checks: list[dict[str, Any]] = []
    score = 0

    primary_ok = primary == expected_primary
    checks.append({"id": "primary", "pass": primary_ok, "notes": f"expected={expected_primary}, actual={primary}"})
    if primary_ok:
        score += 50

    forbidden_ok = primary not in forbidden_primary
    checks.append({"id": "forbidden-primary", "pass": forbidden_ok, "notes": f"forbidden={sorted(forbidden_primary)}"})
    if forbidden_ok:
        score += 15

    unexpected_secondary = set(secondary) - allowed_secondary
    secondary_ok = not unexpected_secondary
    checks.append({
        "id": "secondary",
        "pass": secondary_ok,
        "notes": f"allowed={sorted(allowed_secondary)}, unexpected={sorted(unexpected_secondary)}",
    })
    if secondary_ok:
        score += 10

    inspect_ok = bool(response.get("inspect_first"))
    checks.append({"id": "inspect-first", "pass": inspect_ok, "notes": f"count={len(response.get('inspect_first', []))}"})
    if inspect_ok:
        score += 10

    verification_ok = bool(response.get("verification"))
    checks.append({"id": "verification", "pass": verification_ok, "notes": f"count={len(response.get('verification', []))}"})
    if verification_ok:
        score += 10

    tags_ok = required_tags.issubset(tags)
    checks.append({
        "id": "reasoning-tags",
        "pass": tags_ok,
        "notes": f"required={sorted(required_tags)}, actual={sorted(tags)}",
    })
    if tags_ok:
        score += 5

    shape_ok = not shape_errors
    checks.append({"id": "response-shape", "pass": shape_ok, "notes": "; ".join(shape_errors) if shape_errors else "valid"})
    if not shape_ok:
        score = min(score, 60)

    return {
        "pass": primary_ok and forbidden_ok and secondary_ok and tags_ok and shape_ok,
        "score": score,
        "checks": checks,
    }


def known_skills() -> set[str]:
    return {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}


def select_cases(cases: list[dict[str, Any]], ids: list[str], limit: int | None) -> list[dict[str, Any]]:
    if ids:
        wanted = set(ids)
        selected = [case for case in cases if case["id"] in wanted]
        missing = wanted - {case["id"] for case in selected}
        if missing:
            raise ValueError(f"Unknown case ids: {sorted(missing)}")
    else:
        selected = cases

    if limit is not None:
        selected = selected[:limit]
    return selected


def write_reports(provider: str, model: str | None, results: list[dict[str, Any]]) -> tuple[Path, Path]:
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = RESULTS_DIR / provider
    out_dir.mkdir(parents=True, exist_ok=True)

    payload = {
        "provider": provider,
        "model": model,
        "generated_at": timestamp,
        "summary": {
            "cases": len(results),
            "passed": sum(1 for item in results if item["grade"]["pass"]),
            "average_score": round(
                sum(item["grade"]["score"] for item in results) / len(results), 2
            ) if results else 0,
        },
        "results": results,
    }

    json_path = out_dir / f"{timestamp}.json"
    md_path = out_dir / f"{timestamp}.md"
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        f"# Model Eval Report: {provider}",
        "",
        f"- Model: {model or 'CLI default'}",
        f"- Cases: {payload['summary']['cases']}",
        f"- Passed: {payload['summary']['passed']}",
        f"- Average score: {payload['summary']['average_score']}",
        "",
        "| Case | Primary | Score | Result |",
        "|---|---|---:|---|",
    ]
    for item in results:
        mark = "PASS" if item["grade"]["pass"] else "FAIL"
        lines.append(
            f"| {item['id']} | {item.get('response', {}).get('primary_skill', 'ERROR')} | "
            f"{item['grade']['score']} | {mark} |"
        )
    lines.append("")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, md_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", choices=sorted(PROVIDERS), required=True)
    parser.add_argument("--model")
    parser.add_argument("--case", action="append", default=[])
    parser.add_argument("--limit", type=int)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    cases = select_cases(load_json(CASES_FILE), args.case, args.limit)
    taxonomy = load_json(TAXONOMY_FILE)["tags"]
    skills = known_skills()
    results: list[dict[str, Any]] = []

    for case in cases:
        prompt = build_prompt(case, taxonomy)
        if args.dry_run:
            print(f"===== {case['id']} =====")
            print(prompt)
            continue

        work_dir = ROOT / ".eval-tmp" / case["id"]
        work_dir.mkdir(parents=True, exist_ok=True)

        try:
            if args.provider == "codex":
                response, stderr = run_codex(prompt, args.model, args.timeout, work_dir)
            else:
                response, stderr = run_antigravity(prompt, args.model, args.timeout)

            shape_errors = validate_response_shape(response, skills, set(taxonomy))
            result = {
                "id": case["id"],
                "expected_primary": case["expected_primary"],
                "response": response,
                "grade": grade(case, response, shape_errors),
                "stderr": stderr.strip(),
            }
        except Exception as exc:
            result = {
                "id": case["id"],
                "expected_primary": case["expected_primary"],
                "response": {},
                "grade": {
                    "pass": False,
                    "score": 0,
                    "checks": [{"id": "execution", "pass": False, "notes": str(exc)}],
                },
                "error": str(exc),
            }

        results.append(result)
        print(
            f"{case['id']}: score={result['grade']['score']} "
            f"{'PASS' if result['grade']['pass'] else 'FAIL'}"
        )

    if args.dry_run:
        return 0

    json_path, md_path = write_reports(args.provider, args.model, results)
    print(f"JSON report: {json_path}")
    print(f"Markdown report: {md_path}")

    return 0 if all(item["grade"]["pass"] for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
