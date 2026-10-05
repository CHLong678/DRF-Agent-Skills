---
name: drf-webhooks-integrations
description: Secure and reliable webhook/integration endpoint guidance for Django REST Framework. Use when receiving third-party webhooks, verifying signatures, deduplicating deliveries, handling retries/out-of-order events, or dispatching webhook work to Celery.
---

# DRF Webhooks & Integrations

## Assume duplicate and out-of-order delivery

Webhook providers may retry and may not preserve event order.

Design handlers to tolerate:

- duplicate delivery
- delayed delivery
- out-of-order delivery
- manual resend
- provider retry after non-2xx responses

## Verify authenticity before processing

Use the provider's supported signature verification mechanism when available.

Important rules:

- verify against the raw request body if the provider requires it
- keep endpoint secrets out of code
- reject invalid/stale signatures according to provider guidance
- use constant-time comparison if implementing HMAC verification manually

Prefer official SDK verification over custom crypto.

## Idempotency

Persist a durable provider event ID or equivalent deduplication key.

Typical flow:

1. verify signature
2. parse minimal envelope
3. atomically claim/store event ID
4. if already processed/claimed, return successful acknowledgement
5. enqueue/process idempotently

Do not use event timestamp alone as duplicate detection.

## Respond quickly

Avoid expensive business logic in the webhook request path.

If work is non-trivial:

- store/claim the event durably
- enqueue after commit
- return 2xx promptly

## Event ordering

Do not assume one event type always arrives before another.

When correctness depends on authoritative current state, consider fetching the current object/state from the provider rather than reconstructing it only from event order.

## Secrets and logs

Do not log signing secrets, raw credentials, or sensitive payloads by default.

## Failure contract

Differentiate:

- invalid signature/payload: 4xx
- temporary internal failure: 5xx if you want provider retry
- accepted/already processed: 2xx

Understand the provider's retry semantics before choosing status codes.

## Deep reference

- `references/signature-dedup-retry.md`

## Authoritative source

Stripe webhook documentation is used as a concrete production reference for duplicate delivery, retry, ordering, raw-body signature verification, and replay protection:
https://docs.stripe.com/webhooks

## Routing contract

### Use this skill when
- receiving provider webhooks, verifying signatures, handling duplicate/out-of-order delivery, or dispatching webhook work

### Do not use this skill when
- the task is a generic outbound HTTP integration with no webhook semantics
- the main issue is worker tuning after webhook dispatch; use `drf-celery`

### Inspect first
- provider signature/retry/order docs
- raw-body handling
- event ID/dedup storage
- transaction/on_commit boundary
- response timeout expectations

### Related skills
- `drf-celery`, `drf-transactions-concurrency`, `drf-auth-security`
