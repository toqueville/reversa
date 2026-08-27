# Code Quality Registry (Reversa Refactor)

> GENERATED / MANAGED by the Reversa Code Quality team. This README holds the registry policies.
> Context folders and transformation artifacts are created on demand.

## Policies

- `control_mode`: gated
  - `gated` (default): reading, analysis, measurement, and behavior proof flow without approval. EVERY step that touches project code goes through a gate with an approved diff.
  - `supervised`: the agent can apply low-risk transformations already proven, notifying; high risk continues with a gate.
  - `autonomous`: automatically applies what is 🟢 and proven. Even here there are mandatory gates: removing code, altering effective spec, sending material to external harness, destructive operation.
- `safety_net_policy`: require-characterization
  - `require-characterization` (default): transformation that alters structure or logic requires a safety net (existing tests + characterization) green before and after.
  - `allow-unproven`: allows transformation without a net, always downgraded to 🔴 and marked as without mechanical proof in the registry.

## Registry invariant

No transformation alters observable behavior. What does not prove preservation stops at the gate. Every applied transformation is reversible via the stored diff.

## Structure

```
_reversa_refactor/
  README.md                         (this file)
  <context>/                        (feature, module, or use case)
    opportunities/                   (detected opportunities, one per file)
    transformations/
      OPP-<date>-<suffix>-<slug>/
        plan.html                    (visual report of the plan, before touching any file)
        safety-net/                  (characterization tests + green/red result)
        before-after/                (evidence: measurement, equivalence proof, death proof)
        CHG-NNN.diff                 (applied diffs, source of reversal)
        transformation.md            (record per opportunity-schema.md)
    generated/                       (index and catalog, regenerable, never manually edited)
```
