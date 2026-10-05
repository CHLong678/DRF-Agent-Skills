# Locking vs Conditional Update

Use this reference when choosing between constraints, `F()`, conditional UPDATE, optimistic checks, and row locks.

## Decision order

Prefer the smallest primitive that enforces the invariant:

1. database constraint
2. set-based/conditional update
3. optimistic version/state check
4. row lock
5. broader distributed coordination only when the invariant crosses the database boundary

## Conditional update

For a state transition:

```python
updated = Order.objects.filter(
    pk=order_id,
    status="pending",
).update(status="processing")

if updated != 1:
    # already changed or not eligible
    ...
```

This can avoid a read-lock-write cycle when the transition predicate is expressible in SQL.

## F expressions

For arithmetic updates:

```python
Account.objects.filter(pk=account_id).update(
    login_count=F("login_count") + 1
)
```

This avoids Python read-modify-write lost updates.

## Row locking

Use `select_for_update()` when the next decision genuinely depends on current locked state across multiple reads/writes.

Keep the transaction short.

Do not hold DB locks while calling external APIs unless the lock must intentionally cover that external operation.

## Optimistic checks

A version/timestamp/state predicate can reject stale writes without blocking readers.

Use when conflicts are uncommon and retry/reload semantics are acceptable.

## Distributed locks

Do not reach for Redis/distributed locks when a database constraint or conditional update already protects the invariant.

Distributed locks add lease expiry, ownership, failure, and fencing concerns.
