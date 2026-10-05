# Serializer Schema Typing

Use this reference when serializer shape feeds OpenAPI, generated clients, frontend types, validation schemas, or agent/MCP tooling.

## Treat serializer metadata as contract metadata

`help_text`, field type, nullability, required/read-only/write-only flags, and choices can flow into generated OpenAPI schemas.

Write useful `help_text` for non-obvious externally consumed fields:

- describe purpose, not only primitive type
- state format constraints when relevant
- mention meaningful defaults
- explain null/empty semantics when ambiguous
- list or expose valid constrained values through `choices`

Do not add noisy descriptions to every trivial internal field merely to satisfy a style rule.

## Type composite fields

Prefer:

```python
tags = serializers.ListField(
    child=serializers.CharField(),
    help_text="Tags attached to this resource.",
)
```

over a bare `ListField()` when item type is known.

For dictionaries whose values share one shape:

```python
properties = serializers.DictField(
    child=serializers.CharField(),
)
```

For `JSONField`, if the JSON structure is stable and consumed as an API contract, document/annotate that structure with the project's schema tooling instead of accepting a permanently untyped `object`.

Do not invent a rigid schema for genuinely arbitrary metadata.

## SerializerMethodField

Computed fields often need explicit schema information.

With drf-spectacular, one possible pattern is:

```python
from drf_spectacular.utils import extend_schema_field

class TeamSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()

    @extend_schema_field(serializers.IntegerField())
    def get_member_count(self, obj):
        return obj.member_count
```

This is tool-specific. Use the schema mechanism already installed in the project.

## Named choices

For repeated or public enum-like values, prefer named choice classes when practical:

```python
class OrderStatus(models.TextChoices):
    NEW = "new", "New"
    PAID = "paid", "Paid"
    CANCELED = "canceled", "Canceled"
```

Named choices improve reuse and can reduce OpenAPI enum-name collisions in schema generators.

Do not force model enums into framework-free domain modules that intentionally avoid importing Django; use an equivalent framework-independent enum there.

## Response typing

If a response shape is consumed by clients or generated tooling, prefer an explicit response serializer instead of returning an undocumented raw dict/list.

Runtime-valid code:

```python
return Response({"status": "ok", "id": obj.pk})
```

can still produce a weak or inaccurate API schema.

## Compatibility

These principles are compatible with Django 3.2+ and ordinary DRF serializers.

drf-spectacular examples are optional and must be used only when that package/version exists in the target project.
