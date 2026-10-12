# Completion Criteria

Every implementation/debugging skill should tell the agent what observable state means the task is complete.

A completion criterion is stronger than "apply the recommendation".

## Rules

Completion criteria should be:

- observable
- tied to the user's invariant/contract
- independent of private chain-of-thought
- checkable by tests, measurements, schema, logs, or explicit code inspection

## Examples

ORM performance:

- baseline query behavior is measured
- the access pattern causing excess queries is identified
- the API payload remains compatible
- before/after query count or DB time is captured

Concurrency:

- the invariant is stated
- the race window is identified
- the chosen primitive protects the invariant
- competing/duplicate execution is tested

Celery:

- producer and consumer paths are known
- retry/redelivery/idempotency behavior is explicit
- queue/routing configuration is checked
- failure and recovery are verifiable

Security:

- the protected resource and trust boundary are stated
- list/detail/create/action paths are checked
- cross-tenant/cross-user regression tests exist where relevant

Migration:

- generated SQL and lock risk are understood
- rollout ordering is compatible with old/new code
- backfill is bounded/restartable where needed
- rollback/retry behavior is explicit

## Anti-pattern

Do not use completion criteria like:

- "code is clean"
- "the solution follows best practices"
- "review complete"

These are not independently verifiable.
