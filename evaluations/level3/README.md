# Level-3 Executable Agent Evaluations

Level 3 evaluates whether an agent can modify a small Django/DRF codebase and make deterministic tests pass.

The runner:

1. copies a fixture to a temporary working directory
2. optionally creates a virtualenv and installs fixture requirements
3. invokes Codex or Antigravity on the task
4. runs the fixture's verification command
5. stores a report

The source fixture is never edited.

## Run

Dry-run:

python scripts/run_level3_evals.py --provider codex --dry-run

Run one fixture:

python scripts/run_level3_evals.py --provider codex --fixture drf-n-plus-one --setup

Antigravity can be selected with --provider antigravity. Whether non-interactive editing is permitted depends on the installed CLI/account policy; the harness does not enable a global dangerous permission-bypass flag.

## Fixtures

- drf-n-plus-one — fix serializer-driven N+1 without changing output
- tenant-list-leak — enforce tenant list isolation
- idempotent-side-effect — make duplicate logical execution produce one business effect
- patch-null-vs-omitted — preserve PATCH omission while allowing explicit null
- cross-tenant-cache-leak — make cache keys tenant-safe without disabling caching
- custom-action-permission-leak — keep custom actions inside authorized object visibility
- side-effect-before-commit — dispatch side effects only after successful commit

## Scoring

A Level-3 fixture passes only when its verification command exits successfully after the agent run.

This measures final observable behavior, not private chain-of-thought.
