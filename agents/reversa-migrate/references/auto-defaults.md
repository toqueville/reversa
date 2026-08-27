# `--auto` defaults

When the user invokes `/reversa-migrate --auto`, the orchestrator skips human pauses and applies these defaults. Before starting, the warning to the user lists each one of them. Each auto-applied item is recorded in `ambiguity_log.md` with the `auto-decided` tag for later review.

## Paradigm Advisor
- Choose **option 1: adopt the natural paradigm of the target stack**.
- `derived_appetite` = `transformational`.

## Curator
- HUMAN DECISION items are marked as pending in `ambiguity_log.md` and do not block the pipeline.
- 🟡 INFERRED items → MIGRATE (with note "validate in the coding agent").
- 🔴 GAP and ⚠️ AMBIGUOUS items → DISCARD with explicit note "auto-discarded, requires review".

## Strategist
- Adopts the strategy marked as **recommended**.
- `critical` risks that would depend on a human owner get `owner = "to be defined"` in `risk_register.md`.

## Designer
- **Topology (Phase 1)**: accepts the proposed modern topology (option 2). Justification recorded in `topology_decision.md` is the Designer's own; in `ambiguity_log.md` the `auto-decided` tag is added for later review. Rationale: `--auto` is for users who want the recommended path; refusing-to-decide would stop the pipeline and violate the `--auto` contract.
- **Architecture (Phase 2)**: approves the first proposal without iteration.
- Bounded contexts, events, and ADRs are accepted as proposed.

## Screen Translator
- **Mode (Phase 1)**: adopts the mode recommended by the agent for the detected source→target pair (literal for textual pairs; modernized for platform changes; hybrid only with an explicit list, therefore never in `--auto`).
- **Generation (Phase 2)**: accepts the generated `target_screens.md` and propagates deviations as `pending`. `--auto` does not approve deviations on its own; they stay in `ambiguity_log.md` as `auto-decided` for later review, without blocking the handoff (exception to `--auto`: if a deviation is `type=correction` in literal mode, the agent refuses and requests human approval even in `--auto`, as changing text without consent breaks expectations).
- **Golden file capture**: not automated in `--auto` (oracle driver is OQ-02). Only emits `manifest.yaml` with suggested commands.
- **Legacy without UI**: marks status `skipped` automatically, without asking.
- **Missing Discovery prerequisites** (`_reversa_sdd/design-system/` or `_reversa_sdd/ui/inventory.md`): creates a minimal `tokens-derived.md` and builds the inventory only from the source code; alerts in `ambiguity_log.md`.

## Inspector
- Uses parity criteria derived directly from the chosen paradigm (see `parity-coverage-matrix.md` in the agent).
- Does not negotiate "accepted parity" criteria with the user.

## Detected manual modifications
- Adopts **option (a)**: preserve the manually modified version and abort regeneration of that artifact. Never destroys human work.

## Mandatory warning

Always before starting `--auto`, present:

> "⚠️ `--auto` mode activated. The defaults below will be applied without pausing for confirmation:
> - Paradigm Advisor: adopt the natural paradigm of the stack (transformational).
> - Curator: ⚠️/🔴 items will be DISCARDED with note; 🟡 items will be MIGRATED with note.
> - Strategist: recommended strategy will be adopted.
> - Designer (topology): proposed modern topology will be adopted (option 2).
> - Designer (architecture): first architecture proposal will be accepted.
> - Screen Translator (mode): adopts the recommended mode for the source→target pair. Hybrid mode never in `--auto`. On legacy without UI, status `skipped`.
> - Screen Translator (generation): deviations stay pending in `ambiguity_log.md` (not approved). Golden file capture not automated (manifest only).
> - Inspector: parity criteria derived from the paradigm without interactive adjustment.
>
> The final `handoff.md` will highlight all auto-decided items for later review.
> Confirm? (y/N)"
