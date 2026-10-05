# Cost-Aware Throttling and Budgets

Request-count throttling is not always enough for expensive APIs.

## When to consider it

Useful candidates include:

- analytics/reporting queries
- exports
- expensive searches
- AI/model requests
- third-party provider calls with quota/cost
- large aggregation endpoints

Do not add this complexity to normal CRUD without evidence.

## Possible budget dimensions

Depending on the system:

- rows/bytes scanned
- estimated query cost
- requested time range
- result size
- provider credits/tokens
- concurrent expensive operations

## Enforcement model

```text
identify caller/tenant
      ↓
estimate or measure cost
      ↓
check rolling budget/quota
      ↓
allow or reject
      ↓
emit metrics
```

Use a stable error code and an appropriate status such as 429 when the failure is fundamentally quota/rate related.

## Trustworthy identity

Bucket by authenticated identity/tenant/resource scope, not arbitrary client-controlled headers.

## Metrics

Normalize dynamic routes before using them as metric labels to avoid high cardinality.

## Bypass controls

If allowlists/bypasses exist:

- make them explicit
- audit/measure bypass usage
- do not silently disable all enforcement
