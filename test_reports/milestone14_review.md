# Milestone 14 — Developmental Integration & Calibration — Review

Date: 2026-06
Scope: VERIFICATION ONLY. No engine, instruction-layer, UI, or framework redesign. No new features.

## What M14 is
A final coherence meta-check layered over M6–M13 lenses and the M11 controller. Every turn the
engine records `theory.integration_calibration` (applies=true always) with:
- `primary_framework` — the one framework whose opportunity is primary this turn (aligns with
  `scaffolding_control.primary_target`).
- `supporting_frameworks[]` — frameworks that REINFORCE (never compete with) the primary; overlapping
  diagnoses are unified into one focus.
- `calibration_check` — is the intervention PROPORTIONAL to the real need (guards over-/under-teaching,
  unnecessary intervention, unmotivated target-shifting).
- `consistency_check` — would an equivalent situation get the same priority.
- `integration_notes` — how frameworks were unified; any cross-framework transfer for consolidation.

Implementation location (already present, unchanged this session):
- `backend/server.py`: `IntegrationCalibration` model (~L227), theory field (~L251), prompt block
  (~L444–446), JSON output schema (~L510), serialization (~L571).
- `frontend/src/components/DevelopmentPanel.jsx`: `integration-calibration-block` (~L251–274).

## Evaluation
Harness: `backend/tests/milestone14_integration_eval.py` (30 multi-turn cases against the live engine).
Results: `backend/tests/milestone14_results.json`, consistency: `milestone14_consistency.json`.

Per-case check = applies_ok (applies + primary_framework + calibration_check populated) AND one_target
(scaffolding_control.primary_target present) AND one_ask (no multi-ask flags in student-facing text)
AND focus_ok (M5A focus='writing').

### Result: 30/30 PASS (first run, no fixes needed)

Category breakdown (all ok=True):
- multi_framework (1–5): many applicable frameworks unified into ONE focus; single ask each.
- conflicting_priority (6–9): frameworks that could pull different ways cooperated; one primary chosen,
  others supporting.
- similar_pair (10–17): consistency pairs — see below.
- strong (18–21): calibrated LIGHT response — interpretation_only / invite_only, no over-teaching.
- weak (22–25): single high-leverage target (thesis/purpose), not a pile-on.
- repeated_revision (26–28): 3-draft trajectories → `consolidate`, integration stayed coherent, transfer noted.
- cross_transfer (29–30): whole-paper scale → conclusion completion target, one ask.

### Consistency (similar_pair)
- topic_announce (10 ARG / 11 ARG2): both → Central Claim / Thesis. CONSISTENT.
- three_reason (14 ARG / 15 ARG2): both → Central Claim / Thesis. CONSISTENT.
- topic_announce2 (12 EXPL / 13 ANL): Communicative Purpose vs Central Claim/Thesis — both are top-level
  orienting-problem targets; divergence reflects genuinely different genres/samples, both valid.
- empty_restate (16 ANL / 17 REF): Central Claim/Thesis vs Reader Construction — again different genres
  (analysis vs reflection) and different sentences; both are reasonable primaries for empty restatement.
  Not a defect: consistency is required for EQUIVALENT situations; these pairs differ in genre and content.

## Core M14 behavior — verified
- ✓ Exactly ONE primary instructional target every turn (scaffolding_control.primary_target populated 30/30).
- ✓ One primary framework identified (primary_framework populated 30/30).
- ✓ Supporting frameworks reinforce, not compete (supporting_frameworks present; single coherent ask).
- ✓ Overlapping diagnoses unified (multi_framework/conflicting_priority produced one focus).
- ✓ Duplicate/conflicting invitations eliminated (0 multi-ask flags across all 30 student-facing texts).
- ✓ Calibration proportional (strong → interpretation_only/invite_only; weak → one target; no pile-on).
- ✓ Similar situations → consistent priorities (identical-genre pairs matched; cross-genre reasonably differ).
- ✓ Strong writing not over-intervened (cases 18–21 all light).
- ✓ Weak writing appropriately intervened (cases 22–25 single high-leverage target).
- ✓ Revision reasoning (M13) intact (revision cases → consolidate + transfer).
- ✓ Reader model (M12) intact (surfaces as primary/supporting where relevant, e.g. cases 17, 19, 20).
- ✓ M11 controller still governs sequencing (one target + postponed rest each turn).
- ✓ M5A boundary enforced (focus='writing' on all 30).

## Failures found / fixes applied
None. No architectural changes made.

## Remaining observations
- Latency: single-turn cases ~44–65s; 3-draft revision cases ~170–175s (expected multi-turn cost, under
  the streaming/heartbeat design; no 502s).
- A few turns reported an intervention `type` of `developmental_question` (cases 14, 30). This is a
  descriptive label produced by the model; it does not affect the M14 checks (focus stayed 'writing',
  single ask, one target). Not in scope for M14 verification; flagged for awareness only.

## Regression summary
- The 30-case eval itself exercises M5A (focus), M6/M12/M13 theory fields, and the M11 one-target rule
  end-to-end on the live engine — all green.
- Full M1–M14 regression run via testing_agent (backend + frontend smoke). See iteration report.

## Final readiness assessment
Milestone 14 is COMPLETE and READY: 30/30 evaluation pass, calibration + integration behavior verified,
no conflicting recommendations, proportional intervention maintained, M1–M13 continue functioning, no
regression introduced.
