---
name: drf-api-contracts
description: Django REST Framework API contract, versioning, deprecation, pagination, idempotency, error-shape, schema-generation, and OpenAPI guidance. Use when designing public/internal API contracts, evolving endpoints, adding versions, documenting schemas, or preventing breaking changes.
---

# DRF API Contracts

## Discover the existing contract first

Before changing an endpoint, inspect URL/versioning conventions, request/response serializers, status codes, pagination, filtering/ordering, error format, auth behavior, and generated schema.

Treat these as part of the API contract even when they are not formally documented.

## Versioning

Do not version automatically. Consider versioning when independently deployed clients cannot migrate atomically, breaking changes are unavoidable, or multiple client generations must coexist.

Common strategies include URI, media-type/header, and host/subdomain versioning.

For internal APIs with coordinated deployments, backward-compatible evolution may be simpler than adding versions.

## Breaking changes

Potential breaking changes include removing/renaming fields, changing field type/nullability, enum values, default ordering, pagination shape, optional-to-required input, error/status semantics, or permission behavior.

Prefer additive evolution where possible.

## Deprecation lifecycle

For externally consumed APIs: announce deprecation, document replacement, provide migration guidance, define a sunset date when appropriate, and observe remaining traffic before removal.

## Error contract

Keep error responses consistent. RFC 9457 Problem Details can be useful, but do not introduce it over a stable existing contract without a migration plan.

## Pagination

Use bounded pagination. Prefer cursor/keyset pagination for large/changing datasets when deterministic ordering is available. For expensive list endpoints, see `drf-filtering-pagination`.

## Idempotency

For create/action endpoints that clients may retry, evaluate durable idempotency/business keys when duplicate execution would be harmful.

## Rate limits

Return 429 when appropriate, provide `Retry-After` where useful, and document scope/behavior. DRF throttling is not complete infrastructure-level DoS protection.

## OpenAPI/schema

Keep generated schema aligned with runtime request/response schemas, authentication, pagination, errors, enums, nullable/required fields, custom actions, and computed fields.

Use the OpenAPI version correctly supported by the project's schema generator and clients.

## Schema-generation safety

Schema generators may instantiate views without normal runtime request context.

If `get_queryset()`, serializer selection, permissions, or filters depend on request-specific attributes:

- understand how the installed schema generator invokes the view
- avoid executing tenant/user-sensitive real queries during schema generation
- return a safe `.none()` queryset or provide explicit schema hints when appropriate
- use generator-specific guards only when that generator actually defines them

Some drf-spectacular/drf-yasg integrations expose schema-introspection flags such as `swagger_fake_view`. Treat that as tooling-specific behavior, not universal DRF behavior.

Do not hide genuine runtime bugs behind a schema-only branch.

## Computed fields

When a computed serializer field cannot be inferred correctly, annotate its schema explicitly using the project's schema tooling.

The schema should describe the runtime value, not merely silence generator warnings.

## Custom actions

Document custom `@action` endpoints explicitly when inference is insufficient: request serializer, response serializer, status codes, permissions/authentication, and path/query parameters.

## Verification

When changing a public contract, update tests and documentation together.

## Deep references

Load `references/openapi-runtime-parity.md` when custom actions, schema overrides, query-parameter serializers, generated clients, or response typing are involved.

A schema annotation must describe runtime behavior faithfully; never make generated clients narrower than the actual endpoint by accident.
