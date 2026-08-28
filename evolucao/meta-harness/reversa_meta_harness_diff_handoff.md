# Reversa, Meta-Harness, Diff, and Handoff

## Conceptual and architectural evolution document

This document consolidates the discussion on the use of **diff** and **handoff** in AI agent-oriented software development and proposes its incorporation into **Reversa** within a **meta-harness** architecture.

The central idea is to treat agent execution not as an informal sequence of prompts, but as a coordinated, verifiable, traceable work system capable of transferring state between different harnesses, agents, and sessions.

---

# 1. What is diff in software development

In software development, **diff** is the representation of the differences between two versions of code or a set of files.

It shows, normally line by line:

- what was added;
- what was removed;
- what was changed.

Example:

```diff
- total = preco * quantidade
+ total = preco * quantidade * desconto
```

In this case:

- `-` represents a removed line;
- `+` represents an added line.

In practice, the old line was replaced by the new one.

## 1.1 Diff as a representation of change

The diff does not need to re-present the entire system.

Its objective is to answer:

> What changed between the previous state and the current state?

This characteristic makes the diff especially important in software maintenance.

A system can contain thousands or millions of lines of code. In a maintenance activity, it is normally not necessary to review the entire system. The interest is concentrated on the change produced.

Therefore, the diff can be understood as:

> The visual and structural unit of change in code.

---

# 2. Where diff is used

| Context | Use of diff |
|---|---|
| Software maintenance | Identify the code changed during a fix |
| Git and versioning | Compare versions, commits, and branches |
| Code review | Review only the changes made |
| Bug fixing | Identify which lines were modified |
| Pull Request | Show proposed changes before integration |
| Audit | Track changes in the system |
| Refactoring | Evaluate the extent of structural changes |
| AI-driven development | Verify exactly what an agent modified |

In Git, for example:

```bash
git diff
```

This command shows local changes not yet committed.

It is also possible to compare two commits:

```bash
git diff commitA commitB
```

Or compare two branches:

```bash
git diff main feature-login
```

---

# 3. Diff in development with AI agents

With agents like Claude Code, Codex, and other programming harnesses, the diff gains even greater importance.

An agent can:

- create files;
- remove code;
- change APIs;
- modify tests;
- alter configurations;
- introduce changes outside the requested scope.

The agent's textual response is not sufficient to precisely determine what happened.

The agent can state:

> I fixed the login.

But the repository can show:

```text
18 files changed
1,842 insertions
763 deletions
```

In this scenario, there is a difference between:

- the **agent's declaration**;
- the **observable material change in the code**.

The diff functions as objective evidence of the execution.

We can summarize:

> The agent describes what it believes it did.

> The diff shows what effectively changed.

---

# 4. What is handoff

**Handoff** means the transfer of responsibility, context, and work from one person, team, process, or agent to another.

In software development, the concept can be summarized as:

> I executed my part. This is the current state. Continuation starts from here.

Handoffs appear in various traditional software engineering contexts.

| Artifact or process | Type of handoff |
|---|---|
| Pull Request | Developer to reviewer |
| Issue | Product or support to development |
| ADR | Architect to current and future developers |
| Runbook | Engineering to operations |
| Incident report | One on-call shift to another |
| README | Author to users and maintainers |
| Ticket | One team to another |
| Change Request | Requester to responsible team |

Therefore, **handoff is not just a developer slang term**.

It is a consolidated professional concept in engineering, operations, SRE, incident response, support, and project management.

However, there is an important distinction:

> There is a consolidated concept of handoff, but there is no mandatory universal file format for handoff.

---

# 5. Handoff in Claude Code, Codex, and agents

When Claude Code or Codex talks about saving a handoff for another session, the term is being used as a form of **operational context persistence**.

A session can end.

Another agent can take over the work.

Another model can be used.

The original LLM context may no longer exist.

The handoff records sufficient information to allow continuity.

Example:

```text
HANDOFF.md

Objective:
Implement OAuth authentication.

Current state:
Backend completed.

Changed files:
- src/auth/oauth.py
- src/routes/login.py

Decisions:
We used OAuth 2.0 with PKCE.

Known issues:
Callback fails on Windows environment.

Next step:
Fix callback and run integration tests.
```

The objective is not simply to document the work.

The objective is to allow another executor to continue without needing to reconstruct all the previous reasoning.

We can define handoff for agents as:

> A structured checkpoint of the operational state of the work.

---

# 6. Handoff as operational memory

There is a difference between traditional documentation and handoff.

Documentation can explain:

- how the system works;
- why an architecture was chosen;
- which APIs exist;
- how to install the project.

The handoff answers different questions:

- what was the current objective?
- what has already been executed?
- what is the state at this moment?
- what decisions were made?
- which files were affected?
- what was proven?
- which risks remain?
- what is still missing?
- who or which harness should continue?

Therefore, the handoff can be seen as **short and medium-term operational memory of the development process**.

In multi-agent systems, it functions as a form of state persistence between executions.

---

# 7. Meta-harness

A **meta-harness** is a harness responsible for coordinating other harnesses.

Instead of directly executing all development activities, the meta-harness acts as a controller.

It can:

- interpret objectives;
- select specialized harnesses;
- delegate tasks;
- track results;
- verify evidence;
- evaluate inconsistencies;
- decide the next step;
- interrupt loops;
- request corrections;
- transfer work between agents.

Conceptual example:

```text
                    META-HARNESS
                         │
                         ▼
               IMPLEMENTATION HARNESS
                         │
                         ▼
                 TESTING HARNESS
                         │
                         ▼
                AUDIT HARNESS
                         │
                         ▼
                CORRECTION HARNESS
```

The fundamental problem of this architecture is:

> How to transfer the work state from one harness to another?

The proposed answer is:

> Handoff.

---

# 8. Handoff as a contract between harnesses

The handoff can be transformed into a **communication contract between harnesses**.

A harness should not simply return:

```text
done
```

Or:

```text
finished
```

Or:

```text
task completed
```

These responses are insufficient for a meta-harness.

The harness should produce a structured package containing the execution state.

Example:

```yaml
objective: Fix BUG-042

status: implemented

summary:
  The login was comparing the password directly.
  The validation was changed to use the stored hash.

reason:
  The previous implementation was incompatible with
  the flow defined in SPEC-AUTH-003.

files_touched:
  - src/auth/login.py
  - tests/auth/test_login.py

specs:
  - SPEC-AUTH-003

verification:
  command: pytest tests/auth/test_login.py
  result: passed
  evidence: 12 tests passed

remaining_risks:
  - OAuth has not yet been validated

unresolved_items:
  - run complete authentication regression

recommended_next_step:
  Run complete authentication regression

recommended_harness:
  regression-testing
```

The handoff ceases to be an informal annotation.

It becomes a machine-processable artifact.

---

# 9. Handoff and diff have different functions

The handoff and the diff are not competitors.

They represent different dimensions of the execution.

## Diff

The diff is:

- mechanical;
- objective;
- observable;
- reproducible;
- verifiable.

It answers:

> What changed?

## Handoff

The handoff is:

- semantic;
- contextual;
- operational;
- interpretive;
- continuity-oriented.

It answers:

> What happened and how to continue?

The relationship can be synthesized as:

> Diff shows what changed.

> Handoff explains what happened and how to continue.

---

# 10. The central combination: handoff + diff

The combination of the two concepts is especially powerful in a meta-harness.

The harness executes an activity.

After execution:

1. the system captures the diff;
2. the harness generates the handoff;
3. the meta-harness receives both;
4. the meta-harness compares declaration and evidence;
5. the meta-harness decides the continuation.

Architecture:

```text
                    BOSS META-HARNESS
                           │
                    delegates objective
                           │
                           ▼
                 IMPLEMENTATION HARNESS
                           │
                    executes work
                           │
                    ┌──────┴──────┐
                    ▼             ▼
                  DIFF         HANDOFF
             "what changed"   "what happened"
                    │             │
                    └──────┬──────┘
                           ▼
                    META-HARNESS
                           │
                    makes decision
                           ▼
              next specialized harness
```

---

# 11. The diff audits the handoff

This is one of the most important ideas of the discussion.

An agent can produce the following handoff:

```yaml
status: completed
summary: Fixed the login problem
```

However, the diff can show:

```text
src/auth/login.py
src/database/models.py
src/api/users.py
src/config.py
src/payment/stripe.py
README.md
```

There is an inconsistency.

The scope described by the agent does not explain the observed changes.

The meta-harness can identify:

```yaml
decision: REJECT_HANDOFF

reason:
  The scope declared in the handoff does not explain
  the changes observed in the diff.

next_harness: diff-auditor
```

Thus:

> The diff audits the handoff.

The handoff is a declaration produced by the agent.

The diff is material evidence collected directly from the repository.

---

# 12. The handoff explains the diff

The relationship also works in the opposite direction.

Consider the diff:

```diff
- if user.password == password:
+ if verify_password(password, user.password_hash):
```

The diff shows a change.

But it does not necessarily explain:

- why it was necessary;
- which bug was related;
- which specification required the change;
- which risks were considered;
- what still needs to be tested.

The handoff can record:

```yaml
objective: Fix BUG-042

summary:
  Authentication was comparing the password in plain text.
  The implementation was adjusted to validate the stored hash.

reason:
  The previous behavior violated SPEC-AUTH-003.

verification:
  - pytest tests/auth/test_login.py
  - 12 tests passed

remaining_risks:
  - OAuth was not validated
```

Thus:

> The handoff explains the diff.

---

# 13. Declaration versus evidence

The handoff + diff combination creates an important conceptual distinction.

## Handoff

Represents the executor's declaration.

```text
The agent claims it did X.
```

## Diff

Represents the material evidence of change.

```text
The repository shows that Y changed.
```

## Meta-harness

Acts as judge.

```text
Is X consistent with Y?
```

The idea can be synthesized as:

> The handoff is the agent's declaration.

> The diff is the material evidence.

> The meta-harness verifies whether declaration and evidence are consistent.

---

# 14. Suggested flow for the meta-harness

An initial flow can be structured as follows:

```text
1. DELEGATE
   │
   ▼
2. EXECUTE
   │
   ▼
3. CAPTURE DIFF
   │
   ▼
4. GENERATE HANDOFF
   │
   ▼
5. CROSS-VALIDATE
   │
   ├── does handoff match diff?
   ├── does diff match objective?
   ├── do changed files make sense?
   ├── were related specs respected?
   ├── did verifications actually pass?
   └── were risks identified?
   │
   ▼
6. DECIDE NEXT HARNESS
```

Step 5 can be called:

```text
Handoff-Diff Consistency Check
```

Or:

```text
Cross-Evidence Validation
```

---

# 15. The four layers of evidence

The architecture can evolve to a comparison between four components:

```text
INTENT
   ↕
HANDOFF
   ↕
DIFF
   ↕
VERIFICATION
```

## 15.1 Intent

Represents the original objective.

Example:

```yaml
objective:
  Fix BUG-042
```

## 15.2 Handoff

Represents the agent's interpretation and declaration.

```yaml
status: completed
summary: Login fixed
```

## 15.3 Diff

Represents the material changes in the repository.

```text
src/auth/login.py
tests/auth/test_login.py
```

## 15.4 Verification

Represents evidence of functionality.

```text
12 tests passed
```

The meta-harness must verify the consistency between these four dimensions.

---

# 16. Acceptance example

Objective:

```yaml
objective:
  Fix BUG-042
```

Handoff:

```yaml
status: completed

summary:
  Login fixed by replacing the direct password
  comparison with stored hash validation.
```

Diff:

```text
src/auth/login.py
tests/auth/test_login.py
```

Verification:

```text
12 passed
```

Decision:

```yaml
decision: ACCEPT

next_harness: regression-auditor

reason:
  Diff consistent with the objective.
  Handoff consistent with the changes.
  Local verification passed.
  Global regression not yet executed.
```

---

# 17. Rejection example

Objective:

```yaml
objective:
  Fix BUG-042 related to login
```

Handoff:

```yaml
status: completed
summary: Fixed login
```

Diff:

```text
src/auth/login.py
src/database/models.py
src/api/users.py
src/config.py
src/payment/stripe.py
README.md
```

Decision:

```yaml
decision: REJECT_HANDOFF

reason:
  The scope declared in the handoff does not explain
  the changes observed in the diff.

next_harness: diff-auditor
```

The meta-harness can forward the work to a harness specialized in change auditing.

---

# 18. Handoff Package

Every child harness can be required to return a **Handoff Package**.

Conceptual structure:

```text
HANDOFF PACKAGE
├── objective
├── task_id
├── status
├── summary
├── decisions
├── assumptions
├── diff_reference
├── files_touched
├── specs_affected
├── bugs_related
├── verification
├── risks
├── unresolved_items
├── recommended_next_step
└── recommended_next_harness
```

A possible YAML representation:

```yaml
handoff:
  version: "1.0"

  task_id: BUG-042

  objective:
    Fix authentication failure in local login.

  status:
    implemented

  summary:
    The direct password comparison was removed.
    Authentication now uses the stored hash.

  decisions:
    - id: DEC-001
      description: Use existing verify_password.
      reason: Avoid duplication of cryptographic logic.

  assumptions:
    - The current password_hash format is valid.

  diff_reference:
    base: abc123
    head: def456

  files_touched:
    - src/auth/login.py
    - tests/auth/test_login.py

  specs_affected:
    - SPEC-AUTH-003

  bugs_related:
    - BUG-042

  verification:
    commands:
      - pytest tests/auth/test_login.py
    results:
      - 12 passed

  risks:
    - OAuth flow was not validated.

  unresolved_items:
    - Run complete authentication regression.

  recommended_next_step:
    Run regression tests.

  recommended_next_harness:
    regression-testing
```

---

# 19. Handoff as a first-class artifact

In Reversa, the handoff should be treated as a **first-class artifact**.

This means it should not be just text freely generated by the LLM.

It should have:

- schema;
- identifier;
- version;
- validation;
- persistence;
- traceability;
- references;
- history.

Example:

```text
.reversa/
├── specs/
├── bugs/
├── traceability/
├── handoffs/
│   ├── BUG-042/
│   │   ├── HO-0001.yaml
│   │   ├── HO-0002.yaml
│   │   └── HO-0003.yaml
│   └── FEATURE-AUTH/
├── decisions/
└── meta-harness/
```

However, care should be taken not to create an excessively deep tree.

A simpler alternative:

```text
.reversa/
├── specs/
├── bugs/
├── handoffs/
├── traceability/
└── state/
```

Files:

```text
handoffs/
├── HO-000001-BUG-042.yaml
├── HO-000002-BUG-042.yaml
├── HO-000003-FEATURE-AUTH.yaml
└── HO-000004-SPEC-AUTH-003.yaml
```

The relationship between entities can be maintained by IDs and by a traceability matrix or graph.

---

# 20. Relationship with traceability in Reversa

The previous discussion about Reversa already pointed to the need to link:

- code;
- SPECs;
- bugs;
- features;
- subsystems;
- modules.

With handoff and diff, new relationships can be added.

Example:

```text
BUG-042
   │
   ├── affected_by ──> SPEC-AUTH-003
   │
   ├── fixed_by ──> HO-000142
   │
   ├── modifies ──> src/auth/login.py
   │
   └── verified_by ──> TEST-AUTH-019
```

The handoff can function as the entity that records a state transition.

Example:

```text
BUG-042
   │
   ▼
HO-000142
   │
   ├── DIFF-000931
   ├── SPEC-AUTH-003
   ├── TEST-AUTH-019
   └── HARNESS-IMPLEMENTER
```

The meta-harness can query these relationships before making decisions.

---

# 21. The handoff as a transition event

An important conceptual evolution is to treat the handoff not just as a document.

It can represent a **responsibility and state transition event**.

Example:

```text
IMPLEMENTATION
      │
      │ HO-000142
      ▼
REGRESSION TESTING
```

The handoff records:

- origin;
- destination;
- previous state;
- produced state;
- evidence;
- pending items.

Example:

```yaml
transition:
  from_harness: implementation
  to_harness: regression-testing

  previous_state: bug_confirmed
  resulting_state: fix_implemented
```

This brings the meta-harness closer to a state machine.

---

# 22. Meta-harness as a state machine

Reversa can structure the meta-harness as an evidence-driven state machine.

Example:

```text
BUG_IDENTIFIED
      │
      ▼
SPEC_LINKED
      │
      ▼
IMPLEMENTATION_REQUESTED
      │
      ▼
IMPLEMENTED
      │
      ▼
DIFF_VALIDATED
      │
      ▼
TESTED
      │
      ▼
AUDITED
      │
      ▼
CLOSED
```

The handoffs are responsible for proposing transitions.

The meta-harness validates the evidence before accepting the state change.

Example:

```yaml
requested_transition:
  from: IMPLEMENTATION_REQUESTED
  to: IMPLEMENTED
```

The meta-harness verifies:

```text
Does the diff exist?
Does the diff contain files?
Are the files related to the objective?
Does the handoff explain the changes?
Is there a reference to the SPEC?
Was the verification command executed?
```

Only after validation:

```yaml
transition:
  accepted: true
```

---

# 23. The meta-harness must not trust the agent's narrative

An important architectural rule:

> The meta-harness must not make decisions based solely on the textual response of the executing agent.

LLMs are language generation systems.

A declaration like:

```text
All tests passed.
```

Should not be automatically accepted as evidence.

The handoff can record the declaration.

The evidence must be collected separately.

Example:

```yaml
verification:
  claimed:
    tests_passed: true

  observed:
    command: pytest
    exit_code: 0
    tests_passed: 142
```

This separation is extremely important.

One can differentiate:

```text
CLAIM
```

and

```text
EVIDENCE
```

The meta-harness validates claims using evidence.

---

# 24. Claims and evidence

A possible structure:

```yaml
claims:
  - id: CLAIM-001
    statement: Login bug fixed.

  - id: CLAIM-002
    statement: Authentication tests passed.

evidence:
  - id: EVID-001
    type: diff
    supports:
      - CLAIM-001

  - id: EVID-002
    type: test_execution
    supports:
      - CLAIM-002
```

The meta-harness can identify claims without evidence.

Example:

```yaml
consistency_check:
  unsupported_claims:
    - CLAIM-003
```

Result:

```yaml
decision: NEEDS_VERIFICATION
```

This approach directly connects the meta-harness to Reversa's traceability concept.

---

# 25. Cross-Evidence Validation

The central function of the meta-harness can be defined as **cross-evidence validation**.

Inputs:

```text
OBJECTIVE
SPEC
BUG
HANDOFF
DIFF
TEST RESULT
REPOSITORY STATE
```

The meta-harness compares the relationships.

Example questions:

```text
Does the handoff declare the task was completed?
             │
             ▼
Does the diff exist?
             │
             ▼
Does the diff touch files related to the objective?
             │
             ▼
Were the related SPECs modified or respected?
             │
             ▼
Were the related tests executed?
             │
             ▼
Is there a regression risk?
             │
             ▼
Which harness should receive the next handoff?
```

---

# 26. Suggested specialized harnesses

Reversa's architecture can contain specialized harnesses.

## Implementation Harness

Responsible for implementing changes.

Input:

```text
objective
specs
bugs
constraints
```

Output:

```text
diff
handoff
```

## Diff Auditor Harness

Responsible for analyzing the scope of changes.

Questions:

- is the diff within scope?
- are there unexpected files?
- was there an undeclared structural change?
- does the diff contain suspicious changes?
- was there excessive removal?

## Spec Consistency Harness

Responsible for verifying consistency between code and specifications.

Questions:

- does the code still reflect the SPEC?
- does the change require a SPEC update?
- is there code without a related specification?

## Regression Harness

Responsible for defining and executing regression checks.

## Bug Traceability Harness

Responsible for relating:

```text
BUG
SPEC
CODE
DIFF
TEST
HANDOFF
```

## Handoff Auditor Harness

Responsible for verifying handoff quality.

Questions:

- is the objective clear?
- does the summary explain the changes?
- are there undocumented decisions?
- were the risks identified?
- are there pending items?
- is the next step verifiable?

---

# 27. Proposed flow for Reversa

A possible execution:

```text
USER GOAL
   │
   ▼
META-HARNESS
   │
   ├── identifies objective
   ├── consults SPECs
   ├── consults bugs
   ├── consults traceability
   │
   ▼
IMPLEMENTATION HARNESS
   │
   ├── implements
   ├── generates handoff
   │
   ▼
DIFF CAPTURE
   │
   ▼
META-HARNESS
   │
   ├── compares objective
   ├── compares handoff
   ├── compares diff
   ├── consults SPECs
   │
   ▼
DIFF AUDITOR
   │
   ▼
REGRESSION HARNESS
   │
   ▼
SPEC CONSISTENCY HARNESS
   │
   ▼
META-HARNESS
   │
   ├── accepts
   ├── rejects
   ├── requests correction
   └── delegates next step
```

---

# 28. Rule: no harness ends with "done"

A strong rule can be defined:

> No harness finishes an execution with just a completion indicator.

Every execution must produce a validatable handoff.

Invalid example:

```yaml
status: done
```

Minimum acceptable example:

```yaml
objective: BUG-042
status: implemented

summary:
  Password validation fixed.

diff_reference:
  base: abc123
  head: def456

verification:
  command: pytest tests/auth/test_login.py
  result: passed

unresolved_items: []

recommended_next_harness:
  regression-testing
```

---

# 29. Handoff as protocol

An important conclusion of this discussion is that Reversa can evolve from a simple reverse engineering tool for specifications to an architecture capable of defining a **work transfer protocol between harnesses**.

This protocol can establish:

- format;
- schema;
- required fields;
- evidence;
- transitions;
- acceptance criteria;
- rejection criteria;
- versioning.

Possible conceptual name:

```text
Harness Handoff Protocol
```

Or:

```text
Meta-Harness Handoff Protocol
```

Or:

```text
Agentic Software Handoff Protocol
```

A possibility directly associated with Reversa:

```text
Reversa Handoff Protocol
RHP
```

---

# 30. Architectural hypothesis

The central hypothesis can be formulated as follows:

> In agent-oriented software development, reliable work continuity depends on explicit mechanisms for state transfer and evidence validation.

The handoff transfers state.

The diff records change.

Tests produce evidence of behavior.

SPECs define the expected intent.

The meta-harness crosses this information and controls continuity.

Formally:

```text
INTENT
   +
HANDOFF
   +
DIFF
   +
VERIFICATION
   =
DECISION CONTEXT
```

The meta-harness operates on this context.

---

# 31. Central principle

The main conclusion of the conversation is:

> The handoff is the agent's declaration. The diff is the material evidence. Verification proves behavior. The SPEC represents the intent. The meta-harness is the mechanism that crosses this information and decides the continuation of development.

Another formulation:

> Diff shows what changed. Handoff explains what happened. Verification shows if it works. The SPEC says what should happen. The meta-harness compares all of this.

---

# 32. Direction for Reversa evolution

From this discussion, a line of evolution for Reversa would be:

1. define a formal handoff schema;
2. transform handoff into a first-class artifact;
3. automatically capture diff after executions;
4. relate diff to bugs and SPECs;
5. create handoff-diff validation;
6. separate claims from evidence;
7. introduce specialized harnesses;
8. model the meta-harness as a state machine;
9. use handoffs as transition events;
10. maintain a traceability matrix or graph between:
   - bugs;
   - SPECs;
   - code;
   - diffs;
   - tests;
   - handoffs;
   - decisions;
   - harnesses;
11. prevent completion without evidence;
12. allow continuity between:
   - Claude Code sessions;
   - Codex sessions;
   - different models;
   - different harnesses;
   - specialized agents.

---

# 33. Final vision

Reversa already has a motivation related to the reconstruction and maintenance of specifications from code.

With meta-harness, handoff, and diff, its function can expand.

Reversa can act as a **coordination, operational memory, and traceability layer for agentic development**.

In this model:

```text
SPEC defines intent.
BUG records deviation.
HARNESS executes.
DIFF records change.
HANDOFF records state and continuity.
TEST provides evidence.
META-HARNESS decides.
REVERSA maintains traceability.
```

The architecture stops depending on the temporary memory of an LLM session.

The state of development comes to exist in explicit, structured, and auditable artifacts.

The objective is not to make agents converse more.

The objective is to make agents **transfer work with sufficient evidence for another agent to continue reliably**.

This can be one of the conceptual foundations for the adoption of **meta-harness in Reversa**.
