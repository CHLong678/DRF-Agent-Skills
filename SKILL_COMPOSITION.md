# Skill Composition

Use one primary skill for the main decision, then load secondary skills in a deliberate order.

## Production async export

1. drf-bulk-large-data — choose sync/stream/background and chunking
2. drf-background-jobs-contracts — define the public 202/job contract
3. drf-celery — implement worker/retry/idempotency behavior
4. postgresql-for-django — optimize the actual data access
5. drf-capacity-scaling — verify capacity and concurrency budget

## Cross-system write + event

1. drf-event-driven-consistency — define consistency model/outbox/idempotency
2. drf-transactions-concurrency — define local DB transaction/invariant
3. drf-celery — implement dispatch/consumer details
4. drf-observability — define lag/failure/replay visibility

## Tenant-safe cached list API

1. drf-auth-security — define tenant isolation
2. drf-permissions-authorization — define list/object/action authorization
3. drf-caching — define tenant/permission-aware key and invalidation
4. drf-testing — add cross-tenant/cache regression tests

## Provider integration under overload

1. drf-resilience-patterns — timeout/retry/backpressure/fallback
2. drf-webhooks-integrations — if provider callbacks are involved
3. drf-celery — if durable background work is used
4. drf-observability — verify error, latency, saturation, recovery

## Large production migration

1. django-migrations-production — rollout/expand-contract/backfill
2. postgresql-for-django — lock/index/database behavior
3. drf-capacity-scaling — resource/headroom impact for large backfill
4. django-production-runtime — rolling deploy compatibility

## Workflow-heavy API

1. django-service-boundaries — decide reusable application boundary
2. drf-transactions-concurrency — own transaction/invariant
3. drf-celery or drf-resilience-patterns — side-effect execution
4. drf-views — keep HTTP orchestration thin and explicit

## Composition stop rule

Do not load the next skill merely because it appears in a bundle. Load it only when that boundary exists in the actual task.
