# Playbook: Database and Message Dual Write

## Goal

Prevent a committed business change from losing its required event/message.

## Flow

1. Start with drf-event-driven-consistency.
2. Identify source of truth and local transaction boundary.
3. Show the failure window between database commit and broker publish.
4. If event loss is unacceptable, consider a transactional outbox in the same DB transaction.
5. Publish asynchronously and idempotently.
6. Make consumers idempotent.
7. Define ordering/version behavior.
8. Define retry exhaustion, replay, and operator visibility.

## Stop conditions

Do not introduce an outbox when no cross-system consistency requirement exists.
