# Sources and Adaptation

The backend-pattern layer is synthesized from high-signal backend/system-design repositories plus authoritative framework/database documentation.

## donnemartin/system-design-primer

Used for performance vs scalability, latency vs throughput, availability/consistency trade-offs, replication, caching, partitioning, and asynchronous processing.

Adaptation: use its trade-off framing; do not copy interview-oriented architecture prescriptions blindly.

## ByteByteGoHq/system-design-101

Used as a broad pattern map for API design, delivery semantics, optimistic/pessimistic locking, read replicas, queues/event-driven systems, caching, database scaling, and production case studies.

Adaptation: treat high-level explanations as pattern discovery, then anchor framework-sensitive behavior in official Django/DRF/PostgreSQL/Celery docs.

## binhnguyennus/awesome-scalability

Used as a curated index for large-scale reliability and performance patterns.

Adaptation: use it to broaden failure modes and trade-offs, not as the sole authority for exact implementation behavior.

## HackSoftware/Django-Styleguide

Used for interface vs core separation, service/application functions, selectors/read paths, and avoiding hidden workflows in serializers/views/signals.

Adaptation: this source is explicitly opinionated. These ideas remain conditional and services/selectors are not mandatory for simple CRUD.

## Sairyss/domain-driven-hexagon

Used for module boundaries, public facades, ports/adapters, bounded contexts, and dependency direction.

Adaptation: apply only when domain/team/codebase complexity justifies it. Do not impose full DDD/hexagonal architecture on ordinary Django applications.

## cookiecutter/cookiecutter-django

Used as a production-project reference for environment-based configuration, PostgreSQL, Celery/process separation, monitoring, containers, and secure production defaults.

Adaptation: current versions target newer Django/Python than this repository baseline, so concepts are adapted and version-sensitive settings must be gated.

## Primary-authority rule

For exact version-sensitive behavior, prefer official Django, DRF, Celery, PostgreSQL, RFC/protocol, and provider documentation.


## Additional pattern grounding

The caching, rate-limiting, distributed-locking, recovery, and object-storage documents are synthesized from the same system-design sources above and must be cross-checked against the exact cache, proxy, storage, broker, and database provider documentation used by the target project.

For distributed locks, treat provider recipes as implementation details rather than proof that a lease enforces the business invariant. For file/object storage, use provider documentation for exact presigned URL, multipart upload, checksum, lifecycle, and consistency semantics.
