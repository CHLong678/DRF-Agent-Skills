# HTTP 202 and Job Resources

## Semantics

202 Accepted says:

```text
request accepted
processing not finished
final success not guaranteed
```

Because HTTP cannot later resend a new final status for the original request, clients need another way to observe outcome.

## Recommended API shape

```text
POST /exports/
→ 202
→ job resource ID

GET /jobs/{id}/
→ queued/running/succeeded/failed

GET /jobs/{id}/result/
→ artifact/result when ready
```

The exact URLs are project conventions, not protocol requirements.

## Error representation

If the job fails after initial 202:

- store stable failure code
- store safe human detail
- do not leak traceback/secrets
- preserve operational error details in internal logs

## Idempotent creation

For operations clients may retry, consider an idempotency/business key so retrying the POST does not create duplicate jobs or duplicate business effects.
