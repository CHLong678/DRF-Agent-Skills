# Skill Routing and Precedence

Use this file when more than one skill appears relevant.

## Routing principles

1. Choose one **primary skill** for the main decision.
2. Load **secondary skills** only when the task crosses a real boundary.
3. Prefer the most specific skill over a broad review/security/core skill.
4. Use `drf-skill-router` only when the correct primary skill is unclear or the task spans several domains.
5. Do not load every potentially related skill.

## Precedence matrix

| Task signal | Primary skill | Secondary skills |
|---|---|---|
| N+1, queryset shape, select/prefetch | `drf-orm-performance` | `drf-serializers` |
| EXPLAIN, PostgreSQL indexes, locks | `postgresql-for-django` | `drf-orm-performance` |
| API slow but bottleneck unknown | `drf-observability` | route after measurement |
| filtering, ordering, pagination, COUNT | `drf-filtering-pagination` | `postgresql-for-django` |
| Redis/HTTP/application cache | `drf-caching` | `drf-auth-security` |
| serializer fields/validation/representation | `drf-serializers` | `drf-api-contracts` |
| API versioning/schema/backward compatibility | `drf-api-contracts` | `drf-serializers` |
| APIView/ViewSet/action/lifecycle | `drf-views` | `drf-core` |
| permission class/object/list/create auth | `drf-permissions-authorization` | `drf-auth-security` |
| BOLA/IDOR/tenant/security review | `drf-auth-security` | `drf-permissions-authorization` |
| transaction/race/row lock/idempotency | `drf-transactions-concurrency` | `postgresql-for-django` |
| Celery retry/ack/queue/prefetch/backlog | `drf-celery` | `drf-transactions-concurrency` |
| 202/job status/progress/cancel/result API | `drf-background-jobs-contracts` | `drf-celery` |
| large import/export/bulk/queryset memory | `drf-bulk-large-data` | `drf-celery`, `postgresql-for-django` |
| webhook signature/duplicate/order/retry | `drf-webhooks-integrations` | `drf-celery` |
| async view/ASGI/sync-async boundary | `drf-async` | `drf-celery` only if work should leave request |
| tests/test strategy/regression | `drf-testing` | skill for behavior under test |
| PR/diff review | `drf-code-review` | load specific domain skill for findings |
| production migration/backfill/schema rollout | `django-migrations-production` | `postgresql-for-django` |
| slow Django admin | `django-admin-large-data` | `postgresql-for-django` |
| slow django.setup/import graph | `django-startup-performance` | `django-architecture-enforcement` |
| CI/static architecture/security invariant | `django-architecture-enforcement` | domain skill defining invariant |
| general architecture/boundaries | `drf-core` | more specific skill after classification |
| hard/intermittent backend bug with unknown root cause | `backend-diagnosing-bugs` | evidence-driven domain skill after repro |
| timeout/retry/jitter/circuit-breaker/backpressure/load shedding | `drf-resilience-patterns` | `drf-observability`, `drf-celery` |
| DB + message/event consistency, outbox, compensation, DLQ | `drf-event-driven-consistency` | `drf-celery`, `drf-transactions-concurrency` |
| saturation, process concurrency, DB connection budget, replicas | `drf-capacity-scaling` | `drf-observability`, `postgresql-for-django` |
| service/selectors/module/facade/adapter boundaries | `django-service-boundaries` | `drf-core`, `django-architecture-enforcement` |
| health/readiness, graceful shutdown, proxy trust, process roles | `django-production-runtime` | `drf-observability`, `drf-capacity-scaling` |

| cost-aware rate/concurrency quota, tenant fairness | `drf-rate-limits-quotas` | `drf-capacity-scaling`, `drf-api-contracts` |

| large file upload/download, presigned URL, object lifecycle | `drf-files-object-storage` | `drf-auth-security`, `drf-reconciliation-repair` |

| reconciliation, repair, replay, poison records | `drf-reconciliation-repair` | `drf-event-driven-consistency`, `drf-bulk-large-data` |

| distributed lease/Redis lock expiry/fencing | `drf-transactions-concurrency` | `postgresql-for-django` |

## Important overlap rules

### Security vs permissions

Use `drf-permissions-authorization` for:
- permission classes
- list/detail/create authorization
- custom action authorization
- role/capability matrices

Use `drf-auth-security` for:
- BOLA/IDOR
- tenant isolation
- authentication/token security
- mass assignment
- abuse/throttling/CSRF/CORS/SSRF

### Celery vs job contract

Use `drf-celery` for worker/broker/task behavior.
Use `drf-background-jobs-contracts` for the public HTTP/job-resource contract.

### ORM vs PostgreSQL

Use `drf-orm-performance` for ORM access shape and query count.
Use `postgresql-for-django` for planner/index/lock/database-specific behavior.

### Async vs Celery

Use `drf-async` when work remains in the request and benefits from concurrent I/O.
Use `drf-celery` when work should be durable, retried, scheduled, or continue after the response.

### Bulk vs Celery

Use `drf-bulk-large-data` first to decide sync/stream/background and chunking.
Load `drf-celery` only when the chosen execution model uses workers.

### Resilience vs Celery

Use `drf-resilience-patterns` for timeout budgets, retry ownership, overload/backpressure, circuit breaking, and graceful degradation.
Use `drf-celery` for task/worker/broker implementation details.

### Event consistency vs transactions

Use `drf-transactions-concurrency` when one database transaction can enforce the invariant.
Use `drf-event-driven-consistency` when correctness spans a DB plus broker/provider/other system.

### Capacity vs observability

Use `drf-observability` when the saturated tier is unknown.
Use `drf-capacity-scaling` after evidence shows a capacity/saturation/scaling decision is needed.

### Service boundaries vs core

Use `django-service-boundaries` when the question is where reusable business logic/module boundaries should live.
Use `drf-core` for broader DRF architecture when no more specific boundary decision dominates.

### Production runtime vs startup performance

Use `django-production-runtime` for runtime process/deployment behavior.
Use `django-startup-performance` when import/django.setup startup time is the problem.

### Rate limits vs resilience

Use `drf-rate-limits-quotas` when admission/fairness/budget policy is the main decision.
Use `drf-resilience-patterns` when dependency failure, retry, timeout, or overload recovery is the main decision.

### File/object storage vs bulk data

Use `drf-files-object-storage` for transfer/lifecycle/security of files or object-store objects.
Use `drf-bulk-large-data` for large database/query/import/export processing.

### Reconciliation vs migration

Use `drf-reconciliation-repair` for live business-state inconsistency, replay, or repair.
Use `django-migrations-production` for schema/data migration rollout.

### Distributed locking vs DB concurrency

Distributed locking remains under `drf-transactions-concurrency`. Prefer constraints, conditional updates, row locks, idempotency, or partitioned ownership before a distributed lease.

### Diagnosis vs observability

Use `backend-diagnosing-bugs` when the problem is a hard/intermittent bug or prior speculative fixes failed and you need a tight reproducible feedback loop.
Use `drf-observability` when the primary task is instrumenting/measuring an unknown production performance or reliability question.

## Stop rule

Once a specific primary skill explains the decision, do not keep loading adjacent skills unless they materially affect correctness, security, compatibility, or verification.
