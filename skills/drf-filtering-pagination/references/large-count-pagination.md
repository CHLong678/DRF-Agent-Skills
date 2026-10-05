# Large-Table Pagination and Count Cost

Use this reference when exact `COUNT(*)` is expensive on a filtered/join-heavy queryset.

## Exact count is an API feature, not a requirement

Before optimizing, ask whether clients truly require an exact total.

Alternatives include:

- cursor/keyset pagination with no total
- `has_more`
- capped count
- approximate count where product semantics allow it

Changing count semantics is a contract change; do not do it silently.

## Capped count

A capped-count paginator can stop counting after a threshold and return metadata such as:

```json
{
  "count": 10001,
  "count_is_capped": true,
  "results": []
}
```

Here `count` is a lower bound, not the exact total.

If count is capped, `next` logic must not stop merely because `offset + limit >= count`; an empty page or another reliable signal must determine the end.

## Measure before redesign

Inspect:

- count query SQL
- joins/distinct
- indexes
- table cardinality
- query plan
- actual latency

Sometimes the fix is query/index design rather than pagination semantics.

## Cursor pagination

Cursor/keyset pagination avoids deep offset scans and usually avoids exact total counts.

Use deterministic ordering with a unique tiebreaker, for example:

```text
-created_at, -id
```

## Two-phase hydration

See the main skill for the pattern of paginating IDs first and hydrating related objects only for the page.
