# ADR-0004: Monorepo

## Status
Accepted

## Context
The platform, demo app, chaos experiments, docs, and skills are tightly coupled and must be read/edited together by the repair agent and eval harness.

## Decision
Single monorepo: `/platform`, `/apps/demo`, `/chaos`, `/docs`, `/.dsh/skills`.

## Alternatives considered
- Separate repos — cleaner separation, but painful cross-repo changes and submodules for a solo dev.

## Consequences
+ Atomic cross-component changes; one CI; easy agent access.
+ Simple for a solo developer.
− Larger single repo; split the demo app later only for external-monitoring realism.
