# [Unit Name], Implementation Tasks

> Template for the `tasks.md` file. Focuses on an executable sequence of tasks to reimplement the unit from the legacy system, with traceability to the original code.

## Prerequisites
- [ ] Unit dependencies listed in `design.md` are available
- [ ] Database schema/migrations are compatible (if applicable)
- [ ] Required environment variables / configs are documented

## Tasks

> Each task references the legacy file from which the behavior was extracted.

- [ ] T-01, [Task description]
  - Legacy source: `path/file.ext:line`
  - Definition of done: [how to validate]
  - Confidence: 🟢 / 🟡 / 🔴

- [ ] T-02, [Task description]
  - Legacy source: `path/file.ext:line`
  - Definition of done: [how to validate]
  - Confidence: 🟢 / 🟡 / 🔴

## Test Tasks

- [ ] TT-01, Test the happy path of the main flow (see `requirements.md`, Acceptance Criteria)
- [ ] TT-02, Test the main error case
- [ ] TT-03, [Other relevant scenarios]

## Data Migration Tasks (if applicable)

- [ ] TM-01, [Data migration X, with reference to the legacy schema]

## Suggested Order
1. [Which tasks should be done first and why]
2. [Blockers between tasks]

## Pending Gaps (🔴)
[List here the decisions that depend on human validation before implementation]
