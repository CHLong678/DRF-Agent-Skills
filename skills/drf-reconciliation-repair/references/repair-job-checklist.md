# Repair Job Checklist

Before mutation:

- define authoritative state
- estimate candidate count
- provide dry-run/report
- define batch size
- define resume/checkpoint
- define duplicate safety
- define interaction with live writes
- define external side-effect policy
- define audit log
- define verification query/metric

Prefer a bounded management command or worker job over an unbounded one-off shell loop for large production repairs.
