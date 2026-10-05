---
name: drf-serializers
description: Django REST Framework serializer design and validation guidance. Use when creating or reviewing Serializer/ModelSerializer classes, nested serializers, create/update methods, validation, read/write fields, computed fields, or serializer performance.
---

# DRF Serializers

## Choose the serializer deliberately

Use `ModelSerializer` when model-backed CRUD maps naturally to API fields.
Use `Serializer` when the payload represents a command, aggregate, external structure, or workflow rather than one model.

## Explicit field allowlists

For externally consumed serializers, prefer an explicit `fields = [...]` allowlist.

Avoid `fields = "__all__"` when new model fields could accidentally become API-readable or writable.

Pay particular attention to ownership/tenant fields, privilege/role fields, internal workflow state, secrets/credentials, audit metadata, and billing/system flags.

## Validation layers

Use:

- field validators / `validate_<field>()` for one-field rules
- `validate()` for cross-field request rules
- database constraints for invariants that must remain true regardless of entry point
- service/domain validation for business rules spanning multiple aggregates or side effects

Do not use validation methods to perform surprising writes or external side effects.

## Unknown input fields

Do not assume every serializer configuration rejects unexpected input keys.

If strict request contracts matter, explicitly detect and reject unknown top-level fields or use a reviewed project base serializer that does so.

This is especially useful for public APIs, typo-sensitive payloads, security-sensitive writes, or clients that should fail fast when sending obsolete fields.

Do not reject unknown fields globally without considering backward/forward compatibility requirements.

## Partial updates

When supporting PATCH:

- respect `serializer.partial`
- do not assume omitted fields exist in `attrs`
- distinguish omitted from explicit `null`
- avoid overwriting omitted fields with defaults unintentionally

## Create/update

Keep `create()`/`update()` small when possible.

Move logic into a service when the operation touches several models, needs locks or transaction orchestration, dispatches async work, calls external systems, or is shared outside the serializer.

## Read/write serializers

Use separate serializers when input and output differ substantially, for example IDs on write and nested objects on read.

Do not split serializers by operation mechanically. Separate them when doing so reduces conditional behavior, writable-surface risk, or representation complexity.

## Sparse/include serializers

For APIs supporting sparse fieldsets or included relationships, use deliberately smaller representations instead of reusing a heavyweight detail serializer everywhere.

Ensure inclusion never bypasses authorization or exposes sensitive fields.

## Computed fields and schema documentation

`SerializerMethodField` and other computed fields may be ambiguous to OpenAPI generators.

If the project uses drf-spectacular or another schema tool, explicitly annotate computed-field types when inference is insufficient.

Keep schema annotations consistent with runtime output.

## Query awareness

Audit dotted `source=` attributes, nested serializers, `SerializerMethodField`, reverse relations, and properties that query the database.

Optimize the view/queryset rather than issuing queries repeatedly in serializer methods.

If a serializer expects prefetched data, make the expectation explicit and provide a safe fallback only when appropriate.

## Uniqueness

A uniqueness validator improves request feedback but is not sufficient protection against races. Keep database unique constraints for true invariants and handle `IntegrityError` where concurrent writes can collide.

## Sensitive representation

Masking a field in `to_representation()` is not authorization by itself.

If a sensitive value may be conditionally exposed, verify caller authorization explicitly, avoid query-parameter-only authorization decisions, keep cache keys permission-aware, and document/test the exposure rule.

## Context

Use `self.context` for request/view-aware serialization when necessary, but avoid using it as an unstructured dependency container.

## Avoid

- DB writes in `validate()`
- network calls in field validation
- N+1 queries from method fields
- giant serializers coordinating full business workflows
- mutating input data unexpectedly
- exposing write-only secrets in output
- broad `__all__` exposure on public serializers

## Review checklist

Check explicit field allowlist, read/write correctness, PATCH semantics, null vs blank, unknown-field policy, uniqueness/race safety, nested-query behavior, computed-field schema accuracy, stable errors, and request/response separation.
