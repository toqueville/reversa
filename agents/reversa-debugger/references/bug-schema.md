# bug.md schema (schema_version: 1)

Shared contract for all Reversa Bugs Team commands. The `bug.md` is the source of truth;
everything in `generated/` is a projection. References between documents always use the canonical ID, never a path.

## Front matter

```yaml
---
schema_version: 1
id: BUG-20260715-A7K3        # BUG-<YYYYMMDD>-<4 chars base32>, immutable, merge-safe
display_number: 7            # human alias; commands accept ID or display_number
title: Discount applied twice at order checkout
status: open                 # open | active | resolved (the folder NEVER carries the status)
phase: triaging              # triaging | mitigating | reproducing | diagnosing | planning |
                             # testing | patching | delivering | observing | awaiting-human
severity: high               # critical | high | medium | low  (size of the damage)
priority: P1                 # P0 | P1 | P2 | P3               (urgency of fix)
created: 2026-07-15
updated: 2026-07-15

origin:
  type: manual-report        # manual-report | github-issue | gitlab-issue | ci-failure |
                             # telemetry | alert | support | customer | security-advisory |
                             # inspection | other
  external_ref: null         # {provider, id} when applicable

area: sales                  # values from taxonomy.yaml or unclassified
module: checkout
feature: discount
labels: []                   # e.g., spec-gap, financial

visibility: normal           # normal | internal | restricted (security: excluded from public views)
security_suspected: false

reproduction:
  classification: deterministic   # deterministic | intermittent | environment-dependent |
                                  # not-reproduced | unknown
  rate: "10/10"                   # attempts with failure / attempts
  suspected_triggers: []          # for intermittent bugs

blocking: []                 # conditions that block the bug; is_blocked is DERIVED, never status
# - kind: bug
#   target: BUG-20260701-Q2R8
# - kind: external
#   reason: "Waiting for vendor credentials"
#   since: 2026-07-15

relationships: []            # canonical edges, recorded ONCE; inverses derived in views
# - bug: BUG-20260701-Q2R8
#   type: caused-by          # directional: caused-by, blocked-by, duplicate-of, regression-of
#   state: proposed          # proposed | supported | confirmed | rejected
#   evidence: []             # required for state >= supported
# symmetric types: related-to, conflicts-with
# forbidden: self-relation, nonexistent ID, duplicate-of cycle

traceability:
  specs: []                  # locators "path#anchor" in the EFFECTIVE spec (original + active addenda)
  affected_code: []          # where the bug APPEARS
  root_cause: null           # where the bug ORIGINATED, with epistemic state (filled by the fix):
  # root_cause:
  #   state: hypothesized    # hypothesized | supported | confirmed | rejected
  #   hypothesis: "..."
  #   causal_path: []
  #   evidence: [{ref, observation}]
  #   code_refs: [{file, symbol, commit}]
  reproduction_tests: []     # prove that the reported defect appears
  regression_tests: []       # protect what must not break again (DISTINCT concepts)

spec_verdict: null           # spec-correct | spec-outdated | spec-gap (HUMAN decision recorded)

change_set: []               # typed corrective changes (filled by the fix)
# - id: CHG-001
#   kind: test | code | configuration | migration | data-repair | dependency | infrastructure |
#         feature-flag | api-contract | cache | observability | specification | documentation | other
#   artifact: path
#   purpose: short phrase
#   diff: fix/CHG-001.diff

closure:
  policy: local-software     # local-software | package | production-service (from the record README)
  satisfied: false
resolution_kind: null        # fixed | duplicate | invalid | cannot-reproduce | spec-only |
                             # instrumentation-required
---
```

Optional blocks (only when the context exists): `mitigation` (kind, applied_at, temporary),
`data_impact` / `data_repair` (cured code is not a cured system), `regression_analysis`
(last_known_good, first_known_bad, bisect, culprit_commit), `versions` / `backports`,
`ownership` (inferred from CODEOWNERS, never invented; without evidence use unclassified),
`delivery` (branch, PR, CI, merge), `post_fix_observation`, `change_risk`
(classification low|medium|high + reasons).

## Body (sections in order)

1. `# <title>`
2. `## Summary`
3. `## Expected Behavior` (quoting the effective spec; if spec-gap, state it explicitly)
4. `## Actual Behavior`
5. `## Steps to Reproduce`
6. `## Evidence` (paths relative to the bug folder, e.g., `evidence/checkout.log`)
7. `## Suspected Area`
8. `## Acceptance Criteria`
9. `## Traceability` (readable mirror of the YAML block)
10. `## Resolution` (filled by the fix: root cause, approved spec verdict, resolution_kind,
    change set table, code and spec diffs TOGETHER, reproduction and regression tests)
11. `## Agent Notes` (constraints for whoever will fix; taxonomy proposals)

## Completion lock (DONE.md)

When the closure policy is satisfied, the fix writes `DONE.md` in the bug folder (date, `resolution_kind`
and the read-only notice). A folder with `DONE.md` is UNTOUCHABLE by any agent: reopening requires the
user to remove the lock, or a new bug with `regression-of`.

## Invariants (/reversa-debugger-graph validates and STOPS with an error, never silently fixes)

- `status: resolved` requires `resolution_kind` filled and `closure.satisfied: true`
- `DONE.md` without `status: resolved`, or `resolved` + `closure.satisfied` without `DONE.md`, is an inconsistency
- `resolution_kind: fixed` requires `root_cause.state: confirmed`, non-empty `regression_tests`, and `spec_verdict` filled
- Duplicate ID, reference to nonexistent ID, self-relation, and `duplicate-of` cycle are errors
- A `proposed` relation never enters automatic prioritization or the impact score
