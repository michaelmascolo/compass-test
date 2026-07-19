# Phase III — Authentic Instructional Testing & Calibration Report

Date: 2026-06
Scope: OBSERVATION ONLY. No instructional architecture, engine, instruction-layer, UI, or
Milestone (M1–M14) changes were made. Purpose: determine whether the completed system behaves
like an expert writing teacher during authentic, multi-turn instructional interactions, and log
evidence-based calibration findings for later review.

## 1. Authentic test set
9 sessions, 24 multi-turn instructional cycles (mostly 3-turn draft→instruction→revision→revision
cycles) run against the LIVE engine via the durable-processing API. Harness:
`backend/tests/phase3_authentic_eval.py`. Full transcripts + engine reasoning:
`test_reports/phase3_transcripts.json`.

| # | Profile | Level / Age | Genre / Purpose | Special case probed |
|---|---------|-------------|-----------------|---------------------|
| P1 | weak | middle school (g7) | argument / persuade | fragmented draft; compliance revision; **unexpected off-target revision** |
| P2 | average | middle school (g8) | personal narrative | narrative must NOT be forced into claim-evidence |
| P3 | average | high school (g10) | explanatory | naïve-reader construction; no invented facts |
| P4 | strong | high school (g12) | literary analysis | strong draft; interpretation gap vs. "more evidence" |
| P5 | strong | college | argument (**near-perfect**) | almost-perfect writing; **repeated revisions**; appropriate stopping |
| P6 | average | college | compare → argument | **communicative purpose CHANGES across turns** |
| P7 | average | adult | reflective | reflection honors uncertainty; not forced into thesis |
| P8 | weak | high school (g9) | informative | **student ignores advice**; **abandoned draft / topic switch** |
| P9 | average | high school (g11) | argument | **multiple frameworks applicable at once** → must unify to ONE target |

## 2. Overall assessment — the architecture behaves like a restrained expert teacher
Measured across all 24 cycles:
- **One high-leverage target per turn: 24/24.** `scaffolding_control.primary_target` always singular; competing frameworks routed to `postponed`. No pile-on, even on P9 (thesis+paragraph+evidence+coherence+conclusion all applicable) — unified to the claim every turn.
- **Author ownership preserved: 24/24.** `intervention.focus='writing'` on every cycle; `writing_not_content_check` consistently confirms no substantive ideas supplied. Zero rewrites; zero invented evidence/arguments. Invitations promote thinking ("what is the one reason a principal would find convincing?"), not compliance.
- **Purpose-adaptive & genre-honoring.** Purposes correctly inferred (persuade/inform/explain/analyze/narrate/reflect/compare) and taught as functions. Narrative (P2) and reflection (P7) were NOT forced into claim-evidence; they were guided toward meaning/significance. **P6's purpose shift (compare→persuade) was tracked** — `communicative_purpose.primary` flipped from "compare" to "persuade" (with "compare … retained as the structure"), and the target adjusted accordingly.
- **Proportional calibration.** Strong drafts (P4, P5) → light `invite_only`/`consolidate`, explicit "intro is already strong — no need to intervene"; weak drafts (P1, P8) → a single foundational target; `calibration_check`/`consistency_check` populated and coherent on every turn.
- **Growth recognition + consolidation + transfer works.** On genuine revisions, `revision_development.primary_growth` named specific qualitative change (P1 "moved from competing reasons to a single coherent narrative"; P6 "committed to a purpose … the essay now has a spine"; P9 "central-claim emergence"), followed by natural, transferable `transfer_message`s. No edit-counting.
- **Stopping/consolidation honored where a real move occurred.** After large student moves the engine consolidated before pushing forward (P1 t3, P8 t2, P9 t2/t3).

## 3. Teacher-experience observations (Development Panel legibility)
- Every turn exposes a clear, human-readable chain: `primary_framework` → `supporting_frameworks` (reinforcing, not competing) → `calibration_check` (why this scope) → `consistency_check` (equivalence rule) → `postponed` (what was deliberately deferred) → `revision_*` (growth). A teacher can reconstruct *why this target, this turn* without guesswork.
- The M14 `consistency_check` strings ("Any persuasive draft at this stage without an arguable claim would receive the same priority") make the calibration policy inspectable — strong for teacher trust.
- No panel legibility defects observed.

## 4. Student-experience observations
- Invitations are level-appropriate in voice (P1 grade-7 phrasing vs. P5 college register) and consistently end with ONE actionable question. They recognize the student's own move first ("you picked one moment and let it carry the reason"), which supports engagement and ownership.
- Across revision cycles the students' drafts improved along the exact dimension the engine targeted (claim formation, meaning-making, precision), and the engine detected and named that growth — evidence the loop drives learning rather than dependence (it never hands the student finished text).

## 5. Calibration log (evidence-based)
For each: observed behavior → why → instructional impact → proposed change (if any) → confidence.

### F1 — Scope assumption on strong, self-contained pieces (MEDIUM confidence)
- **Observed:** For P5 (a complete, tight ~5-sentence argumentative paragraph), the engine assumed an "essay with body paragraphs" frame and asked "what job must the **first body paragraph** do?" — identically across all **3** turns (`invite_only`→`consolidate`→`consolidate`), `cycle_status="continue"` every time, `stopping_reason` always empty. It never (a) recognized the piece might be complete at its intended scope, (b) asked the student's intended scope, or (c) offered an independence/hand-back move despite 3 strong revisions with diminishing returns.
- **Why:** When a draft is strong and short, the highest-leverage "next" the engine finds is forward development, and it defaults to the culturally common essay structure (intro + body). No signal in the prompt distinguishes "self-contained short form, possibly done" from "intro to a longer essay."
- **Instructional impact:** Mild. Guidance stayed non-harmful and non-formulaic, but a real teacher would either affirm completeness/hand back, or clarify scope, rather than repeat a body-paragraph prompt a third time. Risk of nudging a complete paragraph toward an essay the assignment may not require.
- **Proposed change (DO NOT implement yet):** A small, domain-independent CALIBRATION nudge (not a redesign): when the unit is a strong self-contained piece and the assignment doesn't specify a longer form, prefer a scope-clarifying question or an independence/stopping move over assuming body paragraphs. This lives in the existing M11 stopping-rules / M14 calibration language — no new framework.
- **Evidence strength:** 3× within one session; needs ≥1 more strong-writer, short-form multi-turn session to confirm cross-session before any change. **Prefer calibration over redesign.**

### F2 — Non-engagement adaptivity when a student ignores/abandons (LOW confidence)
- **Observed:** P8 turn 2 (student ignored the invitation, only added detail) and turn 3 (student **abandoned** the topic entirely, switching basketball→dog): the engine correctly held the same developmental target (controlling idea) and re-invited patiently, rephrasing to the new topic. It did NOT try a fundamentally different scaffolding *entry point* for the same target, nor probe *why* the student wasn't engaging.
- **Why:** The developmental need genuinely persisted, so re-targeting is arguably correct; the engine optimizes for the true need, not for engagement tactics.
- **Instructional impact:** Low. Behavior is defensible (need is real), but an expert might vary the scaffold (e.g., offer 2–3 candidate controlling ideas *drawn from the student's own sentences* to choose among) after repeated non-engagement.
- **Proposed change:** None yet — single session, defensible behavior. Log only.

### F3 — `revision_development.applies=true` on a full topic switch (LOW confidence)
- **Observed:** P8 turn 3 (student abandoned draft, new topic): `revision_development.applies=true` but `primary_growth` correctly left empty and no fabricated growth/transfer. The engine text explicitly noted "you've switched topics entirely."
- **Why:** The turn `kind` was `revise`, so the revision lens engaged; the model correctly declined to claim growth.
- **Instructional impact:** Negligible to the student; slightly misleading panel semantics (a topic switch is not a revision of the same piece).
- **Proposed change:** None. If ever revisited, treat a detected topic switch as a new first-submission for the revision lens. Not warranted on this evidence.

### Non-findings (explicitly checked, no issue)
- Multi-framework pile-on (P9): **not observed** — clean single-target unification.
- Over-teaching strong writing (P4, P5): **not observed** — light interventions, explicit restraint.
- Formulaic/template imposition (all genres): **not observed**.
- Content coauthoring / rewriting: **not observed** (focus='writing' 24/24).
- Purpose mis-inference or failure to track purpose shift (P6): **not observed**.

## 6. Prioritized, evidence-supported improvement list (for review — NOT implemented)
1. **P-High(candidate, MEDIUM evidence) — Strong self-contained piece → scope/stopping calibration (F1).** Confirm with one more strong-writer short-form session; if replicated, add a minimal calibration nudge within existing M11/M14 language. Highest instructional value; smallest change.
2. **P-Low(LOW evidence) — Non-engagement scaffold variation (F2).** Watch for repetition across future sessions before acting.
3. **P-Low(cosmetic) — Revision-lens semantics on topic switch (F3).** Optional panel-clarity tweak only.

## 7. Success-criteria check
- ✓ Architecture evaluated under authentic, multi-turn instructional use (9 profiles, 24 cycles).
- ✓ Strengths and weaknesses documented (Sections 2–5).
- ✓ Proposed changes are evidence-based and gated by the change policy (repeated cross-session evidence required; none met that bar yet, so **nothing was changed**).
- ✓ No unnecessary architectural changes introduced.
- ✓ The completed instructional model is treated as STABLE; only one MEDIUM-confidence candidate (F1) is flagged for confirmation before any calibration.

**Conclusion:** The completed developmental architecture (M1–M14 + durable processing + reorganized panel) performs like a disciplined expert writing teacher across levels, ages, genres, and adversarial cases. It is stable. The single most actionable observation is F1 (scope/stopping on strong short forms), pending cross-session confirmation. STOP per phase directive — no new instructional domains and no changes until these findings are reviewed.
