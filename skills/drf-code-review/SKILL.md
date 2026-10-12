---
name: drf-code-review
description: Django REST Framework code review guidance for correctness, architecture, ORM performance, transactions, permissions, API compatibility, and tests. Use when reviewing DRF pull requests, diffs, refactors, endpoints, or bug-risk changes.
---

# DRF Code Review

Review changed behavior first. Prioritize correctness and production risk over style preferences.

## Review axes

Review the change on three independent axes.

### Spec

Ask whether the diff implements the requested behavior:

- missing requirement
- wrong semantics
- incompatible API behavior
- scope creep

### Backend safety

Check production correctness:

- authorization/tenant isolation
- data integrity
- transaction/concurrency
- idempotency/retry
- migrations
- ORM/database behavior
- external side effects

### Code quality

Check whether the implementation fits the codebase:

- project conventions
- abstraction quality
- duplication
- service/module boundaries
- testability
- unnecessary complexity

A change can pass one axis and fail another.

## Review order

### 1. Correctness

Check:

- request validation
- PATCH vs PUT semantics
- status codes
- serializer fields
- error handling
- edge cases
- backwards compatibility

### 2. Authorization

Check:

- authentication assumptions
- queryset scoping
- permission classes
- object-level permissions
- sensitive writable fields

Security findings outrank style findings.

### 3. Database and performance

Check:

- N+1 queries
- queries inside loops
- missing `select_related`/`prefetch_related`
- unnecessary queryset evaluation
- large unpaginated lists
- expensive serializer method fields
- inappropriate bulk behavior

Do not recommend indexes automatically. Explain the workload/query-plan reason.

### 4. Transactions and concurrency

Check:

- read-modify-write races
- `select_for_update()` outside `atomic()`
- task/event dispatch before commit
- application-only uniqueness checks
- duplicate request/task handling
- external I/O inside long transactions

### 5. Architecture

Check whether:

- views are overloaded with business workflows
- serializers have side effects
- logic is duplicated
- a proposed abstraction actually improves maintainability

Do not demand a service layer for trivial CRUD.

### 6. Tests

Check coverage for changed behavior, especially:

- permissions
- invalid input
- boundary values
- rollback
- concurrency where relevant
- public API contract

## Finding format

For each meaningful issue report:

1. severity: critical/high/medium/low
2. exact code/location
3. why it is a problem
4. concrete failure scenario
5. minimal safe fix

Avoid vague comments such as "optimize this" without identifying the concrete query or failure.

## Distinguish requirements from preferences

Label architectural/style suggestions as suggestions unless they affect correctness, security, performance, or maintainability materially.

## Final review summary

Summarize findings grouped by:

1. Spec
2. Backend Safety
3. Code Quality

Then report residual risk and missing tests.



Summarize:

- blocking issues
- important non-blocking issues
- residual risks
- missing tests

If no meaningful issues are found, say so rather than inventing findings.

## Routing contract

### Use this skill when
- reviewing a PR, diff, refactor, endpoint change, or bug-risk change across DRF concerns

### Do not use this skill when
- implementing one known domain behavior from scratch; use that domain skill directly

### Inspect first
- changed files and surrounding code
- public contract changes
- permissions/scoping
- query/transaction behavior
- tests and migration impact

### Related skills
- load only the domain skills required by concrete findings

## Deep reference

- `references/finding-quality.md`

## Output contract

Use the repository `OUTPUT_CONTRACTS.md` code-review format for every blocking or meaningful finding.

## Completion criteria

Done when:
- Spec, Backend Safety, and Code Quality have each been checked independently
- every reported finding has a concrete failure scenario and location
- severity reflects impact rather than style preference
- residual risks and missing tests are stated without inventing findings
