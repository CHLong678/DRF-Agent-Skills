# Distributed Locking

## Start with the invariant

A distributed lock is not a default concurrency tool.

First ask whether the invariant can be protected by:

1. database constraint
2. conditional update
3. row lock
4. idempotency key
5. queue partitioning / single consumer per key

Only use a distributed lock when coordination truly spans processes/systems and simpler ownership mechanisms do not solve it.

## Lease semantics

A distributed lock is commonly a lease with expiry.

Questions that must be answered:

- owner identity
- lease duration
- renewal
- safe release
- behavior when holder pauses
- behavior after network partition

## Expiry hazard

A worker can keep running after its lease expires.

Another worker may acquire the same lock, so both can act concurrently.

Therefore a lock alone may not protect destructive external effects.

## Fencing tokens

A monotonically increasing fencing token lets the protected resource reject stale lock holders.

Useful when the downstream system can enforce token ordering.

Without downstream enforcement, a fencing token is only metadata.

## Redis lock caution

Atomic acquire/release scripts can improve correctness of a Redis lease, but they do not remove network/expiry/fencing limitations.

Do not describe Redis locks as equivalent to database serializability.

## Long work

Do not hold a lease longer than needed.

For durable workflows prefer explicit state ownership, idempotency, queue partitioning, or resumable jobs where possible.

## Verification

Test holder crash, lease expiry, slow pause, network failure, duplicate workers, and stale-owner release.
