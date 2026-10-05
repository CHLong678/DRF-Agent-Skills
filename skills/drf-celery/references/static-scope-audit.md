# Static Audit for Celery Tenant Scope

Use this reference when tenant isolation is important enough that missing scope should be caught in CI.

## Why static checks help

Celery tasks do not inherit HTTP request context. A task can accidentally query tenant-owned models without tenant/account restriction.

Tests catch known cases; static checks can catch new suspicious call sites during review.

## What to check

A project-specific static rule can flag Django ORM access inside Celery tasks unless one of these is present:

- an approved tenant-scope decorator/context
- an explicit tenant filter
- an intentional cross-tenant escape marker

Do not copy another project's model names or decorators.

## Escape hatches

An escape hatch should be explicit, rare, reviewable, and named to signal cross-tenant behavior.

## Baseline migration

For existing codebases:

1. detect current violations
2. generate a baseline
3. fail CI only on new violations
4. shrink the baseline as old code is migrated

This avoids all-or-nothing adoption while preventing new debt.
