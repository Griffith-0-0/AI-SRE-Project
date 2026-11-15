# Managing DeepSeek (DeepSeek Harness) for the IncidentAI Learning Project

> Goal: a development assistant that **guides and reviews by default, and implements only when explicitly asked.**
> Verified against this installation: the **standard** agent preset already mounts `@deepseek-ai/dsh-agent-instructions` (loads `AGENTS.md`) and `@deepseek-ai/dsh-skill-filesystem` (discovers skills under `.dsh/skills/`). **No profile change is required.**

## What is active now

| Mechanism | File(s) | Effect |
|-----------|---------|--------|
| **Context / rules** | `AGENTS.md` (repo root) | Auto-loaded as workspace instructions; encodes mentor mode. |
| **Skills** | `.dsh/skills/<name>/SKILL.md` | Discovered and loaded on demand; encode recurring procedures. |
| **Persona preset** | (not used) | The standard preset's persona remains; mentor behavior comes from `AGENTS.md`. |

## The mentor behavior

`AGENTS.md` sets the mentor contract: guide/review by default, implement only when explicitly asked; read `docs/decisions.md` before advising; evaluation-first; open-source tooling + DeepSeek API only. It applies to every session whose working directory is this project. A git repo is recommended so project-root discovery is robust (`git init`).

## Skills

Six skills live under `.dsh/skills/`:

| Skill | When it loads |
|-------|---------------|
| `planning-review` | Architecture / design / ADR reviews |
| `code-review` | Code / diff / PR reviews |
| `incident-design` | Designing Chaos Lab incidents |
| `evaluation` | AI evaluation methodology & metrics |
| `observability-sre` | OTel / Grafana / Prometheus / Loki / Tempo work |
| `security-review` | Threat-modeling tools / prompts / sandbox |

Each skill is a directory containing a `SKILL.md` with YAML frontmatter (`name` + `description`) followed by the procedure. They appear in the session skill catalog on the next model step after the files exist; editing a body is picked up on the next load (no restart).

## Optional: a separate "Mentor" persona preset (later)

The standard preset's persona is a generic coding-agent line. A dedicated preset with a mentor persona prefix is possible but would require a bundle that duplicates the full tool list and runs code in the host when installed. For this project the mentor behavior is already delivered by `AGENTS.md` with all standard tools retained, so a separate preset is not recommended unless you want a distinct, selectable agent mode. Ask explicitly if you want it.
