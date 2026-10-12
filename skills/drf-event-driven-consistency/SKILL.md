---
name: drf-event-driven-consistency
description: Event-driven consistency guidance for Django REST Framework and Celery systems. Use when coordinating database changes with messages/events, implementing transactional outbox, idempotent consumers, eventual consistency, ordering, compensation, dead-letter handling, or event schema evolution.
---

# DRF Event-driven Consistency

Read backend-patterns/event-driven-consistency.md for framework-neutral concepts.

## Start from the consistency boundary

Identify the source of truth, systems that must change, which changes can share one DB transaction, acceptable consistency lag, duplicate behavior, and ordering requirements.

## Avoid unsafe dual writes

Do not assume database commit plus broker publish is atomic.

When losing the message is unacceptable, consider a transactional outbox stored with the business change.

## Consumer idempotency

Every retryable/redeliverable event handler should define a durable duplicate-protection strategy.

Prefer DB-backed uniqueness or state transitions over process-local memory.

## Ordering

If business logic depends on order, define the ordering scope explicitly.

Use aggregate/version-aware logic when possible.

## Compensation

Cross-system workflows may need compensating business actions rather than pretending a distributed rollback exists.

## Poison messages

Define retry exhaustion, quarantine/dead-letter behavior, alerting, and replay ownership.

## Event schemas

Treat event payloads as contracts that can outlive a deployment.

## Routing contract

### Use this skill when
- DB state and messages/events must stay consistent
- outbox, eventual consistency, idempotent consumers, ordering, compensation, or DLQ/replay are primary

### Do not use this skill when
- the problem is only Celery worker configuration; use drf-celery
- one database transaction can fully enforce the invariant; start with drf-transactions-concurrency
- the task is receiving third-party webhooks; use drf-webhooks-integrations first

### Inspect first
- producer transaction boundary
- broker/task publication path
- consumer idempotency
- event/business key
- ordering requirements
- retry/dead-letter policy
- source of truth and reconciliation path

### Related skills
- drf-celery, drf-transactions-concurrency, drf-webhooks-integrations, django-migrations-production

## Deep reference

- references/outbox-and-consumers.md
