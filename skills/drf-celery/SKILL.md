---
name: drf-celery
description: Production Celery guidance for Django REST Framework backends compatible with Celery 5.0+. Use when dispatching tasks from DRF endpoints, designing retries/idempotency, acknowledgements, queues, prefetch/concurrency, Canvas/chunks, task security, or diagnosing worker backlog and duplicate execution.
---

# DRF + Celery

## Compatibility baseline

This skill must work with Celery 5.0+.

Inspect the installed Celery version before recommending settings introduced after 5.0.

## Decide whether work belongs in Celery

Use a background task when work does not need to complete before the response, is long-running, needs durable retry/scheduling, performs batch processing, calls unreliable external systems, or would hold request workers too long.

## Dispatch committed database state

When a task will read rows changed by the current transaction, use Django `transaction.on_commit()`.

    with transaction.atomic():
        order = Order.objects.create(...)
        transaction.on_commit(lambda: sync_order.delay(order.pk))

`on_commit()` prevents premature dispatch but does not provide exactly-once delivery.

## Prefer small, stable task arguments

Prefer IDs and compact JSON-serializable values over model snapshots or large payloads.

Do not place secrets or unnecessary sensitive request bodies in task messages.

## Idempotency first

Design tasks to tolerate duplicate logical execution using durable business keys, DB constraints, explicit state transitions, conditional updates, or external-provider idempotency keys.

Do not rely on Celery task IDs as a business invariant.

## Retry is not redelivery

Keep separate:

- `Task.retry()` / autoretry: application retry
- broker redelivery: delivery/acknowledgement behavior
- duplicate execution: something task design may need to tolerate

`acks_late=True` does not automatically retry Python exceptions.

## Retry only recoverable failures

Retry transient network failures, selected 429/5xx responses, and temporary provider outages.

Do not normally retry validation, permission, permanent input, business-rule, or deterministic programming failures.

Use narrow exception classes.

## Backoff

Celery 5.0 supports automatic retry with exponential backoff.

Baseline-safe example:

    @shared_task(
        bind=True,
        autoretry_for=(RequestException,),
        retry_backoff=True,
        max_retries=5,
    )
    def sync_provider(self, provider_id):
        ...

Do not emit newer retry options unless the installed Celery version supports them. Always set explicit dependency timeouts separately.

## Acknowledgement semantics

`acks_late=True` acknowledges after execution and may allow duplicate execution after worker-loss scenarios.

Only use late acknowledgement with an understood idempotency model.

`task_reject_on_worker_lost` exists in Celery 5.0 but can create message loops; use deliberately.

## Queue and worker isolation

Consider separate queues/workers for long-running tasks, latency-sensitive short tasks, rate-limited provider work, CPU-heavy work, and bulk imports/exports.

## Prefetch

`worker_prefetch_multiplier` exists in Celery 5.0.

For long-running tasks, a multiplier such as 1 is often fairer; short tasks may benefit from higher prefetch. Measure workload behavior.

Do not recommend these newer settings without version checks:

- `worker_enable_prefetch_count_reduction`: Celery >= 5.4
- `worker_disable_prefetch`: Celery >= 5.6 and Redis-broker specific

For Celery 5.0 + RabbitMQ, tune `worker_prefetch_multiplier` rather than suggesting `worker_disable_prefetch`.

## Concurrency pool

Prefork is the default/recommended baseline for most Celery workloads.

Do not switch pools just to increase a concurrency number; choose based on workload/libraries and load-test.

## Task granularity and chunks

Use bounded chunks for large independent batches. Celery Canvas/chunks exist in Celery 5.0.

Balance task runtime, memory, broker overhead, retry blast radius, and DB pressure.

## Time limits

Soft/hard time limits can protect workers from runaway tasks but do not replace explicit network/database/socket timeouts.

Interrupted tasks must leave partial state safe.

## Result backend

If no caller needs results, consider `ignore_result=True`; do not disable results where Canvas workflows genuinely depend on them.

## Monitoring and backlog

Inspect active, reserved, scheduled, worker stats, failures/retries, queue ready depth, unacknowledged messages, and task runtime distribution.

With RabbitMQ, distinguish ready messages from unacknowledged messages.

## Security

Restrict broker access, use authentication/TLS where appropriate, prefer JSON, avoid unsafe serializers such as pickle when producers are not fully trusted, and restrict accepted content types where appropriate.

## DRF long-running endpoint pattern

Validate request, create durable job record if needed, commit, enqueue with `on_commit()`, return `202 Accepted` with an identifier when appropriate, and expose bounded authenticated status.

## Authoritative baseline references

- Celery 5.0 User Guide: https://docs.celeryq.dev/en/v5.0.5/userguide/
- Celery 5.0 Tasks: https://docs.celeryq.dev/en/v5.0.5/userguide/tasks.html
- Celery 5.0 Optimizing: https://docs.celeryq.dev/en/v5.0.5/userguide/optimizing.html
- Celery 5.0 Configuration: https://docs.celeryq.dev/en/v5.0.0/userguide/configuration.html
- Django 3.2 transactions/on_commit: https://docs.djangoproject.com/en/3.2/topics/db/transactions/

## Deep references

- `references/tenant-scope.md` — explicit tenant/account scope propagation from DRF requests into Celery workers.
- `examples/tenant_task.py` — baseline-compatible dispatch-after-commit and scoped task example.

Request-local authorization context does not survive broker dispatch automatically.
