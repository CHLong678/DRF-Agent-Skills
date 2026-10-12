# Production Runtime Checklist

## Startup

- validate critical configuration
- avoid unnecessary remote calls at import/startup
- identify migration responsibility
- record build/version metadata

## Web

- bounded request timeout
- trusted proxy configuration
- health/readiness behavior
- graceful termination
- realistic DB connection budget

## Celery

- queue ownership
- concurrency
- task time limits where appropriate
- graceful shutdown/requeue behavior
- broker/result backend failure handling

## Deploy

- old/new version coexistence
- migration compatibility
- event/API compatibility
- rollback path
- monitoring during rollout
