# Multi-Tenant Scoping

Use this reference for SaaS/CRM systems where records belong to an organization, account, workspace, project, or tenant.

## API-layer isolation first

Always scope list/detail/bulk/export queries to an authorized tenant/account.

Object permission checks do not compensate for an unscoped list endpoint.

## Never trust a mutable 'current tenant' preference alone

A user's UI preference such as `current_team_id` or `current_workspace_id` may differ from the resource identified by the URL/request.

Prefer the tenant/resource context explicitly identified by the endpoint, then verify caller membership/authority.

## Fail-closed data access as defense in depth

For high-risk multi-tenant systems, consider a scoped manager/query abstraction that refuses to query when tenant context is missing instead of silently returning all tenants.

Conceptually:

```text
tenant context present  -> automatically scope query
tenant context missing  -> raise
explicit cross-tenant path -> deliberate escape hatch
```

This is defense in depth, not a complete authorization boundary:

- raw SQL can bypass managers
- framework base/default managers may behave differently
- related-object access may use alternate managers
- migrations/admin/cross-tenant jobs need explicit behavior

Do not implement a ContextVar manager casually without understanding Django manager semantics and test coverage.

## Background jobs

Request-local context does not magically survive Celery dispatch.

Tasks that operate on tenant-owned data should receive an explicit tenant/account identifier or durable scoped resource ID and re-establish/verify scope in the worker.

Bad assumption:

```text
HTTP request had tenant context
therefore worker has tenant context
```

## Cache isolation

Tenant/account scope must be included in cache keys for tenant-specific responses or derived data.

## Static enforcement

For critical isolation rules, consider tests or static checks that flag:

- unscoped manager usage in tenant-sensitive modules
- Celery tasks querying scoped models without a tenant identifier
- bulk/export paths missing tenant filters

Conventions that protect tenant data should not rely only on developers remembering prose.
