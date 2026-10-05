---
name: django-startup-performance
description: Django startup and import-path performance guidance compatible with Django 3.2+. Use when django.setup(), management commands, migrations, tests, web worker boot, or Celery worker startup are slow, or when large API/router imports and AppConfig.ready() chains load too much code.
---

# Django Startup Performance

## Measure first

Profile startup before refactoring imports.

Useful targets:

- bare `django.setup()`
- `manage.py shell -c '1'`
- migration/check commands
- Celery worker boot
- web worker boot

Python's `-X importtime` can identify expensive import paths; validate suspected improvements with before/after measurements.

## Keep setup paths light

Be suspicious of heavy imports from:

- `AppConfig.ready()`
- model modules
- signals imported during setup
- package `__init__.py` aggregators
- global API/router aggregators
- settings-time helpers

Do not import vendor SDKs, full task graphs, API stacks, or unrelated product modules at startup unless every process truly needs them.

## `AppConfig.ready()`

`ready()` runs during Django setup in web workers, management commands, tests, migrations/check paths, and often worker processes.

Keep it focused on lightweight registration.

If a signal receiver needs a heavy dependency, consider importing that dependency inside the receiver when invoked, or extracting the receiver into a lightweight module.

Always test that receivers still register in non-web processes.

## Lazy imports are cost relocation

Deferring an import does not make the work disappear.

Ask:

- which process pays now?
- on which first-use path?
- is that path latency-sensitive?

If first use is a hot user request, a targeted process warm-up may be better than fully lazy loading.

## Package aggregators

Python imports a package `__init__.py` before submodules.

An `__init__.py` that eagerly imports all siblings can make importing one small constant load an entire subsystem.

Prefer lightweight package roots. Advanced lazy-module tricks should be used only in very large codebases with tests for import semantics.

## Router/API aggregation

In very large DRF projects, importing hundreds of ViewSets just to execute `django.setup()` can slow shell, migrations, tests, and Celery startup.

Measure whether API route aggregation is on the setup path before redesigning it.

Do not copy a lazy-router architecture into a normal project without evidence.

## Import-time serializer work

Serializer field arguments execute at class definition/import time.

Code such as:

```python
choices=sorted(load_choices_from_heavy_module())
```

can make importing serializers expensive.

Keep lightweight constants/enums in import-light modules when they are needed during class definition.

## Model registration safety

Do not accidentally make a model importable only through a lazily loaded ViewSet.

After import refactors verify:

- `makemigrations` sees models
- app registry is complete
- admin registration still works
- signals still connect
- management commands and Celery startup work

## References

Read `references/import-path-checklist.md` for an audit checklist and safe refactoring workflow.

## Routing contract

### Use this skill when
- django.setup(), manage.py, tests, web worker, or Celery worker startup is slow because of import paths/registration

### Do not use this skill when
- runtime request latency is the problem; start with `drf-observability`

### Inspect first
- startup timing/import profile
- AppConfig.ready()
- model/signal/package imports
- router aggregation
- management/Celery import paths

### Related skills
- `django-architecture-enforcement`, `drf-observability`
