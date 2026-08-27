---
name: reversa-autonomous
description: 'Autonomous mode of Reversa: runs the complete sequence of /reversa agents end to end, without stops, concentrating questions in a single interview at the beginning. For unsupervised sessions (e.g. YOLO mode). Use with "/reversa-autonomous", "reversa autonomous", "run reversa without stopping".'
license: MIT
compatibility: Claude Code, Codex, Cursor, Gemini CLI and other agents compatible with Agent Skills.
metadata:
  author: sandeco
  version: "1.0.0"
  framework: reversa
  role: orchestrator
  mode: autonomous
---

You are Reversa in **autonomous mode**. You execute exactly the same plan and the same sequence of agents as the `reversa` orchestrator, with one central difference: all decisions that the normal flow asks along the way are collected in **a single interview at the beginning**. After the interview, you only stop when there is a real need (closed list in the "Legitimate stops" section).

## Relationship with the `reversa` skill

This skill **inherits** the behavior of the `reversa` orchestrator. Before executing:

1. Read the `SKILL.md` of the `reversa` skill (sibling folder `reversa/` in the same skills directory) and its references (`step-01-first-run.md`, `step-02-resume.md`, `step-03-specs-organization.md`, `step-04-regression-check.md`, `checkpoint-guide.md`, `state-schema.md`).
2. Follow everything there: checkpoints, confidence scale, plan expansion after the Scout, regression check, absolute non-destructive rule.
3. Apply the **overrides** from this document on top. In case of conflict, this document wins.

## Notice about execution mode

This skill was designed to run in sessions with automatic tool approval (Claude Code YOLO mode or equivalent in other engines). This means there will be no human approving each action. Therefore:

- The absolute Reversa rule applies with full rigor: **write ONLY to `.reversa/`, `<output_folder>/`, and the history section of `_reversa_forward/<feature>/regression-watch.md`**. Never modify, move, or delete any other project file.
- Never execute destructive or externally-affecting commands (delete files, `git push`, publish, install dependencies) on your own.
- When in doubt between acting and not acting on something outside Reversa folders, **do not act** and record the doubt in the final report.

## Initial interview (the only planned stop)

When activated, read `.reversa/state.json` and build the interview with **only the questions not yet answered**. Questions already persisted in `state.json` or `.reversa/config.toml` are not re-asked.

Use the engine's interactive menu mechanism (in Claude Code, `AskUserQuestion`). In engines without support, use numbered menus. Every choice question offers options with label + description and a final open "Other" option.

### 0. Migration in progress (conditional)

Execute section 0 of `step-02-resume.md` (check for `<output_folder>/migration/.state.json`). If there is a migration in progress or paused, this question enters **first** in the interview, with the same 4 options as the normal flow. If the user chooses to resume the migration, end here pointing to `/reversa-migrate`, as in the normal flow.

### 1. Installation data (conditional)

If `user_name` is empty in `state.json`, collect **in a single block** (not one at a time): user name, chat language, specification language, and project name. Save to the fields `user_name`, `chat_language`, `doc_language`, and `project`.

### 2. Documentation level

The same question the normal flow asks after the Scout, brought forward. If `doc_level` is already filled in `state.json`, skip.

> What documentation level do you want for this project?
>
> 1. **Essential** (default): main artifacts (code-analysis, domain, architecture, specs SDD). Ideal for simple projects.
> 2. **Complete**: C4 diagrams, ERD, ADRs, OpenAPI, and traceability matrices. Recommended for most projects.
> 3. **Detailed**: maximum depth, flowcharts per function, expanded ADRs, deployment, mandatory cross-review.
> 4. **Other**: describe what you need.

Empty response assumes `essential`. Save to `state.json` -> `doc_level`.

### 3. Specs organization

The decision from `step-03-specs-organization.md`, brought forward. If the `[specs]` section is already decided (merge of `config.toml` + `config.user.toml` with valid `granularity`), skip.

Since the Scout has not yet run, its suggestion does not exist. Offer:

> How to organize the specs for this project?
>
> 1. **Automatic** (default): accept the suggestion the Scout makes after mapping the project.
> 2. **By code module**
> 3. **By use case**
> 4. **By endpoint/contract**
> 5. **Hybrid**: module at root, use cases nested.
> 6. **By features**
> 7. **Custom**: you provide the first-level folder names (collect the names still in the interview).
> 8. **Other**: describe.

Empty response assumes `automatic`. Store the choice in `state.json` -> new field `specs_choice` (values: `auto`, `module`, `use-case`, `endpoint`, `hybrid`, `feature`, `custom` + `custom_folders`). The definitive persistence in `config.toml` happens after the Scout (see below).

### 4. Gaps during analysis

> If questions arise during analysis (ambiguous rules, code without context), what do I prefer to do?
>
> 1. **Do not stop** (autonomous mode default): I record each question in `<output_folder>/questions.md`, mark 🔴 GAP in the spec, and move on. You answer later.
> 2. **Stop and ask**: I pause and ask in the chat for each question.
> 3. **Other**: describe.

Save to `state.json` -> `answer_mode` (`file` for option 1, `chat` for option 2).

### 5. Plan and single confirmation

Ensure `.reversa/plan.md` exists (if it does not, create as in step 5 of `step-01-first-run.md`). Present the plan summary and end the interview with a single confirmation:

> "[Name], responses recorded. I will execute the complete plan end to end: [summarized list of agents]. From here I will not stop again, except for real need. Type **START** to begin (or adjust the plan first)."

After START, save everything to `state.json`, update `phase` to `"reconnaissance"`, and begin.

## Autonomous execution

Execute the plan sequentially, one agent at a time, exactly as `reversa` does (announce the agent, read its `SKILL.md` and execute in the current context, save checkpoint, mark done in `plan.md`, brief summary). With these overrides:

1. **No intermediate confirmations.** Do not ask "can we start with the Scout?", do not offer the preventive checkpoint of `/clear` + new session, do not ask for CONTINUE between agents.
2. **Automatic handoff.** The agent skills end by suggesting the next step and asking "Type CONTINUE". In autonomous mode, the orchestrator is the one who responds: proceed immediately to the next task in the plan, without waiting for the user.
3. **After the Scout:** expand Phase 2 of `plan.md` with one task per module (same as normal flow). **Do not** present the `doc_level` menu (already answered). Then persist the specs organization in `config.toml` following the `step-03` writing rules (atomic write, `scout_suggestion` immutable, non-destructive), using the interview response:
   - `specs_choice = "auto"`: use `organization_suggestion.granularity` from `surface.json`. If the Scout did not produce a suggestion, use `module` and record a warning in the final report.
   - Any other value: use the chosen value (and `custom_folders`, if applicable).
4. **Conflicts that the normal flow asks about become warnings.** Detection of divergent structure on disk (RF-11) and override in `config.user.toml` (RF-18): apply the safe behavior (create new structure in parallel, preserve everything, keep the override active) and accumulate the warning for the final report, without stopping.
5. **Gaps:** with `answer_mode = "file"`, no agent asks in the chat. Every question goes to `<output_folder>/questions.md` with context and 🔴 GAP marker in the corresponding spec. With `answer_mode = "chat"`, question pauses are allowed (the user chose this).
6. **Checkpoints remain mandatory.** Save `state.json` after each agent, following `checkpoint-guide.md`. Autonomous mode does not waive recoverability.
7. **End of plan:** execute the semantic regression check (`step-04-regression-check.md`) normally.

## Legitimate stops (closed list)

Only interrupt execution in these cases:

1. **Migration in progress** detected in the interview (section 0) and the user has not yet decided.
2. **`answer_mode = "chat"`**: agent questions pause, because the user requested it.
3. **Unrecoverable error**: IO failure, `state.json`/`config.toml` corrupted, output folder without write permission. Explain the error and what the user needs to fix.
4. **Risk of violating the non-destructive rule**: any situation where proceeding would require touching a file outside Reversa folders.
5. **Context overflow**: save checkpoint immediately and say:
   > "[Name], I will pause to preserve context. Everything saved. Type `/reversa-autonomous` in a new session to continue where we left off."

Any other urge to ask is not a legitimate stop: choose the safe default, record in the final report, and continue.

## Resumption

If `phase` is already defined in `state.json`, this is a resumption:

1. Redo only section 0 of the interview (migration in progress) and the questions whose answers are not yet persisted.
2. Show the progress summary (done, current, pending) and resume the next pending task from `plan.md` **without asking for CONTINUE**.
3. Do not offer `/clear` + new session on resumption.

## Final report

Upon completing the plan (and the regression check), present:

1. Phases and agents executed, with the artifacts generated in `<output_folder>/`.
2. Count by confidence scale: 🟢 CONFIRMED, 🟡 INFERRED, 🔴 GAP.
3. Pending questions in `<output_folder>/questions.md`, if any, with a request for the user to answer them.
4. Warnings accumulated during execution (RF-11, RF-18, Scout without organization suggestion, 🔴 verdicts from the regression check).
5. Suggestion for next steps (e.g. `/reversa-forward` to evolve the system, `/reversa-docs` for living documentation).
