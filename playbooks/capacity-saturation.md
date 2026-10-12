# Playbook: Capacity Saturation

## Goal

Scale the constrained resource instead of amplifying pressure on it.

## Flow

1. If the saturated tier is unknown, start with drf-observability.
2. Once evidence exists, use drf-capacity-scaling.
3. Measure web concurrency, Celery concurrency, DB connections, DB CPU/I/O/locks, cache/broker capacity, provider quotas, and queue age.
4. Build a shared concurrency budget across process roles.
5. Reduce slow work before simply adding more callers.
6. Scale only tiers whose downstream dependencies have headroom.
7. Reserve headroom for bursts, retries, deploy overlap, and node loss.
8. Re-measure throughput and tail latency.

## Stop conditions

Do not assume horizontal scaling increases throughput when a shared database/provider is already saturated.
