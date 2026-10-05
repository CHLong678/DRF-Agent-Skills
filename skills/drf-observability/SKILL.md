---
name: drf-observability
description: Django REST Framework observability, profiling, performance verification, logging, metrics, tracing, and load-test guidance. Use when diagnosing slow endpoints, adding monitoring, reviewing production readiness, or validating performance changes.
---

# DRF Observability & Performance Verification

## Measure before optimizing

For slow or high-traffic endpoints, establish a baseline:

- latency distribution, not only average
- request rate
- error rate
- DB query count/time
- external-call latency
- cache hit/miss rate
- worker saturation where relevant

Avoid performance claims based only on code appearance.

## Development profiling

Useful tools may include:

- Django Debug Toolbar
- django-silk
- Django query logging
- database `EXPLAIN (ANALYZE, BUFFERS)`
- Python profilers

Use profiling tools in appropriate environments; do not expose debug tooling publicly in production.

## Structured logging

Prefer structured, searchable logs with useful context such as:

- request/correlation ID
- endpoint/action
- user/account/tenant identifier when safe
- duration
- status code
- downstream service name

Never log secrets, raw tokens, passwords, or sensitive request bodies by default.

## Metrics

Track signals that drive decisions, for example:

- p50/p95/p99 latency
- 4xx/5xx rate
- DB pool saturation
- Celery queue depth / task failure
- Redis/cache health
- external dependency latency

Avoid high-cardinality metric labels such as raw user IDs or arbitrary URLs.

## Tracing

Distributed tracing is useful when latency spans:

- DRF request
- database
- Redis
- Celery
- external services

Propagate correlation/trace context where the stack supports it.

## Load testing

Use load tests for capacity questions, not as a substitute for correctness tests.

Model realistic:

- authentication
- request mix
- payload sizes
- cache warm/cold behavior
- concurrency
- database state

Observe bottlenecks before and after the change.

## Performance regression tests

For critical endpoints, consider:

- query-count regression tests
- bounded response-size checks
- benchmark/load-test scenarios in CI or scheduled environments

Do not set brittle microsecond-level assertions in normal unit tests.

## Production readiness

Check:

- health/readiness behavior
- timeout configuration
- error reporting
- slow-query visibility
- alertable SLO/SLA signals
- dependency failure visibility

## Routing contract

### Use this skill when
- the bottleneck/failure source is unknown or you need profiling, logs, metrics, tracing, load tests, or operational verification

### Do not use this skill when
- a specific root cause is already established and a dedicated skill owns the fix

### Inspect first
- latency distribution
- request/error rate
- DB/external/cache timings
- query count
- worker/queue saturation
- existing logs/metrics/traces

### Related skills
- route to `drf-orm-performance`, `postgresql-for-django`, `drf-caching`, or `drf-celery` after evidence
