---
name: drf-views
description: Django REST Framework view lifecycle and view design guidance. Use when implementing or reviewing APIView, GenericAPIView, mixins, generic views, ViewSets, ModelViewSet, custom actions, serializer selection, or queryset/permission overrides.
---

# DRF Views

## Choose the smallest abstraction that fits

Use:

- `APIView` for highly custom HTTP behavior
- `GenericAPIView` + mixins for reusable CRUD pieces with explicit control
- concrete generic views for conventional single-purpose CRUD endpoints
- `ViewSet`/`ModelViewSet` when router/action semantics genuinely fit the resource

Do not choose `ModelViewSet` automatically just because a model exists.

## Understand lifecycle hooks

Common hooks:

- `get_queryset()`
- `get_serializer_class()`
- `get_serializer_context()`
- `get_permissions()`
- `perform_create()`
- `perform_update()`
- `perform_destroy()`
- custom `@action`

Prefer hooks over duplicating framework internals.

## Querysets

Use `get_queryset()` when results depend on request/user/action.

Always apply authorization scoping before exposing objects. Object-level permission checks are not a substitute for appropriately scoped list querysets.

## Serializer selection

Use action-aware serializer selection when read/write shapes differ.

```python
def get_serializer_class(self):
    if self.action == "create":
        return OrderCreateSerializer
    return OrderDetailSerializer
```

Avoid deeply nested action/role/version conditionals; extract a mapping or separate endpoints when complexity becomes hard to reason about.

## perform_create/update

Use `perform_create()` and `perform_update()` for small save-time request context such as `created_by=request.user`.

For complex workflows, invoke a service instead of forcing everything through `serializer.save()`.

## Custom actions

For `@action`:

- use a clear resource-oriented name
- choose `detail=True/False` intentionally
- set method, serializer, permission, throttling as needed
- avoid turning a ViewSet into a collection of unrelated RPC endpoints

## HTTP semantics

Use correct status codes and idempotency expectations.

Examples:

- create: usually 201
- successful delete with no body: usually 204
- validation failure: 400
- unauthenticated: 401 where authentication class semantics support it
- authenticated but forbidden: 403
- state conflict: often 409 when appropriate

Do not blindly convert every business error to 400.

## Pagination/filtering

For list endpoints with potentially large datasets:

- use pagination
- explicitly define allowed ordering/search/filter fields
- avoid unbounded result sets
- ensure expensive filters have appropriate query plans

## Avoid

- business workflows directly in view methods
- broad `.all()` list endpoints for large tables
- permission logic duplicated across methods
- manually reimplementing mixin behavior without need
- queries inside loops
- swallowing exceptions and returning 200 with error strings

## Routing contract

### Use this skill when
- choosing APIView/generic view/ViewSet/action structure
- reasoning about DRF view lifecycle and hooks
- implementing HTTP orchestration around serializers/querysets/services

### Do not use this skill when
- serializer design is the primary problem
- permission/security behavior is the primary problem
- business workflow/transaction design is the primary problem

### Inspect first
- URL/router registration
- target view/viewset base classes
- serializer/queryset/permission hooks
- nearby actions and tests

### Related skills
- `drf-core`, `drf-serializers`, `drf-permissions-authorization`

## Deep reference

- `references/view-hooks-lifecycle.md`

## Output contract

For implementation guidance, state the chosen DRF abstraction/hook, why it fits, adjacent security/transaction concerns, and how to verify behavior.
