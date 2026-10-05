# Playbook: Celery Backlog

## Goal

Determine whether backlog comes from production rate, task runtime, worker capacity, prefetch, routing, or failures.

## Flow

1. Load `drf-celery`.
2. Inspect ready vs unacknowledged/reserved/active tasks.
3. Measure task runtime and failure/retry rate.
4. Inspect concurrency pool, queue routing, and prefetch.
5. Check dependency latency/timeouts.
6. Check whether long and short workloads share one queue.
7. Load `drf-observability` for missing metrics/tracing.
8. Load `drf-bulk-large-data` if giant jobs should be chunked.

## Stop conditions

Do not increase concurrency before identifying DB/provider/broker capacity constraints.
