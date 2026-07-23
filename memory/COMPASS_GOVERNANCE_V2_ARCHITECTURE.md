# Compass Governance v2 — Architecture Specification (DRAFT FOR REVIEW)

> Status: **DRAFT**, architectural level only (behavior + interfaces, no code). Once approved this becomes the authoritative implementation contract for Governance v2.
> Relationship to v1: Governance v2 is a **candidate successor** to Governance v1. It is implemented behind the existing `reasoning_mode` feature flag (`reasoning_mode: "governance_v2"`). The default **`exhaustive` (frozen v1) engine remains unchanged and is the safety net + baseline.** v2 is promoted to default only after it passes the 66-case Compare-Two-Runs constitutional review AND demonstrates improvement in clarity, transparency, instructional quality, and latency — not merely output matching.

---

## 0. Core thesis — what v2 changes (and what it does NOT)

**v2 changes the CONTROL ARCHITECTURE, not the instructional knowledge.**

- The frozen `SYSTEM_MESSAGE` is treated as a **reusable Instructional Knowledge Base (KB)**: developmental principles, canonical functional models (M6–M13), the IO 12-step element library, scaffolding strategies, ZPD/learner-model concepts, dialogue guidance, and constitutional rules. **It is not rewritten in this round.**
- A new **Governance v2 Orchestrator** owns the *sequence* of reasoning and *when* each governance layer is invoked. It queries the KB as needed at each stage.
- If, after validation, we find the KB *itself* needs changes, that becomes a future "true SYSTEM_MESSAGE v2." Not a goal now.

The 5-Layer Governance Architecture (L1 Constitutional, L2 Developmental Policy, L3 Diagnosis, L4 Learner Model, L5 Presentation) is preserved. v2 changes **the order in which the layers are engaged** and adds an explicit, inspectable orchestration spine.

---

## 1. Overall processing pipeline

```
                         ┌──────────────────────────────────────────────┐
   student turn ───────▶ │  GOVERNANCE V2 ORCHESTRATOR                    │
   (text + session)      │                                                │
                         │  S1 PURPOSE ───────────────┐                   │
                         │      │  (purpose unclear?) ─┴──▶ [B1 CLARIFY]   │
                         │      ▼                                          │
                         │  S2 WRITING UNIT                                │
                         │      ▼                                          │
                         │  S3 CANONICAL FUNCTIONAL MODEL  (KB lookup)     │
                         │      ▼                                          │
                         │  S4 FUNCTIONAL INTERPRETATION ─┐                │
                         │      │ (conceptual org missing?)┴─▶ [B2 PREWRITE]│
                         │      │ (off-task/incoherent?) ──────▶ [B3 FALLBACK]
                         │      ▼                                          │
                         │  S5 INSTRUCTIONAL TARGET  (exactly ONE)         │
                         │      ▼    ◀───── learner modeling BEGINS here ──│
                         │  S6 DEVELOPMENTAL STRATEGY (L4 + scaffolding)   │
                         │      ▼                                          │
                         │  S7 DIALOGUE / EXPLICIT TEACHING (L5)           │
                         │      │  Orient→Teach→Locate→Invite→Reflect      │
                         └──────┼─────────────────────────────────────────┘
                                ▼
                    one learner-facing invitation + transparency_state
```

**Ordering principles enforced by the spine:** purpose before development (S1); writing unit before learner model (S2 before S6); interpret before teach (S4 before S7); exactly one target (S5); developmental reasoning deferred until after the target is chosen (S6); explicit, reader-centered teaching (S7); function over form (S3/S4); prewriting as a decision point (B2); transparency emitted every turn (S7).

---

## 2. The reasoning ledger (data passed between stages)

A single accumulating structure flows through the stages and is persisted per turn for inspectability and for the transparency UI. Conceptually:

```
GovernanceV2Trace {
  purpose:                { communicative_purpose, confidence, source, assignment_alignment }
  writing_unit:           { unit, scope, confidence, prior_unit_continuity }
  functional_model:       { functions[], reader_needs[] }
  functional_interpretation: { function_status[ {function, status, evidence} ], reader_gap_summary }
  target:                 { primary_target, leverage_rationale, target_continuity }
  developmental_strategy: { learner_state, zpd_position, scaffolding_level, support_move, consolidation/fading }
  dialogue:               { student_facing_invitation, candidate_invitations[2], teaching_content, reflection_prompt }
  transparency_state:     { where_you_are, current_unit, why_it_matters, todays_goal, whats_next }
  branch:                 none | purpose_unclear | prewriting | foundational_fallback
  layers_invoked:         { per-stage list of L1..L5 }
  stage_latencies_s:      { per-stage timing }
}
```

Each stage appends only its own outputs; downstream stages read only what they need. This ledger directly powers (a) the Compare-Two-Runs governance panel (one panel per stage + branch) and (b) the transparency UI (point #10).

---

## 3. Stage-by-stage contract

For each stage: **Responsibility · Inputs · Outputs · Does NOT do · Governance layer(s) · KB referenced.**

### S1 — PURPOSE
- **Responsibility:** Determine the communicative purpose of the writing task — what the student is trying to accomplish for a reader — honoring the teacher's stated purpose.
- **Inputs:** session telos (teacher purpose, assignment, teacher_notes), current student text, prior conversation.
- **Outputs:** `communicative_purpose`, `purpose_confidence`, `purpose_source` (teacher | student-stated | inferred), `assignment_alignment` (on-task | drift | off-task).
- **Does NOT:** diagnose weaknesses, model the learner, select a target, or teach.
- **Layers:** L2 (purpose-first, honor teacher purpose), L1 (answer-the-assignment gate).
- **KB:** M6 communicative purpose; telos/teacher_notes.
- **Branch:** if `purpose_confidence` below threshold or intended meaning indeterminate → **B1 Purpose-Unclear**.

### S2 — WRITING UNIT
- **Responsibility:** Identify the current instructional object (prewriting, thesis, introduction, body paragraph, evidence, transition, conclusion, whole-draft, …).
- **Inputs:** purpose, student text, turn kind, prior target/unit.
- **Outputs:** `writing_unit`, `unit_scope` (local span | whole draft), `unit_confidence`, `prior_unit_continuity` (same | advanced | regressed).
- **Does NOT:** judge quality, teach, or model the learner.
- **Layers:** L2; L3 (light — object identification only).
- **KB:** IO 12-step canonical element library.

### S3 — CANONICAL FUNCTIONAL MODEL
- **Responsibility:** Load, from the KB, the canonical functional model for the identified unit — the communicative functions that unit performs for a reader, and what the reader needs from it. Function over form: multiple valid realizations.
- **Inputs:** `writing_unit`, `communicative_purpose`.
- **Outputs:** `functions[]` (ordered communicative functions of the unit), `reader_needs[]`.
- **Does NOT:** evaluate the student's text (this is a KB lookup, not a judgment).
- **Layers:** L2 (function-over-form), reader-centered framing (M12).
- **KB:** the unit's functional frameworks (M6–M13) + IO element definitions.

### S4 — FUNCTIONAL INTERPRETATION
- **Responsibility:** Interpret the student's actual writing against the functional model — which functions are **present & working**, **weak**, or **missing** — from the reader's perspective. **Understand, not teach.**
- **Inputs:** `functions[]`, `reader_needs[]`, student text, purpose.
- **Outputs:** `function_status[]` (each: function, status ∈ {present, weak, missing}, evidence = span/quote), `reader_gap_summary`.
- **Does NOT:** select a target, teach, model the learner, invent deficiencies (restraint), or score.
- **Layers:** L3 (diagnosis — interpretation only), reader-centered, L1 (restraint: no invented deficiencies).
- **KB:** the unit's functional frameworks.
- **Branches:** if weakness reflects **insufficient conceptual organization** (no locatable idea/claim to organize; the unit's functions cannot even be attempted because the thinking isn't developed yet) → **B2 Prewriting Mode**. If the text is **off-task or incoherent across ideas** (inconsistent with the established purpose/unit) → **B3 Foundational Fallback**.

### S5 — INSTRUCTIONAL TARGET
- **Responsibility:** Select **exactly ONE** instructional target with the greatest developmental leverage among the weak/missing functions.
- **Inputs:** `function_status[]`, `reader_gap_summary`, purpose, prior target/continuity.
- **Outputs:** `primary_target` (single function/aspect of the unit), `leverage_rationale`, `target_continuity` (new | continued | resolved→advance).
- **Does NOT:** model the learner (next stage), teach, or address multiple issues.
- **Layers:** L2 (one-target policy), L3.
- **Constitutional:** exactly one target.

### S6 — DEVELOPMENTAL STRATEGY  ◀ learner modeling & developmental reasoning BEGIN here
- **Responsibility:** Now invoke the learner model + ZPD + scaffolding decision for the selected target only. Decide amount of support, question/explanation balance, and whether to teach-heavy, guide, or fade — given the learner's history.
- **Inputs:** `primary_target`, learner `developmental_profile`/history, `revision_history`, teacher scaffolding config.
- **Outputs:** `learner_state` (for this target), `zpd_position`, `scaffolding_level`, `support_move` (teach-heavy | guided | fade), `consolidation`/`fading` flags.
- **Does NOT:** generate the student-facing text yet; address other targets.
- **Layers:** L4 (learner model), L2 (scaffolding/fading policy).
- **KB:** scaffolding strategies, ZPD, learner-model concepts.

### S7 — DIALOGUE / EXPLICIT TEACHING
- **Responsibility:** Generate ONE learner-facing coaching turn following the **explicit-teaching pattern**:
  1. **Orient** — where we are (unit) and why it matters (reader-centered).
  2. **Teach** — explicitly explain the concept and the communicative function it serves for the reader.
  3. **Locate** — identify the student's closest current attempt; explain why it's working or where its function is incomplete.
  4. **Invite** — invite the student to apply/revise **their own writing** (one invitation).
  5. **Reflect** — set up reflection on how the revision improved communication.
- **Inputs:** `primary_target`, developmental strategy, functional interpretation (to locate the attempt), purpose, unit, KB dialogue guidance.
- **Outputs:** `student_facing_invitation` (single), `candidate_invitations` (exactly 2, internal), `teaching_content`, `reflection_prompt`, `transparency_state` (see §5).
- **Does NOT:** write, rewrite, or supply the student's content; introduce a second target; score.
- **Layers:** L5 (presentation), L1 (anti-coauthoring), L2.
- **Constitutional:** one invitation; explicit teaching of the concept is permitted, but the student generates the ideas, makes the decisions, and produces the revised text.

---

## 4. Branches / decision points

### B1 — Purpose-Unclear (after S1)
- **Trigger:** low `purpose_confidence` / intended meaning indeterminate.
- **Behavior:** skip heavy diagnosis (S3–S6); run a clarification turn (inside-out) whose single target is *surface the student's intended meaning/purpose*. Still explicit + reader-centered ("to help a reader, we first need to know what you're trying to say"). One invitation.
- **Exit:** once purpose is sufficiently clear (this or a later turn), resume the normal pipeline at S2.

### B2 — Prewriting Mode (after S4)
- **Trigger:** functional interpretation shows the weakness is insufficient conceptual organization, not drafting.
- **Behavior:** temporarily set `writing_unit = prewriting`; the target becomes organizing thinking (idea generation, claim formation, structure-of-thought) before returning to drafting/revision. Explicit teaching of the prewriting move; the student does the thinking.
- **Exit:** when sufficient conceptual organization exists, return to the drafting unit.
- **Design intent:** detection uses only S4 signals (cheap), so we do NOT reintroduce the global analysis v2 is trying to avoid.

### B3 — Foundational Fallback (anti-suppression; inherited from v1)
- **Trigger:** any stage finds evidence inconsistent with the established purpose/unit (off-task, incoherent across ideas) that the current lens cannot contain.
- **Behavior:** raise a fallback flag → escalate to the full frozen `exhaustive` engine. Never force material into the wrong lens. Preserves constitutional safety.

---

## 5. Transparency contract (point #10)

Every v2 turn MUST emit `transparency_state` (the engine produces it even before any UI consumes it):
- `where_you_are` — position in the assignment arc.
- `current_unit` — the writing unit being worked.
- `why_it_matters` — reader-centered rationale.
- `todays_goal` — the single instructional target as a student-facing goal.
- `whats_next` — the anticipated next unit/step.

Layer: L5 + a later `StudentWorkspace` UI sub-phase. The evaluator scores its completeness/accuracy.

---

## 6. Where key things happen (explicit answers)
- **Purpose determination:** S1.
- **Writing unit / instructional context:** S2 (before learner modeling).
- **Functional interpretation (understand, not teach):** S4.
- **Single instructional target selected:** S5.
- **Learner modeling BEGINS:** S6.
- **Developmental reasoning BEGINS:** S6.
- **Explicit teaching occurs:** S7 (steps 2–3), using KB concept definitions.
- **Dialogue generation occurs:** S7.

---

## 7. Updated evaluator dimensions for Compare-Two-Runs

Keep all existing v1 dimensions (constitutional preservation, anti-coauthoring, target defensibility, restraint, etc.) and ADD:
- **Purpose-first ordering** — purpose established before diagnosis.
- **Single-target discipline** — exactly one target addressed.
- **Explicit teaching present** — concept taught (function + reader value) before the invitation; the 5-step pattern followed.
- **Reader-centered framing** — instruction framed by what the reader needs.
- **Function over form** — no rigid template imposed; alternative valid realizations respected.
- **Transparency completeness** — all five transparency fields present + accurate.
- **Prewriting-mode appropriateness** — entered only when warranted; not over-triggered.
- **Latency** — total + per-stage timings.

**Promotion criteria:** constitutional preservation maintained (0 regressions, 0 anti-coauthoring violations) AND measurable improvement on clarity / explicit-teaching / transparency / latency vs. v1. NOT mere output matching (per the v1 precedent: judge governing behavior, not textual similarity).

---

## 8. Constitutional invariants every stage must preserve (L1 — non-negotiable)
- Student authorship / anti-coauthoring: never write, rewrite, or supply copyable content.
- Exactly one instructional target; exactly one learner-facing invitation.
- Restraint: no invented deficiencies; intervention proportional to genuine need.
- No scores.
- Honor stopping rules (independence requests / diminishing returns).
- Answer-the-assignment / honor the teacher's stated purpose.
- The student performs all revision and all cognitive work. **Explicit teaching is permitted but must not cross into doing the student's thinking or writing.**

---

## 9. Reuse & integration map (least disruption)
- `reasoning_mode` gains a third value: `governance_v2` (alongside `exhaustive`, `triage_experimental`). Default stays `exhaustive`.
- Reuse the existing triage Stage-1 signals for S1/S2 where suitable (or a v2-specific purpose/unit pass — see open choices).
- Reuse the `ROUTE_LENS_MAP` concept as the basis for the S3 functional-model lookup.
- Reuse durable polling + streaming (stream the S7 invitation).
- Reuse the Compare-Two-Runs harness + governance inspectability UI (extend to 7 stage-panels + branch + transparency).
- Frozen `SYSTEM_MESSAGE` untouched — referenced as the KB.

---

## 10. Open implementation choices (for discussion — NOT decided here)
1. **Call granularity:** one LLM call per stage (max control/inspectability, more latency) vs. batching (e.g., S1–S2 together, S3–S5 together, S6–S7 together). Latency vs. control tradeoff.
2. Whether S1/S2 reuse the existing triage prompt or a new v2 purpose/unit prompt.
3. Exact **prewriting-detection** signals at S4.
4. **Purpose-confidence threshold** for the B1 branch.
5. Candidate-invitation count (keep 2 as in v1?).
6. Where `transparency_state` is authored (within S7 vs a dedicated step).
7. How much KB to inject per stage (token/latency management).
8. Whether B1/B2 produce a full 5-step teaching turn or an abbreviated clarification turn.

---

## 11. Non-goals for this round
- No rewrite of the instructional knowledge (frozen `SYSTEM_MESSAGE` stays; a "true SM v2" is a possible future).
- No teacher-product changes (**Phase III Teacher Dashboard is PAUSED** until v2 is specced, implemented, validated, and promoted).
- No constitutional changes.

---

## 12. Proposed workstream sequence (after this spec is approved)
1. Approve this spec (authoritative contract).
2. Implement Governance v2 behind `reasoning_mode="governance_v2"`.
3. Extend the evaluator with the §7 dimensions.
4. Validate via the full 66-case Compare-Two-Runs vs the frozen v1 baseline (+ vs Governance v1).
5. Promote v2 to default only on passing constitutional review + comparative improvement.
6. Transparency UI sub-phase (#10).
7. Prewriting-mode refinement sub-phase (#9).
8. Resume Phase III Teacher Dashboard, designed around v2's actual outputs.
