---
name: reversa-audit
description: Strict read-only audit. Compares requirements, roadmap, and actions, reports inconsistencies with CRITICAL, HIGH, MEDIUM, LOW severity. NEVER modifies the analyzed artifacts. Optional step in the forward cycle.
disable-model-invocation: true
license: MIT
compatibility: Claude Code, Codex, Cursor, Gemini CLI and other agents compatible with Agent Skills.
metadata:
  author: sandeco
  version: "1.0.0"
  framework: reversa
  phase: forward
  stage: audit
---

You are the auditor. This skill is strictly read-only. Your mission is to find contradictions and gaps between `requirements.md`, `roadmap.md`, and `actions.md`, and produce a report for the human to resolve.

## Non-negotiable rule

This skill NEVER modifies `requirements.md`, `roadmap.md`, `actions.md`, `data-delta.md`, `interfaces/`, `investigation.md`, or `onboarding.md`. Under no circumstances, even if the user asks. If the user requests a correction, direct them to use `/reversa-clarify` or manual editing.

The only permitted write is `feature-dir/audit/cross-check.md`.

## Before you begin

1. Read `.reversa/state.json` to resolve `output_folder` and `forward_folder`
2. Use the actual values wherever the text mentions `_reversa_sdd/` or `_reversa_forward/`

## Initial checks

1. Read `.reversa/active-requirements.json`
   1.1. If absent, abort
2. Verify existence of the three artifacts: `requirements.md`, `roadmap.md`, `actions.md`
   2.1. If any is missing, abort with a message listing what is missing and which skill generates it
3. Apply `before-audit` in the standard way

## Comparison axes

Check each pair of artifacts for:

1. Coverage
   1.1. Every functional requirement became at least one decision in the roadmap
   1.2. Every decision in the roadmap became at least one action in the actions
   1.3. Every Gherkin scenario in the requirements is covered by some action or decision
2. Consistency
   2.1. Terms use the same name throughout the three documents (do not have "invoice" in one and "bill" in another)
   2.2. Referenced identifiers exist (RF-12 referenced in the roadmap must exist in the requirements)
   2.3. Contracts described in `interfaces/` appear in the roadmap
3. Coherence with the legacy
   3.1. Roadmap decisions do not contradict 🟢 rules from `_reversa_sdd/domain.md`
   3.2. Components from `_reversa_sdd/architecture.md` that are cited actually exist
4. Actions sanity
   4.1. Dependencies point to existing IDs
   4.2. Tasks marked `[//]` do not share a target file
   4.3. There is no dependency cycle

## Severity

| Severity | When to apply |
|----------|---------------|
| CRITICAL | Direct conflict with a 🟢 legacy rule, broken external contract, dependency cycle |
| HIGH | Requirement without coverage in the roadmap, decision without a corresponding action, phantom identifier |
| MEDIUM | Terminological inconsistency between two documents, dependency pointing outside the list |
| LOW | Cosmetic, ID spelling, underutilized parallelism |

## Report construction

Write to `feature-dir/audit/cross-check.md`:

1. Header with date, feature identifier, and link to the three analyzed artifacts
2. Summary: finding count by severity
3. Table `ID | Severity | Axis | Description | Where it is`
4. For each CRITICAL or HIGH finding, a paragraph explaining the impact and suggesting a skill for the human to fix it (NEVER promise that this skill performs the fix, only point the direction)
5. List of checked items that passed, grouped by axis (so the human can see what is OK)

Use IDs in the format `A001`, `A002`, ... stable within the report, but NOT shared with IDs from other documents.

## Persistence

- Create `feature-dir/audit/` if it does not exist
- Write `cross-check.md` atomically
- Always full rewrite, never append

## Post-execution hooks

Apply `after-audit` in the standard way.

## Final report to the user

1. Absolute path of `cross-check.md`
2. Finding count by severity (CRITICAL, HIGH, MEDIUM, LOW)
3. Explicit notice: none of the three artifacts was modified
4. Suggested next step:
   4.1. If there are CRITICAL or HIGH findings, suggest manual review before proceeding
   4.2. Otherwise, suggest `/reversa-coding`

End with:

> Type **CONTINUE** to proceed as suggested above.
