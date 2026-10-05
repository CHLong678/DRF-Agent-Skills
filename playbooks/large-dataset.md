# Playbook: Large Dataset

## Goal

Choose sync, streaming, or background processing without unbounded memory/DB pressure.

## Flow

1. Load `drf-bulk-large-data`.
2. Estimate rows, payload size, latency budget, memory, and failure semantics.
3. Choose:
   - bounded synchronous work
   - streaming read/export
   - durable background job
4. For background public APIs, load `drf-background-jobs-contracts`.
5. For worker execution, load `drf-celery`.
6. For query plans/indexes/locks, load `postgresql-for-django`.
7. Define chunk/transaction boundaries and partial-success semantics.

## Stop conditions

Do not materialize the entire QuerySet/file unless the size is known and safely bounded.
