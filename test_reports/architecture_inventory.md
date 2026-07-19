# Compass — Instructional Architecture Inventory (read-only)

Inventory only — no evaluation, no recommendations. Source of truth: `backend/server.py`
(models + SYSTEM_MESSAGE prompt + engine functions) and `backend/canonical_writing_model.json`.
Two knowledge types are kept deliberately separate: (1) the domain-INDEPENDENT reasoning engine,
(2) the domain-SPECIFIC Canonical Writing Model (data the engine consults).

Legend for field 6 ("explicitly teaches writing concepts"): the whole system, per the M5A boundary,
teaches the FUNCTION of writing concepts (how writing works) and never supplies content.

================================================================================
GROUP A — REASONING CORE & ENGINE INFRASTRUCTURE (domain-independent)
================================================================================

### A1. Developmental Guide Engine (core reasoner / SYSTEM_MESSAGE)
1. Name: Developmental Guide Engine (system prompt `SYSTEM_MESSAGE`, `server.py`).
2. Purpose: Interpret the student's participation as an unfolding process relative to a provisional
   telos; maintain ONE provisional working theory of the developing pedagogical SYSTEM; run the
   recursive loop and emit ONE developmental invitation. Domain-independent as a reasoner.
3. Inputs: telos (A), compact working theory (C), interaction summary (B), selected canonical domain
   sections (data), the student's current draft/reply + previous draft.
4. Outputs: one JSON object = student_facing_invitation + revised telos + revised theory + 2–3
   candidate_invitations + selected_invitation + intervention + observed_reorganization.
5. Writing concepts represented: none intrinsically — holds NO built-in essay sequence; all writing-
   concept vocabulary comes from the M6–M13 framework blocks and the Canonical Writing Model.
6. Explicitly teaches writing concepts: indirectly — it teaches only via the frameworks/domains it
   coordinates; on its own it teaches developmental reasoning, not writing content.
7. Milestone: M1 (foundational loop), refined through all later milestones.

### A2. Recursive Interpretive Loop (10-step loop inside the prompt)
1. Name: Recursive Loop / Master Interpretive Loop.
2. Purpose: The fixed per-turn procedure: state telos → describe organization → note
   differentiation/integration/coordination/tension → supporting & complicating evidence → changes
   since last turn → possible reorganizations → generate 2–3 candidates → select ONE by COHERENCE
   (not optimality) → produce one invitation → revise the whole theory (never append).
3. Inputs: same as A1.
4. Outputs: the structured reasoning that populates the theory + candidates + selected invitation.
5. Writing concepts represented: none directly (process scaffold).
6. Explicitly teaches: no (it is the reasoning procedure, not a writing lesson).
7. Milestone: M1.

### A3. Two-Stage Canonical Retrieval — STAGE A Domain Selector
1. Name: Domain/Section Selector (`_selector_prompt`, `_select_relevant_domains`).
2. Purpose: Choose the 1–3 canonical domains AND the 3–6 relevant SECTION KEYS per domain most
   relevant to the current participation/tension — so the reasoner receives only relevant data.
3. Inputs: compact domain index (name + 1-sentence function + relationships), telos, current primary
   tension, previously-relevant domains, the latest student block.
4. Outputs: JSON `{relevant_domains:[{domain_name, relevant_sections:[...]}]}`.
5. Writing concepts represented: only by reference — it names which writing domains (thesis, paragraph,
   evidence, etc.) are relevant; it carries no concept definitions itself.
6. Explicitly teaches: no (retrieval/routing only).
7. Milestone: introduced with the two-stage performance fix (post-M1); section-level selection added M3.

### A4. Two-Stage Canonical Retrieval — STAGE B Section Retriever
1. Name: Section-level Domain Retriever (`get_relevant_domain_data`, `_build_compact_domain_index`,
   `ALWAYS_KEYS`).
2. Purpose: Fetch each selected domain record filtered to safety-rail sections (domain_name,
   governing_communicative_function, domain_status, prohibitions) + the selected sections; assemble
   the reasoner prompt (`_build_prompt`).
3. Inputs: STAGE A selections; the Canonical Writing Model on disk.
4. Outputs: the trimmed domain data injected into the reasoner prompt.
5. Writing concepts represented: passes through whatever the domains define (see Group E).
6. Explicitly teaches: no (data assembly; the reasoner does any teaching).
7. Milestone: two-stage fix (post-M1); generic section filtering M3.

### A5. Durable Turn Processing (orchestration, non-instructional)
1. Name: Durable reasoning pipeline (`interact`, `_run_engine`, `_run_reasoning`, `_finalize_turn`,
   Turn.status).
2. Purpose: Persist a student turn + a processing placeholder immediately, reason in a background
   task, persist the completed/failed turn — decoupled from the client connection.
3. Inputs: session, InteractRequest (kind, content).
4. Outputs: persisted Turn (complete/failed) + updated theory/telos/interactions.
5–6. Writing concepts / teaches: none (infrastructure only).
7. Milestone: Infrastructure Phase 1 (post-M14).

================================================================================
GROUP B — INSTRUCTIONAL FRAMEWORKS (the writing-concept lenses, M6–M13)
Each is a Pydantic sub-model on DevelopmentalTheory + a prompt block. Inputs to every framework =
the student's draft/reply + telos + prior theory; Outputs = that framework's fields on the theory.
================================================================================

### B1. Communicative Purpose Framework (M6)
- Model: `CommunicativePurpose` (primary, secondary, inferred_from, uncertainty).
2. Purpose: Infer the writer's communicative purpose BEFORE evaluating any writing; every element's
   function is judged relative to it.
5. Writing concepts represented: PURPOSE / communicative function — persuade, inform, explain,
   interpret, analyze, narrate, reflect, evaluate, compare, propose; and the purpose-sensitivity of
   thesis, introduction, organization, evidence, paragraph, transition, conclusion, counterargument,
   reader awareness, revision.
6. Explicitly teaches: YES — purpose and the communicative FUNCTION of writing elements (never a fixed
   structural formula, never content).
7. Milestone: M6.

### B2. Functional Paragraph Framework (M7)
- Model: `ParagraphFunction` (applies, purpose, contribution_to_whole, coherence, development, placement).
2. Purpose: Analyze a paragraph by the WORK it does within the whole, relative to M6 purpose (applies
   only when a paragraph is the unit in focus).
5. Writing concepts represented: PARAGRAPH, topic/controlling idea, paragraph coherence, development
   (explanation/description/interpretation/illustration/comparison/clarification/evidence/reflection),
   placement/role.
6. Explicitly teaches: YES — paragraph FUNCTION and coherence (explicitly NOT a topic-sentence→evidence
   →analysis template; never content).
7. Milestone: M7.

### B3. Functional Evidence Framework (M8)
- Model: `EvidenceFunction` (applies, forms, function, interpretation_gap, quality).
2. Purpose: Treat evidence/support as a communicative resource read relative to purpose, paragraph, and
   the claim it supports; distinguish evidence FROM its interpretation (applies when support is at issue).
5. Writing concepts represented: EVIDENCE / SUPPORT (facts, statistics, quotations, examples, details,
   dialogue, observations, memories), the evidence-vs-interpretation distinction, functional quality
   (relevance/sufficiency/appropriateness/credibility) — never by count.
6. Explicitly teaches: YES — the function of evidence and the evidence↔interpretation relationship
   (never "add more evidence", never invents evidence).
7. Milestone: M8.

### B4. Functional Transition & Coherence Framework (M9)
- Model: `CoherenceFunction` (applies, intended_relationship, level, resources_in_use, reader_can_follow).
2. Purpose: Evaluate the RELATIONSHIPS among ideas (before the wording) at whatever level is in focus
   (applies when continuity/coherence is at issue).
5. Writing concepts represented: TRANSITIONS & COHERENCE; relationships (sequence, cause-effect,
   comparison, contrast, elaboration, concession, emphasis, problem-solution, question-answer,
   chronology); coherence resources (transition words, repetition, conceptual links, parallel structure,
   pronoun reference, progression); four coherence levels (sentence→whole-piece).
6. Explicitly teaches: YES — coherence as communication of relationships (never "add transition words",
   never content).
7. Milestone: M9.

### B5. Functional Conclusion Framework (M10)
- Model: `ConclusionFunction` (applies, functions_in_play, completes_purpose, relationship_to_opening,
  final_understanding).
2. Purpose: Analyze a conclusion as communicative COMPLETION (not summary), relative to M6 purpose
   (applies when an ending is present/at issue).
5. Writing concepts represented: CONCLUSION / ENDING; completion, reinforcing purpose, integration,
   significance, resolution (narrative), answering the opening question, returning to the opening,
   implications, final understanding; the new-idea-in-conclusion caution.
6. Explicitly teaches: YES — communicative completion (explicitly NOT "In conclusion…"/restate-thesis
   formulas; never content).
7. Milestone: M10.

### B6. Reader Construction Framework (M12)
- Model: `ReaderConstruction` (applies, reader_understanding, likely_reader_questions, assumed_knowledge,
  clarification_needed, elaboration_needed, precision_risk, next_reader_need).
2. Purpose: Maintain a dynamic model of what a reasonable NAÏVE reader understands at each point and
   what they need next (applies whenever there is text to read). Feeds all other frameworks.
5. Writing concepts represented: READER / AUDIENCE understanding (as the text builds it — not audience
   adaptation), assumed knowledge vs unsupported assumption, elaboration (as reader understanding, not
   more words), precision/shared meaning, reader questions.
6. Explicitly teaches: YES — clarification, elaboration, precision, reader orientation, inferential gaps
   (never content, never rewriting).
7. Milestone: M12.

### B7. Revision as Development Framework (M13)
- Model: `RevisionDevelopment` (applies, development_detected, primary_growth, communication_change,
  reader_change, remaining_opportunity, transfer_message).
2. Purpose: Read a revision as developmental CHANGE (not editing) by comparing current vs prior draft;
   name the single most important capacity that strengthened; consolidate with transfer (applies when a
   prior draft exists).
5. Writing concepts represented: REVISION (as growth, not edit-counting), developmental trajectory,
   transfer to future writing, consolidation.
6. Explicitly teaches: YES — revision as communicative growth + transfer (never rewrites/generates
   improved versions, never content).
7. Milestone: M13.

================================================================================
GROUP C — ORCHESTRATION & META LAYERS
================================================================================

### C1. Recursive Developmental Scaffolding Controller (M11)
1. Name: Scaffolding Controller — Model `ScaffoldingControl` (current_unit, diagnosed_opportunities,
   primary_target, prioritization_rationale, instructional_mode, postponed, cycle_status,
   stopping_reason, future_opportunity).
2. Purpose: The master orchestrator (every turn): diagnose opportunities ACROSS all frameworks
   (M6–M10, informed by M12/M13), select EXACTLY ONE primary target, postpone the rest, choose an
   instructional mode, run one bounded cycle, and apply stopping/consolidation rules (independence
   request + diminishing-returns are mandatory stops).
3. Inputs: all framework outputs + student response + prior theory.
4. Outputs: the ScaffoldingControl fields; governs which single concept becomes this turn's invitation.
5. Writing concepts represented: none new — it sequences the other frameworks' concepts (unit =
   sentence/paragraph/section/whole paper; modes = developmental_question / explicit_instruction /
   brief_demonstration / guided_revision / reflection / consolidation).
6. Explicitly teaches: no writing concept itself; it decides WHICH concept is taught and HOW, and
   enforces "one target per turn." Never overrides the M5A boundary.
7. Milestone: M11.

### C2. Developmental Integration & Calibration (M14)
1. Name: Integration & Calibration meta-check — Model `IntegrationCalibration` (applies,
   primary_framework, supporting_frameworks, calibration_check, consistency_check, integration_notes).
2. Purpose: Final coherence meta-check (every turn, after M11): confirm frameworks cooperate (never
   compete), unify overlapping diagnoses into one focus, keep the intervention PROPORTIONAL, keep
   priorities CONSISTENT across equivalent situations, note cross-framework transfer.
3. Inputs: all framework outputs + the M11 proposed target.
4. Outputs: the IntegrationCalibration fields (primary_framework aligns with M11 primary_target).
5. Writing concepts represented: none new — operates on the relationships AMONG frameworks.
6. Explicitly teaches: no; guarantees one coherent, calibrated interpretation. Never overrides M11
   one-target, one-invitation, or M5A.
7. Milestone: M14.

================================================================================
GROUP D — INSTRUCTIONAL OUTPUT LAYER
================================================================================

### D1. Developmental Instruction Layer (M5)
1. Name: Developmental Instruction Layer — Model `Intervention` (type, interpretation, instruction,
   consolidation, cultural_resource, timing_rationale, focus, writing_not_content_check).
2. Purpose: Generic (domain-independent) INSIDE→OUTSIDE→INSIDE mediation: each turn choose ONE
   intervention type and, when instructing, introduce a cultural resource and invite its use; includes
   a RESTRAINT rule (teach only when a resource would reorganize present understanding).
3. Inputs: the selected target + student organization + the domain's `cultural_resources` (data).
4. Outputs: Intervention fields; woven into the single student-facing invitation.
5. Writing concepts represented: not concept-specific — the concept taught is whatever cultural resource
   the relevant domain supplies. Intervention types: interpretation_only, instruct_then_invite,
   invite_only, consolidate, postpone_instruction.
6. Explicitly teaches: YES — this is the mechanism by which a cultural resource (writing concept) is
   introduced; the concept content comes from the domains, not the layer.
7. Milestone: M5.

### D2. Writing Instruction Boundary / Anti-Coauthoring Rule (M5A)
1. Name: Writing Instruction Boundary (prompt rule + Intervention.focus + writing_not_content_check).
2. Purpose: Strict boundary — develop better WRITERS, not better essays; teach HOW writing works, never
   decide WHAT the essay says; per-turn self-check; narrow CONTENT MODE only when brainstorming is
   explicitly enabled.
3. Inputs: the proposed invitation.
4. Outputs: focus ('writing'|'content') + a one-line self-audit; rejects/reframes content-coaching.
5. Writing concepts represented: it partitions WRITING targets (purpose, organization, thesis/paragraph
   FUNCTION, reader orientation, transitions, clarity, coherence, rhetorical function, interpreting the
   student's OWN evidence) vs CONTENT (arguments, reasons, examples, new claims, stakes) which is off-limits.
6. Explicitly teaches: it is a constraint on teaching (defines the legitimate teaching space); it does
   not itself teach a concept.
7. Milestone: M5A.

================================================================================
GROUP E — CANONICAL WRITING MODEL (domain-specific knowledge, loaded as DATA)
`canonical_writing_model.json` — 13 domains. These are the cultural resources the engine consults;
they explicitly REPRESENT writing concepts and (for the enriched ones) supply the concept content the
engine teaches. NONE are stages, sequences, or templates.
================================================================================

For every domain — Inputs: selected by STAGE A, filtered by STAGE B. Outputs: injected as prompt data.
Shared base sections: communicative_functions, canonical_writing_resources, functional_evaluation_questions,
possible_differentiations, possible_integrations, common_productive_tensions,
candidate_developmental_invitations, relationships_to_other_domains.

ENRICHED domains (full schema incl. domain_status, governing_communicative_function, reader_needs,
observable_organizations, prohibitions, and a `cultural_resources` teaching section):
- E1. **Opening / Introduction** (M2) — concept: INTRODUCTION/opening; prepares the reader to enter the
  essay's meaning. Teaches: YES (cultural_resources present). Not a hook-background-thesis formula.
- E2. **Central Claim / Thesis** (M3) — concept: THESIS / controlling idea. Teaches: YES. Not a
  one-sentence template, not location-bound.
- E3. **Paragraph Purpose** (M4) — concept: PARAGRAPH function within the whole (31 fields incl. 22
  observable organizations). Teaches: YES. Not a topic-sentence/claim-evidence-analysis template.

BASE/EXEMPLAR domains (base schema; represent the concept as cultural resources but WITHOUT the
`cultural_resources`/`prohibitions`/`domain_status` enrichment):
- E4. Whole Essay Purpose — concept: whole-essay PURPOSE. Represents; base teaching resources only.
- E5. Audience Awareness — concept: AUDIENCE. Represents; base only.
- E6. Evidence — concept: EVIDENCE/support. Represents; base only.
- E7. Interpretation / Reasoning — concept: interpretation/reasoning (evidence→meaning). Represents; base only.
- E8. Organization — concept: whole-piece ORGANIZATION. Represents; base only.
- E9. Transitions — concept: TRANSITIONS. Represents; base only.
- E10. Conclusion — concept: CONCLUSION. Represents; base only.
- E11. Sentence Construction — concept: SENTENCE craft. Represents; base only.
- E12. Word Choice and Voice — concept: DICTION / VOICE. Represents; base only.
- E13. Revision and Reflective Control — concept: REVISION / metacognitive control. Represents; base only.

(6) Explicitly teaches, for Group E: the enriched three (Opening, Thesis, Paragraph Purpose) carry the
`cultural_resources` teaching content the Instruction Layer uses to teach those concepts explicitly. The
other ten currently provide functional description/evaluation resources (represent the concept) but not
the enriched cultural-resource teaching payload.

================================================================================
GROUP F — SUPPORTING STATE / DATA OBJECTS (non-teaching)
================================================================================
- F1. `Telos` (component A, M1): governing pedagogical purpose, task purpose, teacher intentions,
  assignment context, audience/communicative purpose, unresolved ambiguity, telos_changed. Purpose:
  the provisional developmental goal the whole system is organized around. Teaches: no.
- F2. `DevelopmentalTheory` (component C, M1→M14): the single evolving theory aggregating all Group B/C
  framework sub-models + differentiation/integration/coordination, tensions, cultural resources in
  use/potential, alternative interpretations, currently_relevant_domains, uncertainty, changes. Teaches: no.
- F3. `CandidateInvitation` (component D, M1): 2–3 candidate invitations with developmental possibility,
  coherence-with-telos, intended participation, what the AI could learn, risk. Teaches: no (selection input).
- F4. `SelectedInvitation` (component E, M1): the chosen invitation + coherence-based selection basis. Teaches: no.
- F5. `InteractionRecord` (component B, M1): per-turn participation event + candidates + selected +
  intervention + observed_reorganization. Teaches: no (history).
- F6. `TheorySnapshot` (M1): versioned prior telos+theory (never overwritten). Teaches: no.
- F7. `Turn` (M1; status added Infra Phase 1): role/kind/content/status/created_at. Teaches: no.

================================================================================
MILESTONE INDEX (what each milestone introduced)
================================================================================
- M1: Core engine, recursive loop, Telos (A), working theory (C), candidates (D), selected (E),
  interaction records (B), theory snapshots, session/turn state. (Two-stage RAG selector + section-level
  retrieval added as a post-M1 performance fix, extended in M3.)
- M2: Enriched "Opening / Introduction" canonical domain.
- M3: Enriched "Central Claim / Thesis" domain + generic section-level retrieval.
- M4: Enriched "Paragraph Purpose" domain.
- M5: Developmental Instruction Layer (Intervention, 5 types + restraint).
- M5A: Writing Instruction Boundary / Anti-Coauthoring (focus + self-check).
- M6: Communicative Purpose Framework.
- M7: Functional Paragraph Framework.
- M8: Functional Evidence Framework.
- M9: Functional Transition & Coherence Framework.
- M10: Functional Conclusion Framework.
- M11: Recursive Developmental Scaffolding Controller.
- M12: Reader Construction Framework.
- M13: Revision as Development Framework.
- M14: Developmental Integration & Calibration meta-check.
- (Post-M14, non-instructional: Durable Turn Processing; Dev-Panel reorganization; Assignment Prompt +
  teacher-facing panel language. These change infrastructure/UI only, not the instructional architecture.)
