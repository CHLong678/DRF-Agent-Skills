# DRF View Hooks and Lifecycle

Use this reference when deciding where endpoint-specific behavior belongs.

## GenericAPIView/ViewSet hooks

Common extension points:

- `get_queryset()`
- `get_serializer_class()`
- `get_permissions()`
- `get_serializer_context()`
- `perform_create()`
- `perform_update()`
- `perform_destroy()`

Prefer framework hooks over duplicating the entire method when the hook expresses the change cleanly.

## get_queryset

Use for request/user/tenant/action-specific visibility and query optimization.

Do not evaluate a user-sensitive queryset at import/class-definition time.

## get_serializer_class

Useful when read/write/action contracts differ materially.

Do not split serializers automatically if one serializer remains clear and safe.

## perform_create/update

Good for small request-aware save parameters:

```python
def perform_create(self, serializer):
    serializer.save(owner=self.request.user)
```

Move multi-model workflows, external calls, or reusable transaction logic into an appropriate service/domain boundary.

## Custom actions

For each `@action`, check:

- detail vs collection
- method
- serializer
- permissions
- queryset/object lookup
- schema
- transaction behavior
- status code

## get_object

If custom code bypasses DRF's normal `get_object()`, remember object-permission checks may need to be called explicitly.

## Avoid giant overridden methods

If an override copies most of DRF's implementation just to change one step, look for a hook/mixin before maintaining a forked lifecycle.
