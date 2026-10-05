# Webhook Signature, Deduplication, and Retry

## Signature verification

Many providers sign the exact raw request body.

Do not deserialize and re-serialize JSON before verifying unless the provider explicitly supports that.

## Replay protection

Signed timestamps can help reject old replayed payloads when the provider's scheme supports a tolerance window.

Use provider SDK behavior when available.

## Deduplication table

A generic durable shape:

```text
provider
event_id
event_type
received_at
processed_at
status
```

Enforce uniqueness on provider + event_id if that key is guaranteed unique.

## Transaction boundary

Claim the event ID and commit before dispatching background work:

```text
verify
→ atomic insert/claim
→ on_commit enqueue
→ 2xx
```

The worker must still be idempotent because dispatch/delivery can duplicate.

## Ordering

If provider ordering is not guaranteed:

- avoid sequence assumptions
- use object version/state when available
- fetch authoritative provider state for recovery-sensitive workflows
- record event metadata for audit/debugging
