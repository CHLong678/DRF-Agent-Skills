# Code Review Finding Quality

## Finding threshold

A review finding should describe a concrete risk, not merely a preference.

Good finding:

```text
[HIGH] Cross-tenant object lookup is unscoped
Location: orders/views.py:retrieve
Why: get_object_or_404(Order, pk=pk) bypasses tenant-scoped queryset
Failure: authenticated user can request another tenant's order ID
Fix: resolve through get_queryset()/scoped manager and run object permissions
Test: cross-tenant retrieve returns the project's denial response
```

Weak finding:

```text
Consider using a service layer.
```

unless the current structure creates a concrete correctness/reuse/transaction problem.

## Severity

Use severity based on impact and likelihood:

- CRITICAL: broad data/security compromise or destructive failure
- HIGH: exploitable authorization/correctness/data-integrity issue
- MEDIUM: meaningful bug/performance/reliability risk
- LOW: limited edge case or maintainability issue with real consequence

Do not inflate severity for style.

## Review order

1. correctness
2. authorization/security
3. data integrity/concurrency
4. database/performance
5. public API compatibility
6. architecture/maintainability
7. tests

## Minimal safe fix

Prefer the smallest change that closes the failure mode.

Do not turn every review into a rewrite.

## Evidence

When claiming N+1, race, schema break, or security leak, point to the exact path that causes it.
