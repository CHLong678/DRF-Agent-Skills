# Distributed Locking

Read backend-patterns/distributed-locking.md before recommending a distributed lock.

Decision order:

1. database constraint
2. conditional update / F expression
3. optimistic state/version check
4. database row lock
5. idempotency / queue partitioning
6. distributed lease only when coordination truly spans boundaries

If using a lease, reason about expiry, stale owners, renewal, safe release, network partitions, and fencing.

A Redis lease does not provide database serializability.

If the protected resource cannot reject a stale lock holder, explain the residual split-brain risk.
