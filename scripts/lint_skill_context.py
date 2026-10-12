#!/usr/bin/env python3
"""Lint skill descriptions and source-of-truth duplication risks."""

from __future__ import annotations

import itertools
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"

FRONTMATTER_RE = re.compile(r"\A---\n(?P<body>.*?)\n---\n", re.DOTALL)
WORD_RE = re.compile(r"[a-z0-9][a-z0-9_-]+", re.IGNORECASE)

STOP = {
    "the","and","for","with","when","use","using","into","from","this","that",
    "django","drf","rest","framework","guidance","api","backend","design","or",
    "a","an","of","to","in","on","is","are","be","by","as","at","it",
}

MAX_DESCRIPTION_CHARS = 360
MAX_DESCRIPTION_WORDS = 55
MAX_PAIR_SIMILARITY = 0.72


def parse_frontmatter(text: str) -> dict[str, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    data: dict[str, str] = {}
    for raw in match.group("body").splitlines():
        if ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def tokens(text: str) -> set[str]:
    return {
        word.lower()
        for word in WORD_RE.findall(text)
        if len(word) >= 3 and word.lower() not in STOP
    }


def similarity(a: str, b: str) -> float:
    ta, tb = tokens(a), tokens(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def normalized_paragraphs(text: str) -> set[str]:
    paragraphs: set[str] = set()
    for paragraph in re.split(r"\n\s*\n", text):
        plain = paragraph.replace(chr(96), "")
        plain = re.sub(r"[*_>#-]", "", plain).strip().lower()
        plain = re.sub(r"\s+", " ", plain)
        if len(plain) >= 180:
            paragraphs.add(plain)
    return paragraphs


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    descriptions: dict[str, str] = {}
    skill_texts: dict[str, str] = {}

    for skill_file in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        name = skill_file.parent.name
        text = skill_file.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        description = fm.get("description", "")
        descriptions[name] = description
        skill_texts[name] = text

        if len(description) > MAX_DESCRIPTION_CHARS:
            errors.append(
                f"{name}: description has {len(description)} chars; "
                f"limit is {MAX_DESCRIPTION_CHARS}"
            )

        word_count = len(description.split())
        if word_count > MAX_DESCRIPTION_WORDS:
            errors.append(
                f"{name}: description has {word_count} words; "
                f"limit is {MAX_DESCRIPTION_WORDS}"
            )

    for (name_a, desc_a), (name_b, desc_b) in itertools.combinations(descriptions.items(), 2):
        score = similarity(desc_a, desc_b)
        if score >= MAX_PAIR_SIMILARITY:
            warnings.append(
                f"description overlap {score:.2f}: {name_a} <-> {name_b}"
            )

    paragraphs: dict[str, list[str]] = {}
    for name, text in skill_texts.items():
        for paragraph in normalized_paragraphs(text):
            paragraphs.setdefault(paragraph, []).append(name)

    for paragraph, names in paragraphs.items():
        unique = sorted(set(names))
        if len(unique) >= 2:
            warnings.append(
                "possible duplicated long paragraph across skills: "
                + ", ".join(unique)
            )

    if errors:
        print("Context-budget lint failed:")
        for error in errors:
            print(f"  - {error}")
        if warnings:
            print("Warnings:")
            for warning in warnings[:30]:
                print(f"  - {warning}")
        return 1

    print(
        f"Context-budget lint passed for {len(descriptions)} skills "
        f"with {len(warnings)} warning(s)."
    )
    for warning in warnings[:30]:
        print(f"  - warning: {warning}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
