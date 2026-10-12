# DRF Throttle Boundaries

DRF throttling is primarily an application policy mechanism, not automatically a precise distributed accounting system.

Review:

- cache backend
- key identity
- proxy/IP extraction
- multi-process behavior
- race/atomicity tolerance
- whether small over-admission is acceptable

Use ordinary throttling for abuse/load control where approximate distributed behavior is acceptable.

For strict entitlement, provider credits, or billable usage, use an explicit durable/atomic accounting design appropriate to that invariant.
