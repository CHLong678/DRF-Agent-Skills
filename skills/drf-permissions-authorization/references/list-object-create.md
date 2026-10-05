# DRF List, Object, and Create Authorization

## List

Object permission methods are not automatically evaluated for every list row.

Therefore:

```text
permission class alone
!=
safe list endpoint
```

Use queryset scoping.

## Retrieve/update/delete

If using DRF generic retrieval, object checks normally happen through `get_object()`.

If bypassing it, call `check_object_permissions()` manually.

## Create

There is no existing object to pass to `has_object_permission()`.

Examples of creation rules:

- caller may create only inside their tenant
- caller may assign only themselves as owner
- only admins may set privileged status
- referenced parent must belong to caller scope

These belong in the appropriate view/serializer/service boundary.

## Bulk endpoints

Object permission loops can become both slow and incomplete.

Prefer a queryset scoped to authorized objects, then validate that the requested ID set and authorized set match according to the contract.

Do not partially mutate unauthorized objects accidentally.
