---
name: reversa-coding
description: 'Executes actions.md into code: marks checkboxes [X], writes progress.jsonl, and generates legacy-impact.md and regression-watch.md. Works anchored on legacy (`_reversa_sdd/`) or greenfield (`/reversa-new`). Last step of the forward cycle.'
disable-model-invocation: true
license: MIT
compatibility: Claude Code, Codex, Cursor, Gemini CLI and other agents compatible with Agent Skills.
metadata:
  author: sandeco
  version: "1.0.0"
  framework: reversa
  phase: forward
  stage: coding
---

You are the executor. Your mission is to transform `actions.md` into real code, phase by phase, respecting parallelism and dependencies. When done, leave two trails for future auditing: `legacy-impact.md` (what was touched in the legacy) and `regression-watch.md` (what must remain true in future extractions).

## Before starting

1. Read `.reversa/state.json` to resolve `output_folder` and `forward_folder`
2. Use the actual values where this text mentions `_reversa_sdd/` or `_reversa_forward/`

## Context anchor: legacy or greenfield

This skill **REQUIRES** a context anchor in `_reversa_sdd/`, otherwise the two central artifacts (`legacy-impact.md` and `regression-watch.md`) lose their value and the forward cycle becomes just another generic framework. Two anchors are valid:

1. **Legacy:** `_reversa_sdd/` contains `architecture.md` AND `domain.md` (Discovery Team extraction via `/reversa`). Classic behavior.
2. **Greenfield:** `_reversa_sdd/` contains `prd.md` AND at least one spec in `_reversa_sdd/sdd/` (`/reversa-new` artifacts). New project is a valid case, the pipeline does not block due to absence of extraction. The skill artifacts adapt as described in the generation sections.

If both anchors exist (project that ran `/reversa` and `/reversa-new`), use the legacy anchor as primary and the SDD specs as complement.

Verification remains strict when NO anchor exists: the skill aborts with a clear message, does NOT offer an option to proceed anyway, does NOT write anything to disk.

## Initial verifications

1. Read `.reversa/active-requirements.json`
   1.1. If absent, abort with a message pointing to `/reversa-requirements`
2. Verify the existence of `feature-dir/actions.md`
   2.1. If absent, abort with a message pointing to `/reversa-to-do`
3. Verify the context anchor:
   3.1. **Legacy anchor:** `_reversa_sdd/` exists AND contains `architecture.md` AND `domain.md`. If satisfied, internally register the scenario as **legacy** and proceed to step 4.
   3.2. **Greenfield anchor:** `_reversa_sdd/` exists AND contains `prd.md` AND at least one `.md` file in `_reversa_sdd/sdd/`. If satisfied (and the legacy one is not), register the scenario as **greenfield**, inform the user ("No legacy extraction found, I will anchor on `/reversa-new` artifacts: `prd.md` and SDD specs.") and proceed to step 4.
   3.3. If NEITHER anchor is satisfied, abort with the message:

       > 🛑 `/reversa-coding` requires a context anchor in `_reversa_sdd/` and I found none:
       >
       > - **Legacy:** `architecture.md` + `domain.md` (generate with `/reversa`)
       > - **Greenfield:** `prd.md` + specs in `sdd/` (generate with `/reversa-new`)
       >
       > Without this context, `legacy-impact.md` and `regression-watch.md` would lack an anchor and the forward cycle would lose its differentiator. Run one of the two pipelines and come back here.

   3.4. In the case of step 3.3, do NOT create `legacy-impact.md`, do NOT create `regression-watch.md`, do NOT touch `actions.md`, do NOT write `progress.jsonl`. Just report and finish.

4. Apply `before-coding` in the standard way

## Round scope

1. If the free argument indicates a phase or ID range (e.g., "only Core", "T001-T005"), restrict execution to that scope
2. Otherwise, execute in order all `[ ]` actions not yet completed

## Execution loop per phase

For each phase, in order Preparation, Tests, Core, Integration, Polish:

1. Select all actions in the phase with status `[ ]`
2. Calculate the independent set (actions with no open dependency)
3. For the independent set, identify the subset marked `[//]`
   3.1. Execute this subset thinking of each action as a coherent block, but report separately
4. Execute the remaining actions in the set sequentially
5. After each action:
   5.1. Update `feature-dir/actions.md` changing `[ ]` to `[X]`
   5.2. Write a line in `feature-dir/progress.jsonl` with ISO 8601 timestamp, action ID, final status, files touched
6. If an action fails:
   6.1. Keep `[ ]` in actions
   6.2. Record `status: failed` in progress
   6.3. Stop the phase and report to the user

## Generating legacy-impact.md

After executing (even if partially):

**Greenfield scenario:** there is no legacy to impact. Generate the file anyway, with adaptations: map each created file to the corresponding component from the specs in `_reversa_sdd/sdd/` (instead of `architecture.md`), use the impact type `new-component` for everything, and record in the header: "Greenfield feature, no pre-existing legacy. Anchor: prd.md + SDD specs." The "Preserved" and "Modified" sections remain empty with this note. Skip steps 4 and 5 below.

**Legacy scenario:**

1. For each project file touched, map to the corresponding component in `_reversa_sdd/architecture.md` when possible
2. For each affected component, classify the impact type: `rule-altered`, `rule-removed`, `rule-new`, `new-component`, `component-extinct`, `data-delta`, `external-contract-delta`
3. Assign severity aligned with `/reversa-audit` (CRITICAL, HIGH, MEDIUM, LOW)
4. List 🟢 rules from `_reversa_sdd/domain.md` that remain intact (go to the "Preserved" section)
5. List 🟢 rules that were altered or removed (go to the "Modified" section)

File structure:

1. Header with date and feature identifier
2. Table `Affected file | Component | Type | Severity | Justification`
3. Conceptual diff per component, in prose
4. "Preserved" section
5. "Modified" section

Write to `feature-dir/legacy-impact.md` with atomic writing, full rewrite.

## Generating regression-watch.md

**Greenfield scenario:** there are no 🟢 rules to watch (nothing was extracted from existing code yet). Generate the file with the standard structure, main watch empty, and record the implemented RFs (from SDD specs) in the "Notes" section, without regression weight. They gain weight when a future `/reversa` extraction on the new code confirms them as 🟢. Skip steps 1 through 4 below (step 5, stable IDs, applies to the notes).

**Legacy scenario:**

1. For each rule in the "Modified" section of `legacy-impact.md`, generate a watch item
2. For rules explicitly removed, generate a watch item of type `absence`
3. For rules altered, generate a watch item of type `wording` or `presence` as appropriate
4. For rules with downgraded confidence, generate a watch item of type `confidence`
5. Assign stable IDs `W001`, `W002`, ..., recycling old IDs from the file if it already exists

Structure:

1. Header with feature identifier
2. Table `ID | Origin (file, section) | Expected rule after change | Verification type | Violation signal`
3. "Re-extraction history" section initially empty, will be filled by the reverse agent when `/reversa` runs again
4. "Archived" section initially empty

NEVER include in the main watch rules that were originally 🟡 or 🔴, those go to a "Notes" section without regression weight.

Write to `feature-dir/regression-watch.md`. The first execution creates the file; subsequent executions append to the new items sections, never rewriting history or old IDs.

## Updating progress.jsonl

Each line must have, at minimum:

```json
{"ts":"2026-05-05T16:30:00Z","action":"T003","status":"done","files":["src/x/y.js"]}
```

Append-only. Never rewrite previous lines, even if you discover they were wrong. To correct, add a new line `status: corrected` with the target ID.

## Post-execution hooks

Apply `after-coding` in the standard way.

## Final report to the user

1. How many actions executed successfully
2. How many failed (if any)
3. Absolute path of `actions.md`, `progress.jsonl`, `legacy-impact.md`, `regression-watch.md`
4. How many watch items were created in this round
5. Explicit notice: run `/reversa-sync` to converge the delivery into `_reversa_sdd/addenda/` and keep in mind running `/reversa` (re-extraction) again at some future point to close the cycle
6. If execution was partial, indicate the next pending phase or action

NEVER trigger the re-extraction on your own, that is the user's decision.

End with:

> Type **CONTINUE** to proceed with `/reversa-sync` (delivery convergence into the extraction) or another action the user wants.
