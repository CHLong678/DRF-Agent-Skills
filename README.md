# DRF Agent Skills

A focused collection of Agent Skills for building and reviewing production Django REST Framework code.

Designed for reusable backend skills across:

- OpenAI Codex and Google Antigravity
- Claude Code, Cursor, GitHub Copilot, and OpenCode

The repository intentionally avoids generic frontend, non-Django, and unrelated framework guidance. Each skill is narrow enough to load only when relevant.

## Community and private editions

This development checkout currently contains **34 skills**. The proposed **Community edition** exports only seven beginner-facing skills: `drf-core`, `drf-serializers`, `drf-views`, `drf-orm-performance`, `drf-testing`, `drf-code-review`, and `drf-api-contracts`.

```bash
python3 scripts/export-community.py --output /tmp/drf-agent-skills-community
python3 scripts/test_community_export.py
```

The export includes only allowlisted files and has no inherited Git history. **This public development repo is not private**: its older commits already exposed the full catalog. Move the full repository to a confirmed private development destination before retiring/replacing the old public distribution. Read [the migration and publication guide](publishing/README.md).

## Compatibility

Baseline target:

- Django >= 3.2
- Celery >= 5.0 when Celery is used
- a Django REST Framework version that officially supports the installed Django version

Agents must inspect the project's actual Django, DRF, Celery, Python, database, and third-party package versions before using version-sensitive APIs. If versions are unknown, skills should fall back to Django 3.2 / Celery 5.0-compatible patterns.

See [`COMPATIBILITY.md`](COMPATIBILITY.md) for explicit version gates and fallbacks.

## Agent operating protocol

For non-trivial work, agents should:

1. inspect the codebase with `CODEBASE_INSPECTION.md`
2. classify change risk with `CHANGE_RISK.md`
3. choose primary/secondary skills through `ROUTING.md`
4. compose cross-boundary skills with `SKILL_COMPOSITION.md`
5. use `OUTPUT_CONTRACTS.md` for a verifiable result
6. verify behavior with tests/measurements appropriate to the risk

## Invocation model

Skills are split into:

- **model-invoked** domain skills, whose descriptions contain concrete discovery triggers
- **user-invoked** workflow skills, currently `drf-skill-router` and `backend-agent-retro`

Every skill also ships `agents/openai.yaml` for Codex display/policy metadata. The repository validates that Codex invocation policy matches the skill frontmatter.

See `AUTHORING/INVOCATION.md`.

## Skill routing

When more than one skill appears relevant, start with `ROUTING.md` or the `drf-skill-router` skill.

Routing rules:

- choose one primary skill for the main decision
- load secondary skills only for real cross-boundary concerns
- prefer the most specific skill over broad/core/review skills
- if the bottleneck is unknown, start with a diagnostic skill such as `drf-observability`
- stop loading adjacent skills once correctness can be decided safely

Decision playbooks live under `playbooks/` for common production problems such as slow APIs, race conditions, Celery backlog, large datasets, permission leaks, and production migrations.

## Backend pattern knowledge layer

Framework-neutral backend knowledge lives in `backend-patterns/` and is adapted into Django/DRF-specific skills only when the pattern is justified by the actual failure mode.

Current topics include resilience, event-driven consistency, capacity/scaling, service/module boundaries, production runtime, caching, rate limiting, distributed locking, failure recovery, and file/object storage.

See `backend-patterns/SOURCES.md` for source/adaptation rules.

## Skills

| Skill | Purpose |
|---|---|
| `drf-skill-router` | Explicit user-invoked router for ambiguous/cross-cutting tasks |
| `backend-diagnosing-bugs` | Tight feedback-loop diagnosis for hard/intermittent backend failures |
| `backend-agent-retro` | Explicit retrospective that improves the agent environment after failures |
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
| `django-migrations-production` | Low/zero-downtime schema changes, backfills, concurrent indexes, migration safety |
| `postgresql-for-django` | EXPLAIN, indexes, locks/deadlocks, PostgreSQL-specific Django performance |
| `drf-webhooks-integrations` | Signature verification, duplicate/retry/out-of-order webhook handling, idempotent processing |
| `drf-background-jobs-contracts` | 202 Accepted, durable job resources, progress/cancellation/result contracts |
| `drf-permissions-authorization` | Deep list/object/create/custom-action authorization and permission design |
| `django-production-runtime` | Runtime configuration, process roles, health/readiness, graceful shutdown, proxy/deploy boundaries |
| `django-service-boundaries` | Services/selectors/module boundaries, facades, adapters, reusable business workflows |
| `drf-capacity-scaling` | Saturation, process concurrency, DB connection budgets, replicas, capacity headroom |
| `drf-event-driven-consistency` | Outbox, idempotent consumers, ordering, eventual consistency, compensation, DLQ |
| `drf-resilience-patterns` | Timeouts, retries, jitter, backpressure, load shedding, graceful degradation |
| `drf-rate-limits-quotas` | Rate/concurrency limits, cost-aware quotas, tenant fairness, 429 contracts |
| `drf-files-object-storage` | Large uploads/downloads, presigned URLs, object lifecycle, untrusted file handling |
| `drf-reconciliation-repair` | Reconciliation, repair/replay jobs, poison data, resumable production repair |

## Skill directory layout

Each skill is a self-contained directory. `SKILL.md` is the entrypoint; deeper material is loaded only when needed:

```text
skills/<skill-name>/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/      # deeper rules, edge cases, compatibility notes
│   └── *.md
└── examples/        # optional copyable examples
    └── *.py
```

The unified installer copies every skill directory recursively for all supported agents, preserving references/examples with the entrypoint.

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
- Production migrations should be reviewed for lock duration, rolling-deploy compatibility, backfill cost, and rollback/retry behavior.
- PostgreSQL-specific optimizations must be justified with real query plans and workload evidence.
- Webhook endpoints must assume duplicate, retry, and out-of-order delivery and verify provider authenticity before processing.
- Long-running APIs should expose a stable job contract instead of leaking Celery implementation details.
- Do not bulk-process huge datasets by materializing every row/object in memory; prefer bounded chunks, `iterator()`, set-based updates, streaming, or background jobs according to workload.

## Install for any supported agent

One installer, one canonical source of skills, six supported agents:

```bash
git clone https://github.com/CHLong678/DRF-Agent-Skills.git
cd DRF-Agent-Skills

# Preview installation in a Django project for every supported agent
python3 scripts/install-agents.py --agent all --scope project --project /path/to/django-project --dry-run

# Install all skills for a single agent
python3 scripts/install-agents.py --agent codex --scope global
python3 scripts/install-agents.py --agent antigravity --scope project --project /path/to/django-project
python3 scripts/install-agents.py --agent claude-code --scope global
python3 scripts/install-agents.py --agent cursor --scope global
python3 scripts/install-agents.py --agent github-copilot --scope global
python3 scripts/install-agents.py --agent opencode --scope global

# Antigravity CLI-specific global directory
python3 scripts/install-agents.py --agent antigravity --scope cli-global

# Install just two skills, for all agents inside the project
python3 scripts/install-agents.py --agent all --scope project --project /path/to/django-project \
  --skill drf-celery --skill drf-transactions-concurrency
```

The installer never replaces existing unowned skill directories unless you explicitly add `--force`; it supports repeatable `--skill` selectors and `--dry-run`. When migrating from the former dedicated Codex/Antigravity installers, their existing installations may be considered unowned, so review conflicts before choosing `--force`.

See [installation paths, compatibility and limitations](adapters/README.md). Invocation/skill-discovery semantics are agent-specific; installing a skill does not prove that the model will invoke it.

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
django-migrations-production     production schema/data migration work
postgresql-for-django             PostgreSQL plans, indexes, locks and DB-specific tuning
drf-webhooks-integrations        third-party webhook/integration endpoints
drf-background-jobs-contracts    202/job-status/result/cancellation API design
drf-permissions-authorization    complex authorization and object/list/create permissions
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

## Level-3 executable evaluations

Level 3 measures whether an agent can actually fix a small broken Django/DRF project and make deterministic tests pass.

Current fixtures:

- `drf-n-plus-one`
- `tenant-list-leak`
- `idempotent-side-effect`
- `patch-null-vs-omitted`
- `cross-tenant-cache-leak`
- `custom-action-permission-leak`
- `side-effect-before-commit`

Dry-run:

```bash
python scripts/run_level3_evals.py --provider codex --dry-run
```

Run a real Codex fixture in a temporary workspace:

```bash
python scripts/run_level3_evals.py \
  --provider codex \
  --fixture drf-n-plus-one \
  --setup
```

See `evaluations/level3/README.md`.

## Benchmark history

Raw model-run reports remain under gitignored `evaluations/results/`.

Selected runs can be normalized into reviewable snapshots under `evaluations/benchmarks/history/`:

```bash
python scripts/benchmark_history.py record \
  --input evaluations/results/codex/<run>.json \
  --output evaluations/benchmarks/history/codex-routing-2026-10.json
```

Compare two snapshots:

```bash
python scripts/benchmark_history.py compare \
  --baseline <before.json> \
  --current <after.json>
```

A comparison surfaces pass-rate/score changes, recovered cases, and regressions.

## Model-based evaluations

The repository can run the routing suite against real agent CLIs.

Codex:

```bash
./scripts/install-codex.sh
python scripts/run_model_evals.py --provider codex
```

Antigravity CLI:

```bash
./scripts/install-antigravity.sh --cli-global
python scripts/run_model_evals.py --provider antigravity
```

The runner scores actual model output against `evaluations/routing-cases.json`: expected primary skill, forbidden primary choices, secondary-skill discipline, inspect-first behavior, verification, and required reasoning tags.

It writes reports to `evaluations/results/<provider>/`. These runtime reports are intentionally not part of normal repository validation because they require authenticated model access and incur inference cost.

See `evaluations/model/README.md` for usage.

## Evaluations and scenarios

The repository includes machine-readable routing cases and production scenarios:

```text
evaluations/
└── routing-cases.json

scenarios/
├── n-plus-one/
├── race-condition/
├── celery-duplicate/
├── tenant-leak/
├── large-export/
└── production-migration/
```

Routing cases define the expected primary skill, allowed secondary skills, forbidden primary choices, and rationale. Scenarios define the expected reasoning path for common production failures.

Agent response structure is standardized in `OUTPUT_CONTRACTS.md` for performance, security, concurrency, Celery/background processing, migrations, and code review.

## Source freshness and context budget

Version-sensitive source reviews are tracked in `metadata/compatibility-sources.json`.

CI rejects stale source-review metadata beyond the configured freshness window.

`scripts/lint_skill_context.py` also enforces concise skill descriptions and reports suspicious trigger/paragraph overlap so the skill catalog can grow without silently diluting routing attention.

## Repository validation

The repository validates its own skill quality in CI:

```bash
python scripts/validate_skills.py
python scripts/validate_invocation_metadata.py
python scripts/validate_source_freshness.py
python scripts/lint_skill_context.py
python scripts/validate_evaluations.py
python scripts/validate_backend_patterns.py
python scripts/validate_agent_protocols.py
python scripts/validate_level3.py
bash -n scripts/install-codex.sh
bash -n scripts/install-antigravity.sh
bash scripts/test_installers.sh
python -m compileall -q skills
```

Checks include:

- backend-pattern documents and source/adaptation notes are present and non-trivial
- agent operating protocols are present and contain required inspection/risk/composition sections
- Level-3 fixture manifests/tasks reference real skills and valid verification commands
- routing evaluation cases reference only real skills and contain no contradictory expectations
- real-world scenarios contain required reasoning/routing sections
- every skill directory contains `SKILL.md`
- frontmatter name matches the directory
- model-invoked descriptions contain a concrete `Use when ...` discovery trigger
- user/model invocation policy is consistent between `SKILL.md` and `agents/openai.yaml`
- every skill contains observable completion criteria
- version-sensitive source metadata is fresh
- skill descriptions stay within the context-budget limits
- selected benchmark snapshots can be compared for regression history
- local `references/` and `examples/` links exist
- Python examples compile
- installer shell syntax is valid
- Codex and Antigravity installers copy the full skill directory, including `agents/openai.yaml`, references, and examples

See `SKILL_AUTHORING.md`, `AUTHORING/`, and `SCOPE.md` before adding a new skill.

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
- `donnemartin/system-design-primer`
- `ByteByteGoHq/system-design-101`
- `binhnguyennus/awesome-scalability`
- `HackSoftware/Django-Styleguide`
- `Sairyss/domain-driven-hexagon`
- `cookiecutter/cookiecutter-django`
- `mattpocock/skills` (invocation boundaries, context-pointer design, feedback loops, seams, completion criteria, and skill governance)

See `backend-patterns/SOURCES.md` for adaptation notes and the primary-authority rule.

Authoritative references used for reliability-sensitive rules:

- Django 3.2 documentation as the compatibility baseline
- Django 4.1 release notes for async ORM / `iterator()` + prefetch version gates
- Django 4.2 release notes for async `StreamingHttpResponse` version gates
- Celery 5.0 documentation as the compatibility baseline
- newer Celery documentation only when a feature is explicitly version-gated
- PostgreSQL official documentation for query plans, indexes, locks, and concurrent index behavior
- DRF official permissions documentation
- RFC 9110 for HTTP 202 semantics
- Stripe webhook documentation as a concrete production reference for signature verification, retries, duplicates, and ordering

## License

MIT
