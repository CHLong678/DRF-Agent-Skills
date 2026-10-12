# Backend Patterns

This directory is a framework-neutral knowledge layer for backend engineering patterns used by the DRF/Django skills.

The purpose is to separate backend principle -> framework adaptation -> Django/DRF implementation.

A pattern here is not automatically a recommendation. Every pattern has a context, trade-offs, failure modes, and signals for when not to use it.

## Catalog

- resilience.md — timeouts, retries, jitter, circuit breaking, bulkheads, load shedding, backpressure
- event-driven-consistency.md — delivery semantics, idempotency, outbox, dual-write risk, compensation, ordering
- capacity-scaling.md — saturation, horizontal scaling, queues, database/cache pressure, read replicas
- service-module-boundaries.md — application/service boundaries, selectors/read paths, modules, facades, ports/adapters
- production-runtime.md — process boundaries, configuration, health/readiness, graceful shutdown, dependency failures

## Use rules

1. Start from the failure mode or invariant, not the pattern name.
2. Prefer the smallest mechanism that solves the problem.
3. Do not add distributed-system complexity to a local transaction problem.
4. Separate correctness requirements from scalability optimizations.
5. Treat every pattern as a trade-off.
6. Verify the chosen pattern under realistic failure/load conditions.

Framework-specific skills should reference these files rather than duplicating generic backend theory.

See SOURCES.md for source repositories and adaptation rules.
