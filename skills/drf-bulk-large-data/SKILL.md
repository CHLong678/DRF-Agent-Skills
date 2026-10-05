---
name: drf-bulk-large-data
description: Django REST Framework large-data and bulk-processing guidance. Use for large imports/exports, bulk create/update APIs, huge QuerySets, chunking, iterator/server-side cursors, streaming CSV, memory-safe jobs, or deciding when to move work to Celery.
---

# DRF Bulk & Large Data

## Start with workload shape

Before choosing an implementation, determine:

- expected row count
- request/response size
- synchronous latency budget
- memory budget
- whether results must be immediate
- database write/read pressure
- failure/retry requirements
- client retry behavior

Do not design a million-row endpoint like ordinary CRUD.

## Choose the execution model

### Synchronous request

Use when work is predictably small and completes well within request/proxy timeouts.

### Streaming response

Use for large read/export responses when rows can be produced incrementally and the client must receive the data directly.

### Background job

Use Celery/job processing when work is long-running, retryable, CPU-heavy, or too expensive to hold an HTTP worker.

For very large export generation, a background job that writes an object/file and later returns a download URL can be operationally safer than keeping one HTTP connection open for minutes.

## Avoid materializing huge QuerySets

Normal QuerySet iteration caches results.

For one-pass processing of many rows, consider:

    queryset.iterator(chunk_size=2000)

`iterator()` avoids QuerySet-level result caching and can significantly reduce memory for large one-pass workloads.

If you use `prefetch_related()`, provide an explicit `chunk_size`; Django only preserves prefetch behavior with `iterator()` when chunk size is supplied.

Choose chunk size by measurement: larger chunks reduce round trips but use more memory.

## PostgreSQL server-side cursors

With PostgreSQL, Django can use server-side cursors for `iterator()` when server-side cursors are enabled.

Be careful when using transaction-pooling connection poolers such as PgBouncer. Verify Django's documented server-side cursor constraints instead of assuming streaming works identically in every deployment.

## Fetch only what you need

For export/batch logic that does not need model methods, consider:

- `values()`
- `values_list()`
- narrow annotations
- selecting only required relations

Be cautious with `only()` / `defer()` when later code accesses deferred fields; that can create hidden per-row queries.

## Bulk create

`bulk_create()` can drastically reduce insert query count, but understand its semantics:

- model `save()` is not called
- `pre_save` / `post_save` signals are not sent
- many-to-many relationships are not created by the call
- generators are normally cast to a list by Django
- conflict options are database-dependent

For generated/unbounded input, batch with `islice()` or equivalent rather than building every model instance in memory first.

Example shape:

    iterator = (Event(**row) for row in source_rows)
    while batch := list(islice(iterator, 1000)):
        Event.objects.bulk_create(batch, batch_size=1000)

Do not use bulk APIs when correctness depends on overridden `save()` or signals unless you explicitly reproduce the required behavior.

## Bulk update

`bulk_update()` is efficient but has important memory behavior.

Django prepares `WHEN` clauses for objects across batches before executing queries; with many rows/fields this can consume more memory than expected.

For huge updates:

1. iterate IDs in bounded chunks
2. load only one chunk
3. compute changes
4. `bulk_update()` that chunk
5. release references and continue

Also prefer a single `QuerySet.update()` when every row can receive the same database expression/value.

## `QuerySet.update()` and `F()` expressions

For set-based updates, push work into the database when semantics are simple.

Examples:

    Account.objects.filter(active=True).update(
        login_count=F("login_count") + 1
    )

This avoids loading objects into Python and can avoid read-modify-write races for arithmetic updates.

Remember that `update()` bypasses model `save()` and related save signals.

## Transactions

Do not wrap a very large multi-minute import/export in one transaction by default.

Long transactions increase lock duration, database resource use, and failure blast radius.

Choose transaction boundaries per chunk or per business atomic unit unless the entire operation must truly be all-or-nothing.

If all-or-nothing semantics are mandatory for huge operations, explicitly assess lock/WAL/rollback cost.

## Locking and worker coordination

For multiple workers claiming rows from a shared work table, `select_for_update(skip_locked=True)` can be useful on supported databases such as PostgreSQL.

Use it only inside `transaction.atomic()`.

Pattern:

    with transaction.atomic():
        rows = list(
            WorkItem.objects
            .filter(status="pending")
            .select_for_update(skip_locked=True)
            .order_by("id")[:batch_size]
        )
        WorkItem.objects.filter(id__in=[x.id for x in rows]).update(
            status="processing"
        )

Then commit before doing slow external work unless the lock must intentionally cover that work.

`skip_locked` is a queue/claiming technique, not a universal substitute for Celery/broker semantics.

## Streaming exports

Django's `StreamingHttpResponse` can stream generated content without buffering the whole response body in memory.

For large CSV:

- use a generator
- combine with `iterator(chunk_size=...)` when reading many DB rows
- write one row/chunk at a time
- set content type/disposition correctly
- handle client disconnects where needed

Streaming reduces response-memory pressure but does not make expensive queries cheap and does not automatically protect database connections from long-lived workloads.

Under ASGI, streaming content should match the async execution model; under WSGI, use a synchronous iterator.

## Import validation strategy

For large imports, avoid validating every row and storing all normalized data in memory before writing.

Use a staged pipeline when appropriate:

1. validate file/request metadata
2. read bounded chunks
3. normalize/validate rows
4. collect row-level errors with bounded storage
5. write valid chunk
6. checkpoint progress

Decide whether partial success is allowed before implementation.

Do not accidentally provide partial writes if the public API promises atomic import semantics.

## Error reporting

For bulk APIs, define a stable error model:

- all-or-nothing vs partial success
- row/item index or stable item identifier
- machine-readable error code
- maximum number of returned errors
- job-level failure vs item-level failure

Do not return millions of validation errors in one HTTP response.

## API size limits

Bound:

- number of items per bulk request
- uploaded file size
- page size
- filter ranges
- exported range

Make limits explicit in validation and documentation.

Choose limits from operational capacity, not arbitrary round numbers.

## Celery chunking

For background bulk work, use bounded task chunks rather than one task per row or one giant task.

See `drf-celery` for retry, idempotency, queue isolation, and Celery Canvas chunk guidance.

## Observability

Track at least:

- rows/items processed
- rows/sec
- chunk duration
- DB query time
- memory high-water mark where available
- error/retry counts
- queue depth for background jobs
- generated file size/export duration

A bulk implementation is not production-ready if operators cannot tell whether it is progressing or stalled.

## Review checklist

Check:

- bounded input/output?
- avoids full QuerySet/list materialization?
- iterator/chunk size appropriate?
- bulk APIs compatible with model/save/signal semantics?
- transaction scope short enough?
- partial-success contract explicit?
- retries/idempotency safe?
- streaming vs background-job choice justified?
- export/import memory bounded?
- query/lock pressure measured?

## Authoritative references

- Django QuerySet API (`iterator`, `bulk_create`, `bulk_update`, `select_for_update`): https://docs.djangoproject.com/en/5.2/ref/models/querysets/
- Django StreamingHttpResponse: https://docs.djangoproject.com/en/5.2/ref/request-response/#streaminghttpresponse-objects
- Django large CSV streaming: https://docs.djangoproject.com/en/5.2/howto/outputting-csv/
- Django transactions: https://docs.djangoproject.com/en/5.2/topics/db/transactions/
- Celery Canvas/chunks: https://docs.celeryq.dev/en/main/userguide/canvas.html
