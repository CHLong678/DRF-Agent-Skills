---
name: drf-skill-router
description: Route ambiguous or cross-cutting Django REST Framework tasks to the smallest correct set of repository skills. Use when multiple skills appear relevant, the bottleneck/domain is not yet known, or a task spans API, database, Celery, security, and production concerns.
---

# DRF Skill Router

## Purpose

This is a routing skill, not a replacement for domain skills.

Use it to choose:
- one primary skill
- zero or more necessary secondary skills
- the order in which they should be read

Do not load every related skill.

## Routing procedure

1. Identify the user's requested outcome.
2. Identify the layer where the decision currently lives.
3. If the layer is unknown, choose the diagnostic skill first.
4. Select the most specific primary skill.
5. Add secondary skills only for real cross-boundary concerns.
6. Stop loading once the required decision can be made safely.

## Diagnostic-first rule

Examples:

- "API is slow" with no evidence -> `drf-observability` first.
- "PostgreSQL plan shows Seq Scan" -> `postgresql-for-django`.
- "serializer causes N+1" -> `drf-orm-performance` + `drf-serializers`.
- "Celery queue is backing up" -> `drf-celery`.
- "request returns 202; how should client poll?" -> `drf-background-jobs-contracts`.

## Deep reference

Read `references/routing-matrix.md` for precedence and overlap rules.

## Routing contract

### Use this skill when
- multiple skills plausibly match
- the problem crosses API/database/Celery/security/production boundaries
- the root domain is not yet known

### Do not use this skill when
- one specific skill clearly owns the task
- the user explicitly selected a domain skill and no cross-boundary decision is needed

### Inspect first
- the requested outcome
- named files/components
- current execution boundary
- framework/database/task versions when relevant
- whether the task is implementation, debugging, review, or architecture

### Related skills
- `ROUTING.md` and `references/routing-matrix.md` are the routing source of truth
- after routing, use the chosen primary domain skill as authoritative
