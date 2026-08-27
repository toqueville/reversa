# Reversa

> Reverse Engineering Framework installed in this project.

## How to use

Use the appropriate flow in the chat:

- `/reversa` — discover and document an existing system
- `/reversa-new` — create PRD and specs for a new project
- `/reversa-forward` — implement or evolve code from specs
- `/reversa-migrate` — plan the migration of a legacy system
- `/reversa-docs` — generate the visual documentation mini-site
- `/reversa-agents-help` — browse the complete agent catalog

## Activation behavior

When the user types `/reversa` or the word `reversa` alone in a message:

1. Activate the `reversa` skill available at `.claude/skills/reversa/SKILL.md`
2. If not found in `.claude/skills/`, try `.agents/skills/reversa/SKILL.md`
3. Read the SKILL.md in full and follow the Reversa instructions exactly

## Non-negotiable rule

{{REVERSA_POLICY}}
