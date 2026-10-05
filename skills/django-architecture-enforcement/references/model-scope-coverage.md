# Model Scope Coverage

Use this reference when tenant/org/user isolation is a critical invariant.

## Registry-driven coverage

Instead of maintaining a permanent handwritten list, inspect Django's app registry.

Conceptually:

```text
for each non-abstract model:
    detect tenant/org/user ownership
    classify expected scope
    verify enforcement exists
```

Possible enforcement mechanisms:

- approved scoped manager/base class
- explicit exemption for global models
- static-analysis coverage
- parent-FK scoping strategy

## Why this helps

When a new tenant-owned model is added, CI can detect that it lacks protection.

## Legitimate exemptions

Examples:

- global configuration/catalog models
- identity/root tenant models
- junction tables scoped through an enforced parent
- migration/system infrastructure

## Generated baseline

For a legacy system:

```text
current violations
      ↓
generated baseline
      ↓
new violations fail
      ↓
migrated items disappear
```

Prefer regeneration from live model metadata over manually adding names to the baseline.
