---
name: reversa-agents-help
description: Explains with analogies what each Reversa agent does and when to use it. Activate with /reversa-agents-help.
license: MIT
compatibility: Claude Code, Codex, Cursor, Gemini CLI, and other agents compatible with Agent Skills.
metadata:
  author: sandeco
  version: "1.0.0"
  framework: reversa
  role: help
---

Present exactly the text below, without changes, without summarizing.

---

# Reversa Agents -- guide with analogies

Reversa is a team of specialists. Each agent does one thing only -- and does it well.

---

## Main menu

| What do you want to do? | Command | Team |
|---|---|---|
| Discover and document a legacy system | `/reversa` | Reversa Agents Core |
| Clarify the idea before any code | `/reversa-brainstorm` | Ideation Agents |
| Create a new project from an idea | `/reversa-new` | Code New Project Agents |
| Implement or evolve code from specs | `/reversa-forward` | Code Forward Agents |
| Plan the migration of a legacy system | `/reversa-migrate` | Migration Agents |
| Generate a visual mini-site of the documentation | `/reversa-docs` | Documentation Agents |
| Understand which agent to use | `/reversa-agents-help` | Agent guide |

The Pricing and Translators teams have specialized commands. Use `/reversa-pricing-profile`, `/reversa-pricing-size`, `/reversa-pricing-estimate`, or `/reversa-n8n` as needed.

---

## :bulb: Reversa Brainstorm, the table before the construction
**Command:** `/reversa-brainstorm`

Before the bricklayer raises a wall, someone sits at the table and asks what is wanted from the house: who is it for, what hurts about living as things are today, what the possible paths are, what could go wrong. Nobody draws blueprints at this table. Only what is worth building gets decided.

> Use Reversa Brainstorm when the idea is still raw, whether for a new project or a legacy system. It runs `Framer -> Explorer -> Challenger -> Arbiter -> Pre-Spec` and delivers the result to `/reversa-new` (greenfield) or `/reversa-requirements` (legacy).

**The five at the table:**

| Agent | Analogy | Command |
|---|---|---|
| **Framer** | The doctor who does not accept "I want drug X" and asks where it hurts | `/reversa-framer` |
| **Explorer** | The guide who shows all the trails, including the one of not climbing the mountain | `/reversa-explorer` |
| **Challenger** | The devil's advocate who has already seen this project fail before | `/reversa-challenger` |
| **Arbiter** | The judge who gives the verdict and owns what is lost with it, but you are the one who decides | `/reversa-arbiter` |
| **Pre-Spec** | The clerk who delivers the minimum for the construction to start, and nothing beyond | `/reversa-pre-spec` |

---

## :new: Reversa New -- the product founder
**Command:** `/reversa-new`

The founder starts with a still-raw idea, investigates the problem, understands who the product exists for, consolidates a PRD, and transforms everything into specs ready for implementation.

> Use Reversa New for greenfield projects. It runs `Ideator -> Researcher -> Drafter -> Spec SDD` and delivers the result to `/reversa-forward`.

---

## :musical_score: Reversa -- central orchestrator
**Command:** `/reversa`

An orchestra conductor does not play any instrument. He knows the entire score and says who enters when, in what order, at what tempo. Without him, each musician would play their part without connecting with the others.

> Use Reversa to start or resume the complete analysis. It handles the sequence for you.

---

## :world_map: Scout -- the real estate agent
**Command:** `/reversa-scout`

The agent does the first tour of the property. Does not open drawers, does not read documents, does not touch anything. Only maps: how many rooms, what neighborhood, what installations exist, what the general condition is.

> Use the Scout at the beginning. It generates the project inventory -- languages, frameworks, modules, dependencies -- without going into the code.

---

## :dna: Soul Extractor: the express biographer
**Command:** `/reversa-extract-soul`

The express biographer visits the character, reads the agent's notes (Scout), quickly flips through some family albums and the letter history (git log), and produces a one-page biography: who they are, what they do, and the founding decisions that shaped their entire life. It is not the complete story, it is the distilled soul.

> Use the Soul Extractor right after the Scout, when you want an executive synthesis of the system (purpose, core entities, and founding decisions) in a single Spec, without waiting for the entire pipeline. It does not replace Archaeologist or Detective.

---

## :pick: Archaeologist -- the excavator
**Command:** `/reversa-archaeologist`

The archaeologist excavates the terrain patiently, layer by layer. Catalogs each artifact found: size, material, location, shape. He does not interpret the civilization, only describes with precision what is there.

> Use the Archaeologist to analyze the code module by module. It extracts functions, algorithms, data structures, and control flows. **Runs one module per session** to save tokens.

---

## :mag: Detective -- the Sherlock Holmes
**Command:** `/reversa-detective`

Sherlock Holmes arrives after the archaeologist. Looks at the cataloged artifacts and asks: *"But why is this here? Who placed it? What does this reveal about who lived here?"* He does not excavate. He interprets.

> Use the Detective after the Archaeologist. It extracts implicit business rules, reads the git history as a diary, and reconstructs decisions that nobody documented.

---

## :triangular_ruler: Architect -- the cartographer
**Command:** `/reversa-architect`

The cartographer visits a territory and produces formal maps: floor plan, elevation map, structural plan. Someone who never set foot there can understand everything by looking at the maps.

> Use the Architect after the Detective. It synthesizes everything into C4 diagrams, complete ERD, and integration map.

---

## :memo: Writer -- the notary
**Command:** `/reversa-writer`

The notary transforms what was discovered into formal, precise, and traceable contracts. Each clause has a declared confidence level. The document serves as a contract: an AI agent can reimplement the system from it.

> Use the Writer after the Architect. It generates the SDD specs, OpenAPI, and user stories with code traceability.

---

## :balance_scale: Reviewer -- the spec reviewer
**Command:** `/reversa-reviewer`

The Reviewer takes the Writer's contracts and tries to poke holes: *"This is a contradiction. This point has no proof. This rule breaks if the user does X."* He does not want to destroy, he wants to ensure that what stood is solid.

> Use the Reviewer after the Writer. It critically reviews the specs, reclassifies confidence, and raises questions for human validation.

---

## :framed_picture: Visor -- the forensic illustrator
**Command:** `/reversa-visor`

The forensic illustrator works only with images. Receives screenshots of the system and faithfully reconstructs the interface: screens, forms, navigation flows. Does not need the system running -- just the photos.

> Use the Visor when you have screenshots available. It documents the UI without needing access to the system.

---

## :file_cabinet: Data Master -- the geologist
**Command:** `/reversa-data-master`

The geologist maps the subsoil -- the layer nobody sees but that supports everything. Tables, relationships, constraints, triggers, procedures. The invisible foundation on which the application is built.

> Use the Data Master when there is DDL, migrations, or ORM models available. It documents the database completely.

---

## :art: Design System -- the stylist
**Command:** `/reversa-design-system`

The stylist catalogs the wardrobe: color palette, typography, spacing, design tokens. The "fashion rules" that govern the system's appearance -- what can and cannot be combined.

> Use the Design System when there are CSS files, themes, or UI screenshots. It extracts the project's visual tokens.

---

## Recommended sequence

```
Legacy project: /reversa -> discovery and specifications
New project:    /reversa-new -> PRD and specs -> /reversa-forward
Migration:      /reversa -> /reversa-migrate -> /reversa-forward

Manual legacy pipeline:
Scout -> Archaeologist (N sessions) -> Detective -> Architect -> Writer -> Reviewer

Optional at any phase:
Soul Extractor . Visor . Data Master . Design System . Reversa Docs
```
