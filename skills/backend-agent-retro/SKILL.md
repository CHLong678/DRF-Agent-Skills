---
name: backend-agent-retro
description: Review a completed or failed backend-agent session and propose improvements to the agent environment, checks, skills, routing, or tests so the same class of failure is less likely next time.
disable-model-invocation: true
---

# Backend Agent Retro

Use this explicitly after a meaningful build/debug/eval session, especially one that failed or required repeated correction.

The target is the **agent environment**, not another review of the application code.

## Inputs

Inspect:

- the task/spec
- agent trace or summary
- changed files
- test/eval results
- corrections the human had to make
- routing/skill choices
- tools/checks that were missing or noisy

## Classify each failure

Prefer this order:

1. deterministic/mechanical failure
2. missing feedback loop/test
3. missing codebase pointer/context
4. ambiguous routing/context pointer
5. missing completion criterion
6. missing backend pattern/reference
7. judgement/architecture guidance

## Choose the strongest prevention

Prefer:

```text
deterministic CI/static check
>
executable regression/eval fixture
>
validator
>
skill/reference rule
>
router/context-pointer update
>
generic AGENTS.md reminder
```

Do not add prose when a deterministic check can prevent the same mistake.

## Output

For each recommendation state:

- observed failure
- why the current environment allowed it
- proposed repository change
- prevention strength
- expected blast radius
- how to verify the improvement

## Routing contract

### Use this skill when
- a session/eval exposed recurring agent failure
- the user wants to improve the skill repo or agent environment after work completed

### Do not use this skill when
- the current application bug is not fixed yet
- the user only wants code review of the product change

### Inspect first
- session/eval evidence
- existing validators/tests
- relevant skill and routing metadata
- whether a deterministic enforcement already exists

### Related skills
- `django-architecture-enforcement`, `drf-testing`, and the domain skill involved in the failure

## Completion criteria

Done when:

- each recommendation is tied to an observed failure
- deterministic prevention is preferred where feasible
- duplicate instructions are avoided
- proposed changes have a concrete verification method
