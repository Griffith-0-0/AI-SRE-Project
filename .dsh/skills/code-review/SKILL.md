---
name: code-review
description: Use when reviewing Python/TypeScript code, diffs, or pull requests for IncidentAI — check correctness, conventions, security, test coverage, and whether AI/agent behavior is measurable.
---

# Code review

## Steps

1. Identify the change's intent and its blast radius.
2. Review for: correctness, error handling, security (no secrets, no injection, least privilege), test coverage, and adherence to the project stack conventions.
3. For AI/agent code, verify: structured outputs, bounded tool calls, auditability, and that the behavior is measurable by the evaluation suite.
4. Return prioritized findings (blocking / important / nit) with file:line references. Do not rewrite code unless asked.

## Boundaries

Read and report only. The user decides what to change.
