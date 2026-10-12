---
name: drf-reconciliation-repair
description: Reconciliation, repair, replay, and production backfill guidance for Django REST Framework systems. Use when detecting or repairing inconsistent state after partial failures, replaying events/tasks, reconciling provider state, building resumable repair jobs, quarantining poison records, or safely fixing large batches.
---

# DRF Reconciliation and Repair

Read backend-patterns/failure-recovery.md first.

## Start from an invariant

Define the expected state and the authoritative source.

A repair job without an explicit invariant can make corruption worse.

## Discovery vs mutation

Prefer separate phases:

1. identify candidates
2. report/dry-run
3. repair bounded batches
4. verify convergence

For critical/destructive repairs, make the candidate set inspectable.

## Idempotency and resume

A repair job should be safe to restart.

Use stable selection criteria/checkpoints rather than relying only on process memory.

## Live writes

Assume production traffic can modify records while a repair runs.

Use conditional updates/version checks/locking only where required by the invariant.

## Replay

Before replaying events/tasks, verify downstream duplicate safety, schema compatibility, ordering, and external side effects.

## Auditability

Record enough information to answer what was changed, why, by which job/operator, and whether repair succeeded.

## Routing contract

### Use this skill when
- inconsistent state must be detected/repaired after partial failure
- event/task replay, reconciliation, repair scripts, poison records, or resumable backfill are primary

### Do not use this skill when
- the task is a normal schema migration; use django-migrations-production
- the invariant can be fixed synchronously in one normal transaction
- the task is only message delivery design before any failure; use drf-event-driven-consistency

### Inspect first
- invariant/source of truth
- inconsistency detection query
- affected row/object count
- live write/concurrency behavior
- external side effects
- replay/idempotency semantics
- audit and rollback/compensation options

### Related skills
- drf-event-driven-consistency, drf-transactions-concurrency, drf-bulk-large-data, django-migrations-production

## Deep reference

- references/repair-job-checklist.md
