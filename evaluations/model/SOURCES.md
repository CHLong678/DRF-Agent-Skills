# Model Eval Harness Sources

The harness intentionally follows current official/headless CLI surfaces rather than inventing private integration behavior.

## OpenAI Codex

Official OpenAI guidance confirms that headless automation uses `codex exec`.

OpenAI's skill-eval guidance recommends `codex exec --json` for structured traces and `--output-schema` / output files for deterministic grading.

References:

- https://developers.openai.com/blog/eval-skills
- https://developers.openai.com/cookbook/examples/codex/build_iterative_repair_loops_with_codex
- https://openai.com/index/codex-now-generally-available/

## Google Antigravity CLI

Google's Antigravity CLI codelab documents:

- binary: `agy`
- non-interactive prompt mode: `agy -p "..."`
- optional model selection: `--model`
- CLI global skills directory: `~/.gemini/antigravity-cli/skills`

References:

- https://codelabs.developers.google.com/antigravity-cli-hands-on
- https://codelabs.developers.google.com/antigravity/how-to-create-agent-skills-for-antigravity-cli

## Safety

Routing evals are read-only. The harness does not enable Antigravity's dangerous permission-bypass mode and runs Codex with a read-only sandbox.
