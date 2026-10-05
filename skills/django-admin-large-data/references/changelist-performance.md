# Admin Changelist Performance

## Diagnostic flow

1. reproduce with a production-like row count
2. inspect total request time
3. inspect DB query count and slow queries
4. identify count/search/sort/relation-widget cost
5. change one source of cost
6. re-measure

## Common symptoms

### Page loads but is very slow

Check full count, ordering, search joins, and N+1 queries.

### Opening add/change form hangs

Check huge FK/M2M select widgets and expensive `__str__()` methods. Use autocomplete/raw-ID style widgets.

### Search hangs

Inspect generated `icontains`/join query and indexes. Admin search is convenience UI, not a reason to add arbitrary indexes without evidence.

### Actions time out

Move large work out of the HTTP request or use set-based operations.

## Compatibility

`show_full_result_count`, `list_select_related`, `autocomplete_fields`, `raw_id_fields`, and `get_queryset()` are available in Django 3.2-era admin APIs.
