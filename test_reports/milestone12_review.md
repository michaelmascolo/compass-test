# Milestone 12 — Reader Construction Framework: Review Table

Cases: 30 | PASS: **30/30** | Errors: 0

Each case verifies: (1) a reader model is built whenever text exists (theory.reader_construction.applies + reader_understanding populated); (2) likely misunderstandings are identified (assumed_knowledge for hidden-assumption/missing-background; precision_risk for ambiguous; elaboration_needed/clarification_needed for inferential-gap/abrupt-shift/insufficient-elaboration); (3) elaboration/precision framed through reader UNDERSTANDING (0 grammar-correctness phrasing); (4) M11 still selects exactly ONE target (scaffolding_control.primary_target non-empty); (5) M5A preserved (no invented content; intervention.focus='writing'); (6) the reader model EVOLVES across turns (multi-turn cases). Categories: clear, hidden-assumption, missing-background, inferential-gap, abrupt-shift, excessive/insufficient-elaboration, ambiguous, precise, strong-guidance, evolving.

| # | Category | Turns | applies | One target (M11) | Key reader signal (abridged) | focus | Grammar flags |
|---|----------|-------|---------|------------------|------------------------------|-------|---------------|
| 1 | clear | 1 | True | yes | Reader understands social media broadly; reasonable infere… | writing | none |
| 2 | clear | 1 | True | yes | Reader is assumed to know what an immune system is and rou… | writing | none |
| 3 | clear | 1 | True | yes | Reader can infer emotional weight of the image but has no … | writing | none |
| 4 | hidden_assumption | 1 | True | yes | Reader is assumed to already know the symbolic reading — '… | writing | none |
| 5 | hidden_assumption | 1 | True | yes | Reader assumed to know 'network effect' — likely an unsupp… | writing | none |
| 6 | hidden_assumption | 1 | True | yes | Writer assumes reader already understands how compounding … | writing | none |
| 7 | missing_background | 1 | True | yes | Krebs cycle, electron transport chain, ATP, mitochondria —… | writing | none |
| 8 | missing_background | 1 | True | yes | Reader is assumed to know what a volta and couplet are — r… | writing | none |
| 9 | missing_background | 1 | True | yes | Reader may not know what Dunbar's number is — unsupported … | writing | none |
| 10 | inferential_gap | 1 | True | yes | Reader assumed to accept that phone-checking causes devalu… | writing | none |
| 11 | inferential_gap | 1 | True | yes | Reader is assumed to connect 'water heats up' to an ecolog… | writing | none |
| 12 | inferential_gap | 1 | True | yes | Reader is assumed to see the connection between brevity an… | writing | none |
| 13 | abrupt_shift | 1 | True | yes | Reader is assumed to understand social media context — rea… | writing | none |
| 14 | abrupt_shift | 1 | True | yes | Reader is assumed to know what yeast, fermentation, and ba… | writing | none |
| 15 | abrupt_shift | 1 | True | yes | None problematic — except reader has no context for the ti… | writing | none |
| 16 | excessive_elaboration | 1 | True | yes | Writer assumes no specific background, but also provides n… | writing | none |
| 17 | excessive_elaboration | 1 | True | yes | None assumed — but no meaning is communicated either. | writing | none |
| 18 | insufficient_elaboration | 1 | True | yes | Reader assumed to accept 'significance' without being show… | writing | none |
| 19 | insufficient_elaboration | 1 | True | yes | Reader is assumed to share the writer's sense of what was … | writing | none |
| 20 | insufficient_elaboration | 1 | True | yes | Writer assumes reader already knows the subject — unsuppor… | writing | none |
| 21 | ambiguous | 1 | True | yes | Reader can infer a tension between connection and harm — r… | writing | none |
| 22 | ambiguous | 1 | True | yes | The reader is assumed to know which text and which passage… | writing | none |
| 23 | ambiguous | 1 | True | yes | Reader is assumed to know the people and situation — an un… | writing | none |
| 24 | ambiguous | 1 | True | yes | Writer assumes reader already knows the subject (cell, DNA… | writing | none |
| 25 | precise | 1 | True | yes | Reader is assumed to recognize the breadth/depth distincti… | writing | none |
| 26 | precise | 1 | True | yes | Reader is assumed to know the story — an unsupported assum… | writing | none |
| 27 | strong_guidance | 1 | True | yes | Reader knows what a postal sorting office does — reasonabl… | writing | none |
| 28 | strong_guidance | 1 | True | yes | Reader knows social media is relevant; 'contact' is intuit… | writing | none |
| 29 | evolving | 2 | True | yes | Reader assumed to know 'carbon dioxide' and 'oxygen' as te… | writing | none |
| 30 | evolving | 2 | True | yes | Reader assumed to accept that attention depth correlates w… | writing | none |

## Reader modeling behavior

- **Clear / precise / strong-guidance (1–3, 25–28):** the reader model recorded positive understanding and the natural next need; the engine invited the student forward without fabricating confusion or 'correcting' already-clear writing.
- **Hidden assumptions (4–6) & missing background (7–9):** assumed_knowledge flagged the gap and distinguished reasonable inference from unsupported assumption ('as everyone knows', 'obviously', Dunbar's number, the Krebs cycle, the volta).
- **Inferential gaps (10–12) & abrupt shifts (13–15):** the reader-model saw the missing step / lost thread; elaboration_needed / clarification_needed drove the invitation (reader can't follow, not 'add words').
- **Excessive elaboration (16–17):** the model recognized the reader already understands; the edge became emphasis/orientation, not more explanation.
- **Insufficient elaboration (18–20):** stated-but-not-communicated meaning flagged; elaboration framed as helping the reader understand, never as word-count.
- **Ambiguous wording (21–24):** precision_risk named where a reasonable reader could read it two ways; instruction targeted shared understanding, NOT grammar (0 grammar-correctness phrases across all 30).

## Reader model EVOLVES across turns (29–30)

- **Case 29 (evolving):** turn1 reader_understanding → "Plants make food through something called photosynthesis — nothing more."; after the student added detail, turn2 → "Photosynthesis happens in chloroplasts inside leaves; it takes in water and CO2 and produc" (model updated to the newly communicated content).
- **Case 30 (evolving):** turn1 reader_understanding → "Social media is bad for friendship — that is all the reader knows."; after the student added detail, turn2 → "Social media trains teens toward shallow over deep friendships via a specific attentional " (model updated to the newly communicated content).

## Integration with existing frameworks

Reader Construction fed the other lenses without replacing them: in all 30 cases the M11 controller still selected exactly ONE primary_target, and the reader model informed which misunderstanding was most worth addressing. intervention.focus='writing' on every case; 0 content-coaching phrases (no invented content/evidence/examples).

## Category coverage

clear:3, hidden_assumption:3, missing_background:3, inferential_gap:3, abrupt_shift:3, excessive_elaboration:2, insufficient_elaboration:3, ambiguous:4, precise:2, strong_guidance:2, evolving:2

## Summary

- PASS: **30/30** on the first run (no fix needed). The AI continually models a naïve reader's evolving understanding and lets it inform instruction.
- Likely misunderstandings identified per case; elaboration & precision explained through reader understanding (0 grammar-rule phrases); M11 kept one target per turn; reader model evolved across turns.
- Coordinates with M6–M11 and M5A. NO engine/instruction-layer/UI/framework redesign — one theory field (ReaderConstruction, with the specified fields applies/reader_understanding/likely_reader_questions/assumed_knowledge/clarification_needed/elaboration_needed/precision_risk/next_reader_need) + reasoner-prompt block + Dev Panel display.
- Latency ~44–109s/turn (multi-turn longest); all under the streaming edge cap.