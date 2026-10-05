# ORM Query-shape Playbook

Use this reference when query count or relation loading is the bottleneck.

## Start from serializer/view access

Map the actual object graph touched by the endpoint.

Example:

```text
Order
 ├─ customer         single-valued
 ├─ account          single-valued
 └─ items[]          collection
      └─ product     single-valued
```

A likely loading strategy is:

- `select_related("customer", "account")`
- `prefetch_related("items__product")`

Do not choose eager loading from model relationships alone; choose it from the access path used by the endpoint.

## select_related vs prefetch_related

Use `select_related()` for ForeignKey/OneToOne-style single-valued joins.

Use `prefetch_related()` for reverse or multi-valued relationships where separate bounded queries are appropriate.

## Serializer-driven N+1

Common sources:

- `SerializerMethodField`
- model properties
- `__str__()`
- nested serializers
- permission/display helpers
- looped `.exists()` / `.count()` / `.first()`

Inspect the serializer and every helper it calls.

## Do not over-fetch

Eager loading every relation can increase row width, memory, duplicate rows, and serialization cost.

Only load relations required by the response or downstream logic.

## Annotations/subqueries

Use annotations, `Exists`, and `Subquery` when they replace repeated per-row queries cleanly.

Do not force a complex SQL expression merely to eliminate one cheap query without evidence.

## Verification

Compare before/after:

- query count
- SQL
- latency
- memory/response size
- database time

A lower query count is not automatically faster if each query became substantially more expensive.
