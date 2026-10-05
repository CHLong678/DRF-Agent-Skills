# Low-Downtime Migration Patterns

## Expand and contract

For changes that must survive rolling deployments, prefer temporary backward compatibility.

Example rename strategy:

```text
add new field
→ code writes old + new / reads compatibly
→ backfill
→ switch reads/writes to new
→ stop using old
→ remove old in later deploy
```

Avoid changing application code and database assumptions in a way that requires all workers to restart atomically.

## Adding indexes

Normal PostgreSQL `CREATE INDEX` blocks writes while building. `CREATE INDEX CONCURRENTLY` allows normal writes but takes longer and has caveats.

With Django 3.2:

```python
from django.contrib.postgres.operations import AddIndexConcurrently

class Migration(migrations.Migration):
    atomic = False
    operations = [
        AddIndexConcurrently(
            model_name="customer",
            index=models.Index(fields=["phone"], name="customer_phone_idx"),
        ),
    ]
```

Do not use concurrent-index operations inside an atomic migration.

## Adding NOT NULL safely

For a populated large table, do not blindly add a new non-null field with a heavy default.

A safer staged approach is often:

1. add nullable field
2. deploy code writing it
3. backfill old rows
4. verify no nulls remain
5. enforce non-null constraint

Actual PostgreSQL behavior depends on server version and operation; inspect generated SQL and lock behavior.

## Constraints

Adding/validating constraints may lock or scan large tables.

Treat them as production operations, not just model metadata.

## Rollback

A migration can be logically irreversible even when Django can technically reverse the schema.

Plan whether data written by the new application version remains compatible with the old version.
