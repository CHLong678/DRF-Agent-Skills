# Stable Machine-Readable API Errors

Use this reference when clients, frontend code, automation, or agents need to branch on API failure type.

## Separate machine contract from human text

Human-readable messages change. Machine-readable codes should remain stable when clients depend on them.

Prefer a shape such as:

```json
{
  "code": "database_schema_unavailable",
  "detail": "Could not load the schema. Try again later."
}
```

Do not require clients to match exact prose.

## Status and code have different jobs

HTTP status communicates the broad protocol result. A stable application code identifies the specific failure.

Examples:

```text
409 + order_already_paid
503 + provider_temporarily_unavailable
503 + database_schema_unavailable
```

Prefer standard HTTP status codes plus application codes.

## DRF APIException pattern

```python
from rest_framework import status
from rest_framework.exceptions import APIException

class Conflict(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_code = "conflict"
    default_detail = "The requested operation conflicts with current state."
```

Create narrower subclasses when clients need a distinct stable code.

## Retryable failures

For temporary overload/capacity failures:

- use 429/503 as appropriate
- provide Retry-After where useful
- consider bounded retry jitter at the client/system level to avoid synchronized retries

Do not recommend retry for deterministic validation or business-rule failures.

## Observability

Use stable error codes as low-cardinality dimensions such as endpoint, status, and error_code.

Do not label metrics with arbitrary detail text or raw identifiers.

## Domain-to-DRF translation

Keep domain/application errors framework-independent where practical, then translate them at the API boundary into ValidationError/APIException.
