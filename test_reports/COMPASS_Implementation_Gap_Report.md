# Compass — Implementation Gap Report (audit only; no code changed)

Scope: locate, inventory, and operationalize existing architecture. No files changed, renamed, or deleted. Content-searched, not filename-only.

---

## SECTION 1 — Authoritative repository sources

**Finding:** No file named or containing "The Compass Instructional Architecture v2.0" exists in the repo. The named likely-source-of-truth is ABSENT. Do not assume it; the current design lives in code + three docs.

Most authoritative CURRENT sources (in force):
1. `backend/server.py` — the running Milestone engine (SYSTEM_MESSAGE + Pydantic theory models + STAGE-A/B retrieval + interact loop). This is the de-facto instructional source of truth (code = truth).
2. `backend/canonical_writing_model.json` (13 domains) + `backend/instructional_objects.json` (35 elements) — the two live knowledge bases the engine consults.
3. `test_reports/architecture_inventory.md` — accurate, current inventory of the Milestone engine (M1–M14). Matches the code.
4. `memory/COMPASS_PRODUCT_DESIGN_SPEC.md` — current product/UX source of truth (13-screen journey, Phase 1 approved).
5. `memory/CANONICAL_DECISION_LOG.md` — governing decisions (engine + evaluator FROZEN; 66-case benchmark; beta posture).
6. `memory/PRODUCT_MAP.md` — screen/route map (v0), consistent with the design spec.

Later revisions that MODIFY the above:
- `memory/SPRINT1_TESTING_NOTES.md` + `memory/PRD.md` (Sprint 1 / 1.1) introduce a NEW decomposition ("Question / Knowledge / Construction / Composing Loops") and a NEW self-contained engine `backend/assignment_representation.py`. This is newer than architecture_inventory.md and is NOT integrated with the Milestone engine.
- `memory/COMPASS_Stage2_Decomposition_Design.md` + governance docs propose refactors (triage / governance_v2) that are DESIGN-ONLY or behind flags.

---

## SECTION 2 — Existing instructional units

Two parallel representations of writing units exist. Neither is consumed by the newest (Sprint) engine.

**(a) `instructional_objects.json`** — 35 domain-tagged elements. Per-element fields map to the requested headings as follows:
- instructional purpose → `communicative_purpose`
- canonical structures → `performance_structure`
- functional relationships → `related_elements`
- developmental expectations → `indicators_of_control`
- teaching strategies → `next_developmental_moves`
- assessment principles → `recognition_diagnostics`
- entry conditions → **Not yet specified** (no field)
- completion/progress conditions → **Not yet specified** (no field)
- possible next units → `related_elements` (+ `next_developmental_moves`)

**(b) `canonical_writing_model.json`** — 13 domains; 3 ENRICHED (with `cultural_resources`, `prohibitions`, `domain_status`, `governing_communicative_function`), 10 BASE.

Per requested unit (IO object present? / canonical domain? / dedicated M-framework?):
| Unit | instructional_objects.json | canonical_writing_model.json | Dedicated framework |
|---|---|---|---|
| Prewriting | ✗ (absent) | ✗ | Only a `governance_v2` phase trigger. **Not specified as an instructional unit.** |
| Thesis | ✓ "Thesis" / "Central Claim" | ✓ "Central Claim / Thesis" (ENRICHED, M3) | via retrieval |
| Introduction | ✓ "Introduction","Hook/Opening","Background/Context" | ✓ "Opening / Introduction" (ENRICHED, M2) | via retrieval |
| Topic Sentence | ✓ "Topic Sentence" | ✗ (covered by "Paragraph Purpose", ENRICHED M4) | ParagraphFunction (M7) |
| Elaboration | partial ("Explanation/Analysis","Supporting Detail") | ✗ | ReaderConstruction `elaboration_needed` (M12) — **partial** |
| Evidence | ✓ "Evidence" | ✓ "Evidence" (BASE) | EvidenceFunction (M8) |
| Explanation | ✓ "Explanation / Analysis" | ✓ "Interpretation / Reasoning" (BASE) | via M8/purpose |
| Transition | ✓ "Transition" | ✓ "Transitions" (BASE) | CoherenceFunction (M9) |
| Counterargument | ✓ "Counterargument","Rebuttal/Response","Qualification" | ✗ (no domain) | **No dedicated framework** |
| Conclusion | ✓ "Conclusion","Concluding Sentence" | ✓ "Conclusion" (BASE) | ConclusionFunction (M10) |

Full 35-element list (writing domain): Purpose, Thesis, Central Claim, Supporting Claim, Evidence, Explanation/Analysis, Example, Counterargument, Rebuttal/Response, Qualification, Comparison, Contrast, Cause-and-Effect, Classification, Transition, Topic Sentence, Supporting Detail, Concluding Sentence, Paragraph, Introduction, Hook/Opening Move, Background/Context, Conclusion, Title, Sentence, Word Choice, Tone, Audience Awareness, Organization, Coherence, Unity, Voice, Revision, Definition, Concept.

---

## SECTION 3 — Existing code and screens

**Backend (active):**
- `server.py` — Milestone engine. Routes: sessions (create/preview/get), `interact` (the writing dialogue), teacher-configs (create/validate/activate), grade-profiles, assignments-by-code start, telos edit, revision-history, preview-analytics, meaning-maps, tests harness. Reasoning modes: `exhaustive` (DEFAULT/frozen), `triage_experimental`, `governance_v2` (behind flag).
- `assignment_representation.py` — Sprint 1/1.1 "Question Loop" engine, self-contained router `/api/assignment/*`. Wired via `_asgrep.init(...)` + `include_router` (lines 2834–2836). Uses its own Mongo collection `assignment_sessions`. Does NOT consult the two canonical KBs.
- `governance_v2.py` — alternate reasoning path (parked; fails constitutional TC10).
- Knowledge: `canonical_writing_model.json`, `instructional_objects.json` (both live in the Milestone engine).

**Frontend screens (routing in `App.js`, query-param based):**
- `?tests` → TestHarness (dev-only benchmark)
- `?preview` → PublicPreview (3–5 min in-character intro) — EXISTS
- `?represent` → AssignmentRepresentation (Sprint 1/1.1 Question Loop + Developer Mode) — EXISTS, standalone
- `?meaning` → MeaningWorkspace (visual thinking canvas) — EXISTS
- `?bridge` → PreviewBridge — EXISTS
- `?teacher` → TeacherHome (assignment list + create) — EXISTS
- `?config` → TeacherConfig (assignment authoring) — EXISTS
- `?app` / `?dev` → StudioApp = TeacherSetup + **StudentWorkspace** (the real writing workspace, full Milestone engine) + DevelopmentPanel — EXISTS
- default → Landing — EXISTS

**Disconnected / unfinished:** The Question Loop (`?represent`) and the mature StudentWorkspace (`?app`) are separate apps with no bridge between them. Teacher Dashboard (S11) and Revision Analytics (S12) are specified in the design spec but not built as screens (data exists in `revision_history`).

---

## SECTION 4 — Universal algorithm implementation map

The Milestone engine (server.py `interact` → `_run_engine`/`_run_reasoning`) implements the full 10-step sequence end-to-end for the writing-development flow. The Sprint Question Loop implements a NARROW subset (steps 1–2 + a task-inference dialogue) for assignment representation only.

| Step | Milestone engine (StudentWorkspace) | Sprint Question Loop (?represent) |
|---|---|---|
| 1. Identify communicative purpose | ✓ M6 `CommunicativePurpose` + `Telos` (`_run_engine`) | Partial — `analyze_assignment` infers task demands/operations, not a communicative purpose model |
| 2. Identify current writing unit | ✓ `scaffolding_control.current_unit` / `InstructionalReasoning.current_unit_of_writing` | N/A (unit = the assignment itself) |
| 3. Activate canonical functional structure | ✓ STAGE-A `_select_relevant_domains` → STAGE-B `get_relevant_domain_data` + `build_instructional_network` | ✗ Does NOT consult canonical KBs (invents demands via LLM) |
| 4. Interpret learner's current writing | ✓ `DevelopmentalTheory` frameworks (M6–M13) | ✓ `compare_interpretation` / `evaluate_operation` |
| 5. Construct functional representation | ✓ `InstructionalReasoning` + full theory | ✓ demand list w/ category/priority/status |
| 6. Select one high-leverage target | ✓ M11 `primary_target` + M14 calibration | ✓ deterministic `_pick_target` (essential-first) |
| 7. Activate teaching strategy | ✓ `instructional_mode` + `Intervention.type` (5 types) | ✓ 4-level scaffold ladder (task-interpretation) |
| 8. Dialogue; learner performs the work | ✓ single invitation + `interact`; M5A anti-coauthoring boundary | ✓ single studentTask; Sprint 1.1 task/answer boundary |
| 9. Evaluate response/revision | ✓ M13 `revision_development` + `_record_revision` | ✓ `evaluate_operation` (operation_performed + reconstruction) |
| 10. Continue / increase / fade / redirect / conclude | ✓ M11 `cycle_status` + mandatory stops (independence, diminishing returns) | ✓ dynamic action (increase_support/switch_target/next_demand/reconstruction/stop) |

**End-to-end status:** Milestone engine — WORKS end-to-end (durable turn processing, persistence, revision history). Sprint Question Loop — WORKS end-to-end for representation only; then dead-ends (no handoff to writing).

---

## SECTION 5 — Contradictions and duplicated systems (flagged, not resolved)

1. **TWO instructional engines / TWO decompositions.** Milestone M1–M14 (server.py, mature, powers StudentWorkspace) vs the newer "Question/Knowledge/Construction/Composing Loops" (Sprint, `assignment_representation.py`). They are not integrated and use different vocabularies. FLAG: which is the canonical forward architecture?
2. **TWO knowledge bases with overlap.** `canonical_writing_model.json` (13 domains, 3 enriched) and `instructional_objects.json` (35 elements) both represent Thesis/Evidence/Transition/Conclusion/etc. and are both retrieved in STAGE-A. The Sprint engine uses NEITHER. FLAG: consolidate or define clear roles.
3. **THREE reasoning modes.** `exhaustive` (default, FROZEN per Decision Log), `triage_experimental`, `governance_v2` (parked, fails TC10). FLAG: governance_v2 remains behind a flag.
4. **Age/grade target contradiction.** Milestone engine + `TeacherConfiguration`/`GradeProfile` default to **Grade 9** ("grade-9 calibration profile ensured" at startup; design spec = Grade-9 calibration). The newest Sprint 1.1 direction FROZE the target at **Grade 10–12 / competent high-school graduate entering college**. FLAG: these disagree; pick one canonical developmental target.
5. **Missing source-of-truth doc.** "Instructional Architecture v2.0" is referenced as likely-authoritative but is absent. FLAG for the owner to supply or designate a replacement.
6. **Enrichment asymmetry.** Only Opening, Thesis, Paragraph Purpose are enriched (teachable) in the canonical model; Counterargument has no canonical domain and no framework. FLAG: uneven teaching coverage.

---

## SECTION 6 — Missing implementation elements

- **Prewriting** is not specified or implemented as an instructional unit (only a governance phase label).
- **Counterargument, Topic Sentence, Elaboration** exist as base instructional objects but lack enriched canonical teaching resources and/or a dedicated framework.
- **No `entry_conditions` / `completion_conditions`** fields on instructional objects (both marked "Not yet specified").
- **Sprint Question Loop is KB-disconnected** — it free-invents demands rather than reasoning from the existing 35-object KB, so its representations aren't grounded in the canonical model.
- **No bridge** from the Question Loop (representation) to the writing workspace (development) — the learner cannot continue into writing within one flow.
- **Multiple entry paths only partly wired.** Present: teacher-config → code → `start_session_by_code`; direct `?app`; preview. Not unified/entry-aware: existing-draft entry, assignment-prompt-without-draft, selected-writing-component, teacher-feedback, Compass-recommendation, continuation-of-prior-session.
- **"Success = progress on one component" + resume** is supported at the data layer (durable sessions, revision_history) but not surfaced as an explicit session goal/resume experience.
- **Teacher Dashboard (S11) & Revision Analytics (S12)** specified but not built as screens.

---

## SECTION 7 — Recommended smallest next build (proposal — awaiting approval)

**Recommendation A (primary): Bridge the existing Question Loop into the existing writing engine to produce ONE end-to-end, one-component activity.**
- When a learner reaches an "adequate representation" in the Question Loop (`?represent`), offer a single handoff that seeds a StudentWorkspace session (existing Milestone engine) whose `telos`/`current_writing_task` is set to develop exactly ONE component the representation surfaced (e.g., the thesis).
- Reuses: `assignment_representation.py` (representation), `server.py` `create_session`/`interact` (development), `canonical_writing_model.json` + `instructional_objects.json` (already retrieved), durable session persistence (save/resume).
- Adds only minimal glue (a hand-off adapter + one CTA), no new schema, no new engine, no Knowledge Loop.
- Success criterion = meaningful progress on one component, not a finished essay — matches the required definition of success and existing persistence.
- Testable with one realistic task (e.g., the mindset assignment): representation → hand off → one thesis-development cycle → save → resume.

**Recommendation B (smaller alternative, if a bridge is out of scope now): Ground the Question Loop in the existing instructional-object KB.**
- Have `analyze_assignment` retrieve/align its demands to `instructional_objects.json` elements (reusing `get_relevant_instructional_objects`) instead of free-inventing them, so representations are canonical and consistent with the mature engine. Smaller, no UI change, improves fidelity; but does not yet produce the writing hand-off.

Both preserve all working features and add no unnecessary infrastructure. **No build will start until you approve a direction and resolve the Section 5 flags (especially #1 engine/decomposition and #4 grade target).**
