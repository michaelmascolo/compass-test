# Public Preview — Latency Audit (measured)

> No change was made to the frozen instructional architecture, evaluator, developmental logic, or decision rules to produce this audit. Timing instrumentation was added around the existing stages only. Two representative preview turns were measured end-to-end through the real pipeline.

## Measured breakdown — one representative preview turn
Seed: **"Phones should be banned in classrooms."** (a second turn, "School lunches.", is shown for confirmation.)

| Stage | Operation | Turn 1 ("Phones…") | Turn 2 ("School lunches.") | Share |
|---|---|---|---|---|
| Frontend request initiation | `POST /interact` round-trip (persist student turn + placeholder, return) | ~instant (student turn visible immediately) | — | ~0% |
| Backend session retrieval | `db.sessions.find_one` (×2 in `_run_reasoning`) | **0.001 s** | ~0.001 s | ~0% |
| Prompt / context construction | `_build_prompt` (assembling ~22 KB reasoner prompt) | **0.001 s** | ~0.001 s | ~0% |
| **STAGE A — selector model call** | LLM (Claude Sonnet 4.6) picks relevant domains + instructional objects | **3.74 s** | 3.93 s | ~6–7% |
| **STAGE B — reasoner model call** | LLM (Claude Sonnet 4.6) generates the full structured JSON (theory + frameworks + candidates + intervention + invitation) | **54.29 s** | 56.57 s | **~93–94%** |
| Evaluator / secondary model call | **NONE in the interact path** (evaluator runs only in the `?tests` harness) | — | — | 0% |
| Persistence / database write | `db.sessions.update_one` | **0.002 s** | ~0.002 s | ~0% |
| Retries / repeated analysis | none fired this turn (each stage retries once only on failure) | 0 | 0 | 0% |
| **Total time to FIRST visible response** | learner's own turn renders on submit | **< 1 s** | < 1 s | — |
| **Total time to COMPLETED response** | background reasoning end-to-end | **58.04 s** | ~60.5 s | 100% |
| Poll detection lag (frontend) | 2.5 s polling interval → coach reply appears up to 2.5 s after completion | +0–2.5 s | +0–2.5 s | — |

**Net: the learner waits ~58–61 s for the coach's reply.** (The earlier "~90 s" figure included polling variance and a slower run; the reasoner call alone accounts for essentially all of it.)

## Classification of operations
1. **Required for the instructional decision:** STAGE B reasoner call — it produces the `student_facing_invitation`. This is the decision.
2. **Inherited from the full app but unnecessary for the preview:**
   - **STAGE A selector call** — for the preview the relevant domains/objects are effectively constant (measured selections were always `Opening/Introduction`, `Central Claim/Thesis`, `Audience Awareness` + `Hook/Introduction/Purpose` objects). The preview never needs to *discover* the domain.
   - **Most of STAGE B's OUTPUT** — the reasoner is asked to emit the entire working theory, a theory-history snapshot, developmental-profile memory updates, multiple candidate invitations, and every framework block. The preview is a single short session with **no Dev Panel, no cross-session developmental memory, and no teacher audit trail**, so the large majority of that generated JSON is never consumed. Generating it is what costs ~55 s.
3. **Duplicated:** two `find_one` reads of the same session inside `_run_reasoning` (pre- and post-reasoning reload). Cost ~1 ms total — not worth changing.
4. **Sequential but potentially parallel:** STAGE A → STAGE B are genuinely dependent (B consumes A's selections), so they cannot be parallelized. STAGE A can instead be *eliminated* for the preview (see R1).
5. **Deferrable until after the visible response:** the profile merge, theory-history snapshot, and interaction append are all cheap local operations on the *single* LLM output — they are not separate calls, so deferring them saves ~0 ms. There is no post-turn model call to defer (the evaluator is not in this path).
6. **Responsible for most of the latency:** STAGE B output generation — **~93%** of total.

## Recommendations — smallest preview-specific wrapper changes

### Safe now (no approval needed; instructional decision unchanged or unaffected)
- **R1 — Skip STAGE A for the preview (pre-supply the fixed domain/object set).** Saves ~3.7–4 s (~7%). The preview always selects the intro/thesis/audience domains anyway (verified in logs), so this removes a redundant model call. *Caveat:* it fixes the reasoner's input context rather than re-selecting it each turn; strictly this is a context change, so it is offered as opt-in and should be spot-checked against a few live turns. Low risk, modest gain.
- **R2 — Tighten perceived wait (pure UX).** Reduce the frontend poll interval 2.5 s → 1.5 s and give the preview a richer in-character "reading" state. Shaves up to ~1 s of detection lag and makes the wait feel intentional. Zero decision change. *This does not reduce the real 55 s.*

**Combined ceiling of the safe changes: ~5 s saved (58 s → ~53 s). Not sufficient on its own for a 3–5 minute preview.**

### High-value but GATED (require explicit approval; may change the instructional output — must re-validate)
- **R3 — Preview-only slimmed reasoner OUTPUT schema (the real fix).** Ask the model, *for preview sessions only*, to emit just the fields the preview consumes — primarily the `student_facing_invitation` plus the minimal reasoning needed to keep its quality — and drop the theory-history snapshot, candidate-invitation list, and full framework JSON that only the Dev Panel and cross-session memory use. **Estimated 40–60% reduction of STAGE B (≈55 s → ≈20–30 s).** *Requires approval because the extended JSON partly functions as the model's chain-of-thought; trimming it can alter the invitation.* If approved, we re-run the decision-table scenarios (A/B/C, anti-coauthoring, stall, transfer beat) and confirm the invitations are equivalent before shipping. **This is the only lever that makes a 3–5 minute preview realistic.**
- **R4 — Stream the invitation.** Would cut *time-to-first-token* dramatically, but only helps if the invitation is emitted early in the output; today it appears near the end (after the full theory). This needs an output-ordering change (schema change, gated) plus streaming support inside the durable-polling architecture. Higher effort — defer unless R3 is insufficient.

## Bottom line
The dominant cost (~93%) is the reasoner **generating a large structured JSON, most of which the preview never uses**. The safe wrapper changes (R1 + R2) trim only ~5 s. A meaningful reduction requires approving **R3** (preview-only slimmed output) — which may change the instructional output and therefore needs explicit sign-off and re-validation. No instructional reasoning was simplified in this audit.
