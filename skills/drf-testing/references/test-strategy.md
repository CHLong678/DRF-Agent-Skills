# DRF Test Strategy

## Test behavior and invariants

Prefer tests that prove externally meaningful behavior rather than internal call sequences.

Examples:

- unauthorized tenant cannot see object
- duplicate task execution does not duplicate business effect
- failed transaction does not dispatch task
- PATCH omission differs from explicit null
- list endpoint stays within query-count budget
- migration/backfill is restart-safe where required

## Test layers

### Unit

Good for:

- pure validation helpers
- state-transition functions
- domain calculations

### API/integration

Good for:

- authentication/permissions
- serializer + view behavior
- transactions
- database constraints
- pagination/filter contracts

### Concurrency

Use real concurrent transactions/processes/threads where the DB behavior matters.

A sequential test does not prove race safety.

### Celery

Test both:

- task business logic
- dispatch boundary / `on_commit()`

Do not rely only on eager mode when broker/ack/routing behavior is what you need to verify.

## PostgreSQL fidelity

If production uses PostgreSQL, SQLite cannot prove:

- row locking
- PostgreSQL constraints/operators
- JSON/Array behavior
- planner/index behavior
- transaction semantics that differ by backend

Use PostgreSQL for tests whose correctness depends on those features.

## Regression budgets

For hot APIs, query-count tests can protect against accidental N+1 regressions.

Keep budgets tied to realistic fixtures so they do not become arbitrary brittle numbers.
