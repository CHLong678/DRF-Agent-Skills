---
name: drf-permissions-authorization
description: Deep Django REST Framework authorization guidance. Use when designing permission classes, object-level access, list/create authorization, custom actions, role matrices, nested resources, or testing authorization behavior.
---

# DRF Permissions & Authorization

## Understand DRF permission layers

Authorization may need enforcement in multiple places:

- `get_queryset()` for visibility/scoping
- view-level permission classes
- object-level permissions
- serializer/write-field restrictions
- service/domain rules for business actions

Do not rely on one layer for every action.

## List endpoints

DRF does not run object-level permission checks for every row in list querysets.

Scope the queryset so unauthorized objects are not returned.

## Detail/custom retrieval

Generic views call object permissions when `get_object()` is used.

If custom code retrieves an object manually or overrides `get_object()`, call:

```python
self.check_object_permissions(request, obj)
```

when object-level permission logic is expected.

## Create authorization

Object-level permission checks do not automatically apply to creation because the object does not exist yet.

Enforce create authorization through:

- view permission logic
- serializer validation where appropriate
- `perform_create()`
- service/domain authorization

depending on project architecture.

## Custom actions

Every `@action` must be reviewed for:

- view-level permission
- object lookup/scoping
- object-level permission
- sensitive writable fields
- bulk/cross-object behavior

## Nested resources

Never trust only the child ID.

Verify the child belongs to the authorized parent/tenant represented by the route.

## Role matrices

For complex systems, document action-to-role/capability rules explicitly.

Avoid scattering role-name comparisons throughout serializers/views.

## Denial behavior

Choose 403 vs scoped 404 intentionally based on the project's security/product contract.

Be consistent.

## Testing

Test at least:

- unauthenticated
- wrong tenant
- same tenant wrong role
- owner vs non-owner
- list leakage
- detail access
- create restrictions
- custom actions
- bulk actions

## Deep reference

- `references/list-object-create.md`

## Authoritative source

DRF permissions documentation:
https://www.django-rest-framework.org/api-guide/permissions/

## Routing contract

### Use this skill when
- permission classes, object permissions, list scoping, create authorization, custom actions, nested resources, or role/capability rules are primary

### Do not use this skill when
- the main task is broader API security/BOLA/tenant design; use `drf-auth-security`
- the question is authentication/token configuration

### Inspect first
- endpoint action and HTTP method
- queryset scoping
- object retrieval path
- permission classes
- create/update writable fields
- role/capability model and tests

### Related skills
- `drf-auth-security`, `drf-views`, `drf-testing`
