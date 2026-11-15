# ADR-0002: Multi-provider model routing (DeepSeek + OpenAI)

## Status
Accepted

## Context
Cost must be minimized with no fixed budget. Tasks differ sharply in quality/latency needs: high-volume triage vs rare hard reasoning/coding.

## Decision
Route by task tier through **LiteLLM**:
- **DeepSeek V4 Flash** — volume (triage, summarization, extraction).
- **OpenAI GPT-5.4 mini → GPT-5.4** — hard reasoning/coding/repair (escalate on failure).
- **Embeddings** — OpenAI `text-embedding-3-small` (DeepSeek has no embeddings endpoint).
- **Reranking** — local cross-encoder.

## Alternatives considered
- Single provider — simpler but either too costly or too weak.
- Local open models — free but weaker at repair.

## Consequences
+ Large cost savings (most tokens on cheap DeepSeek).
+ Cross-provider diversity for the critic.
− Two providers to manage; tier mapping must be centralized in LiteLLM.
