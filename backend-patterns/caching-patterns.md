# Caching Patterns

## Goal

Reduce repeated expensive work without making correctness, tenant isolation, or freshness implicit.

## Cache-aside

The application reads cache first, then falls back to the source of truth and fills the cache.

Useful when reads dominate and stale windows are acceptable.

Failure modes:

- stampede on miss/expiry
- stale data after write
- key cardinality explosion
- tenant/permission leakage from incomplete keys

## Write-through

Update the cache as part of the write path.

This can improve freshness but couples write availability to the cache unless carefully designed.

Do not make a non-durable cache the only copy of business state.

## Write-behind

The cache accepts a write and persistence happens later.

This changes durability semantics and is inappropriate for correctness-sensitive state unless the architecture explicitly accepts that risk.

## Stale-while-revalidate

Serve a bounded stale value while one caller refreshes it.

Useful for expensive non-critical reads.

Define:

- maximum stale age
- who refreshes
- what happens when refresh fails

## Stampede prevention

Options include:

- single-flight/coalescing
- short distributed lease used only for refresh coordination
- TTL jitter
- prewarming
- stale-while-revalidate

Do not hold long distributed locks around ordinary request work.

## Key design

A cache key must include every dimension that changes the allowed or correct result.

Common dimensions:

- tenant
- user/role/permission context
- resource/version
- normalized filter parameters
- locale
- schema/representation version

## Invalidation

Choose one:

- explicit invalidation on write
- short TTL
- versioned namespace/key
- event-driven invalidation
- accept bounded staleness

Do not claim cache correctness without an invalidation/freshness story.

## Cache failure

Decide whether cache outage should:

- fall back to source of truth
- fail closed
- reject overload-prone requests

Fallback can overload the database, so degraded mode needs capacity thinking.

## Verification

Measure hit rate, miss latency, source load, memory/cardinality, stale behavior, and stampede behavior.
