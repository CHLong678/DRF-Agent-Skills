---
name: django-migrations-production
description: Production-safe Django migration guidance compatible with Django 3.2+. Use when changing schemas on large/live tables, backfilling data, adding indexes or constraints, splitting schema/data migrations, or planning zero/low-downtime rollouts.
---

# Django Production Migrations

## Compatibility baseline

Target Django >= 3.2. Inspect the actual database engine/version before using backend-specific operations.

## Treat migrations as deployable production code

Before applying a non-trivial migration, evaluate:

- table size and write rate
- lock level/duration
- transaction scope
- rollback/retry plan
- application compatibility during rolling deploys
- backfill cost
- index/constraint build cost

## Separate schema from data when risk is high

For large changes, prefer staged migrations over one all-in-one migration.

Typical expansion pattern:

1. add nullable/new structure
2. deploy code that can handle old + new states
3. backfill in bounded batches
4. verify completeness
5. add constraint / tighten nullability
6. remove obsolete compatibility code later

Do not assume every field addition or constraint is instant.

## Historical models in RunPython

Always use the migration app registry:

```python
def forwards(apps, schema_editor):
    Customer = apps.get_model("crm", "Customer")
```

Do not import the current model directly inside old migrations.

## Transactions

Django wraps PostgreSQL migrations in a transaction by default.

Use `atomic = False` only when required, such as PostgreSQL concurrent index operations or intentionally chunked work.

Keep transaction boundaries explicit.

## PostgreSQL concurrent indexes

On PostgreSQL, prefer `AddIndexConcurrently` for large live tables when write blocking from a normal index build would be unacceptable.

This requires a non-atomic migration.

## Data backfills

For large backfills:

- iterate in deterministic bounded batches
- avoid loading the entire table
- use set-based `update()` when possible
- keep each transaction small
- make the operation resumable/idempotent where practical
- monitor progress and DB load

## State vs database operations

When custom SQL changes schema outside Django's normal state operations, keep migration state synchronized using `state_operations` or `SeparateDatabaseAndState`.

## Verification

Use:

- `makemigrations --check`
- `sqlmigrate`
- staging/prod-like row counts
- lock/query observation
- rollback/re-run tests for reversible migrations

## Deep references

- `references/zero-downtime-patterns.md`
- `references/data-migrations.md`

## Authoritative sources

- Django 3.2 migrations: https://docs.djangoproject.com/en/3.2/topics/migrations/
- Django 3.2 migration operations: https://docs.djangoproject.com/en/3.2/ref/migration-operations/
- Django PostgreSQL migration operations: https://docs.djangoproject.com/en/3.2/ref/contrib/postgres/operations/
