---
name: drf-auth-security
description: Django REST Framework API authentication, authorization, permissions, throttling, object access, and secure endpoint review guidance. Use when implementing or auditing DRF security-sensitive behavior.
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

## Custom permission classes

Keep permission classes side-effect free and cheap. Avoid expensive repeated queries when authorization data can be selected/prefetched once.

## Mass assignment / writable fields

Do not expose sensitive model fields as writable merely because `ModelSerializer` can infer them.

Explicitly control fields such as:

- ownership/account IDs
- roles/privileges
- billing state
- audit fields
- internal workflow status

## Authentication tokens

Never log raw credentials, access tokens, refresh tokens, API keys, passwords, or secret headers.

Apply token expiry/revocation strategy appropriate to the authentication mechanism in use.

## Throttling

Use throttling/rate limits where abuse or expensive operations justify it, but do not treat DRF throttling as a complete DDoS defense.

## Input handling

Use serializers/parsers and parameterized ORM queries. Avoid string-interpolated raw SQL.

Validate uploads by actual content/type policy where security depends on file type; do not trust filename extensions alone.

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

## Security settings

Prefer current Django-supported security controls and current browser behavior. Do not add legacy settings solely because older snippets recommend them.

## Review checklist

Check:

- authentication class
- permission class
- queryset scoping
- object permission
- sensitive writable fields
- secrets in logs/errors
- unsafe raw SQL
- upload policy
- throttle/abuse risk
- CORS/CSRF assumptions
