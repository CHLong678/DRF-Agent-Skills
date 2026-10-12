# Scenario: Runtime Readiness and Graceful Shutdown

## Symptom

A deployment starts routing traffic before the Django process can safely serve requests, while Celery workers are terminated with in-flight tasks.

## Expected reasoning

1. Separate process liveness from readiness.
2. Identify only dependencies/configuration that should block readiness.
3. Keep probes lightweight.
4. Define shutdown sequence and termination grace.
5. Align web/task timeouts with shutdown grace.
6. Preserve broker delivery/requeue semantics during worker shutdown.
7. Verify old/new version coexistence during rolling deployment.

## Primary skill

django-production-runtime

## Secondary skills

drf-capacity-scaling, drf-celery, and drf-observability.
