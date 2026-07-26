# Compass Instructional Object Specification

> **Canonical developer reference for the Compass instructional-object schema.**
> This document explains the SCHEMA — the meaning, contents, and intended use of every field — not the individual objects. It is the authority for how instructional objects are structured and how new ones must be created. For the current per-object inventory and enrichment status see `CURRENT_STATE.md`; for the enrichment audit trail see `test_reports/SPRINT3_CANONICAL_ENRICHMENT_REPORT.md`.

## 1. What an instructional object is

An **instructional object** is a structured knowledge record describing one canonical element of writing (e.g. Thesis, Topic Sentence, Transition). Objects live in **`backend/instructional_objects.json`** under the `instructional_objects` array. They are **DATA, not code** — the frozen Milestone M1–M14 engine (`backend/server.py`) reads them at import and injects selected objects into its reasoning prompts. Objects therefore shape *what the coach can recognize, name, and invite* — they never contain student-facing answers, essay content, or pedagogy that overrides the engine.

**Non-negotiables**
- Objects describe the *writer's developmental work*, never the substantive content of any assignment.
- Editing an object changes engine behavior indirectly (via retrieval + prompt injection). It must never require editing the engine, prompts, evaluator, or architecture.
- The **canonical source of truth** for instructional content is the **Writing Elements Chart**. Objects must faithfully reflect it; they must not invent instructional theory.

## 2. File structure

```
instructional_objects.json
├── schema_version                      # string
├── note                                # provenance note for the whole KB
├── shared_developmental_resources[]    # 15 shared coaching "moves" (see §6)
└── instructional_objects[]             # the 35 objects
```

Each object is a JSON dictionary. There are three field tiers: **identity/base**, **canonical (from the chart)**, and **deeper enrichment (Compass pattern)**.

## 3. Field reference

### 3.1 Identity & base fields
| Field | Type | Purpose | Used by |
|---|---|---|---|
| `element` | string | Canonical name of the object (e.g. `"Topic Sentence"`). Primary key. | Retrieval index, network edges |
| `domain` | string | Coarse grouping; currently `"writing"` for all. | Retrieval filtering |
| `aliases` | string[] | Alternate names/synonyms a learner or teacher might use. | STAGE-A retrieval matching |
| `communicative_purpose` | string | One-line statement of the element's job in communication. Compass-authored (predates chart adoption). | STAGE-A index, target selection |
| `common_obstacles` | string[] | Legacy list of typical failure modes (Compass-authored). Superseded in practice by `common_difficulties` but retained. | Diagnostics (secondary) |
| `related_elements` | string[] | **The instructional network.** Names of neighboring objects. Defines retrieval-network edges. | STAGE-B neighbor injection, `followup_decisions` change-target |
| `developmental_resources` | (varies) | Legacy per-object resource hints. | Instructional invitation (secondary) |

> **Do not modify `related_elements`** unless the canonical chart explicitly requires a new relationship. The network is load-bearing for retrieval.

### 3.2 Canonical fields (VERBATIM from the Writing Elements Chart)
These five fields are the heart of the object and must be copied **verbatim** from the chart. Provenance = `canonical_verbatim`.

| Field | Chart column | Contents | Engine use |
|---|---|---|---|
| `definition` | *Definition — What is it?* | What the element is, in the present context. | STAGE-A retrieval index; interpretation |
| `performance_structure` | *Performance Structure* | The element's parts and how it is constructed. | Interpretation — the gap between the learner's attempt and the canonical function |
| `recognition_diagnostics` | *Recognition & Diagnosis* | The diagnostic questions that reveal whether/how the element is working. | Diagnostics — how the coach reads the current draft |
| `next_developmental_moves` | *Next Developmental Move* | The primary developmental invitation for this element. | Instructional invitation (the canonical "one next move") |
| `indicators_of_control` | *Indicators of Increasing Control* | What growing mastery looks like. | Interpretation of degree-of-control; stopping conditions |

### 3.3 Deeper enrichment fields (Compass pattern)
These extend the canonical content into the shape the pilot objects (Thesis, Evidence, Explanation/Analysis, Introduction) established. They are derived **conservatively** from the canonical fields + the pilot pattern. Each carries a provenance tag (see §4).

| Field | Type | What belongs here | Engine use |
|---|---|---|---|
| `reader_function` | string | What the element does *for the reader*. | Target selection + interpretation (why it matters now) |
| `writer_function` | string | What producing the element does *for the writer's development*. | Target selection + interpretation |
| `functional_relationships` | object `{purpose, reader, neighboring_components, overall_organization}` | How the element relates to the whole-essay purpose, the reader, its neighbors, and the overall structure. | Target selection (bottleneck vs neighbor) + sequencing |
| `common_difficulties` | `[{type, description}]` | The characteristic ways the element fails, derived from `recognition_diagnostics`. | Diagnostics — name what the learner is attempting |
| `productive_misconceptions` | `[{misconception, why_productive, leverage}]` | Errors that are developmentally useful; how to build on them rather than correct them. | Instructional invitation (turn error into a step) |
| `indicators_of_development` | object `{early, partial, independent, flexible}` | A four-stage view of control. `independent`/`flexible` = the chart's Indicators of Increasing Control (verbatim); `early`/`partial` = conservative interpolation. | Interpretation (degree_of_student_control) + stopping |
| `recognition_diagnostics_detailed` | object `{attempting, control_level, likely_misconception, next_move}` | A structured expansion of `recognition_diagnostics` for the diagnosis step. | Diagnostics |
| `developmental_invitations` | `[{type, purpose, use_when, avoid_when}]` | The menu of moves the coach may offer for this element (only ONE is used per turn). | Instructional invitation |
| `followup_decisions` | `[{after, consider}]` | Decision logic for the turn AFTER an invitation (continue / increase support / change target / conclude / stop). | Instructional decision |
| `revision_strategies` | string[] | Functional revision moves (re-seeing, not editing), derived from `performance_structure`/`recognition_diagnostics`. | Instructional invitation for revision |
| `stopping_conditions` | string[] | When to stop working this element (mastery, diminishing returns, another element now primary, independence request, teacher override). | Stopping / session closure |
| `transfer` | object `{other_genres, other_assignments, other_disciplines, future_writing}` | How the underlying capability generalizes beyond the current task. | Session closure (consolidation + transfer note) |
| `engine_usage` | object | A field→engine-stage map documenting how the object's fields are consumed. Object-independent boilerplate. | Documentation (reused from pilots) |

### 3.4 Metadata fields
| Field | Type | Purpose |
|---|---|---|
| `enrichment_version` | string | `"sprint3-v1"` (4 pilots) or `"sprint3-canonical-v1"` (31 chart-enriched). Presence marks an object as enriched. |
| `canonical_source` | string | `"Writing Elements Chart"` for chart-enriched objects. Absent on the 4 pilots. |
| `field_provenance` | object | Per-field provenance class (see §4). REQUIRED on every enriched object. |

## 4. Provenance classes (`field_provenance`)

Every field on an enriched object is classified so future developers and reviewers can see what is authoritative vs interpreted:

| Class | Meaning | Applies to (typical) |
|---|---|---|
| `canonical_verbatim` | Exact text from the Writing Elements Chart. | the 5 canonical fields; `indicators_of_development.independent`/`flexible` |
| `canonical_derived` | Restatement or decomposition of chart content; low interpretation. | `common_difficulties`, `recognition_diagnostics_detailed`, `revision_strategies` |
| `pattern_interpreted` | Conservative inference from the chart + pilot pattern. **Flagged for human review.** | `reader_function`, `writer_function`, `functional_relationships`, `productive_misconceptions`, `developmental_invitations`, `followup_decisions`, `stopping_conditions`, `transfer`, and `indicators_of_development.early`/`partial` |
| `pattern_boilerplate` | Object-independent structure reused verbatim from the pilots. | `engine_usage` |
| `mixed (...)` | Per-subfield provenance within one field. | `indicators_of_development` |

**Rule:** never fabricate. If a field cannot be populated without genuine invention beyond what the chart + pilots + pattern support, leave it blank and record the reason in `field_provenance` (e.g. `"blank — insufficient canonical basis"`) rather than inventing content.

## 5. How objects are used by the retrieval and instructional systems

1. **STAGE-A (retrieval).** Each turn, the engine builds a compact index from `element`, `definition`, `communicative_purpose`, and `aliases`, and selects 1–3 relevant objects for the learner's current writing. `related_elements` pulls in neighbors.
2. **STAGE-B (reasoning).** The selected objects (full records) are injected into the reasoner prompt. The engine uses `reader_function`/`writer_function` and `functional_relationships` to decide *whether this element is the current bottleneck*, `recognition_diagnostics(_detailed)` + `common_difficulties` to *diagnose*, and `developmental_invitations` + `next_developmental_moves` to choose **exactly one** invitation.
3. **Follow-up & stopping.** `followup_decisions` and `stopping_conditions` govern the next turn and when to release the target. `indicators_of_development` calibrates degree-of-control.
4. **Closure.** `transfer` feeds end-of-session consolidation.

The engine remains **frozen**: objects supply *knowledge*, the engine supplies *behavior*. Richer objects make diagnosis and invitations sharper; they never add new engine rules.

## 6. Shared developmental resources

`shared_developmental_resources` (15 items) is the global menu of coaching moves available to the engine (e.g. *brief direct explanation, contrastive example, focused question, request for revision, partial scaffold, brief consolidation*). Objects do **not** each bind their own subset; the engine chooses from the global menu at reasoning time. These overlap conceptually with the engine's `instructional_mode` and `Intervention` enums — keep the three vocabularies aligned; do not add a fourth.

## 7. Authoring a new instructional object (checklist)

When adding or (re-)enriching an object, follow this exactly:

1. **Locate the canonical entry** in the Writing Elements Chart (or the approved canonical source). If none exists, stop — do not invent instructional content.
2. **Set identity fields**: `element` (canonical name), `domain`, `aliases`. Set `related_elements` **only** from a canonical relationship; otherwise leave the existing network untouched.
3. **Copy the 5 canonical fields VERBATIM** (`definition`, `performance_structure`, `recognition_diagnostics`, `next_developmental_moves`, `indicators_of_control`) → provenance `canonical_verbatim`.
4. **Derive the deeper fields conservatively** following the pilot pattern (§3.3), drawing only on: the chart entry, the four pilot objects, and this specification. Keep lists tight (≈2–5 items) and grounded in the canonical text.
5. **Set `indicators_of_development`**: `independent`/`flexible` = chart Indicators (verbatim); `early`/`partial` = conservative interpolation.
6. **Reuse `engine_usage`** verbatim from the pilots (`pattern_boilerplate`).
7. **Record `field_provenance` for every field** (§4). Flag anything that required interpretation. Leave a field blank + note it rather than inventing.
8. **Set metadata**: `enrichment_version` and `canonical_source`.
9. **Do NOT** touch the engine, prompts, evaluator, retrieval network (beyond canonical edges), architecture, or the four pilot objects (unless correcting a genuine error).
10. **Validate**: JSON parses; all fields present and non-empty (or explicitly blank-with-reason); canonical fields byte-match the chart; backend reloads and the engine index builds; `related_elements` unchanged. Update `CURRENT_STATE.md` counts and the Sprint validation report.

## 8. Consistency guarantees

- **Additive & data-only:** enrichment changes JSON consumed by prompts; it never changes engine logic.
- **Faithful to the chart:** canonical fields are verbatim; deeper fields are conservative and provenance-tagged.
- **Reviewable:** `field_provenance` makes every interpretation visible; `pattern_interpreted` fields are the review queue.
- **Stable network:** `related_elements` changes only for canonical reasons.
- **Frozen engine:** no object may encode behavior that belongs to the M1–M14 engine, the evaluator, or the anti-coauthoring boundary.

_This specification is the canonical schema reference for Compass instructional objects. Keep it updated when the schema (not the individual objects) changes._
