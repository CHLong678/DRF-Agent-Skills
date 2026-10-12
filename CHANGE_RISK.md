# Backend Change Risk Classification

Classify a change before implementation. Risk determines how much context, testing, rollout planning, and verification is required.

## LOW

Examples:

- pure helper with no I/O
- local formatting/representation change with no public contract impact
- internal refactor with behavior locked by tests

Required:

- inspect direct callers
- unit/regression test

## MEDIUM

Examples:

- serializer validation
- view/action behavior
- query/filter/pagination change
- cache behavior with bounded scope
- ordinary Celery task logic without critical side effect

Required:

- trace request/task path
- compatibility check
- integration tests
- query/permission review when relevant

## HIGH

Examples:

- authentication/authorization
- transaction/concurrency behavior
- cache invalidation across tenants
- retry/ack/idempotency semantics
- external provider side effect
- schema/data migration
- job contract/state machine
- read-replica routing

Required:

- inspect all boundaries/callers
- explicit invariant
- failure scenario
- rollback/retry behavior
- production-like tests where behavior is backend-specific
- observability/verification plan

## CRITICAL

Examples:

- tenant isolation
- payment/billing
- destructive/irreversible migration
- credential/security boundary
- cross-system consistency for money or durable business state
- mass data repair
- incident-time production fix with large blast radius

Required:

- everything in HIGH
- explicit blast-radius analysis
- fail-closed behavior where appropriate
- staged rollout or migration plan
- reconciliation/recovery plan
- operator-visible verification
- peer review strongly recommended in real projects

## Risk multipliers

Increase risk when:

- code runs in multiple processes/workers
- retries/redelivery are possible
- large tables are involved
- old/new application versions coexist
- external APIs are not idempotent
- state is tenant-scoped
- operation cannot be reversed
- behavior depends on database-specific semantics

## Agent behavior

The agent should state the risk level for substantial changes and explain the concrete reason.

Do not inflate risk because a technology sounds complex. Risk is driven by failure impact, concurrency, irreversibility, security, and blast radius.
