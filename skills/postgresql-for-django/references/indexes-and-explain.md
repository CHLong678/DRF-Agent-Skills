# PostgreSQL Indexes and EXPLAIN

## EXPLAIN workflow

1. capture the real SQL
2. run plain `EXPLAIN`
3. if safe, run `EXPLAIN (ANALYZE, BUFFERS)`
4. compare estimated vs actual rows
5. inspect the largest repeated/expensive nodes
6. change query/index/statistics
7. re-measure

Do not run `EXPLAIN ANALYZE` on dangerous write statements or expensive production queries casually because it executes the statement.

## Statistics

Bad cardinality estimates can produce poor plans.

After major data-distribution changes, verify that statistics are current.

## Index tradeoffs

Indexes speed reads but increase:

- insert/update/delete cost
- storage
- maintenance
- vacuum/index overhead

Unused indexes are not free.

## Partial indexes

Useful when a stable selective predicate matches common queries, for example active/unprocessed subsets.

Do not use a partial index if application predicates do not match it reliably.

## Covering/index-only behavior

`INCLUDE` can help some read-heavy queries, but wider indexes cost more to maintain.

Measure before adding.
