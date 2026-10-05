# Agent instructions

This repository contains reusable DRF skills for Codex and Antigravity.

When editing a skill:

- Keep the skill focused on Django REST Framework.
- Prefer production-safe rules over tutorial shortcuts.
- Distinguish correctness requirements from optional architectural preferences.
- Do not recommend an abstraction solely because it is fashionable.
- Preserve compatibility with current Django/DRF versions where possible.
- Treat PostgreSQL transaction and locking behavior explicitly.
- Avoid rules that imply every query field needs an index.
- Avoid serializer validation side effects.
- Add examples only when they clarify a non-obvious rule.
- Keep YAML front matter `name` and `description` precise because they drive skill discovery.
