# Brainstorm: /reversa-add

> Recorded on 2026-07-29, decided on 2026-07-30. No code at this stage.

## The problem

For a last-minute tweak ("make that title bigger", "add a loading spinner here"), the entire forward pipeline is too expensive. In practice the user asks directly in the chat, the code changes, and no artifact records it. The spec falls behind the code.

## The solution

A new command in the forward team: `/reversa-add`. Records the amendment in the spec and implements it, in the same step.

The name stays `/reversa-add`, not `/add`: the spec namespace rule requires `reversa-<verb>`, and `/add` collides with the native `/add-dir` and with the user's own commands in other engines.

## How it works

1. Reads `.reversa/active-requirements.json`. If there is no active feature, aborts and points to `/reversa-requirements`.
2. Refuses and redirects to `/reversa-requirements` if the request requires a new dependency, a schema or contract change, a new API, or touches auth or payments.
3. Writes the amendment under `## Amendments` in the feature's `requirements.md`.
4. Implements.
5. Adds the already-completed action `[X]` to `actions.md`, updates `legacy-impact.md`, appends to `progress.jsonl`.
6. Suggests the next step and waits for CONTINUE.

Order matters: spec before code. The reverse recreates the problem the command solves.

Only touches what belongs to the active feature. Anything outside that goes to `/reversa-requirements`.

## Why step 5 is mandatory

`/reversa-sync` aborts when `legacy-impact.md` is missing, and displays a menu when it finds an open `[ ]` action in `actions.md`. Without those three files, whatever `/reversa-add` does never converges into `_reversa_sdd/addenda/` and the extraction drifts silently.

## What needs to change in Reversa

- `specs/reversa-forward/01-comandos-forward.md`: catalog, fixed command set rule, functional requirements
- `specs/reversa-forward/03-estrutura-saidas.md`: artifact owner and updater table, `requirements.md` and `actions.md` gain a second updater
- `agents/reversa-add/SKILL.md`
- `FORWARD_TEAM` in `lib/installer/prompts.js`
- `before-add` and `after-add` in `templates/forward/hooks.yml`
- docs, README and homepages en, pt, es
- `package.json`, 1.2.56 to 1.2.57

## To verify before implementing

Where the installer reads the forward commands from. The spec mentions `templates/commands-forward/`, the repository has `templates/forward/` with no commands directory. Use `/reversa-sync` as a reference, it is the most recent member of the team.

## Passing debt

The spec calls `/reversa-doubt` what the installer installs as `reversa-clarify`. Fix when that spec is opened.

## Status

Decided. Ready to implement.
