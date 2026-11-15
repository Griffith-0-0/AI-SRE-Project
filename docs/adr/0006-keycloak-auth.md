# ADR-0006: AuthN/Z with Keycloak from the start

## Status
Accepted

## Context
The platform needs realistic auth (human RBAC + scoped agent identities) to demonstrate production-grade security. Skipping auth would simplify the MVP but weaken the security story.

## Decision
Run **Keycloak (OIDC)** from Phase 0; humans get RBAC; agents get scoped service identities.

## Alternatives considered
- Skip auth for MVP — faster, but no RBAC/agent-identity story.
- Auth0/Azure AD — managed, but a paid/cloud dependency.

## Consequences
+ Realistic, portfolio-grade auth.
+ Enables per-tool least privilege.
− One more service to run and configure; budget Phase-0 time for it.
