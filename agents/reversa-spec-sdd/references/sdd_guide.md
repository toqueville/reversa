# Methodology Guide — Spec-Driven Development

## What is SDD?

Spec-Driven Development is the practice of writing a detailed behavioral specification **before** writing any code. The spec answers **what** the system should do — not **how** to implement it.

Do not confuse with:
- **TDD** (Test-Driven Development): writes tests before code — complementary to SDD
- **DDD** (Domain-Driven Design): architectural pattern — independent of SDD
- **BDD** (Behavior-Driven Development): focuses on behaviors with Gherkin — a subset of SDD

---

## Fundamental Principles

### 1. Behavior, not Implementation

The spec describes observable behavior, not internal implementation.

❌ Bad: "The system should use Redis for session caching"
✅ Good: "The system should keep the user's session active for 30 days on devices where they checked 'remember me'"

The implementation (Redis, JWT, database) is a technical decision for the implementer — not for the spec.

### 2. Ambiguity = Future Bug

Every ambiguity in the spec becomes a bug, an alignment meeting, or a PR discussion in the future. Make ambiguities explicit with `⚠️ OPEN:` — a visible open item is better than a silent assumption.

### 3. Non-Goals are as important as Goals

"What we won't do" prevents scope creep, aligns expectations, and accelerates decisions. A feature without non-goals tends to grow indefinitely.

### 4. The Spec is a Living Contract

The spec changes as understanding evolves — and that is healthy. What matters is that changes are recorded (Decision Log) and that all stakeholders are aligned with the current version.

### 5. LLM-Readiness

A good modern spec should be readable by LLMs that will help implement. This means:
- Numbered requirements (traceable IDs)
- Explicit behaviors, not implicit ones
- Documented edge cases (LLMs do not guess edge cases)
- Business context included (the "why" helps make good implementation decisions)

---

## The SDD Cycle

```
Idea/Problem
      ↓
  Interview  ←──────────────────────┐
      ↓                              │
  Spec Draft                         │
      ↓                              │
  Evaluation (Score)                 │
      ↓                              │
  Score < 80? ──── Yes ──── Identify gaps
      ↓ No
  Spec Approved
      ↓
  Implementation
      ↓
  Spec vs. Code (final validation)
```

---

## When to Write the Spec

| Feature size | Recommendation |
|-------------------|--------------|
| Bug fix | Does not need a spec |
| Small improvement (< 1 day dev) | Minimal spec: goals + main requirements |
| New feature (1–5 days) | Complete spec, but concise |
| Complex feature (> 5 days) | Complete spec + review by 2+ people |
| New system | Architecture spec + per-feature specs |

---

## Requirement Priorities (MoSCoW)

| Priority | Meaning | Decision if it doesn't fit the deadline |
|-----------|-------------|-------------------------------|
| **Must** | Mandatory — cannot launch without it | Blocks the launch |
| **Should** | Important — but there is a workaround | Defers to next version |
| **Could** | Nice-to-have | Discards if necessary |
| **Won't** | Consciously out of scope | Documents as Non-Goal |

---

## Common Antipatterns

### "Spec like a big-company PRD"
50-page specs that nobody reads. Prefer concise specs that cover the essentials with clarity.

### "Spec as a list of technical tasks"
"Create users table, add POST /auth endpoint, integrate with OAuth..." — this is an implementation plan, not a spec. The spec talks about behavior.

### "Verbal / Slack spec"
Decisions made in conversation without records are lost and generate conflicts. Every spec must exist as a written document.

### "Spec that never changes"
Frozen specs that don't reflect the reality of what was implemented. The spec should be updated when the implementation intentionally diverges.

### "Silent Open Questions"
Assuming answers for unanswered questions. Always use `⚠️ OPEN:` and resolve before implementing.

---

## SDD Vocabulary

| Term | Definition |
|-------|-----------|
| **Spec** | Document that describes the expected behavior of a feature |
| **RF** | Functional Requirement — what the system should do |
| **RNF** | Non-Functional Requirement — how the system should behave (performance, security...) |
| **Goal** | Objective that the feature must achieve |
| **Non-Goal** | What is explicitly out of scope |
| **Edge Case** | Boundary or non-obvious case that the system must handle correctly |
| **Happy Path** | The main and most common usage flow |
| **Acceptance Criterion** | Verifiable condition that defines when a requirement is implemented |
| **Open Question** | Unresolved question that may impact the design |
| **Decision Log** | Record of important decisions and why they were made |
