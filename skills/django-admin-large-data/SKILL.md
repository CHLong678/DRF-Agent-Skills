---
name: django-admin-large-data
description: Django admin performance guidance for large tables compatible with Django 3.2+. Use when admin changelists time out, perform huge COUNT queries, load massive FK dropdowns, or suffer N+1 queries.
---

# Django Admin for Large Data

## Diagnose the changelist

Check SQL/query count and identify:

- full table counts
- N+1 foreign-key access
- expensive search filters
- huge relation widgets
- expensive model `__str__()` calls
- default ordering without useful indexes

## Avoid expensive full result counts

For very large tables consider:

```python
class CustomerAdmin(admin.ModelAdmin):
    show_full_result_count = False
```

This avoids the extra full-result count used to display the unfiltered total after filtering/searching.

The paginator may still need a count for pagination; this setting does not solve every count bottleneck.

## Use `list_select_related`

If `list_display` touches ForeignKey/OneToOne relations:

```python
class CustomerAdmin(admin.ModelAdmin):
    list_select_related = ("account", "owner")
```

This reduces row-by-row relation queries.

## Large FK/M2M widgets

Do not render enormous select boxes.

Prefer `autocomplete_fields` for large related tables when the related admin has suitable `search_fields`.

Use `raw_id_fields` when appropriate for older/simple setups.

## Search carefully

Broad `icontains` searches across large unindexed columns or multiple joins can be expensive.

Keep `search_fields` intentional and inspect query plans for high-volume admin usage.

## Filters

Admin list filters can execute expensive distinct/choice queries.

Do not add high-cardinality filters casually.

## Ordering

Default admin ordering can force expensive sorts. Choose ordering that matches common use and available indexes when dataset size justifies it.

## `get_queryset()`

Use admin `get_queryset()` for explicit `select_related`, annotations, or safe scoping when `list_select_related` is insufficient.

Do not prefetch large reverse collections that the changelist never renders.

## `__str__()`

Keep model `__str__()` cheap. It is invoked by admin widgets and relation displays in ways that can multiply hidden queries.

## Actions

Bulk admin actions should use set-based `QuerySet.update()` or bounded background processing where semantics allow it.

Do not loop over millions of rows with `save()` in a request.

## References

Read `references/changelist-performance.md` for a diagnostic flow.

## Routing contract

### Use this skill when
- Django admin changelist/forms/actions are slow or fail on large tables

### Do not use this skill when
- the same problem exists in a normal DRF endpoint; use the relevant DRF performance skill

### Inspect first
- admin queryset/query count
- count query
- list_display relation access
- search/list filters
- FK/M2M widgets
- __str__ cost

### Related skills
- `postgresql-for-django`, `drf-bulk-large-data`
