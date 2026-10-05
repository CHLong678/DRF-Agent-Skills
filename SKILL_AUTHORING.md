# Skill Authoring Guide

Use this guide when adding or changing skills in this repository.

## Directory contract

Each skill is self-contained:

```text
skills/<skill-name>/
├── SKILL.md
├── references/      # optional deep guidance
└── examples/        # optional copyable examples
```

`SKILL.md` is the discovery/decision entrypoint. Keep deep material in references so agents only load it when relevant.

## Required frontmatter

```yaml
---
name: drf-example
description: Explain what the skill covers. Use when the agent is doing a concrete class of work.
---
```

Rules:

- `name` must match the directory name.
- `description` must be specific enough for skill discovery.
- Include a clear `Use when ...` trigger.
- Avoid generic descriptions such as "Django best practices."

## Compatibility

Repository baseline:

- Django >= 3.2
- Celery >= 5.0 when Celery is used
- DRF version compatible with the installed Django version

If a recommendation requires a newer version:

1. state the minimum version
2. provide a baseline-compatible fallback where practical
3. tell the agent to inspect the project's installed versions first

## SKILL.md content

Prefer:

- decision rules
- when/when-not-to-use guidance
- correctness invariants
- links to local references
- compatibility gates

Move long explanations, edge cases, large examples, and implementation recipes into `references/` or `examples/`.

## Examples

Examples should:

- be minimal
- illustrate one non-obvious pattern
- avoid project-specific names unless clearly placeholders
- avoid secrets/credentials
- avoid requiring a newer Django/Celery API without a version note

## Validation

Before pushing:

```bash
python scripts/validate_skills.py
bash -n scripts/install-codex.sh
bash -n scripts/install-antigravity.sh
bash scripts/test_installers.sh
python -m compileall -q skills
```

CI runs the same checks.
