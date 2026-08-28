# Improvements to Reversa to make /reversa-debugger more effective

> Actionable post-mortem written from the `mira-studio-full` case, where
> `/reversa-debugger` closed 8 bugs as "fixed" and still delivered a
> recording that never worked in the browser. The goal here is not the case, it is the
> process: what to change in the framework so that this does not repeat for any feature.

## TL;DR

The debugger did not fail by diagnosing poorly. It failed at the **closure gate**: it accepted
"synthetic green" as proof of fix for a feature that can only be proven in a
real browser, and let a critical inspection finding be closed even after
it said "do not close". The improvements below harden exactly these two points.

---

## The root cause, in one sentence

**Nothing in the debugger loop touched the reality of the feature a single time.** The recording is
100% browser runtime (`getDisplayMedia`, Element Capture, WebCodecs, muxer). The
harness ran in a sandbox without a browser. Without reality in the loop, every test degenerated
into regex on source code, and "green" came to prove that the code *contains* lines,
not that the feature *works*. From there everything cascades down:

1. Test becomes regex on source, not behavior.
2. Closure policy `local-software` accepts this green as `fixed`.
3. The wrong oracle ships without contestation.
4. The fail-closed relocates the symptom (black video becomes "recording dies on start") and still passes green.
5. The fine-tooth inspection diagnoses correctly, but the gate closes the bug over it.

---

## Improvement 1: "browser-only" verification class in the closure policy

**Problem.** The `local-software` policy closes a bug with "green regression + verdict". For
browser runtime features (screen capture, media, WebCodecs, WebGPU, canvas,
audio), green tests in Node prove nothing. In this case, the CGU3 `DONE.md` downgraded the
real proof to "recommended confirmation, does not block closure". That is exactly the hole.

**Change.** Create a closure class `browser-runtime` that **requires a real artifact**
before accepting `fixed`. For recording this would be the MP4 1920x1080 with the `.fmt-frame`,
or the `window.__miraLastRecordingDiagnostics` captured from a real attempt. As long as the
artifact does not exist, the maximum state of the bug is `awaiting-human-verification`, never `fixed`.

**Practical rule.** At intake, the registrar classifies the feature. If it depends on an API that
the harness cannot execute (explicit list: media, capture, GPU, native permissions,
File System Access), the bug is born marked `verification: browser-runtime` and inherits the stricter
closure. The fixer can propose the diff, but what closes it is the binary evidence from the user.

## Improvement 2: critical inspection finding BLOCKS closure

**Problem.** The fine-tooth inspection on 07/17 nailed F-conformity-01 (critical) and wrote, in
full words, "the spec verdict of CGU3 should not be accepted while the oracle does not
follow RF-05". The next day `/reversa-debugger-fix` closed CGU3 anyway. The
diagnosis was correct and the gate simply overrode it.

**Change.** A finding with `suspected_severity: critical` and `promoted_to` pointing to an
active bug becomes a **hard block**: that bug cannot receive `DONE.md` while the finding
is not explicitly resolved or downgraded, with recorded justification. The closure
must reference the `finding_id` and state why it no longer applies. Silence does not close.

## Improvement 3: prohibit "string presence test" as proof of behavior

**Problem.** `recording-health.test.cjs` and `recording-oracle.test.cjs` read the `.js` as
text and matched regex. They proved that the fail-closed code *exists*, not that the recording
works. The golden frame-by-frame suite (RF-13 from the spec itself) was never implemented, and
it was precisely because of this that the regression that disables recording shipped "green".

**Change.** The fixer must label each test it writes as `static` (regex/AST on
source) or `behavioral` (executes the path and observes the effect). A behavior bug
**cannot** be closed with only `static` tests. If the spec defines a behavioral suite
(like RF-13 golden) and it does not exist, that is a blocker for `fixed`, not an
"observation about coverage" that goes in the report footer.

## Improvement 4: fail-closed that changes the symptom is not a fix

**Problem.** CGU3 made the pipeline reject `encoded === 0`. This transformed "black video"
into "the recording dies right after starting". The defect was relocated, not resolved, and even
so it was closed. This is what "killed the feature".

**Change.** When the fix is fail-closed (aborts instead of producing bad output),
the fixer is required to answer in writing: "what is the happy path that now produces
CORRECT output, and where is the proof of it?". Fail-closed without a proven happy path is damage
containment, and the bug stays `mitigated`, never `fixed`. These are different states and the user needs to see
the difference.

## Improvement 5: caution with the "outdated-spec" verdict

**Honest observation.** In this case, the CGU3 addendum (`outdated-spec`) was
technically correct: it replaced "getSettings must be 16:9" with "read frames until one arrives in
the session's aspect ratio", reasoning well from the API documentation. In other words, the mechanism
of versioned and immutable addenda worked as designed. **But** the feature remained broken
after it, because the new logic also never ran in Chrome.

**Risk to watch.** `outdated-spec` is the most dangerous verdict of the debugger, because it
makes the "error" disappear on paper: it rewrites the ruler until the code passes. Here it was used with
integrity, but the process needs a brake for when it is not. Suggestion: every
`outdated-spec` verdict on a `browser-runtime` feature only takes effect **after** the real evidence that
Improvement 1 requires. Changing the spec and closing the bug in the same step, without touching reality, is the
combination that produces "perfect document, dead feature".

## Improvement 6: integration gate above the per-bug gate

**Problem.** Each of the 8 bugs was closed and locked in isolation (`DONE.md` = read-only
folder). The MILD fix brought `WIDE`/`discardMismatch`; the CGU3 fix brought the
blocking oracle. Each one "ready" locally, while the entire recording never worked
end to end. Nobody asked "does the whole feature record?".

**Change.** When N bugs share the same feature (same aggregating context), the last one to
close triggers an **integration gate**: a single end-to-end test of the feature (here:
"press record, stop, and a correct MP4 comes out"). No `DONE.md` from the group is definitive while
this gate has not had a real passing run recorded. Bugs closed in sequence do not sum up to a
feature that works.

## Improvement 7: intake should capture "has this ever worked?"

**Problem.** The `mira-record.js` from the deck was the file inherited from 9:16, patched with flags
(`__miraFormat`, `__miraElemCapture`). The two paths clashed within the same file, and the
"surgical change" directive pushed the debugger toward conditional-on-top-of-conditional instead
of the clean fork (`mira-record-16x9.js` dedicated) that actually solved it in the separate folder.

**Change.** At intake, a mandatory question: "has this feature ever worked in this deck,
or is it being built now?". If the answer is "never worked", the problem is not a
*bug* (regression of something that was working), it is an *incomplete feature*, and the right path may be
rewrite/fork, not surgical patching. The debugger is good at fixing regressions; it should not
try to *finish building* a feature via successive surgical fixes.

---

## Why the separate folder worked (the underlying lesson)

The perfect version evolved with **you as the browser in the loop**: the `updates/` folder shows
live iteration against the real API, pressing record in Chrome on each pass. The feedback from the real
world replaced the synthetic green from the sandbox, and the separation into `mira-record-16x9.js` killed the
flag clash.

None of the improvements above tries to "put a browser inside reversa". The conclusion is simpler:
**when the truth of the feature only exists in the browser, the human is a non-optional part of the
gate.** The role of the framework is to stop hiding this behind synthetic green and to start requiring
the real evidence, loud and clear, before writing `fixed`.

## Summary of changes, in order of impact

1. Closure class `browser-runtime` that requires a real artifact before `fixed` (Improvement 1).
2. Critical inspection finding blocks bug closure (Improvement 2).
3. Tests labeled `static` vs `behavioral`; `static` does not close a behavior bug (Improvement 3).
4. Fail-closed without a proven happy path = `mitigated`, not `fixed` (Improvement 4).
5. `outdated-spec` on a browser-runtime feature only takes effect after real evidence (Improvement 5).
6. Feature integration gate above the per-bug gates (Improvement 6).
7. Intake distinguishes "regression" from "feature never worked" and avoids patching where forking is appropriate (Improvement 7).
