# Scenario: Large Object Upload Lifecycle

## Symptom

Clients upload multi-gigabyte files through Django workers, causing memory pressure and incomplete DB/object-storage state after interrupted uploads.

## Expected reasoning

1. Move large byte transfer away from unbounded web-process memory when possible.
2. Authorize and scope an application-controlled object key.
3. Use a bounded presigned/direct or multipart upload flow.
4. Model explicit pending/uploaded/verified/ready states when needed.
5. Treat client filename/type as untrusted input.
6. Make finalization retry-safe.
7. Reconcile abandoned uploads and orphan objects.

## Primary skill

`drf-files-object-storage`

## Secondary skills

`drf-auth-security` and `drf-reconciliation-repair`.
