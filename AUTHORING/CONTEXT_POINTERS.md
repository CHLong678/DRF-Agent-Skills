# Context Pointers

A skill description is a routing pointer, not a marketing summary.

Its job is to make the model load the right skill at the right moment with the least possible context cost.

## Good pointer

A good model-facing description states:

1. the domain owned by the skill
2. concrete task/failure signals
3. the boundary against the closest sibling when ambiguity is likely

Example:

```text
Django/DRF ORM performance guidance. Use when a request is slow because of
queryset shape, N+1 queries, relation loading, annotations, repeated existence
checks, or excessive ORM round trips.
```

## Weak pointer

Avoid descriptions that are only category labels:

```text
Guidance for optimizing Django APIs.
```

They do not give the model enough trigger information.

Avoid descriptions that list every related backend concept. Over-broad pointers cause skill fan-out.

## Positive target before negation

Prefer a strong positive trigger first:

```text
Use when the invariant is protected by database/transaction concurrency...
```

Then use negative routing only for the nearest common confusion.

## Leading words

Use stable vocabulary repeatedly when it gives the model a compact semantic hook.

Examples in this repository:

- invariant
- boundary
- feedback loop
- seam
- saturation
- idempotency
- source of truth
- outbox
- reconciliation
- blast radius

Do not invent a new synonym in every skill.

## Environment is source of truth

Do not duplicate version numbers, commands, queue names, settings, or directory layouts that the target codebase can reveal directly.

Point the agent at the environment and require inspection.

Documentation should contain durable decision rules; the code/configuration should contain current facts.
