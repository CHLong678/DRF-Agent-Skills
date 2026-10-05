# OpenAPI and Runtime Parity

Use this reference when schema annotations, generated clients, or custom DRF actions are involved.

## Runtime is the source of truth

OpenAPI must describe what the endpoint actually accepts and returns.

A schema override can accidentally narrow runtime behavior:

```python
@extend_schema(request=PatchSerializer)
def partial_update(...):
    ...
```

If the runtime serializer accepts fields omitted from `PatchSerializer`, generated clients and agent tools will incorrectly believe those fields do not exist.

Before overriding inferred schemas:

1. identify the runtime serializer and action
2. list accepted body/query/path fields
3. ensure the explicit schema is equivalent or intentionally changed
4. regenerate/inspect schema if the project commits generated artifacts

## Custom actions

Custom `@action` and plain `ViewSet` methods often need explicit request/response documentation because inference is weaker than for conventional `ModelViewSet` CRUD.

Document when inference is insufficient:

- body serializer
- query parameters
- path parameters
- success serializer
- meaningful error responses
- content type for streaming endpoints

## Query parameter serializers

When query parameters have real structure or validation, a serializer can be clearer than repeated manual parsing:

```python
class ExportQuerySerializer(serializers.Serializer):
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()
    limit = serializers.IntegerField(min_value=1, max_value=10000, required=False)
```

Then validate `request.query_params` with the project convention.

This is especially useful for non-filter query parameters, complex actions, and generated API schemas.

Do not replace a clean `django-filter` FilterSet with a second serializer that duplicates the same filter contract.

## Response serializers

For consumed APIs, serialize stable success response shapes even when no model is involved.

```python
class JobAcceptedSerializer(serializers.Serializer):
    job_id = serializers.UUIDField()
    status = serializers.ChoiceField(choices=["queued"])
```

This improves OpenAPI, client generation, and backward-compatibility review.

## Streaming endpoints

Streaming/SSE responses may not have a normal structured response serializer, but the request and content type should still be documented where the schema tooling supports it.

## Machine-readable errors

Prefer stable machine-readable error codes in addition to human-readable detail when clients branch on error type.

Do not make clients parse human text.
