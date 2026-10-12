# Scenario: Retry Storm

## Symptom

A provider outage causes retries at multiple layers. Request threads, Celery tasks, and SDK retries amplify load and exhaust worker/provider capacity.

## Expected reasoning

1. Identify every retrying layer.
2. Define one clear retry owner per operation path.
3. Set bounded timeout/deadline budgets.
4. Retry only transient failures.
5. Require idempotency for duplicated attempts.
6. Add jitter/backoff where synchronized retries are possible.
7. Apply concurrency limits or load shedding when overload is the real failure mode.
8. Verify behavior during sustained provider failure and recovery.

## Primary skill

drf-resilience-patterns

## Secondary skills

drf-observability and drf-celery.
