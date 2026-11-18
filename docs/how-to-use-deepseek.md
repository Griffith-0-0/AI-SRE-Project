# How to use your DeepSeek mentor (short manual)

Two things help me help you. You barely have to think about either.

## 1. `AGENTS.md` — always on, nothing to do

This file is read automatically at the start of every session in this project.
It tells me to be a **mentor**: explain and review, and only write code when you explicitly ask.

- You never have to mention it.
- It's why I guide instead of coding ahead.

For development tasks, the mentor will suggest **A** (you lead to learn deeply), **B** (guided work together), or **C** (delegate routine work). The category can change as your skills grow. It does not authorize edits by itself: ask explicitly in the current turn whenever you want implementation. You can also ask for hints, a review, or a complete explanation at any time. The roadmap summarizes the learning focus for each phase; the daily backlog remains the task queue.

## 2. Skills — loaded when needed, two ways

Six skills live in `.dsh/skills/`. Each is a short "playbook" I follow for a recurring task.

**You don't need to remember names.** Just describe what you want in plain words, and I'll load the matching skill myself. Or name it explicitly if you prefer.

| Skill | Use it when you want to… | Example sentence |
|---|---|---|
| `planning-review` | check a design/plan against your decisions | "Review this design for scope creep." |
| `code-review` | get code/diff/PR feedback | "Review my diff for security and tests." |
| `incident-design` | design a reproducible Chaos Lab incident | "Help me design a DB-outage incident." |
| `evaluation` | set up or interpret AI evaluation | "How do I score my agent's accuracy?" |
| `observability-sre` | work on OTel / Grafana / logs / traces | "Help me configure the OTel Collector." |
| `security-review` | threat-model tools, prompts, sandbox | "Threat-model my repair sandbox." |

### Two ways to trigger a skill

- **Natural:** "Can you review this code?" → I load `code-review`.
- **Explicit:** "Use the `security-review` skill on this tool."

## Rules of thumb

1. **Talk normally.** The right skill loads automatically.
2. **You ask for code, I write code.** Otherwise I guide, review, and explain.
3. **Start a session by telling me the goal** — I'll read `docs/decisions.md` and the relevant doc myself.

## What you never need to do

- Paste any preamble or boilerplate.
- Enable/install anything.
- Remember skill names.
