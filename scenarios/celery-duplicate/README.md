# Scenario: Duplicate Celery Execution

## Symptom

A task calling an external billing/provider API is executed twice after retry/redelivery and creates duplicate side effects.

## Expected reasoning

1. Separate application retry from broker redelivery.
2. Identify acknowledgement settings.
3. Define a durable business idempotency key.
4. Use DB constraints/state transitions/provider idempotency where available.
5. Dispatch only after commit when task reads newly committed state.
6. Test duplicate logical execution.

## Primary skill

`drf-celery`

## Secondary skills

`drf-transactions-concurrency`, `drf-testing`.
