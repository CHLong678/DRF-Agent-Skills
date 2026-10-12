# Task

The DRF endpoint at /customers/ accepts a trusted X-Tenant-ID header in this simplified fixture, but the list endpoint leaks rows from other tenants.

Fix the implementation so the caller only sees rows for its tenant.

Keep the response shape unchanged and do not weaken or delete tests.
