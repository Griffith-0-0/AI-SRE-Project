# ADR-0003: Repair target is L1 (propose patch, human applies)

## Status
Accepted

## Context
Full autonomous repair (L2/L3) is research-grade: it needs a sandbox, test loop, and PR automation (~6–9 weeks). The project's value can be demonstrated without autonomous execution.

## Decision
**L1**: the AI proposes a structured patch (diff); the human applies it; the eval harness verifies (apply + tests) deterministically. **No sandbox** (the AI does not execute code).

## Alternatives considered
- L2 (sandbox + tests + PR) — impressive but heavy and uncertain.
- L0 (diagnose only) — too little value.

## Consequences
+ Simpler, safer, cheaper (~2–4 weeks).
+ Still measures repair quality honestly.
− Not autonomous; the human is in the loop.
− L2 sandbox remains a later option.
