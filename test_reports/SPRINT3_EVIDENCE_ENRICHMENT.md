# Sprint 3 — Evidence: Instructional Object Enrichment (SECOND OBJECT)

Scope: enriched ONLY the `Evidence` object in the existing `backend/instructional_objects.json` (additive). No new KB, no duplication, no engine/session/interface change. Fields reach the frozen engine automatically via `_build_prompt` (whole object serialized).

Guiding principle applied: encode what an **expert developmental writing teacher** knows that Compass did not — especially how to *diagnose which of four independent evidence faults* is present and teach each differently. Every field below improves recognition, diagnosis, invitation choice, interpretation, revision, stopping, or transfer; nothing was added merely to be complete.

---

## A. Updated object specification
`Evidence` now adds (to its preserved originals): `reader_function`, `writer_function`, `functional_relationships`, **`evidence_quality_dimensions`** (relevance / sufficiency / credibility / accuracy — each with test, failure_signal, remedy), `common_difficulties`, **`look_alike_distinctions`** (same-looking cases needing different teaching), `productive_misconceptions`, `indicators_of_development`, `recognition_diagnostics_detailed`, **`genre_variation`** (what counts as evidence + the bar per genre), `developmental_invitations` (9 evidence-specific types with use_when/avoid_when), `followup_decisions`, `revision_strategies`, `stopping_conditions`, `transfer`, `engine_usage`, `enrichment_version`.

The three bolded fields are the "missing expertise" beyond the generic template:
- **evidence_quality_dimensions** — an expert never says "your evidence is weak"; they diagnose WHICH of relevance/sufficiency/credibility/accuracy fails, because each has a different remedy.
- **look_alike_distinctions** — background-vs-outcome (false positive), illustration-vs-proof, and unconnected-quote (can't-connect vs assumes-obvious); identical-looking text, different teaching.
- **genre_variation** — the admissible kind of evidence and the credibility/sufficiency bar differ by discipline (literary/historical/scientific/argument/personal).

## B. Fields added (17)
reader_function, writer_function, functional_relationships, evidence_quality_dimensions, common_difficulties, look_alike_distinctions, productive_misconceptions, indicators_of_development, recognition_diagnostics_detailed, genre_variation, developmental_invitations, followup_decisions, revision_strategies, stopping_conditions, transfer, engine_usage, enrichment_version.

## C. Fields revised
None rewritten. All originals (definition, communicative_purpose, performance_structure, recognition_diagnostics, common_obstacles, next_developmental_moves, indicators_of_control, related_elements) preserved for backward compatibility. Enrichment is purely additive.

## D. Engine mapping
`engine_usage` (in-object) maps each section to a Canonical-Session-Model decision: quality_dimensions + look_alike_distinctions + genre_variation → **Stage 5 diagnostics** (score each dimension separately; resolve look-alikes; calibrate the bar); developmental_invitations → **Stage 3 invitation** (one type matched to the failing dimension); followup_decisions → **Stage 6 decision** (retarget upstream to Claim or downstream to Explanation); functional_relationships → **Stage 2 sequencing** (is Evidence even the bottleneck?); stopping_conditions/transfer → **Stage 7 closure**. No engine code changed.

## E. Validation — THREE realistic teaching situations (before vs after; transcripts in `evidence_enrichment_validation.json`)
Each scenario uses a draft with a SOLID claim so the engine's highest-leverage target is Evidence (confirmed: `active_instructional_element == "Evidence"` in all three).

### Situation 1 — Weak credibility ("a blog post says so, and kids I know don't like it")
- **Before:** "...a claim works when it's contestable and you can back it up with trustworthy grounds..." — correct instinct but framed as a *claim* concept, blending two objects.
- **After:** "...your two pieces of support are a blog post and kids you know — a doubting reader would likely question whether those sources are enough to **trust** the claim." Target logged: *"Evidence credibility — the support actively weakens the claim for a reader."*
- **Why superior:** the after-coach isolates the **credibility** dimension by name and teaches from reader trust, instead of drifting back to claim framing. Precise diagnosis → precise remedy.

### Situation 2 — Relevance mismatch (1929 crash offered for "the New Deal reduced unemployment")
- **Before:** "...your evidence describes the problem, not the solution..." — catches it, but generically.
- **After:** tension logged as *"Evidence relevance failure: student offers background/context (crisis severity) where outcome evidence (program impact) is needed,"* and the coach asks specifically for evidence that the **programs actually lowered** unemployment.
- **Why superior:** the after-coach names the exact **look-alike distinction** (background-vs-outcome / false positive) from the enriched object and directs the learner to outcome evidence — the expert move, not a generic "explain more."

### Situation 3 — Insufficient anecdote ("my friend felt anxious one night" = proof)
- **Before:** "...one friend's one night is a very thin foundation... A claim works when it tells the reader what kind of evidence would support it..." — again slides into claim language.
- **After:** "...a personal anecdote can **illustrate** a point vividly, but it doesn't by itself **prove** that heavy use broadly causes anxiety. What is the difference between your friend's case and...?"
- **Why superior:** the after-coach deploys the **illustration-vs-proof** distinction (sufficiency dimension) verbatim from the enriched object and invites the learner to articulate it — turning a vague "thin" into a teachable, transferable principle.

Across all three, the enrichment made the engine (1) name the specific failing dimension, (2) apply the correct look-alike distinction, and (3) stay in evidence territory rather than reverting to claim framing. (LLM output is stochastic; the improvement is directional but consistent and clearly attributable to the added fields.)

## F. Regression check
- `instructional_objects.json`: 35 → 35 objects (unchanged); element list byte-identical; all original Evidence fields preserved (verified by `tests/enrich_evidence.py`); JSON re-parses valid.
- Backend restarted cleanly; KB loaded.
- Full Question-Loop → bridge → Milestone-engine flow ran fine with the enriched object (the AFTER capture created 3 sessions and produced valid invitations + populated `theory`).
- Only the `Evidence` object changed; Thesis (sprint3-v1) and all other objects untouched.

## Constraint compliance
Reused existing KB (no new base/duplication). Enriched ONE object (Evidence). Not grade-specific (learner profiles vary language/support; the object encodes mature function). Grounded in accepted argumentation/writing principles (relevance, sufficiency, credibility, accurate representation; illustration≠proof; reader-as-skeptic; genre-appropriate evidence) and observed engine behavior — no invented theory, no curriculum/rubrics. Engine, session model, loops, interface unchanged. STOP: Explanation NOT started — awaiting approval.
