# Scenario: Cost-aware API Quota

## Symptom

A DRF endpoint can be cheap or extremely expensive depending on the requested date range and result size. Requests-per-minute allows one tenant to consume disproportionate backend capacity.

## Expected reasoning

1. Identify the finite resource being protected.
2. Measure request-cost distribution.
3. Define tenant/user budget ownership.
4. Choose a bounded cost proxy such as rows, bytes, time range, or concurrent jobs.
5. Reject or reshape requests before expensive work begins.
6. Define stable 429/error/retry behavior.
7. Test tenant fairness and bypass paths.

## Primary skill

`drf-rate-limits-quotas`

## Secondary skills

`drf-capacity-scaling`, `drf-api-contracts`, and `drf-auth-security`.
