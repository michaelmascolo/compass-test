# Sprint 3 — Introduction: Instructional Object Enrichment (FOURTH OBJECT)

Scope: enriched ONLY the `Introduction` object in the existing `instructional_objects.json` (additive; no new KB; engine/session/interface unchanged; fields reach the frozen engine via `_build_prompt`). Introduces the new **standard `instructional_leverage`** section (expert prioritization, A–E) and an explicit **`cross_object_dependencies`** section, alongside the now-standard `instructionally_significant_discriminations`.

New canonical principle applied: when several instructional moves are possible, encode which one has the greatest DEVELOPMENTAL leverage — and note that the most *correct* move is not always the best *instructional* move (clarity/purpose/reader-awareness/confidence may come first).

---

## A. Updated object specification
Adds (to preserved originals): `reader_function`, `writer_function`, `functional_relationships`, `common_difficulties`, `instructionally_significant_discriminations` (3 cases, A–F), **`instructional_leverage`** (4 situations, A–E), **`leverage_over_correctness_note`**, **`cross_object_dependencies`** (5 mappings), `productive_misconceptions`, `indicators_of_development`, `recognition_diagnostics_detailed`, `developmental_invitations` (8 intro-specific incl. `orient_the_reader`, `connect_hook_to_purpose`, `select_relevant_context`, `convert_announcement_to_idea`), `followup_decisions`, `revision_strategies`, `stopping_conditions`, `genre_variation`, `transfer`, `engine_usage`, `enrichment_version`.

### instructional_leverage (the new section) — the four situations, each with:
A observable learner state · B possible responses · C recommended first response · D why highest leverage · E when another response takes priority. Situations: (1) hook without/disconnected from direction → secure the destination first; (2) background info-dump → surface direction + stakes before trimming; (3) reader confused about trajectory → make the destination visible early; (4) competent-but-flat opening → check leverage before polishing (usually move to higher-leverage body work).

### cross_object_dependencies
Maps each intro symptom to its likely upstream cause + action: hook_disconnected/announcement → Thesis/Purpose; background_no_direction → Purpose/Organization; reader_confusion → Thesis precision/Organization; can't-judge-relevant-context → Audience Awareness or **Missing Knowledge → route to the Knowledge Loop**. Documentation only — no engine logic added.

## B. Fields added (19)
reader_function, writer_function, functional_relationships, common_difficulties, instructionally_significant_discriminations, instructional_leverage, leverage_over_correctness_note, cross_object_dependencies, productive_misconceptions, indicators_of_development, recognition_diagnostics_detailed, developmental_invitations, followup_decisions, revision_strategies, stopping_conditions, genre_variation, transfer, engine_usage, enrichment_version.

## C. Fields revised
None rewritten; all originals preserved (additive only).

## D. Engine mapping
`instructional_leverage` → **Stage 6 decision** (when multiple moves exist, pick the highest-leverage FIRST response; respect "when_another_takes_priority"). `cross_object_dependencies` + `functional_relationships` → **Stage 2 target selection** (decide whether Introduction is the real target or a symptom → retarget upstream to Thesis/Purpose/Audience/Organization, or route to the Knowledge Loop). `leverage_over_correctness_note` → Stage 6 (prefer clarity/purpose/reader-awareness/confidence over a technically better opening). Discriminations → Stage 5 diagnostics + Stage 6. Other sections map as in prior objects. No engine code changed.

## E. Validation — THREE teaching situations (before vs after; transcripts in `introduction_enrichment_validation.json`)
Each draft carries a solid/near-solid thesis so the introduction can plausibly be the target.

### Situation 1 — Hook disconnected from thesis (dinosaurs → transit)
- **Before:** target "Opening / Introduction (with Thesis consolidated)"; "...what work do you want that first sentence to do for your reader before they reach your thesis?" (open, unfocused).
- **After:** target "Hook / Opening Move → connection to thesis"; "...your opening sentence — about dinosaurs — doesn't connect to that argument... What could you put in that opening sentence that would actually **lead your reader toward your claim** about public transit?" — the `connect_hook_to_purpose` leverage move.
- **Why superior:** the after-move applies the highest-leverage response (make the opening serve the destination) rather than an open-ended "what should it do," giving the learner a concrete, transferable target.

### Situation 2 — No reader orientation (French Revolution causes stated with no context)
- **Before & After:** both target Cause-and-Effect Explanation (mechanism), NOT intro cosmetics.
- **Why this is correct leverage:** the enriched `leverage_over_correctness_note` and `cross_object_dependencies` say an introduction is a symptom when a deeper content move (here, the causal mechanism) is higher leverage. The engine correctly declines to polish orientation while the mechanism is missing — leverage over correctness in action.

### Situation 3 — Background with a buried thesis (Gatsby settings)
- **Before:** target "Thesis precision" — sharpen the interpretive claim.
- **After:** target "Background / Context — what a reader needs before the thesis will land"; tension logged as *"the student treats background as factual reporting rather than as analytical framing that orients the reader,"* and the coach asks: "...what does your reader need to understand **before** that final claim will make sense? Not facts about the book, but the idea that sets up why the relationship between setting and mood matters."
- **Why superior:** the after-move deploys the enriched leverage principle (surface direction/stakes; select reader-necessary context) and reframes background as orientation rather than reporting — a durable introduction skill the before-run did not teach.

Across the three, the enrichment makes the engine (1) choose the leverage-ranked intro move, (2) treat the introduction as a symptom when an upstream/content dependency dominates, and (3) reframe background as reader-orientation. (LLM output is stochastic; the shifts are directional but clearly attributable to the added leverage/dependency fields.)

## F. Regression check
- `instructional_objects.json`: 35 → 35 objects; element list byte-identical; all original Introduction fields preserved (verified by `tests/enrich_introduction.py`); JSON re-parses valid; 4 leverage situations + 5 dependencies + 3 discriminations present.
- Backend restarted cleanly; KB loaded.
- Full Question-Loop → bridge → Milestone-engine flow ran fine with the enriched object (AFTER capture produced valid invitations + populated `theory`).
- Only `Introduction` changed; Thesis, Evidence, Explanation (all sprint3-v1) and every other object untouched.

## Constraint compliance
Reused existing KB (no new base/duplication). Enriched ONE object (Introduction). Not grade-specific. Grounded in accepted composition principles (orientation, motivation, reader-necessary context, hook-serves-purpose, introduction-as-trajectory) and observed engine behavior — no invented theory, no curriculum/rubrics. Engine, session model, loops, interface unchanged. `instructional_leverage` and `cross_object_dependencies` join `instructionally_significant_discriminations` as standard sections for future objects. STOP: Topic Sentence NOT started — awaiting approval.
