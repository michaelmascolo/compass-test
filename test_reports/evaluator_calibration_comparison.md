# Evaluator Calibration — Comparison Report

- **Baseline run (old evaluator):** `2598c428-3a60-408b-9acd-313d319262f7`
- **Calibrated run (new evaluator):** `85624a68-ddda-4692-abbd-d927dffcf3d7`
- **Date:** 2026-07-20
- **What changed:** ONLY the evaluator (`EVAL_SYSTEM_MESSAGE` + `_eval_prompt` in `server.py`) — rewritten to judge Compass by its own instructional philosophy (principles P1–P10). The instructional engine, prompts, and the 32 test cases are **byte-for-byte unchanged**. Both runs execute the same production engine; differences below are almost entirely the evaluator's judgment (with some LLM run-to-run variance in the engine's wording).

## Headline

| | Pass | Partial (ambiguous) | Fail | Pass rate |
|---|---|---|---|---|
| Baseline (old) | 23 | 8 | 1 | 71.9% |
| **Calibrated (new)** | **24** | **8** | **0** | **75.0%** |

The single hard FAIL (TC21) is eliminated, confirming the architect's earlier meta-finding that it was an **evaluator over-reach**, not an engine defect. Pass rate is a modest headline move (+3.1 pts), but the *composition* changed substantially: 4 cases improved and 3 different cases were newly flagged, so the calibration is doing real work rather than uniformly loosening.

## 1. Changes in pass/fail outcomes

**Improved — evaluator no longer flags (4):**

| Case | Old → New | Why the old flag was unfair (Compass-fidelity) |
|---|---|---|
| **TC03** No thesis | partial → pass | Old evaluator called the fill-in stance starters "near-copyable templates." New evaluator (P2): sentence starters that leave the student to generate the position are **scaffolding, not coauthoring**. |
| **TC21** Unclear pronoun ref | **fail → pass** | Old evaluator read "try rewriting the sentence so a reader can follow" as directing a rewrite. New evaluator (P2): a generic revision **prompt** that returns the work to the student is not coauthoring. |
| **TC28** Student succeeds | partial → pass | Old evaluator wanted more consolidation before advancing. New evaluator (P8/P9): Turn 2 **did** consolidate the thesis principle and advanced on the same objective via guided action — an acceptable implementation. |
| **TC32** Reflective piece | partial → pass | Old evaluator treated the reader-orientation question as tilting toward argument. New evaluator (P5/P6): honoring communicative purpose while engaging the student in guided action is legitimate; reader context is a real gap. |

**Newly flagged — calibrated evaluator now marks partial (3):**

| Case | Old → New | New concern (verbatim principle) |
|---|---|---|
| **TC06** Adequate thesis | pass → partial | **P8**: Compass calls the thesis "strong/arguable" but never **restates the transferable principle** (a thesis makes a specific, contestable claim that drives the argument) before advancing. Praise ≠ consolidation. |
| **TC13** Effective topic sentence | pass → partial | **P8**: "You have a strong topic sentence" but does not articulate *why* it works (names a device, links it to a dynamic, stakes an interpretive claim) — the transfer-oriented consolidation step is absent. |
| **TC14** Poor organization | pass → partial | **P3/P4**: teacher purpose is *whole-essay organization*; Compass spent the turn on **thesis formation**, a target shift away from the stated sequencing problem. |

**Unchanged (25):** 20 stable passes + 5 stable partials (below).

## 2. Cases that remain ambiguous (partial in BOTH runs) — 5

TC07, TC18, TC29, TC30, TC31. Under the calibrated evaluator these now cluster around **two genuine, principle-grounded concerns**:

- **P8 consolidation gap** (TC07, TC18, TC30, TC31): Compass praises the success but stops short of restating the transferable rule.
- **P7 restraint / invented deficiency on competent work** (TC07, TC31): on strong/nuanced theses Compass still probes ("what position do you want the reader to accept?", "what could someone push back on?"), implying the claim is unfinished when it is not.
- **P2 authorship (TC29, this run only):** in this run's Turn 3, Compass supplied a *complete copyable thesis* — "Students should choose their own books because they read more when they're interested." The evaluator correctly flagged this as a coauthoring **violation** (though it graded it `partial` rather than `fail` — see §4).

## 3. Recurring evaluator disagreements (old vs calibrated)

Seven cases changed verdict; the disagreements fall into two clean, repeating patterns:

**A. Old evaluator over-applied a generic anti-coauthoring / anti-support reflex (now corrected).**
The old grader penalized *any* structural support — sentence starters (TC03), revision prompts (TC21), audience/reader moves in reflection (TC32) — as if support itself compromised authorship. The calibrated evaluator, per **P2/P6/P9**, treats these as scaffolding or acceptable alternatives and passes them. This resolved the lone hard FAIL and 3 partials.

**B. Calibrated evaluator strictly enforces P8 "consolidate by restating the principle."**
This is the single biggest new source of disagreement: **6 of the non-pass cases** are driven by the `consolidation_and_alternatives` criterion, almost always the same finding — *"acknowledged/praised the success but did not restate the underlying transferable principle."* Where the old evaluator accepted praise-then-advance, the new one requires an explicit principle restatement.

Classification tally across all calibrated non-pass flags: **`consolidation_and_alternatives` ×6, `developmentally_appropriate` ×3, `authorship_preserved` ×1** — and every flag was classified as a `violation` (none as stylistic preference), i.e. the calibrated evaluator no longer fails Compass for mere style, but when it does flag, it asserts a principle breach.

## 4. Recurring ENGINE weaknesses remaining after evaluator calibration

With the grader now fair to Compass's philosophy, the residual partials point at **genuine engine behaviors** to address in the (still-deferred) engine phase, in priority order:

1. **W-A — Consolidation-by-principle is missing (dominant, 6 cases: TC06, TC13, TC18, TC30, TC31, TC07).** On success the engine praises ("that's strong") but does not *restate the transferable rule the student just applied*. This is the highest-frequency, most consistent weakness and the clearest single lever (P8).
2. **W-B — Under-firing restraint on strong/nuanced work (TC07, TC31; also TC14 target-shift).** The engine still probes competent theses as if unfinished, edging toward inventing a deficiency (P7).
3. **W-C — Occasional authorship slip under repeated scaffolding (TC29, this run).** When a student stalls across turns, the engine escalated to supplying a **complete copyable thesis** — a real P2 breach. Low frequency but high severity.
4. **W-D — Teacher-purpose adherence on organization (TC14).** When the teacher names whole-essay organization, the engine chose thesis formation instead of engaging sequencing.

## 5. Note on evaluator residue (for the architect)

The calibration is sound but two second-order observations remain:
- **Severity mapping on P2:** TC29's copyable-thesis slip was classified `violation` yet graded `partial`, not `fail`. If supplying finished student content is a hard boundary, the evaluator should escalate that specific pattern to `fail`. (Candidate for a small future evaluator tweak — flagged, not changed.)
- **P8 strictness:** enforcing "restate the principle" turns many *good* turns into partials. This is defensible (it is a real Compass principle and a real engine gap), but the architect should confirm P8 should down-grade an otherwise-correct turn to `partial` vs. merely annotate it.

## Export files (all under `/app/test_reports/`)

| File | Contents |
|---|---|
| `baseline_run_2598c428.{md,json}` | Old-evaluator run (23/8/1) |
| `calibrated_run_85624a68.{md,json}` | New-evaluator run (24/8/0) |
| `evaluator_calibration_comparison.md` | This report |
| `baseline_enhanced_review_2598c428.md` | Per-case architect dossier (prior task) |
