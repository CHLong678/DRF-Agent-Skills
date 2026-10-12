# Capacity and Scaling Patterns

## Start with saturation

Before scaling, identify which resource is saturated:

- CPU
- memory
- web worker slots
- DB connections
- DB CPU/I/O/locks
- Redis
- broker queue/consumer capacity
- external provider quota
- network bandwidth

Scaling the wrong tier can make the bottleneck worse.

## Horizontal vs vertical scaling

Vertical scaling increases resources per node. Horizontal scaling adds nodes or worker processes.

Horizontal scaling only helps when the workload and shared dependencies can support it.

Doubling web workers can double concurrent database demand and move the bottleneck to PostgreSQL.

## Queueing

Queue depth alone is incomplete.

Observe arrival rate, service rate, oldest-message age, active/reserved/unacked work, runtime distribution, and retry rate.

A growing queue means sustained production rate exceeds completion rate or consumers are impaired.

## Little's Law intuition

For a stable system, concurrency is related to throughput multiplied by time-in-system.

Longer task/request durations consume more concurrency even when request rate stays constant.

## Database connections

Web, Celery, and management jobs can jointly exhaust PostgreSQL connection capacity.

Estimate total potential concurrency rather than configuring each process in isolation.

Connection pooling does not remove database capacity limits.

## Read replicas

Read replicas can offload eligible reads, but introduce consistency concerns.

Define acceptable replica lag, read-after-write requirements, transaction consistency, and whether auth/security reads can tolerate staleness.

Critical state reads may need the primary.

## Cache scaling

Watch for hot keys, cache stampede, oversized values, memory pressure/eviction, tenant key cardinality, and dependency on cache availability.

## Capacity headroom

Plan headroom for bursts, deploy overlap, retry storms, node loss, and batch jobs.
