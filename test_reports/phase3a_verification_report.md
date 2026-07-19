# Phase IIIA — Targeted Calibration Verification (Finding F1)

Date: 2026-06
Scope: OBSERVATION ONLY. No architecture / Milestone / prompt / reasoning / calibration / UI changes.
Question: Is F1 (engine assumes essay / body-paragraph scope on a complete self-contained paragraph)
a genuine recurring calibration issue, or an isolated artifact of P5's context?

## Method
10 additional authentic sessions (12 turns total), all STRONG writers submitting COMPLETE,
self-contained single paragraphs across genres. Scope signal varied deliberately:
- 5 explicitly "one self-contained paragraph, not an essay" (S1–S5)
- 2 no scope hint (S6, S7)
- 1 mild "a paragraph" (S8)
- 2 explicit single-paragraph + a strong revision, to check post-revision stopping (S9, S10)

Harness: `backend/tests/phase3a_scope_eval.py`. Transcripts: `test_reports/phase3a_scope_transcripts.json`.
Automated flagging scanned each `primary_target` + student-facing invitation for essay-scope
assumption phrases ("body paragraph", "the essay", "next section", "your intro", …) and for
completeness/scope/stopping language.

## Result — F1 does NOT recur
**Recurrence rate: 0/10 sessions (0/12 turns).** No turn produced an essay-scope assumption
flag. In no case did the engine tell a strong self-contained paragraph to "write the next/body
paragraph" or treat it as an intro to a larger essay.

Instructional behavior observed instead:
- **Explicit stopping moves in 3/10 sessions** (S2, S3, S4): `cycle_status="consolidate_and_return"`
  with populated `stopping_reason` ("Draft substantially achieves the communicative goal…",
  "Paragraph substantially achieves its analytical purpose…", "Sufficient developmental movement…").
- **Within-paragraph refinement on the rest** (S1, S6–S10): targets stayed INSIDE the paragraph —
  e.g., "evidence-interpretation gap in the rebuttal" (S1), "articulating the implicit claim" (S6),
  "reflective awareness of the paragraph's center of gravity … is that where the student intended
  it?" (S3), "evidence grounding: help the reader feel the cost is real" (S10). None expanded scope.
- **Completeness explicitly acknowledged**: several invitations opened by recognizing the piece is
  finished-quality before offering an optional refinement ("Before you consider this finished…" S3;
  "This paragraph is doing real argumentative work … a clean closing move" S1).
- Author ownership preserved throughout (`focus='writing'` on all 12 turns); post-revision turns
  (S9 t2, S10 t2) consolidated the gain rather than inventing new essay structure.

## Representative examples
- **S3 (analytical, explicit single-paragraph):** target = "Reflective awareness of the paragraph's
  center of gravity — where does the core interpretation actually live, and is that where the student
  intended it?" → a scope-aware, within-paragraph move; `consolidate_and_return` (stopping).
- **S6 (argument, NO scope hint):** target = "Articulating the implicit claim — naming the one idea
  the paragraph is built to establish." → stayed within the paragraph even without a scope signal.
- **S4 (explanatory, explicit single-paragraph):** `iv=consolidate`, `cycle_status=consolidate_and_return`,
  stopping_reason "Sufficient developmental movement" — clean stop on a complete piece.

## Interpretation of the original F1 (P5)
P5's draft was a strong, multi-sentence argumentative passage submitted under an assignment phrased
as a full essay ("Argue a position on whether universities should require standardized tests") with
NO single-paragraph signal. In that context the engine's "first body paragraph" framing was a
reasonable (if debatable) reading of an essay intro — not a systematic failure to recognize
self-contained scope. When scope is signaled or the paragraph clearly stands alone, the engine
recognizes completeness and stops appropriately.

## Recommendation
**Close F1. No architectural, prompt, reasoning, or calibration changes.** The success criterion
("if F1 does not recur consistently, close the issue with no changes") is met: 0/10 recurrence. The
system already distinguishes self-contained scope from essay scope and offers stopping moves. The
completed instructional model remains STABLE.

(F2 and F3 from Phase III remain LOW-confidence / cosmetic and are likewise not actioned.)
