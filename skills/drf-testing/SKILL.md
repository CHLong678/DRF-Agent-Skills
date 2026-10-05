---
name: drf-testing
description: Django REST Framework testing guidance using pytest-django, DRF APIClient/APIRequestFactory, factories, database constraints, transaction tests, security tests, performance checks, and API contract coverage. Use when writing or reviewing tests for DRF endpoints and services.
---

# DRF Testing

## Test behavior, not framework internals

Prioritize externally meaningful behavior and domain rules.

Test:

- successful path
- validation failures
- permissions/authentication
- not-found/object scoping
- partial updates
- business conflicts
- transaction rollback
- side-effect scheduling
- pagination/filter/order behavior where part of the API contract

## API tests

Use DRF test clients for endpoint behavior. Avoid mocking DRF itself.

## Factories

Use factories/builders to make test intent clear. Override only fields relevant to the scenario.

Avoid giant fixtures shared across unrelated tests.

## Database backend fidelity

If production uses PostgreSQL, important tests for database-specific behavior should run on PostgreSQL.

Do not assume SQLite reproduces:

- row locking
- `select_for_update()`
- PostgreSQL constraints/indexes
- JSON behavior
- transaction semantics
- query planner behavior

SQLite may still be useful for lightweight unit-style tests when database-specific semantics are irrelevant.

## Transaction tests

Use transaction-aware tests when verifying:

- `select_for_update()`
- `transaction.on_commit()`
- concurrent modifications
- deadlock/retry behavior

Be aware that test wrappers can hide transaction behavior if the wrong pytest/Django test mode is used.

## Celery / async side effects

Test that the application schedules work at the correct boundary. Do not require a live worker for every unit test.

Where `on_commit()` is used, assert that dispatch does not occur on rollback and occurs after successful commit.

## Security tests

For access-controlled APIs, explicitly test:

- unauthenticated access
- horizontal privilege escalation (BOLA/IDOR)
- vertical privilege escalation
- tenant/account boundary violations
- sensitive field mass assignment
- function-level/admin action authorization

Do not assume one generic permission test covers list, detail, nested, and custom-action endpoints.

## Rate-limit and abuse tests

For security- or cost-sensitive endpoints, test the intended throttle/quota behavior and identity scope.

Where infrastructure honors proxy headers, ensure attacker-controlled headers cannot trivially alter the rate-limit identity.

## Query-performance tests

For endpoints prone to N+1 regressions, use query-count assertions carefully. Keep thresholds meaningful and resilient to harmless framework changes.

Use profiling/load tests for throughput/capacity questions rather than forcing them into unit-test timing assertions.

## Contract stability

For public APIs, cover important:

- response fields
- status codes
- error shape
- pagination shape
- versioning behavior
- deprecation behavior where relevant

so accidental contract changes fail visibly.

## Test coverage

Coverage percentage is a signal, not a correctness target by itself.

Do not optimize for an arbitrary percentage such as 90% at the expense of meaningful boundary, permission, concurrency, or failure-path tests.

## Avoid

- testing only happy paths
- using SQLite to claim lock correctness
- mocking the code under test so heavily that behavior is no longer exercised
- brittle assertions on irrelevant full response bodies
- sleeping to coordinate concurrency when deterministic synchronization is possible
- using wall-clock microbenchmarks as ordinary unit tests

## Routing contract

### Use this skill when
- test design, regression coverage, API/security/concurrency tests, factories, or DB fidelity is primary

### Do not use this skill when
- the implementation decision is still unknown; first load the domain skill that defines correct behavior

### Inspect first
- behavior/invariant being tested
- existing test framework/factories
- DB backend
- transaction/Celery execution mode
- authorization boundaries

### Related skills
- use alongside the skill that owns the behavior under test

## Deep reference

- `references/test-strategy.md`

## Output contract

For test work, state the behavior/invariant, test layer, environment fidelity, failure path, and why the test proves the intended contract.
