# Invocation axis policy

> Rule that governs how each Reversa skill is reached — by the human or by the model.
> Verified by `scripts/verify-invocation.py` (CI gate). Write the next skill already compliant.

## The axis

Every skill is **user-invoked** or **model-invoked** — there is no third state.

- **Model-invoked** — the model can reach it on its own, recognizing the user's intent in
  natural language. For this, the `description` is **permanently loaded in the context of every
  request**. It costs context even when the skill is not used.
- **User-invoked** — only reached when the human types `/name`, or when an orchestrator reads its
  `SKILL.md`. It is not loaded into the model's context. Marked with `disable-model-invocation: true`.

## The decision test

> *Would the model have a reason to reach this skill on its own, from a natural language sentence,
> without the user typing the command?*

In Reversa, the answer is **yes only for the 9 flow entry points**: the 8 orchestrators
(`role: orchestrator`) plus `reversa-agents-help`. All phase agents — Scout, Architect,
Reviewer, the `pricing-*`, the `debugger-*`, the `docs-*`, the refactor specialists and the
renderers — are reached by the **orchestrator reading their `SKILL.md`**, never by the model guessing.
Therefore, they are user-invoked.

**The 9 model-invoked:** `reversa`, `reversa-new`, `reversa-forward`, `reversa-migrate`,
`reversa-autonomous`, `reversa-refactor`, `reversa-debugger`, `reversa-docs`, `reversa-agents-help`.

## The two marks, in lockstep

A skill is user-invoked **in both harnesses or in neither**:

| State | Claude Code (`SKILL.md`) | Codex (`agents/openai.yaml`) |
| --- | --- | --- |
| Model-invoked | absence of the flag | only the `interface:` block |
| User-invoked | `disable-model-invocation: true` | `interface:` **+** `policy.allow_implicit_invocation: false` |

The verifier rejects any mismatch between the two marks.

## The reachability rule

A user-invoked skill **cannot be invoked by another skill by name** — without a `description`, the
model cannot see it. That is why the orchestrator **reads the `SKILL.md`** of the sub-agent (sibling
folder, in the same skills directory) and executes the instructions in the current context, instead of
activating by name. When writing a new orchestrator, always use this read pattern.

## The `description` rule

- **User-invoked** — human-facing: a summary of what the skill does, plus usage hints in prose
  (*"Use when \<condition\>"*, *"Activation: /x (invoked by /y)"*, cycle phase). **No model trigger
  lists** — nothing like `Use with "/x", "phrase"`, `type "..."`, `Activate with /x, ...`,
  `ask "..."`. They serve no one (the human reads noise; the model no longer sees the skill).
- **Model-invoked** — model-facing: keeps the trigger-rich phrasing, because that is what fires
  auto-invocation. **Do not touch them.**

## The cost, measured (07/31/2026, v1.2.57)

The permanent context load from model-invoked `description`s:

| | Model-invoked skills | Chars | Tokens |
| --- | ---: | ---: | ---: |
| Before (all) | 65 | 19,948 | ~4,987 |
| After (Scenario B) | 9 | 2,336 | ~668 |
| | | | **−4,319 tokens (−86%)** |

This is what makes the axis an *"engineering decision with measured and assumed cost"* — not a tacit
convention. The savings come from context window and routing precision (the model chooses among 9
descriptions, not 65). In billing tokens, the gain is partially mitigated by prompt caching — do not
promise proportional savings on the bill.

## The executor

```bash
npm run verify
# or, separately:
python3 scripts/verify-invocation.py            # axis, lockstep, description hygiene
node   scripts/test-installer-transport.mjs     # marks survive the installer copy
```

Runs automatically in CI (`.github/workflows/verify-invocation.yml`) on every change to `agents/`.
Exits with code 1 on any violation. **When adding a skill, run `npm run verify` before
committing** — this is what prevents the axis from drifting with the next skill.
