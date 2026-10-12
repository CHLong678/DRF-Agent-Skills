# Task

The PATCH endpoint incorrectly clears the existing note when the client omits the note field.

Fix partial-update semantics so an omitted field is preserved while an explicit null still clears it.

Keep the response shape unchanged and do not weaken or delete tests.
