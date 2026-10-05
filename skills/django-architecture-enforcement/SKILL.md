---
name: django-architecture-enforcement
description: Mechanical enforcement of Django/DRF architectural and security boundaries. Use when important conventions such as tenant scoping, layer boundaries, forbidden imports, state transitions, or safe task patterns should be checked by CI/static analysis instead of relying only on code review.
---

# Django Architecture Enforcement

## Principle

If violating a convention can cause security, data-isolation, or large maintainability failures, consider making it mechanically checkable.

Examples:

- API/presentation code must not bypass service/facade boundaries
- tenant-scoped models must not be queried unscoped
- Celery tasks must establish tenant scope
- sensitive state transitions must go through one approved path
- dangerous imports/APIs must not be used directly

Do not lint preferences that are cheap to review and expensive to encode.

## Choose the lightest tool

Options include:

- tests
- Django system checks
- custom management-command checks
- Semgrep
- import-linter
- dependency graph tools
- CI scripts that introspect Django's app/model registry

Use the tool that expresses the invariant clearly with low false-positive cost.

## Architecture boundaries

For layered code, enforce the project's actual dependency direction rather than inventing a new architecture solely for linting.

See `references/import-boundaries.md`.

## Security coverage from model introspection

A strong pattern is:

1. introspect registered Django models
2. identify models with tenant/org/user ownership
3. compare them against the project's protection mechanism
4. fail CI when a new scoped model lacks protection

See `references/model-scope-coverage.md`.

## Baselines

For legacy systems, baseline existing violations mechanically where possible. New violations should fail while the baseline shrinks over time.

## Escape hatches

Prefer explicit APIs/decorators such as `unscoped()`, `cross_tenant()`, or `skip_scope_audit` over broad suppressions.

## Compatibility

These are tooling/architecture patterns and can apply to Django 3.2+.

## Routing contract

### Use this skill when
- an important architecture/security invariant should be enforced mechanically in CI/static analysis

### Do not use this skill when
- the architecture rule itself has not been established yet
- the issue is only style/readability

### Inspect first
- invariant and failure mode
- current architecture/dependency direction
- false-positive/escape-hatch cost
- existing CI/lint tooling

### Related skills
- pair with the domain skill that defines the invariant, such as `drf-auth-security` or `drf-celery`
