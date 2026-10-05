---
name: drf-async
description: Django REST Framework and Django async/ASGI guidance. Use when considering async views, ASGI deployment, concurrent I/O, sync/async boundaries, or deciding between request-time async work and Celery/background jobs.
---

# DRF Async & ASGI

## Async is not a default optimization

Use async when the request performs meaningful concurrent I/O and the full execution path can benefit from it.

Good candidates include:

- multiple independent external HTTP calls
- async-compatible cache/network clients
- long-lived concurrent I/O under ASGI

Async usually does not help CPU-bound work.

## Know the boundary

A single blocking sync dependency can erase much of the benefit of an async view.

Before converting a view, inspect:

- middleware
- authentication
- permissions
- ORM access
- cache client
- external SDKs
- logging/instrumentation

Avoid mixing sync and async casually.

## ORM

Use Django's supported async ORM APIs where appropriate and available for the project's Django version.

Do not wrap arbitrary ORM operations in ad-hoc thread execution without understanding connection/thread-safety implications.

Transactions and async support have version-specific constraints; verify the installed Django version before proposing an async transaction pattern.

## ASGI

Async views require an ASGI-capable deployment path to obtain their intended concurrency benefits.

Check:

- ASGI application configuration
- server choice
- middleware compatibility
- connection limits/timeouts
- proxy/load balancer behavior

Do not claim that changing `def` to `async def` alone improves throughput.

## Background jobs

Move work to Celery/background processing when:

- it does not need to finish before the HTTP response
- it is long-running
- it needs retry/scheduling
- it is CPU-heavy
- it interacts with slow external systems with durable retry requirements

Async request handling and background jobs solve different problems.

## Cancellation/timeouts

For external I/O:

- set explicit timeouts
- propagate cancellation when the client/library supports it
- avoid orphaned long-running requests

## Testing

Test async endpoints with tooling that actually exercises the async path when that behavior matters.

Also test sync/async integration points and timeout/error handling.

## Review checklist

Check:

- measurable reason for async
- blocking dependencies
- ASGI deployment
- ORM compatibility
- timeout/cancellation handling
- whether Celery is a better fit
