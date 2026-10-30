# Community / Private distribution

## Intended architecture

- **Private development repository**: full 34 skills, evaluation fixtures, history, internal documentation and release tooling.
- **Public Community repository**: only 7 selected skills, LICENSE, standalone installer and generated README; **no development Git history**.
- `publishing/community.json` is the release allowlist. Everything not explicitly allowed is excluded.

## Safe migration

1. **Before changing the current public repository**, create a new GitHub **private** repository, e.g. `CHLong678/DRF-Agent-Skills-Dev`, using GitHub Settings/UI. Keep it private.
2. Make a full mirror/backup of the current repository. Push all desired history to the private repository and verify the default branch, files and commit history are accessible privately.
3. Rotate any secrets ever committed and audit the public commit history. This step cannot erase downloaded copies.
4. From the private development checkout, run:

       python3 scripts/export-community.py --output /tmp/drf-agent-skills-community

5. Verify the export:

       python3 scripts/test_community_export.py

6. Review the output for secrets, company content, and protected files. Publish it as a **new independent public Git repository**, initialized with a fresh history, without carrying over `.git`:

       cd /tmp/drf-agent-skills-community
       git init
       git add .
       git commit -m "release: Community edition with 7 skills"

7. Publish to a new, empty public repository. Do **not** force-push to the existing Public repository while trying to hide past objects. If reusing an existing repo name, plan a controlled rename/replacement and understand that previously exposed history can remain available in copies/caches/forks.
8. Maintain the private repository as the primary working copy; export/review/publish Community only as a release action.

**Important:** Current `CHLong678/DRF-Agent-Skills` is already public with all 34 skills. Removing files or rewriting history does not revoke existing public copies or MIT permissions previously granted. This export is designed for clean *future* distributions, not retroactive secrecy.

## Community allowlist

- drf-core
- drf-serializers
- drf-views
- drf-orm-performance
- drf-testing
- drf-code-review
- drf-api-contracts

Never automatically upload the full development checkout to Public.
