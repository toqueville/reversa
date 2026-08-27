---
schemaVersion: 1
generatedAt: <ISO-8601>
reversa:
  version: "x.y.z"
kind: screen_deviation_log
producedBy: screen-translator
mode: append-only
hash: "sha256:<hash of body below the front-matter>"
---

# Screen Deviation Log

> Record of every divergence between the legacy and the spec generated in `target_screens.md`. Append-only. Pending deviations block the handoff to the Inspector.
> Approved deviations are propagated to `parity_specs.md § Exceptions` when the Inspector runs.

## Conventions

- **ID**: `DEV-NNN` (sequential, three digits).
- **Type**:
  - `technical`: technical limitation of the target (e.g.: Windows terminal without UTF-8 without `chcp 65201`).
  - `modernization`: intentional divergence resulting from modernized mode.
  - `platform`: divergence forced by platform incompatibility (e.g.: Win16 → web).
  - `correction`: visual bug in the legacy that the target corrects (e.g.: label typo).
- **Approval**: `pending` | `approved` | `rejected`.
- Deviation `approved` → also listed in `parity_specs.md § Exceptions`.
- Deviation `pending` → blocks handoff to the Inspector.
- Deviation `rejected` → archived with explicit note; agent regenerates the screen in conforming mode.

## Summary

- **Total**: <N>
- **Pending**: <N>
- **Approved**: <N>
- **Rejected**: <N>

## Entries

### DEV-001

| Field | Value |
|---|---|
| Affected screen | <canonical-name> |
| Type | `technical` \| `modernization` \| `platform` \| `correction` |
| Description | <what diverges between legacy and new> |
| Reason | <why the divergence is necessary or acceptable> |
| Origin in legacy | <file:line> |
| Implication for parity tests | <e.g.: byte-by-byte comparison false, use semantic comparison> |
| Approval | `pending` \| `approved` \| `rejected` |
| Approved by | <name or identifier, when approved> |
| Approved on | <ISO-8601, when approved> |
| Propagates to `parity_specs.md § Exceptions` | yes \| no |

### DEV-002

(repeat the block above for each deviation)

## Screens with more than one deviation

| Screen | IDs |
|---|---|
| <screen X> | DEV-001, DEV-007 |

## Notes

<General observations about the deviation set: patterns, learnings applicable to future migrations on the same source→target pair, suggestions for improved adapter for v2.>
