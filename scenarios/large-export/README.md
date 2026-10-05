# Scenario: Multi-million Row Export

## Symptom

A synchronous DRF export materializes a huge QuerySet and response in memory, timing out workers.

## Expected reasoning

1. Estimate row count, payload size, DB cost, and latency budget.
2. Decide streaming vs durable background artifact generation.
3. Iterate/chunk without QuerySet result-cache explosion.
4. Keep transaction scope bounded.
5. Use a job resource if result is produced asynchronously.
6. Measure DB and memory behavior.

## Primary skill

`drf-bulk-large-data`

## Secondary skills

`drf-background-jobs-contracts`, `drf-celery`, `postgresql-for-django`.
