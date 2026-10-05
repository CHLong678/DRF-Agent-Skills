---
name: drf-filtering-pagination
description: Django REST Framework filtering, django-filter, pagination, query-boundary, and large-list endpoint guidance. Use when implementing FilterSet classes, multi-value filters, date-range filters, dynamic filters, list endpoints, cursor/page pagination, or expensive large-query APIs.
---

# DRF Filtering & Pagination

## Treat filtering as part of the API contract

Before adding or changing filters, inspect:

- existing query parameter names
- lookup semantics
- null/blank behavior
- multi-value encoding
- default ordering
- pagination interaction
- authorization/tenant scoping

Do not silently change a filter from exact matching to partial matching or alter its accepted value shape without considering compatibility.

## Prefer explicit FilterSet classes for non-trivial APIs

For simple stable filters, `filterset_fields` can be sufficient.

Use a dedicated `FilterSet` when you need:

- custom parameter names
- validation
- range limits
- multi-value filters
- related-field lookups
- method filters
- reusable behavior
- action-specific filter logic

Keep the allowed filter surface explicit. Do not expose arbitrary model lookups merely because django-filter can generate them.

## Multi-value filters

For `?status=a,b,c`-style filtering, use an explicit `BaseInFilter` subclass or another well-defined parser.

Validate maximum value count, type conversion, duplicate semantics, and empty-value behavior. Very large `IN (...)` lists can become a database/performance problem.

## Expensive endpoints may require bounding filters

For very large event/history/audit tables, it can be reasonable to require a time-range or another selective filter.

Examples include findings/history endpoints, logs/audit records, call records, telemetry, and events.

When enforcing a range:

- return a clear validation error
- define a maximum range
- document timezone semantics
- apply the constraint consistently to exports/background jobs too

Do not impose arbitrary range limits without workload evidence.

## Dynamic FilterSet selection

Different actions may legitimately need different filter surfaces. Use `get_filterset_class()` or the project convention when list/latest/metadata actions have different contracts.

Avoid one giant FilterSet full of action-dependent conditionals.

## Related-field filters

When filtering across relationships, verify join cost, duplicate rows, whether `distinct()` is necessary, indexes on the real join/filter path, and tenant/authorization scoping.

Do not add `distinct()` reflexively; it can be expensive.

## PostgreSQL Array/JSON filters

For ArrayField/JSONField lookups:

- make semantics explicit (`contains`, `overlap`, key/path lookup)
- validate input types
- inspect query plans for large datasets
- consider GIN/GiST indexes only when workload evidence supports them

## Pagination strategy

Use bounded pagination for collection endpoints.

Choose based on workload:

- page-number/offset: simple and reasonable for smaller datasets/admin UIs
- limit-offset: flexible but deep offsets may be expensive
- cursor/keyset: better for large/changing datasets when deterministic ordering is available

Cursor/keyset ordering should include a unique tiebreaker.

## Two-phase page hydration

For list queries with expensive joins/prefetches, a useful pattern is:

1. apply authorization + filters + ordering to a lightweight queryset
2. paginate only identifiers
3. fetch full related data for the current page
4. restore the original page order

Example:

    page_ids = list(paginator.paginate_queryset(
        base_qs.values_list("id", flat=True), request, view=self
    ))

    position = {pk: index for index, pk in enumerate(page_ids)}

    objects = (
        Finding.objects
        .filter(id__in=page_ids)
        .select_related("provider")
        .prefetch_related("tags")
    )

    ordered = sorted(objects, key=lambda obj: position[obj.id])

This preserves O(n) lookup for ordering. Avoid repeatedly calling `page.index(obj.id)`, which makes the reorder step O(n²).

Do not use two-phase hydration blindly. Compare query plans/query counts and ensure filtering and ordering semantics remain identical.

## Pagination count cost

Some pagination styles issue `COUNT(*)`. For very large or complex querysets, measure whether count is actually a bottleneck before redesigning the API.

## Filter security

Never allow user-supplied field names, raw order-by expressions, or arbitrary ORM lookup strings without an allowlist.

Validate ordering fields explicitly.

## Testing

Cover valid filters, invalid values, multi-value filters, max-range boundaries, ordering stability, pagination boundaries, authorization/filter interaction, and query-count regressions for expensive list endpoints.

## Deep references

Load `references/large-count-pagination.md` when exact `COUNT(*)` becomes a measurable bottleneck.

Exact total counts are part of the API contract, not an automatic requirement. Consider cursor pagination, `has_more`, or capped counts only when client semantics allow it.

## Routing contract

### Use this skill when
- FilterSet design, filter validation, ordering, pagination, cursor/keyset, count cost, or list-query boundaries are primary

### Do not use this skill when
- the main issue is general ORM N+1/query composition; use `drf-orm-performance`
- the main issue is PostgreSQL index/EXPLAIN analysis; use `postgresql-for-django`

### Inspect first
- current query parameters
- ordering and uniqueness
- pagination class
- authorization scope
- generated SQL/count query
- client contract

### Related skills
- `drf-orm-performance`, `postgresql-for-django`, `drf-api-contracts`
