# Agent instructions

This repository contains reusable DRF skills for Codex and Antigravity.

Compatibility baseline:

- Django >= 3.2
- Celery >= 5.0 when Celery is used
- DRF version compatible with the installed Django version

Before using version-sensitive APIs, inspect the actual Django, DRF, Celery, Python, database, and relevant third-party package versions.

Routing requirements:

- Read `ROUTING.md` when multiple skills overlap.
- Choose one primary skill; add secondary skills only when they materially affect correctness.
- Prefer the most specific skill once the problem domain is known.
- If the root cause is unknown, start with the diagnostic skill instead of guessing a fix.
- Respect each skill's `Routing contract`: Use when, Do not use, Inspect first, and Related skills.
- Use playbooks for common cross-cutting investigations rather than loading every related skill.

If versions are unknown, prefer Django 3.2 / Celery 5.0-compatible patterns. Newer features must be version-gated with a fallback.

When editing a skill:

- Keep the skill focused on Django REST Framework.
- Prefer production-safe rules over tutorial shortcuts.
- Distinguish correctness requirements from optional architectural preferences.
- Do not recommend an abstraction solely because it is fashionable.
- Preserve compatibility with Django >= 3.2 and Celery >= 5.0.
- Treat PostgreSQL transaction and locking behavior explicitly.
- Avoid rules that imply every query field needs an index.
- Avoid serializer validation side effects.
- Avoid unnecessary modern Python syntax unless the project runtime supports it.
- Add examples only when they clarify a non-obvious rule.
- Keep YAML front matter `name` and `description` precise because they drive skill discovery.

See `COMPATIBILITY.md` for version gates.
