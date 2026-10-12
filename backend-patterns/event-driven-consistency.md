# Event-driven Consistency Patterns

## Delivery reality

Duplicate delivery must be expected unless stronger guarantees are explicitly established end-to-end.

Exactly-once claims should be scoped carefully: transport guarantees do not automatically make business side effects exactly once.

## Idempotent consumer

A consumer should produce the same business outcome when the same logical event is delivered more than once.

Techniques:

- durable event/business key
- uniqueness constraint
- processed-event table
- conditional state transition
- provider idempotency key

Do not rely only on an in-memory cache for correctness.

## Dual-write problem

Updating a database and publishing a message in two separate reliability domains creates a failure window regardless of which action happens first.

## Transactional outbox

Store the domain change and an outbox record in the same database transaction. A separate publisher sends pending outbox records.

The publisher and consumer still need idempotency because publication and delivery can repeat.

## Ordering

Do not assume global event ordering unless the system explicitly guarantees it.

Prefer per-aggregate sequence/version, compare current state/version, partition keys aligned with ordering requirements, or safely ignore stale events.

## Eventual consistency

Define the source of truth, convergence mechanism, acceptable lag, stale-read behavior, and reconciliation/replay strategy.

## Compensation / saga

When a workflow spans systems that cannot share one transaction, failures after partial completion may require compensation.

Compensation is a new business action, not a database rollback. It must itself be idempotent and observable.

## Poison messages

A permanently failing message should not retry forever.

Define max retry policy, dead-letter/quarantine path, alerting, replay procedure, and operator visibility.

## Schema evolution

Events can outlive one deployment. Prefer additive evolution and version-aware consumers. Do not couple event consumers to transient internal ORM structure.
