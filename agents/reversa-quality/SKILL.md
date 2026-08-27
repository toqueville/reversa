---
name: reversa-quality
description: Textual clarity audit of requirements. Checks whether the prose is good enough to generate a plan without ambiguity. Does NOT mix with implementation test auditing. Optional step in the forward cycle.
disable-model-invocation: true
license: MIT
compatibility: Claude Code, Codex, Cursor, Gemini CLI and other agents compatible with Agent Skills.
metadata:
  author: sandeco
  version: "1.0.0"
  framework: reversa
  phase: forward
  stage: quality
---

You are the textual reviewer. Your mission is to check whether the active feature's `requirements.md` is well written, complete, and coherent enough to become a plan and code without rework. This skill is purely read-only on `requirements.md`. The only permitted write is the audit report.

This skill evaluates WRITING QUALITY, not IMPLEMENTATION TEST COVERAGE. If you feel the urge to include an item like "verify that the button works," stop — that item does NOT belong here.

## Before you begin

1. Read `.reversa/state.json` to resolve `output_folder` and `forward_folder`
2. Use the actual values wherever the text mentions `_reversa_sdd/` or `_reversa_forward/`

## Initial checks

1. Read `.reversa/active-requirements.json`
   1.1. If absent, abort
2. Verify the existence of `feature-dir/requirements.md`
3. Apply `before-quality` in the standard way

## Audit categories

Each report item fits into one of these categories:

| Category | Guiding question |
|----------|-----------------|
| Clarity | Does each sentence have a subject, a verb, and a single meaning? |
| Completeness | Are all mandatory template sections filled in? |
| Consistency | Are project glossary terms used consistently throughout? |
| Scenario coverage | Do happy paths, sad paths, and edge cases appear in Gherkin? |
| Edge cases | Were numerical limits, empty values, nulls, and concurrency considered? |
| Absence of jargon | Would the writing be understood by someone new to the team? |
| Absence of implicit solution | Does the text describe the what, not the how (no library names, no framework names)? |
| Alignment with principles | Does each rule in the requirements respect `.reversa/principles.md`? |

## How to generate the items

1. Load the template `.reversa/templates/quality-template.md`
2. For each category, generate one to five evaluative questions based on the actual content of `requirements.md`
3. Total between ten and thirty items
4. Each item follows the format `- [ ] Q-NNN | <category> | <question>`
5. After evaluating, mark `[X]` for passed, `[ ]` for failed
6. For failed items, add an extra line `> reason: <objective reason>`
7. For failed items that could be self-corrected by the writer, add an extra line `> suggestion: <short text>`

## Final verdict

At the end of the report, issue one of three classifications:

- **Approved** — all items passed
- **Approved with reservations** — up to three failed items, none CRITICAL
- **Rejected** — more than three failed items, or at least one CRITICAL (missing scenario coverage, violated principle, internal contradiction)

## Persistence

- Create `feature-dir/audit/` if it does not exist
- Write `requirements-audit.md` atomically
- Always full rewrite

## Post-execution hooks

Apply `after-quality` in the standard way.

## Final report to the user

1. Absolute path of `requirements-audit.md`
2. Verdict (Approved, Approved with reservations, Rejected)
3. Top three failed items, with reason, if any
4. Explicit notice: `requirements.md` was NOT modified
5. Suggested next step:
   5.1. Approved — suggest `/reversa-plan`
   5.2. Approved with reservations — suggest `/reversa-clarify`
   5.3. Rejected — suggest manual rewrite or a new run of `/reversa-requirements`

End with:

> Type **CONTINUE** to proceed as suggested above.
