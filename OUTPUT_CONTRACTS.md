# Agent Output Contracts

Output contracts make recommendations easier to verify and reduce vague "best practice" answers.

Use the contract that matches the task. Do not mechanically print every field when it adds no value.

## Performance/debugging

```text
Observed evidence:
Likely root cause:
Primary skill:
Proposed change:
Why this change:
Compatibility/version constraints:
Risks/trade-offs:
How to verify:
```

Do not claim a root cause without evidence. If evidence is missing, say what to measure first.

## Security/authorization

```text
Protected resource/invariant:
Attack/failure path:
Affected endpoint/path:
Severity:
Authorization/scoping gap:
Minimal safe fix:
Regression tests:
Related background/cache/export paths:
```

## Concurrency

```text
Invariant:
Competing operations:
Current race window:
Chosen primitive:
Why a simpler primitive is insufficient:
Transaction/lock scope:
Deadlock/idempotency considerations:
Concurrency test:
```

## Celery/background processing

```text
Workload/task:
Delivery/retry semantics:
Idempotency strategy:
Commit boundary:
Queue/routing/concurrency:
Timeouts:
Failure/recovery behavior:
Observability:
```

## Production migration

```text
Schema/data change:
Table/workload assumptions:
Generated SQL / DB behavior:
Lock risk:
Rollout sequence:
Backfill plan:
Forward/backward compatibility:
Rollback/retry plan:
Verification:
```

## Code review

```text
[SEVERITY] Finding
Location:
Why it matters:
Concrete failure scenario:
Minimal safe fix:
Missing test:
```

List findings before optional suggestions. Avoid style-only comments unless requested.


## Resilience / dependency failure

```text
Failure mode:
Dependency/deadline:
Retry owner:
Idempotency protection:
Timeout/backoff policy:
Backpressure/load-shedding policy:
Fallback/degradation:
Failure-recovery verification:
```

## Event-driven consistency

```text
Source of truth:
Cross-system consistency requirement:
Dual-write failure window:
Delivery/idempotency strategy:
Ordering/version strategy:
Outbox/relay design if needed:
Retry/DLQ/replay:
Reconciliation/verification:
```

## Capacity / scaling

```text
Observed saturation:
Traffic/workload:
Current process concurrency:
Shared dependency budget:
Scaling option:
Consistency implications:
Headroom/failure assumptions:
Before/after verification:
```

## Service/module boundary

```text
Business operation:
Current callers/interfaces:
Current coupling/problem:
Proposed boundary:
Transaction/side-effect ownership:
Why simpler local code is insufficient:
Migration/refactor scope:
Tests/verification:
```

## Production runtime

```text
Runtime roles:
Critical configuration:
Health/readiness contract:
Shutdown/termination behavior:
Proxy/trust boundary:
Rolling-deploy compatibility:
Observability:
Deployment verification:
```
