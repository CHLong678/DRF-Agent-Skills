# Codebase Inspection Protocol

Use this protocol before substantial implementation, debugging, refactoring, or review in an unfamiliar Django/DRF codebase.

The goal is to prevent local edits based on incomplete context.

## 1. Establish runtime and compatibility

Inspect the project's actual:

- Python version
- Django version
- DRF version
- Celery version when used
- database engine/version
- cache/broker
- deployment/runtime process model

Likely sources:

- pyproject.toml
- requirements*.txt
- uv.lock
- poetry.lock
- Dockerfile / docker-compose files
- settings modules
- deployment manifests

Do not assume the repository baseline is the application's actual version.

## 2. Trace the entrypoint

For an API task inspect:

1. URL/router
2. view/viewset/action
3. serializer(s)
4. queryset/model(s)
5. service/domain function if present
6. task/integration calls
7. tests
8. schema/API documentation

For a Celery task inspect:

1. caller
2. transaction/on_commit boundary
3. task definition
4. queue/routing
5. retry/ack/time-limit settings
6. models/providers it changes
7. idempotency invariant
8. tests/monitoring

For a migration inspect:

1. model before/after
2. migration dependency chain
3. generated SQL
4. table size/write profile
5. deployment order
6. rollback/retry path

## 3. Search all callers before moving logic

Before extracting, renaming, or changing behavior:

- find all imports/callers
- find custom actions and management commands
- find Celery tasks and signals
- find tests
- find schema/client expectations

Do not infer ownership from one file.

## 4. Identify invariants and contracts

Write down the relevant invariant before changing code.

Examples:

- tenant A must never read tenant B
- an order may transition pending -> paid once
- duplicate task delivery must not duplicate charge
- PATCH omission is different from explicit null
- API response fields/status/error code must stay compatible

## 5. Identify boundaries

Locate:

- HTTP boundary
- transaction boundary
- process boundary
- queue/broker boundary
- external-provider boundary
- cache consistency boundary

Many backend bugs come from confusing these boundaries.

## 6. Inspect existing conventions

Prefer existing project conventions when they are safe.

Do not introduce:

- a service layer into one endpoint if the project has a coherent simpler pattern
- a new error envelope beside an established contract
- a second Celery routing style
- a different tenant-scoping mechanism

unless there is a concrete reason.

## 7. Form an evidence-based change hypothesis

Before editing, state:

- observed problem
- likely root cause
- files/boundaries affected
- chosen primary skill
- expected change
- verification method

If root cause is unknown, measure/inspect first.

## 8. Verify blast radius after editing

Re-check:

- callers
- tests
- migrations
- schema/OpenAPI
- permissions/tenant scope
- transaction/on_commit behavior
- query count
- queue/task behavior
- deployment compatibility

## Stop rule

Do not keep reading unrelated code after the relevant execution path, invariants, compatibility constraints, and verification strategy are sufficiently known.
