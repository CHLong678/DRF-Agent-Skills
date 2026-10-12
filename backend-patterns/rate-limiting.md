# Rate Limiting and Quotas

## Goal

Protect finite capacity and enforce fair usage with a policy tied to a real resource or abuse model.

## Requests per time window

Simple fixed/sliding windows can limit request frequency.

Useful for basic abuse protection, but request count alone is weak when requests have very different cost.

## Token bucket

Tokens replenish over time and requests consume tokens.

Useful when short bursts are allowed but sustained rate must be bounded.

## Leaky bucket / paced output

Smooths bursts into a steadier processing rate.

Useful when downstream capacity is sensitive to spikes.

## Concurrency limit

Bound the number of expensive operations in flight.

Often more directly useful than requests/minute for:

- long exports
- provider calls
- CPU-heavy work
- limited DB/provider slots

## Cost-aware quota

Charge by a cost proxy such as:

- rows scanned/exported
- time range
- file size
- provider credits
- tokens
- result size

Prefer this when one request can be orders of magnitude more expensive than another.

## Identity

Define who owns the budget:

- IP
- authenticated user
- API key
- tenant/company
- endpoint/resource class

Do not trust spoofable proxy headers unless the proxy boundary is trusted.

## Distributed counters

Distributed rate limits need atomic/consistent counter semantics appropriate to the policy.

Approximation may be acceptable for overload protection, but not always for billing/entitlement.

## Response contract

For rejected requests define:

- status code, commonly 429 for rate/quota policy
- stable machine-readable error code
- Retry-After when a meaningful retry time exists

## Fairness

One noisy tenant should not consume the entire shared budget when multi-tenant fairness matters.

## Verification

Test burst, sustained load, multiple identities, bypass attempts, clock/window edges, and backend/cache failure.
