---
schemaVersion: 1
generatedAt: <ISO-8601>
reversa:
  version: "x.y.z"
kind: discard_log
producedBy: curator
hash: "sha256:<hash of the body below the front-matter>"
---

# Discard Log

> Complete record of what was discarded from the migration and why. Each item has traceability to its source in the legacy.

## Discarded items

### BR-DISCARD-001
- **Source**: `_reversa_sdd/<unit>/{requirements,design}.md` section <section>
- **Description**: <discarded rule or behavior>
- **Justification**: <text>
- **Linked to paradigm**: yes | no
  - If yes: <which paradigm and how the target paradigm absorbs the case>
- **Replacement in the new system**: <none | replaced by X>
- **Risk of discarding**: low | medium | high, with explanatory note

<repeat per item>

## Items discarded due to paradigm change (dedicated subsection)

> List only of items whose `Linked to paradigm = yes`. Explicit audit for the coding agent.

| ID | Source | Legacy paradigm | Substitute in target paradigm |
|---|---|---|---|
| BR-DISCARD-XXX | <ref> | <e.g.: synchronous pessimistic lock> | <e.g.: idempotency via event ID> |

## Notes
<Curator's final observations about the discarded set.>
