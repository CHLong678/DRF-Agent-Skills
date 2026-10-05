---
name: drf-serializers
description: Django REST Framework serializer design and validation guidance. Use when creating or reviewing Serializer/ModelSerializer classes, nested serializers, create/update methods, validation, read/write fields, or serializer performance.
---

# DRF Serializers

## Choose the serializer deliberately

Use `ModelSerializer` when model-backed CRUD maps naturally to API fields.
Use `Serializer` when the payload represents a command, aggregate, external structure, or workflow rather than one model.

## Validation layers

Use:

- field validators / `validate_<field>()` for one-field rules
- `validate()` for cross-field request rules
- database constraints for invariants that must remain true regardless of entry point
- service/domain validation for business rules spanning multiple aggregates or side effects

Do not use validation methods to perform surprising writes or external side effects.

## Partial updates

When supporting PATCH:

- respect `serializer.partial`
- do not assume omitted fields exist in `attrs`
- distinguish omitted from explicit `null`
- avoid overwriting omitted fields with defaults unintentionally

## Create/update

Keep `create()`/`update()` small when possible.

Move logic into a service when the operation:

- touches several models
- needs locks or transaction orchestration
- dispatches async work
- calls external systems
- is shared outside the serializer

## Read/write serializers

Use separate serializers when input and output differ substantially, for example IDs on write and nested objects on read.

```python
class OrderCreateSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1)

class OrderDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
```

## Query awareness

Serializer fields can trigger hidden queries.

Audit:

- dotted `source=` attributes
- nested serializers
- `SerializerMethodField`
- reverse relations
- properties that query the database

Optimize the view/queryset rather than issuing queries repeatedly in serializer methods.

## Uniqueness

Understand the distinction between serializer validation and database enforcement.

A uniqueness validator improves request feedback but is not sufficient protection against races. Keep database unique constraints for true invariants and handle `IntegrityError` where concurrent writes can collide.

## Context

Use `self.context` for request/view-aware serialization when necessary, but avoid using it as an unstructured dependency container.

## Avoid

- DB writes in `validate()`
- network calls in field validation
- N+1 queries from method fields
- giant serializers coordinating full business workflows
- mutating input data unexpectedly
- exposing write-only secrets in output

## Review checklist

Check:

- required/read_only/write_only correctness
- PATCH semantics
- null vs blank semantics
- uniqueness/race safety
- nested relation query behavior
- stable error messages/codes
- separation of request and response shapes
