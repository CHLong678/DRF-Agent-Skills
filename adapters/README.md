# Multi-agent adapters

One canonical knowledge source: `skills/<skill-name>/SKILL.md`. Each target agent gets a copy of the **whole skill directory**, including `references/`, `examples/` and `agents/openai.yaml`.

## Supported install destinations

| Agent | Project | Global |
|---|---|---|
| Codex | `.codex/skills` | `~/.codex/skills` |
| Antigravity | `.agents/skills` | `~/.gemini/config/skills` |
| Claude Code | `.claude/skills` | `~/.claude/skills` |
| Cursor | `.cursor/skills` | `~/.cursor/skills` |
| GitHub Copilot | `.github/skills` | `~/.copilot/skills` |
| OpenCode | `.opencode/skills` | `~/.config/opencode/skills` |

The existing Antigravity CLI-specific installer `install-antigravity.sh --cli-global` remains available.

## Unified installer

From the source repository:

    python3 scripts/install-agents.py --agent claude-code --scope project --project /path/to/project
    python3 scripts/install-agents.py --agent cursor --scope global
    python3 scripts/install-agents.py --agent github-copilot --scope project --project /path/to/project
    python3 scripts/install-agents.py --agent opencode --scope global
    python3 scripts/install-agents.py --agent all --scope project --project /path/to/project --dry-run

Use `--skill drf-celery` (repeatable) to install only selected skills. Default is all skills.

### Ownership safety

Installer writes `.drf-agent-skills-install.json` into each installed directory. Existing unowned skill directories are **not overwritten** unless `--force` is specified. Dry-run changes nothing. Old `install-codex.sh` and `install-antigravity.sh` are kept for backward compatibility; those legacy scripts still overwrite matching directories.

### Invocation portability

`agents/openai.yaml` is Codex-oriented metadata; other agents may ignore it. `disable-model-invocation: true` and implicit invocation behavior are **not guaranteed cross-agent**. For sensitive/manual workflow skills (`drf-skill-router`, `backend-agent-retro`), verify the target agent's own invocation and permission behavior; do not assume Codex policy applies to Claude Code, Cursor, Copilot, or OpenCode.

Avoid installing the same skill into multiple directories searched by the same agent; precedence differs and duplicate discovery may be confusing. In particular, Cursor and OpenCode also discover some Claude/agent-compatible paths.

This integration tests installation paths and packaging. It does **not** assert real model invocation, correctness, or compatibility across every agent version.

## Official references

- Claude Code: https://code.claude.com/docs/en/skills
- Cursor: https://cursor.com/docs/skills
- GitHub Copilot: https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills
- OpenCode: https://opencode.ai/docs/skills
