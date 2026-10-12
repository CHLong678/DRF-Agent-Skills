# Scenario: Hard Intermittent Backend Bug

## Symptom

A DRF endpoint intermittently returns stale or incorrect state after a refactor. The path crosses request handling, Celery, and database code, and speculative fixes have not solved it.

## Expected reasoning

1. Build one tight feedback loop that reproduces the exact failure.
2. Minimise the failing case before proposing a fix.
3. Form a small set of falsifiable hypotheses.
4. Add discriminating instrumentation for query/transaction/task/order behavior.
5. Select the owning domain skill only after evidence identifies the boundary.
6. Apply the smallest root-cause fix.
7. Add a regression test/check and rerun the original repro.

## Primary skill

`backend-diagnosing-bugs`

## Secondary skills

Only the domain skills supported by evidence, such as `drf-transactions-concurrency`, `drf-celery`, or `drf-observability`.
