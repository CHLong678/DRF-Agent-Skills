---
name: django-service-boundaries
description: Django application/service/module boundary guidance. Use when deciding where business logic belongs across views, serializers, models, services, selectors/query services, Celery tasks, management commands, modules, facades, or external adapters.
---

# Django Service and Module Boundaries

Read backend-patterns/service-module-boundaries.md for framework-neutral reasoning.

## Goal

Make business workflows traceable and reusable without forcing enterprise architecture onto simple Django code.

## When a service boundary helps

Use an application/service function when logic spans multiple models, owns a transaction, coordinates tasks/external providers, is reused by API/Celery/commands/webhooks, or expresses a meaningful business operation.

For simple CRUD, normal DRF hooks and serializer/model behavior can be enough.

## Deep modules

Prefer **deep modules**: a small interface that gives callers substantial useful behavior while hiding coordination complexity.

Evaluate a proposed boundary using:

- **leverage** — how much useful behavior callers get per concept they must understand
- **locality** — whether related change concentrates behind one interface
- **seam** — whether the boundary is a stable place to test/use the behavior

### Deletion test

Ask what happens if the abstraction is removed.

- If complexity disappears, the abstraction may be a shallow middleman.
- If complexity spills into many callers, the boundary may be providing real locality/leverage.

### Adapter test

One adapter often means a hypothetical seam.

A production adapter plus a meaningful test/local adapter, or multiple real implementations, makes the seam more concrete.

Do not add ports/adapters only to satisfy an architecture diagram.

## Read/query boundaries

Selectors/query services can help centralize complex reusable read paths, tenant scoping, and relation loading.

Do not wrap every ORM call merely to follow a pattern.

## Views and serializers

Keep HTTP parsing/status/authentication concerns at the interface.

Avoid surprising external side effects in serializer validation.

## Signals

Use signals when decoupling is genuinely valuable.

Avoid hiding tightly related core workflow steps inside implicit signals that make control flow hard to trace.

## Modules

Group by cohesive capability/domain, not automatically one app/module per entity.

Use explicit public interfaces/facades when a large codebase needs enforceable module boundaries.

## External integrations

Ports/adapters are useful when vendor complexity would otherwise leak through the application.

Do not create abstraction layers with only one trivial call and no meaningful isolation benefit.

## Routing contract

### Use this skill when
- deciding placement of business logic or cross-interface reuse
- service/selectors/module/facade/adapter boundaries are the primary design question
- a view/serializer/task has become workflow-heavy

### Do not use this skill when
- the task is straightforward CRUD with no architectural pressure
- the main concern is transaction mechanics; use drf-transactions-concurrency
- the task is generic DRF view/serializer mechanics; use drf-views or drf-serializers

### Inspect first
- all callers of the workflow
- models and transaction boundary
- external side effects
- existing project service/query conventions
- duplicated logic
- module ownership and dependency direction
- tests

### Related skills
- drf-core, django-architecture-enforcement, drf-views, drf-serializers, drf-transactions-concurrency

## Deep reference

- references/services-selectors-modules.md

## Completion criteria

Done when:
- the business operation and all important callers are known
- the proposed boundary increases leverage/locality rather than adding a shallow middleman
- transaction and side-effect ownership are explicit
- callers can be tested through a stable seam
