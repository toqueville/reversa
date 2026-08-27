# Step 3 — Specs organization

This step happens immediately after the user chooses the `doc_level` (Essential / Complete / Detailed) and before invoking the Archaeologist. This is when Reversa decides and persists the structure in which specs will be generated.

## 1. Decide whether to display the menu

Read, in this order, and merge key by key (full precedence for `config.user.toml`):

1. `.reversa/config.toml`, section `[specs]` (config managed by Reversa)
2. `.reversa/config.user.toml`, section `[specs]` (user's manual override)

The merge is evaluated per key: each key present in `config.user.toml` replaces the corresponding one in `config.toml`. Missing keys continue to come from `config.toml`.

The section is considered **decided** when, after the merge, `granularity` is filled with one of the valid values: `module`, `use-case`, `endpoint`, `hybrid`, `feature`, `custom`.

- **If decided:** skip this entire step. Go directly to invoking the Archaeologist.
- **If not decided** (section absent, or `granularity` empty): present the menu (step 2 below).

### Special case — RF-18

If `granularity` is empty in `config.toml` (or the section was removed) **and** a `[specs]` section exists in `config.user.toml` with any filled key, warn the user before displaying the menu. Use exactly this format:

> "I detected that `.reversa/config.toml` has no specs organization decision, but `.reversa/config.user.toml` contains an override in `[specs]`. The override will remain active after your choice and may overwrite fields you decide now.
>
> Current override in `config.user.toml`:
> [list keys and values]
>
> Do you want to proceed with the menu anyway? (y/N)"

Wait for an explicit affirmative response before proceeding to the menu. An empty or negative response aborts without persisting anything.

## 2. Present the menu

Read `.reversa/context/surface.json` → `organization_suggestion`. Use the `granularity` field to pre-select the suggested option and the `rationale` field to show the reason.

If `surface.json` does not have `organization_suggestion` filled (Scout did not run or failed), display the menu without a default and ask the user to choose manually, per EC-01 of the organization spec.

Use exactly this format (language following `chat_language` from `state.json`, example below in en-us):

```
How do you want to organize the specs for this project?

The Scout analyzed the legacy system and suggests: [translation of the suggested granularity].
Reason: [organization_suggestion.rationale]

  [1] [marker] By code module
  [2] [marker] By use case
  [3] [marker] By endpoint/contract
  [4] [marker] Hybrid (module at root, use cases nested)
  [5] [marker] By features (Scout lists the discovered features)
  [6] [marker] Custom

Choose (Enter accepts the suggested):
```

Where `[marker]` is `*` (asterisk) on the pre-selected option and a space on the others. Add `(suggested)` next to the pre-selected option.

Mapping of the 6 options to the `granularity` value:

| Option | `granularity` |
|--------|---------------|
| 1 | `module` |
| 2 | `use-case` |
| 3 | `endpoint` |
| 4 | `hybrid` |
| 5 | `feature` |
| 6 | `custom` |

### Accepting input

- Enter without typing: accepts the pre-selected option.
- Number from 1 to 6: accepts the corresponding option.
- Any other input: ask again without persisting anything.
- Ctrl+C / ESC / cancellation: abort execution and persist nothing (EC-02).

### Option 6 — custom

If the user chooses 6, open the following prompt:

> "What are the top-level folder names? List them separated by commas or one per line (minimum 1)."

Accept the input, sanitize each name (remove characters forbidden by the OS file system, discard empty names). If the list results empty, repeat the prompt (EC-07). The names go into `custom_folders`.

## 3. Detect conflict with existing structure on disk (RF-11)

Before persisting the decision, check if a specs structure already exists materialized in `<output_folder>/` (defined in `state.json`).

If the output folder has subfolders that correspond to a different granularity from the one just chosen (for example, `endpoint` was chosen but the disk has folders that look like `module`), display a warning comparing the two structures and ask for confirmation:

> "I detected that specs already exist with the **[old]** structure in `<output_folder>/`. You just chose **[new]**, which differs from the previous one.
>
> I will create the new structure in parallel, without touching the previous one. Existing specs remain preserved.
>
> Confirm? (y/N)"

Wait for an explicit affirmative response. A negative response aborts without persisting.

The detection is heuristic and best-effort: compare top-level subfolder names with the modules identified by the Scout (`module`), with URIs/routes (`endpoint`), with features (`feature`), etc. When the heuristic cannot decide clearly, **do not** display the warning (avoids false positives).

## 4. Persist the decision (RNF-03, atomic write)

Update `.reversa/config.toml`, section `[specs]`, with:

```toml
[specs]
layout = "feature-folder"
granularity = "<user's choice>"
custom_folders = [<list>]   # only when granularity == "custom", otherwise []
scout_suggestion = "<organization_suggestion.granularity from surface.json>"
decided_at = "<ISO 8601 UTC timestamp, e.g., 2026-05-03T14:32:00Z>"
```

Rules:

- **Atomic write:** write to a temporary file in the same directory (`config.toml.tmp`) and perform an atomic rename to `config.toml`. A failure during writing must not leave `config.toml` corrupted.
- **scout_suggestion is immutable** (RF-14): if the `[specs]` section already existed but had `granularity` empty and `scout_suggestion` filled, preserve `scout_suggestion`. On first execution, copy the current value of `organization_suggestion.granularity` from `surface.json`.
- **Non-destructive:** preserve any key/section you are not explicitly updating. Do not touch `[project]`, `[user]`, `[output]`, `[agents]`, `[engines]`, `[analysis]`, or other sections.
- **Do not touch `.reversa/config.user.toml`.** That file belongs to the user.
- **IO failure** (full disk, no permission, EC-06): display a clear error, do not create spec folders, do not consider the choice as confirmed. The user can try again on the next execution.

## 5. Flow continuation

After successful persistence, proceed with invoking the Archaeologist per `plan.md`. The decision is available to all agents that write specs.

## 6. Manual re-presentation (RF-17)

There is no dedicated CLI flag for reconfiguration. The user re-presents the menu by manually removing the `[specs]` section from `.reversa/config.toml` (or emptying `granularity`). On the next execution, this step detects the "not decided" state and runs again.

## Folder language (RF-10)

The names Reversa uses for feature folders follow `doc_language` from `state.json`. Do not ask about language in this step. In a `pt-br` installation, folders come out in pt-br; in `en`, in English.

## Checklist before proceeding

- [ ] Read `[specs]` from `config.toml` and merge with `config.user.toml` key by key
- [ ] If already decided, skip the step
- [ ] If there is an override in `config.user.toml` but `config.toml` is empty, display RF-18 warning
- [ ] Read `organization_suggestion` from `surface.json`
- [ ] Display menu with pre-selected suggestion
- [ ] Accept Enter, number 1 to 6, or cancellation
- [ ] If option 6, collect `custom_folders`
- [ ] Detect conflict with existing structure on disk and ask for confirmation
- [ ] Atomic write to `config.toml`
- [ ] Preserve `scout_suggestion` on re-executions with partial section
- [ ] Proceed to the Archaeologist
