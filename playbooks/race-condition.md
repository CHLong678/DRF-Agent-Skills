# Playbook: Race Condition

## Goal

Choose the smallest correct concurrency primitive.

## Flow

1. Load `drf-transactions-concurrency`.
2. Identify the invariant and transaction boundary.
3. Ask whether a DB constraint can enforce the invariant.
4. For simple set-based changes, consider conditional UPDATE or `F()`.
5. If correctness requires reading current state before write, evaluate row locking.
6. If PostgreSQL lock/deadlock behavior matters, load `postgresql-for-django`.
7. If a Celery/external side effect depends on commit, use `on_commit()` and load `drf-celery` when task behavior matters.
8. Test competing operations, not only single-request success.

## Stop conditions

Do not choose `select_for_update()` merely because concurrency exists.
