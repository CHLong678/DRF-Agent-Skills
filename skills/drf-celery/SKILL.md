---
name: drf-celery
description: Production Celery guidance for Django REST Framework backends. Use when dispatching tasks from DRF endpoints, designing retries/idempotency, choosing acknowledgements, queues, prefetch/concurrency, Celery Canvas/chunks, task security, or diagnosing worker backlog and duplicate execution.
---

# DRF + Celery

## Decide whether work belongs in Celery

Use a background task when work:

- does not need to complete before the HTTP response
- is slow or long-running
- needs durable retry/scheduling
- performs batch processing
- calls unreliable external systems
- would otherwise hold request workers for too long

Keep short request-critical work synchronous when that produces simpler and more reliable behavior.

Async request handling and Celery solve different problems.

## Dispatch only committed database state

If a task will read rows created or modified by the current transaction, dispatch it with `transaction.on_commit()`.

    with transaction.atomic():
        order = Order.objects.create(...)
        transaction.on_commit(lambda: sync_order.delay(order.pk))

Do not enqueue a task inside an uncommitted transaction and assume the worker will wait for the commit.

Remember: `on_commit()` prevents premature dispatch but does not provide exactly-once delivery.

## Prefer small, stable task arguments

Prefer IDs, immutable identifiers, and compact JSON-serializable data over passing model-like snapshots or large payloads.

Reasons:

- the worker should normally read fresh authoritative state
- large messages increase broker/memory/network cost
- serialized snapshots can be stale
- JSON-compatible messages are easier and safer to operate

Never place passwords, access tokens, secrets, or sensitive request bodies in task arguments unless the security model explicitly requires and protects them.

## Idempotency first

Design tasks so that executing the same logical task more than once does not create unintended duplicate effects.

Useful techniques:

- durable idempotency/business keys
- database unique constraints
- explicit processed-state transitions
- conditional updates
- upserts where semantics are correct
- external-provider idempotency keys

Do not rely on Celery task IDs alone as a business invariant.

## Retry is not redelivery

Keep these concepts separate:

- `Task.retry()` / autoretry: application-controlled retry after a recoverable failure
- broker redelivery: a message becomes available again because it was not acknowledged
- duplicate execution: an operational reality tasks may need to tolerate

`acks_late=True` does not automatically retry Python exceptions.

## Retry only recoverable failures

Good retry candidates:

- network timeout
- temporary connection failure
- HTTP 429
- selected HTTP 5xx responses
- transient broker/provider outage

Usually do not retry:

- serializer/request validation failure
- permission failure
- malformed permanent input
- business rule rejection
- deterministic programming errors

Use narrow exception classes instead of `autoretry_for=(Exception,)` unless the failure model genuinely justifies it.

## Backoff and jitter

For transient failures, use bounded retries with exponential backoff and jitter where appropriate.

Example shape:

    @shared_task(
        bind=True,
        autoretry_for=(RequestException,),
        retry_backoff=True,
        retry_jitter=True,
        max_retries=5,
    )
    def sync_provider(self, provider_id):
        ...

Set explicit network timeouts as well. Celery retry/time limits are not substitutes for HTTP/database/socket timeouts.

## Acknowledgement semantics

Celery normally acknowledges a task before execution.

`acks_late=True` moves acknowledgement until after task execution and can improve recovery from some worker-loss scenarios, but the task may execute multiple times.

Only enable late acknowledgement when duplicate execution is understood and the task is idempotent enough for that delivery model.

Do not confuse `acks_late` with application retry.

`task_reject_on_worker_lost` changes worker-loss redelivery behavior and can create repeated crash/redelivery loops; use it only with a deliberate failure model.

## Queue and worker isolation

Do not make one worker pool handle every workload when task characteristics differ materially.

Consider separate queues/workers for:

- long-running tasks
- latency-sensitive short tasks
- rate-limited provider tasks
- CPU-heavy tasks
- bulk imports/exports

This reduces head-of-line blocking and makes capacity tuning easier.

## Prefetch

Celery prefetch controls how many messages workers reserve ahead of execution.

For long-running tasks, a low `worker_prefetch_multiplier` such as 1 is often more fair.

For very short tasks, a higher multiplier may improve throughput.

Do not set a universal prefetch value without considering task duration and queue behavior.

`worker_disable_prefetch` is broker-specific; current Celery documentation notes support for Redis broker, so do not recommend it generically for RabbitMQ deployments.

## Concurrency pool

Celery's prefork pool is the default and is recommended for most workloads.

Do not switch to eventlet/gevent/threads merely to increase a concurrency number. Pool choice changes runtime semantics and some Celery features.

Choose based on CPU/I/O characteristics and libraries used, then load-test.

## Task granularity and chunks

Do not enqueue one tiny message per row for millions of rows without considering broker overhead.

For large independent batches, process bounded chunks.

Celery Canvas `chunks()` can reduce messaging overhead while retaining parallelism.

Chunk size should balance:

- task runtime
- memory
- broker message overhead
- retry blast radius
- DB pressure

A failed 100-row chunk is cheaper to retry than a failed 500,000-row task, but millions of one-row tasks can overwhelm the broker.

## Time limits

Soft/hard Celery time limits can protect workers from runaway tasks, but they are not a replacement for explicit dependency timeouts and bounded algorithms.

Code that writes partial state must remain safe if interrupted.

## Result backend

If no caller needs the task result, consider `ignore_result=True` to avoid unnecessary result-backend work.

Do not disable results for workflows such as chords or operational flows that genuinely depend on task state/results.

## Monitoring and backlog

Operationally inspect at least:

- active tasks
- reserved/prefetched tasks
- scheduled tasks
- worker stats
- task failure/retry rate
- queue ready depth
- unacknowledged messages
- task runtime distribution

With RabbitMQ, distinguish ready messages from unacknowledged messages when diagnosing backlog.

High queue depth alone does not tell you whether workers are slow, tasks are prefetched, or concurrency is insufficient.

## Security

Treat the Celery broker as security-sensitive infrastructure.

- restrict broker network access
- use broker authentication/TLS where appropriate
- prefer safe serializers such as JSON
- avoid pickle when message producers are not fully trusted
- restrict accepted content types where appropriate
- assume workers execute with the worker process's filesystem/network privileges

## DRF endpoint pattern

For long-running work, prefer an asynchronous job contract:

1. validate request
2. create durable job/request record if needed
3. commit
4. enqueue with `on_commit()`
5. return `202 Accepted` with a job/resource identifier when appropriate
6. expose job status through a bounded authenticated endpoint

Do not return 200 with a vague "processing" string if the client needs a durable status contract.

## Review checklist

Check:

- should this be background work at all?
- dispatch after commit?
- idempotency key/invariant?
- retry only transient errors?
- bounded retries + backoff/jitter?
- dependency timeouts?
- `acks_late` semantics understood?
- queue isolation?
- prefetch/concurrency appropriate?
- task payload small and non-secret?
- chunk size bounded?
- monitoring/backlog signals available?

## Authoritative references

- Celery Tasks: https://docs.celeryq.dev/en/main/userguide/tasks.html
- Celery Optimizing: https://docs.celeryq.dev/en/main/userguide/optimizing.html
- Celery Routing: https://docs.celeryq.dev/en/main/userguide/routing.html
- Celery Concurrency: https://docs.celeryq.dev/en/main/userguide/concurrency/
- Celery Canvas: https://docs.celeryq.dev/en/main/userguide/canvas.html
- Celery Monitoring: https://docs.celeryq.dev/en/main/userguide/monitoring.html
- Celery Security: https://docs.celeryq.dev/en/main/userguide/security.html
- Django transactions/on_commit: https://docs.djangoproject.com/en/5.2/topics/db/transactions/
