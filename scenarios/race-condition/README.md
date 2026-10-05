# Scenario: Lost Update

## Symptom

Two concurrent requests read the same mutable value, compute a new value in Python, and overwrite each other.

## Expected reasoning

1. State the invariant.
2. Check whether a DB constraint or set-based conditional update can solve it.
3. Prefer `F()`/conditional UPDATE for simple arithmetic/state changes.
4. Use row locks only when correctness requires reading current state before writing.
5. Keep lock transaction short.
6. Test concurrent execution.

## Primary skill

`drf-transactions-concurrency`

## Secondary skill

`postgresql-for-django` when PostgreSQL lock behavior matters.
