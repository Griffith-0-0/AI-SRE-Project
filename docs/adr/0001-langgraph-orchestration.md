# ADR-0001: Use LangGraph for agent orchestration

## Status
Accepted

## Context
Incident investigation is a stateful, multi-step workflow (evidence → hypothesis → verify → report) with retries, conditional routing, and human-in-the-loop gates. We need checkpointed state and tool calling.

## Decision
Use **LangGraph** for the agent orchestrator.

## Alternatives considered
- OpenAI Agents SDK — simpler, but less stateful/graph control.
- PydanticAI — type-safe, but less suited to complex state machines.
- AutoGen/AG2/CrewAI — fragmented or role-play oriented.

## Consequences
+ Checkpointed state, retries, human gates, MCP support.
+ State can be persisted and replayed.
− Framework-specific learning; keep the graph thin and logic in plain Python.
