---
name: drf-caching
description: Django REST Framework caching and Redis guidance. Use when adding cache layers, HTTP caching, ETags, cache invalidation, per-user/tenant cache keys, or diagnosing cache correctness and stampede issues.
---

# DRF Caching

## Cache only with a correctness model

Before caching, define:

- what is cached
- who may read it
- cache key dimensions
- TTL
- invalidation trigger
- stale-data tolerance

A cache without an invalidation/security model is a correctness risk.

## Cache key design

Include every dimension that can change the response, such as:

- object/resource identifier
- API version
- authenticated user/account/tenant when response is scoped
- locale
- relevant query parameters
- permission-sensitive variants

Never share a cached private response across users or tenants accidentally.

## Cache levels

Possible layers include:

- application/object/query-derived cache
- per-view cache
- low-level Django cache API
- HTTP cache semantics
- reverse proxy/CDN

Choose the lowest-complexity layer that meets the requirement.

## HTTP caching

For safe cacheable responses, consider:

- `Cache-Control`
- `ETag`
- conditional requests
- `Last-Modified`

Do not mark personalized or authorization-sensitive data as publicly cacheable.

## Invalidation

Prefer explicit invalidation tied to the write path when freshness matters.

Be cautious with signal-based invalidation when:

- bulk updates bypass expected signals
- writes happen through multiple systems
- invalidation ordering matters

Document eventual-consistency expectations.

## Redis

Redis is useful for shared application caching, but:

- set sensible TTLs
- namespace keys
- avoid unbounded high-cardinality keys
- understand serialization cost
- plan behavior when Redis is unavailable

Do not make correctness depend on a cache entry existing unless the cache is intentionally being used as durable state, in which case call it state rather than cache.

## Stampede / hot keys

For expensive hot data, consider:

- lock/single-flight behavior
- stale-while-revalidate style patterns
- jittered TTLs
- prewarming when justified

Do not add distributed locks casually; they introduce their own failure modes.

## Transactions

If invalidation or population depends on committed DB state, use `transaction.on_commit()` where appropriate.

## Measure

Validate:

- hit ratio
- latency improvement
- memory/key growth
- invalidation correctness
- stale-response behavior

Do not keep a cache solely because it exists.

## Routing contract

### Use this skill when
- Redis/application/HTTP caching, cache keys, TTL, invalidation, ETag, or stampede behavior is primary

### Do not use this skill when
- the bottleneck is not yet identified; start with `drf-observability`
- the main issue is tenant authorization rather than cache behavior

### Inspect first
- exact data being cached
- caller/tenant/permission dimensions
- invalidation trigger
- freshness tolerance
- transaction boundary
- observed hit/miss behavior

### Related skills
- `drf-observability`, `drf-auth-security`, `drf-transactions-concurrency`
