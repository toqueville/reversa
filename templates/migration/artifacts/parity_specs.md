---
schemaVersion: 1
generatedAt: <ISO-8601>
reversa:
  version: "x.y.z"
kind: parity_specs
producedBy: inspector
hash: "sha256:<hash of body below front-matter>"
---

# Parity Specs

> Behavioral equivalence validation strategy between legacy and new system, adapted to the paradigm chosen in `paradigm_decision.md`.

## General strategy
- **Applicable validation modes** (check those used):
  - [ ] Shadow mode (traffic mirroring with asynchronous comparison)
  - [ ] Characterization tests (suite derived from the legacy's current behavior)
  - [ ] Contract tests (external interfaces)
  - [ ] Data parity (snapshots and checksums)
  - [ ] Other: <specify>

## "Accepted parity" criteria
- **Primary metric**: <e.g.: functional divergence index < 0.01% for N consecutive days>
- **Observation window**: <evaluation period>
- **Blocking criterion**: <when insufficient parity blocks the cutover>

## Coverage adapted to paradigm

> This section changes according to the target paradigm confirmed in `paradigm_decision.md`.

### No paradigm change
- Standard functional equivalence: same input -> same output -> same observable side effect.

### Synchronous -> event-driven change
- **Message ordering**: <acceptance criterion per channel / partition>
- **Idempotency**: <proof that reprocessing does not duplicate effect>
- **Eventual consistency**: <maximum accepted propagation window>
- **Behavior under queue failure**: <retry, DLQ, replay>

### Procedural -> OO change
- **Invariants in aggregates**: <set to validate>
- **Validation in factories / constructors**: <critical cases>

### OO -> functional change
- **Immutability**: <critical points to observe>
- **Absence of expected side effects**: <where the legacy had implicit side effects>
- **Equivalence under composition**: <composed functions equivalent to legacy flow>

## Test types to apply
- **Functional**: <description, tool>
- **Contract**: <description, tool>
- **Load / performance**: <description, targets>
- **Resilience** (if applicable): <queue failure, external dependency unavailable>

## Reuse of discovery team characterization_specs
- **Source**: `_reversa_sdd/characterization_specs/` or equivalent available.
- **Adaptations needed for the new system**: <text>

## Outputs
- `parity_tests/*.feature`: Gherkin scenarios for critical flows.

## Notes
<Additional observations.>
