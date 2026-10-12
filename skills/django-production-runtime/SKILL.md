---
name: django-production-runtime
description: Django production runtime and deployment-boundary guidance. Use when configuring environment-driven settings, web/Celery process roles, health/readiness checks, graceful shutdown, reverse proxy trust, startup dependency behavior, rolling deployments, or runtime observability.
---

# Django Production Runtime

Read backend-patterns/production-runtime.md for framework-neutral runtime principles.

## Configuration

Keep secrets and deploy-specific configuration outside source.

Fail clearly on missing critical production configuration.

Do not silently use development defaults in production.

## Process roles

Treat web, Celery worker, beat/scheduler, and migration/admin jobs as separate capacity and lifecycle roles.

## Health/readiness

Use lightweight health checks.

Readiness should represent whether this instance can safely receive work, not whether every optional external integration is healthy.

Avoid expensive DB/provider queries on every probe.

## Graceful shutdown

Align process termination grace with web/task time limits and broker delivery semantics.

## Reverse proxy trust

Configure forwarded-protocol/host behavior only for trusted proxy boundaries.

Do not trust arbitrary client forwarding headers.

## Rolling deploy compatibility

New application versions may coexist with old ones.

Coordinate schema/event/API changes accordingly.

## Routing contract

### Use this skill when
- runtime/deployment configuration, process roles, health/readiness, shutdown, proxy trust, or rolling deployment behavior is primary

### Do not use this skill when
- the task is schema migration mechanics; use django-migrations-production
- the issue is only startup import performance; use django-startup-performance
- the issue is application metrics/tracing design; use drf-observability

### Inspect first
- deployment/runtime platform
- Django settings split/environment loader
- web server/process model
- Celery/beat topology
- health/readiness probes
- termination grace/timeouts
- reverse proxy/load balancer trust path
- rollout strategy

### Related skills
- django-migrations-production, django-startup-performance, drf-observability, drf-celery, drf-capacity-scaling

## Deep reference

- references/runtime-checklist.md
