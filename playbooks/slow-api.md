# Playbook: Slow DRF API

## Goal

Find the bottleneck before changing code.

## Flow

1. Start with `drf-observability`.
2. Measure latency, query count, DB time, external-call time, serialization time, response size, and cache behavior.
3. Route by evidence:
   - N+1/query count -> `drf-orm-performance`
   - filter/order/count -> `drf-filtering-pagination`
   - EXPLAIN/index/lock -> `postgresql-for-django`
   - repeated expensive reads -> `drf-caching`
   - serializer CPU/hidden relation access -> `drf-serializers`
4. Verify the improvement with the same measurement.

## Stop conditions

Do not add cache/index/select_related until evidence identifies the bottleneck.
