# Production Data Migrations

## Use historical models

```python
def forwards(apps, schema_editor):
    Customer = apps.get_model("crm", "Customer")
    alias = schema_editor.connection.alias
```

Use `.using(alias)` in multi-database environments.

## Prefer set-based operations

Good:

```python
Customer.objects.using(alias).filter(status__isnull=True).update(status="new")
```

Avoid one `save()` per row when a set-based update is equivalent.

## Batch when per-row transformation is required

Use deterministic primary-key windows or bounded chunks.

Requirements:

- stable progress order
- bounded memory
- bounded transaction size
- restart-safe behavior where possible

## Separate schema and data changes

Django documents that combining schema changes and `RunPython` on PostgreSQL can cause issues around pending trigger events.

Prefer separate migrations when both are non-trivial.

## Reversibility

Provide `reverse_code` when safe and meaningful.

Do not fake reversibility if the original data cannot actually be reconstructed.
