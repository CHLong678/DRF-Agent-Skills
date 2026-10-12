# Scenario: Database / Broker Dual Write

## Symptom

Business state commits in PostgreSQL, then a process attempts to publish to RabbitMQ. A crash between the two loses the event.

## Expected reasoning

1. Identify PostgreSQL as business source of truth.
2. State the dual-write failure window explicitly.
3. Store an outbox record in the same DB transaction as the business change.
4. Publish outbox records asynchronously.
5. Make publication and consumption idempotent.
6. Define retry exhaustion, monitoring, and replay.
7. Version event payloads when they are durable contracts.

## Primary skill

drf-event-driven-consistency

## Secondary skills

drf-transactions-concurrency and drf-celery.
