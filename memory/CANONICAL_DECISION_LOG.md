# Compass — Canonical Decision Log

Adopted decisions governing the instructional engine, evaluator, benchmark suite, and beta strategy. Newest at top.

---

## ADOPTED — 2026-07-20 · Expanded-suite generalization audit & beta posture

1. **Benchmark suite expanded 32 → 66 cases** to test whether the instructional architecture *generalizes* across a broad range of writing situations (genres, writing elements, learner states, proficiency levels), rather than to optimize performance on the original 32.
2. **Further benchmark expansion is DEFERRED until after the public beta.** The current 66-case suite is the frozen benchmark for the beta period.
3. **Purpose of the Expanded Suite v1 Baseline run is to identify launch-blocking weaknesses**, not to pursue perfect benchmark performance. Result: 58/8/0 (87.9%); 93.8% on the original 32 and 82.4% on the 34 new cases; **zero failures; no launch-blocking (Class A) issues.**
4. **Beta readiness is determined by instructional integrity and first-use reliability** — the anti-coauthoring/authorship boundary holding, safe and on-purpose instruction, and reliable first-use behavior — **not** by a requirement that every benchmark case pass. Under this criterion Compass is judged **beta-ready**.
5. **Engine and evaluator remain FROZEN** pending explicit approval. At most **one focused engine-refinement cycle** is permitted during beta prep unless a serious authorship, safety, or reliability problem is found (none was). Proposed (awaiting approval): R1 consolidation-by-general-principle, R2 honor explicit teacher-specified target, optional R3 AI-paste authorship prompt.

## ADOPTED — 2026-07-20 · Evaluator calibrated to Compass fidelity, then frozen
- Evaluator rewritten to judge Compass by its own philosophy (principles P1–P10: scaffolding≠coauthoring, respect competent performance, consolidate-by-principle, communicative-purpose-first, evidence-based, etc.). After calibration the evaluator is **frozen**; it will not be modified unless a later engine analysis demonstrates it is *demonstrably inconsistent* with Compass principles.

## ADOPTED — 2026-07-20 · Engine refinement cycle W-A→W-D (evaluator held constant)
- Engine improved via SYSTEM_MESSAGE-only refinements: W-A consolidation-by-principle, W-B restraint on competent performance, W-C no copyable content, W-D honor teacher purpose + developmental profile. Result on the 32-case suite: 75.0% → 90.6%, 0 fails. Deltas attributable to engine only (evaluator frozen).

---

# Benchmark Framework (canonical)

- **Suite:** `backend/test_cases/instructional_test_cases.json`, 66 cases (TC01–TC32 original essay-centric; TC33–TC66 diversity expansion). Frozen for beta.
- **Case schema:** id, name, level, assignment, pedagogical_purpose, current_writing_task, initial_draft, responses[], initial_profile[], expected_issues[], expected_primary_target, avoid_behaviors[].
- **Harness (developer-only, `?tests`):** runs each case through the REAL production engine (STAGE-A retrieval → networks → one-target → governed instruction → anti-coauthoring → developmental memory), then grades the actual decisions with a SEPARATE frozen LLM evaluator. Runs persist in Mongo `test_runs`; JSON/Markdown export; labels + rename; Compare-Two-Runs.
- **Verdict scale:** pass / partial (genuine developmental concern) / fail (hard Compass violation: coauthoring, >1 target, invented deficiency on competent work, overriding explicit genre constraint, performing the writing).
- **Grouped reporting rule (external, applied at report time — cases NOT modified):** genre = communicative purpose; writing element = primary instructional object; student state = defining learner condition (else "typical developing writer"); proficiency = `level` normalized to Middle/early-secondary (grades 7–9), High school (10–12), College, Adult/Professional. Categories with n<3 are directional only.
- **Change control:** benchmark cases are not modified during or immediately after a run; no per-case optimization to inflate score.

# Beta Strategy (canonical)

- **Launch gate:** instructional integrity (authorship boundary intact, safe/on-purpose instruction) + first-use reliability. NOT universal benchmark passing.
- **Weakness classification for launch:** A = launch-blocking (undermines trust, student authorship, instructional safety, or basic first-use); B = important but not launch-blocking (document + address post-beta or in the single permitted refinement round); C = edge case (may remain in beta if disclosed internally).
- **Current posture:** No Class A issues. Class B: W1 consolidation-by-principle, W2 target precision vs. teacher purpose, W3a AI-paste authorship surfacing. Class C: W3b parenthetical steering.
- **Refinement budget for beta:** ≤1 focused engine-refinement cycle unless a serious authorship/safety/reliability problem emerges. Every refinement must be re-benchmarked (full 66-case run) and compared against `fd0dec0c` (Expanded Suite v1 Baseline) via Compare-Two-Runs to confirm gains without regressions.
