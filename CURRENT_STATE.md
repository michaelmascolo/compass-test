# Compass Current State

> Canonical implementation index for the Compass AI Developmental Writing Studio.
> Describes only what actually exists in the repository. Maintained after significant commits.

## Overview
- **Purpose**: Compass is an AI-powered *developmental* writing studio. It develops the student as a *writer* through scaffolded conversation — it never edits, grades, co-authors, or supplies substantive content. Target learner: capable high-school-graduate level (Grade 9 treated as a scaffolded profile underneath it).
- **Current development phase**: Instructional-object enrichment (Sprint 3) — **PAUSED** for an inventory/reconciliation pass. Engine is frozen; work is additive knowledge-base enrichment + wrapper experiences.
- **Current version**: Milestones M1–M14 complete + Instructional-Object Knowledge Layer + Public Preview + Assignment Representation (Question/Knowledge loops). Instructional-objects schema `v1`; enrichment tag `sprint3-v1`.
- **Last updated**: 2026-06 (auto-maintained after major commits).

## Architecture
- **Backend**: FastAPI (`backend/server.py`, ~3,180 lines) mounting an `APIRouter(prefix="/api")` plus a second router `assignment_representation.py` (`prefix="/api/assignment"`). Async, MongoDB via Motor. Reasoning runs as a decoupled background `asyncio` task (durable processing, not SSE) so client disconnects never lose completed work.
- **Frontend**: React (CRA) single-page app. `src/App.js` is a query-param router (no react-router): `?tests`, `?preview`, `?represent`, `?meaning=<id>`, `?bridge`, `?teacher`, `?config`, `?app`/`?dev`, else Landing. Tailwind + shadcn/ui components in `src/components/ui/`. Academic/editorial theme (Cormorant Garamond + IBM Plex).
- **Database**: MongoDB. Key collections: `sessions`, `assignment_sessions`, `teacher_configs`, `grade_profiles`, `meaning_maps`, `test_runs`.
- **Memory system**: `/app/memory/*.md` — canonical design docs, PRD, decision logs, known limitations, product map. `/app/test_reports/*` — evaluation runs, milestone reviews, iteration reports.
- **AI components**: Single LLM model `claude-sonnet-4-6` via `emergentintegrations` (`EMERGENT_LLM_KEY`). Two prompt roles: the developmental reasoner (`SYSTEM_MESSAGE`) and the automated evaluator (`EVAL_SYSTEM_MESSAGE`). Two data knowledge bases loaded at import: `canonical_writing_model.json` (13 domains) and `instructional_objects.json` (35 objects).
- **External services**: Emergent LLM gateway only. No other third-party integrations.

## Implemented Features
**Developmental engine (M1–M14, FROZEN)**
- One focused developmental invitation per turn; internal `DevelopmentalTheory` updated (merged) each turn with `theory_history` snapshots.
- Communicative Purpose framework (M6); Functional Paragraph (M7); Functional Evidence (M8); Functional Transitions/Coherence (M9); Functional Conclusions (M10).
- Recursive Scaffolding Controller (M11) — exactly ONE target/turn with stopping rules; Reader Construction (M12); Revision-as-Development (M13); Integration & Calibration (M14).
- Anti-coauthoring boundary (M5A): `intervention.focus` must be `writing`; narrow `content` mode only when teacher enables brainstorming.

**Instructional-object knowledge layer**
- STAGE-A retrieval selects 1–3 canonical domains + 1–3 instructional objects per turn; STAGE-B reasons from the retrieved objects + instructional network neighbors.
- Governed Canonical Instruction: teach the concept (canonical term + plain definition tied to the student's writing), require ONE next student act, never rewrite.
- Developmental Memory (not chat memory): per-student `developmental_profile` observations merged across turns and injected into every prompt.

**Assignment Representation (Sprint 1) + Knowledge Loop (Sprint 2)**
- Question Loop: interpret assignment demands before writing; scaffold one high-leverage demand at a time; never answers the assignment.
- Question-Loop → Writing Bridge: handoff readiness + `origin_representation` context passed into the main writing session.
- Knowledge Loop: Stage-1 Orientation extension to build missing conceptual prerequisites without giving answers.

**Public Preview** — in-character 3–5 min entry experience (`?preview`) over the frozen engine via a `PREVIEW_BOOTSTRAP` telos; slimmed output schema for latency; invisible per-turn analytics.

**Teacher configuration** — teacher configs, grade profiles, assignment codes, session creation from config.

**Developer harness** — 66-case automated instructional test suite run through the real pipeline, LLM-graded by a separate evaluator, with run labels, compare-two-runs UI, and JSON/Markdown export.

**Infrastructure** — durable background reasoning, orphaned-turn recovery on boot, 409 guard against concurrent interacts, 2.5s frontend polling.

## Writing Domains
Runtime source: `backend/canonical_writing_model.json` (13 domains, loaded as DATA; NOT stages/sequence/templates). **Fully enriched (32 fields): Opening / Introduction, Central Claim / Thesis, Paragraph Purpose.** Base (9 fields): Whole Essay Purpose, Audience Awareness, Evidence, Interpretation / Reasoning, Organization, Transitions, Conclusion, Sentence Construction, Word Choice and Voice, Revision and Reflective Control.

## Instructional Objects
Runtime source for all: `backend/instructional_objects.json` (schema v1). Data source: parsed from the Writing Elements Chart. All `domain = writing`. Consumed by `server.py` via STAGE-A retrieval + instructional-network injection. Dependencies below = each object's `related_elements` count (network edges). Enrichment status: **ENRICHED** = `sprint3-v1` (adds writer/reader function, discriminations, developmental invitations, followup decisions, transfer, stopping conditions, etc.); otherwise **BASE** schema.

| # | Object | Implemented | Enrichment | Dependencies (edges) |
|---|--------|-------------|------------|----------------------|
| 1 | Purpose | Yes | BASE | 4 |
| 2 | Thesis | Yes | **ENRICHED** | 6 |
| 3 | Central Claim | Yes | BASE | 5 |
| 4 | Supporting Claim | Yes | BASE | 6 |
| 5 | Evidence | Yes | **ENRICHED** | 6 |
| 6 | Explanation / Analysis | Yes | **ENRICHED** | 4 |
| 7 | Example | Yes | BASE | 4 |
| 8 | Counterargument | Yes | BASE | 4 |
| 9 | Rebuttal / Response | Yes | BASE | 4 |
| 10 | Qualification | Yes | BASE | 4 |
| 11 | Comparison | Yes | BASE | 3 |
| 12 | Contrast | Yes | BASE | 3 |
| 13 | Cause-and-Effect Explanation | Yes | BASE | 2 |
| 14 | Classification | Yes | BASE | 3 |
| 15 | Transition | Yes | BASE | 4 |
| 16 | Topic Sentence | Yes | BASE | 5 |
| 17 | Supporting Detail | Yes | BASE | 5 |
| 18 | Concluding Sentence | Yes | BASE | 4 |
| 19 | Paragraph | Yes | BASE | 6 |
| 20 | Introduction | Yes | **ENRICHED** | 5 |
| 21 | Hook / Opening Move | Yes | BASE | 3 |
| 22 | Background / Context | Yes | BASE | 4 |
| 23 | Conclusion | Yes | BASE | 5 |
| 24 | Title | Yes | BASE | 2 |
| 25 | Sentence | Yes | BASE | 4 |
| 26 | Word Choice | Yes | BASE | 4 |
| 27 | Tone | Yes | BASE | 4 |
| 28 | Audience Awareness | Yes | BASE | 5 |
| 29 | Organization | Yes | BASE | 5 |
| 30 | Coherence | Yes | BASE | 5 |
| 31 | Unity | Yes | BASE | 4 |
| 32 | Voice | Yes | BASE | 4 |
| 33 | Revision | Yes | BASE | 5 |
| 34 | Definition | Yes | BASE | 3 |
| 35 | Concept | Yes | BASE | 3 |

- **Runtime location for every object**: retrieved per turn by `get_relevant_instructional_objects()` and injected into the reasoner prompt by `_build_prompt()` in `server.py`.
- **Shared developmental resources** (15, applied across all objects): brief direct explanation, introduction of canonical terminology, contrastive example, parallel example unrelated to the student's topic, comparison of two versions, ordinary-language restatement, naive-reader perspective, focused question, request for explanation, request for revision, partial scaffold, decomposition into a smaller act, reminder of the assignment, connection between local writing and whole-essay purpose, brief consolidation.
- **Enriched count**: 4 / 35. **Base count**: 31 / 35.

## Developmental Engine
- **Question loop** (`assignment_representation.py`): builds the student's representation of assignment demands (interpret → operation → restatement) before any writing; one demand at a time; never answers.
- **Instructional loop** (`server.py` Governed Canonical Instruction, M-frameworks): each turn identifies the unit, confirms purpose, diagnoses across frameworks, selects ONE target, chooses an instruction mode, requires one student act, consolidates. Recorded in `theory.instructional_reasoning` (12 fields).
- **Feedback / knowledge loop**: Knowledge Loop (Sprint 2) assesses/answers/respond/skip to build missing prerequisites without giving answers (`/api/assignment/.../knowledge/*`); developmental profile updates merge student observations across turns.
- **Milestone engine**: the M1–M14 reasoning stack encoded in `SYSTEM_MESSAGE` — FROZEN and benchmarked (66-case evaluator). Not to be modified.
- **Session engine**: `POST /api/sessions/{id}/interact` appends the student turn + a `processing` placeholder, returns in <0.2s, then a background task (`_run_reasoning`) runs STAGE-A selection + STAGE-B reasoning and finalizes the turn. Startup recovers orphaned `processing` turns.
- **Assessment**: developer-only evaluator (`EVAL_SYSTEM_MESSAGE` + `_eval_prompt`) grades each case on 4 Compass-fidelity criteria → pass/partial/fail; persisted to `test_runs`.
- **Reasoning modes** (per session): `exhaustive` (default, frozen path), `triage_experimental`, `governance_v2` (behind flag; parked/not promoted).

## Prompt Library
| Prompt | Location | Used by |
|--------|----------|---------|
| `SYSTEM_MESSAGE` (developmental reasoner, M1–M14 + governed instruction + M5A boundary + engine refinements) | `server.py` ~L678 | STAGE-B reasoning in `interact` / `_run_reasoning` |
| STAGE-A selector prompt (compact domain index + instructional-object index) | `server.py` `_build_prompt` region ~L985 | domain + object retrieval each turn |
| `PREVIEW_OUTPUT_OVERRIDE` + `PREVIEW_TEACHER_NOTES` + `PREVIEW_BOOTSTRAP` | `server.py` ~L1005–1427 | `?preview` slimmed output + bootstrap telos |
| `EVAL_SYSTEM_MESSAGE` + `_eval_prompt` (10 Compass principles, 4-criterion rubric) | `server.py` ~L2529–2630 | developer test harness grading |
| Assignment-representation prompts (interpret / operation / restatement / knowledge) | `assignment_representation.py` | Question & Knowledge loops |
| `COMPASS_CONSTITUTION` / `SYSTEM_CONSTITUTIONAL_RULES` | `server.py` ~L560–620 | governance guardrails |

## UI
- **Landing** (`Landing.jsx`, default route): product entry.
- **Public Preview** (`PublicPreview.jsx`, `?preview`): minimal single-column in-character coach conversation; no dev panel, no scoring, no jargon.
- **Preview Bridge** (`PreviewBridge.jsx`, `?bridge`): preview → real-app handoff.
- **Assignment Representation** (`AssignmentRepresentation.jsx`, `?represent`): Question Loop UI, Knowledge Loop modals, Writing Bridge handoff.
- **Meaning Workspace** (`MeaningWorkspace.jsx`, `?meaning=<id>`): visual thinking canvas / meaning map.
- **Student Workspace + Development Panel** (`StudentWorkspace.jsx` + `DevelopmentPanel.jsx`, `?app`/`?dev`): writing canvas + conversation thread; collapsible teacher-facing dev panel (framework accordions, teacher/research toggle) showing the engine's reasoning.
- **Teacher Home** (`TeacherHome.jsx`, `?teacher`): assignment list + create CTA.
- **Teacher Config / Setup** (`TeacherConfig.jsx`, `TeacherSetup.jsx`, `?config`): configure an assignment (purpose, task, grade profile).
- **Test Harness** (`TestHarness.jsx`, `?tests`): developer suite — run cases, past runs, compare-two-runs, exports.

## Data Model
- **Session** (`sessions`): telos (governing pedagogical purpose, task, assignment), `turns[]` (student + AI, each with `status`: complete/processing/failed/cancelled), `theory` (`DevelopmentalTheory` with the M6–M14 sub-frameworks), `theory_history[]`, `interactions[]`, `developmental_profile[]`, `reasoning_mode`, `is_preview` + `preview_analytics`, `origin_representation`, `gradeCalibration`.
- **AssignmentSession** (`assignment_sessions`): `demands[]` (`AssignmentDemand`), `scaffolds[]`, `interactions[]`, `knowledge_state`, `writing_session_id` (links Question Loop → main writing session).
- **TeacherConfiguration** (`teacher_configs`): class/assignment/learning/guidance/classroom configs + assignment code + grade calibration.
- **GradeProfile** (`grade_profiles`): grade expectations resource (engine TARGET stays `high-school-graduate`; default profile `grade-9`).
- **MeaningMap** (`meaning_maps`): nodes/edges for the visual thinking canvas, linked by session.
- **TestRun** (`test_runs`): case results, verdicts, per-turn decisions, label, export.
- **Relationships**: AssignmentSession → Session via `writing_session_id`; Session.origin_representation carries the Question-Loop context; TeacherConfiguration → Session via create-session/assignment code.

## APIs
**Core session / engine** (`/api`): `GET /`, `POST /sessions`, `POST /sessions/preview`, `GET /sessions/{id}`, `PATCH /sessions/{id}/reasoning-mode`, `PATCH /sessions/{id}/telos`, `POST /sessions/{id}/interact`, `GET /sessions/{id}/revision-history`, `GET /sessions/{id}/preview-analytics`, `POST /sessions/{id}/preview-continue`, `GET /sessions/{id}/export`.
**Compass governance**: `GET /compass/constitution`, `POST /compass/validate-request`.
**Teacher**: `POST /teacher-configs`, `GET/PATCH /teacher-configs/{id}`, `POST /teacher-configs/{id}/validate|activate|create-session`, `GET /grade-profiles`, `GET /grade-profiles/{id}`, `POST /sessions/from-representation`, `GET /teacher/assignments`, `GET /teacher/assignments/{config_id}/sessions`, `POST /assignments/{code}/start`.
**Meaning map**: `GET /meaning-maps/by-session/{id}`, `PUT /meaning-maps/{id}`, `POST /meaning-maps/{id}/coach`, `POST /meaning-maps/{id}/events`.
**Developer test harness**: `GET /tests/cases`, `POST /tests/run`, `PATCH /tests/runs/{id}/label`, `GET /tests/runs`, `GET /tests/runs/{id}`, `GET /tests/runs/{id}/export`.
**Assignment representation** (`/api/assignment`): `POST /sessions`, `GET/PATCH /sessions/{id}`, `POST /sessions/{id}/interpret|operation|restatement`, `GET /sessions/{id}/handoff`, `GET/POST /sessions/{id}/knowledge`, `POST /sessions/{id}/knowledge/assess|respond|skip`, `GET /sessions/{id}/record`, `PATCH /sessions/{id}/developer-notes`, `GET /recommendation-options`, `GET /library`.

## Tests
- **Automated instructional suite**: `backend/test_cases/instructional_test_cases.json` — 66 cases (TC01–TC66) run through the real production pipeline and LLM-graded. Latest full run baseline: 58/8/0 = 87.9% (0 fails). Runs persisted to `test_runs`; UI at `?tests`.
- **Milestone eval harnesses**: `backend/tests/milestone{2..14}_*.py` + `*_results.json` — 24–30 cases per milestone, all previously passed (reports in `test_reports/milestone*_review.md`).
- **Enrichment validation**: `test_reports/{thesis,evidence,explanation,introduction}_enrichment_validation.json` + Sprint 3 reports.
- **QA iterations**: `test_reports/iteration_1.json … iteration_32.json` (testing-agent runs). Latest: iteration_31/32.
- **Loop e2e**: `backend/tests/knowledge_loop_e2e.py`, `bridge_e2e.py`, acceptance drives.

## Outstanding Work
- **Sprint 3 (paused)**: enrich remaining instructional objects — next targets Topic Sentence, Transition, Counterargument, Conclusion (awaiting approval to resume).
- **Reconciliation Report**: full inventory/crosswalk of taught content vs. knowledge homes (requested; not yet written).
- **Construction Loop & Composing Loop** (Sprint 3/4).
- **Teacher Dashboard & Revision Analytics** (Phase III/IV, paused).
- Base→enriched gap: 31/35 instructional objects and 10/13 canonical domains remain at base schema.

## Known Limitations
- **Foothold definition leak** (`KNOWN_LIMITATION_engine_boundary_foothold.md`): under adversarial pushing the coach can occasionally concede a one-line definition of a target concept. Logged, NOT fixed — the leak originates in the frozen 66-case-benchmarked engine prompt; requires a dedicated engine-boundary sprint.
- **Governance v2 (TC10 constitutional failure)**: parked behind the `governance_v2` reasoning-mode flag; not promoted.
- **Latency**: reasoner STAGE-B LLM call dominates (~50–90s/turn); mitigated by durable background processing + polling, not eliminated.
- **Minor carry-over**: `POST /sessions` returns 200 (not 201); some `integration_calibration.supporting_frameworks` values not humanized in teacher view.

## Current Sprint
Inventory / reconciliation pass over the writing-content system (instructional objects + canonical domains) to map exactly what Compass teaches and where the knowledge lives before resuming Sprint 3 enrichment. Engine and evaluator FROZEN — documentation and additive knowledge-base work only. No code changes to the M1–M14 engine.

## Next Recommended Steps
1. Deliver the Instructional Content Reconciliation Report (crosswalk of the 35 objects ↔ 13 domains; completed / pending / documented-but-unimplemented / missing).
2. Resume Sprint 3 enrichment on the highest-leverage base objects (Topic Sentence, Transition, Counterargument, Conclusion) — additive JSON only, re-validate via the harness.
3. Confirm object↔domain naming alignment (e.g. Introduction object ↔ Opening/Introduction domain; Conclusion object ↔ Conclusion domain) to avoid divergence.
4. Schedule a separate, benchmarked engine-boundary sprint for the foothold-definition leak (only when engine changes are explicitly approved).
5. Keep this file (`CURRENT_STATE.md`) updated after each significant commit.

## Repository Map
- `/backend` — FastAPI app. `server.py` (frozen M1–M14 engine, session/engine orchestration, teacher configs, test harness, meaning maps), `assignment_representation.py` (Question/Knowledge loops + Bridge), `governance_v2.py` (parked, flag-gated), `canonical_writing_model.json` (13 domains), `instructional_objects.json` (35 objects), `test_cases/` (66 eval cases), `tests/` (milestone eval + enrichment + e2e scripts), `.env` (MONGO_URL, DB_NAME, EMERGENT_LLM_KEY).
- `/frontend` — React app. `src/App.js` (query-param router), `src/components/` (screens + `DevelopmentPanel`), `src/components/ui/` (shadcn), `src/lib/api.js`, `.env` (REACT_APP_BACKEND_URL).
- `/memory` — canonical design docs, PRD, decision logs, product map, known limitations, test credentials.
- `/test_reports` — evaluation runs, milestone reviews, iteration QA reports, enrichment validations.
- `/tests` — top-level test scaffolding.
- Root — `README.md`, `design_guidelines.json`, `CURRENT_STATE.md` (this file), `test_result.md`, `.gitignore`, `.emergent/`.
