# Outbox and Consumer Adaptation

## Producer

Inside one transaction:

1. change business state
2. create outbox record

After commit, a publisher can send pending records.

Do not mark an outbox row permanently delivered before broker publication is known to have succeeded according to your publisher design.

## Consumer

Use a durable message/event key where available.

Possible strategy:

- atomically claim event ID
- verify current business state/version
- apply transition
- record processed state

The exact schema depends on throughput and retention requirements.

## Celery as transport/execution

Celery tasks can carry event-like work, but Celery result state is not a domain event log.

Do not expose internal task IDs as durable business event identity unless that coupling is intentional.
