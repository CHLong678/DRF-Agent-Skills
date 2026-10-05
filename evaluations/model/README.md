# Model-based Routing Evaluations

This harness runs the routing cases against a real coding agent and scores the observed structured answer.

Supported adapters:

- OpenAI Codex CLI: `codex exec`
- Google Antigravity CLI: `agy -p`

## Preconditions

Install/authenticate the CLI you want to evaluate and install this repository's skills for that agent.

Codex:

```bash
./scripts/install-codex.sh
codex --version
```

Antigravity CLI:

```bash
agy --version
```

For Antigravity CLI global skill installation, set the CLI-specific directory explicitly when needed:

```bash
ANTIGRAVITY_SKILLS_DIR="$HOME/.gemini/antigravity-cli/skills" \
  ./scripts/install-antigravity.sh --global
```

The runner does not use a dangerous auto-write mode. Routing evals are read-only.

## Run

Codex:

```bash
python scripts/run_model_evals.py --provider codex
```

Antigravity:

```bash
python scripts/run_model_evals.py --provider antigravity
```

Run selected cases:

```bash
python scripts/run_model_evals.py \
  --provider codex \
  --case slow-api-unknown \
  --case race-lost-update
```

Choose a model:

```bash
python scripts/run_model_evals.py --provider antigravity --model "Gemini 3.7 Flash (High)"
```

Dry-run prompts without calling a model:

```bash
python scripts/run_model_evals.py --provider codex --dry-run
```

## Scoring

The deterministic grader checks:

- expected primary skill
- forbidden primary avoidance
- secondary skills are known/allowed
- inspect-first content exists
- verification content exists
- required reasoning tags, when defined

It writes both JSON and Markdown reports under `evaluations/results/<provider>/`.

This is a behavior eval, not a chain-of-thought eval. The harness scores concise decision artifacts exposed by the agent.
