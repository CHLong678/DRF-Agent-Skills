---
name: drf-capacity-scaling
description: Capacity and scaling guidance for Django REST Framework production systems. Use when diagnosing saturation, sizing web/Celery concurrency, planning horizontal scaling, database connection budgets, read replicas, cache/broker pressure, queue growth, or capacity headroom.
---

# DRF Capacity and Scaling

Read backend-patterns/capacity-scaling.md for framework-neutral capacity principles.

## Diagnose the saturated tier

Do not start with "add more workers".

Measure request arrival rate and latency, web worker utilization, DB connection/CPU/I/O/locks, Redis latency/memory, broker queue age/depth, Celery runtime/concurrency, and external provider limits.

## Concurrency budget

Compute total concurrency across process roles.

Web and Celery can independently look safe while jointly overwhelming PostgreSQL or a provider.

## Horizontal scaling

Before adding web/workers verify shared dependencies have capacity.

Stateless request handling makes web horizontal scaling easier.

## Queue capacity

Use oldest-message age and completion rate, not only queue length.

A stable non-zero queue can be healthy; increasing age indicates insufficient service rate.

## Read replicas

Use replicas only for reads that tolerate lag.

Read-after-write, permission, workflow-state, and transaction-sensitive reads may need the primary.

## Capacity headroom

Design for bursts, retries, deploy overlap, and node loss rather than steady-state average only.

## Routing contract

### Use this skill when
- saturation, horizontal/vertical scaling, capacity budgets, DB connections, replicas, queue growth, or system headroom are primary

### Do not use this skill when
- root cause is unknown; start with drf-observability
- the issue is only one SQL plan/index; use postgresql-for-django
- the issue is only one Celery task retry/ack behavior; use drf-celery

### Inspect first
- traffic and latency percentiles
- process counts/concurrency
- DB max/current connections
- queue age/depth and task runtime
- cache/broker/provider metrics
- deployment topology and scaling limits

### Related skills
- drf-observability, drf-celery, postgresql-for-django, drf-caching, drf-resilience-patterns

## Deep reference

- references/django-process-budget.md

## Completion criteria

Done when:
- the saturated resource is identified with evidence
- shared concurrency/capacity budgets are calculated
- the proposed scaling change does not overload downstream dependencies
- before/after throughput and tail latency are verified
