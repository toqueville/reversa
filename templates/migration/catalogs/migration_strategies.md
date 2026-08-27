---
schemaVersion: 1
kind: migration_strategies
description: Advisory catalog of migration strategies with applicability criteria. Used by the Strategist.
---

# Migration Strategies

> Catalog of canonical migration strategies with applicability criteria, cost, risk, timeline, examples, and references.
> Updating this catalog is a maintenance task independent of the Strategist agent.

## Strategies

### Strangler Fig
- **Description**: New system grows around the legacy, incrementally capturing functionalities until the legacy can be shut down.
- **When applicable**:
  - System in production that cannot stop.
  - Need for incrementality.
  - Ability to route between old and new (proxy / API gateway).
- **Cost**: medium.
- **Risk**: low (partial rollback is feasible).
- **Timeline**: long (months to years for large systems).
- **Favored appetite**: conservative, balanced.
- **Example**: API gateway redirects `/v2/orders/*` endpoints to the new system while `/orders/*` continues on the legacy.
- **References**: Martin Fowler, "StranglerFigApplication"; Sam Newman, "Monolith to Microservices".

### Big Bang
- **Description**: Complete replacement in a single cutover window.
- **When applicable**:
  - Small system.
  - Maintenance window tolerated.
  - High transformational appetite.
  - Low number of live external integrations.
- **Cost**: low (no maintenance of two versions).
- **Risk**: high (full rollback is expensive; failure takes down the service).
- **Timeline**: short.
- **Favored appetite**: transformational (for small systems).
- **Example**: internal tool used by 50 people migrated overnight with documented rollback.
- **References**: described in various migration frameworks; high correlation with historical failures in large systems.

### Parallel Run
- **Description**: Legacy and new run in parallel receiving the same input; output is compared to detect divergences.
- **When applicable**:
  - Critical logic (financial, tax, regulatory).
  - Need for equivalence proof over a long period.
  - Large paradigm change + transformational appetite (high operational risk).
- **Cost**: high (two stacks operating simultaneously; output comparison).
- **Risk**: medium (risks come from dual operation, not the cut).
- **Timeline**: medium.
- **Favored appetite**: balanced.
- **Example**: tax calculation running on legacy and new for 60 days; cutover only after divergence < 0.01%.
- **References**: Michael Nygard, "Release It!"; common in banking and tax systems.

### Branch by Abstraction
- **Description**: Internal refactoring of the legacy to introduce an abstraction that allows swapping the implementation underneath, then replacing it.
- **When applicable**:
  - Internal migration (language or framework changes, but the domain stays).
  - Conservative appetite.
  - Team already inside the legacy, with code domain knowledge.
- **Cost**: low.
- **Risk**: low.
- **Timeline**: medium.
- **Favored appetite**: conservative.
- **Example**: extract `OrderRepository` interface in the legacy, let old and new implementations be chosen by flag, then remove the old one.
- **References**: Paul Hammant, "Branch By Abstraction".

## Quick comparison

| Strategy | When applicable | Cost | Risk | Timeline |
|---|---|---|---|---|
| Strangler Fig | system in production, cannot stop | medium | low | long |
| Big Bang | small system, controlled window, transformational appetite | low | high | short |
| Parallel Run | critical logic (financial / tax) | high | medium | medium |
| Branch by Abstraction | internal refactoring before migration | low | low | medium |

## Paradigm influence on strategy choice

- **`conservative` appetite** -> favors Branch by Abstraction and Strangler Fig.
- **`balanced` appetite** -> favors Strangler Fig and Parallel Run.
- **`transformational` appetite** -> allows Big Bang for small systems, Strangler Fig with deep boundaries for larger systems.
- **Large paradigm change + transformational appetite** -> flag `high operational divergence risk` and recommend Parallel Run for validation.

## Utility function (usage by the Strategist)

Pseudo-procedure the agent follows when consulting the catalog:

1. Receive `migration_brief` (scope, deadline, constraints) + `derived_appetite` + `paradigm gap`.
2. Filter strategies by applicability (drop-out those that clearly do not fit).
3. Score each remaining strategy by adherence to appetite and gap.
4. Select the 2 to 3 best candidates.
5. Mark one as `recommended` with explicit justification.
6. For each remaining strategy, list cons as reasons for non-recommendation.

## Catalog test scenarios

1. brief = banking system in production, conservative appetite -> recommend Strangler Fig + Branch by Abstraction.
2. brief = internal tool 50 users, transformational appetite -> recommend Big Bang.
3. brief = tax system, balanced appetite, high paradigm change -> recommend Parallel Run + Strangler Fig.
4. brief = Rails monolith to Go microservices, transformational appetite, large paradigm change -> recommend Strangler Fig with deep boundaries, flag operational risk, suggest Parallel Run for critical domains.
5. brief = .NET WebForms to Blazor, balanced appetite, no large paradigm change -> recommend Strangler Fig.
6. brief = legacy system with few integrations, maintenance window tolerated, balanced appetite -> recommend Big Bang with robust rollback plan, alternative Strangler Fig.
