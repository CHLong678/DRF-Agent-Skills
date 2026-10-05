# Django Import-Path Checklist

## Investigation

1. measure a baseline
2. capture import timing
3. identify the import edge that brings a heavy subtree onto startup
4. confirm the cost is removable, not simply relocated through another edge
5. change one edge
6. re-measure

## High-risk startup import locations

- `apps.py` / `AppConfig.ready()`
- `models.py` and `models/__init__.py`
- signals modules
- root package `__init__.py`
- API router aggregators
- settings helpers
- Celery app import hooks

## Regression tests

After deferring imports, run representative non-web paths:

```text
django.setup()
manage.py check
manage.py makemigrations --check
manage.py shell
Celery worker/task import
URLconf import
```

Also test the behavior that depended on registration, such as signals.

## Circular imports

Eager import order can hide an existing circular dependency. Removing one eager edge may expose it.

Fix the cycle rather than restoring an unrelated eager import solely to preserve accidental ordering.

## Rule

Startup performance work is architecture work. Treat import paths as dependencies, not cosmetic style.
