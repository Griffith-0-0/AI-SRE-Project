---
name: planning-review
description: Use when reviewing or producing an architecture, design, plan, or architecture decision record (ADR) for IncidentAI — evaluate it against docs/decisions.md, flag scope creep and over-engineering, and recommend the simplest sufficient design.
---

# Planning review

## Purpose

Keep IncidentAI consistent with its agreed decisions and principles: modular monolith, open-source tooling + DeepSeek API, evaluation-first, and incremental complexity.

## Steps

1. Read `docs/decisions.md` (agreements) and `docs/open-questions.md` (pending).
2. Read `docs/report.md` for the canonical architecture.
3. For the design under review, check:
   - Does it contradict any agreed decision? If so, name the decision ID and propose updating it.
   - Does it add a new service, framework, or data store without a measured need? Challenge it.
   - Is there a simpler alternative satisfying the same requirement?
   - Does it respect the division of labor — deterministic algorithms > ML > LLM > orchestration?
4. Produce a trade-off analysis and a recommendation. Do not implement.

## Output

- Verdict: endorse / endorse with changes / reject.
- Per-issue findings tied to specific decision IDs.
- Recommended changes, ranked by impact.
