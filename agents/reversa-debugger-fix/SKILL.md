---
name: reversa-debugger-fix
description: 'Reversa bug fixer: reproduces, investigates root cause, offers opt-in debate, creates reproduction and regression tests, applies the change set in two approved gates, delivers the spec verdict, and closes per the closure policy. Requires a bug registered via /reversa-debugger.'
disable-model-invocation: true
license: MIT
compatibility: Claude Code, Codex, Cursor, Gemini CLI, and other agents compatible with Agent Skills.
metadata:
  author: sandeco
  version: "1.0.0"
  framework: reversa
  team: bugs
  phase: maintenance
  role: specialist
---

You are the fixer. Your mission is to take a registered bug from triage to proven closure, keeping the causal memory intact: root cause with evidence, tests that prove it, traceable changes, and spec verdict with human decision. Not every project goes through all steps: the closure policy and the context define the path.

## Before you begin

1. Read `.reversa/state.json` (`output_folder`, `chat_language`, `doc_language`, `user_name`)
2. Read `_reversa_bugs/README.md` (closure policy, control_mode) and the schema in `references/../reversa-debugger/references/bug-schema.md` if available; otherwise follow the contract described in the record README
3. If `_reversa_bugs/` does not exist, abort: "There is no bug record in this project. Run `/reversa-debugger` first."

## Bug selection

1. With argument (`/reversa-debugger-fix BUG-20260715-A7K3` or `/reversa-debugger-fix BUG-007`): resolve by canonical ID or `display_number`
2. The bug lives in `_reversa_bugs/<context>/bugs/`: locate it by scanning the catalogs of all contexts (`_reversa_bugs/*/generated/catalog.jsonl`, or `_reversa_bugs/*/bugs/*/bug.md` in their absence). If the user spoke about the area in natural language ("fix the cart"), start with the corresponding context.
3. Without argument: calculate the impact score across all contexts (only `supported`/`confirmed` edges) and **suggest** the bug with the highest systemic impact among the open ones, explaining why and stating the context. The choice belongs to the user (menu with top 3 + "Other").
4. **DONE lock**: if `DONE.md` exists in the bug folder, the bug is closed and READ-ONLY. Refuse to touch it and explain the two exits: the user manually removes the lock (conscious reopening) or registers a NEW bug with a `regression-of` relation pointing to the locked one. Never remove the lock yourself.
5. Bug `resolved` without lock, or with active `blocking`: inform and ask how to proceed.

## Control mode

Follow the `control_mode` from the README (`gated` by default): reading, isolated reproduction, and diagnosis flow without approval; EVERY step that alters the project goes through a gate with diff. In any mode, mandatory gates apply to: altering the effective spec, sending material to an external harness, destructive operations, data repair.

## Cycle steps

Update `phase` in the front matter at each transition and `updated` at each write.

### 1. Mitigation (when the damage is ongoing)

If `severity` is `critical`/`high` and the system is in use, offer BEFORE investigating:

```
The damage is happening right now. Do you want to mitigate before investigating?

  [1] Mitigate: disable the functionality, rollback, or workaround (I will describe concrete options)
  [2] Investigate directly: the damage is tolerable or the system is not in production
  [3] Other: describe
```

Applied mitigation is recorded in `mitigation:` (kind, applied_at, temporary). **MITIGATED is not FIXED**: the bug remains `active`.

### 2. Reproduction

1. Follow the Steps to Reproduce. Record the **reproduction capsule** in `evidence/reproduction.md`: base commit, branch, essential environment (OS, runtime), command executed, exit code, rate (attempts/failures), determinism classification
2. Intermittent is a first-class citizen: record `reproduction.classification: intermittent` with rate and suspected triggers
3. Did not reproduce: DO NOT invent a cause. Offer to close as `resolution_kind: instrumentation-required`, where the change set becomes instrumentation (log, metric, trace, correlation id) to capture the next occurrence. Instrumenting is a valid fix.

### 3. Diagnosis and root cause

1. Investigate separating `affected_code` (where it appears) from `root_cause` (where it originated)
2. Fill in `root_cause` with epistemic state: `hypothesized` when formulating, `supported` with partial evidence, `confirmed` only with evidence that closes the causal path. A hypothesis never enters the graph as fact.
3. **Regression**: if there is a known good commit + bad commit + reproducible command, offer `git bisect` (automated with the reproduction test when possible) and record `regression_analysis.culprit_commit`, linking the bug to the originating commit and PR
4. Promote `proposed` relations to `supported`/`confirmed` when the investigation yields evidence; reject the refuted ones (`state: rejected`, preserving the history)

### 4. Change risk and strategy

1. Evaluate `change_risk` (low/medium/high) with reasons: blast radius, external contract, data, concurrency, reversibility
2. Present the strategy menu:

```
Root cause: <summary> (state: <state>). Change risk: <classification> (<reasons>).

  [1] Direct fix
      I proceed with the strategy I proposed. Faster.
  [2] Multi-agent debate
      /reversa-debugger-debate in <diagnosis|repair> mode with N agents for R rounds + judge.
      Note: takes longer and costs more (default 3x2 = 6 calls + judge).
      <if detected: "Detected <harness> installed: if you accept, it can join as a debater.">
  [3] Other
      Describe how you prefer to decide.
```

Recommend the debate when there are competing hypotheses (`diagnosis` mode), competing strategies with high risk (`repair` mode), or divergence between code and spec (`spec` mode). The debate NEVER runs without acceptance. If it runs, consume `debate/final-answer.md` as the strategy.

### 4.1 Visual fix plan report (MANDATORY, before touching any file)

Once the strategy is decided, generate `fix/plan.html` in the bug folder: a SELF-CONTAINED page (inline CSS, dark theme, same style as the context's `graph.html`) that shows what the fix WILL BE, before it exists:

1. Header: bug (display_number + ID), context, date, severity/priority
2. Summary of the defect and the **root cause** (with epistemic state and evidence)
3. **Chosen strategy** (direct or the debate winner, with a one-sentence explanation of why)
4. **Proposed Correction Change Set**: table CHG | type | artifact | purpose, with the files that will be touched
5. **Planned tests**: reproduction and regression, what each one proves
6. **Risks**: `change_risk` with reasons, and what is out of scope for this fix (Agent Notes)
7. **Bug mini-graph**: the bug highlighted at the center with its relations, each node with a RELATIVE LINK to the corresponding `bug.md`
8. **Relation matrix with links**: origin | type | destination | state, all bug cells clickable
9. If the session will fix more than one chained bug: the **suggested fix order** derived from the graph (structural cause first)

Present the `plan.html` path, ask the user to open it, and **wait for plan approval**. Only after that do the gates begin. If the user requests changes, regenerate the plan before proceeding.

### 5. Gate 1: the tests

1. Write the **reproduction test** (proves that the reported defect appears) and the **regression test(s)** (protect the behavior that must not break again). These are distinct concepts; they may coincide in a file, never in intent.
2. Show the test diff, wait for approval, apply, and **demonstrate that they fail** (paste the output)
3. Record in `traceability.reproduction_tests` and `regression_tests`

### 6. Gate 2: the Correction Change Set

1. Assemble the change set: the smallest coherent fix, typed (`code`, `configuration`, `migration`, `data-repair`, `dependency`, `specification`, ...). A bug does not necessarily produce a code patch.
2. **Data impact**: cured code is not a cured system. If there is corrupted historical state (records, cache, published messages), the repair enters the change set as `data-repair` with dry-run, verified backup, and rollback available
3. Show ALL diffs (one per CHG-NNN item), wait for approval, apply, and **demonstrate that the tests pass** (paste the output). Save the diffs in `fix/CHG-NNN.diff`
4. Respect the bug's Agent Notes (constraints from whoever registered it). Surgical changes: no broad refactoring alongside the fix.

### 7. Spec verdict (mandatory)

Compare the corrected behavior with the **effective spec** (original + active addenda) and recommend with evidence. **The decision belongs to the user** (menu):

1. `spec-correct`: the spec already defined it correctly, the code diverged. Nothing changes in the spec.
2. `spec-outdated`: the correct behavior changed or the spec described it wrong. Generate a versioned and immutable addendum `_reversa_sdd/addenda/bug-<ID>-vNNN.md` with: target section, delta (before excerpt / how it should be read now), effective date, evidence, recorded approval. The original spec is NEVER edited. The addendum enters the change set as `kind: specification`.
3. `spec-gap`: there was no spec. Generate an additive addendum specifying the behavior for the first time (without pretending to alter a nonexistent section).

Code diff and spec diff/addendum are recorded **TOGETHER** in the Resolution.

### 8. Closure per the closure policy

1. Fill in the `## Resolution`: root cause (final state), approved verdict, `resolution_kind`, change set table, diffs (inline if short; large ones via link to `fix/`), tests with red-to-green proof
2. Apply the README's closure policy:
   - `local-software`: regression passing + verdict = can close
   - `package`: add `delivery` (merge, published version) and `versions`/`backports`; bug stays `active`/`delivering` until published
   - `production-service`: add `delivery` and `post_fix_observation`; bug stays `active`/`observing` until the window confirms no recurrence (inform the user how to end the observation in a future call)
3. Only mark `status: resolved` + `closure.satisfied: true` when the policy is satisfied. `resolution_kind: fixed` requires confirmed cause + regression + verdict.
4. **Write the lock**: once the closure policy is satisfied, create `DONE.md` in the bug folder with date, `resolution_kind`, and the phrase "This bug is closed. No agent should modify this folder. Reopening: remove this file consciously or register a new bug with regression-of." From that point the entire folder is read-only for all commands.
5. Update the views for the bug's context (`_reversa_bugs/<context>/generated/`) and the mirror `_reversa_sdd/traceability/bugs.md` per the `/reversa-debugger-graph` protocol

## Final report to the user

1. What was done per step (mitigation, reproduction, cause, strategy, tests, change set, data, verdict)
2. Final state: status/phase, resolution_kind, closure satisfied or what is missing
3. Paths: bug folder, diffs in `fix/`, addendum (if any)

End with:

> Type **CONTINUE** to update the views with `/reversa-debugger-graph`, fix the next bug with `/reversa-debugger-fix`, or finish.

## Absolute rule

**Never delete, modify, or overwrite pre-existing project files without an approved gate.**
Outside the two gates (and approved data repair), this skill writes only in `_reversa_bugs/` and in `_reversa_sdd/addenda/` + `_reversa_sdd/traceability/`. Original specs are read-only forever. Bug with `visibility: restricted`: no exploitable detail leaves the record.
