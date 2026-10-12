#!/usr/bin/env python3
"""Record compact benchmark snapshots and compare benchmark history."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize(payload: dict[str, Any]) -> dict[str, Any]:
    results = payload.get("results", [])
    normalized_results: list[dict[str, Any]] = []

    for item in results:
        grade = item.get("grade", {})
        passed = item.get("pass")
        if passed is None:
            passed = grade.get("pass", False)

        score = grade.get("score")
        normalized_results.append(
            {
                "id": item.get("id"),
                "pass": bool(passed),
                "score": score if isinstance(score, (int, float)) else None,
                "primary": (
                    item.get("response", {}).get("primary_skill")
                    if isinstance(item.get("response"), dict)
                    else item.get("primary_skill")
                ),
            }
        )

    scored = [item["score"] for item in normalized_results if item["score"] is not None]
    passed_count = sum(1 for item in normalized_results if item["pass"])

    return {
        "provider": payload.get("provider"),
        "model": payload.get("model"),
        "generated_at": payload.get("generated_at"),
        "cases": len(normalized_results),
        "passed": passed_count,
        "pass_rate": round(
            (passed_count / len(normalized_results) * 100), 2
        ) if normalized_results else 0,
        "average_score": round(sum(scored) / len(scored), 2) if scored else None,
        "results": normalized_results,
    }


def command_record(args: argparse.Namespace) -> int:
    snapshot = normalize(load(Path(args.input)))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
    print(f"Recorded benchmark snapshot: {output}")
    return 0


def command_compare(args: argparse.Namespace) -> int:
    baseline = load(Path(args.baseline))
    current = load(Path(args.current))

    before = {item["id"]: item for item in baseline.get("results", [])}
    after = {item["id"]: item for item in current.get("results", [])}
    common = sorted(set(before) & set(after))

    recovered = [
        case_id for case_id in common
        if not before[case_id].get("pass") and after[case_id].get("pass")
    ]
    regressed = [
        case_id for case_id in common
        if before[case_id].get("pass") and not after[case_id].get("pass")
    ]

    score_deltas = []
    for case_id in common:
        old_score = before[case_id].get("score")
        new_score = after[case_id].get("score")
        if isinstance(old_score, (int, float)) and isinstance(new_score, (int, float)):
            delta = new_score - old_score
            if delta:
                score_deltas.append((case_id, delta))

    print(f"Pass rate: {baseline.get('pass_rate')}% -> {current.get('pass_rate')}%")
    if baseline.get("average_score") is not None or current.get("average_score") is not None:
        print(
            "Average score: "
            f"{baseline.get('average_score')} -> {current.get('average_score')}"
        )

    print(f"Recovered cases: {', '.join(recovered) if recovered else '-'}")
    print(f"Regressed cases: {', '.join(regressed) if regressed else '-'}")

    if score_deltas:
        print("Score deltas:")
        for case_id, delta in sorted(score_deltas, key=lambda item: item[1]):
            print(f"  {case_id}: {delta:+}")

    return 1 if regressed else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    record = sub.add_parser("record")
    record.add_argument("--input", required=True)
    record.add_argument("--output", required=True)
    record.set_defaults(func=command_record)

    compare = sub.add_parser("compare")
    compare.add_argument("--baseline", required=True)
    compare.add_argument("--current", required=True)
    compare.set_defaults(func=command_compare)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
