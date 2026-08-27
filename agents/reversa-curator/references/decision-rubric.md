# Curator Decision Rubric

Quick reference table for applying the decision policy.

## Decision table

| Signal observed in the rule | Default decision | Notes |
|---|---|---|
| 🟢 CONFIRMED, compatible with target paradigm, no pain point | MIGRATE | no caveat |
| 🟡 INFERRED, compatible with target paradigm | MIGRATE | add note "validate in the coding agent" |
| 🔴 GAP | HUMAN DECISION | optional recommendation |
| ⚠️ AMBIGUOUS | HUMAN DECISION | mandatory to list interpretations |
| Rule cited as pain point | HUMAN DECISION | default recommendation: replace with X in the new system |
| Rule incompatible with brief (out of scope) | DISCARD | justification: "out of declared scope in migration_brief.md" |
| Rule incompatible with brief (technical) | DISCARD | justification: "technical constraint of the brief prevents it" |
| Rule is a mechanism of the legacy paradigm, paradigm changed | DISCARD (linked to paradigm) | indicate substitute in target paradigm |
| Rule is a mechanism of the legacy paradigm, paradigm is the same | MIGRATE | no caveat |

## List of typical paradigm mechanisms (discardable when paradigm changes)

### Procedural -> event-driven
- Pessimistic lock (`SELECT ... FOR UPDATE`)
- Full ACID transaction around the flow
- Synchronous response to the user with inline side effect
- Retry implemented as `for` in the controller

### Classic OO -> OO with DI
- Active Record that mixes persistence and domain
- Inheritance used for behavior reuse (prefer composition)
- Manual singleton (prefer scoped DI)

### Classic OO -> functional
- Mutable encapsulation (prefer immutable types)
- Void methods with side effects (prefer return + pure function)

### OO with DI -> event-driven
- Synchronous commands with immediate return (prefer event + ack)
- Centralized orchestration (prefer choreography)
- 2PC / distributed transaction (prefer saga)

### Synchronous -> asynchronous in general
- Timeout configured in controller (goes to consumer retry policy)
- Error handling as propagated exception (becomes DLQ)

## What NEVER to discard by paradigm

- Pure business rules (calculations, conditions, derivations).
- Regulatory rules.
- Domain invariants.
- Rights / permissions.

These rules change **location** in the new paradigm, but they do not disappear.
