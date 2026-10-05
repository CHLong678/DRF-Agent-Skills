# Scenario: Large-table Schema Change

## Symptom

A deployment needs a new populated field/index/constraint on a large, write-heavy PostgreSQL table.

## Expected reasoning

1. Inspect generated SQL and PostgreSQL version.
2. Identify lock/scan/backfill risk.
3. Use expand/backfill/validate/contract stages when needed.
4. Keep large backfills resumable and bounded.
5. Use concurrent index creation when justified.
6. Verify old/new app version compatibility during rolling deploy.
7. Plan rollback/retry honestly.

## Primary skill

`django-migrations-production`

## Secondary skill

`postgresql-for-django`.
