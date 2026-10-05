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

## Routing contract

Every `SKILL.md` must include:

```markdown
## Routing contract

### Use this skill when
...

### Do not use this skill when
...

### Inspect first
...

### Related skills
...
```

The purpose is to reduce overlap between skills. Write explicit negative routing rules for the most likely neighboring skills.

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

## Evaluation coverage

When a new skill overlaps an existing skill or changes routing behavior:

1. add/update at least one case in `evaluations/routing-cases.json`
2. set one expected primary skill
3. list only materially useful secondary skills
4. add plausible wrong primary skills to `forbidden_primary`
5. add a scenario under `scenarios/` when the behavior is important enough to require a reasoning fixture

For substantial implementation/review skills, reference the relevant contract from `OUTPUT_CONTRACTS.md` or define an equally concrete skill-specific output structure.

## Validation

Before pushing:

```bash
python scripts/validate_skills.py
python scripts/validate_evaluations.py
bash -n scripts/install-codex.sh
bash -n scripts/install-antigravity.sh
bash scripts/test_installers.sh
python -m compileall -q skills
```

CI runs the same checks.
