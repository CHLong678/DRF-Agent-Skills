# DRF Agent Skills

A focused collection of Agent Skills for building and reviewing production Django REST Framework code.

Designed specifically for:

- OpenAI Codex
- Google Antigravity

The repository intentionally avoids generic frontend, non-Django, and unrelated framework guidance. Each skill is narrow enough to load only when relevant.

## Compatibility

Baseline target:

- Django >= 3.2
- Celery >= 5.0 when Celery is used
- a Django REST Framework version that officially supports the installed Django version

Agents must inspect the project's actual Django, DRF, Celery, Python, database, and third-party package versions before using version-sensitive APIs. If versions are unknown, skills should fall back to Django 3.2 / Celery 5.0-compatible patterns.

See [`COMPATIBILITY.md`](COMPATIBILITY.md) for explicit version gates and fallbacks.

## Skills

| Skill | Purpose |
|---|---|
| `drf-core` | Architecture, API boundaries, service-layer guidance, response/error conventions |
| `drf-serializers` | Serializer design, validation, nested data, read/write separation |
| `drf-views` | APIView, GenericAPIView, mixins, generic views, ViewSets, actions, lifecycle |
| `drf-orm-performance` | QuerySet design, N+1 prevention, annotations, bulk work, indexing guidance |
| `drf-transactions-concurrency` | `atomic`, `select_for_update`, `on_commit`, race conditions, idempotency |
| `drf-auth-security` | Authentication, permissions, BOLA/IDOR, tenant isolation, throttling, secure API behavior |
| `drf-testing` | pytest-django, API/security tests, factories, transaction/concurrency tests |
| `drf-code-review` | DRF-specific code review checklist and risk prioritization |
| `drf-api-contracts` | API evolution, versioning, deprecation, error contracts, pagination, OpenAPI |
| `drf-async` | Async views, ASGI, sync/async boundaries, deciding between async and background jobs |
| `drf-caching` | Redis/application/HTTP caching, key design, invalidation, ETags, stampede prevention |
| `drf-observability` | Profiling, structured logging, metrics, tracing, load testing, performance verification |
| `drf-filtering-pagination` | django-filter, bounded ranges, multi-value filters, large-list pagination, two-phase hydration |
| `drf-celery` | Task boundaries, `on_commit`, idempotency, retries, `acks_late`, queues, prefetch, chunking, monitoring |
| `drf-bulk-large-data` | Large imports/exports, `iterator`, bulk create/update, streaming, chunking, memory-safe processing |
| `django-startup-performance` | `django.setup()`/worker startup, import graphs, `AppConfig.ready()`, lazy-load tradeoffs |
| `django-admin-large-data` | Large-table Django admin counts, N+1, relation widgets, search/filter performance |
| `django-architecture-enforcement` | CI/static enforcement for tenant scope, import boundaries, architecture/security invariants |

## Skill directory layout

Each skill is a self-contained directory. `SKILL.md` is the entrypoint; deeper material is loaded only when needed:

```text
skills/<skill-name>/
├── SKILL.md
├── references/      # deeper rules, edge cases, compatibility notes
│   └── *.md
└── examples/        # optional copyable examples
    └── *.py
```

The installers copy the entire skill directory recursively, so Codex and Antigravity receive references/examples together with the entrypoint.

## Design principles

These skills were inspired by production-grade agent-skill repositories such as ECC and claude-code-templates, but the rules here are deliberately tightened for DRF and corrected where generic examples are unsafe, overly broad, or too prescriptive.

Key corrections include:

- `select_for_update()` must execute inside an active transaction.
- Celery/external side effects that depend on committed state should usually be triggered with `transaction.on_commit()`.
- Do not create database indexes merely because a field appears in `filter()` or `order_by()`; require workload/selectivity/query-plan justification.
- PostgreSQL projects should test important database behavior against PostgreSQL rather than assuming SQLite equivalence.
- Avoid legacy Django/browser security settings as blanket recommendations.
- Serializer validation should not perform surprising side effects.
- Views should orchestrate HTTP concerns; complex reusable business workflows belong in services/domain functions.
- Do not force arbitrary test-coverage percentages; prioritize meaningful behavioral, security, and concurrency tests.
- Do not convert views to async without checking the complete sync/async dependency path and ASGI deployment.
- Do not force the newest OpenAPI version when the project's schema generator or clients do not support it correctly.
- Do not add caching without defining isolation, invalidation, TTL, and stale-data behavior.
- Treat Celery delivery as potentially duplicate: separate application retry from broker redelivery and require idempotency where delivery semantics need it.
- Use stable machine-readable API error codes when clients need to branch on failure type; do not make them parse human text.
- For expensive APIs, consider cost-aware budgets/quotas instead of relying only on requests-per-minute throttling.
- When tenant isolation or architecture boundaries are critical, prefer CI/static enforcement over prose-only conventions.
- Do not bulk-process huge datasets by materializing every row/object in memory; prefer bounded chunks, `iterator()`, set-based updates, streaming, or background jobs according to workload.

## Install for Codex

### User scope

```bash
git clone https://github.com/CHLong678/DRF-Agent-Skills.git
cd DRF-Agent-Skills
./scripts/install-codex.sh
```

This installs the skills into:

```text
~/.codex/skills/
```

You can also keep skills repo-scoped by copying selected directories into:

```text
<project>/.codex/skills/
```

### Manual install

```bash
mkdir -p ~/.codex/skills
cp -R skills/drf-* ~/.codex/skills/
```

## Install for Antigravity

For project-scoped skills, install under `.agents/skills/`.

### Recommended: project scope

From your DRF project root:

```bash
/path/to/DRF-Agent-Skills/scripts/install-antigravity.sh --project .
```

This installs to:

```text
<project>/.agents/skills/
```

### Global scope

```bash
./scripts/install-antigravity.sh --global
```

If your Antigravity installation uses another global directory, set `ANTIGRAVITY_SKILLS_DIR` explicitly:

```bash
ANTIGRAVITY_SKILLS_DIR="$HOME/.gemini/config/skills" \
  ./scripts/install-antigravity.sh --global
```

## Use selected skills only

You do not need all skills in every project.

For a typical production DRF backend, a good baseline is:

```text
drf-core
drf-serializers
drf-views
drf-orm-performance
drf-transactions-concurrency
drf-auth-security
drf-code-review
```

Add these when relevant:

```text
drf-api-contracts     public/versioned APIs
drf-async             ASGI/async endpoint work
drf-caching           Redis/HTTP/application caching
drf-observability     performance and production diagnostics
drf-filtering-pagination   large/complex list endpoints and FilterSet work
drf-celery           background jobs, retries, queues, worker/backlog behavior
drf-bulk-large-data  imports, exports, bulk APIs, huge QuerySets, chunked processing
django-startup-performance  slow Django/Celery/manage.py startup and import graphs
django-admin-large-data     admin changelist/form performance on large tables
django-architecture-enforcement  enforce critical boundaries/invariants in CI
drf-testing          implementation or review of tests
```

## Example prompts

```text
Use drf-code-review to review this ViewSet and serializer for architecture,
N+1 queries, permissions, transaction risks, and backward compatibility.
```

```text
Use drf-transactions-concurrency to implement this order update safely when
multiple workers may modify the same record.
```

```text
Use drf-orm-performance to optimize this endpoint without changing API output.
```

```text
Use drf-api-contracts to review whether this API change is backward-compatible
and whether it needs versioning or a deprecation path.
```

```text
Use drf-auth-security and drf-testing to check this endpoint for BOLA/IDOR,
tenant isolation, mass assignment, and missing authorization tests.
```

```text
Use drf-celery to review this task for idempotency, retry/redelivery semantics,
queue isolation, prefetch, timeouts, and dispatch-after-commit.
```

```text
Use drf-bulk-large-data to redesign this million-row import/export so memory,
transaction scope, chunk size, retries, and API limits remain bounded.
```

## Repository philosophy

The skills should prefer the existing project's conventions unless they are clearly unsafe. They should not refactor unrelated code, invent abstractions prematurely, or turn DRF code into architecture for architecture's sake.

Before changing code, agents should inspect nearby serializers, views, models, services, tests, shared utilities, schema generation, and API conventions to preserve local consistency and backward compatibility.

## Sources and adaptation

This repository is not a verbatim copy of upstream skill collections. Ideas are reviewed, narrowed to DRF, and rewritten to favor production correctness.

Notable inspiration:

- `affaan-m/ECC`
- `davila7/claude-code-templates`
- `prowler-cloud/prowler` (`skills/django-drf`)
- `Jeffallan/claude-skills` (`skills/django-expert`)
- `PostHog/posthog` (`.agents/skills/improving-drf-endpoints` plus production Django patterns)

Authoritative references used for reliability-sensitive rules:

- Django 3.2 documentation as the compatibility baseline
- Django 4.1 release notes for async ORM / `iterator()` + prefetch version gates
- Django 4.2 release notes for async `StreamingHttpResponse` version gates
- Celery 5.0 documentation as the compatibility baseline
- newer Celery documentation only when a feature is explicitly version-gated

## License

MIT
