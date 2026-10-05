# Import Boundary Enforcement

Use this reference when a Django codebase has explicit layers/modules that should not bypass each other.

Example architecture:

```text
api/presentation -> services -> domain/models
```

A boundary check can prevent API code from importing deep internal implementation modules directly.

Do not assume this exact layering is universal. First identify the architecture the project actually wants.

Tools such as import-linter can express forbidden dependency directions in CI.

Architecture rules are most valuable when they protect transaction ownership, domain reuse, team ownership, or dependency direction.
