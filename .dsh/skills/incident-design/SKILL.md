---
name: incident-design
description: Use when designing a reproducible incident for the Chaos Lab — the fault, ground truth, and scorers — or when modifying benchmark incidents.
---

# Incident design

## Steps

1. Define the fault: type, target service, and injection point. Make it deterministic (seedable, time-boxed, repeatable).
2. Record ground truth: the true root cause, the expected evidence, and a known-good fix.
3. Define scorers: root-cause match, evidence completeness, fix-verified, time-to-diagnosis, token cost.
4. Validate reproducibility (3 clean runs) before adding the incident to the corpus.
5. Assign a train / dev / hold-out split. Never edit the hold-out set after creation (prevents benchmark leakage).

## Boundaries

Isolated environments only. No production or external side effects.
