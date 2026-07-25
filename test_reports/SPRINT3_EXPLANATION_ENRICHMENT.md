# Sprint 3 — Explanation / Analysis: Instructional Object Enrichment (THIRD OBJECT)

Scope: enriched ONLY the `Explanation / Analysis` object in the existing `instructional_objects.json` (additive; no new KB; engine/session/interface unchanged; fields reach the frozen engine via `_build_prompt`). Introduces the new **standard `instructionally_significant_discriminations`** section (A–F per case).

Design principle applied: teaching depends on recognizing which *apparently similar* explanations reflect *different underlying understanding* and therefore need *different responses*. The discriminations section encodes exactly that expert judgment.

---

## A. Updated object specification
Adds (to preserved originals): `reader_function`, `writer_function`, `functional_relationships`, `common_difficulties`, **`instructionally_significant_discriminations`** (4 cases, each with observable_performance / possible_interpretations / evidence_to_distinguish / response_per_interpretation / common_incorrect_response / why_it_matters), `productive_misconceptions`, `indicators_of_development`, `recognition_diagnostics_detailed`, `developmental_invitations` (8 explanation-specific types incl. `say_it_aloud`, `name_the_warrant`, `consider_alternative_explanation`), `followup_decisions` (branch on what the probe reveals), `revision_strategies`, `stopping_conditions`, `transfer`, `engine_usage`, `enrichment_version`.

### The four instructionally-significant discriminations
1. **No explanation given** → cannot-reason vs assumes-reader-knows vs cannot-organize vs believes-evidence-speaks-for-itself.
2. **Explanation restates the evidence** → summary-as-interpretation vs reasoning-missing vs weak-reader-awareness vs assignment-misread.
3. **Unsupported causal claim** → missing-warrant vs genuine-misconception (correlation=causation) vs evidence-cannot-establish-cause.
4. **Description instead of reasoning** → genre-confusion vs not-yet-inferred vs self-evident-warrant.
Each records the distinguishing probe, the correct response per interpretation, the common WRONG response, and why the distinction matters.

## B. Fields added (15)
reader_function, writer_function, functional_relationships, common_difficulties, instructionally_significant_discriminations, productive_misconceptions, indicators_of_development, recognition_diagnostics_detailed, developmental_invitations, followup_decisions, revision_strategies, stopping_conditions, transfer, engine_usage, enrichment_version.

## C. Fields revised
None rewritten; all originals preserved (additive only).

## D. Engine mapping
`instructionally_significant_discriminations` → **Stage 5 diagnostics + Stage 6 decision**: run the distinguishing probe (usually `say_it_aloud`) BEFORE teaching, resolve the underlying case, choose the matching `developmental_invitations` type, and AVOID the documented `common_incorrect_response`. `followup_decisions` branch on what the probe revealed. Other sections map as in prior objects (Stage 2/3/5/7). No engine code changed.

## E. Validation — THREE teaching situations (before vs after; transcripts in `explanation_enrichment_validation.json`)

### Situation 1 — No explanation (Lady Macbeth quote dropped after "shows she is ambitious")
- **Before:** "...evidence doesn't speak for itself... what does 'unsex me here' reveal about how she thinks about power?" (asks for interpretation, but assumes the gap is 'cannot reason').
- **After:** "...that's the conclusion, not the reasoning... what do those specific words actually reveal, and why? Try writing... **in your own words**." — deploys the `say_it_aloud` distinguishing probe.
- **Why superior:** the after-move first surfaces whether the learner CAN reason (own-words probe) instead of assuming one cause, matching the discrimination's evidence_to_distinguish; it avoids the common wrong response of handing over reasoning.

### Situation 2 — Restatement mistaken for explanation (printing press: "so the press meant books could be produced quickly")
- **Before:** "...your explanation is missing a step — the mechanism connecting faster books to ideas spreading..." (correct, but generic 'missing step').
- **After:** "...saying the press 'meant books could be produced quickly' tells us the **outcome**, but a causal explanation also shows the reader the **mechanism** — the actual process..." — deploys the summary/interpretation (outcome-vs-mechanism) discrimination explicitly.
- **Why superior:** names the exact restatement-vs-reasoning distinction the learner is missing, giving a transferable concept rather than a one-off "add a step."

### Situation 3 — Unsupported causal claim (testing: "higher scores, therefore students learn more")
- **Before:** framed as claim circularity ("your claim and reason use the same words").
- **After:** voices the rival interpretation precisely — "...is scoring higher on tests the **same thing as learning more**?... What do you actually want your reader to accept — that testing raises scores, that it produces deeper understanding, or something more?" — the `consider_alternative_explanation` discrimination in action.
- **Why superior:** instead of a generic circularity note, the after-coach exposes the specific correlation/equivocation gap (scores ≠ learning) and asks the learner to resolve it — the expert move that distinguishes a missing warrant from a genuine misconception.

Across all three, the enrichment shifts Compass from a single generic "add reasoning" toward **probe-then-teach**: surface which underlying case is present and respond to that case. (LLM output is stochastic; improvements are directional but clearly attributable to the added discrimination fields.)

## F. Regression check
- `instructional_objects.json`: 35 → 35 objects; element list byte-identical; all original Explanation fields preserved (verified by `tests/enrich_explanation.py`); JSON re-parses valid; 4 discriminations present.
- Backend restarted cleanly; KB loaded.
- Full Question-Loop → bridge → Milestone-engine flow ran fine with the enriched object (AFTER capture produced valid invitations + populated `theory`).
- Only `Explanation / Analysis` changed; Thesis (sprint3-v1) and Evidence (sprint3-v1) and all other objects untouched.

## Constraint compliance
Reused existing KB (no new base/duplication). Enriched ONE object (Explanation). Not grade-specific. Grounded in accepted analysis/reasoning principles (warrant, correlation≠causation, interpretation vs summary, reader who does not share the reasoning) and observed engine behavior — no invented theory, no curriculum/rubrics. Engine, session model, loops, interface unchanged. `instructionally_significant_discriminations` is now the standard diagnostic section for future objects. STOP: Introduction NOT started — awaiting approval.
