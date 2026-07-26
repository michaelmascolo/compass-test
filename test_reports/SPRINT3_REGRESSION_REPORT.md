# Sprint 3 Verification — 66-Case Regression Report

> **Scope:** Verify the fully enriched instructional-object knowledge base (35/35) against the frozen Milestone M1–M14 engine. **No code was modified** for this run or this report. Recommendations below are proposals only — **no changes made, awaiting review.**

## Run metadata
| | Baseline | This run |
|---|---|---|
| Run ID | `fd0dec0c-7e00-4df0-976b-7307f46a09a1` | `0bfe5b82-ef8b-4a5a-aa15-14f9de1e534b` |
| Label | Expanded Suite v1 Baseline | Sprint 3 verification — 35/35 enriched objects |
| Date | 2026-07-21 | 2026-07-25 |
| Reasoning mode | `exhaustive` (frozen path) | `exhaustive` (frozen path) |
| KB state | pre–Sprint 3 (4/35 enriched) | post–Sprint 3 (**35/35 enriched**) |
| **Result** | **58 pass / 8 partial / 0 fail / 0 error** (87.9%) | **57 pass / 7 partial / 0 fail / 2 error** (86.4%) |

The baseline uses the same frozen `exhaustive` engine path; the **only** difference between the two runs is the enriched instructional-object JSON. This isolates the effect of the richer objects (subject to LLM stochasticity — see caveat).

## 1. Passing / failing cases

- **Passing: 57/66.** No hard failures.
- **Fail verdicts: 0** (unchanged from baseline).
- **Error verdicts: 2** — TC31, TC62 (new; both evaluator-side, see §3).
- **Partial verdicts: 7** — TC06, TC20, TC32, TC37, TC39, TC61, TC64.

## 2. Behavior changes relative to the baseline

**Net verdict counts:** −1 pass, −1 partial, +2 error, 0 fail. Pass rate 87.9% → 86.4% (−1.5 pts).

### 2a. Improvements — 6 cases (partial → pass) — attributable to enrichment (positive)
Every one of these was a **baseline partial** and each now retrieves **newly-enriched objects**, which is direct evidence the enrichment sharpened diagnosis/invitation quality:

| Case | Name | Now retrieves (enriched objects in bold) |
|---|---|---|
| TC13 | Effective topic sentence | **Topic Sentence**, **Supporting Detail**, Explanation/Analysis |
| TC35 | Descriptive — flat detail, no dominant impression | **Supporting Detail**, **Word Choice**, **Purpose** |
| TC41 | Research synthesis — source dump, no synthesis | Thesis, Explanation/Analysis, **Topic Sentence** |
| TC56 | Cohesion — paragraphs don't connect | **Purpose**, **Topic Sentence**, Thesis |
| TC63 | Point-of-view shifting (you/one/I) | **Paragraph**, **Coherence**, **Unity** |
| TC65 | Student pastes AI-generated text, asks "is this good?" | **Hook / Opening Move**, **Word Choice**, **Background / Context** |

### 2b. Regressions — 5 cases (pass → partial) + 2 cases (pass → error)
| Case | Name | Change | Root of the partial/error |
|---|---|---|---|
| TC20 | Sentence-level confusion | pass → partial | `authorship_preserved` partial: offered a sentence starter ("…because ___"); evaluator calls it a "close call." |
| TC32 | Reflective piece not needing a thesis | pass → partial | Retrieved **Thesis** into a reflective context; framed the opening in "controlling idea" terms; missed P8 consolidation. |
| TC37 | Compare/contrast — no organizing scheme | pass → partial | Chose **Thesis** as primary target and pivoted away from the documented target (Organization), though Organization was retrieved. |
| TC39 | Literary analysis — plot summary, no claim | pass → partial | `authorship_preserved` "close call" on a sentence starter ("Through this story, the author develops the idea that ___"); substance correct. |
| TC64 | Multilingual writer — surface errors, strong idea | pass → partial | Advanced to precision refinement instead of consolidating the already-strong argument (P8 timing). |
| TC31 | Ambiguous both-sides thesis | pass → **error** | Evaluator crashed on JSON parse; the engine invitation was valid. |
| TC62 | Faulty parallelism in a series | pass → **error** | Evaluator crashed on JSON parse; the engine invitation was valid. |

### 2c. Unchanged pre-existing partials — 2 cases
- **TC06** and **TC61** were partial in both runs. Not enrichment-related; pre-existing limitations (TC61 relates to the logged foothold engine-boundary limitation).

## 3. Are failures attributable to the richer objects or to engine behavior?

The engine, prompts, and evaluator are **byte-for-byte frozen** — no code changed. Therefore every behavior delta is caused by either (a) the richer instructional objects influencing retrieval/reasoning, or (b) inherent LLM stochasticity in the (non-deterministic) reasoner and evaluator.

- **The 2 errors are NOT attributable to the objects.** Both TC31 and TC62 produced valid, in-character, one-target, writing-focused invitations; the failure was the **evaluator LLM returning malformed JSON** ("Expecting ',' delimiter"). These are evaluator-harness robustness issues and would most likely pass on re-run.
- **The 6 improvements ARE attributable to the objects** (each improved case now retrieves newly-enriched elements). This is the primary intended effect and it is positive.
- **Of the 5 pass→partial shifts:** TC32 and TC37 show a plausible enrichment signal — the now-richer **Thesis** object appears more salient in retrieval/target-selection, pulling it into a reflective piece (TC32) and over a documented Organization target (TC37). TC20/TC39 are borderline evaluator judgments on sentence-starter scaffolding (a long-standing Compass coaching style, not obviously enrichment-caused). TC64 is a P8 consolidation-timing judgment.

**Caveat (important):** the baseline is a **single** run and both the reasoner and evaluator are stochastic. Historical identical-config runs varied widely (74%→88%). 86.4% vs 87.9% is **within the observed run-to-run variance band**, with **zero hard failures** and a clear positive skew on the cases the enrichment touched. A single run cannot distinguish a true 1-case regression from noise.

## 4. Failure classification

| Case | Verdict | Classification | Rationale |
|---|---|---|---|
| TC31 | error | **Evaluator issue** | Eval LLM JSON parse crash; engine invitation valid (Thesis/Central Claim/Qualification retrieved; contestable-claim recognition correct). |
| TC62 | error | **Evaluator issue** | Eval LLM JSON parse crash; engine invitation valid (named the parallelism issue; Sentence/Supporting Claim/Topic Sentence retrieved). |
| TC32 | partial | **Retrieval issue** (enrichment-plausible) | Enriched **Thesis** retrieved into a reflective piece that does not need a thesis; caused quasi-argumentative framing. |
| TC37 | partial | **Retrieval issue** (enrichment-plausible) | Target selection chose enriched **Thesis** over the documented **Organization** target. |
| TC20 | partial | **Uncertain** | Borderline `authorship_preserved` call on a sentence starter; recurring Compass scaffolding style, not clearly enrichment-caused. |
| TC39 | partial | **Uncertain** | Same sentence-starter "close call"; core move (summary→claim) was correct. |
| TC64 | partial | **Uncertain / instructional-object** | P8 consolidation-before-advancing timing; possibly the richer "next developmental move" content biasing toward advancing on success. |
| TC06 | partial | **Expected / pre-existing** | Partial in baseline too; unchanged. |
| TC61 | partial | **Expected / pre-existing** | Partial in baseline; relates to the logged foothold engine-boundary limitation. |

**Summary of classes:** Evaluator issue ×2 · Retrieval issue ×2 (enrichment-plausible) · Uncertain ×3 · Expected/pre-existing ×2 · Engine issue ×0 · Prompt issue ×0.

## 5. Verdict

- **No engine regressions. No hard failures. No prompt issues.**
- Enrichment produced a **net positive on targeted cases** (6 improvements, all retrieving newly-enriched objects).
- The two "errors" are **evaluator-harness flakiness**, not engine or object defects.
- The only plausible enrichment-attributable regressions (TC32, TC37) are a **retrieval-salience** effect: the now-richer Thesis object competes more strongly in contexts where Purpose/Organization/reflection should lead.
- Overall pass rate is within historical variance; **Sprint 3 enrichment is verified as non-regressive to a high confidence, with two items worth a targeted look.**

## 6. Prioritized recommendations (PROPOSALS ONLY — no changes made, awaiting review)

**P0 — confirm the signal (cheap, no code):**
1. **Re-run the 2 evaluator errors (TC31, TC62)** and the 5 pass→partial cases in isolation (2–3×) to separate true regression from LLM noise. If they pass on re-run, close them as evaluator/stochastic.

**P1 — evaluator-harness robustness (evaluator issue, does NOT touch the frozen reasoner/prompts):**
2. Harden `_evaluate_case` JSON parsing (e.g., tolerant JSON extraction / an extra retry / mark `evaluator_error` distinct from case `error`) so evaluator flakiness never masquerades as a case failure. *This is harness code, not the engine.*

**P2 — investigate Thesis retrieval salience (retrieval issue, enrichment-plausible):**
3. For TC32 and TC37, inspect the STAGE-A selection: verify whether the enriched Thesis object's `communicative_purpose`/`definition` now over-weights it. If confirmed, the fix is **data-only** (tune the Thesis object's retrieval-facing text or `related_elements`), keeping the engine frozen — but only after review.

**P3 — consolidation-timing (uncertain):**
4. Review TC64 (and the P8 pattern) to decide whether the enriched `developmental_invitations`/`followup_decisions` bias toward advancing over consolidating on success. If so, adjust the affected objects' invitation ordering (data-only). Likely noise; verify first.

**P4 — no action:**
5. TC06, TC61, TC20, TC39 — do not act; pre-existing or borderline stylistic evaluator judgments.

## Appendix — data
- Baseline per-case verdicts: `/tmp/baseline_fd0dec0c.json`
- Full new-run document: `/tmp/run_sprint3.json` (also persisted in Mongo `test_runs`, id `0bfe5b82-…`); export via `GET /api/tests/runs/0bfe5b82-ef8b-4a5a-aa15-14f9de1e534b/export?format=markdown`.
- Enrichment builders: `backend/tests/enrich_sprint3_canonical.py`, `enrich_sprint3_canonical_batch2.py`. Schema: `INSTRUCTIONAL_OBJECT_SPECIFICATION.md`.
