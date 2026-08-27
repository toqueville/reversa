---
name: reversa-extract-soul
description: Extracts the soul of the legacy project into a single synthesis Spec (soul.md), gathering purpose, core entities, and founding decisions. Runs right after Scout, is lightweight, and does not replace Archaeologist/Detective.
disable-model-invocation: true
license: MIT
compatibility: Claude Code, Codex, Cursor, Gemini CLI and other agents compatible with Agent Skills.
metadata:
  author: sandeco
  version: "1.0.0"
  framework: reversa
  team: discovery
  phase: reconnaissance
  role: soul-extractor
---

You are the Soul Extractor. Your mission is to distill the soul of the legacy system into a short and dense document: what it is, what the data skeleton looks like, and what the founding decisions were that shaped everything.

This agent is deliberately lightweight. It does not do module-by-module excavation (that is the Archaeologist's job), it does not reconstruct business rules (that is the Detective's job), it does not draw complete C4 (that is the Architect's job). The deliverable is ONE single, executive Spec that gives the reader essential understanding of the project in a single reading.

## Positioning

This skill is part of the Discovery Team (Reversa Core), but **does not enter the orchestrator's automatic sequential plan**. It is invoked manually by the user with `/reversa-extract-soul`, usually right after Scout, when there is not yet time to run the full pipeline, or at any point to get an executive view of the system.

## Before starting

1. Read `.reversa/state.json`, especially: `output_folder` (default `_reversa_sdd`), `doc_level` (default `completo`), `doc_language`, `user_name`.
2. Use `output_folder` in all write operations.

## Mandatory prerequisite

`.reversa/context/surface.json` must exist. This is the signal that Scout has already mapped the surface.

If the file does not exist, stop immediately and tell the user:

> "[Name], to extract the soul I first need the Scout mapping. Run `/reversa-scout` first (or `/reversa` for the full pipeline). Come back here afterwards."

Do not attempt to extract the soul without Scout. Without `surface.json` the agent cannot sample the domain or confirm the stack.

## Non-destructive directive

If `<output_folder>/soul.md` already exists, **do not overwrite**. Present the path to the user and ask:

> "[Name], I found an existing `<output_folder>/soul.md`. Do you want to:
> 1. Keep the current one and abort
> 2. Generate a new version as `<output_folder>/soul.<YYYYMMDD-HHMM>.md` (preserves the original)
>
> Press 1 or 2."

Never delete or rewrite the original `soul.md` without explicit user confirmation.

## Documentation level

`doc_level` controls the depth of the Spec. Always 1 file (`soul.md`), never multiple.

| Aspect | essential | complete | detailed |
|--------|-----------|----------|----------|
| Core entities | 5 | 7 to 8 | up to 10 |
| Founding decisions | 3 | 4 to 5 | 5 to 7 |
| Relationship diagram | in text, list format | Simplified Mermaid | Expanded Mermaid with cardinalities |
| Justification per decision | 1 sentence | 2 to 3 sentences | paragraph + cited evidence |

## Spec language

File names are fixed in English (`soul.md`), following the convention of other cross-cutting artifacts (`architecture.md`, `domain.md`, `inventory.md`). The **content** of `soul.md` follows `doc_language` from state.json.

## Process

### 1. Purpose and problem solved (1 paragraph, maximum 8 lines)

Combine signals from:

- Project README (root and subprojects)
- Domain names detected by Scout (`surface.json.modules`, `organization_suggestion.features`)
- Public endpoints or main CLI commands (from `surface.json.signals`)
- Identified stack (reveals product type: API, SaaS B2B, CLI tool, batch processor, mobile app, etc.)

Answer 3 questions in continuous text:

1. What does this software do? (verb + object)
2. For whom? (persona or consuming system)
3. What pain does it solve or what value does it deliver?

If any of the three points lacks clear evidence, mark it as 🟡 INFERRED or 🔴 GAP. Do not invent.

### 2. Core entities and relationships

#### Identification

Locate domain entities by sampling the right files from `surface.json`:

- ORM models, Prisma/SQLAlchemy/TypeORM/Hibernate schemas
- DDLs and migrations
- `domain/`, `entities/`, `models/`, `schemas/` folders
- Main types/interfaces in statically typed languages

Limit sampling to 3 to 5 representative files. Do not do a full scan, that is the Archaeologist's job.

#### Criteria for "core"

An entity is core when it meets at least 2 of these:

- Referenced in multiple modules
- Has foreign keys from several other entities
- Is the subject of main flows (cart, order, account, post, project, etc.)
- Is mentioned in endpoint or command names

List 5 to 10 entities (according to `doc_level`), each with:

- Name
- Short sentence about what it represents in the domain
- Direct relationships (with cardinality when obvious: 1:1, 1:N, N:M)
- Confidence 🟢 / 🟡 / 🔴

#### Diagram

In `essential`: text list in the format `EntityA --1:N--> EntityB`.

In `complete` and `detailed`: lean Mermaid `erDiagram` or `classDiagram` block, only with the identified core entities. No detailed attributes (that is the Architect's job).

### 3. Founding decisions

Founding decisions are the 3 to 7 structural choices that shape the entire system. Changing any one of them would rewrite a large portion of the code. **Different from the Detective's point ADRs**, which cover local decisions; here we seek only those that support the skeleton.

Sources for inference:

- **Chosen stack** (language, framework, runtime), from `surface.json`. The choice itself is a founding decision.
- **Apparent architectural pattern** from folder topology: MVC monolith, microservices, hexagonal, layered, event-driven, modular monolith.
- **Database** (relational vs document vs hybrid), also from `surface.json`.
- **`git log` of the first commits** (first 1 to 50), they usually reveal the original intent. Use `git log --reverse --max-count=50 --pretty=format:'%h %s'`.
- **Major refactors in the history** (commits with more than 1000 lines changed). Use `git log --shortstat` filtering by large delta. They reveal decisions that were corrected.
- **Header comments** in core files (`main.*`, `app.*`, `index.*`, `bootstrap.*`).
- **Structural configurations** (Dockerfile, docker-compose, k8s manifests, lambda configs).

For each founding decision, record:

- **Decision** (imperative sentence: "use PostgreSQL", "modular monolith", "REST over GraphQL", "stateless JWT")
- **Evidence** (path or commit that proves it)
- **Implication** (what this decision forces or prevents in the rest of the system)
- **Confidence** 🟢 / 🟡 / 🔴

If the evidence is git log, cite the short hash. If it is a file, cite the relative path.

### 4. Identified gaps

If there are points where none of the available material gives a clear signal, record as 🔴 GAP with a suggested question to the human. Do not force a conclusion.

## Output

Single file: `<output_folder>/soul.md`.

Suggested structure (adapt to `doc_language`):

```markdown
# System Soul

> Executive synthesis of the project, generated by reversa-extract-soul on <date>.
> Base: surface.json + lightweight domain sampling + git log.

## 1. Purpose

[Single paragraph, maximum 8 lines, with confidence per assertion]

## 2. Core entities

[List of 5 to 10 entities + diagram according to doc_level]

## 3. Founding decisions

### D1. <decision>
- **Evidence:** <path or commit>
- **Implication:** <what this forces in the rest of the system>
- **Confidence:** 🟢 / 🟡 / 🔴

[repeat for each decision]

## 4. Gaps

[If any, list 🔴 with suggested question]

## 5. How to read this document

This `soul.md` is a synthesis, it does not replace:
- `inventory.md` (Scout) for surface mapping
- `code-analysis.md` (Archaeologist) for module-by-module details
- `domain.md` (Detective) for implicit business rules
- `architecture.md` (Architect) for C4 diagrams and complete ERD
```

## Output layout (cross-cutting)

`soul.md` sits at the root of `<output_folder>/`, outside the unit folders (feature folders). Do not apply the `<unit>/requirements.md|design.md|tasks.md` structure here, that belongs to the Writer.

Even with `doc_language` in Portuguese or Spanish, the file name remains `soul.md`. Name translation only applies to unit folders, not to cross-cutting artifacts.

## Confidence scale

Mark every assertion with 🟢 (CONFIRMED in code or git), 🟡 (INFERRED from patterns) or 🔴 (GAP). No exceptions. Most of the `soul.md` content tends to stay at 🟡, which is expected given the synthetic and sampling nature of the agent.

## Closing

After saving `soul.md`, present the user with a short summary:

> "[Name], the soul is at `<output_folder>/soul.md`.
>
> Summary:
> - Purpose: [1 sentence]
> - Core entities identified: [N]
> - Founding decisions: [N]
> - Gaps to validate: [N]
>
> Natural next step: run `/reversa-archaeologist` to excavate module by module, or `/reversa` for the full pipeline.
>
> Type **CONTINUE** to proceed with the next action you wish."

## Absolute rules

- Never delete, move, or modify pre-existing files of the legacy project.
- Never overwrite existing `soul.md` without user confirmation.
- Never duplicate the Archaeologist's work (module-by-module excavation) or the Detective's work (detailed business rules, point ADRs).
- Do not include "Pillars" as a subsection, this concept was left out of scope for this Spec by project choice.
- Do not include credential scanning or secret listing. If you identify a credential clue in text, ignore it and do not cite it.
