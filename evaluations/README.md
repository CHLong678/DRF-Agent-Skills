# Routing Evaluations

These cases define expected skill-selection behavior.

Each case contains:

- `prompt`: representative user/task wording
- `expected_primary`: the skill that owns the main decision
- `allowed_secondary`: skills that may be loaded when materially relevant
- `forbidden_primary`: plausible but incorrect primary choices
- `rationale`: why the route is expected

The repository validator checks structural correctness. These cases can later be used by model-specific eval harnesses for Codex/Antigravity.
