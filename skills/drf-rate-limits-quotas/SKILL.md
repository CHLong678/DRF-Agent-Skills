---
name: drf-rate-limits-quotas
description: Rate-limit, quota, concurrency-limit, and cost-budget guidance for Django REST Framework APIs. Use when protecting finite backend/provider capacity, enforcing tenant/user fairness, designing 429 behavior, or limiting expensive operations by request count, concurrency, rows, bytes, credits, tokens, or other cost.
---

# DRF Rate Limits and Quotas

Read backend-patterns/rate-limiting.md for the framework-neutral policy models.

## Start from the protected resource

Define what is finite:

- request handling capacity
- provider quota
- expensive query/export capacity
- concurrent job slots
- tenant entitlement
- bytes/rows/credits/tokens

Do not choose requests-per-minute merely because it is easy.

## Identity

Choose a stable budget owner: user, API key, tenant/company, trusted client, or IP when appropriate.

Do not trust spoofable forwarded headers outside a trusted proxy boundary.

## Request rate vs concurrency

Rate limits control arrivals over time.

Concurrency limits control expensive in-flight work.

For long-running operations, concurrency can be the more direct protection.

## Cost-aware budgets

If request cost varies significantly, consider charging by a bounded proxy such as rows, bytes, time range, provider credits, or tokens.

Validate requested cost before expensive work begins where possible.

## DRF throttling

DRF throttles can be useful for ordinary request-rate policies.

Inspect the actual cache/backend semantics before treating them as strict billing-grade quotas.

For critical entitlement/accounting, use a storage/atomicity model appropriate to the requirement.

## Response contract

Use stable machine-readable error codes.

Use HTTP 429 when the rejection is a rate/quota policy and include Retry-After only when a meaningful retry time exists.

## Routing contract

### Use this skill when
- request rates, concurrency limits, quotas, usage budgets, provider credits, or tenant fairness are primary
- one request can be much more expensive than another and cost-aware admission is needed

### Do not use this skill when
- the main issue is generic provider outage/retries; use drf-resilience-patterns
- the task is authorization/entitlement ownership rather than usage limiting; use drf-permissions-authorization
- the bottleneck is unknown; start with drf-observability

### Inspect first
- resource/capacity being protected
- identity/tenant boundary
- request cost distribution
- cache/counter backend and atomicity
- proxy/header trust
- existing DRF throttle classes
- API error/retry contract

### Related skills
- drf-resilience-patterns, drf-auth-security, drf-capacity-scaling, drf-api-contracts

## Deep reference

- references/drf-throttle-boundaries.md

## Completion criteria

Done when:
- the finite resource and budget owner are explicit
- rate/concurrency/cost accounting matches the real workload
- bypass/fairness/backend-failure behavior is considered
- rejection and Retry-After behavior are tested
