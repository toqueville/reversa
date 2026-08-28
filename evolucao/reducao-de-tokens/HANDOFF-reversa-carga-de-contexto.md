# HANDOFF — Reversa context optimization

> **To:** another Claude Code session
> **Nature:** **optimization**, not refactoring. Reversa's behavior should remain **identical**.
> **Objective:** save user tokens by reducing the permanent context load of the 49 skills
> **Origin:** `mattpocock-skills x Reversa` report, 07/30/2026
> **Effort:** 1-2 h, almost entirely scriptable
> **Reversa author:** `sandeco` — is the user of this session themselves

---

## What the user asked for

Two **characteristics** of `mattpocock-skills`, named by the user:

| Characteristic | What it means |
|---|---|
| **Context economy** | *"The invocation axis is treated as an engineering decision, with measured and assumed cost"* |
| **Real portability between harnesses** | *"41 of 41 skills with dual mark (Claude + Codex), 0 mismatches"* |

Warning: **Notice what makes these characteristics, not one-time achievements:** *"engineering decision with measured cost"* and *"0 mismatches"* are properties that are **maintained** — not states that are reached once. Marking the 49 skills today delivers the state; without a written policy and without a verifier, Reversa will drift again on the next skill added.

That is why the execution has 8 steps, not 5: **steps 1-5** produce the state, **6-8** make it permanent. And there is a point where Reversa can **surpass** the reference — see Step 7.

---

## Warning: Rule governing this task

**Reversa working today is worth more than any token savings.**

This is a cost optimization, not a functionality improvement. If at any point there is doubt between "saves more" and "definitely does not break", **choose not to break**. An 85% savings that introduces an intermittent bug in the orchestrator is a loss, not a gain.

That is why section 4 executes in **8 steps, each with its own commit and the framework working at the end**. Do not skip steps or combine commits.

---

## TL;DR — what you gain

Reversa injects **~3,677 tokens into the context of every request**, before any work begins, because the 49 skills are model-invoked and each one keeps its `description` permanently loaded.

| | Today | After (Scenario B) |
|---|---:|---:|
| Skills occupying context | 49 | 8 |
| Injected characters | 14,708 | 2,336 |
| Permanent tokens | **~3,677** | **~584** |
| | | **-3,093 tokens (-85%)** |

**What this savings honestly means:**

- **Context window space** — 3,093 tokens returned to real work. This is the most durable gain and does not depend on cache. In a long analysis, it is space that stops being wasted.
- **Routing quality** — today the model chooses between 49 competing descriptions, many nearly identical to each other (13 `specialist` maintenance skills with similar phrasing). With 8, the choice becomes more precise. This qualitative gain is probably larger than the cost gain.
- **Token cost** — it is real, but partially mitigated by prompt caching: after the first request, a good portion becomes cache reads, cheaper than new input. **Do not promise the user a proportional savings on the bill.** The guaranteed gain is in window space and precision.

---

## Section 0 - READ BEFORE TOUCHING ANY FILE

### Pitfall 1 — `git branch` does NOT protect this work

The user asked for a branch for this rework. **Doing this the obvious way does not work**, and it is important to understand why before trying:

```
pocoyo-skills/  →  is a git repository
                   .claude/skills/  →  0 tracked files  (untracked)
                   .agents/skills/  →  0 tracked files  (untracked)
```

**Untracked files do not belong to any branch.** They survive `git checkout` intact. Creating a branch in `pocoyo-skills`, editing the skills, and then switching back to `main` **does not undo anything** — the changes remain there, and you lose rollback precisely on the task where rollback is the main safety mechanism.

Worse: the `origin` of this repository is **`https://github.com/mattpocock/skills.git`** — someone else's repository. It is not the place for Reversa's code.

The **solution is in section 1.** Do not improvise a branch here.

### Pitfall 2 — There are TWO copies of everything, and they are not links

```
pocoyo-skills/.claude/skills/   ← 49 skills, 108 files
pocoyo-skills/.agents/skills/   ← 49 skills, 108 files
```

**Independent** copies (different inodes), currently byte-for-byte identical (verified with `diff -rq`).

**Every change goes in both.** If you change only one, Reversa will behave differently depending on which engine loaded it — a nearly untraceable bug afterwards. Check at the end:

```bash
diff -rq pocoyo-skills/.claude/skills pocoyo-skills/.agents/skills   # must return EMPTY
```

### Pitfall 3 — Do not confuse what belongs to Reversa with what is legacy

`pocoyo-skills/` is a **third-party repository** (`mattpocock/skills`) that was the target of reverse engineering. Reversa is merely installed inside it.

| Path | Belongs to | Can modify? |
|---|---|---|
| `.claude/skills/reversa*` | Reversa installation, untracked | Yes, this is the target |
| `.agents/skills/reversa*` | Reversa installation, untracked | Yes, this is the target |
| `.agents/adr/`, `.agents/invocation.md`, `.agents/writing-docs.md` | **Legacy**, tracked | **NO** |
| `skills/`, `docs/`, `CLAUDE.md`, `README.md`, `package.json` | **Legacy**, tracked | **NO** |
| `_reversa_sdd/`, `.reversa/` | Extraction artifacts, completed | Out of scope |

Warning: `.agents/` has content from **both**: `.agents/skills/` belongs to Reversa; `.agents/adr/` and `.agents/invocation.md` are legacy and are versioned.

### Pitfall 4 — `git status` lies in this repository

167 files appear modified since 07/26, **before** any work. It is CRLF conversion from the Windows mount. A `git diff` shows `-node_modules` / `+node_modules` — identical text, just the `\r`.

- **Do not use `git status`/`git diff` from `pocoyo-skills`** to check your work.
- **The files have CRLF.** `sed -n '/^---$/,/^---$/p'` **does not match**, because the line is `---\r`. Every script needs to normalize (`.replace("\r\n","\n")`) and **restore CRLF when writing**. The section 4.3 script already does this.

### Pitfall 5 — `npx reversa update` undoes everything

Installed version: `1.2.56`, from the npm package `reversa`. **There is no Reversa source repository on this machine** — I searched.

Since the user is the Reversa author, the fix probably needs to go upstream to the source. The section 1 repository serves exactly as the patch to be applied there.

**Ask the user:** should this optimization go to the Reversa source repository? If yes, ask for the path. Do not run `npx reversa update` during the task.

---

## Section 1 - Git strategy — create a dedicated repository

As Pitfall 1 shows, a branch in `pocoyo-skills` does not give rollback. The solution provides **real rollback, real diff, and a reusable patch for the source**:

```bash
cd /workspaces/CHUPA-CABRA
mkdir -p reversa-otimizacao && cd reversa-otimizacao

# the installation becomes a real repository
cp -r ../pocoyo-skills/.claude/skills claude-skills
cp -r ../pocoyo-skills/.agents/skills agents-skills

git init
git add -A
git commit -m "baseline: Reversa 1.2.56 as installed, without changes"
git tag baseline

git switch -c otimizacao/carga-de-contexto
```

From here you have what the user asked for: **a branch where the rework happens**, with `baseline` untouched for comparison and rollback.

**At the end**, after all section 6 verifications pass, sync back:

```bash
cd /workspaces/CHUPA-CABRA/reversa-otimizacao
rsync -a --delete claude-skills/ ../pocoyo-skills/.claude/skills/
rsync -a --delete agents-skills/ ../pocoyo-skills/.agents/skills/
```

**Rollback at any time**, even after syncing:

```bash
cd /workspaces/CHUPA-CABRA/reversa-otimizacao
git checkout baseline -- .
rsync -a --delete claude-skills/ ../pocoyo-skills/.claude/skills/
rsync -a --delete agents-skills/ ../pocoyo-skills/.agents/skills/
```

> Note: The git identity is already configured (`sandeco` / `physialtda@gmail.com`), no need to ask.

---

## Section 2 - The problem

`description` exists for the **model** to discover the skill on its own. A skill that the human invokes by typing `/name` does not need to be discovered — it was already chosen. That is what `disable-model-invocation: true` is for: the skill remains reachable by the human and disappears from the model's context.

mattpocock applies it to **24 of 41** skills. Reversa, to **0 of 49**.

### Correction to an error in the source report

The PDF, section 7, states that *"most reversa-* agents never need to be discovered by anyone... they are called by the orchestrator"* and proposes marking "the other ~43".

**This is wrong.** The measurement shows that **34 of 49 declare a `/name` command that the user types** in the `description` itself. Only 15 are exclusively for the orchestrator.

But the practical conclusion becomes **stronger**:

- The **34 that the user types** are the canonical case of user-invoked — it is literally what the mark exists for.
- The **15 from the orchestrator** also do not need `description`: what reaches them is another skill reading the file, not the model choosing (see section 4.2).

Use the numbers from this document, not those from the PDF.

---

## Section 3 - The decision

| | Model-invoked skills | Chars | Tokens | Savings |
|---|---:|---:|---:|---:|
| Today | 49 | 14,708 | ~3,677 | — |
| **Scenario A** — only `reversa` | 1 | 291 | ~72 | -99% |
| **Scenario B** — 8 orchestrators | 8 | 2,336 | ~584 | **-85%** |

**Scenario B keeps model-invoked:** `reversa`, `reversa-new`, `reversa-forward`, `reversa-migrate`, `reversa-autonomous`, `reversa-agents-help`, `reversa-debugger`, `reversa-refactor`.

**I recommend B, and the reason is the rule at the top of this document.** The `CLAUDE.md` declares that Reversa activates *"when the user types `/reversa` **or the word `reversa` alone in a message**"*. Recognizing natural language requires the model to see the skill. Scenario A saves 512 more tokens and **changes the product behavior** — the user loses natural language routing to the flows. That is regression disguised as optimization.

**Confirm A or B with the user before executing.**

---

## Section 4 - Execution — 8 steps, framework working at each one

> **Steps 1-5** produce the right *state*. **Steps 6-8** transform that state into a **permanent characteristic** — without them, Reversa will drift again on the next skill someone adds.

### 4.1 - Step 1 — baseline and functional test BEFORE

Create the repository from section 1. Then, **before changing anything**, establish that the framework works today and record how:

- In a clean session, type `/reversa` — it needs to load and read `.reversa/state.json`
- Type `/reversa-agents-help` — the catalog needs to appear
- Note what happened

Without this "before", you have no way to know if a problem in the "after" was caused by you.

Warning: `.reversa/state.json` has `phase: concluido` — the extraction was completed. To test the Scout path without dirtying that state, back up `.reversa/` or point Reversa to another directory.

```bash
git commit --allow-empty -m "step 1: baseline validated, framework working"
```

### 4.2 - Step 2 — fix invocation sites (BEFORE the marks)

**This is the step that can break the framework, and that is why it comes first and alone.**

A user-invoked skill **cannot be invoked by another skill** — without `description`, nothing besides the human reaches it. This collides with the orchestrator's mode of operation.

**The good news:** the alternative path **already exists** in 3 of the 4 sites — read the `SKILL.md` and execute in the current context, which works regardless of any mark. The fix is to **invert the precedence**: what is currently the fallback becomes the primary path.

**The 4 sites, mapped by grep:**

| # | File | Line | Has reading fallback? |
|---|---|---|---|
| 1 | `reversa/SKILL.md` | 26 | Yes |
| 2 | `reversa-migrate/SKILL.md` | 102 | Yes |
| 3 | `reversa-new/SKILL.md` | 195 | Yes |
| 4 | `reversa/references/step-01-first-run.md` | 63 | **NO** |
| 5 | `reversa-autonomous/SKILL.md` | 98 | Indirect — *"exactly as `reversa` does"* |

**Site 4 is the one that breaks.** Current text: *"After confirmation, activate the `reversa-scout` skill."* — it commands activation by name, without alternative, and `reversa-scout` is precisely one of those that will become user-invoked.

Suggested wording for site 1 (apply the same pattern to the others):

> `2. Read `.agents/skills/reversa-[agent]/SKILL.md` in full and execute the instructions in the current context. (If your engine supports direct activation by name and the agent is accessible, activating it directly is equivalent.)`

For site 4:

> `After confirmation, read `.agents/skills/reversa-scout/SKILL.md` in full and execute in the current context.`

**At the end of this step, the framework needs to be working exactly as before** — no marks have been added yet, only the order of precedence changed. Repeat the Step 1 test.

```bash
git commit -am "step 2: direct SKILL.md reading as primary path in the 4 invocation sites"
```

### 4.3 - Step 3 — mark ONE skill and validate end to end

**Do not mark all 41 at once.** Mark **one** and prove the approach works.

Choose `reversa-scout`: it is the most critical of the user-invoked skills (it is the first the orchestrator calls, and it is the target of site 4). If it works with this one, it works with all.

Add **one line** to the frontmatter, in both trees:

```yaml
---
name: reversa-scout
description: Maps the legacy project surface — ...
disable-model-invocation: true          # ← just this
license: MIT
...
---
```

**KEEP the `description`.** Do not remove it. I verified the 24 user-invoked from mattpocock: **all 24 keep the `description`** and only add the flag. The `description` continues serving the command listing that the human sees; it is the **flag** that removes the skill from the model's context.

**Test now, in a new session:**
- Can `/reversa` reach the Scout and execute it? (this exercises site 4)
- Does `/reversa-scout` typed directly still work?

**If either fails, STOP.** Revert with `git checkout baseline -- .` and report to the user. Do not proceed to Step 4 with doubt.

```bash
git commit -am "step 3: reversa-scout as user-invoked, validated end to end"
```

### 4.4 - Step 4 — mark the remaining 40

Script validated in sandbox: **82 files changed** (41 skills x 2 trees), insertion in the right place, control skills intact, idempotent.

```python
#!/usr/bin/env python3
import re, pathlib

BASE = pathlib.Path("/workspaces/CHUPA-CABRA/reversa-otimizacao")
ARVORES = [BASE/"claude-skills", BASE/"agents-skills"]

# Scenario B — remain model-invoked
MANTER = {
    "reversa", "reversa-new", "reversa-forward", "reversa-migrate",
    "reversa-autonomous", "reversa-agents-help", "reversa-debugger", "reversa-refactor",
}

alterados = 0
for arvore in ARVORES:
    for p in sorted(arvore.glob("*/SKILL.md")):
        if p.parent.name in MANTER:
            continue
        bruto = p.read_text(encoding="utf-8")
        crlf = "\r\n" in bruto
        t = bruto.replace("\r\n", "\n")
        if re.search(r"^disable-model-invocation:", t, re.M):
            continue                                   # idempotent
        m = re.match(r"^---\n(.*?)\n---\n", t, re.S)
        if not m:
            print(f"  !! missing frontmatter: {p}"); continue
        fm = m.group(1)
        novo_fm, n = re.subn(
            r"(^description:\s*(?:.+?)(?=\n[a-zA-Z_-]+:|\Z))",
            r"\1\ndisable-model-invocation: true",
            fm, count=1, flags=re.S | re.M)
        if n != 1:
            print(f"  !! description not found: {p}"); continue
        t = t[:m.start(1)] + novo_fm + t[m.end(1):]
        if crlf:
            t = t.replace("\n", "\r\n")
        p.write_text(t, encoding="utf-8")
        alterados += 1

print(f"{alterados} files changed (expected: 82)")
```

Warning: **If the number is not 82, stop and investigate.** (80 if Step 3 already marked the Scout — check your case before concluding there was an error.)

```bash
git diff --stat            # review before committing
git commit -am "step 4: 41 skills as user-invoked (scenario B)"
```

### 4.5 - Step 5 — the Codex mark

Every Reversa skill declares `compatibility: Claude Code, Codex, Cursor, Gemini CLI...`, but there are **0 `agents/openai.yaml` files in 49 skills**. The invocation policy does not cross over to Codex.

This **gains urgency with Step 4**: without the `openai.yaml`, the context savings only applies in Claude Code — in Codex all 49 remain implicitly invocable.

mattpocock solves this with a conceptual axis and **two physical marks in lockstep**: 41 of 41 skills marked in both formats, **zero mismatches**.

| State | Claude Code (`SKILL.md`) | Codex (`agents/openai.yaml`) |
|---|---|---|
| Model-invoked | absence of flag | only the `interface:` block |
| User-invoked | `disable-model-invocation: true` | `interface:` **+** `policy.allow_implicit_invocation: false` |

Create `<skill>/agents/openai.yaml` in **both** trees.

**For the 41 user-invoked:**
```yaml
interface:
  display_name: "Reversa Scout"
  short_description: "Maps project structure, stack, and entry points"
policy:
  allow_implicit_invocation: false
```

**For the 8 model-invoked:**
```yaml
interface:
  display_name: "Reversa"
  short_description: "Orchestrates legacy system analysis"
```

`display_name` in Title Case. `short_description` short — in mattpocock's examples, 25 to 45 characters. You can derive from the first sentence of the `description`, but **review manually**: Reversa's start with long phrases that do not fit well here.

```bash
git commit -am "step 5: agents/openai.yaml in 49 skills, marks in lockstep"
```

---

### 4.6 - Step 6 — rewrite the `description` of user-invoked skills

Warning: **This is not cosmetic and not optional.** It is half of one of the two requested characteristics.

mattpocock's policy (`.agents/invocation.md`) defines that the **content** of the `description` changes according to which side of the axis:

> - **User-invoked** — the `description` is **human-facing**: a one-line summary read by a person browsing the slash-commands. **Strip trigger lists** (*"Use when the user says..."*).
> - **Model-invoked** — the `description` is **model-facing** and keeps the rich trigger phrasing (*"Use when the user wants..., mentions..., asks for..."*) so that auto-invocation fires.

Reversa's `description` fields average **300 chars** because they are full of model triggers: *"Use when the user types /X, 'do Y' or 'start Z'"*. In a user-invoked skill these triggers serve no purpose — nobody reads them, the model no longer sees the skill, and the human reads noise.

Reference from mattpocock's user-invoked: ~50 chars (`"A relentless interview to sharpen a plan or design."`).

**Rule:** in the 41 user-invoked, reduce the `description` to a human one-line summary, without triggers. In the 8 model-invoked, **do not touch** — there the triggers are the mechanism.

The Step 7 verifier rejects a user-invoked `description` that still contains `Use quando`, `Use when`, or `digitar "/`.

```bash
git commit -am "step 6: user-invoked description rewritten as human summary"
```

### 4.7 - Step 7 — the verifier (this is where Reversa surpasses mattpocock)

**This step is what transforms the two changes into permanent characteristics.**

Without it, Reversa has the right *state* today and drifts again on the next skill someone adds. With it, the invocation axis becomes an executable invariant.

**mattpocock does not have this, and pays the price.** He declares 12 structural invariants and **verifies none** — the only CI is the release CI. Two are broken right now, and both are exactly the type a thirty-line check would catch. **Copy the declaration, not the absence of executor.**

Proof that the verifier does real work: run against mattpocock's 41 skills, it confirms **0 mismatches** — and still finds **2 deviations** of `description` hygiene that their policy prescribes and nobody applied (`personal/edit-article`, `deprecated/ubiquitous-language`, both in non-promoted buckets).

**The script already exists and is validated:** `/workspaces/CHUPA-CABRA/verify-invocation.py`

It checks five things:

| # | Check |
|---|---|
| 1 | Every skill has `agents/openai.yaml` |
| 2 | `openai.yaml` has `interface.display_name` and `interface.short_description` |
| 3 | **Lockstep:** `disable-model-invocation: true` iff `allow_implicit_invocation: false` — user-invoked in both marks or in neither |
| 4 | `description` of user-invoked does not contain model trigger |
| 5 | The two trees (`.claude/skills`, `.agents/skills`) are identical |

Exits with code **1** if there is any violation, so it serves as a gate.

```bash
# current state (before work): 98 violations, all for missing openai.yaml
python3 /workspaces/CHUPA-CABRA/verify-invocation.py claude-skills agents-skills

# target at the end: RESULT: APPROVED
```

**Copy the verifier into Reversa** — it needs to travel with the framework, not remain loose on this machine. Suggestion: `scripts/verify-invocation.py` in the source repository, referenced in the Step 8 document.

```bash
git commit -am "step 7: invocation axis verifier, with lockstep gate"
```

### 4.8 - Step 8 — the written policy

The last piece of the characteristic: a document that declares the rule, so the next skill is born correct instead of being fixed later.

The model to follow is `pocoyo-skills/.agents/invocation.md` — **read it before writing**. It is short and solves exactly this problem. Adapt for Reversa covering:

- **The axis** — every skill is user-invoked or model-invoked, with no third state.
- **The two marks** — `disable-model-invocation: true` (Claude Code) **and** `policy.allow_implicit_invocation: false` (Codex). *"A skill is user-invoked in both harnesses or in neither."*
- **The decision test** — *would the model have a reason to reach this skill on its own?* In Reversa the answer is yes only for the 8 flow orchestrators; the phase agents are reached by the orchestrator reading the `SKILL.md`.
- **The `description` rule** — human-facing and short in user-invoked; model-facing and with triggers in model-invoked.
- **The reach rule** — a user-invoked skill cannot be invoked by another skill; that is why the orchestrator **reads the `SKILL.md`** instead of activating by name (Step 2).
- **The cost, measured** — record the numbers: 14,708 to 2,336 chars, ~3,677 to ~584 tokens. This is what makes the axis *"an engineering decision with measured and assumed cost"* instead of a tacit convention.
- **The executor** — point to `verify-invocation.py` and say when to run it.

```bash
git commit -am "step 8: invocation axis policy, with measured cost and executor"
```

---

## Section 6 - Verification, definition of "broken", and rollback

### 6.1 - The verifier — the main check

```bash
cd /workspaces/CHUPA-CABRA/reversa-otimizacao
python3 /workspaces/CHUPA-CABRA/verify-invocation.py claude-skills agents-skills
```

**Target:** `RESULT: APPROVED` and exit code 0.

It covers lockstep, presence of `openai.yaml`, UI metadata, `description` hygiene, and equality between the two trees. For reference, the same script run **today**, before work, reports **98 violations** (49 per tree, all for missing `openai.yaml`) — use this to confirm you are measuring the right thing.

### 6.2 - Complementary checks

```bash
cd /workspaces/CHUPA-CABRA/reversa-otimizacao

# count of marks  → 41 and 41
grep -rl "disable-model-invocation: true" claude-skills --include=SKILL.md | wc -l
find claude-skills -name openai.yaml | xargs grep -l "allow_implicit_invocation: false" | wc -l

# openai.yaml in all  → 49
find claude-skills -name openai.yaml | wc -l

# nothing from legacy was touched  → EMPTY
cd /workspaces/CHUPA-CABRA/pocoyo-skills
find . -newermt "2026-07-30" -type f \
  -not -path "./.claude/*" -not -path "./.agents/skills/*" -not -path "./.git/*"
```

### 6.2 - The savings, measured

```python
import re, pathlib
tot = n = 0
for p in pathlib.Path("claude-skills").rglob("SKILL.md"):
    t = p.read_text(encoding="utf-8").replace("\r\n", "\n")
    fm = re.match(r"^---\n(.*?)\n---", t, re.S).group(1)
    if re.search(r"^disable-model-invocation:\s*true", fm, re.M):
        continue
    d = re.search(r"^description:\s*(.+?)(?=\n\w+:|\Z)", fm, re.S | re.M)
    tot += len(" ".join(d.group(1).split())); n += 1
print(f"{n} skills - {tot:,} chars - ~{tot//4:,} tokens")
# BEFORE:  49 skills - 14,708 chars - ~3,677 tokens
# TARGET B:  8 skills -  2,336 chars -   ~584 tokens
```

### 6.3 - Functional test — mandatory, do not skip

No check above proves that Reversa works. In a new session, after the `rsync` from section 1:

| # | Test | Expected |
|---|---|---|
| 1 | Type `/reversa` | Orchestrator loads and reads `.reversa/state.json` |
| 2 | Write just the word `reversa` in a message | Activates (only in Scenario B — this is what A sacrifices) |
| 3 | `/reversa` reaching the Scout | Executes via direct reading (exercises site 4) |
| 4 | `/reversa-scout` typed directly | Works |
| 5 | `/reversa-agents-help` | Catalog appears |
| 6 | `/reversa-forward` | Flow loads |

### 6.4 - Definition of "broken" — any of these aborts delivery

- The orchestrator cannot reach a user-invoked agent
- A `/reversa-*` command that worked stopped working
- The two trees diverged
- Any legacy file was modified
- Scenario B was chosen and the word `reversa` alone stopped activating

**Upon encountering any of these: stop, rollback (section 1), report to user.** Do not try to fix on top.

---

## Section 7 - What NOT to do

- **Do not create a branch in `pocoyo-skills`.** It protects nothing (Pitfall 1) and the `origin` is someone else's repository.
- **Do not remove the `description`.** mattpocock keeps all 24; it is the flag that cuts the cost.
- **Do not modify `skills/`, `docs/`, `CLAUDE.md`, `README.md`, `.agents/adr/`, `.agents/invocation.md`, `.agents/writing-docs.md`** — all legacy.
- **Do not touch `_reversa_sdd/` or `.reversa/`.**
- **Do not trust `git status` from `pocoyo-skills`** (Pitfall 4).
- **Do not apply only to one of the two trees.**
- **Do not run `npx reversa update`** during the task.
- **Do not group the 8 steps into a single commit.** The value is in having a return point per step.
- **Do not change behavior "as a bonus".** If you notice something else to improve, note it and report — do not include in this task.
- **Do not copy an invariant without an executor.** If it is tempting to declare these rules in a Reversa governance document: mattpocock declares 12 invariants, verifies none, and **two are broken right now**. If you declare, declare with a verifier.

---

## Section 8 - Reference facts

Measured on 07/30/2026, reproducible.

| Fact | Value |
|---|---|
| Reversa skills | 49 |
| Files per tree | 108 |
| Independent trees | 2 (`.claude/skills`, `.agents/skills`) |
| Skills with `disable-model-invocation` | **0** |
| `agents/openai.yaml` files | **0** |
| Skills with `/name` in `description` | 34 |
| Orchestrator-only skills | 15 |
| Skill-to-skill invocation sites | 4 (+1 indirect) |
| Summed `description` | 14,708 chars - ~3,677 tokens |
| Average per `description` | 300 chars |
| Average lines per `SKILL.md` | 133 (vs 69 from mattpocock) |
| Largest `SKILL.md` | `reversa-new`, 328 lines |
| Installed version | 1.2.56 |
| Reversa source on machine | **does not exist** |
| Git identity | `sandeco` / `physialtda@gmail.com` (configured) |

**Pattern to copy:** `pocoyo-skills/skills/` (mattpocock's 41 skills). Good user-invoked examples: `skills/productivity/grill-me/` (7 lines), `skills/engineering/ask-matt/`, `skills/engineering/wayfinder/`. The axis rationale is in `skills/productivity/writing-great-skills/GLOSSARY.md`, entries **Model-Invoked**, **User-Invoked**, **Description**, **Context Load**, **Cognitive Load**.

**Source analysis:** `/workspaces/CHUPA-CABRA/relatorio-mattpocock-vs-reversa.pdf` — section 7, suggestions 1 and 2. **See the section 2 correction before following the PDF.**

---

## Section 9 - Execution order

1. Read section 0 entirely.
2. **Confirm with the user:** Scenario **A or B**? (recommended B) - does the optimization go upstream to Reversa source? (Pitfall 5)
3. Set up the dedicated repository and branch (section 1).
4. **Step 1** — functional test BEFORE, recorded (section 4.1).
5. **Step 2** — fix the 4 invocation sites. Test. Commit. (section 4.2)
6. **Step 3** — mark only `reversa-scout`. Test end to end. Commit. (section 4.3)
7. **Step 4** — mark the remaining 40. Check 82 (or 80). Commit. (section 4.4)
8. **Step 5** — create the 98 `openai.yaml`. Commit. (section 4.5)

> Up to here the **state** is correct. The next three steps are what makes it a **characteristic**.

9. **Step 6** — rewrite the `description` of the 41 user-invoked. Commit. (section 4.6)
10. **Step 7** — run and embed the verifier. Commit. (section 4.7)
11. **Step 8** — write the invocation axis policy. Commit. (section 4.8)
12. Verifier section 6.1 -> `APPROVED`. Checks section 6.2. Functional test section 6.3.
13. `rsync` back to `pocoyo-skills` (section 1).
14. Report: load before/after, files touched, tests executed, verifier output, and whether it needs to go upstream.

---
---

# PART 2 — Structural improvements (later, separate task)

> Warning: **Do not mix with Part 1.** Part 1 is cost optimization, with controlled risk and rollback per step. These 5 are organization improvements, without urgency. Do them only **after** Part 1 is validated and synchronized. Each one is its own branch.
>
> Approved by the user on 07/30/2026.

## M1 - Prune the large skills

Reversa's `SKILL.md` averages **133 lines**, versus 69 from mattpocock. Text that is too long the model reads poorly — the middle part is what it ignores most.

The 8 largest:

| Skill | Lines |
|---|---:|
| `reversa-new` | 328 |
| `reversa-screen-translator` | 278 |
| `reversa-spec-sdd` | 277 |
| `reversa-migrate` | 272 |
| `reversa-reconstructor` | 242 |
| `reversa-forward` | 231 |
| `reversa-requirements` | 216 |
| `reversa-designer` | 216 |

**What to do:** move reference blocks (formats, examples, long tables) to `<skill>/references/`, leaving only the flow and a prose pointer in `SKILL.md`. Reversa **already does this** in 17 skills — it is applying the house pattern to those that were left behind.

Warning: Only the `SKILL.md` of **model-invoked** skills costs permanent context. In user-invoked, the pruning is for reading quality, not for tokens.

## M2 - Maturity buckets

The 49 agents are all at the same level, all implicitly ready. There is nowhere to put a draft or a retired one.

**What to do:** separate into folders by maturity, and install only the main one. mattpocock's model: `engineering/` + `productivity/` (go), `in-progress/` (draft, does not go), `deprecated/` (retired, kept as history, does not go).

Gain: you can write a new agent inside the repository without it reaching the user, and retire one without deleting its history.

## M3 - Record the refusals

A folder with what the project decided **not** to do, with the argument and the request that originated the discussion. mattpocock has 3 documents in `.out-of-scope/`.

Prevents re-discussing the same request every quarter, and allows responding with a page instead of a conversation. The value is not in the refusal, it is in the preserved argument.

## M4 - Reversa vocabulary glossary

Proprietary terms — **unit, spec, gap, phase, checkpoint, doc_level, granularity, independent agent, confidence scale** — today live scattered between the orchestrator's `SKILL.md`, the `references/`, and the `config.toml`.

With 49 agents written over time, it is what prevents two of them from using different words for the same thing.

**Model:** `pocoyo-skills/skills/productivity/writing-great-skills/GLOSSARY.md` — opinionated definition and an `_Avoid_:` line with rejected terms.

## M5 - Declared invariants — with verifier

An invariant is a rule of "these things must always be in agreement". Reversa already has several, implicit. The known ones:

| # | Invariant | State on 07/30/2026 |
|---|---|---|
| 1 | Every agent in `config.toml [agents] installed` has a folder in `.claude/skills/` | Intact (49 = 49) |
| 2 | `.claude/skills/` and `.agents/skills/` are identical | Intact |
| 3 | Every skill has both invocation marks in lockstep | Broken — this is Part 1 |
| 4 | `.reversa/version` matches the npm package version | Not verified |

**The rule governing this improvement:** declare **only** what you will verify by script.

mattpocock declared 12 invariants and checks none. Two are broken right now — and one of them violates a rule he himself published in an ADR (*"bump both together on release"*). A list without an executor is decoration that ages silently.

The `verify-invocation.py` already covers #2 and #3. Extend it to the others, instead of creating a new document without a script.
