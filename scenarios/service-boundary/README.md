# Scenario: Workflow-heavy DRF View

## Symptom

A ViewSet action updates several models, calls an external provider, and schedules a task. The same operation is now needed from a management command.

## Expected reasoning

1. Identify the business operation independently of HTTP.
2. Locate its transaction boundary and side effects.
3. Extract a reusable application/service function if it improves traceability and reuse.
4. Keep request parsing, auth, response/status handling in DRF.
5. Keep provider/Celery details at appropriate integration boundaries.
6. Avoid adding selectors/services for trivial operations.
7. Test the workflow through more than one interface where relevant.

## Primary skill

django-service-boundaries

## Secondary skills

drf-core, drf-transactions-concurrency, and drf-celery.
