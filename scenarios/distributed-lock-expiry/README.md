# Scenario: Distributed Lock Expiry

## Symptom

A worker holds a Redis lease, pauses past its expiry, then resumes after another worker has acquired the same lock. Both can write concurrently.

## Expected reasoning

1. State the protected invariant.
2. Ask whether a DB constraint, conditional update, row lock, idempotency key, or queue partitioning can replace the distributed lease.
3. If a distributed lease is unavoidable, reason about owner identity, expiry, renewal, stale release, and network pauses.
4. Use fencing only when the protected resource can reject stale tokens.
5. Do not claim the Redis lock alone proves exclusive business execution.
6. Test stale-holder behavior.

## Primary skill

`drf-transactions-concurrency`

## Secondary skill

`postgresql-for-django` when the invariant is DB-backed.
