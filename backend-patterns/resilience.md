# Resilience Patterns

## Goal

Keep partial dependency failures from becoming whole-system failures.

## Timeout budget

Every remote dependency call should have an explicit bounded timeout appropriate to the caller's end-to-end latency budget.

Do not let default socket/client timeouts define production behavior accidentally.

A timeout is not merely a performance setting; it bounds resource occupancy.

## Retry

Retry only failures that are plausibly transient.

Before retrying ask:

- is the operation idempotent?
- can the provider receive the request twice?
- does the failure indicate overload?
- will retrying amplify the outage?
- is there enough deadline left?

Use bounded attempts, exponential backoff where appropriate, and jitter to avoid synchronized retry storms.

Do not retry deterministic validation/business failures.

## Retry amplification

If client, API, worker, and provider SDK all retry independently, the total attempt count can multiply unexpectedly.

Assign retry ownership deliberately.

## Circuit breaker

A circuit breaker can temporarily stop calls to a dependency that is persistently failing.

Useful when failure is sustained, calls are expensive, and fallback/degradation exists.

Avoid adding a circuit breaker when ordinary timeouts plus bounded retries already solve the problem.

## Bulkhead / isolation

Separate unrelated workloads so one saturated dependency or queue does not consume every resource.

Examples:

- separate Celery queues for long vs latency-sensitive tasks
- bounded concurrency per external provider
- resource isolation only where operationally justified

## Backpressure

When producers can generate work faster than consumers process it, the system needs a pressure signal.

Possible responses:

- bound queue size
- reject or defer work
- reduce producer rate
- shed low-priority work
- apply concurrency limits
- coalesce duplicate work

An unbounded queue converts overload into delayed failure.

## Load shedding

Under overload, rejecting some work early can preserve useful service for the rest.

Define which requests can be rejected, status/error contract, retry guidance, priority tiers, and tenant fairness.

## Graceful degradation

Examples:

- stale cache for non-critical read
- omit optional enrichment
- enqueue later processing
- disable expensive secondary feature

Do not silently degrade correctness-sensitive operations such as payments or state transitions.

## Verification

Test dependency timeout, 429/5xx, slow dependency, retry storm, queue saturation, recovery, and resource usage during failure.
