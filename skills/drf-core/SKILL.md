---
name: drf-core
description: Production Django REST Framework architecture and API implementation guidance. Use when designing or modifying DRF endpoints, deciding where business logic belongs, structuring services, handling API errors, or preserving API compatibility.
---

# DRF Core

Use these rules when implementing or restructuring Django REST Framework code.

## First principles

1. Inspect nearby project code before introducing new patterns.
2. Preserve existing API behavior unless the task explicitly changes it.
3. Keep HTTP orchestration in views and reusable business workflows outside views.
4. Keep serializers focused on representation, deserialization, and validation.
5. Do not introduce a service/repository/domain abstraction unless it reduces real duplication, transaction complexity, or coupling.
6. Prefer explicit, readable code over hidden behavior.
7. Minimize unrelated refactors.

## Responsibility boundaries

### Views

Views should primarily handle:

- authentication and permissions
- request parsing already delegated to serializers/parsers
- selecting serializer/queryset behavior
- HTTP status and response concerns
- invoking a service/domain operation

Avoid long multi-model workflows directly in views.

### Serializers

Serializers should primarily handle:

- input/output shape
- field validation
- cross-field validation
- representation
- straightforward object creation/update when behavior is local and simple

Avoid external API calls, Celery dispatch, emails, and unrelated writes inside validation.

### Services/domain functions

Use a service/domain function when logic:

- coordinates multiple models
- requires an explicit transaction boundary
- is reused by multiple endpoints/tasks/commands
- invokes external systems
- has meaningful domain rules that deserve isolated tests

Keep functions explicit about required inputs and returned values.

## Error handling

- Use DRF validation errors for request-validation failures.
- Use explicit domain/application exceptions for business-state conflicts.
- Map exceptions to stable API responses in one predictable layer.
- Do not leak stack traces, database errors, credentials, or internal identifiers.
- Prefer stable error codes where clients may branch on error type.

## API compatibility

Before changing response or request behavior, check:

- field names and nullability
- default values
- status codes
- pagination shape
- ordering
- filtering semantics
- error response shape
- permission behavior

Do not silently rename or remove public fields.

## Read/write separation

Separate serializers when request and response shapes differ significantly. Do not force one serializer to handle incompatible read/write responsibilities through many conditional fields.

## Side effects

When a successful database commit is a prerequisite for a side effect, schedule the side effect with `transaction.on_commit()`.

Example:

```python
with transaction.atomic():
    order = create_order_record(...)
    transaction.on_commit(lambda: sync_order.delay(order.pk))
```

Do not dispatch a worker inside an uncommitted transaction when the worker immediately reads committed database state.

## Definition of done

For non-trivial endpoint changes, verify:

- validation behavior
- permission behavior
- query count/performance risk
- transaction consistency
- error responses
- backward compatibility
- tests for changed behavior

## Routing contract

### Use this skill when
- deciding DRF architecture/boundaries before a more specific domain is known
- deciding whether logic belongs in views, serializers, services, or domain functions
- reviewing broad request-to-domain orchestration

### Do not use this skill when
- the problem is specifically ORM performance, permissions, Celery, migrations, caching, or another dedicated domain
- the task is only a PR/diff review; use `drf-code-review`

### Inspect first
- nearby views/serializers/models/services
- project conventions and tests
- transaction and side-effect boundaries

### Related skills
- `drf-views`, `drf-serializers`, `drf-transactions-concurrency`
- use the most specific related skill as primary once the problem is classified
