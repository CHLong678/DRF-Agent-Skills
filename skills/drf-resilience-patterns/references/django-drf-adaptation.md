# Django/DRF Resilience Adaptation

## HTTP clients

Inspect the actual HTTP client library before recommending syntax. Exact timeout and retry APIs are library/version-specific.

Keep retry policy close enough to the integration boundary that ownership is visible.

## DRF status behavior

Use 429 for rate/quota semantics and 503 for temporary unavailability when those meanings match the contract.

Retry-After can be useful when the server has a meaningful retry delay.

## Celery

A Celery retry is not a substitute for idempotency.

For long-running/retryable work, combine transaction.on_commit when committed state is required, bounded task retry, task timeouts where appropriate, idempotent business effects, and isolated queues/concurrency for risky providers.

## Database pressure

If overload originates in PostgreSQL, increasing web/Celery concurrency can worsen the incident. Measure DB connection and lock pressure before scaling callers.
