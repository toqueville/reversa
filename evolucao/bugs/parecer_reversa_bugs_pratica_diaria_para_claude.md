# Architecture Opinion for Reversa Bugs Review

**Recipient:** Claude
**Project:** Reversa Bugs
**Objective:** review the current plan before any implementation
**Base analyzed:** `Reversa Bugs, Understanding Document`, 07/15/2026
**Decision:** do not implement version 1.2.52 before incorporating and evaluating the points below

---

## 1. Context

The current design of Reversa Bugs is conceptually strong in four aspects:

1. separates registration, diagnosis, decision, and correction;
2. treats the bug as a traceability entity between `SPEC ↔ CODE ↔ TEST ↔ BUG`;
3. creates causal defect memory within the repository itself;
4. proposes multi-engine execution and multi-agent debate without making a specific harness mandatory.

The architecture, however, is still excessively oriented toward the following mental model:

```text
reproduce
    ↓
find root cause
    ↓
create test
    ↓
fix code
    ↓
tests pass
    ↓
spec verdict
    ↓
resolved
```

This flow represents well **how an agent understands and fixes a defect in code**.

It does not yet fully represent **how a modern team takes a defect from discovery to proven correction in the real system**.

The objective of this review is to bring Reversa Bugs closer to the daily practice of software maintenance without destroying its main virtue: agent-oriented causal traceability.

---

# 2. New central premise

Reversa Bugs should not model only a **program repair** process.

It should model the **complete lifecycle of a defect**.

The reference model should become:

```text
INTAKE
   ↓
TRIAGE
   ↓
MITIGATE?
   ↓
REPRODUCE
   ↓
DIAGNOSE
   ↓
ROOT CAUSE
   ↓
PLAN
   ↓
CHANGE SET
   ↓
LOCAL VERIFY
   ↓
PR / REVIEW
   ↓
CI
   ↓
MERGE
   ↓
BACKPORT?
   ↓
RELEASE / DEPLOY
   ↓
OBSERVE
   ├── success → RESOLVED
   └── failure → REOPEN

POSTMORTEM?
```

Not every project will have all these stages.

Reversa should detect the repository context and adapt the cycle.

Examples:

```text
local library:
FIX → TEST → MERGE → RELEASE

production service:
FIX → TEST → PR → CI → MERGE → DEPLOY → OBSERVE

legacy system without CI:
FIX → LOCAL TEST → HUMAN APPROVAL → DELIVERY

critical incident:
MITIGATE → RESTORE → INVESTIGATE → FIX → DEPLOY → OBSERVE
```

Therefore, the lifecycle needs to be **configurable and contextual**, not a single rigid flow.

---

# 3. Mandatory change: separate mitigation from correction

The current plan moves almost immediately to reproduction and root cause.

In practice, severe defects frequently require damage reduction before investigation.

Example:

```text
BUG: duplicate customer billing
```

The correct operational action may be:

```text
1. preserve evidence
2. disable the feature
3. reduce the blast radius
4. apply rollback
5. restore the service
6. investigate the root cause
```

Mitigation is not correction.

The bug schema must explicitly accommodate:

```yaml
mitigation:
  required: true
  status: applied
  kind: feature-disable
  applied_at: 2026-07-15T14:32:00-03:00
  service_restored: true
  temporary: true
```

Initially possible types:

```text
rollback
feature-disable
configuration-change
traffic-reduction
dependency-pin
rate-limit
workaround
manual-procedure
other
```

The system must distinguish:

```text
MITIGATED
≠
FIXED
≠
RESOLVED
```

The bug can remain `active` even after the service is restored.

---

# 4. The fix should not be modeled as "code diff + spec diff"

This is an important limitation of the current design.

A real defect can be fixed by changes in:

```text
CODE
TEST
CONFIGURATION
DATABASE MIGRATION
DATA REPAIR
DEPENDENCY
INFRASTRUCTURE
FEATURE FLAG
API CONTRACT
CACHE
OBSERVABILITY
SPECIFICATION
DOCUMENTATION
```

Therefore, replace the narrow concept of:

```text
code_diff
spec_diff
```

with:

# `Correction Change Set`

Example:

```yaml
change_set:
  - id: CHG-001
    kind: test
    artifact: tests/checkout/test_discount.py
    purpose: reproduce

  - id: CHG-002
    kind: code
    artifact: src/checkout/fechamento.py
    purpose: eliminate-root-cause

  - id: CHG-003
    kind: configuration
    artifact: config/payment.yaml
    purpose: reduce-retry-window

  - id: CHG-004
    kind: data-repair
    artifact: scripts/repair_duplicate_orders.py
    purpose: heal-historical-state

  - id: CHG-005
    kind: specification
    artifact: _reversa_sdd/addenda/bug-BUG-042-v001.md
    purpose: update-effective-spec
```

Each item in the `change_set` must be traceable.

Recommended initial types:

```text
test
code
configuration
migration
data-repair
dependency
infrastructure
feature-flag
api-contract
cache
observability
specification
documentation
other
```

The principle is:

> A bug does not necessarily produce a code patch.
> A bug produces a set of traceable corrective changes.

---

# 5. Add data impact and state recovery

Fixing future logic does not automatically fix the historical state already affected.

Example:

```text
bug fixed:
duplicate discount

historical state:
38,421 orders stored with incorrect value
```

Reversa needs to ask:

```text
Is the system fixed going forward?
Is the old data still incorrect?
Is there affected external state?
Do caches need to be invalidated?
Have incorrect messages already been published?
```

Add:

```yaml
data_impact:
  assessed: true
  historical_corruption: confirmed
  affected_records_estimate: 38421
  external_state_affected: false
```

And, when applicable:

```yaml
data_repair:
  required: true
  strategy: reconciliation-script
  dry_run: passed
  backup_verified: true
  idempotent: true
  rollback_available: true
  artifact: scripts/repair_duplicate_orders.py
```

Also add a systemic recovery view:

```yaml
system_recovery:
  code: healed
  data: healed
  cache: unaffected
  external_state: verified
```

Conceptual rule:

```text
CODE HEALED
≠
SYSTEM HEALED
```

A bug should not be closed just because the test passed if the system still contains corrupted state caused by the defect.

---

# 6. Add a Reproduction Capsule

This is an important structural requirement.

Today the bug points to code, spec, and tests, but does not describe with sufficient precision **in what state of the world the defect occurred**.

Create an entity called:

# `Reproduction Capsule`

Example:

```yaml
reproduction:
  status: confirmed

  repository:
    base_commit: a1b2c3d4
    branch: main
    dirty_tree_digest: sha256:xxxx

  environment:
    os: windows-11
    runtime: python-3.12.4
    lockfile_digest: sha256:yyyy
    container: null

  execution:
    command: pytest tests/checkout/test_discount.py -x
    exit_code: 1
    duration_ms: 1420

  fixture:
    refs:
      - evidence/BUG-007/order.json

  observed_failure:
    expected: 90.00
    actual: 81.00

  determinism:
    attempts: 5
    failures: 5
    reproduction_rate: 1.0
    classification: deterministic

  evidence:
    trace: evidence/BUG-007/run-001.trace.json
    stdout: evidence/BUG-007/run-001.stdout.log
```

The capsule must freeze the minimum context necessary to reproduce and interpret the defect.

It is especially important for:

```text
environment bugs
regressive bugs
intermittent bugs
dependency bugs
concurrency bugs
configuration-sensitive bugs
```

---

# 7. Separate reproduction test from regression test

The current plan approximates the two concepts too closely.

They may coincide, but they are not semantically equivalent.

```text
REPRODUCTION TEST
"Can I make the reported defect appear?"

REGRESSION TEST
"Can I protect the behavior that must not break again?"
```

Example:

```text
Bug:
duplicate payment after timeout
```

Reproduction test:

```text
simulate HTTP timeout
execute retry
observe two charges
```

Regression test:

```text
for any retry with the same idempotency_key
number of effective charges must be exactly 1
```

Recommended schema:

```yaml
tests:
  reproduction_tests:
    - id: BRT-001
      artifact: tests/repro/test_bug_042.py
      proves: reported-manifestation

  regression_tests:
    - id: REG-001
      artifact: tests/payment/test_idempotency.py
      protects: SPEC-PAYMENT-0042
```

The correction may require multiple regression tests to protect distinct properties of the behavior.

---

# 8. Root cause needs epistemological status

The current `root_cause_code` field primarily answers:

```text
where?
```

It does not adequately answer:

```text
why do we believe this is the cause?
how confident are we in this?
what evidence supports the claim?
```

Replace or complement with:

```yaml
root_cause:
  status: confirmed
  confidence: 0.94

  hypothesis:
    "The coupon is reapplied during the closing phase."

  causal_path:
    - cart.apply_coupon
    - order.close
    - apply_adjustments
    - apply_coupon

  evidence:
    - run: RUN-004
      observation: total 90 -> 81

    - trace: TRACE-002
      observation: apply_coupon called twice

  code_refs:
    - symbol: checkout.fechar_pedido
      file: src/checkout/fechamento.py
```

Recommended states:

```text
hypothesized
supported
confirmed
rejected
```

Rule:

> A causal memory needs to distinguish hypothesis from confirmed fact.

Without this, incorrect relationships can contaminate:

```text
graph
impact score
prioritization
future debates
subsequent diagnoses
```

---

# 9. BUG ↔ BUG relationships also need evidence

Today typed relationships are a good idea, but they should not be automatically treated as facts.

Example:

```yaml
relationships:
  - type: caused-by
    target: BUG-003
    status: confirmed
    confidence: 0.91
    evidence:
      - TRACE-044
    asserted_by: reversa-correlator
```

States:

```text
proposed
supported
confirmed
rejected
```

Apply different weights in views and impact score.

Example:

```text
confirmed caused-by: full weight
supported caused-by: partial weight
proposed caused-by: does not enter automatic prioritization
```

A proposed relationship cannot automatically alter the operational priority of other bugs.

---

# 10. The debate should have three modes

The debate should not serve only to choose a correction strategy.

Create:

```yaml
debate_mode:
  - diagnosis
  - repair
  - spec
```

## 10.1 `diagnosis`

Used when there are multiple causal hypotheses.

```text
H1: inconsistent cache
H2: non-idempotent retry
H3: duplicate message in the queue
```

Objective:

```text
compare hypotheses
evaluate evidence
propose discriminative probes
consolidate diagnosis
```

## 10.2 `repair`

Used when the cause is sufficiently confirmed, but there are competing correction strategies.

Objective:

```text
smallest coherent change
lowest regression risk
best alignment with the spec
best reversibility
smallest blast radius
```

## 10.3 `spec`

Used when code, tests, and spec diverge and it is not clear which represents the correct behavior.

Objective:

```text
evaluate observed behavior
evaluate effective spec
evaluate historical evidence
evaluate contracts and consumers
propose spec verdict
```

The `spec` debate should end in a **recommendation**, never an automatic decision.

The final decision remains human.

---

# 11. Spec references cannot depend only on path#anchor

The format:

```yaml
specs:
  - _reversa_sdd/domain.md#regras-de-desconto
```

is a locator, not a stable identity.

After re-extraction:

```text
domain.md
```

can become:

```text
business-rules.md
```

The heading can be changed.

Create stable spec IDs:

```yaml
spec_refs:
  - id: SPEC-DOMAIN-0042
```

And a catalog:

```yaml
id: SPEC-DOMAIN-0042
kind: business-rule
title: Maximum discount limit

current_location:
  file: _reversa_sdd/domain.md
  anchor: regras-de-desconto
```

The bug points to:

```text
SPEC ID
```

The views resolve:

```text
SPEC ID → current location
```

The identity should not be the physical path.

---

# 12. Code references also need to be stronger

An isolated file is too little for temporal traceability.

Example:

```yaml
code_refs:
  - file: src/checkout/fechamento.py
    symbol: checkout.fechar_pedido
    blob_sha: 718f...
    captured_at_commit: a1b2c3
```

When possible, record:

```text
file
symbol
commit
blob sha
line range only as auxiliary locator
```

Line number should never be canonical identity.

The objective is to distinguish:

```text
where the code is today
```

from:

```text
which version of the code participated in the defect
```

---

# 13. The BUG ID needs to be merge-safe

A central registrar solves collisions within a coordinated execution.

It does not necessarily solve:

```text
Codex worktree A
Claude worktree B
```

both reading the same last number and creating `BUG-042`.

Do not use a simple global sequence as canonical identity.

Suggestion:

```text
BUG-20260715-A7K3
BUG-20260715-P9M2
```

or ULID.

The interface can maintain an optional human number:

```yaml
id: BUG-20260715-A7K3
display_number: 42
```

The identity needs to be globally unique and tolerant of concurrent branches and worktrees.

---

# 14. Do not move bug files between status folders

The current design maintains:

```text
open/
active/
resolved/
```

and also:

```yaml
status: active
```

This duplicates the same fact.

The need to detect:

```text
file in active/
status: open
```

is evidence of architectural redundancy.

Recommendation:

```text
_reversa_bugs/
├── bugs/
├── evidence/
├── debates/
├── inspections/
├── postmortems/
└── generated/
```

All bugs go in:

```text
_reversa_bugs/bugs/
```

Status:

```yaml
status: active
phase: diagnosing
```

Recommended statuses:

```text
open
active
resolved
```

Recommended phases:

```text
triaging
mitigating
reproducing
localizing
diagnosing
planning
testing
patching
reviewing
ci-verifying
merging
backporting
releasing
deploying
observing
awaiting-human
```

The generated views can materialize:

```text
generated/open.md
generated/active.md
generated/resolved.md
```

The folder should not be a source of state.

---

# 15. Add PR, review, CI, and merge to the cycle

A local correction is not necessarily the delivery of the correction.

The lifecycle should support:

```text
branch/worktree
commits
pull request
review
CI
merge
```

Example:

```yaml
delivery:
  workspace:
    kind: worktree
    path: .worktrees/BUG-A7K3

  branch:
    name: fix/BUG-A7K3-discount

  commits:
    - a82c91f

  pull_request:
    provider: github
    number: 142
    status: open

  review:
    required: true
    requested:
      - checkout-team

  ci:
    run_id: 1827731
    commit_sha: a82c91f
    status: passed

  merge:
    commit: null
```

Reversa should not depend on GitHub.

Detect:

```text
GitHub
GitLab
other remote
Git without remote
without Git
```

And adapt the workflow.

The integration should be optional, but the lifecycle schema needs to accommodate it.

---

# 16. `resolved` needs to depend on a closure policy

Today the plan tends to close the bug after correction, test, and spec verdict.

This is too early for several types of systems.

Example:

```text
local test passed
CI passed
merge was done
deploy occurred
production exhibited the problem again
```

The bug was not resolved.

Create:

```yaml
closure_policy:
  type: production-service
  requires:
    - merged
    - deployed
    - observation-window-passed
```

Other examples:

```yaml
closure_policy:
  type: package
  requires:
    - merged
    - fixed-version-published
```

```yaml
closure_policy:
  type: local-software
  requires:
    - regression-tests-passed
```

The bug remains:

```yaml
status: active
phase: observing
```

until the closure policy is satisfied.

`resolved` should mean:

> The closure condition defined for this project was provably satisfied.

---

# 17. Add post-correction observation

Reversa records evidence of the defect.

It also needs to record evidence of non-recurrence.

Create:

```yaml
post_fix_observation:
  window:
    started_at: 2026-07-15T16:00:00-03:00
    duration: 2h

  signals:
    - metric: checkout.discount_violation
      before: 8.2%
      after: 0.0%

    - metric: checkout.error_rate
      before: 0.3%
      after: 0.31%

  traces:
    sampled: 1000
    recurrence: 0

  verdict: verified
```

The evidence can come from:

```text
tests
logs
metrics
traces
queries
health checks
smoke tests
external telemetry
manual procedure
```

The idea is to record:

```text
BEFORE FIX
    ↓
CHANGE
    ↓
AFTER FIX
```

and not just:

```text
test failed
    ↓
test passed
```

---

# 18. Intermittent bugs should be first-class citizens

Do not limit reproduction to:

```yaml
reproducible: always
```

Model:

```yaml
reproduction:
  classification: intermittent

  attempts: 100
  failures: 7
  reproduction_rate: 0.07

  suspected_triggers:
    - concurrent-request
    - cache-warm
    - timezone-transition

  controlled_variables:
    random_seed: 4242
    timezone: America/Sao_Paulo
    clock: real
    load: 200-rps
```

Initial classifications:

```text
deterministic
intermittent
environment-dependent
not-reproduced
unknown
```

When there is no reproduction, the flow should be able to conclude:

```yaml
resolution_kind: instrumentation-required
```

In this case, the result of the investigation may be:

```text
add logs
add metrics
add trace
add correlation id
add temporary probe
```

The objective is to capture evidence on the next occurrence.

Instrumentation can be a valid corrective action even without a confirmed root cause.

---

# 19. Make git bisect a formal mechanism

The current document treats Git history primarily as an auxiliary source.

For suspected regression, formalize:

```yaml
regression_analysis:
  suspected: true

  last_known_good: 718ac31
  first_known_bad: ff82d14

  bisect:
    attempted: true
    automated: true
    test_command: pytest tests/repro_bug_42.py
    culprit_commit: b921af2

  introduced_by:
    commit: b921af2
    pull_request: 118
```

When there is:

```text
a known good commit
a known bad commit
a reproducible command
```

Reversa should suggest or execute `git bisect` within the defined security constraints.

This directly combines with the causal memory proposal:

```text
BUG
 ↓
CULPRIT COMMIT
 ↓
PR
 ↓
CHANGE
 ↓
SPEC IMPACT
```

---

# 20. Add affected versions, fixed versions, and backports

Real projects frequently maintain multiple version lines.

Add:

```yaml
versions:
  affected:
    - ">=2.3.0 <2.5.4"

  unaffected:
    - "<2.3.0"

  fixed:
    - 2.5.4
    - 2.4.9
    - 2.3.17
```

And:

```yaml
backports:
  - branch: release/2.4
    status: merged
    commit: a7c31ff

  - branch: release/2.3
    status: conflict
    requires_manual_adaptation: true
```

The bug can be fixed in `main` and remain active for a supported release.

The closure policy needs to consider this when the project has maintained branches.

---

# 21. Add ownership

The fields:

```text
area
module
feature
```

do not say who is responsible for the affected part.

Add:

```yaml
ownership:
  owning_team: checkout

  codeowners:
    - "@empresa/payments"

  assignees:
    - sandeco

  reviewers:
    - "@maria"

  stakeholders:
    - finance
```

When possible, infer ownership from:

```text
CODEOWNERS
Git history
repository structure
project configuration
```

Do not invent ownership.

If there is no evidence:

```yaml
owning_team: unclassified
```

---

# 22. The bug origin can be external

`/reversa-bug` remains valid as a conversational intake.

But bugs also arrive via:

```text
GitHub Issue
GitLab Issue
CI failure
alert
log
trace
Sentry
support
customer
security advisory
```

Add:

```yaml
origin:
  type: github-issue

  external_ref:
    provider: github
    id: "#317"
```

Or:

```yaml
origin:
  type: telemetry

  external_ref:
    provider: sentry
    id: EVENT-82828
```

Initial types:

```text
manual-report
github-issue
gitlab-issue
ci-failure
telemetry
alert
support
customer
security-advisory
inspection
other
```

The `BUG-XXX.md` remains the Reversa source of truth.

The external origin only records where the defect entered the lifecycle.

---

# 23. Add special flow for security bugs

Reversa cannot record exploitable vulnerabilities in public artifacts without considering confidentiality.

Add:

```yaml
visibility:
  classification: restricted
```

Classifications:

```text
normal
internal
restricted
embargoed
```

Upon detecting security indicators:

```text
authentication bypass
authorization bypass
secret exposure
remote code execution
injection
privilege escalation
cryptographic failure
sensitive data exposure
```

the protocol should change.

Minimum rules:

```text
do not write exploitable details in public artifacts
do not send material to external harness without approval
do not include the bug in public views
do not automatically publish detailed root cause
do not expose sensitive evidence in debates
```

The security classification should not be silently assigned as a definitive fact.

The agent can mark:

```yaml
security_suspected: true
```

and request confirmation when necessary.

---

# 24. Separate bug impact from correction risk

The `impact score` answers:

```text
what is the importance or propagation of the defect?
```

It does not answer:

```text
what is the risk of modifying the system to fix it?
```

Create:

# `change_risk`

Example:

```yaml
change_risk:
  score: 87
  classification: critical

  blast_radius:
    affected_symbols: 12
    transitive_callers: 147
    modules: 8

  public_api_change: false
  database_change: true
  external_contract_change: false
```

Possible dimensions:

```text
blast radius
transitive callers
public API
database
external contract
security surface
concurrency
migration
irreversibility
critical path
test coverage
```

The execution policy should consider:

```text
BUG IMPACT
     +
DIAGNOSTIC UNCERTAINTY
     +
CHANGE RISK
     ↓
EXECUTION POLICY
```

Example:

```text
low risk + confirmed cause
→ direct fix

high diagnostic uncertainty
→ diagnosis debate

high change risk
→ repair debate + mandatory review

spec change
→ mandatory human approval

critical production change
→ controlled rollout + observation gate
```

---

# 25. Reduce approval fatigue

The current principle of manual handoff at every stage is safe, but can make approval mechanical and unread.

Do not require `CONTINUE` after every reading or diagnosis action.

Create control modes:

```yaml
control_mode: gated
```

Values:

```text
supervised
gated
autonomous
```

Suggested behavior:

## `supervised`

Frequent approval.

Suitable for:

```text
sensitive environments
onboarding
exploratory investigation
```

## `gated`

Recommended default.

Automatic:

```text
reading
localization
isolated reproduction
diagnosis
evidence collection
view generation
```

Mandatory gate:

```text
apply test that modifies the project
apply correction change set
alter effective spec
use external harness with project access
execute destructive operation
deploy
```

## `autonomous`

Only when explicitly enabled and limited by project policies.

Even in autonomous mode, certain operations may remain mandatorily gated.

Example:

```text
spec change
security
production
irreversible data
```

---

# 26. Add selective postmortem

Do not generate a postmortem for every bug.

Create policy:

```yaml
postmortem_policy:
  required_when:
    - severity: critical
    - data_corruption: true
    - security: true
    - recurrence_count: ">=2"
```

Other possible triggers:

```text
customer outage
major incident
regression recurrence
large financial impact
SLA breach
```

Reversa will already have the necessary data:

```text
BUG RECORD
+
TIMELINE
+
ROOT CAUSE
+
MITIGATION
+
CHANGE SET
+
OBSERVATION
=
POSTMORTEM
```

Save, when required:

```text
_reversa_bugs/postmortems/BUG-XXXX.md
```

The postmortem should be derived from the existing record and not a second source of truth.

---

# 27. Conceptual architecture review

The architecture should not be thought of as:

```text
BUG FILE
   ↓
AGENTS
   ↓
FIX
```

Adopt the following mental model:

```text
                 BUG RECORD
                     │
                     ▼
              BUG STATE MACHINE
                     │
       ┌─────────────┼─────────────┐
       ▼             ▼             ▼
 REPOSITORY      EXECUTION      EFFECTIVE SPEC
   GRAPH           EVIDENCE          GRAPH
       │             │             │
       └─────────────┼─────────────┘
                     ▼
               BUG ORCHESTRATOR
                     │
           ┌─────────┼─────────┐
           ▼         ▼         ▼
        SOLVERS   CRITICS   VERIFIERS
                     │
                     ▼
              APPROVAL GATES
                     │
                     ▼
           CORRECTION CHANGE SET
                     │
                     ▼
               DELIVERY LIFECYCLE
                     │
                     ▼
              CLOSURE POLICY
```

Central point:

> The agents are not the architecture.
> The agents are ephemeral workers of an architecture governed by state, evidence, policies, and traceability.

---

# 28. The five current commands can continue

Do not create ten or fifteen new commands.

Keep:

```text
/reversa-bug
/reversa-bug-fix
/reversa-bug-debate
/reversa-depth-inspection
/reversa-bug-graph
```

The gain should enter primarily in the internal state machine and in the schemas.

## `/reversa-bug`

Responsible for:

```text
intake
initial triage
origin
dedup
initial traceability
classification
security suspicion
registration
```

## `/reversa-bug-fix`

Should become the main lifecycle orchestrator:

```text
mitigation
reproduction
diagnosis
root cause
planning
change set
local verification
delivery
observation
closure
```

Does not mean it executes all stages in all projects.

The closure policy and context define the flow.

## `/reversa-bug-debate`

Receives:

```text
mode: diagnosis | repair | spec
```

## `/reversa-depth-inspection`

Continues as diagnosis-only.

Confirmed findings enter the central registrar.

Should also evaluate signals of:

```text
data corruption
operational risk
security
intermittency
configuration drift
version-specific behavior
```

## `/reversa-bug-graph`

Generates derived views.

Do not use a global NxN matrix as storage.

Prefer catalog and sparse edges.

---

# 29. Implementation requirements derived from this opinion

Before implementing, review `specs/reversa-bugs/` and incorporate, at minimum:

- [ ] complete defect lifecycle;
- [ ] `phase` separated from `status`;
- [ ] stable bug path;
- [ ] mitigation;
- [ ] Reproduction Capsule;
- [ ] reproduction tests separated from regression tests;
- [ ] root cause with epistemological status and evidence;
- [ ] relationships with status, confidence, and evidence;
- [ ] `Correction Change Set`;
- [ ] data impact and data repair;
- [ ] stable spec IDs;
- [ ] temporal and symbolic code refs;
- [ ] merge-safe bug IDs;
- [ ] debate `diagnosis | repair | spec`;
- [ ] delivery lifecycle;
- [ ] optional PR/review/CI/merge;
- [ ] versions, fixed versions, and backports;
- [ ] closure policy;
- [ ] post-fix observation;
- [ ] explicit handling of intermittent bugs;
- [ ] `instrumentation-required`;
- [ ] git bisect as a formal regression mechanism;
- [ ] ownership;
- [ ] external origins;
- [ ] visibility and security flow;
- [ ] `change_risk`;
- [ ] control modes and risk-based gates;
- [ ] postmortem policy.

---

# 30. Acceptance criteria for the new spec

The review will be ready when the design can clearly answer the scenarios below.

## Scenario A: simple local bug

```text
test reproduces
cause confirmed
small patch
regression test passes
no CI
```

Reversa should be able to close the bug without excessive bureaucracy.

## Scenario B: production incident

```text
duplicate payment
financial impact
immediate mitigation
rollback
subsequent investigation
controlled deploy
production observation
```

The bug cannot be marked `resolved` after just a local test.

## Scenario C: data corruption

```text
code fixed
historical data still wrong
```

The system must distinguish `code healed` from `system healed`.

## Scenario D: intermittent bug

```text
7 failures in 100 executions
cause not confirmed
```

The flow should allow additional instrumentation without inventing a root cause.

## Scenario E: regression

```text
there is a good commit
there is a bad commit
reproducible test
```

The system should accommodate `git bisect` and link the bug to the culprit commit.

## Scenario F: multiple versions

```text
main fixed
release/2.4 still affected
```

The bug should remain operationally open when the closure policy requires backport.

## Scenario G: spec divergence

```text
code, test, and spec disagree
it is not clear who represents the correct rule
```

Reversa should be able to open a `spec` debate and require human decision.

## Scenario H: vulnerability

```text
authentication bypass
public repository
```

Reversa cannot publish exploitable details in external views or debates.

## Scenario I: two harnesses in worktrees

```text
Claude registers a bug
Codex registers another at the same time
```

The IDs cannot collide.

## Scenario J: high-risk fix

```text
medium bug
change in middleware used by 147 callers
```

The execution should consider `change_risk`, not just bug impact.

---

# 31. Final directive for the review

Do not implement yet.

First:

```text
1. review requirements.md
2. review design.md
3. review tasks.md
4. update schemas and invariants
5. simulate the 10 acceptance scenarios
6. submit again for review
```

Do not add complexity just for the sake of adding.

The objective is not to transform Reversa Bugs into Jira, Sentry, GitHub Actions, or an observability platform.

The objective is:

> To create a causal, repository-native, agent-oriented memory that accompanies the defect from its discovery to the proven recovery of the system.

The recommended architectural formulation is:

> **Reversa Bugs is a repository-native causal defect memory and orchestration layer that continuously reconciles specifications, implementation, tests, runtime evidence, delivery state, and defect history for agentic software maintenance.**

The main thesis of the project should not be:

> "multiple agents fix bugs".

It should be:

> **The system maintains a verifiable causal memory of the defect and uses specialized agents as ephemeral workers to investigate, decide, fix, and prove the recovery of the software.**

This is the north star for redesigning the spec.
