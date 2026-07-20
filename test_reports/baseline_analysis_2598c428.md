# Instructional Engine — Untouched Baseline Analysis

- **Run ID:** `2598c428-3a60-408b-9acd-313d319262f7`
- **Date:** 2026-07-20
- **Scope:** All 32 canonical instructional test cases (TC01–TC32), each run through the REAL production engine (STAGE-A retrieval → instructional networks → one-target selection → governed instruction → anti-coauthoring → developmental memory), graded by a separate `claude-sonnet-4-6` evaluator.
- **Engine state:** UNCHANGED. This is a baseline; no engine/prompt revisions were made.

## Headline results

| Metric | Value |
|---|---|
| Overall pass rate | **71.9%** |
| Passed | **23** / 32 |
| Failed | **1** (TC21) |
| Ambiguous (partial) | **8** (TC03, TC07, TC18, TC28, TC29, TC30, TC31, TC32) |
| Errors | 0 |

- **Passed (23):** TC01, TC02, TC04, TC05, TC06, TC08, TC09, TC10, TC11, TC12, TC13, TC14, TC15, TC16, TC17, TC19, TC20, TC22, TC23, TC24, TC25, TC26, TC27

## Hard-constraint violations

Only **one** hard-constraint violation across all 32 cases:

- **TC21 (Unclear pronoun reference) — REWRITE-DIRECTION violation.** The tutor explicitly told the student to *"rewrite the sentence"* and prescribed the strategy (*substituting names for pronouns*), directing a rewrite rather than teaching the concept and leaving the revision approach to the student. This is the app's core anti-coauthoring boundary and is the single most serious finding.

No violations of the one-target rule, no `intervention_focus` other than `writing`, no invented evidence/arguments.

**Soft (non-hard) authorship edges** — flagged `partial`, not violations, but same family as TC21:
- TC03 & TC29 supplied near-copyable **sentence-starter templates** ("Homework should be limited because…", "Students should / should not…") while teaching thesis — borderline doing the structural work for the student.

## Failures grouped by evaluation criterion

| Criterion | Fail | Partial | Cases |
|---|---|---|---|
| `constraint_compliance` | 1 | 4 | FAIL: TC21 · PARTIAL: TC03, TC07, TC18, TC29 |
| `target_alignment` | 0 | 6 | PARTIAL: TC07, TC18, TC28, TC30, TC31, TC32 |
| `one_target_and_authorship` | 0 | 1 | PARTIAL: TC21 |

`target_alignment` (6 partials) is the largest weak surface — the engine chose a defensible but non-optimal instructional target.

## Failures grouped by Instructional Object

| Instructional Object | Non-pass cases |
|---|---|
| **Thesis / Central Claim** (all variants) | TC03, TC07, TC18, TC28, TC29, TC31 → **6 of 9** non-pass |
| Sentence | TC21 (FAIL) |
| Purpose | TC30 |
| Hook / Opening Move | TC32 |

The **Thesis object dominates the weak surface**: two-thirds of all non-pass cases fired on thesis/central-claim reasoning.

## Recurring patterns (systematic weaknesses)

**W1 — Under-firing restraint on strong / intentionally-open writing (highest leverage).**
On strong or deliberately-open drafts the engine *invents a problem* instead of recognizing "this is strong → consolidate / move forward."
- TC07: treated a sharp, intentionally-open strong thesis as needing narrowing ("better in what ways, for whom?").
- TC18: implied an effective intro needed pre-explanation of its own distinction.
- TC31: treated a legitimate nuanced both-sides thesis as a problem to "resolve."
This is the F1 / over-teaching family resurfacing at the thesis level. 3 clear cases + adjacent to TC30.

**W2 — Anti-coauthoring micro-leak at the "how to phrase it" level.**
The boundary holds conceptually (no invented content, focus always `writing`) but leaks when scaffolding *form*: sentence-starter templates (TC03, TC29) and — the hard failure — an explicit "rewrite the sentence" directive (TC21). The engine knows *not* to supply the idea, but occasionally supplies the *sentence shape*.

**W3 — Consolidation-before-advance not reliably triggered on success.**
TC28: after the student produced a good thesis, the engine immediately advanced to a new structural distinction (thesis vs. body) instead of consolidating the gain first, missing the "consolidate after success" requirement.

**W4 — Developmental-memory / genre priority sometimes overridden by a generic reader/purpose target.**
- TC30: ignored the documented profile (thesis already `consolidating`; evidence/explanation is the growth edge) and pivoted to audience awareness.
- TC32: nudged a reflective piece toward reader orientation/explanation rather than deepening meaning/significance.

## Priority for future work (NOT yet implemented)

1. **W1 restraint calibration** on strong/adequate/nuanced drafts (thesis especially) — biggest cluster, most user-visible as "over-teaching".
2. **W2 authorship boundary tightening** — no "rewrite the sentence" directives, no fill-in-the-blank sentence starters; teach the distinction, let the student choose the phrasing. (Includes the only hard failure, TC21.)
3. **W3 consolidation-on-success** trigger.
4. **W4 honor developmental profile / genre** when selecting the primary target.

## Export files (all under `/app/test_reports/`)

| File | Contents |
|---|---|
| `baseline_run_2598c428.md` | Complete run — all 32 cases, readable Markdown |
| `baseline_run_2598c428.json` | Complete structured JSON record (full run doc) |
| `baseline_failures_ambiguous_2598c428.md` | Failed (1) + ambiguous (8) cases only |
| `baseline_analysis_2598c428.md` | This analysis |
