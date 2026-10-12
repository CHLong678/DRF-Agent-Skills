# Scenario: Provider State Reconciliation

## Symptom

After an outage, the external provider reports completed operations while local Django records remain pending.

## Expected reasoning

1. Define the authoritative state and reconciliation invariant.
2. Query/report candidates before mutation.
3. Add a dry-run mode for risky repair.
4. Repair in bounded resumable batches.
5. Protect against live-write races.
6. Avoid duplicating external side effects.
7. Audit repairs and verify convergence.

## Primary skill

`drf-reconciliation-repair`

## Secondary skills

`drf-event-driven-consistency`, `drf-bulk-large-data`, and `drf-transactions-concurrency`.
