# Routing Matrix

The repository-level source of truth is `ROUTING.md`.

## Primary/secondary rule

A primary skill owns the main decision.
A secondary skill contributes constraints or verification.

Examples:

```text
slow API
  primary: drf-observability
  after evidence:
    N+1 -> drf-orm-performance
    COUNT -> drf-filtering-pagination
    planner/index -> postgresql-for-django
```

```text
large export endpoint
  primary: drf-bulk-large-data
  secondary:
    drf-background-jobs-contracts if public async job
    drf-celery if worker implementation
    postgresql-for-django if DB plan/locking dominates
```

```text
tenant permission leak
  primary: drf-auth-security
  secondary: drf-permissions-authorization
```

## Avoid skill fan-out

Do not load:
- `drf-core` just because the code is DRF
- `drf-code-review` during ordinary implementation unless review is the task
- `drf-testing` before the implementation decision unless test design is central
- PostgreSQL-specific skills when the project does not use PostgreSQL


```text
resilience failure / retry storm
  primary: drf-resilience-patterns
  secondary:
    drf-observability for evidence
    drf-celery when worker retry/queue mechanics matter
```

```text
DB state + message/event consistency
  primary: drf-event-driven-consistency
  secondary:
    drf-transactions-concurrency for local transaction
    drf-celery for task/broker implementation
```

```text
system saturation / capacity planning
  primary: drf-capacity-scaling
  secondary:
    drf-observability when measurements are incomplete
    postgresql-for-django for DB-specific limits
```

```text
workflow-heavy view/serializer reused elsewhere
  primary: django-service-boundaries
  secondary:
    drf-core
    django-architecture-enforcement when boundaries should be enforced
```

```text
health/readiness/shutdown/deploy process behavior
  primary: django-production-runtime
  secondary:
    drf-capacity-scaling
    drf-observability
```
