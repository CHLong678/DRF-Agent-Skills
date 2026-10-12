---
name: drf-files-object-storage
description: File upload/download and object-storage guidance for Django REST Framework. Use when handling large uploads, presigned URLs, multipart upload, streaming downloads, untrusted content, object metadata/finalization states, orphan cleanup, or S3-compatible storage integration.
---

# DRF Files and Object Storage

Read backend-patterns/file-object-storage.md for framework-neutral storage patterns.

## Avoid routing large bytes through web memory

For large uploads/downloads, prefer direct object-storage transfer, presigned URLs, or streaming where the security/product contract allows it.

Do not call .read() on an unbounded upload merely for convenience.

## Separate metadata and object state

Database metadata and object storage are different systems.

When correctness matters, model explicit states such as:

- pending
- uploaded
- verified
- ready
- failed

Do not assume DB row creation and object upload are atomic.

## Authorization

Authorize before issuing upload/download access.

Bind object ownership/key scope to tenant/user/resource context.

Do not expose predictable cross-tenant object keys as authorization.

## Untrusted uploads

Enforce size/content constraints and validate content according to risk.

User filename, extension, and Content-Type are claims, not proof.

## Cleanup and reconciliation

Define cleanup for abandoned multipart uploads, failed finalization, deleted resources, and orphaned objects.

Use reconciliation rather than assuming every request completes perfectly.

## Routing contract

### Use this skill when
- uploads/downloads, large files, presigned URLs, multipart upload, object storage, or file lifecycle/cleanup are primary

### Do not use this skill when
- the task is generic large database export; use drf-bulk-large-data first
- the task is only serializer FileField syntax with no storage/lifecycle concern
- the primary problem is background job contract; use drf-background-jobs-contracts

### Inspect first
- storage backend/provider
- maximum object/file size
- upload/download path
- authorization/tenant ownership
- DB metadata model
- finalization workflow
- scanning/validation requirements
- cleanup/reconciliation behavior

### Related skills
- drf-bulk-large-data, drf-auth-security, drf-reconciliation-repair, drf-background-jobs-contracts

## Deep reference

- references/upload-state-machine.md

## Completion criteria

Done when:
- upload/download and authorization flow are explicit
- DB metadata and object lifecycle states are consistent by design
- large/untrusted file constraints and finalization are defined
- orphan/failed-upload cleanup can be verified
