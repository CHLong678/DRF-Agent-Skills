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
