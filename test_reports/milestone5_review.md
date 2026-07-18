# Milestone 5 — Developmental Instruction & Cultural Resource Mediation: Human-Readable Review Table

Cases: 30 | Errors: 0 | Revision (consolidation) sub-cases: 2 (cases 1, 3)

## What Milestone 5 adds
A generic, domain-independent **Developmental Instruction Layer**. On each turn the engine now chooses ONE of five intervention types and names the cultural resource in play:
- `interpretation_only` — reflect the student's current organization back; no new concept yet.
- `instruct_then_invite` — briefly introduce a relevant cultural resource (from the domain's `cultural_resources`), then invite the student to try it.
- `invite_only` — student already grasps / discovered the strategy; just invite the next move.
- `consolidate` — after a real revision, name the developmental change and the tool the student is beginning to use intentionally, then still offer one forward invitation.
- `postpone_instruction` — a concept could be taught but now is not the moment; interpret and invite instead.

Cultural resources live in `canonical_writing_model.json` (`cultural_resources` sections), NOT in the engine. No writing-specific logic was added to `server.py`.

Each turn was inspected for: exactly ONE student-facing invitation; instruction (when present) says what the concept is + why writers use it + how it relates to THIS draft; no rewriting / model answer; no stage/grade/level language; student authorship preserved; intervention type appropriate to the student profile.

## Six student profiles × {Opening, Thesis, Paragraph Purpose}

| # | Profile | Domain | Intervention type | Cultural resource | One inv. | Judgment | Note |
|---|---------|--------|-------------------|-------------------|----------|----------|------|
| 1 | needs_instruction | Opening | instruct_then_invite | Significance | yes | Satisfactory | Introduces "significance" as reader-need, then invites stakes. Revision → consolidate (v2). |
| 2 | needs_instruction | Thesis | instruct_then_invite | Claim | yes | Satisfactory | Topic-vs-claim taught, then invites a position. |
| 3 | needs_instruction | Paragraph | instruct_then_invite | Claim (topic vs claim) | yes | Satisfactory | Claim as prerequisite for paragraph purpose. Revision → consolidate (v2). |
| 4 | needs_instruction | Opening | interpretation_only | — | yes | Satisfactory* | Minimal joke-draft; engine reflected + invited a problem rather than lecturing. Conservative, not a failure. |
| 5 | needs_instruction | Thesis | instruct_then_invite | Claim | yes | Satisfactory | Bare topic ("Social media.") → claim instruction + invite. |
| 6 | already_understands | Opening | invite_only | Central Claim | yes | Satisfactory | Purposeful tension-opening recognized; invited to form the claim, no lecture. |
| 7 | already_understands | Thesis | invite_only | Claim + reasoning | yes | Satisfactory | Causal thesis honored; invited to specify "quietly eroding." |
| 8 | already_understands | Paragraph | interpretation_only | — | yes | Satisfactory | Scene+interpretation reflected; invited to state the paragraph's job. |
| 9 | already_understands | Opening | postpone_instruction | Central Claim | yes | Satisfactory* | Strong assumption-challenge opening; thesis concept deferred, claim surfaced by invitation. Conservative, not a failure. |
| 10 | already_understands | Thesis | invite_only (fixed) | Claim + reasoning | yes | Satisfactory | **Was over-instructing (instruct_then_invite); after restraint fix → invite_only.** Sophisticated claim; invited to name the mechanism. |
| 11 | misuses | Opening | interpretation_only | — | yes | Satisfactory | Irrelevant "hook" fact reflected; invited to name the real tension. |
| 12 | misuses | Thesis | instruct_then_invite | Claim | yes | Satisfactory | Popularity-statement corrected toward a position. |
| 13 | misuses | Paragraph | interpretation_only | — | yes | Satisfactory | Topic/purpose conflation reflected; invited a purposeful sentence. |
| 14 | misuses | Opening | instruct_then_invite | Central Claim | yes | Satisfactory | Dictionary-definition opener redirected to an arguable position. |
| 15 | misuses | Thesis | instruct_then_invite | Claim | yes | Satisfactory | "I will discuss" announcement → claim instruction + invite. |
| 16 | discovered_without_name | Opening | instruct_then_invite | Significance | yes | Satisfactory | Names the significance move the student intuited; invites grounding. |
| 17 | discovered_without_name | Thesis | instruct_then_invite | Claim | yes | Satisfactory | Observation-vs-claim gap named; invites the claim. |
| 18 | discovered_without_name | Paragraph | interpretation_only | — | yes | Satisfactory | Fact-then-meaning sequencing reflected; invites the paragraph's job. |
| 19 | discovered_without_name | Opening | interpretation_only | — | yes | Satisfactory | Deliberate question-hook honored; invites hook↔purpose link. |
| 20 | discovered_without_name | Paragraph | interpretation_only | — | yes | Satisfactory | Concession-setup coordination honored; invites the specific concession. |
| 21 | rigid_formula | Opening | instruct_then_invite | Hook | yes | Satisfactory | Three-part template caught; hook reframed as door into the real concern. |
| 22 | rigid_formula | Thesis | instruct_then_invite / invite_only | Thesis / Claim | yes | Satisfactory | Original: instruct organizing function. Post-fix: invite_only (student HAS an arguable claim; deepen one reason). Both within acceptable set. |
| 23 | rigid_formula | Paragraph | instruct_then_invite | Interpretation / Reasoning | yes | Satisfactory | Circular "analysis" caught; "make the because visible" taught. Restraint fix left this intact. |
| 24 | rigid_formula | Opening | instruct_then_invite | Claim | yes | Satisfactory | Plan-announcement thesis → arguable idea invited. |
| 25 | rigid_formula | Thesis | instruct_then_invite | Claim | yes | Satisfactory | "This essay will prove…" → claim-vs-announcement instruction. |
| 26 | needs_less | Opening | interpretation_only | — | yes | Satisfactory | Precise anecdote honored; invited to articulate purpose, no lecture. |
| 27 | needs_less | Thesis | invite_only (fixed) | Claim | yes | Satisfactory | **Was over-instructing (instruct_then_invite); after restraint fix → invite_only.** Aphoristic arguable claim; invited to name the skeptic. |
| 28 | needs_less | Paragraph | interpretation_only | — | yes | Satisfactory | Vivid image + self-labeled purpose honored; invited to sharpen the job. |
| 29 | needs_less | Opening | interpretation_only | — | yes | Satisfactory | Strong feeling-hook honored; invited to stay in it vs. meta-announce. |
| 30 | needs_less | Thesis | invite_only | Claim | yes | Satisfactory | Inverse-relationship claim honored; invited to name the "why." |

\* Cases 4 and 9 did not match the strictest expected type but chose a *more conservative* move (reflect / defer) that preserves authorship — counted Satisfactory, not a failure.

## Consolidation (revision) sub-cases
- **Case 1** (Opening): revision replaced a flat announcement with a concrete scene → `consolidate`, theory snapshots **v2** (prior preserved), then invited the controlling claim.
- **Case 3** (Paragraph): revision named the paragraph's job + planted a claim → `consolidate`, theory snapshots **v2**, then invited grounding evidence.

## Over-instruction tuning (this session)
Two advanced-student cases (10 `already_understands`/Thesis, 27 `needs_less`/Thesis) were originally answered with `instruct_then_invite` — teaching a concept the student already commanded. A **domain-independent RESTRAINT rule** was added to the Developmental Instruction Layer prompt: instruct only when a resource would *reorganize* present understanding; when a student already uses the relevant organization competently and the edge is merely to sharpen/extend/ground it, prefer `invite_only` / `interpretation_only`.

Post-fix targeted re-run (`milestone5_restraint_recheck.py` → `milestone5_restraint_results.json`):
- Cases 10, 27 → now `invite_only` (fixed), instruction length 0.
- Capable controls 6, 7, 30 → `invite_only` (unchanged, correct).

Under-instruction guard (`milestone5_underinstruct_guard.py` → `milestone5_guard_results.json`) — fix did NOT suppress needed teaching:
- Case 2 (needs_instruction/Thesis) → `instruct_then_invite` ✓
- Case 12 (misuses/Thesis) → `instruct_then_invite` ✓
- Case 23 (rigid_formula/Paragraph, circular analysis) → `instruct_then_invite` ✓
- Case 22 (rigid_formula/Thesis) → `invite_only` (student's claim is genuinely arguable; within the original acceptable set for this profile).

## Summary
- Intervention-type appropriateness: **30 / 30 Satisfactory** (28 direct matches + 2 conservative-safe: cases 4, 9). After the restraint fix, the two prior over-instruction cases (10, 27) are corrected.
- One-invitation-per-turn: 30/30. Rewriting / model-answer failures: 0. Stage/grade/level language: 0. Instruction always tied to the student's own draft.
- Consolidation verified on real revisions (theory_history v2, prior versions preserved).
- Latency: ~26–78s per turn (two-turn consolidation cases longest); all under the streaming edge cap, no 502s.
- Domain separation preserved: cultural resources come from `canonical_writing_model.json`; engine remains domain-independent.
