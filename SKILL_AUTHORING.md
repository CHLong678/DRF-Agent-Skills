# Skill Authoring Guide

Use this guide when adding or changing skills in this repository.

## Directory contract

Each skill is self-contained:

```text
skills/<skill-name>/
├── SKILL.md
├── agents/
│   └── openai.yaml
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

## Source freshness

When a skill depends on version-sensitive framework/database/provider behavior, register its authoritative sources in `metadata/compatibility-sources.json` and keep the review date current.

Community repositories may supply patterns, but official/provider documentation owns compatibility claims.

## Compatibility

Repository baseline:

- Django >= 3.2
- Celery >= 5.0 when Celery is used
- DRF version compatible with the installed Django version

If a recommendation requires a newer version:

1. state the minimum version
2. provide a baseline-compatible fallback where practical
3. tell the agent to inspect the project's installed versions first

## Invocation metadata

Every skill must contain `agents/openai.yaml` with:

```yaml
interface:
  display_name: "Human-readable name"
  short_description: "Concise picker description"
```

Model-invoked skills omit the policy block.

User-invoked skills must set both:

- `disable-model-invocation: true` in `SKILL.md`
- `policy.allow_implicit_invocation: false` in `agents/openai.yaml`

See `AUTHORING/INVOCATION.md`.

## Context budget

Descriptions are always-on routing context. Keep them concise and let `scripts/lint_skill_context.py` flag excessive length or suspicious overlap.

Do not duplicate long pattern explanations across skills; link to the authoritative backend-pattern/reference instead.

## Context pointers

Treat frontmatter descriptions as routing pointers. Model-invoked skills need concrete `Use when ...` trigger language; user-invoked skill descriptions remain human-facing.

See `AUTHORING/CONTEXT_POINTERS.md`.

## Completion criteria

Every `SKILL.md` must include an observable `## Completion criteria` section.

See `AUTHORING/COMPLETION_CRITERIA.md`.

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

## Codebase and risk integration

For implementation-oriented skills:

- `Inspect first` should align with `CODEBASE_INSPECTION.md`.
- Call out HIGH/CRITICAL failure modes when the skill commonly touches security, tenant isolation, money, migrations, concurrency, cross-system consistency, or irreversible repair.
- Do not force a risk level for trivial/local changes.

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
python scripts/validate_invocation_metadata.py
python scripts/validate_source_freshness.py
python scripts/lint_skill_context.py
python scripts/validate_evaluations.py
python scripts/validate_backend_patterns.py
python scripts/validate_agent_protocols.py
python scripts/validate_level3.py
python scripts/test_multi_agent_installer.py
python -m compileall -q skills
```

CI runs the same checks.


## Scope governance

Before adding a new skill, read `SCOPE.md` and `.out-of-scope/README.md`.

Prefer deepening an existing skill/reference/playbook/eval over adding another top-level skill unless a distinct routing boundary is demonstrated.
