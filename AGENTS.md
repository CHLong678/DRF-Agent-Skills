# Agent instructions

This repository contains reusable DRF skills for Codex and Antigravity.

Compatibility baseline:

- Django >= 3.2
- Celery >= 5.0 when Celery is used
- DRF version compatible with the installed Django version

Before using version-sensitive APIs, inspect the actual Django, DRF, Celery, Python, database, and relevant third-party package versions.

Routing requirements:

- Read `ROUTING.md` when multiple skills overlap.
- Choose one primary skill; add secondary skills only when they materially affect correctness.
- Prefer the most specific skill once the problem domain is known.
- If the root cause is unknown, start with the diagnostic skill instead of guessing a fix.
- Respect each skill's `Routing contract`: Use when, Do not use, Inspect first, and Related skills.
- Use playbooks for common cross-cutting investigations rather than loading every related skill.

Output requirements:

- Use `OUTPUT_CONTRACTS.md` for performance/debugging, security, concurrency, background processing, migration, and code-review tasks.
- Separate observed evidence from hypotheses.
- If the root cause is not established, say what must be measured instead of presenting a guess as fact.
- State compatibility/version constraints for version-sensitive recommendations.
- End substantial implementation/debugging advice with a concrete verification method.

If versions are unknown, prefer Django 3.2 / Celery 5.0-compatible patterns. Newer features must be version-gated with a fallback.

When editing a skill:

- Keep the skill focused on Django REST Framework.
- Prefer production-safe rules over tutorial shortcuts.
- Distinguish correctness requirements from optional architectural preferences.
- Do not recommend an abstraction solely because it is fashionable.
- Preserve compatibility with Django >= 3.2 and Celery >= 5.0.
- Treat PostgreSQL transaction and locking behavior explicitly.
- Avoid rules that imply every query field needs an index.
- Avoid serializer validation side effects.
- Avoid unnecessary modern Python syntax unless the project runtime supports it.
- Add examples only when they clarify a non-obvious rule.
- Keep YAML front matter `name` and `description` precise because they drive skill discovery.

See `COMPATIBILITY.md` for version gates.


Evaluation assets:

- `evaluations/routing-cases.json` defines expected primary/secondary routing behavior.
- `scenarios/` contains real-world reasoning fixtures.
- Changes to routing or skill scope should update these assets when behavior changes.


Model-eval behavior:

- `evaluations/model/` defines the structured response schema and reasoning-tag taxonomy.
- `scripts/run_model_evals.py` runs real Codex/Antigravity CLI routing evaluations.
- Do not optimize a skill solely to game one eval case; preserve the underlying routing invariant.
- When changing routing semantics, update cases and required reasoning tags intentionally.


Backend-pattern knowledge layer:

- `backend-patterns/` contains framework-neutral backend patterns.
- Read a backend-pattern file when the task needs pattern-level reasoning before framework adaptation.
- A backend pattern is not automatically a recommendation; apply it only when the failure mode, invariant, and trade-offs justify it.
- Prefer the smallest correct mechanism. Do not introduce distributed-system patterns for a problem solvable by one database transaction or ordinary DRF code.
- Framework-specific implementation guidance in `skills/` remains authoritative for Django/DRF compatibility.


Codebase inspection and risk:

- Before substantial implementation, debugging, refactoring, or review, follow `CODEBASE_INSPECTION.md`.
- Do not infer architecture or ownership from one file; trace callers, boundaries, tests, migrations, and version/runtime context.
- Classify substantial changes with `CHANGE_RISK.md`.
- HIGH/CRITICAL changes require an explicit invariant, failure scenario, verification plan, and recovery/rollback thinking.
- Use `SKILL_COMPOSITION.md` for cross-boundary tasks, but stop loading skills when the real task no longer crosses that boundary.


Level-3 executable evals:

- `evaluations/level3/fixtures/` contains small intentionally broken Django/DRF projects.
- `scripts/run_level3_evals.py` copies fixtures to temporary workspaces, invokes an agent, and runs deterministic verification commands.
- Never weaken or delete fixture tests to make an eval pass.
- Normal CI validates and dry-runs the Level-3 harness; real agent runs are explicit because they need authenticated model access.


Invocation and attention:

- Skill descriptions are context pointers, not marketing summaries.
- Model-invoked skills use concrete `Use when ...` triggers.
- User-invoked skills are limited to explicit workflow choices and must disable implicit invocation in both `SKILL.md` and `agents/openai.yaml`.
- `ROUTING.md` and router summaries are secondary sources. Before acting on a routed skill, read that skill's own `SKILL.md`.
- Follow `AUTHORING/CONTEXT_POINTERS.md` when changing descriptions.
- Every skill must define observable `Completion criteria`.


Debugging discipline:

- For hard/intermittent bugs, prefer `backend-diagnosing-bugs`.
- Build a tight red-capable feedback loop before speculative fixes.
- Minimise the failing case, form falsifiable hypotheses, and gather discriminating evidence.
- Preserve useful regression checks after the fix.
