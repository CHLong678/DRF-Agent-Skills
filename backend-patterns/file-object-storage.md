# File and Object Storage Patterns

## Goal

Handle large/untrusted files without routing every byte through application memory or treating object storage as a trusted database.

## Direct upload

For large files, clients can upload directly to object storage using a bounded presigned upload contract.

The application should control:

- object/key scope
- content/size limits where supported
- expiry
- tenant/owner association
- finalization workflow

## Multipart upload

Use multipart upload for large objects when supported.

Define abort/cleanup for abandoned uploads.

## Metadata vs object

Database metadata and object storage are separate systems.

Do not assume creating DB metadata and uploading the object are atomic.

Use explicit states such as pending/uploaded/verified/ready when needed.

## Download

Prefer streaming or presigned download rather than loading the whole object into process memory.

Authorization must happen before issuing access.

## Untrusted content

Treat user uploads as untrusted.

Consider:

- MIME/content validation
- filename/path normalization
- size limits
- malware/content scanning when risk requires it
- image/document parsing risk
- archive bombs
- public/private ACL

## Object keys

Do not rely on user-provided filenames as globally unique or safe object keys.

Use opaque application-controlled keys and store display names separately.

## Cleanup

Define cleanup for:

- abandoned multipart uploads
- orphan objects
- deleted DB records
- failed finalization
- expired temporary files

A reconciliation job is often necessary.

## Verification

Test authorization, oversize files, interrupted uploads, duplicate finalization, orphan cleanup, and memory usage.
