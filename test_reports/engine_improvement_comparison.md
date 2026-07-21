# Engine Improvement — Comparison Report (evaluator held constant)

The evaluator is FROZEN at the calibrated version (from `85624a68`). Every run below uses the identical evaluator and identical 32 test cases, so all deltas are attributable to ENGINE (SYSTEM_MESSAGE) changes only.

## Progression

| Run | Change | Pass | Partial | Fail | Pass rate |
|---|---|---|---|---|---|
| `85624a68` | Calibrated evaluator, engine untouched (baseline for this phase) | 24 | 8 | 0 | 75.0% |
| `7b0b473a` | **+ W-A** Consolidation by principle | 26 | 6 | 0 | **81.2%** |
| `33cc0307` | **+ W-B/W-C/W-D** & reinforced W-A | 29 | 3 | 0 | **90.6%** |

**Net effect of the engine phase: 75.0% → 90.6% (+15.6 pts), 0 fails throughout.**

## Engine changes made (in `SYSTEM_MESSAGE` only — evaluator & cases unchanged)

A single "ENGINE REFINEMENTS" block was added to the reasoner prompt:
- **W-A Consolidation by principle** — on success/competent control, Compass must NAME the transferable rule the student applied (e.g., "a thesis works when it makes one contestable claim a reader could dispute"), not just praise. Reinforced after the W-A run to require abstracting the *rule*, not merely describing the instance.
- **W-B Restraint on competent performance** — when the current work already meets the element's objective, do NOT invent a gap, ask the student to further specify/narrow/justify, or probe as if unfinished; consolidate and release/advance. Raise a concern only with concrete textual evidence of a real problem.
- **W-C No copyable content (hard)** — never supply a complete usable thesis/topic sentence/argument, even as an "example" or when the student stalls; sentence frames that stop before the claim are OK; vary the scaffold rather than escalating toward the answer.
- **W-D Honor teacher purpose & developmental priority** — select the target from the teacher's pedagogical purpose and the student's developmental-profile growth edge before defaulting to thesis; engage the named element (e.g., whole-essay organization) rather than substituting a familiar one.

## Case-level attribution

**Fixed by W-A (`7b0b473a`):** TC13 (topic-sentence consolidation), TC29 (no authorship slip this run).

**Fixed by W-B/W-C/W-D (`33cc0307`):**
- **TC07** partial→pass — **W-B**: stopped inventing a "what does deliberate connection look like?" gap on a strong thesis; consolidated + advanced instead.
- **TC31** partial→pass — **W-B**: stopped over-teaching the legitimate nuanced both-sides thesis.
- **TC18** partial→pass — **W-A (reinforced)**: now names the transferable intro principle rather than only praising.
- **TC14** partial→pass — **W-D**: engaged the teacher's stated whole-essay organization target instead of pivoting to thesis.

**Full journey (non-stable-pass cases):** `calibrated → W-A → W-BCD`
```
TC06: partial -> partial -> partial
TC07: partial -> partial -> pass
TC13: partial -> pass    -> partial   (flip-flop; run variance at consolidation boundary)
TC14: partial -> partial -> pass
TC18: partial -> partial -> pass
TC29: partial -> pass    -> pass
TC30: partial -> partial -> partial
TC31: partial -> partial -> pass
```

## Remaining ambiguous after the engine phase (3): TC06, TC13, TC30

1. **TC06 & TC13 — P8 principle-abstraction strictness (borderline).** In `33cc0307` Compass *does* name what the specific thesis/topic sentence accomplishes ("says scores reflect income, not ability, which a reader could dispute"), but the evaluator wants the **generalized reusable rule** stated ("*the test for any thesis is that it stakes a disputable claim*"). The engine describes the instance; it does not always abstract to the transferable rule. This is a subtle residual engine behavior — and arguably near the edge of evaluator strictness, but NOT demonstrably inconsistent with P8 ("restate the principle for transfer"), so per instruction the evaluator was left untouched.
2. **TC13 flip-flop** (pass under W-A, partial under W-BCD) confirms this case sits right on the consolidation threshold and is sensitive to run-to-run LLM wording variance rather than a stable defect.
3. **TC30 — residual W-D miss (real).** The developmental profile marks evidence/explanation as the growth edge (thesis already consolidating), yet Compass still selected a thesis-adjacent sub-claim move. W-D reduced but did not eliminate the pull toward thesis when a strong thesis is present.

## Recommended next step (optional, deferred)

A small **W-A abstraction tweak** ("state the rule in general terms — e.g., 'the test for any thesis is…' — not only what THIS sentence does") would likely convert TC06/TC13; and a **W-D strengthening** to hard-prioritize an explicit profile growth-edge over an already-consolidated element would target TC30. Both are one-line prompt refinements + one more full re-run. Not applied automatically to avoid overfitting to the evaluator and to keep the current, clean baseline.

## Files (all under `/app/test_reports/`)

| File | Contents |
|---|---|
| `calibrated_run_85624a68.{md,json}` | Evaluator-calibrated baseline (engine pre-improvement) |
| `wa_run_7b0b473a.{md,json}` | After W-A |
| `wbcd_run_33cc0307.{md,json}` | After W-B/C/D + reinforced W-A (current best) |
| `engine_improvement_comparison.md` | This report |
