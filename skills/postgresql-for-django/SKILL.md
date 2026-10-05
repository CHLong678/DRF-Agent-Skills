---
name: postgresql-for-django
description: PostgreSQL-specific production guidance for Django/DRF. Use when optimizing queries/indexes, analyzing EXPLAIN plans, choosing composite/partial/GIN indexes, debugging locks/deadlocks, or using PostgreSQL-specific concurrency and JSON/search features.
---

# PostgreSQL for Django

## Scope

Use this skill only when the project actually uses PostgreSQL.

Do not present PostgreSQL-specific behavior as generic Django behavior.

## Measure queries with EXPLAIN

Use `EXPLAIN` to inspect planner decisions and `EXPLAIN ANALYZE` only when it is safe to execute the statement.

Remember that `ANALYZE` actually runs the query.

Inspect:

- estimated vs actual rows
- scan type
- joins
- sort/hash operations
- loops
- buffers when available
- stale statistics

## Indexes

Index decisions should follow real query patterns.

Evaluate:

- equality vs range predicates
- join columns
- ordering
- composite index column order
- partial indexes for selective subsets
- expression indexes
- GIN/GiST for supported workloads
- write/update overhead

Do not add a standalone index merely because a field appears in a filter.

## Composite indexes

Match the index to the query pattern.

An index on `(tenant_id, created_at)` may be useful when queries consistently constrain tenant then range/order by time.

Do not assume reversing column order is equivalent.

## Locks

Understand row/table locks before using `select_for_update()`, DDL, or long transactions.

Keep locks short and acquire multiple locks in a consistent order to reduce deadlock risk.

## Deadlocks

PostgreSQL detects deadlocks and aborts one transaction.

Best defense:

- consistent lock order
- short transactions
- small lock scope
- bounded retry for recognized transient deadlock failures when business semantics permit

## Concurrent indexes

For production index builds on large hot tables, consider PostgreSQL concurrent index creation.

See `django-migrations-production` for Django integration.

## JSON/Array/search

PostgreSQL-specific JSON/Array/full-text/trigram features can be valuable, but use indexes/operators that match measured workload.

## Deep references

- `references/indexes-and-explain.md`
- `references/locking-and-deadlocks.md`

## Authoritative sources

- PostgreSQL EXPLAIN: https://www.postgresql.org/docs/current/using-explain.html
- PostgreSQL indexes: https://www.postgresql.org/docs/current/indexes-intro.html
- PostgreSQL CREATE INDEX: https://www.postgresql.org/docs/current/sql-createindex.html
- PostgreSQL locking: https://www.postgresql.org/docs/current/explicit-locking.html

## Routing contract

### Use this skill when
- PostgreSQL EXPLAIN/planner/indexes/locks/deadlocks/JSON/GIN/GiST or DB-specific behavior is primary

### Do not use this skill when
- the project does not use PostgreSQL
- the main problem is ORM N+1/query composition without DB-plan evidence; use `drf-orm-performance`

### Inspect first
- actual PostgreSQL version
- generated SQL
- EXPLAIN plan when safe
- table/index statistics
- lock/transaction behavior
- workload read/write balance

### Related skills
- `drf-orm-performance`, `drf-transactions-concurrency`, `django-migrations-production`
