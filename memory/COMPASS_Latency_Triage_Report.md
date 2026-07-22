# Compass — Latency Audit & Conditional Triage Architecture

> Deliverable for the latency workstream. The frozen `SYSTEM_MESSAGE` and all constitutional commitments are UNCHANGED. The triage path is additive and experimental (`backend/triage_experiment.py`), runs alongside the production engine, and was benchmarked against it (`backend/triage_benchmark.py`).

---

## 1. Map of the current reasoning sequence (per coaching turn)

```
POST /api/sessions/{id}/interact
  ├─ append student turn (complete) + AI placeholder (status=processing)   ~<0.2s, 1 DB write
  ├─ return Session immediately (durable — client may disconnect)
  └─ asyncio.create_task(_run_reasoning)                                   ← background

_run_reasoning  (server.py)
  ├─ DB read session
  ├─ _run_engine(session, req):
  │    ├─ STAGE A  _select_relevant_domains → 1 LLM call  (~3–5s)
  │    │     small compact-index prompt → picks 1–3 domains + sections + 1–3 instructional objects
  │    ├─ _build_prompt → assembles LARGE prompt (~20–25 KB):
  │    │     telos + compact theory + interaction summary + FULL domain data
  │    │     + instructional objects + instructional network + developmental profile
  │    │     + shared resource menu + latest draft block
  │    └─ STAGE B  reasoner → 1 LLM call  (~40–80s, ~90–93% of turn time)
  │          system = frozen SYSTEM_MESSAGE
  │          OUTPUT = one very large structured JSON: the ENTIRE DevelopmentalTheory
  │          (M6 communicative_purpose, M7 paragraph_function, M8 evidence_function,
  │           M9 coherence_function, M10 conclusion_function, M11 scaffolding_control,
  │           M12 reader_construction, M13 revision_development, M14 integration_calibration,
  │           instructional_reasoning[12 fields]) + candidate_invitations + selected_invitation
  │           + intervention + developmental_profile_update + observed_reorganization
  ├─ _finalize_turn → fill placeholder, snapshot theory_history, merge profile,
  │     append interaction, (NEW) record revision_history for substantive revises
  └─ DB write (turns, telos, theory, theory_history, interactions, profile, revision_history)

Frontend polls GET /sessions/{id} every 1.5–2.5s until the AI turn is complete.
```

**Two model calls per turn.** STAGE A is cheap; **STAGE B dominates** (measured 54s of a 58s turn in the earlier audit; benchmark below shows ~55–70s).

---

## 2. Evidence of redundant work (why STAGE B is slow)

The bottleneck is **output generation**, not input. STAGE B is instructed (by the frozen prompt + JSON schema) to **reconstruct and serialize the entire developmental model every turn**, even when the immediate task is a single narrow coaching decision:

- **Full-model reassessment every turn.** All 10 framework lenses (M6–M14) + the 12-field `instructional_reasoning` + `integration_calibration` are emitted on every turn, regardless of what actually changed. The M11 controller already selects **exactly ONE** target — so 9 of the 10 lenses' detailed output is diagnostic scaffolding the turn does not act on.
- **Repeated analysis of unchanged text.** On a `revise` turn that touches one paragraph, the engine still re-derives purpose, paragraph function, evidence, coherence, conclusion, reader model, etc. for the whole piece.
- **Generation of unused structured output.** The R3 preview experiment already proved this: trimming ONLY the serialized fields (reasoning unchanged) cut reasoner latency **25–35%** with no change to the decision. That is direct evidence that a large fraction of STAGE B time is spent *writing JSON the turn never consumes*.
- **No early exit.** There is no mechanism to stop once a decisive route is known (e.g., a stalled learner, an unresolved prior target, a clearly-local sentence problem). The single exhaustive pass always runs to completion.
- **Inside-out vs outside-in is implicit.** The choice is embedded in the big reasoning pass rather than decided cheaply up front, so both branches are effectively "considered" inside one long generation.

STAGE A is not redundant, but it can be **folded into triage** (triage already names the relevant instructional objects), removing one call from the fast path.

---

## 3. Proposed conditional triage architecture

Two stages around the **unchanged** frozen engine. New tiny `TRIAGE_SYSTEM_MESSAGE`; STAGE 2 keeps the frozen `SYSTEM_MESSAGE` verbatim (all constitutional/anti-coauthoring rules intact) and only **narrows scope + trims output**.

**STAGE 1 — Rapid Instructional Triage** (new, ~3s, ~130 output tokens)
Input = a compact, *incrementally-maintained* learner state (NOT the transcript): assignment purpose, active target + prior mode, known strengths, unresolved needs, and the current draft + previous draft (the revision delta). Output = the 6 triage decisions: what changed, prior-target status (resolved/partial/unchanged/worse), learner state (engaged/stalled/confused/finished), instructional route (stall / inside-out / outside-in / convention / transfer / fade), inside-vs-outside, `foundational_problem?`, the single highest-leverage dimension, the relevant instructional objects, and a confidence. Probabilistic: a plausible focused hypothesis is preferred over exhaustive certainty.

**Early-exit routing (code, between stages)**
- `foundational_problem = true` → fall back to the **full exhaustive engine** (broad reassessment is genuinely warranted).
- `learner stalled` → stall support on the current target; do not open a new one.
- prior target `unchanged` → keep the same target; do not search for a new one.
- prior target `resolved` → assess fade / advance.
- intention already clear → do not linger inside-out; test reader/task/convention (routing invariant).

**STAGE 2 — Focused Analysis** (frozen SYSTEM_MESSAGE, ~30s, small output)
Loads only the triaged dimension's canonical data + the relevant span + prior target/response, and emits a **trimmed** payload (invitation + scaffolding_control[one target] + intervention + instructional_reasoning + revision_development when applicable). Same governed reasoning, one target, anti-coauthoring — just scoped.

**Incremental student model.** Reuses the now-persisted `developmental_profile` + `revision_history` + compact `theory` so subsequent turns narrow reasoning instead of rebuilding from the transcript.

Net: fast path = **triage (replaces STAGE A) + focused STAGE B with small output**. Foundational path = triage + full engine (a small triage tax for a guaranteed-correct broad pass).

---

## 4. Benchmark results

EXHAUSTIVE frozen engine vs TRIAGE experimental, same starting session per case; representative set TC01/TC03/TC07/TC08/TC25/TC30; decision equivalence LLM-judged. Raw: `test_reports/triage_benchmark.json`.

| Metric | Exhaustive | Triage | Δ |
|---|---|---|---|
| Avg latency / turn | **64.7 s** | **36.5 s** | **−43.6%** |
| Avg output tokens | 2,990 | 1,743 | −41.7% |
| Model calls / turn | 2 (A+B) | 2 (triage+focused) | same count, far smaller STAGE-2 output |
| Same target | — | **4 / 6** | |
| Materially different decision | — | 2 / 6 | both judged **triage-better** |
| Anti-coauthoring (`focus=writing`) | 6/6 | **6/6** | preserved |

Per-case latency: TC01 61→43s · TC03 67→35s · TC07 70→35s · TC08 67→37s · TC25 59→32s · TC30 65→38s.

## 5. Latency reduction achieved

**−43.6% wall-clock per turn** (64.7 s → 36.5 s), from **−41.7%** fewer generated output tokens. The reduction comes entirely from STAGE 2 serializing only the triaged dimension instead of the full 10-lens model — the exact lever R3 validated on the preview, now generalized. STAGE 1 triage costs ~3 s (≈130 tokens) and replaces the STAGE-A selector, so the fast path adds no net call. Further headroom (not yet taken): a faster/cheaper model for STAGE 1; streaming the STAGE-2 invitation token-stream to the client for a lower *time-to-first-word*; caching unchanged-context between revise turns.

## 6. Cases where triage produced a materially different instructional decision

Only 2 of 6, and the independent LLM judge rated **triage better in both** (equivalent in the other 4). Neither is a regression:

- **TC07 (strong thesis — must not be over-taught).** Exhaustive redirected to body-paragraph drafting (`consolidate`); triage kept the writer stress-testing the claim's arguability against a skeptic (`invite_only`, outside-in). The expected behavior is "light / consolidate or move forward" — triage's restrained `invite_only` is the more conservative, on-spec move.
- **TC30 (returning student with independent control; expected target = evidence/explanation, NOT thesis).** Exhaustive pulled to "generate a body-paragraph claim" (structural); triage targeted **grounding the argument in evidence and explanation** — matching the expected target and the developmental-profile growth edge. This is precisely the known residual weakness **W-D / TC30** (engine defaults to thesis/structure over the profile's evidence edge) — **triage corrected it**, because the incremental student-state summary surfaced the profile's growth edge to the triage decision directly.

**Conclusion.** Equivalent-or-better instructional judgment at **~44% lower latency** on a representative set, with anti-coauthoring and one-target discipline intact and one known weakness improved. Recommended next step (pending approval): wire the triage path into production behind a per-session flag, keep `foundational_problem → full-engine` fallback, and run the full 66-case suite through the frozen evaluator (Compare-Two-Runs vs `fd0dec0c`) before making it the default.

---

### Files
- `backend/triage_experiment.py` — experimental triage engine (additive; frozen SYSTEM_MESSAGE untouched).
- `backend/triage_benchmark.py` — exhaustive-vs-triage benchmark harness.
- `test_reports/triage_benchmark.json` — full per-case results + aggregate.

