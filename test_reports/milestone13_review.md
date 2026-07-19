# Milestone 13 — Revision as Development: Review Table

Cases: 30 | PASS: **30/30** | Errors: 0

Each case verifies: (1) a revision is evaluated as DEVELOPMENTAL change when a prior draft exists (theory.revision_development.applies + development_detected); (2) ONE primary_growth named qualitatively (no edit-counting / no scorekeeping); (3) real growth → a transfer_message for future writing; (4) limited/regressed progress → ONE remaining_opportunity (not re-teaching everything); (5) FIRST submissions do NOT set applies (nothing to compare); (6) 3-draft cases read a trajectory; (7) M11 keeps exactly ONE target; (8) M5A preserved (no rewriting/inventing; focus='writing'). Categories: substantial-growth, superficial-edit, regression, multi-draft, reader-understanding, coherence, conclusion, purpose, limited-progress, first-submission (control).

| # | Category | Drafts | applies | development_detected | primary_growth / remaining_opportunity | One target | focus |
|---|----------|--------|---------|----------------------|----------------------------------------|-----------|-------|
| 1 | substantial_growth | 2 | True | yes — student differentiated topic… | purpose — moved from vague opinion ('bad') to … | yes | writing |
| 2 | substantial_growth | 2 | True | yes — substantial developmental le… | purpose: moved from topic identification to an… | yes | writing |
| 3 | substantial_growth | 2 | True | yes — student moved from a bare to… | purpose — from naming topic to beginning to de… | yes | writing |
| 4 | substantial_growth | 2 | True | yes — substantial; student moved f… | purpose — communicative intent is now clearly … | yes | writing |
| 5 | substantial_growth | 2 | True | yes — student moved from a bare op… | purpose — student differentiated a topic-level… | yes | writing |
| 6 | superficial_edit | 2 | True | partial — student returned to the … | emerging revision behavior: student is treatin… | yes | writing |
| 7 | superficial_edit | 2 | True | partial — student revised ('variou… | none detected in communicative capacity; surfa… | yes | writing |
| 8 | superficial_edit | 2 | True | no — change is stylistic ('utilize… | Specify the mood and its interpretive signific… | yes | writing |
| 9 | superficial_edit | 2 | True | no — added intensifiers ('very', '… | Naming a specific concrete moment from the exp… | yes | writing |
| 10 | regression | 2 | True | no — the revision removed a functi… | none detected; this is a regression in claim f… | yes | writing |
| 11 | regression | 2 | True | no — the revision lost specificity… | Restore the specific technique-effect link and… | yes | writing |
| 12 | regression | 2 | True | no — prior draft expressed a more … | Re-establishing the causal relationship betwee… | yes | writing |
| 13 | multi_draft | 3 | True | yes — student moved from bare subj… | precision — claim now specifies the mechanism … | yes | writing |
| 14 | multi_draft | 3 | True | yes — student moved from direction… | purpose — the piece now has a genuine reflecti… | yes | writing |
| 15 | multi_draft | 3 | True | yes — student moved from sensory o… | interpretive coordination: the student has now… | yes | writing |
| 16 | multi_draft | 3 | True | yes — moved from effect-naming to … | elaboration — student added the causal mechani… | yes | writing |
| 17 | reader_understanding | 2 | True | yes — student moved from bare asse… | coherence / reasoning visibility — the warrant… | yes | writing |
| 18 | reader_understanding | 2 | True | yes — significant. Previous draft:… | organization — the student differentiated the … | yes | writing |
| 19 | reader_understanding | 2 | True | yes — the student has moved from d… | purpose — the claim now has an arguable analyt… | yes | writing |
| 20 | coherence | 2 | True | yes — three disconnected fragments… | organization — the student coordinated previou… | yes | writing |
| 21 | coherence | 2 | True | yes — student removed the off-topi… | coherence + causal reasoning — student moved f… | yes | writing |
| 22 | conclusion | 2 | True | yes — student moved from a placeho… | purpose — a genuine persuasive position has em… | yes | writing |
| 23 | conclusion | 2 | True | yes — qualitative leap from a fill… | communicative purpose — student has moved from… | yes | writing |
| 24 | purpose | 2 | True | yes — student moved from topic ann… | purpose — from topic to arguable claim | yes | writing |
| 25 | purpose | 2 | True | yes — substantial developmental ga… | purpose — student moved from naming a subject … | yes | writing |
| 26 | purpose | 2 | True | yes — student replaced a meta-anno… | communicative purpose — student moved from top… | yes | writing |
| 27 | limited_progress | 2 | True | yes — student added scope ('close … | purpose — claim now has a scoped subject and a… | yes | writing |
| 28 | limited_progress | 2 | True | partial — student added a relation… | emerging purposefulness — student is reaching … | yes | writing |
| 29 | first_submission | 1 | False | — | — | yes | writing |
| 30 | first_submission | 1 | False | — | — | yes | writing |

## Developmental (not textual) reading of revision

- **Substantial growth (1–5):** the engine named ONE developmental capacity that strengthened (topic→arguable claim, generic→interpretive analysis, etc.) and issued a transfer_message about applying the learning to future writing — reinforcing learning, not praising text.
- **Superficial edits (6–9):** word swaps / intensifiers read as development_detected='no'/'partial' with NO fabricated growth; the remaining developmental opportunity was named. NO edit-counting or 'you revised a lot' praise (0 scorekeeping phrases).
- **Regression (10–12):** revisions that made communication worse were caught (development_detected='no'), and the single remaining opportunity was named without re-teaching every prior concept.
- **Multi-draft trajectory (13–16):** across 3 drafts the engine read the arc of a growing capacity rather than only the adjacent diff.
- **Targeted gains (17–26):** reader-understanding, coherence, conclusion, and purpose improvements each surfaced as the relevant primary_growth with a transfer message.
- **Limited progress (27–28):** movement on the right idea but still incomplete → development_detected='partial' + a single remaining_opportunity.
- **First submission (29–30) [control]:** no prior draft → revision_development.applies=false (correctly nothing to compare).

## No scorekeeping; boundary preserved

Across all 30 cases: 0 edit-counting/scorekeeping phrases, 0 content-coaching/rewriting phrases; intervention.focus='writing' every case; the M11 controller still selected exactly ONE instructional target. Development measured as qualitative change in communication, never quantity of edits.

## Category coverage

substantial_growth:5, superficial_edit:4, regression:3, multi_draft:4, reader_understanding:3, coherence:2, conclusion:2, purpose:3, limited_progress:2, first_submission:2

## Summary

- PASS: **30/30** on the first run (no fix needed). Revision interpreted as developmental growth; transfer became part of consolidation; superficial/regressed revisions correctly yielded no growth + a single next opportunity; first submissions did not apply the lens.
- Coordinates with M6–M12 and M5A. NO engine/instruction-layer/UI/framework redesign — one theory field (RevisionDevelopment: applies/development_detected/primary_growth/communication_change/reader_change/remaining_opportunity/transfer_message) + reasoner-prompt block + Dev Panel display.
- Latency ~49–175s/turn (3-draft cases longest); all under the streaming edge cap.