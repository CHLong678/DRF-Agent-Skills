---
name: drf-transactions-concurrency
description: Django REST Framework transaction, locking, race-condition, idempotency, and async side-effect guidance. Use when endpoints update shared state, use atomic/select_for_update/on_commit, dispatch Celery tasks, or may be called concurrently.
---

# DRF Transactions & Concurrency

## Transaction boundaries

Use `transaction.atomic()` around the smallest coherent database unit that must commit or roll back together.

Do not keep transactions open while doing slow network I/O unless there is a compelling consistency reason.

## `select_for_update()`

`select_for_update()` must execute inside an active transaction on databases such as PostgreSQL.

Correct:

```python
from django.db import transaction

@transaction.atomic
def reserve_stock(product_id, quantity):
    product = Product.objects.select_for_update().get(pk=product_id)
    if product.stock < quantity:
        raise InsufficientStock()
    product.stock -= quantity
    product.save(update_fields=["stock"])
```

Do not evaluate a `select_for_update()` queryset before entering `atomic()`.

## Lock only when necessary

Locks serialize access and may reduce throughput or deadlock under poor ordering.

Consider alternatives:

- conditional `UPDATE`
- `F()` expressions
- database constraints
- optimistic concurrency/version columns
- unique constraints

Use row locks for read-modify-write invariants that genuinely require them.

## `F()` expressions

Use `F()` expressions for atomic arithmetic updates where you do not need to inspect the prior value in Python.

## Constraints beat application-only checks

If an invariant must always hold, prefer database constraints in addition to application validation where feasible.

Application check-then-write logic alone is race-prone.

## `transaction.on_commit()`

Use `on_commit()` for side effects that should run only after successful commit:

```python
with transaction.atomic():
    order = Order.objects.create(...)
    transaction.on_commit(lambda: send_order.delay(order.pk))
```

Typical uses:

- Celery tasks reading committed state
- webhook/event publication
- cache invalidation dependent on committed state

`on_commit()` does not make the downstream side effect exactly-once. The consumer still needs idempotency where duplicate delivery is possible.

## Idempotency

For retryable APIs/tasks:

- identify an idempotency key or durable business key
- enforce uniqueness where appropriate
- make retries safe
- distinguish retryable infrastructure failures from permanent business failures

## Deadlocks

Reduce deadlock risk by locking rows in a stable order and keeping transactions short.

When deadlocks are possible, design bounded retry behavior rather than hiding the problem.

## External systems

Do not assume a database transaction can roll back an already-completed external API call.

For cross-system consistency, consider patterns such as:

- outbox/event table
- compensating actions
- idempotent consumers

## Review checklist

Check:

- race between validation and write
- lock scope/order
- task dispatch before commit
- duplicate requests/tasks
- uniqueness enforced only in Python
- external I/O inside transactions
- transaction duration

## Routing contract

### Use this skill when
- race conditions, atomicity, row locking, idempotency, conditional updates, or commit-dependent side effects are central

### Do not use this skill when
- the question is primarily PostgreSQL lock diagnostics; use `postgresql-for-django`
- the question is task retry/ack/queue behavior; use `drf-celery`
- the task is a schema/data migration rollout; use `django-migrations-production`

### Inspect first
- invariant being protected
- current read/write sequence
- DB constraints
- transaction boundary
- external/Celery side effects

### Related skills
- `postgresql-for-django`, `drf-celery`, `django-migrations-production`

## Deep reference

- `references/locking-vs-conditional-update.md`

## Output contract

For concurrency work, use the repository `OUTPUT_CONTRACTS.md` concurrency contract: invariant, competing operations, race window, chosen primitive, scope, and concurrency test.
