# Playbook: Production Migration

## Goal

Change a live schema/data set with bounded lock and rollout risk.

## Flow

1. Load `django-migrations-production`.
2. Inspect table size, write rate, generated SQL, deployment strategy, and database version.
3. Decide whether expansion/backfill/constraint/removal must be split across deploys.
4. For PostgreSQL lock/index behavior, load `postgresql-for-django`.
5. Use historical models in data migrations.
6. Batch/resume large backfills.
7. Use concurrent indexes when justified and supported.
8. Verify rollback/forward compatibility with old and new application versions.

## Stop conditions

Do not assume a migration is safe because it is syntactically valid or fast on development data.
