# Scenario: Tenant Data Leak

## Symptom

Detail permissions are correct, but list/export/background paths can access records from another tenant.

## Expected reasoning

1. Scope list/export querysets by authorized tenant.
2. Verify nested parent-child ownership.
3. Review writable tenant/owner fields.
4. Review cache-key isolation.
5. Propagate explicit tenant/resource scope into background jobs.
6. Add cross-tenant regression tests.

## Primary skill

`drf-auth-security`

## Secondary skills

`drf-permissions-authorization`, `drf-celery`, `drf-testing`.
