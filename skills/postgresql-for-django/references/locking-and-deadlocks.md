# PostgreSQL Locks and Deadlocks

## Row locks

`SELECT ... FOR UPDATE` locks selected rows against conflicting writers/lockers until transaction end.

In Django, evaluate `select_for_update()` inside `transaction.atomic()`.

## DDL locks

Many schema operations take table locks. Some `ALTER TABLE` operations can block application traffic.

Review migration SQL for large/high-write tables.

## Deadlocks

Deadlocks happen when transactions wait cyclically on one another.

Reduce risk by acquiring locks in the same order everywhere.

Example:

```text
always lock Account rows by ascending ID
```

instead of request-dependent order.

## Long transactions

Long transactions hold locks and old snapshots longer.

Do not perform network calls or wait for user interaction while holding database locks unless absolutely required.

## Monitoring

Useful PostgreSQL views include `pg_locks` and activity/session views.

Operational debugging should identify:

- blocker PID
- blocked PID
- relation/lock mode
- query age
- transaction age
