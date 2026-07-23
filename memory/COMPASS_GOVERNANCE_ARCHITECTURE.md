# COMPASS GOVERNANCE ARCHITECTURE

> Enduring architecture, not a latency fix. This document defines Compass as a **hierarchy of reasoning governance** — five layers, ordered by authority. Higher layers constrain lower ones; lower layers may never override higher ones. The Stage-2 decomposition (and every future change) must conform to this hierarchy. Implementation of the decomposition should begin only after this architecture is reviewed and approved.

## Orientation: governance, not a pipeline
Compass is not a sequence of steps; it is a **chain of authority**. Each coaching turn is an act of governed reasoning in which:
- **Constitutional commitments** decide what Compass may and may not do — ever.
- **Pedagogical policy** decides how good teaching is chosen among lawful options.
- **Diagnostic reasoning** decides what is actually going on in *this* piece of writing.
- **The learner model** supplies who this writer is and where they are developing.
- **The presentation contract** decides how the resulting coaching is expressed.

Authority flows downward (1 → 5). Information flows upward (the learner model and diagnosis inform policy application, but never suspend the constitution). A violation at a higher layer invalidates the turn regardless of how good the lower layers were.

---

## Layer 1 — Constitutional Commitments (identity-level invariants)
- **Purpose.** Define Compass's identity and inviolable boundaries. These are *what Compass is*, not *how it teaches*. They protect the learner's ownership of their own writing and thinking.
- **Always active or conditional.** **Always active**, on every turn, on every path (triage focused, foundational fallback, exhaustive), with no exceptions and no confidence threshold.
- **Persistent or reconstructed.** **Persistent and fixed** — not recomputed per turn. They are the frame within which every turn runs.
- **Expected rate of change.** **Almost never.** Changing the constitution changes Compass's identity; it requires deliberate governance review and full re-validation. Treat as amendments, not edits.
- **Examples.** Anti-coauthoring (never write, rewrite, or supply copyable content); learner ownership / functional asymmetry (the author does the writing); restraint on competent performance (do not over-teach a working move); exactly one coaching invitation per turn; no hidden traits, no fixed stages, no scores/grades; the answer-the-assignment safeguard; stopping rules (honor an independence request; stop on diminishing returns); "culture leads instruction, student thinking leads the turn." (In the current prompt: M5A boundary, W-A/W-B/W-C, the no-labels/no-scores stance, stopping rules.)
- **Dependencies.** **None upward** — this layer depends on nothing and constrains everything below. Every other layer is subordinate to it.

## Layer 2 — Pedagogical Policy (instructional principles governing teaching decisions)
- **Purpose.** Within constitutional bounds, decide *what good teaching does here*: how to sequence development, when to move, how much support to give, which developmental edge is highest-leverage. This is Compass's philosophy of teaching, expressed as decision policy rather than fixed rules.
- **Always active or conditional.** **Always active** as governing policy, but it *governs a choice* rather than performing analysis. It is the policy that the triage decision and the diagnostic layer must obey.
- **Persistent or reconstructed.** **Persistent** (the principles) but **applied fresh** each turn to the current situation. The principles do not change; their application does.
- **Expected rate of change.** **Slow and deliberate.** Policy evolves as pedagogy is refined (e.g., tuning the inside-out→outside-in transition, restraint calibration, support-fading criteria). Each change is reviewed and validated, but it is not identity-level.
- **Examples.** Inside-out vs outside-in routing (work meaning/intention first; move promptly to reader/task/convention once intention is clear); developmental sequencing (consolidate a gain before advancing); support calibration and fading (give the least support that still enables the next move); "teach, don't only ask"; one-highest-leverage-target discipline; honor the teacher's stated purpose and developmental priority (W-D). This is also exactly what the **rapid triage stage** encodes: it is Layer 2 made explicit and fast.
- **Dependencies.** Depends on **Layer 1** (all policy choices must be constitutional) and reads from **Layer 4** (the learner model tells policy where the writer is). Governs **Layer 3** (selects which diagnosis runs) and shapes **Layer 5** (support level → how the invitation is framed).

## Layer 3 — Diagnostic Reasoning (conditional instructional analysis)
- **Purpose.** Determine what is actually happening in the current writing along the dimension policy has prioritized: is the claim arguable, is the evidence interpreted, do the ideas cohere, is the reader oriented, is a convention functionally needed, has learning transferred?
- **Always active or conditional.** **Conditional** — this is the layer that *should* run selectively. Only the diagnostic lenses relevant to the triage route/dimension execute; the rest stay dormant. (This is the core of the Stage-2 decomposition: today the frozen prompt runs "diagnose across ALL frameworks" every turn; the enduring architecture says diagnosis is conditional, governed by Layer 2.)
- **Persistent or reconstructed.** **Reconstructed each turn** from the current draft + revision delta. Diagnosis is about *this* text now; it is not carried over (its *conclusions* are folded into Layer 4, but the analysis itself is fresh).
- **Expected rate of change.** **Moderate.** The catalogue of diagnostic lenses (paragraph function, evidence function, coherence, reader construction, conventions, sentence construction, stall diagnosis, transfer assessment) grows and improves over time as the canonical knowledge base expands. Higher churn than Layers 1–2, lower than Layer 4's per-turn updates.
- **Examples.** M7 paragraph function, M8 evidence function, M9 transitions/coherence, M10 conclusion, M12 reader construction, the IO 12-step element analysis, stall diagnosis, support-fading/transfer assessment. Each is a *tool* invoked when the route calls for it.
- **Dependencies.** Governed by **Layer 2** (which lenses to run) and bounded by **Layer 1** (diagnosis may never justify writing *for* the student). Consumes **Layer 4** (prior targets, known strengths) and **produces** updates *to* Layer 4.

## Layer 4 — Learner Model (persistent developmental state)
- **Purpose.** Maintain who this writer is and how their control of writing is developing — across turns and across the whole revision arc — so Compass reasons from accumulated understanding rather than re-reading the transcript each time.
- **Always active or conditional.** **Always available** as read context; **updated conditionally** (after substantive turns/revisions). It is consulted every turn and revised when there is new developmental evidence.
- **Persistent or reconstructed.** **Persistent** — this is the one layer that is explicitly stored and evolves incrementally. It is *never* reconstructed from scratch.
- **Expected rate of change.** **Continuous** — it changes every substantive turn. It is the most dynamic layer by design (that dynamism is its purpose).
- **Examples.** The developmental profile (per-element control statements + trend: emerging/developing/consolidating/independent); the revision-history record (before/after drafts, active target, resolution status, whether the next instructional decision changed); the current inside-out/outside-in route; active + resolved coaching targets; current support level; evidence of transfer or failed transfer. (In the system: `developmental_profile`, `revision_history`, the working `theory`.)
- **Dependencies.** Written by **Layer 3** (diagnosis produces the updates) under **Layer 2** policy; read by **Layers 2 and 3** to narrow reasoning. Must respect **Layer 1** (no hidden traits, no deficit labels, no scores — the model records developmental *control*, never a ranking).

## Layer 5 — Presentation Contract (how coaching is expressed to the learner)
- **Purpose.** Govern the surface form of coaching: one invitation, in the coach's voice, developmental not evaluative, anchored to the learner's document, never grading, never supplying content. Turns a governed decision into words the learner receives.
- **Always active or conditional.** **Always active** — every turn produces exactly one learner-facing expression under this contract, whatever path produced the decision.
- **Persistent or reconstructed.** The **contract is persistent**; the **expression is reconstructed** each turn (the specific invitation is new every time).
- **Expected rate of change.** **Low for the contract** (voice, one-invitation rule, no-scores), **higher for the delivery mechanism** (e.g., streaming/anchored-marker UX) — the *how it is delivered* may evolve as long as the contract's guarantees hold. Streaming is a Layer-5 delivery change that provably did not touch Layers 1–4.
- **Examples.** The single `student_facing_invitation`; "read as a reader, don't rewrite" voice; the anchored coaching marker + inline card; progressive streaming of the invitation; no numeric feedback. Note: parts of this overlap Layer 1 (the *one-invitation* and *no-content* rules are constitutional guarantees enforced at the presentation surface).
- **Dependencies.** Depends on **Layer 1** (its guarantees are constitutional) and receives the decision from **Layers 2–3** plus context from **Layer 4**. It is the terminal layer: it expresses, it does not decide.

---

## How the layers interact during one coaching turn
1. **Intake (Layer 5 in / Layer 4 read).** The learner submits or revises the document. The revision delta and the persistent learner model (Layer 4) are loaded — not the whole transcript.
2. **Policy decision (Layer 2, reading Layer 4, bounded by Layer 1).** Rapid triage applies pedagogical policy to the delta + learner model: what changed, prior-target status, learner state, inside/outside, the single highest-leverage dimension, and whether the situation is *foundational* (requiring broad reassessment). This is Layer 2 selecting how Layer 3 will run — under the constitution.
3. **Conditional diagnosis (Layer 3, governed by Layer 2, bounded by Layer 1).** Only the lenses the route selected execute against the current text. If Layer 2 flagged a foundational problem, the full diagnostic breadth runs (fallback); otherwise a focused subset does. Diagnosis may never conclude "write it for them" — Layer 1 forbids it.
4. **Constitutional check (Layer 1, continuous).** Restraint, anti-coauthoring, one-target, answer-the-assignment, and stopping rules are enforced throughout and as a final gate: if the chosen move would over-teach a competent writer, supply content, or ignore an independence request, it is vetoed regardless of the diagnosis.
5. **Learner-model update (Layer 4, written by Layer 3 under Layer 2).** The turn's findings — target resolved/partial, growth detected, next-decision change — are folded into the persistent developmental profile and revision history. This is the only durable side effect of reasoning.
6. **Expression (Layer 5, bounded by Layer 1).** The decision becomes exactly one invitation in the coach's voice, anchored to the document and streamed to the learner; background bookkeeping (Layer 4 persistence, analytics) completes after the invitation has begun rendering, and may never alter it.

**Invariant across the turn:** authority is top-down. Triage (Layer 2) may narrow diagnosis (Layer 3) and even skip most of it, but it can never relax a constitutional commitment (Layer 1) or fabricate learner state (Layer 4). Latency optimization lives entirely in *how much of Layer 3 runs* and *how Layer 5 delivers* — never in weakening Layers 1, 2, or 4.

---

## Implications for the Stage-2 decomposition (why this comes first)
The decomposition is simply this architecture made executable:
- **Constitutional Core** = Layer 1 (+ the constitutional guarantees of Layer 5) — always run, immutable.
- **Conditional Diagnostic Modules** = Layer 3 — run only when Layer 2 (triage) selects them.
- **Policy** = Layer 2 — expressed as the triage decision + the always-on principles the core enforces.
- **Learner-model update** = Layer 4 — incremental, persistent.
- **Delivery** = Layer 5 — the invitation + streaming.

The earlier classification in `COMPASS_Stage2_Decomposition_Design.md` (A/B/C/D) maps directly: **A → Layers 1 & 2**, **B → Layer 3**, **C → Layer 4**, **D → Layer 5**. The decomposition is acceptable only if it preserves this hierarchy: the constitution and policy stay always-on and unweakened, diagnosis becomes conditional, the learner model stays persistent, and presentation guarantees hold. Any refactor that reduces Layer-1 or Layer-2 guarantees to gain speed is out of bounds, by definition of this architecture.

**Gate:** review and approve this governance architecture, then implement the Stage-2 decomposition against it. Validation remains the full 66-case Compare-Two-Runs vs `fd0dec0c`, judged on constitutional behavior — i.e., on whether Layers 1–2 held — not textual similarity.
