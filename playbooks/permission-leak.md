# Playbook: Permission / Tenant Leak

## Goal

Find where unauthorized data can enter list/detail/create/action flows.

## Flow

1. Start with `drf-auth-security`.
2. Identify authenticated identity and tenant/resource scope.
3. Check list queryset scoping.
4. Check detail lookup and object permissions.
5. Check nested/bulk/export paths.
6. Check writable ownership/role/tenant fields.
7. Load `drf-permissions-authorization` for permission-class and action-specific rules.
8. Check cache keys and Celery/background propagation.
9. Add cross-user/cross-tenant regression tests with `drf-testing`.

## Stop conditions

Do not treat UUID unpredictability or UI-hidden fields as authorization.
