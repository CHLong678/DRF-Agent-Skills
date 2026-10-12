# Task

The process_charge service can be called more than once with the same idempotency key, which currently creates duplicate business effects.

Make duplicate logical execution produce exactly one PaymentEffect for a key.

Use durable database semantics. Do not solve this with process-local memory, and do not weaken or delete tests.
