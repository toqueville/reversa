---
schemaVersion: 1
generatedAt: <ISO-8601>
reversa:
  version: "x.y.z"
kind: target_domain_model
producedBy: designer
hash: "sha256:<hash of body below front-matter>"
---

# Target Domain Model

> Domain model for the new system. Explicit traceability to the legacy (in `_reversa_sdd/domain.md` or equivalent).

## Aggregates

### AGG-Pedido
- **Aggregate root**: Pedido
- **Invariants**:
  - <invariant 1>
  - <invariant 2>
- **Accepted commands**: <list>
- **Published events** (if event-driven paradigm): <list>
- **Legacy origin**: <ref to `domain.md` or equivalent>

<repeat per aggregate>

## Entities

| Entity | Owning aggregate | Main attributes | Legacy origin |
|---|---|---|---|
| <name> | <agg> | <summarized list> | <ref> |

## Value objects

| Value object | Attributes | Validations | Origin |
|---|---|---|---|
| <name> | <list> | <rules> | <ref> |

## Domain events
> Mandatory section if the paradigm is event-driven or hybrid.

| Event | Published by | Consumed by | Schema (summarized) |
|---|---|---|---|
| <PedidoCriado> | AGG-Pedido | Pagamento, Estoque | <fields> |

## Domain rules
> Mapping of rules from `target_business_rules.md` (only the MIGRATE ones) to the aggregates / services where they now live.

| Rule (ID) | Location in new domain | Origin (target_business_rules.md) |
|---|---|---|
| BR-MIGRATE-001 | AGG-Pedido.invariant <name> | BR-MIGRATE-001 |

## Traceability to legacy

| New element | Legacy origin | Mapping type |
|---|---|---|
| AGG-Pedido | `domain.md section Pedido` + `sdd/orders.md` | merged |
| <new> | <ref> | 1-to-1 / merged / split / new |

## Notes
<Additional modeling observations.>
