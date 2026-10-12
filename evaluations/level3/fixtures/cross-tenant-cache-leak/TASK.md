# Task

The customer list endpoint caches a response without tenant context. A request from tenant 2 can receive tenant 1 data.

Fix the cache design so tenant isolation is preserved.

Keep the endpoint contract unchanged and do not disable caching or weaken tests.
