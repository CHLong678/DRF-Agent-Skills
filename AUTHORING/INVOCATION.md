# Skill Invocation

Skills have one of two invocation modes.

## Model-invoked

Default for domain skills that the agent can usefully select on its own.

Requirements:

- `SKILL.md` description is model-facing and contains concrete trigger language.
- Do not set `disable-model-invocation: true`.
- `agents/openai.yaml` omits `policy.allow_implicit_invocation: false`.
- The skill must be safe and useful when selected automatically from task context.

Examples:

- `drf-orm-performance`
- `drf-celery`
- `drf-auth-security`
- `postgresql-for-django`

## User-invoked

Use only for workflow/orchestration actions that should require an explicit human choice.

Requirements:

- `SKILL.md` sets `disable-model-invocation: true`.
- `agents/openai.yaml` sets `policy.allow_implicit_invocation: false`.
- The description is human-facing; do not add fake model trigger phrases merely to satisfy discovery.
- A model-invoked skill must never operationally invoke a user-invoked skill.

Current user-invoked skills:

- `drf-skill-router`
- `backend-agent-retro`

## Cross-skill invocation

A router or composition document may name skills for orientation.

Before acting on another skill's guidance, read that skill's own `SKILL.md`. Router summaries are secondary sources.

Operational dependencies should name the target skill explicitly rather than copying its rules into the caller.

## Why this matters

Every model-invoked description consumes routing attention. Making every workflow auto-invoked increases ambiguity and context load.

Prefer model invocation for reusable domain expertise; prefer explicit invocation for workflow choices the human should control.
