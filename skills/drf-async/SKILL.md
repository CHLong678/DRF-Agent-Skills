---
name: drf-async
description: Django REST Framework and Django async/ASGI guidance compatible with Django 3.2+. Use when considering async views, ASGI deployment, concurrent I/O, sync/async boundaries, or deciding between request-time async work and Celery/background jobs.
---

# DRF Async & ASGI

## Compatibility baseline

This skill must work with Django 3.2+.

Always inspect the installed Django version before emitting async ORM or async streaming code.

## Async is not a default optimization

Use async when the request performs meaningful concurrent I/O and the full execution path can benefit from it.

Good candidates include multiple independent external HTTP calls, async-compatible network/cache clients, and long-lived concurrent I/O under ASGI.

Async usually does not help CPU-bound work.

## Django 3.2-safe ORM boundary

In Django 3.2, the ORM is synchronous and async-unsafe.

From an async view, move cohesive DB work into a synchronous function and call it through `sync_to_async(..., thread_sensitive=True)`.

Example:

    from asgiref.sync import sync_to_async

    def _load_order(order_id):
        return (
            Order.objects
            .select_related("customer")
            .get(pk=order_id)
        )

    order = await sync_to_async(_load_order, thread_sensitive=True)(order_id)

Do not call synchronous ORM methods directly from an async context.

## Django >= 4.1 async ORM

Django 4.1 introduced async QuerySet iteration and async-prefixed ORM interfaces.

Use those only after verifying the installed Django version and the exact operation's async support.

Do not rewrite a Django 3.2-compatible project to `aget()`, `acreate()`, `aiterator()`, or `async for` over QuerySets unless its version supports them.

Transactions still deserve special care in async code; verify the installed Django version and prefer a cohesive synchronous transactional function when necessary.

## Know the request-stack boundary

A blocking sync dependency can erase much of the benefit of an async view.

Before converting a view, inspect middleware, authentication, permissions, ORM access, cache client, external SDKs, and instrumentation.

## ASGI

Async views exist in Django 3.2, but the intended concurrency benefits require an ASGI-capable deployment path and compatible middleware.

Async views under WSGI can run but do not provide a fully asynchronous request stack.

Do not claim that changing `def` to `async def` alone improves throughput.

## Streaming compatibility

For Django 3.2 through 4.1, use a synchronous iterator with `StreamingHttpResponse`.

Async iterators for `StreamingHttpResponse` are supported starting in Django 4.2 under ASGI.

Version-gate async streaming examples.

## Background jobs

Move work to Celery when it does not need to finish before the response, is long-running, needs retry/scheduling, is CPU-heavy, or needs durable retry against slow external systems.

Async request handling and background jobs solve different problems.

## Timeouts and cancellation

For external I/O, set explicit timeouts and propagate cancellation when the client/library supports it.

## Testing

Exercise the actual async path when async behavior matters, and test sync/async boundaries plus timeout/error handling.

## Review checklist

Check installed Django version, measurable async benefit, blocking dependencies, ASGI deployment, ORM compatibility, streaming compatibility, timeouts, and whether Celery is a better fit.

## Routing contract

### Use this skill when
- async views, ASGI, concurrent request-time I/O, or sync/async boundaries are primary

### Do not use this skill when
- work should survive the request, retry durably, or be scheduled; use `drf-celery`
- the task is only ordinary synchronous DRF

### Inspect first
- Django version
- ASGI/WSGI deployment
- middleware/auth/ORM/cache/client sync-async compatibility
- whether work is request-critical

### Related skills
- `drf-celery`, `drf-observability`
