# Sprint 3 — Thesis / Controlling Idea: Instructional Object Enrichment (FIRST OBJECT ONLY)

Scope: enriched ONLY the `Thesis` object in the existing `backend/instructional_objects.json`. No new knowledge base, no duplication, no engine/session/interface change. The engine is frozen; `_build_prompt` already serializes the FULL object into the engine prompt, so the added fields reach the engine automatically (mapping only, no code change).

---

## A. Updated object specification
`instructional_objects.json → element "Thesis"` now contains, in addition to its original fields:
- **IDENTITY**: `reader_function`, `writer_function` (plus existing `element`, `communicative_purpose`, `related_elements`).
- **CANONICAL PERFORMANCE**: existing `performance_structure` (already a functional, non-template description — kept as-is).
- **FUNCTIONAL RELATIONSHIPS**: `functional_relationships` {purpose, reader, neighboring_components, overall_organization}.
- **COMMON DIFFICULTIES**: `common_difficulties` [{type, description}] — missing, topic_not_claim, too_broad, too_narrow, unsupportable, obvious, announcement, disconnected, buried_or_multiple. (Existing terse `common_obstacles` retained.)
- **PRODUCTIVE MISCONCEPTIONS**: `productive_misconceptions` [{misconception, why_productive, leverage}].
- **INDICATORS OF DEVELOPMENT**: `indicators_of_development` {early, partial, independent, flexible}. (Existing `indicators_of_control` retained.)
- **RECOGNITION DIAGNOSTICS**: `recognition_diagnostics_detailed` {attempting, control_level, likely_misconception, next_move}. (Existing `recognition_diagnostics` retained.)
- **DEVELOPMENTAL INVITATIONS**: `developmental_invitations` [{type, purpose, use_when, avoid_when}] — clarify, compare, predict_reader_understanding, reorganize, justify, evaluate, connect, simplify, expand, test, reflect.
- **FOLLOW-UP DECISIONS**: `followup_decisions` [{after, consider}].
- **REVISION STRATEGIES**: `revision_strategies` [functional improvements, not editing].
- **STOPPING CONDITIONS**: `stopping_conditions` [...].
- **TRANSFER**: `transfer` {other_genres, other_assignments, other_disciplines, future_writing}.
- **ENGINE MAPPING (in-object)**: `engine_usage` {section → engine decision}; `enrichment_version: "sprint3-v1"`.

Not grade-specific (§5): every field describes MATURE writing function; learner profiles vary language/examples/support/pace, the object stays stable.

## B. Fields added
`reader_function, writer_function, functional_relationships, common_difficulties, productive_misconceptions, indicators_of_development, recognition_diagnostics_detailed, developmental_invitations, followup_decisions, revision_strategies, stopping_conditions, transfer, engine_usage, enrichment_version` (14 new keys).

## C. Fields revised
None rewritten. All original fields (`definition, communicative_purpose, performance_structure, recognition_diagnostics, common_obstacles, next_developmental_moves, indicators_of_control, related_elements`) preserved verbatim to guarantee backward compatibility. Enrichment is purely additive (spec: "improve only where clearly incomplete" — the originals were adequate; richer detail was added as new, non-conflicting sections).

## D. Engine mapping (which frozen-engine decision uses each section)
| Section | Canonical-model stage / engine field it feeds |
|---|---|
| reader_function / writer_function | Stage 2 Target Selection + Stage 5 Interpretation (`instructional_reasoning`) |
| performance_structure | Stage 5 Interpretation — gap vs `primary_developmental_tension` |
| functional_relationships | Stage 2 Target Selection (`scaffolding_control.primary_target` / `postponed`) + sequencing |
| common_difficulties + recognition_diagnostics_detailed | Stage 5 Diagnostics (`student_current_organization`, `primary_developmental_tension`) |
| productive_misconceptions | Stage 3 Invitation (`intervention` — leverage, not correct) |
| indicators_of_development | Stage 5 Interpretation (`degree_of_student_control`) + Stage 6 Decision |
| developmental_invitations | Stage 3 Invitation (`instructional_mode` / invitation choice; still ONE per turn) |
| followup_decisions | Stage 6 Decision (`cycle_status`, continue/redirect/±support/retarget/conclude) |
| revision_strategies | Stage 3 Invitation for revision (functional) |
| stopping_conditions | Stage 6 Decision + Stage 7 Closure (`stopping_reason`) |
| transfer | Stage 7 Closure (consolidation + transfer note) |
No engine code changed — the object is injected whole via `_build_prompt` (server.py line ~1061).

## E. Validation examples (same scenario, before vs after — transcripts in `thesis_enrichment_validation.json`)
Scenario: assignment "Write an essay explaining the most important cause of the fall of the Roman Empire." + a weak topic-not-claim draft ("...There were many reasons... It was a big empire and then it fell. This essay is about that.").

- **Before (opening invitation):** "...a thesis isn't the topic itself, it's the one idea you want the reader to accept... there's no position a reader could agree or disagree with. What do you think was the single most important cause?"
- **After (opening invitation):** "...the assignment asks you to explain the *most important cause*. A thesis for this essay isn't just the topic; it's a specific answer to that question... not 'this essay is about' the topic, but your actual claim about why it fell."
- **After (second cycle):** "...'Rome got too big to manage' is something a reader could actually push back on. That's what a thesis does. Now, a reader holding this claim would naturally ask: *too big to manage in what way, and how did that bring the empire down?*"

**Why the interaction improved:** the after-enrichment coach (1) anchors the thesis to the assignment's specific question (from `functional_relationships.purpose`), (2) explicitly names the topic-not-claim / announcement difficulty (from `common_difficulties`), and (3) deploys the **predict_reader_understanding** invitation type near-verbatim (from `developmental_invitations`) and foregrounds **contestability** (from `indicators_of_development`/performance function). The engine was already competent; enrichment made its diagnosis and invitation more precise, reader-oriented, and task-connected. (LLM output is stochastic, so the gain is directional but observable across the captured runs.)

## F. Regression check (no existing functionality broke)
- `instructional_objects.json`: object count 35 → 35 (unchanged); element list byte-identical; all original Thesis fields preserved (verified by `tests/enrich_thesis.py`); JSON re-parses valid.
- Backend restarted cleanly and loaded the KB (`grade-9 + high-school-graduate calibration profiles ensured`).
- Live end-to-end still works with the enriched object: the AFTER capture ran the full Question-Loop → bridge → Milestone-engine flow (create representation → from-representation → 2 interact cycles) and produced valid invitations + populated `theory` — confirming retrieval, prompt assembly, and reasoning are intact.
- Only the `Thesis` object changed; all other objects untouched.

## Constraint compliance
Reused existing KB (no new base/duplication). Enriched ONE object only (Thesis/Controlling Idea). Grounded in accepted writing principles (contestable, focused, supportable controlling idea; reader expectation-setting) and existing Compass behavior — no invented theory, no curriculum/rubrics/lesson plans. Engine, session model, loops, and interface unchanged. STOP: second object (Evidence) NOT started — awaiting approval.
