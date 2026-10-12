# Compatibility and Source Registry

`compatibility-sources.json` records version gates and source-review freshness for skills where stale external behavior could materially change recommendations.

This registry does **not** replace project inspection.

The target codebase's lockfiles, settings, runtime, database, and provider configuration remain the source of truth.

## Policy

- Official/framework/provider documentation is preferred for version-sensitive behavior.
- Community repositories may justify design patterns but not compatibility guarantees.
- A source review older than the configured freshness window should produce a validation failure or explicit refresh work.
- Not every skill needs a source entry. Add one when the skill depends on external/version-sensitive behavior.
