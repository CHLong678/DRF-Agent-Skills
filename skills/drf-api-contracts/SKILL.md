---
name: drf-api-contracts
description: Django REST Framework API contract, versioning, deprecation, pagination, idempotency, error-shape, and OpenAPI guidance. Use when designing public/internal API contracts, evolving endpoints, adding versions, documenting schemas, or preventing breaking changes.
---

# DRF API Contracts

## Discover the existing contract first

Before changing an endpoint, inspect:

- URL/versioning conventions
- request and response serializers
- status codes
- pagination shape
- filtering and ordering
- error format
- authentication/permission behavior
- generated OpenAPI schema if present

Treat these as part of the API contract even when they are not formally documented.

## Versioning

Do not version automatically.

Consider versioning when:

- public or independently deployed clients cannot migrate atomically
- breaking response/request changes are unavoidable
- multiple client generations must coexist

Common strategies:

- URI: `/api/v1/orders/`
- media type / header versioning
- host/subdomain versioning

For internal APIs with coordinated deployments, careful backward-compatible evolution may be simpler than adding versions.

Use DRF's versioning facilities consistently if the project already uses them.

## Breaking changes

Potential breaking changes include:

- removing or renaming fields
- changing field type or nullability
- changing enum/status values
- changing default ordering
- changing pagination shape
- making optional input required
- changing error/status semantics
- tightening permissions in a way clients do not expect

Prefer additive evolution where possible.

## Deprecation lifecycle

For externally consumed APIs:

1. announce deprecation
2. document the replacement
3. provide migration guidance
4. define a sunset date when appropriate
5. observe remaining traffic before removal

Do not delete an old endpoint merely because the new version exists.

## Error contract

Keep error responses consistent across endpoints.

For APIs that benefit from a standardized error envelope, RFC 9457 Problem Details is a good option, but do not introduce it if the project already has a stable incompatible contract without a migration plan.

Useful fields include:

- machine-readable code
- human-readable detail
- HTTP status
- per-field validation details
- correlation/request identifier when appropriate

Never expose internal exceptions or secrets.

## Pagination

Use bounded pagination for collections.

Prefer cursor/keyset-style pagination when:

- datasets are large
- deep offsets are expensive
- stable ordering can be guaranteed

Cursor pagination requires deterministic ordering, usually including a unique tiebreaker.

Offset pagination remains reasonable for smaller/admin-style datasets.

## Idempotency

For create/action endpoints that clients may retry, evaluate idempotency.

Examples:

- payment/order creation
- webhook ingestion
- bulk actions
- externally retried POST requests

Use a durable idempotency/business key when duplicate execution would be harmful.

## Rate limits

For rate-limited APIs:

- return 429 when appropriate
- provide `Retry-After` where useful
- document rate-limit scope and behavior

Do not assume DRF throttling alone provides infrastructure-level DoS protection.

## OpenAPI/schema

Keep the generated schema aligned with real runtime behavior.

Check:

- request/response schemas
- authentication requirements
- pagination
- error responses
- enum values
- nullable/required fields
- custom actions

Use the OpenAPI version supported correctly by the project's schema generator and client tooling. Do not force the newest specification version solely because it exists.

## Verification

When changing a public contract, update tests and documentation together.
