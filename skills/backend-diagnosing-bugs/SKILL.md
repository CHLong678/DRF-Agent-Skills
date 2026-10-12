---
name: backend-diagnosing-bugs
description: Diagnose hard Django/DRF/Celery/PostgreSQL/backend bugs with a tight feedback loop before proposing fixes. Use when a bug is intermittent, unclear, regression-like, performance-related, or has resisted a first-pass explanation.
---

# Backend Diagnosing Bugs

The leading word is **tight**: build the smallest fast feedback loop that already goes red on this bug.

## Phase 1 — Build a red-capable feedback loop

Before theorising, get one reproducible command/harness that demonstrates the failure.

Examples:

- focused Django/DRF test
- APIClient/curl replay
- `assertNumQueries()`
- `TransactionTestCase` concurrency harness
- Celery task invocation/replay
- webhook payload replay
- management command fixture
- EXPLAIN/measurement script
- provider response fixture
- human-in-the-loop script when the bug requires UI/manual state

If you cannot reproduce the exact failure yet, keep working on the loop.

## Phase 2 — Minimise

Remove unrelated data, settings, callers, and steps until the smallest failing case remains.

Preserve the failure while shrinking the search surface.

## Phase 3 — Form falsifiable hypotheses

Generate a small set of concrete hypotheses.

Use the form:

```text
If X is the cause, changing or instrumenting Y should change/observe Z.
```

Avoid vague statements such as "Redis may be slow".

## Phase 4 — Instrument and discriminate

Collect evidence that separates the hypotheses.

Examples:

- query count / SQL
- transaction boundaries
- lock wait
- task delivery/retry state
- cache hit/miss
- external latency/status
- process/worker saturation
- version/config difference

Prefer one discriminating measurement over broad logging.

## Phase 5 — Fix the root cause

Apply the smallest change that closes the demonstrated failure.

Do not solve the symptom by masking errors, increasing timeouts/concurrency blindly, or weakening the repro.

## Phase 6 — Regression and original repro

Turn the failure into a regression test or deterministic check when practical.

Run both:

- the new regression
- the original red-capable feedback loop

## Phase 7 — Cleanup

Remove temporary instrumentation and debugging-only code.

Preserve useful deterministic checks.

## Routing contract

### Use this skill when
- the root cause is unknown
- a bug is intermittent or regression-like
- a performance failure has multiple plausible sources
- previous speculative fixes failed
- the problem crosses multiple backend layers

### Do not use this skill when
- the root cause is already established and a domain skill clearly owns the fix
- the user only wants an explanation of known behavior

### Inspect first
- exact failing behavior
- shortest reproducible path
- versions/configuration
- recent changes when regression is plausible
- logs/metrics already available

### Related skills
- route to the relevant domain skill only after the feedback loop identifies the owning layer

## Completion criteria

Done when:

- one command/harness reproducibly demonstrates the original failure
- the failing case has been minimised enough to identify the relevant boundary
- the chosen root cause is supported by discriminating evidence
- the fix makes the original feedback loop green
- a regression test/check exists when practical
- temporary debugging instrumentation is removed
