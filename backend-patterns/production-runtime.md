# Production Runtime Patterns

## Configuration

Separate deploy-time configuration from source code.

Validate required configuration at startup where failure should be immediate.

Never silently fall back to insecure production secrets.

## Process roles

Treat web/API, Celery worker, scheduler/beat, and migration/admin jobs as independent runtime roles.

Each role can have different CPU/memory needs, connection demand, concurrency, shutdown behavior, and health checks.

## Health vs readiness

Health answers whether the process/runtime is alive.

Readiness answers whether it should receive traffic.

A process can be alive but not ready because required configuration or a critical dependency is unavailable.

Do not make every optional dependency a readiness blocker.

## Graceful shutdown

On deploy/termination:

- stop accepting new work
- allow bounded in-flight work to finish
- release resources
- requeue/retry work according to delivery semantics

Grace periods must align with request/task time limits.

## Dependency startup

Avoid requiring all remote dependencies during import unless essential for process startup.

Startup dependency calls can turn a partial external outage into total inability to boot.

## Proxy/TLS boundary

When Django runs behind a reverse proxy or load balancer, security behavior depends on trusted forwarding configuration.

Do not trust arbitrary forwarded headers from untrusted clients.

## Observability

Every process role should expose enough information to answer whether it is alive, ready, running the expected build, saturated, or failing a dependency.

## Deployment compatibility

Rolling deployments temporarily run old and new code together.

Database, event, and API changes should tolerate that overlap or deployment strategy must prevent incompatible coexistence.
