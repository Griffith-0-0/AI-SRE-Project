---
name: evaluation
description: Use when defining or applying IncidentAI's AI evaluation methodology — metrics, benchmark construction, hold-out discipline, and interpretation of agent results.
---

# Evaluation

## Metrics

root-cause accuracy · hallucination rate · patch pass rate · time-to-diagnosis · token cost · latency.

## Steps

1. Ensure the change is measurable against the labeled incident corpus.
2. Enforce hold-out discipline: never tune against the hidden set.
3. Interpret results with variance in mind (multiple runs, confidence intervals); avoid single-run conclusions.
4. Flag cherry-picked demos and benchmark leakage.
5. Report what changed (prompt / tool / architecture) and its measured effect.

## Rule

Reproducible numbers only. No subjective demonstrations.
