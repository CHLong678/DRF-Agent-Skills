# Tenant Scope in Celery Tasks

Use this reference when a DRF request schedules work on tenant/account-owned data.

## Explicit propagation

Celery workers run outside the HTTP request context.

Pass a stable scope identifier:

```python
transaction.on_commit(
    lambda: rebuild_customer.delay(tenant_id, customer_id)
)
```

Inside the task:

1. validate/resolve tenant scope
2. load the resource within that scope
3. enforce business authorization/invariants appropriate to the worker path
4. perform idempotent work

Do not trust an arbitrary tenant ID supplied by an external client without the request-layer membership check that created the task.

## Resource ID only?

If the resource ID is globally unique and loading it safely derives the tenant, passing only the resource ID can be sufficient.

Still ensure downstream queries stay within that resource's tenant.

## Retry and scope

Scope identifiers must remain stable across retries.

Do not depend on mutable request-local state or user session state inside the task.

## Cross-tenant jobs

Jobs intentionally scanning multiple tenants should be explicit and separately reviewed. Avoid making cross-tenant behavior the default escape hatch.
