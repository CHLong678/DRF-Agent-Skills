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

## Stop rule

Once a specific primary skill explains the decision, do not keep loading adjacent skills unless they materially affect correctness, security, compatibility, or verification.
