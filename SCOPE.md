# Repository Scope

This repository exists to improve AI-agent correctness and effectiveness for production Django, DRF, Celery, PostgreSQL, Redis/cache, integrations, and adjacent backend engineering.

## A new skill/pattern belongs here when

At least one is true:

1. a real agent failure repeatedly occurs because the decision boundary is missing
2. the topic has a distinct routing boundary that existing skills cannot express cleanly
3. a recurring production backend failure mode needs its own reasoning/checklist
4. existing skills compose poorly because one shared concept lacks a source of truth
5. executable/model evals demonstrate a persistent gap

## A new skill does not belong here merely because

- the topic is interesting
- another repository has a skill for it
- a framework has a feature for it
- a one-paragraph reference can solve the problem
- it can be represented as a reference under an existing primary skill

## Prefer depth over skill count

Before creating a new skill, consider:

1. extend an existing reference
2. add a backend-pattern document
3. add a playbook
4. add a scenario/eval
5. only then add a new skill if routing ownership is genuinely distinct

## Failure-driven improvement

When an agent fails a Level-2 or Level-3 eval, improve the smallest layer that caused the failure:

- routing pointer
- inspect-first guidance
- completion criterion
- reference/playbook
- deterministic validator/test
- only create a new skill if the domain boundary is actually missing

## Primary authority

Community repositories provide patterns and agent-design ideas.

Exact version-sensitive behavior must be checked against official Django, DRF, Celery, PostgreSQL, protocol, provider, or library documentation.
