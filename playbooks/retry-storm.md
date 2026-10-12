# Playbook: Retry Storm

## Goal

Stop transient dependency failure from becoming self-amplifying overload.

## Flow

1. Start with drf-resilience-patterns.
2. Map every retry layer: client, proxy, DRF code, SDK, Celery, provider.
3. Measure timeout/deadline and attempt counts.
4. Assign retry ownership.
5. Require idempotency for duplicated attempts.
6. Bound attempts and add jitter/backoff where appropriate.
7. If the dependency is still overloaded, apply concurrency limits/backpressure/load shedding.
8. Use drf-observability to verify tail latency, error rate, and resource use during failure/recovery.

## Stop conditions

Do not keep adding retries when the failure is deterministic or overload-driven.
