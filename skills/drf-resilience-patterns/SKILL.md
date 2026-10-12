---
name: drf-resilience-patterns
description: Resilience guidance for Django REST Framework dependencies and overload behavior. Use when designing timeouts, retries, jitter, circuit breakers, backpressure, load shedding, bulkheads, or graceful degradation around external services and backend capacity.
---

# DRF Resilience Patterns

Read backend-patterns/resilience.md first when the problem is pattern-level rather than framework-specific.

## Core decisions

For every remote dependency call define timeout budget, retry ownership, retryable failure classes, idempotency implications, concurrency limits, overload behavior, and fallback/degradation policy.

Do not add every resilience pattern by default.

## Timeouts

Set explicit connect/read/overall timeouts appropriate to the request or task deadline.

A timeout that is longer than the caller's useful deadline does not protect the caller.

## Retries

Retry only transient failures and only when duplicate execution is safe or protected.

Prefer bounded exponential backoff with jitter when repeated clients/workers may retry together.

Avoid stacked retries across request, Celery task, SDK, and proxy layers.

## Request-path vs background work

If the client does not need the result synchronously and work is durable/retryable, consider moving it to Celery rather than holding a web worker.

Do not use Celery merely to hide a slow dependency if the user still needs immediate synchronous correctness.

## Backpressure / overload

For expensive endpoints consider bounded concurrency, explicit quotas/rate limits, queue limits, load shedding, and tenant fairness.

Do not let unbounded queues become hidden overload storage.

## Degradation

Only degrade features whose business correctness permits stale/partial behavior.

## Verification

Simulate slow/failed dependencies, retry storms, queue saturation, and recovery. Measure resource usage and tail latency.

## Routing contract

### Use this skill when
- timeouts, retries, jitter, overload, backpressure, circuit breaking, isolation, or graceful degradation are the primary concern
- a dependency failure is propagating into API/worker saturation

### Do not use this skill when
- the main problem is Celery queue mechanics; use drf-celery
- the main problem is cache invalidation; use drf-caching
- the bottleneck is still unknown; start with drf-observability

### Inspect first
- caller deadline/SLO
- dependency timeout and retry settings at every layer
- idempotency guarantees
- worker/web concurrency
- queue/provider quotas
- current failure metrics

### Related skills
- drf-observability, drf-celery, drf-caching, drf-auth-security

## Deep reference

- references/django-drf-adaptation.md

## Completion criteria

Done when:
- deadline, timeout, and retry ownership are explicit
- duplicate/idempotency implications are handled
- overload/backpressure/fallback policy matches the failure mode
- sustained failure and recovery behavior are tested or measured
