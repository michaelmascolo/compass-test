# Compass — Reconciliation Report (Design-to-Implementation Audit)

> **Purpose.** Determine whether the current implementation faithfully realizes the canonical Compass design. This is an audit, not an inventory: every conclusion is cross-checked against the actual repository (`backend/server.py`, `assignment_representation.py`, the two JSON knowledge bases, `frontend/src/`), `CURRENT_STATE.md`, and the canonical design docs in `/memory`.
>
> **Method.** For each concept: design presence → runtime presence → location → enrichment/completeness → drift → duplication → architectural consistency.
> **Legend.** ✅ Implemented · 🟡 Partial · 📄 Documentation-only (design, not runtime) · ❌ Missing · ⚠️ Drift/inconsistency.
> **Sources cross-checked.** `COMPASS_CANONICAL_SESSION_MODEL.md`, `COMPASS_PRODUCT_DESIGN_SPEC.md`, `COMPASS_StudentWorkspace_Design.md`, `PRODUCT_MAP.md`, `COMPASS_SEMANTIC_OBJECT_CONTRACT.md`, `IMPLEMENTATION_SPEC_Module01_Introductions.md`, `COMPASS_Stage2_*`, `CANONICAL_DECISION_LOG.md`, `KNOWN_LIMITATION_engine_boundary_foothold.md`, and `CURRENT_STATE.md`.

---

# Executive Summary

**Overall implementation completeness.** The **instructional core is complete and faithful**; the **surrounding product is largely design-only**. The frozen Milestone M1–M14 engine, the anti-coauthoring boundary (M5A), the one-target/one-invitation discipline, durable background reasoning, developmental memory, the Question Loop + Knowledge Loop + Writing Bridge, the Public Preview wrapper, and the 66-case developer evaluation harness all exist and run. What remains largely on paper: the multi-screen teacher/student product (auth, class creation, student join, teacher dashboard, revision analytics, assignment-complete), the document-centered anchored Student Workspace, the Meaning-Object overlay architecture, and the proposed constitutional/diagnostic engine decomposition.

**Architectural fidelity — high on the instructional spine, lower on product surface.**
- The **Canonical Session Lifecycle** (Orientation → Target → Invitation → Performance → Interpretation → Decision → Closure) is realized end-to-end. This is the strongest fidelity in the system.
- The **whole-product journey** (Product Design Spec S1–S13 / Product Map S1–S9) is only partially built: Landing, Preview, Bridge, Assignment Representation, Student Workspace, Teacher Config/Home exist; **no authentication, class/roster, student-join, dashboard, or analytics screens exist**.
- The **Student Workspace** diverged from its canonical "coach-the-document / anchored-span" design toward a thread + single marker-reveal model (⚠️ drift, functionally sound).

**Major strengths.**
1. Constitutional integrity holds: anti-coauthoring, no scores/stages, one target per turn — verified across a 66-case benchmark (58/8/0, zero fails).
2. One engine, one rhythm: the Question/Knowledge loops correctly hand off into the single frozen engine rather than spawning parallel coaches (matches the Session Model non-negotiable).
3. Durable, decoupled reasoning + developmental memory are production-grade.

**Major omissions.**
1. **Knowledge-base enrichment is 11% complete** — only 4/35 instructional objects and 3/13 writing domains are enriched.
2. **No product shell**: auth, teacher dashboard, revision analytics, student join, class creation are design-only.
3. **Meaning-Object overlay architecture** (Writing Plan / Draft / Revision / Teacher / Analytics overlays) is documented but unbuilt.
4. **End-of-session recap artifact** and **anchored span coaching** are specified but not emitted/built.

**Highest-priority work remaining.**
1. Resume and finish **instructional-object enrichment** (Topic Sentence, Transition, Counterargument, Conclusion next) — highest instructional leverage, additive, engine stays frozen.
2. Resolve the **object↔domain naming/duplication** ambiguity (Thesis vs Central Claim vs "Central Claim / Thesis" domain).
3. Decide the **product-shell** path (auth + teacher dashboard reading existing `revision_history`) — the biggest gap between design and runtime.

---

# Writing Domains

Runtime source: `backend/canonical_writing_model.json` — 13 domains, loaded as DATA by the engine (`CANONICAL_WRITING_MODEL`), retrieved per turn via STAGE-A selection. Enriched = 32 fields (full `observable_organizations`, tensions, resources, prohibitions); Base = 9 fields.

| Domain | Design status | Runtime status | Enrichment | Missing capabilities | Recommendation |
|---|---|---|---|---|---|
| Opening / Introduction | Canonical | ✅ | ✅ Enriched (32) | — | Reference exemplar; keep as schema template. |
| Central Claim / Thesis | Canonical | ✅ | ✅ Enriched (32) | — | See naming/duplication note (Design Drift D3). |
| Paragraph Purpose | Canonical | ✅ | ✅ Enriched (32) | — | Reference exemplar. |
| Whole Essay Purpose | Canonical | ✅ | 🟡 Base (9) | observable organizations, tensions, resources | Enrich after object round; underpins M6 purpose-first. |
| Audience Awareness | Canonical | ✅ | 🟡 Base (9) | full field set | Enrich; also exists as an instructional object (overlap). |
| Evidence | Canonical | ✅ | 🟡 Base (9) | full field set | Domain base but Evidence *object* is enriched — align them. |
| Interpretation / Reasoning | Canonical | ✅ | 🟡 Base (9) | full field set | Pairs with the enriched Explanation/Analysis object. |
| Organization | Canonical | ✅ | 🟡 Base (9) | full field set | Enrich mid-priority. |
| Transitions | Canonical | ✅ | 🟡 Base (9) | full field set | Enrich alongside the Transition object. |
| Conclusion | Canonical | ✅ | 🟡 Base (9) | full field set | Enrich alongside the Conclusion object. |
| Sentence Construction | Canonical | ✅ | 🟡 Base (9) | full field set | Lower priority. |
| Word Choice and Voice | Canonical | ✅ | 🟡 Base (9) | full field set | Lower priority; overlaps Word Choice/Tone/Voice objects. |
| Revision and Reflective Control | Canonical | ✅ | 🟡 Base (9) | full field set | Pairs with the Revision object; supports Analytics later. |

**Findings.** All 13 designed domains exist in runtime — **zero missing, zero orphaned**. Enrichment is the gap: **3/13 enriched, 10/13 base**. The three enriched domains (Opening/Introduction, Thesis, Paragraph Purpose) are the M2–M4 exemplars and define the target schema. No domain has drifted from design; the base domains are simply thinner data than the canonical schema intends.

---

# Instructional Objects

Runtime source (all): `backend/instructional_objects.json` (schema v1, all `domain=writing`). Retrieved per turn by `get_relevant_instructional_objects()` and injected by `_build_prompt()` in `server.py`; neighbors added via `build_instructional_network()`. **All 35 objects are present in both the design (Writing Elements Chart) and the runtime.** Enrichment marker = `enrichment_version: sprint3-v1`. "Shared resources used" = every object draws from the shared 15-item menu at retrieval time (per-object subsets are not hard-bound — see Shared Resources section). "Dependencies" = `related_elements` edge count.

**Enriched objects (4) — full treatment:**

| Object | Purpose | Design | Runtime | Location | Enrichment | Deps | Missing / Drift | Recommendation |
|---|---|---|---|---|---|---|---|---|
| Thesis | Controlling idea of the whole | ✅ | ✅ | instructional_objects.json + Thesis domain | ✅ sprint3-v1 | 6 | Overlaps Central Claim object + "Central Claim/Thesis" domain (⚠️ D3) | Disambiguate vs Central Claim. |
| Evidence | Support serving a communicative function | ✅ | ✅ | object + Evidence domain (base) | ✅ sprint3-v1 (+evidence_quality_dimensions, genre_variation, look_alike_distinctions) | 6 | Domain still base while object enriched | Enrich the Evidence *domain* to match. |
| Explanation / Analysis | Connect evidence to claim (interpretation) | ✅ | ✅ | object + Interpretation/Reasoning domain (base) | ✅ sprint3-v1 (+instructionally_significant_discriminations) | 4 | — | Pair-enrich the Interpretation domain. |
| Introduction | Orient + motivate the reader | ✅ | ✅ | object + Opening/Introduction domain (enriched) | ✅ sprint3-v1 (+instructional_leverage, cross_object_dependencies, leverage_over_correctness_note) | 5 | Realizes Module-01 spec generically, not as a discrete module (⚠️ D5) | Richest object; use as enrichment template. |

**Base objects (31) — audit table** (Purpose abbreviated; Design ✅ & Runtime ✅ for all; all Base schema; shared-resource access = global menu):

| # | Object | Deps | Notes / Missing implementation / Drift |
|---|---|---|---|
| 1 | Purpose | 4 | Base; conceptually overlaps Whole Essay Purpose domain. Enrich to anchor M6. |
| 2 | Central Claim | 5 | ⚠️ Overlaps Thesis object + Thesis domain — clarify distinction (D3). |
| 3 | Supporting Claim | 6 | Base; pairs with Thesis/Evidence. |
| 4 | Example | 4 | Base; overlaps Evidence. |
| 5 | Counterargument | 4 | **Priority enrichment target.** |
| 6 | Rebuttal / Response | 4 | Enrich with Counterargument. |
| 7 | Qualification | 4 | Base. |
| 8 | Comparison | 3 | Base; overlaps Contrast. |
| 9 | Contrast | 3 | Base; overlaps Comparison — consider merging or cross-linking. |
| 10 | Cause-and-Effect Explanation | 2 | Lowest connectivity (2 edges) — under-networked; add edges. |
| 11 | Classification | 3 | Base. |
| 12 | Transition | 4 | **Priority enrichment target;** pair with Transitions domain. |
| 13 | Topic Sentence | 5 | **Next enrichment target (per sprint plan).** |
| 14 | Supporting Detail | 5 | Base; overlaps Evidence/Example. |
| 15 | Concluding Sentence | 4 | Base; overlaps Conclusion. |
| 16 | Paragraph | 6 | Base object; the Paragraph *domain* is enriched — align. |
| 17 | Hook / Opening Move | 3 | Sub-component of Introduction; used in Preview retrieval. |
| 18 | Background / Context | 4 | Sub-component of Introduction. |
| 19 | Conclusion | 5 | **Priority enrichment target;** pair with Conclusion domain. |
| 20 | Title | 2 | Low priority; under-networked. |
| 21 | Sentence | 4 | Base; overlaps Sentence Construction domain. |
| 22 | Word Choice | 4 | Overlaps Word Choice/Voice domain + Tone/Voice objects. |
| 23 | Tone | 4 | Overlaps Voice/Word Choice. |
| 24 | Audience Awareness | 5 | Object **and** domain both exist (⚠️ duplication D4). |
| 25 | Organization | 5 | Object and domain both exist (⚠️ D4). |
| 26 | Coherence | 5 | Overlaps Transitions/Unity. |
| 27 | Unity | 4 | Overlaps Coherence/Paragraph. |
| 28 | Voice | 4 | Overlaps Word Choice/Tone. |
| 29 | Revision | 5 | Object and Revision domain both exist (⚠️ D4); pairs with future Analytics. |
| 30 | Definition | 3 | Implicated in the foothold known-limitation (defining a target concept = learner's work). |
| 31 | Concept | 3 | Base; abstract; low retrieval frequency. |

**Findings.**
- **Coverage is complete** (35/35 designed objects present in runtime); **enrichment is 4/35 (≈11%)**.
- **Systematic overlap** between the object base and the domain base (Audience Awareness, Organization, Evidence, Revision, Conclusion, Transitions, Paragraph, Sentence, Word Choice/Voice appear in both). This is *by design* (domains = broad retrieval, objects = precise element) per the Session Model, but the two bases are **enriched independently and can drift** (e.g., Evidence object enriched, Evidence domain base). See Technical Debt.
- **Under-networked objects** (Cause-and-Effect=2, Title=2) weaken the instructional-network reasoning; add `related_elements` edges.
- No object has *drifted in meaning*; the drift is structural (dual homes) and completeness (base vs enriched), not semantic.

---

# Shared Instructional Resources

Source: `instructional_objects.json → shared_developmental_resources` (15 items). These are the developmental "moves" the engine may select; they map onto the engine's `instructional_mode` / `Intervention` types.

| Resource | Purpose | Where used | Completeness |
|---|---|---|---|
| brief direct explanation | name/teach a concept concisely | STAGE-B reasoner (instruct_then_invite) | ✅ |
| introduction of canonical terminology | attach a canonical term to a felt function | governed instruction (meaning-before-convention) | ✅ |
| contrastive example | show a distinction | reasoner | ✅ |
| parallel example unrelated to the student's topic | model without co-authoring the student's topic | reasoner (M5A-safe illustration) | ✅ |
| comparison of two versions | make a difference visible | reasoner | ✅ |
| ordinary-language restatement | de-jargon | reasoner | ✅ |
| naive-reader perspective | reader construction (M12) | reasoner | ✅ |
| focused question | developmental_question mode | reasoner (default move) | ✅ |
| request for explanation | elicit reasoning (`explain` turn) | reasoner + UI reply mode | ✅ |
| request for revision | drive the revise loop (`revise` turn) | reasoner + UI | ✅ |
| partial scaffold | supported performance without answers | reasoner | ✅ |
| decomposition into a smaller act | reduce load | reasoner | ✅ |
| reminder of the assignment | answer-the-assignment check | reasoner (drift guard) | ✅ |
| connection between local writing and whole-essay purpose | coherence across scales | reasoner | ✅ |
| brief consolidation | W-A consolidate-by-principle | reasoner (consolidation mode) | ✅ |

**Findings.**
- The menu is **implemented as prompt-available options**, not as a per-object binding: objects do **not** each declare which shared resources apply. The engine chooses from the global menu at reasoning time.
- **Opportunity for consolidation:** the 15 shared resources partially duplicate the engine's `instructional_mode` enum (developmental_question / explicit_instruction / brief_demonstration / guided_revision / reflection / consolidation) and the `Intervention` types (interpretation_only / instruct_then_invite / invite_only / consolidate / postpone_instruction). Three overlapping vocabularies describe the same act. **Recommendation:** map the 15 resources explicitly onto the mode/intervention enums in one table (documentation, no engine change) to remove ambiguity and prevent future divergence.

---

# Developmental Engine

Design source: `COMPASS_CANONICAL_SESSION_MODEL.md` (7-stage lifecycle) + `CANONICAL_DECISION_LOG.md`.

| Component | Design | Status | Where | Assessment |
|---|---|---|---|---|
| **Question Loop** (Orientation Stage 1) | Build an adequate assignment representation; one demand at a time; never answer | ✅ Complete | `assignment_representation.py` (`/api/assignment/*`), `AssignmentRepresentation.jsx` | Faithful. `assess_handoff_readiness` + `build_handoff` implement the readiness gate. |
| **Instructional Loop** (Stages 2–6) | One target → invitation → performance → interpretation → decision | ✅ Complete | `server.py` `SYSTEM_MESSAGE`, `_run_reasoning`, `Intervention`, `scaffolding_control` | Faithful; the M11 controller enforces one target + stopping rules. |
| **Feedback / Knowledge Loop** | Stage-1 variant that builds missing prerequisites without answers; hands into same engine | ✅ Complete | `assignment_representation.py` knowledge endpoints; `AssignmentRepresentation.jsx` (`assessKnowledge/knowledgeRespond/knowledgeSkip`) | Correctly a Stage-1 variant, not a parallel engine (matches non-negotiable #1). |
| **Milestone Engine (M1–M14)** | Frozen, benchmarked reasoning core | ✅ Complete / **FROZEN** | `server.py` `SYSTEM_MESSAGE` (~L678) | Faithful and locked. Known probabilistic boundary leak (foothold) logged, not fixed by directive. |
| **Session Management** (Stage 7 Closure/Resume) | Durable, resumable state; decoupled reasoning | ✅ Complete | `interact` + background `_run_reasoning`, `recover_orphaned_turns`, `GET /sessions/{id}`, `revision-history` | Faithful. ⚠️ **Gap:** explicit end-of-session **recap artifact** not emitted (Session Model §7 "Gaps"). |
| **Assessment Engine** | Developer-only evaluator judging Compass fidelity | ✅ Complete (developer scope) | `EVAL_SYSTEM_MESSAGE`, `_eval_prompt`, `_run_test_suite`, `?tests` | Faithful for developer QA. **Not** a student/teacher assessment surface (by design — no scores to users). |

**Per-component verdicts.**
- **Complete:** Question Loop, Instructional Loop, Knowledge Loop, Milestone Engine, Session Management (core), Assessment (developer).
- **Partial:** Session Management — resumable state ✅ but no recap object; Assessment — exists for developers, no teacher-facing analytic surface yet.
- **Missing:** none of the six core components is absent.
- **Drift:** the **Stage-2 constitutional/diagnostic decomposition** (`COMPASS_Stage2_*`) is 📄 design-only — the engine still runs *all* frameworks every turn (the documented ~33s Stage-2 cost). Not a defect (deliberately deferred, engine frozen), but a known design-vs-runtime divergence.
- **Recommendation:** emit a Stage-7 recap object (additive, no engine change) to close the Session Model gap and unlock the future Teacher Dashboard/Analytics reads.

---

# Prompt Library

| Prompt | Intended role | Runtime | Location | Assessment |
|---|---|---|---|---|
| `SYSTEM_MESSAGE` (reasoner: M1–M14 + governed instruction + M5A + W-A→W-D) | The instructional constitution + diagnosis | ✅ | server.py ~L678 | Faithful; frozen. |
| STAGE-A selector prompt | Retrieve domains + objects | ✅ | server.py `_build_prompt` region ~L985 | Faithful. |
| `EVAL_SYSTEM_MESSAGE` + `_eval_prompt` | Frozen fidelity evaluator (P1–P10) | ✅ | server.py ~L2529–2630 | Faithful; frozen per Decision Log. |
| Preview prompts (`PREVIEW_OUTPUT_OVERRIDE`, `PREVIEW_TEACHER_NOTES`, `PREVIEW_BOOTSTRAP`) | Slimmed preview output + bootstrap arc | ✅ | server.py ~L1005–1427 | Faithful wrapper; no engine change. |
| Assignment-representation prompts (interpret / operation / restatement / knowledge) | Question & Knowledge loops | ✅ | assignment_representation.py | Faithful. |
| `COMPASS_CONSTITUTION` / `SYSTEM_CONSTITUTIONAL_RULES` | Governance guardrails | ✅ | server.py ~L560–620 | Present; surfaced via `/compass/constitution`. |
| **Constitutional-core / conditional-diagnostic split** | Proposed refactor of SYSTEM_MESSAGE | 📄 Documentation-only | `COMPASS_Stage2_Decomposition_Design.md` | **Not implemented** (needs approval + 66-case revalidation). |
| **Governance v2 prompt** | Alternative governance path | 🟡 Behind flag | `governance_v2.py` (reasoning_mode=`governance_v2`) | Parked; not promoted (TC10 failure). |

- **Missing prompts:** none required for current runtime; the constitutional-core split is intended-but-deferred.
- **Duplicated prompts:** the **triage/focused-output override** and **governance_v2** both attempt to scope the frozen reasoner — two experimental paths addressing the same latency/scope concern (⚠️ inconsistency; see Technical Debt).
- **Obsolete prompts:** none confirmed obsolete; `triage_experimental` and `governance_v2` are experimental, flag-gated, and unpromoted — candidates for a keep/retire decision.
- **Inconsistent prompts:** the shared-resource vocabulary vs `instructional_mode` vs `Intervention` type triple (see Shared Resources) is the main terminological inconsistency.

---

# User Interface

Design sources: `COMPASS_PRODUCT_DESIGN_SPEC.md` (S1–S13) and `PRODUCT_MAP.md` (S1–S9). Runtime: `frontend/src/App.js` query-param routing.

| Designed screen | Status | Runtime component / route | Notes |
|---|---|---|---|
| S1 Landing | ✅ | `Landing.jsx` (default) | Exists. |
| S2 Public Preview | ✅ | `PublicPreview.jsx` (`?preview`) | Exists (slimmed wrapper over engine). |
| S3 Preview→Real Bridge | ✅ | `PreviewBridge.jsx` (`?bridge`) | Exists; fires `preview-continue`. |
| S4 Auth (sign in/up) | ❌ | — | **Not implemented.** No auth anywhere in backend or frontend. |
| S5 Role Gateway | ❌ | — | Not implemented. |
| S6 Teacher Home | 🟡 | `TeacherHome.jsx` (`?teacher`) | Exists; lists assignments (no auth/roster behind it). |
| S7 Create Class / Assignment | 🟡 | `TeacherConfig.jsx` / `TeacherSetup.jsx` (`?config`) | Assignment/config exists; **class + join-code creation not built**. |
| S8 Student Join | ❌ | — | Backend has `POST /assignments/{code}/start`; **no join UI**. |
| S9/S10 Student Workspace | 🟡 ⚠️ | `StudentWorkspace.jsx` (`?app`/`?dev`) | Exists but **drifted** from the canonical document-centered anchored-span design (see below). |
| S11 Teacher Dashboard | ❌ 📄 | — | Design-only; data (`revision_history`) exists, no UI. |
| S12 Revision Analytics | ❌ 📄 | — | Design-only; `GET /sessions/{id}/revision-history` exists, no UI. |
| S13 Assignment Complete | ❌ 📄 | — | Design-only. |
| (extra) Meaning Workspace | ✅ | `MeaningWorkspace.jsx` (`?meaning=<id>`) | Exists; not in the S1–S13 spec (semantic-object canvas). |
| (extra) Test Harness | ✅ | `TestHarness.jsx` (`?tests`) | Developer-only. |
| (extra) Dev Panel | ✅ | `DevelopmentPanel.jsx` | Developer/teacher-research surface. |

**Student Workspace drift (⚠️, the most significant UI divergence).**
- **Intended (`COMPASS_StudentWorkspace_Design.md`):** document-centered canvas (~70%), coaching **anchored to a specific sentence/span** via an inline marker→popover, one active marker at a time, revise-in-place, recessed right rail.
- **Implemented:** a draft canvas + **conversation thread**, with a single boolean `markerOpen` that reveals the latest coach turn "marker-first." It is a thread-with-reveal, **not** span-anchored inline coaching. Functionally sound and engine-faithful, but it is the "chat about the document" pattern the design explicitly warns against.
- **Recommendation:** treat the anchored-span workspace as a defined Phase-3 build; the engine already emits a single target per turn, so the change is UI-only (no engine/API change).

**Workflow findings.** Implemented: Landing→Preview→Bridge, Assignment Representation (Question/Knowledge loop → Bridge → Workspace), Meaning Workspace, developer Test Harness. Partial: teacher setup (config without accounts/classes). Missing: the entire **authenticated product journey** (auth → class → join → dashboard → analytics → complete).

---

# Data Model

Design source: `COMPASS_SEMANTIC_OBJECT_CONTRACT.md` + Session Model + implemented Pydantic models in `server.py`/`assignment_representation.py`.

| Structure | Design | Runtime | Location | Assessment |
|---|---|---|---|---|
| `Session` (telos, turns[], theory, theory_history, interactions, developmental_profile, revision_history, origin_representation, is_preview/preview_analytics, reasoning_mode, gradeCalibration) | Canonical writing session | ✅ | `sessions` | Faithful, rich. |
| `AssignmentSession` (demands[], scaffolds[], knowledge_state, writing_session_id) | Orientation representation | ✅ | `assignment_sessions` | Faithful; links to Session. |
| `DevelopmentalTheory` (M6–M14 sub-frameworks + instructional_reasoning + developmental_profile_update) | Internal developmental state | ✅ | embedded in Session | Faithful. |
| `TeacherConfiguration` (class/assignment/learning/guidance/classroom) | Teacher framing (Stage 1) | ✅ | `teacher_configs` | Exists; **not tied to an authenticated teacher**. |
| `GradeProfile` | Support profile under the HS-graduate target | ✅ | `grade_profiles` | Seeded (`grade-9`); target stays `high-school-graduate`. |
| `MeaningMap` (objects/groups/connections/events) | Canonical semantic objects | ✅ | `meaning_maps` | Object identity/immutability implemented per contract. |
| **Meaning-Object overlays** (Writing Plan / Draft / Revision / Teacher / Analytics) | One object, many overlays | 📄 Documentation-only | — | **Not built** (contract says "document only, do not build yet"). |
| **Reserved MeaningObject fields** (creation_timestamp, creator, lineage) | Immutable identity for multi-user/versioning | 📄 Documentation-only | — | Reserved, not implemented (as intended). |
| **Session recap artifact** | Stage-7 closure summary | ❌ | — | Missing (Session Model gap). |
| `User` / account | Teacher/Student identity | ❌ | — | **No user/account model exists.** |

**Findings.**
- **Missing fields/structures:** no `User`/account model; no overlay stores; no recap object; MeaningObject `creation_timestamp/creator/lineage` reserved-only.
- **Duplicated structures:** the **two knowledge bases** (domains vs objects) encode overlapping writing concepts (see Instructional Objects / Design Drift D4). Within models, `InteractionRecord` is defined in *both* `server.py` and `assignment_representation.py` (same name, different shapes) — ⚠️ naming collision risk.
- **Inconsistencies:** `TeacherConfiguration` and sessions presuppose a teacher, but there is no authenticated owner linking them — configs/sessions are effectively anonymous/localStorage-scoped (`dws_session_id`).

---

# API Surface

Backend routers: `api_router` (`/api`) in `server.py`; `router` (`/api/assignment`) in `assignment_representation.py`. (Full list in `CURRENT_STATE.md`.)

**Supports the intended architecture?** Yes for the **instructional spine**; no for the **product shell**.
- ✅ Session lifecycle, interact/durable processing, telos, revision-history, preview, teacher-config, grade-profiles, assignment representation + knowledge loop, from-representation bridge, meaning-maps, developer test harness — all present and coherent with the Session Model.
- ❌ **Missing endpoints for designed product:** authentication (sign-up/in/session), user/account CRUD, class creation + roster, teacher dashboard aggregation (class-level participation), revision-analytics aggregation, assignment-complete. `POST /assignments/{code}/start` exists but has **no matching join UI**.
- ⚠️ **Potentially unnecessary / experimental:** `PATCH /sessions/{id}/reasoning-mode` exposing `triage_experimental` and `governance_v2` — parked paths; keep only if the experiments continue.
- **Minor:** `POST /sessions` returns **200, not 201** (documented carry-over).

**Recommendation.** The dashboard/analytics endpoints can be **thin read aggregations** over existing `sessions.revision_history` / `developmental_profile` — no new instructional logic (matches Session Model "Teacher Dashboard = read surface"). Auth is the true new subsystem and should be scoped explicitly.

---

# Design Drift

**D1 — Student Workspace: document-centered anchored coaching → thread + marker-reveal.** *Intended:* coach the document with one span-anchored inline marker (`COMPASS_StudentWorkspace_Design.md`). *Current:* draft canvas + conversation thread with a single `markerOpen` reveal of the latest turn. *Reason:* the thread model was the earliest workspace and predates the Phase-3 anchored design; the anchored build was deferred. *Recommendation:* build the anchored-span workspace (UI-only; engine already emits one target/turn).

**D2 — Product journey: 13-screen teacher/student product → instructional slices only.** *Intended:* Landing→Preview→Bridge→**Auth**→Teacher Home→**Create Class**→**Student Join**→Workspace→**Dashboard**→**Analytics**→**Complete**. *Current:* the non-authenticated instructional pieces exist; auth/class/join/dashboard/analytics/complete do not. *Reason:* focus stayed on the frozen instructional engine per directive; product shell was mapped (Product Map v0) but not built. *Recommendation:* sequence the shell starting with auth + a read-only teacher dashboard.

**D3 — Thesis vs Central Claim vs "Central Claim / Thesis".** *Intended:* a single controlling-idea concept. *Current:* **two objects** (`Thesis`, `Central Claim`) plus one **domain** named "Central Claim / Thesis" — Thesis is enriched, Central Claim is base. *Reason:* the Writing Elements Chart listed both; the canonical domain merged them. *Recommendation:* declare one as canonical (or make Central Claim an alias of Thesis) to prevent retrieval ambiguity and split enrichment.

**D4 — Dual knowledge bases with overlapping concepts.** *Intended (Session Model):* domains = broad retrieval, objects = precise element — complementary. *Current:* ~9 concepts exist in *both* bases (Audience Awareness, Organization, Evidence, Revision, Conclusion, Transitions, Paragraph, Sentence, Word Choice/Voice) and are **enriched independently**, so they can and do diverge (Evidence object enriched, Evidence domain base). *Reason:* the object layer was added later on top of the domain model. *Recommendation:* keep both layers but enrich them **as pairs** and add a documented crosswalk (object ↔ domain) so they never drift.

**D5 — Module-01 Introductions: discrete decision module → emergent engine behavior.** *Intended:* an explicit introduction module with a prerequisite gate and H1–H6 hypothesis selection. *Current:* introductions are handled **generically** by the frozen engine using the enriched Introduction object — no discrete module logic. *Reason:* the engine is frozen and domain-independent; encoding a bespoke module would fork it. *Recommendation:* accept emergent handling; verify the H1–H6 behaviors are covered by benchmark cases rather than building a separate module.

**D6 — Stage-2 decomposition & latency plan.** *Intended (design docs):* factor the frozen prompt into a constitutional core + conditional diagnostic layer to cut ~33s Stage-2 cost. *Current:* all frameworks run every turn. *Reason:* touching the frozen prompt requires approval + 66-case revalidation. *Recommendation:* keep deferred; revisit only if latency becomes a launch blocker.

---

# Missing Features (ranked by implementation priority)

1. **P0 — Instructional-object/domain enrichment completion.** 31/35 objects + 10/13 domains are base. Highest instructional leverage; additive; engine frozen. Next: Topic Sentence, Transition, Counterargument, Conclusion.
2. **P0 — Authentication + teacher/student accounts.** Nothing persists to an owner; blocks the entire authenticated product journey (D2). New subsystem — scope explicitly (integration).
3. **P1 — Teacher Dashboard + Revision Analytics (read surfaces).** Data exists (`revision_history`, `developmental_profile`); needs aggregation endpoints + UI. Delivers the core teacher value proposition ("see what you couldn't before").
4. **P1 — Class creation + Student Join UI.** Backend `assignments/{code}/start` exists; needs create-class (join code) + join screen.
5. **P1 — Anchored-span Student Workspace (D1).** UI-only realization of the canonical document-centered design.
6. **P2 — End-of-session recap artifact (Stage-7).** Additive; unlocks dashboard/analytics summaries.
7. **P2 — Assignment Complete screen (S13).** Developmental closure surface.
8. **P3 — Meaning-Object overlays** (Writing Plan/Draft/Revision/Teacher/Analytics) + reserved identity fields. Explicitly "do not build yet."
9. **P3 — Object↔domain crosswalk doc + shared-resource/mode mapping** (removes D3/D4 and the vocabulary triple).

---

# Technical Debt

**Architectural debt.**
- **Two experimental reasoning paths** (`triage_experimental`, `governance_v2`) behind a `reasoning_mode` flag, both attempting to scope the frozen engine; `governance_v2` is parked (TC10 failure). Decide keep-vs-retire to avoid dead paths.
- **Dual knowledge bases** enriched independently (D4) — the largest structural debt; risks silent divergence.
- **No account/ownership layer** underneath teacher configs/sessions.

**Duplicated logic / structures.**
- `InteractionRecord` defined in both `server.py` and `assignment_representation.py` (same name, divergent shapes).
- Overlapping concepts across the object base, the domain base, and the sub-component objects (Hook/Background inside Introduction; Comparison/Contrast; Coherence/Unity; Word Choice/Tone/Voice).
- Three vocabularies for the same coaching act: 15 shared resources ↔ 6 `instructional_mode`s ↔ 5 `Intervention` types.

**Inconsistent naming.** Thesis/Central Claim (D3); object vs domain names for the same concept (Evidence, Organization, Audience Awareness, Revision, Conclusion, Transitions).

**Temporary implementations.**
- Session identity via `localStorage dws_session_id` (no real auth).
- `POST /sessions` returns 200 not 201.
- Some `integration_calibration.supporting_frameworks` values not humanized in teacher view.
- Question Loop "Continue to Knowledge" originated as a Sprint-2 placeholder (now wired).

**Opportunities for simplification.**
- Collapse the coaching-act vocabularies into one documented mapping.
- Enrich objects+domains as pairs and publish the crosswalk.
- Retire or promote the experimental reasoning modes.

---

# Priority Recommendations (highest → lowest)

1. **Finish instructional enrichment (P0).** Enrich Topic Sentence, Transition, Counterargument, Conclusion (then remaining base objects), pairing each object with its domain. Additive JSON only; re-validate via the 66-case harness vs baseline `fd0dec0c`. Engine stays frozen.
2. **Resolve Thesis/Central Claim + publish the object↔domain crosswalk (P0/P1, cheap).** Documentation + minor JSON alias; removes the clearest retrieval ambiguity (D3/D4).
3. **Introduce authentication + accounts (P0).** Route via the integration process; unblocks the authenticated product journey (D2). Scope explicitly with the user before building.
4. **Build the Teacher Dashboard + Revision Analytics as read surfaces (P1).** Thin aggregation endpoints over existing `revision_history`/`developmental_profile` + UI. Delivers the headline teacher value.
5. **Class creation + Student Join UI (P1).** Wrap the existing `assignments/{code}/start` endpoint.
6. **Realize the anchored-span Student Workspace (P1, UI-only).** Close D1 without touching the engine.
7. **Emit the Stage-7 recap artifact (P2).** Additive; feeds #4 and closes the Session Model gap.
8. **Decide keep-vs-retire for `triage_experimental` / `governance_v2` (P2).** Remove dead reasoning paths or commit to promoting them (with benchmarking).
9. **Consolidate the coaching-act vocabularies and de-duplicate `InteractionRecord` (P3).** Simplification/hygiene.
10. **Defer Meaning-Object overlays and the constitutional/diagnostic engine split (P3)** until explicitly scheduled and (for the engine) approved + re-benchmarked.

---

_Audit basis: cross-checked against `backend/server.py`, `backend/assignment_representation.py`, `backend/instructional_objects.json` (35 objects, 4 enriched), `backend/canonical_writing_model.json` (13 domains, 3 enriched), `frontend/src/App.js` + components, `CURRENT_STATE.md`, and the `/memory` canonical design documents. No runtime behavior was changed to produce this report. Implemented features are distinguished from planned features, and documentation is distinguished from runtime behavior throughout._
