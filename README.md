# DRF Agent Skills

A focused collection of Agent Skills for building and reviewing production Django REST Framework code.

Designed specifically for:

- OpenAI Codex
- Google Antigravity

The repository intentionally avoids generic frontend, non-Django, and unrelated framework guidance. Each skill is narrow enough to load only when relevant.

## Skills

| Skill | Purpose |
|---|---|
| `drf-core` | Architecture, API boundaries, service-layer guidance, response/error conventions |
| `drf-serializers` | Serializer design, validation, nested data, read/write separation |
| `drf-views` | APIView, GenericAPIView, mixins, generic views, ViewSets, actions, lifecycle |
| `drf-orm-performance` | QuerySet design, N+1 prevention, annotations, bulk work, indexing guidance |
| `drf-transactions-concurrency` | `atomic`, `select_for_update`, `on_commit`, race conditions, idempotency |
| `drf-auth-security` | Authentication, permissions, object access, throttling, secure API behavior |
| `drf-testing` | pytest-django, API tests, factories, transaction/concurrency tests |
| `drf-code-review` | DRF-specific code review checklist and risk prioritization |

## Design principles

These skills were inspired by production-grade agent-skill repositories such as ECC, but the rules here are deliberately tightened for DRF and corrected where generic examples are unsafe or overly broad.

Key corrections include:

- `select_for_update()` must execute inside an active transaction.
- Celery/external side effects that depend on committed state should usually be triggered with `transaction.on_commit()`.
- Do not create database indexes merely because a field appears in `filter()` or `order_by()`; require workload/selectivity/query-plan justification.
- PostgreSQL projects should test important database behavior against PostgreSQL rather than assuming SQLite equivalence.
- Avoid legacy Django/browser security settings as blanket recommendations.
- Serializer validation should not perform surprising side effects.
- Views should orchestrate HTTP concerns; complex reusable business workflows belong in services/domain functions.

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
drf-code-review
```

Add `drf-auth-security` and `drf-testing` where appropriate.

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

## Repository philosophy

The skills should prefer the existing project's conventions unless they are clearly unsafe. They should not refactor unrelated code, invent abstractions prematurely, or turn DRF code into architecture for architecture's sake.

Before changing code, agents should inspect nearby serializers, views, models, services, tests, and shared utilities to preserve local consistency and backward compatibility.

## License

MIT
