---
schemaVersion: 1
generatedAt: <ISO-8601>
reversa:
  version: "x.y.z"
kind: target_data_model
producedBy: designer
hash: "sha256:<hash of body below front-matter>"
---

# Target Data Model

> Data model for the new system. Schema, relationships, and constraints.

## Overview
<Short text: main database type, division by bounded context, roles (OLTP / OLAP / event store).>

## Data entities

| Entity | Table / collection | Owning aggregate | PK | Bounded context |
|---|---|---|---|---|
| <name> | <ref> | <AGG> | <field> | <BC> |

## Schema (DDL or equivalent)

```sql
-- Replace with the actual DDL for the target system.
CREATE TABLE pedidos (
    id UUID PRIMARY KEY,
    cliente_id UUID NOT NULL,
    status TEXT NOT NULL,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

## Relationships

| Source | Destination | Cardinality | Integrity | Notes |
|---|---|---|---|---|
| pedidos.cliente_id | clientes.id | N:1 | FK ON DELETE RESTRICT | |

## Constraints

- **Uniqueness**: <list>
- **Referential integrity**: <enabled / disabled and why>
- **Partitioning / sharding** (if applicable): <description>
- **Critical indexes**: <list>

## Target paradigm-specific considerations

> Dedicated section when the target paradigm is event-driven, functional, or another with direct impact on the data model.

- <e.g.: event-driven -> outbox table for at-least-once guarantee>
- <e.g.: event sourcing -> event store as source of truth, derived projections>
- <e.g.: immutability -> immutable events / snapshots, no updates>

## Legacy origin

| New table / collection | Legacy origin | Transformation |
|---|---|---|
| pedidos | `<legacy schema>.tb_pedidos` | rename + normalized types |

## Notes
<Additional observations about the data model.>
