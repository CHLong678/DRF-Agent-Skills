---
name: drf-auth-security
description: Django REST Framework API authentication, authorization, permissions, throttling, tenant isolation, object access, and secure endpoint review guidance. Use when implementing or auditing DRF security-sensitive behavior.
---

# DRF Authentication & Security

## Authentication vs authorization

Keep distinct:

- authentication: who is the caller?
- authorization: may this caller perform this action on this resource?

Do not treat successful authentication as sufficient authorization.

## Permissions

Set permissions intentionally for every endpoint or rely on a deliberate global default that is verified for the project.

For object access:

- scope querysets to the caller where possible
- apply object-level permission checks for retrieved objects
- ensure list endpoints do not leak rows that would fail detail permissions

## BOLA / IDOR

Treat object identifiers as attacker-controlled.

Test horizontal access explicitly:

1. create resource owned by user/account A
2. authenticate as user/account B
3. request A's resource by ID
4. verify the response does not disclose or mutate it

Do not rely on unguessable UUIDs as authorization.

## Tenant isolation

For multi-tenant systems, tenant scope must be applied consistently to:

- list querysets
- detail lookup
- nested resources
- bulk actions
- exports
- background tasks
- cache keys

Never accept a tenant/account identifier from the request and trust it without checking caller membership/authority.

## Custom permission classes

Keep permission classes side-effect free and cheap. Avoid expensive repeated queries when authorization data can be selected/prefetched once.

## Mass assignment / property authorization

Do not expose sensitive model fields as writable merely because `ModelSerializer` can infer them.

Explicitly control fields such as:

- ownership/account IDs
- roles/privileges
- billing state
- audit fields
- internal workflow status

Also review response fields for accidental sensitive-data exposure.

## Authentication tokens

Never log raw credentials, access tokens, refresh tokens, API keys, passwords, or secret headers.

Apply token expiry/revocation strategy appropriate to the authentication mechanism in use.

For JWT-style authentication, validate the claims required by the project's trust model, such as expiry, issuer, and audience where applicable.

## Throttling

Use throttling/rate limits where abuse or expensive operations justify it, but do not treat DRF throttling as a complete DDoS defense.

Test whether rate-limit identity can be bypassed by attacker-controlled proxy headers or alternate routes/methods.

Trust forwarded IP headers only when the deployment proxy chain is configured to sanitize them.

## Business-flow abuse

Security is not limited to technical authorization.

Review workflows for abuse such as:

- repeatedly triggering expensive operations
- replaying state-changing requests
- bypassing sequence/state transitions
- automating actions intended to have business limits

Use idempotency, state constraints, rate limits, or explicit quotas where justified.

## Input handling

Use serializers/parsers and parameterized ORM queries. Avoid string-interpolated raw SQL.

For endpoints that fetch user-provided URLs, consider SSRF risks and restrict destination schemes/hosts/networks as required.

Validate uploads by actual content/type policy where security depends on file type; do not trust filename extensions alone.

## External API consumption

Treat third-party responses as untrusted input.

Validate required fields, set timeouts, bound payload sizes where practical, and do not pass remote error content directly to clients.

## Error responses

Do not reveal:

- stack traces
- SQL errors
- secret configuration
- internal paths
- unnecessary existence information for sensitive resources

## CSRF/CORS

Understand the authentication mode before changing CSRF behavior. Cookie/session-authenticated APIs require different CSRF considerations than bearer-token APIs.

Do not use permissive CORS settings as a shortcut in production.

## API inventory

Old versions, forgotten endpoints, debug routes, and shadow APIs expand attack surface.

When versioning or replacing endpoints, include removal/deprecation ownership rather than leaving obsolete routes indefinitely.

## Security settings

Prefer current Django-supported security controls and current browser behavior. Do not add legacy settings solely because older snippets recommend them.

## Review checklist

Check:

- authentication class
- permission class
- queryset scoping
- object permission
- BOLA/IDOR
- tenant isolation
- sensitive writable/readable fields
- privilege escalation
- secrets in logs/errors
- unsafe raw SQL
- SSRF/file-upload risk
- throttle/abuse bypass
- CORS/CSRF assumptions
- obsolete/shadow endpoints
