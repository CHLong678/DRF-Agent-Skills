---
name: drf-orm-performance
description: Django ORM and DRF endpoint performance guidance. Use when optimizing QuerySets, preventing N+1 queries, reviewing annotations/subqueries, bulk operations, pagination, indexes, or high-volume API behavior.
---

# DRF ORM & Performance

## Start from access patterns

Before optimizing, identify:

- rows returned
- relations serialized
- filters/orderings used
- expected table cardinality
- query frequency
- whether model instances are actually required

Measure before making invasive changes where possible.

## Prevent N+1 queries

Use:

- `select_related()` for single-valued FK/OneToOne relations
- `prefetch_related()` for reverse FK and many-to-many relations
- `Prefetch()` for filtered/custom prefetch querysets

Match prefetching to fields actually serialized.

## QuerySet evaluation

Avoid unnecessary evaluations.

Prefer:

- `.exists()` for existence checks
- `.values()` / `.values_list()` when instances are unnecessary
- `.iterator(chunk_size=...)` for large streaming-style processing where caching all objects is undesirable
- bulk operations for large batches

Do not call `.count()` simply to know length after a queryset has already been fully materialized unless another DB count is intended.

## Bulk work

Consider:

- `bulk_create()`
- `bulk_update()`
- queryset `.update()`

But verify whether you rely on:

- `save()` overrides
- signals
- per-object validation
- generated fields
- side effects

Bulk operations may bypass these behaviors.

## Annotations and subqueries

Use `annotate`, `Exists`, `Subquery`, conditional expressions, and database aggregation when they reduce repeated application-side queries.

Do not move logic into SQL merely to be clever. Favor maintainable queries and inspect SQL/query plans for expensive endpoints.

## Indexing

Do not create an index just because a field appears in `filter()` or `order_by()`.

Evaluate:

- table size
- selectivity/cardinality
- query frequency
- sort/filter combination
- composite index order
- write overhead
- existing indexes/constraints
- `EXPLAIN` / `EXPLAIN ANALYZE`

A low-selectivity boolean field, for example, often does not benefit from a standalone index.

## Pagination

Large datasets require bounded pagination. Be cautious with very deep offset pagination; consider cursor/keyset-style pagination when ordering guarantees allow it.

## Serialization cost

Performance is not only SQL. Check:

- expensive `SerializerMethodField`
- Python loops over large results
- nested serializers
- large response payloads
- repeated date/format calculations

## Large jobs and exports

For large exports/processes:

- query in chunks
- avoid materializing all rows
- use streaming responses only when operationally appropriate
- avoid long transactions around full exports

## Verification

For meaningful optimization, compare:

- query count
- SQL shape
- execution plan
- response time
- memory behavior

Do not claim an optimization without evidence when evidence is practical to obtain.

## Routing contract

### Use this skill when
- query count, N+1, select/prefetch, annotations, subqueries, bulk ORM access, or serializer-driven queries are the main issue

### Do not use this skill when
- the task is primarily PostgreSQL EXPLAIN/index/lock analysis; use `postgresql-for-django`
- the bottleneck is unknown; start with `drf-observability`
- pagination/filter/count semantics dominate; use `drf-filtering-pagination`

### Inspect first
- actual queryset and serializer access pattern
- query count and SQL
- relation cardinality
- existing indexes/constraints only after query shape is understood

### Related skills
- `postgresql-for-django`, `drf-serializers`, `drf-filtering-pagination`
