---
name: drf-bulk-large-data
description: Django REST Framework large-data and bulk-processing guidance compatible with Django 3.2+. Use for large imports/exports, bulk create/update APIs, huge QuerySets, chunking, iterator/server-side cursors, streaming CSV, memory-safe jobs, or deciding when to move work to Celery.
---

# DRF Bulk & Large Data

## Compatibility baseline

This skill must work with Django 3.2+.

Version-sensitive QuerySet and streaming behavior must be gated.

## Start with workload shape

Determine expected row count, request/response size, latency budget, memory budget, DB pressure, failure/retry requirements, and client retry behavior.

Do not design a million-row endpoint like ordinary CRUD.

## Choose the execution model

- synchronous request: predictably small work
- streaming response: large incremental reads when the client needs direct output
- background job: long-running, retryable, CPU-heavy, or operationally expensive work

For very large exports, generating a file in a background job and returning a later download URL is often safer than holding one HTTP connection open.

## `iterator()` version behavior

`iterator()` avoids QuerySet-level result caching and can reduce memory for one-pass processing.

Baseline Django 3.2 example:

    for row in queryset.iterator(chunk_size=2000):
        process(row)

Important version gate:

- Django 3.2 through 4.0: prior `prefetch_related()` calls are ignored when `iterator()` is used
- Django >= 4.1: `iterator(chunk_size=...)` can preserve prefetching when an explicit chunk size is provided

Therefore, on Django 3.2-4.0, do not combine `iterator()` with an expectation that prefetched relations remain available. Instead redesign the query, process IDs in chunks and hydrate each chunk, or tolerate bounded related queries deliberately.

Choose chunk size by measurement.

## PostgreSQL server-side cursors

With PostgreSQL, Django can use server-side cursors for `iterator()` when enabled.

Verify deployment constraints when using transaction-pooling connection poolers such as PgBouncer.

## Fetch only what you need

Consider `values()`, `values_list()`, narrow annotations, and only required relations when model instances are unnecessary.

Be cautious with `only()` / `defer()` because later access to deferred fields can create hidden queries.

## Bulk create

`bulk_create()` reduces insert query count, but model `save()` is not called, save signals are not sent, and many-to-many relationships are not created by the call.

Django normally casts the provided iterable to a list. For generated/unbounded input, manually batch without requiring modern Python syntax:

    from itertools import islice

    objects = (Event(**row) for row in source_rows)
    while True:
        batch = list(islice(objects, 1000))
        if not batch:
            break
        Event.objects.bulk_create(batch, batch_size=1000)

Conflict/update-conflict options are version- and database-dependent. For example, `bulk_create(update_conflicts=...)` is a newer Django feature and must not be emitted for Django 3.2.

## Bulk update

`bulk_update()` is available in Django 3.2, but large batches can consume substantial memory.

For huge updates, iterate IDs in bounded chunks, load one chunk, compute changes, `bulk_update()` it, then release references.

Prefer a single `QuerySet.update()` when all rows can receive the same database expression/value.

## Set-based updates

Use `QuerySet.update()` and `F()` expressions when semantics are simple and model `save()`/signals are not required.

## Transactions

Do not wrap a very large multi-minute operation in one transaction by default.

Use transaction boundaries per chunk or business atomic unit unless the whole operation must truly be all-or-nothing.

## Locking and worker coordination

`select_for_update(skip_locked=True)` can help multiple workers claim rows on supported databases such as PostgreSQL.

Use it only inside `transaction.atomic()` and verify database support.

Commit the claim before slow external work unless the lock intentionally must cover that work.

## Streaming exports

`StreamingHttpResponse` exists in Django 3.2 and can stream a synchronous iterator without buffering the whole response body.

For Django 3.2 through 4.1, use a synchronous iterator.

Async iterator support for `StreamingHttpResponse` starts in Django 4.2 and must be version-gated.

Streaming reduces response-memory pressure but does not make an expensive query cheap and may hold a WSGI worker for the response duration.

## Large import strategy

Process bounded chunks: validate metadata, read a chunk, normalize/validate rows, keep bounded error storage, write the chunk, checkpoint progress.

Decide whether partial success is allowed before implementation.

## Error and size contracts

Define all-or-nothing vs partial success, stable item identifiers, machine-readable errors, maximum returned errors, and explicit limits for item count/file size/page size/filter/export range.

## Celery chunking

For background bulk work, use bounded task chunks rather than one task per row or one giant task. See `drf-celery`.

## Observability

Track rows processed, rows/sec, chunk duration, DB time, memory where available, errors/retries, queue depth, file size, and export duration.

## Authoritative baseline references

- Django 3.2 QuerySet API: https://docs.djangoproject.com/en/3.2/ref/models/querysets/
- Django 3.2 DB optimization: https://docs.djangoproject.com/en/3.2/topics/db/optimization/
- Django 3.2 StreamingHttpResponse: https://docs.djangoproject.com/en/3.2/ref/request-response/
- Django 4.1 release notes for iterator/prefetch behavior: https://docs.djangoproject.com/en/4.1/releases/4.1/
- Django 4.2 release notes for async streaming: https://docs.djangoproject.com/en/4.2/releases/4.2/
