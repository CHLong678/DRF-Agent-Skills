# Benchmark History

Real model runs produce volatile reports under `evaluations/results/`, which is gitignored.

Use `scripts/benchmark_history.py` to convert a selected Level-2 or Level-3 result into a compact, reviewable snapshot under this directory.

## Record

```bash
python scripts/benchmark_history.py record \
  --input evaluations/results/codex/<run>.json \
  --output evaluations/benchmarks/history/codex-routing-2026-10.json
```

Level-3 results work the same way.

## Compare

```bash
python scripts/benchmark_history.py compare \
  --baseline evaluations/benchmarks/history/before.json \
  --current evaluations/benchmarks/history/after.json
```

The comparison reports pass-rate/average-score changes, newly failing cases, recovered cases, and per-case score deltas when scores exist.

Only intentionally selected snapshots should be committed. Raw model traces remain ignored.
