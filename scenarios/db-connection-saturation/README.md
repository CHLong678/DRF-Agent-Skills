# Scenario: Database Connection Saturation

## Symptom

Increasing Gunicorn and Celery concurrency increases PostgreSQL connection pressure and makes latency worse instead of increasing throughput.

## Expected reasoning

1. Measure web and Celery concurrency together.
2. Inspect DB max/current connections, CPU, I/O, waits, and locks.
3. Calculate a process-wide connection/concurrency budget.
4. Reduce or isolate concurrency if the DB is saturated.
5. Fix slow query/runtime issues before scaling callers further.
6. Preserve capacity headroom for deploy overlap, retries, and node loss.
7. Re-measure throughput and tail latency.

## Primary skill

drf-capacity-scaling

## Secondary skills

drf-observability, postgresql-for-django, and drf-celery.
