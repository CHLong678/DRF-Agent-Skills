# Backend Feedback Loops

Choose the smallest loop that reproduces the real failure.

## API correctness

Use a focused APIClient/pytest/Django test or a curl/request replay.

Capture:

- status
- stable error code/body
- database/business effect

## ORM performance

Use:

- `assertNumQueries()`
- captured SQL
- realistic fixture cardinality
- DB timing when query count alone is insufficient

## Concurrency

Use a real database/backend whose semantics matter.

A sequential test is not a concurrency repro.

Coordinate competing operations with barriers/events when needed.

## Celery

Separate:

- business logic failure
- dispatch timing
- retry/redelivery
- broker/worker behavior

A direct function call can reproduce business logic, but it does not prove broker semantics.

## Webhooks

Persist/replay the exact raw payload and headers needed for signature/order/duplicate behavior.

## PostgreSQL

Use EXPLAIN/lock inspection only when the failure concerns the database plan/locking.

Remember that EXPLAIN ANALYZE executes the statement.

## Human-in-loop

If reproducing the bug needs manual state, create a short script that tells the human exactly what to do and captures the observation back into the loop.
