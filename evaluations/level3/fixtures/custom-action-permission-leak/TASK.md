# Task

The normal retrieve path is tenant-scoped, but a custom action fetches an Order directly and can expose another tenant's order.

Fix the custom action so it uses the same authorized object visibility as normal retrieve.

Keep the route and response shape unchanged. Do not weaken or delete tests.
