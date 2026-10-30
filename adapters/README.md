# Unified multi-agent installation

All six coding agents install from the same canonical `skills/` tree using **one command**: `python3 scripts/install-agents.py`.

## Supported directories

| Agent | Project | Global |
|---|---|---|
| Codex | `.codex/skills` | `~/.codex/skills` |
| Antigravity | `.agents/skills` | `~/.gemini/config/skills` |
| Claude Code | `.claude/skills` | `~/.claude/skills` |
| Cursor | `.cursor/skills` | `~/.cursor/skills` |
| GitHub Copilot | `.github/skills` | `~/.copilot/skills` |
| OpenCode | `.opencode/skills` | `~/.config/opencode/skills` |

Antigravity CLI additionally supports `--agent antigravity --scope cli-global`, targeting `~/.gemini/antigravity-cli/skills`.

## Usage

```bash
# Preview before writing
python3 scripts/install-agents.py --agent all --scope project --project /path/to/project --dry-run

# All skills into selected agent's global directory
python3 scripts/install-agents.py --agent codex --scope global
python3 scripts/install-agents.py --agent cursor --scope global

# All skills to six agents, project-scoped
python3 scripts/install-agents.py --agent all --scope project --project /path/to/project

# Only selected skills
python3 scripts/install-agents.py --agent claude-code --scope project --project /path/to/project --skill drf-celery
```

## Migration from legacy scripts

The separate `install-codex.sh` and `install-antigravity.sh` scripts have been retired. Replace them with:

- old `install-codex.sh` -> `python3 scripts/install-agents.py --agent codex --scope global`
- old `install-antigravity.sh --project DIR` -> `python3 scripts/install-agents.py --agent antigravity --scope project --project DIR`
- old `install-antigravity.sh --global` -> `python3 scripts/install-agents.py --agent antigravity --scope global`
- old `install-antigravity.sh --cli-global` -> `python3 scripts/install-agents.py --agent antigravity --scope cli-global`

The unified installer refuses to overwrite pre-existing unowned directories by default. Installations made with legacy scripts may not contain the new management marker; inspect the target and use `--force` only if intentionally replacing it. The installer does not delete legacy directories or search for duplicate skill installations.

## Portability notes

Each agent receives `SKILL.md`, references, examples and agent metadata from the same source. `agents/openai.yaml` is Codex-oriented; other agents may ignore it. Invocation settings such as `disable-model-invocation` are not guaranteed equivalent on every agent. Test actual discovery and invocation in your target agent independently.

Do not install overlapping copies into multiple directories the same agent searches without checking precedence.

## Official documentation

- Claude Code: https://code.claude.com/docs/en/skills
- Cursor: https://cursor.com/docs/skills
- GitHub Copilot: https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills
- OpenCode: https://opencode.ai/docs/skills
