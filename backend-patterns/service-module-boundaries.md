# Service and Module Boundaries

## Goal

Make business behavior traceable without forcing unnecessary architecture.

## Interface vs core

HTTP views and serializers are interface adapters.

Business rules that must also work from Celery tasks, management commands, webhooks, scripts, or other APIs should not depend unnecessarily on an HTTP request/view implementation.

## Service/application layer

A service/application function is useful when a workflow spans multiple models, owns a transaction, coordinates side effects, is reused from multiple interfaces, or contains meaningful domain decisions.

A trivial CRUD endpoint does not automatically require a service layer.

## Read selectors / query services

A dedicated read function can help when query logic is reused, relation loading is non-trivial, tenant/filter rules must be centralized, or derived data spans relations.

Do not create selector wrappers that merely rename Model.objects.get() without adding clarity.

## Model behavior

Simple behavior based on one object's local fields may fit naturally on the model/domain object.

Relation-heavy queries and orchestration are usually easier to reason about outside a property that silently hits the DB.

## Modules / bounded contexts

Group code by cohesive business capability, not automatically one module per database entity.

Prefer explicit public interfaces between modules and avoid reaching deeply into another module's internals.

## Facade / public module API

A module facade can make allowed cross-module operations explicit and protect internals from accidental coupling.

Use only when the project is large enough that module boundaries matter.

## Ports and adapters

External systems may benefit from an application-facing interface when vendor APIs are complex, multiple implementations exist, tests need isolation, or vendor-specific models would otherwise leak widely.

Do not create an interface for every library call merely to satisfy an architecture diagram.

## Dependency direction

Prefer core business decisions that do not need to import DRF, Celery, or provider-specific code.
