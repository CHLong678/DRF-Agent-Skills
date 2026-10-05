---
name: drf-background-jobs-contracts
description: HTTP/API contract guidance for long-running DRF operations backed by Celery or other workers. Use when returning 202 Accepted, exposing job status/progress, handling cancellation, retries, result downloads, or designing async bulk/report endpoints.
---

# DRF Background Job Contracts

## Use 202 intentionally

HTTP 202 means the request was accepted for processing but processing is not complete and may still fail later.

Do not return 202 if the work already completed synchronously.

## Prefer a durable job resource

For client-visible long work, create a durable record with a stable ID.

Typical response:

```json
{
  "job_id": "…",
  "status": "queued"
}
```

Optionally expose a status URL through response body/headers according to project conventions.

## Job states

Keep states explicit and stable, for example:

```text
queued
running
succeeded
failed
canceled
```

Avoid exposing raw Celery internal states directly as your public API contract unless you intentionally want to couple clients to Celery.

## Progress

Only expose progress if it is meaningful and measurable.

Prefer durable counters such as processed/total over fake percentages.

## Retries

A task retry should not look like a new public job unless the business operation is actually new.

Keep one job identity across internal retries where practical.

## Cancellation

Cancellation semantics must define whether cancellation is:

- requested
- accepted
- best-effort
- guaranteed before side effects

Do not promise hard cancellation if workers cannot safely interrupt the operation.

## Result delivery

Large results are often better represented as a stored artifact/download resource than inline in the status endpoint.

## Expiration

Define retention for completed job metadata/results.

## Security

Status/result endpoints must enforce the same tenant/ownership permissions as the operation that created the job.

## Deep reference

- `references/http-202-job-resource.md`

## Authoritative sources

- RFC 9110 HTTP 202: https://www.rfc-editor.org/rfc/rfc9110.html#name-202-accepted
- Celery 5.0 task/retry semantics: https://docs.celeryq.dev/en/v5.0.5/userguide/tasks.html
