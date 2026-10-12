# Task

The create_order service dispatches an external/background side effect before the database transaction is safely committed.

Fix the transaction boundary so dispatch happens only after a successful commit and never after rollback.

Do not weaken or delete tests.
