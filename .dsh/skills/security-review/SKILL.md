---
name: security-review
description: Use when threat-modeling IncidentAI tools, prompts, the repair sandbox, or data flows — especially prompt-injection surfaces and anything that executes generated code.
---

# Security review

## Threat surfaces

- Telemetry, logs, and commit messages are untrusted input (prompt-injection).
- Generated code executes only in a sandbox (no egress, resource caps, unprivileged).
- Investigation tools are read-only by default; write tools require escalation.
- Secrets are never passed to agents.

## Steps

1. Identify the asset, the actor, and the attack path.
2. List mitigations per path, favoring least privilege and fail-closed defaults.
3. For any new tool, prompt, or repair change, return a risk list ordered by severity with concrete mitigations.
