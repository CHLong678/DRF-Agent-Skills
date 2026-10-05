# Compatibility Policy

This repository targets production Django REST Framework projects with:

- Django >= 3.2
- Celery >= 5.0 when Celery is used
- a DRF version that officially supports the installed Django version

## Agent rule: inspect versions first

Before using a version-sensitive API, inspect the project's actual versions from files such as:

- `pyproject.toml`
- `requirements*.txt`
- `Pipfile.lock`
- `poetry.lock`
- `uv.lock`

Also inspect the Python version when syntax/runtime behavior may differ.

Do not assume latest Django, DRF, Celery, Python, drf-spectacular, Redis client, or database behavior.

## Baseline-first behavior

If the installed version is unknown, generate code compatible with the baseline:

- Django 3.2
- Celery 5.0
- conservative Python syntax compatible with the project's declared runtime

Use newer APIs only after confirming the installed version supports them.

## Important Django version gates

### Django 3.2

- async views are supported
- Django ORM is still synchronous from async code; use `sync_to_async(..., thread_sensitive=True)` around a cohesive synchronous DB function
- `QuerySet.iterator()` ignores prior `prefetch_related()` calls
- `StreamingHttpResponse` expects a synchronous iterator

### Django >= 4.1

- async ORM interfaces such as async iteration / `a*` QuerySet methods begin to become available
- `iterator(chunk_size=...)` can preserve `prefetch_related()` behavior when an explicit chunk size is provided

### Django >= 4.2

- `StreamingHttpResponse` supports asynchronous iterators under ASGI

Do not emit a newer pattern without checking the project's installed Django version.

## Important Celery version gates

Baseline Celery 5.0 supports the core patterns used by these skills:

- `Task.retry()` / `autoretry_for`
- retry backoff
- late acknowledgements
- routing/queues
- prefetch multiplier
- Canvas primitives/chunks
- monitoring/inspect

Newer Celery configuration must be gated. Examples:

- `worker_enable_prefetch_count_reduction` requires Celery >= 5.4
- `worker_disable_prefetch` requires Celery >= 5.6 and is currently Redis-broker specific

When a setting is newer than Celery 5.0, provide a 5.0-compatible alternative or omit it.

## DRF compatibility

DRF compatibility depends on both DRF and Django versions.

Agents must inspect the installed DRF version before using version-sensitive DRF behavior. Prefer stable framework hooks (`get_queryset`, `get_serializer_class`, `perform_create`, permissions, pagination, serializers) that exist across supported generations.

Third-party package behavior such as drf-spectacular, django-filter, SimpleJWT, and django-redis must be checked independently.

## Database compatibility

Database-specific features must be conditional.

For example:

- PostgreSQL supports useful row-locking/server-side-cursor patterns
- `skip_locked`, conflict handling, JSON/Array lookups, and index types vary by backend/version

Do not present a PostgreSQL-specific optimization as universal Django behavior.
