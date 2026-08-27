---
name: reversa-sync
description: 'Post-coding convergence for Reversa: distills the delivered feature into an addendum in `_reversa_sdd/addenda/`, keeping the representative extraction between re-extractions, without touching the original artifacts. Optional step of the forward cycle after /reversa-coding.'
disable-model-invocation: true
license: MIT
compatibility: Claude Code, Codex, Cursor, Gemini CLI, and other agents compatible with Agent Skills.
metadata:
  author: sandeco
  version: "1.0.0"
  framework: reversa
  phase: forward
  stage: sync
---

You are the synchronizer. Between a forward cycle delivery and the next `/reversa` re-extraction, the extraction in `_reversa_sdd/` becomes stale: the code has already changed, but `architecture.md` and `domain.md` still describe the previous system. Your mission is to close this gap by creating an **addendum** per delivered feature in `_reversa_sdd/addenda/`, so that whoever reads the extraction (human or agent) sees the system as it stands today. The addendum is a bridge: it remains valid until the next re-extraction, which will mark it as superseded.

## Before you begin

1. Read `.reversa/state.json` to resolve `output_folder` and `forward_folder`
2. Use the actual values wherever the text mentions `_reversa_sdd/` or `_reversa_forward/`

## Initial Checks

1. Read `.reversa/active-requirements.json`
   1.1. If absent, abort with a message pointing to `/reversa-requirements`
2. Check for the existence of `feature-dir/legacy-impact.md`
   2.1. If absent, abort: "The active feature has not yet gone through `/reversa-coding`; there is no delivery to converge. Run `/reversa-coding` first."
3. Detect the delivery scenario:
   3.1. **Legacy:** `_reversa_sdd/` contains `architecture.md` AND `domain.md`
   3.2. **Greenfield:** the header of `legacy-impact.md` records "Greenfield feature", or `_reversa_sdd/` contains `prd.md` AND specs in `_reversa_sdd/sdd/` (without the legacy anchor)
4. If `feature-dir/actions.md` still has open `[ ]` actions, present the menu before proceeding:

   ```
   The active feature still has <N> open action(s) in actions.md.

     [1] Partial sync: generate the addendum with what has already been delivered; a future re-execution will complement it
     [2] Wait: end now and come back after /reversa-coding closes all actions
     [3] Other: describe what you prefer to do
   ```

   Wait for the choice. Do not decide on your own.
5. Apply `before-sync` in the standard way

## Reading sources

Read the following, skipping any that do not exist:

1. `feature-dir/legacy-impact.md` (required, main source of the delta)
2. `feature-dir/regression-watch.md` (IDs of created watch items)
3. `feature-dir/requirements.md` (feature objective and requirements)
4. `feature-dir/progress.jsonl` (count of executed actions)
5. The extraction artifacts referenced in `legacy-impact.md`, only to verify section names when building the pointers

## Addendum generation

Path: `_reversa_sdd/addenda/<feature-id>-<short-name>.md` (same name as the feature folder in `_reversa_forward/`). Create the `addenda/` folder if it does not yet exist.

File structure:

1. Header with title, feature identifier, ISO 8601 date, and scenario (`legacy` or `greenfield`)
2. Section `## Validity` containing, on creation, a single line:

   ```
   Valid since YYYY-MM-DD.
   ```

   The reversa pipeline later appends the line `Superseded by re-extraction of YYYY-MM-DD.` when `/reversa` runs again. An addendum is **valid** as long as there is no supersession line. Never create the addendum already superseded; never write that second line yourself.
3. Section `## Delivery summary`: feature objective in short prose (from `requirements.md`) and the count of completed actions
4. Section `## Impact per extraction artifact`: table `Artifact | Section | Impact type | Delta`
   4.1. **Legacy scenario:** derive the rows from `legacy-impact.md`. Components point to `_reversa_sdd/architecture.md#<section>`, business rules to `_reversa_sdd/domain.md#<section>`. Reuse the coding taxonomy: `rule-changed`, `rule-removed`, `rule-new`, `component-new`, `component-extinct`, `data-delta`, `external-contract-delta`
   4.2. **Greenfield scenario:** point to `_reversa_sdd/prd.md` and to the specs in `_reversa_sdd/sdd/`, with type `component-new`, recording the implemented functional requirements
   4.3. The `Delta` column describes in one sentence how the artifact should be read now (for example: "rule X now requires Y, see legacy-impact.md of the feature")
5. Section `## Rules under watch`: only the IDs of watch items (`W001`, ...) with a pointer to `_reversa_forward/<feature>/regression-watch.md`. Do not duplicate the content of watch items
6. Section `## Sources`: relative paths of the feature artifacts used as the basis

Writing policy:

- First execution: create the file (atomic write, tempfile plus rename, UTF-8 without BOM)
- Re-execution for the same feature (for example, after partial sync): append a `## Update YYYY-MM-DD` section at the end with the new delta. Never rewrite or delete previous addendum content
- Never modify `architecture.md`, `domain.md`, `prd.md`, the specs in `sdd/`, or any other extraction artifact. The addendum annotates, it does not correct

## Post-execution Hooks

Apply `after-sync` in the standard way.

## Final report to the user

1. Absolute path of the created or updated addendum
2. Number of impacts recorded in the table, broken down by type
3. Detected scenario (legacy or greenfield)
4. Explicit notice: the addendum keeps the extraction readable until the next re-extraction. When running `/reversa` again, the regression check will mark this addendum as superseded and the regenerated extraction becomes the single source again

End with:

> Type **CONTINUE** to proceed with `/reversa-forward` (new feature) or type `/reversa` when you want the full re-extraction.

## Absolute rule

**Never delete, modify, or overwrite pre-existing project files.**
This skill writes ONLY to `_reversa_sdd/addenda/`. The original extraction artifacts and the feature artifacts in `_reversa_forward/` are read-only here.
