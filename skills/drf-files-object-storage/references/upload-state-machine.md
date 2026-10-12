# Upload State Machine

For non-trivial direct uploads, an explicit state machine can make cross-system behavior observable.

Example lifecycle:

pending -> uploaded -> verified -> ready

Failure paths may move to failed/expired.

A finalize endpoint should be idempotent when clients can retry it.

Do not mark an object ready merely because a client says upload succeeded; verify the storage object/metadata required by your contract.

Periodic reconciliation can detect stale pending rows and orphan objects.
