---
schemaVersion: 1
generatedAt: <ISO-8601>
reversa:
  version: "x.y.z"
kind: data_migration_plan
producedBy: designer
hash: "sha256:<hash of body below the front-matter>"
---

# Data Migration Plan

> Plan for migrating data from the legacy to the new system: mapping, transformations, ETL, data cutover, and validation.

## Summary
- Estimated volume: <rows / GB per main entity>
- Migration window: <see `cutover_plan.md`>
- Strategy: prior backfill + delta + cut | single bulk | continuous replication

## Legacy → new mapping

| Source | Destination | Type | Notes |
|---|---|---|---|
| `<legacy schema>.tb_pedidos` | `pedidos` | rename | type normalization |
| `<legacy schema>.tb_pedido_item` | `pedido_itens` | rename | FK adjusted |
| `<legacy schema>.usr_x` | `usuarios` (partial) + `perfis` | split | extracts profile data |

## Transformations

### Transformation T-01: <name>
- **Applies to**: <column or table>
- **Rule**: <explicit text>
- **Invalid data handling**: <discard | reject | fill with default>
- **Rule origin**: <reference to `target_business_rules.md` or `discard_log.md`>

<repeat per transformation>

## ETL Strategy

- **Tool**: <e.g.: SQL scripts, dbt, Airbyte, custom>
- **Flow**:
  1. <extraction>
  2. <transformation>
  3. <loading>
- **Idempotency**: <how the ETL is safe for re-execution>
- **Expected throughput**: <e.g.: 50k rows/s>

## Backfill and delta

- **Backfill**: <start date, scope, duration>
- **Delta capture**:
  - **Mechanism**: CDC | log mining | timestamps | replication | trigger
  - **Acceptable latency**: <seconds>
- **Periodic reconciliation**: <frequency, scope>

## Data cutover

> See also `cutover_plan.md`. Here only the data-specific part.

- **Window**: <ISO-8601>
- **Cut sequence**:
  1. <step>
  2. <step>
- **Post-cut verification**:
  - **Counts**: <which tables, tolerance>
  - **Checksums**: <critical columns>

## Quality validation

| Metric | Target | Measurement source |
|---|---|---|
| Count per entity | equal ± 0% | direct comparison |
| Monetary value sums | equal ± 0.01% | financial reconciliation |
| Referential integrity | 0 orphans | audit scripts |

## Data-specific risks
- <RISK-XXX: see `risk_register.md`>

## Notes
<Additional observations.>
