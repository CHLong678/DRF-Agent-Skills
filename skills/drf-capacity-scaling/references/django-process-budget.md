# Django Process Capacity Budget

## Web

Estimate maximum simultaneous request work from worker/process/thread configuration.

## Celery

Estimate potential simultaneous DB/provider work from worker replicas multiplied by concurrency.

## Database

Compare total potential application concurrency with PostgreSQL connection capacity and realistic query workload.

Do not equate connection count with throughput; too much concurrency can increase contention and latency.

## Replicas

When adding read replicas, explicitly classify read paths:

- stale-safe
- read-after-write sensitive
- authorization/security sensitive
- transaction-bound

Route only paths whose consistency contract permits replica lag.
