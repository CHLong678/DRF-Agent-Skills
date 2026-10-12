# Failure Recovery and Reconciliation

## Goal

Assume some production failures will escape the synchronous request/task path and provide a deterministic way to detect and repair them.

## Reconciliation

Compare expected business state with observed external/internal state.

Examples:

- paid order exists but invoice event is missing
- provider says call completed but local status is stale
- outbox row is stuck pending
- storage object exists but DB metadata was not committed

Reconciliation should be idempotent and resumable.

## Repair jobs

A repair operation should define:

- selection criteria
- invariant being restored
- batch size
- dry-run mode when destructive
- idempotency
- checkpoint/resume
- audit log
- operator visibility

## Replay

Events/tasks may need replay after a bug or outage.

Before replaying define:

- deduplication/idempotency behavior
- event version compatibility
- ordering requirements
- replay scope/window
- downstream side-effect safety

## Quarantine

Poison data/messages should be isolated rather than retried forever.

Store enough context for diagnosis without leaking secrets.

## Backfill

Large data repair/backfill should be bounded, observable, restartable, and compatible with live writes.

## Manual overrides

For critical workflows, explicit operator actions can be safer than magical auto-recovery.

Audit who changed what and why.

## Verification

Measure unresolved inconsistency count, repair throughput, retry/failure rate, and convergence time.
