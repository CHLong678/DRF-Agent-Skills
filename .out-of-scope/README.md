# Out-of-scope Decisions

Record rejected or deferred skill ideas here so the same design debate does not repeatedly reopen.

Current decisions:

- No generic `microservices` skill: too broad; use capacity, event consistency, resilience, runtime, and service-boundary skills.
- No generic `clean-architecture` skill: architecture guidance must remain conditional to Django/project context.
- No separate distributed-lock skill: distributed leases belong under `drf-transactions-concurrency`.
- No Kafka-specific skill yet: add only when repeated Kafka-specific agent failures justify a distinct routing boundary.
- No sharding skill yet: keep partitioning/scaling concepts in backend patterns until executable/project evidence demands a dedicated skill.
- No user-invoked implementation/spec/ticket workflow suite: this repository is specialized backend intelligence, not a general engineering project-management framework.

Add a short rationale here when a tempting new topic is deliberately kept out.
