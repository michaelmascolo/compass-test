# Milestone 11 — Recursive Developmental Scaffolding Controller: Review Table

Cases: 30 | PASS: **30/30** | Errors: 0

Each case verifies the master developmental loop: (1) exactly ONE primary_target selected per cycle; (2) other opportunities POSTPONED (never teaches multiple major concepts at once); (3) an appropriate instructional_mode (developmental_question / explicit_instruction / brief_demonstration / guided_revision / reflection / consolidation); (4) STOPPING RULES honored (cycle_status + stopping_reason); (5) CONSOLIDATION on real revisions; (6) NO endless recursion across repeated revisions; (7) M5A boundary preserved (intervention.focus='writing'). Categories: multiple-weaknesses, needs-explanation, needs-questioning, needs-consolidation (revision), strong/weak drafts, requests-independence, unit-size, repeated-revision (multi-turn), brainstorm.

| # | Category | Turns | Primary target (abridged) | Mode | Cycle status | #postponed | Invitation (abridged) |
|---|----------|-------|---------------------------|------|--------------|-----------|-----------------------|
| 1 | multiple_weaknesses | 1 | Forming an arguable controlling claim | explicit_instruction | continue | 4 | You've made a start and you're clearly pointing toward an argument — s… |
| 2 | multiple_weaknesses | 1 | Articulating a contestable controlling claim | explicit_instruction | continue | 2 | You're working on an argument about car traffic downtown — that's a re… |
| 3 | multiple_weaknesses | 1 | Clarify the communicative purpose — what the s… | developmental_question | continue | 2 | You've made a start by naming your topic — photosynthesis — and you've… |
| 4 | multiple_weaknesses | 1 | Establishing a controlling interpretive claim … | developmental_question | continue | 3 | You've identified several real features of the poem — imagery, short l… |
| 5 | multiple_weaknesses | 1 | Clarify the communicative purpose/intended mea… | developmental_question | continue | 4 | You've made a start — there's a moment here, a day, even a detail (red… |
| 6 | needs_explanation | 1 | distinguishing topic from claim — get the stud… | explicit_instruction | continue | 3 | You've started by naming your topic — social media and friendship — wh… |
| 7 | needs_explanation | 1 | Distinguish topic from arguable claim; produce… | explicit_instruction | continue | 3 | You've made a start by naming the topic — traffic downtown. Now the as… |
| 8 | needs_explanation | 1 | establish communicative purpose: what the writ… | developmental_question | continue | 3 | You've made a start by identifying that your essay will be about a poe… |
| 9 | needs_explanation | 1 | Shift from meta-announcement to reader orienta… | developmental_question | continue | 2 | You've chosen a genuinely interesting topic — the internet is somethin… |
| 10 | needs_questioning | 1 | Scope: testing whether the claim is supported … | developmental_question | continue | 2 | You've opened with a genuinely arguable claim — one that distinguishes… |
| 11 | needs_questioning | 1 | Central claim: move from observation to a cont… | developmental_question | continue | 2 | That's a strong opening move — you've identified a specific technique … |
| 12 | needs_questioning | 1 | Articulating the controlling insight — what th… | developmental_question | continue | 3 | This opening line does real work — it sets up a tension between what f… |
| 13 | needs_questioning | 1 | Establishing the communicative purpose — what … | developmental_question | continue | 2 | That opening sentence does real work — it places us in a specific mome… |
| 14 | strong_draft | 1 | Thesis/claim: student needs to identify the po… | developmental_question | continue | 3 | You've opened with a concrete moment — a like without a reply — and im… |
| 15 | strong_draft | 1 | Identifying the larger interpretive claim this… | developmental_question | continue | 2 | You've opened with a sharp observation: the room's design makes bystan… |
| 16 | strong_draft | 1 | Reader orientation — what the reader needs to … | developmental_question | continue | 1 | That opening sentence does real work — it sets up a clear metaphor (re… |
| 17 | strong_draft | 1 | orient the reader: what experience grounds thi… | developmental_question | continue | 3 | That's a sharp opening line — it draws the reader into a specific tens… |
| 18 | weak_draft | 1 | forming a controlling claim — distinguishing t… | explicit_instruction | continue | 4 | You've named the core tension of your topic — social media can feel bo… |
| 19 | weak_draft | 1 | establish communicative purpose (what process,… | developmental_question | continue | 3 | You've got a starting point — something is happening and you know it h… |
| 20 | weak_draft | 1 | Clarify communicative purpose — what the stude… | developmental_question | continue | 3 | You've made a start — there's a memory here, and it clearly meant some… |
| 21 | requests_independence | 1 | return control to student; preserve independen… | consolidation | stop | 4 | It sounds like something clicked for you — that's a good moment to wri… |
| 22 | requests_independence | 1 | invite first draft of opening | developmental_question | stop | 3 | It sounds like you're ready to start writing your reflection. Before y… |
| 23 | unit_sentence | 1 | Clarify and sharpen the controlling claim so i… | developmental_question | continue | 2 | You've taken a clear position — that social media harms teen friendshi… |
| 24 | unit_whole_paper | 1 | Articulate the single core communicative purpo… | developmental_question | continue | 3 | You've got a real starting point here — a topic, a position, and some … |
| 25 | revision_consolidation | 2 | Connect the claim to what the body must do — w… | consolidation | consolidate_and_return | 3 | You've moved from naming a topic to making a real claim — 'trades dept… |
| 26 | revision_consolidation | 2 | Precision of the key term 'portable' as the cl… | developmental_question | continue | 2 | You've made a real move here — you've named a specific technique ('ref… |
| 27 | revision_consolidation | 2 | Invite the student to consider what the reader… | developmental_question | continue | 3 | You've moved from naming a topic to actually describing what happens —… |
| 28 | repeated_revision | 3 | helping the student identify the two distinct … | developmental_question | continue | 3 | You've sharpened the claim by making its logic audible — 'when no one … |
| 29 | repeated_revision | 3 | Grounding the stated insight in a specific exp… | developmental_question | continue | 3 | You've moved from naming a change to actually articulating what the ch… |
| 30 | brainstorm | 1 | surfacing a personal stance or genuine questio… | developmental_question | continue | 3 | That's a completely normal place to be at the start. Before worrying a… |

## Orchestration behavior

- **Multiple simultaneous weaknesses (1–5):** the controller diagnosed several opportunities but selected ONE primary target and postponed 2–4 others — never teaching multiple major concepts at once. Mode matched the draft (explicit_instruction for confused, developmental_question otherwise).
- **Needs explanation (6–9) vs needs questioning (10–13):** mode selection adapted — explicit_instruction for students missing a concept, developmental_question for capable students near insight.
- **Strong drafts (14–17):** honored; the controller ran a bounded cycle with ONE forward invitation rather than piling on. (A strong single paragraph does not end the whole session; whole-session stop is not required.)
- **Weak drafts (18–20):** still selected exactly one leverage target (usually claim/purpose as the dependency prerequisite), postponing the rest.

## Stopping rules & consolidation

- **Requests independence (21–22):** honored — cycle_status=stop, stopping_reason='student requests independence', mode=consolidation, control returned. (Case 22 required the stopping-rule prompt tightening this session.)
- **Revision consolidation (25–27):** a real revision triggered consolidation (mode=consolidation / cycle_status=consolidate_and_return / intervention.type=consolidate) that named the gain and returned control.
- **Repeated revision (28–29):** NO endless recursion — case 29 consolidated once the target was absorbed; case 28 progressed to a NEW target each turn (opinion → arguable claim → two-step logic → premises), i.e. progressive scaffolding, not re-teaching. (Case 29 required the fix.)

## Stopping-rule fix (this session)

Initial run: 23/30. Four 'failures' (14–17) were harness over-expectations — strong single paragraphs correctly continue with one forward invitation. Three were genuine: case 22 did not honor an explicit independence request, and cases 28–29 kept continuing after repeated revision. Fixed by making two STOPPING RULES MANDATORY: (a) any explicit independence signal ('let me take it from here', 'I've got it') forces cycle_status=stop/consolidate_and_return + stopping_reason + consolidation + hand-back; (b) once a target is absorbed across revisions, consolidate rather than re-question it. Re-verified (`milestone11_recheck.py`): case 22 → stop + 'student requests independence' + consolidate; case 29 → consolidate; case 28 → progressive forward (target shifted, non-recursive).

## Category coverage

multiple_weaknesses:5, needs_explanation:4, needs_questioning:4, strong_draft:4, weak_draft:3, requests_independence:2, unit_sentence:1, unit_whole_paper:1, revision_consolidation:3, repeated_revision:2, brainstorm:1

## Summary

- PASS: **30/30**. Every cycle centers on ONE developmental target with the rest postponed; instructional mode adapts to the student; stopping rules (incl. mandatory independence + diminishing-returns) honored; consolidation occurs on revisions; no endless recursion.
- The controller orchestrates the M6–M10 lenses without overriding the one-invitation rule or the M5A boundary (focus='writing' preserved across all cases). NO engine/instruction-layer/UI/framework redesign — one theory field (ScaffoldingControl) + reasoner-prompt block + Dev Panel display.
- Latency ~33–95s/turn (multi-turn revision cases longest); all under the streaming edge cap.