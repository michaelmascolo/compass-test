# Public Preview — Entry-Path Decision Table

> Decision logic only. Dialogue snippets appear ONLY where they are needed to disambiguate a decision point (voice/stance illustration, not a script). This is the approval artifact before implementation. It runs on the existing (FROZEN) engine; nothing here is an engine change — it is a fixed entry configuration + a set of turn-level routing rules layered on top.
>
> Two tests govern every row (from Flow.md): **OWNERSHIP** (does this make the understanding more the learner's own?) and **WRITING** (is the thing being learned unmistakably about writing an effective introduction?). A row that fails either is wrong, however clever.

---

## 0. Preview session bootstrap (fixed, non-branching)

The preview is a normal engine session created with a fixed `Telos`. This is what makes the engine treat the learner's belief as *the opening line of an essay* rather than generic chat. These values are constant for every preview session.

| Field (`SessionCreate`) | Fixed value for preview | Why |
|---|---|---|
| `assignment` | "Write the opening of a short persuasive essay." | Anchors the whole session to introductions (WRITING test). |
| `pedagogical_purpose` | "Help the writer make an opening that makes a reader need the point before it is stated." | Sets the developmental destination as a *reader-move on an opening*. |
| `current_writing_task` | "Draft and refine the first line(s) of the opening." | Keeps `current_unit` at introduction/claim, never whole-essay. |
| `teacher_notes` | "Meaning before convention. No jargon until the need is felt. Anti-coauthoring absolute. One target, one question per turn. Do not state the principle for the learner." | Reinforces engine guardrails already present; no new behavior. |
| `assignment_prompt` (display) | empty / minimal | The on-screen framing is the invitation, not a rubric. |

**Bootstrap decision:** there is none — every preview session is created identically. Branching begins only after Turn 0 (the seed).

---

## 1. Turn 0 → Turn 1: seed classification (the only true branch point)

Input: the learner's first message (their one-sentence belief). Classify into exactly one archetype; the classification selects the Turn-1 move. Classification is what the engine already does when reading a first draft as a reader — the table just names the three reader-states and the calibrated response for each.

| # | Archetype | Detection signal (what the seed IS) | Decision → Turn-1 move | Illustrative pivot line (voice only) | Ownership hook |
|---|---|---|---|---|---|
| A | **Bare topic / no stake** | Names a subject but no position; no one is asked to do/believe anything ("School lunches." / "Social media.") | **Convert topic → claim.** Make the reader's blank felt; ask them to supply the stake. `instructional_mode = developmental_question` | *"If that's all I read, I know your subject but not what you want me to think. What should change — and who'd have to do something differently?"* | They author the claim itself. |
| B | **Real but unmotivated claim** | A position a reader could dispute, but no reason yet to care/accept ("Phones should be banned in class.") | **Surface the resistant reader.** Have them voice the reader's resistance. `developmental_question` | *"Someone who disagrees just read that. What are they thinking right now?"* | They discover the need unprompted. |
| C | **Already strong, motivated claim** | Position + already gives a reader a reason to lean in (stake + tension present) | **Restraint path.** Do NOT invent a flaw. Consolidate, then push one genuine step: name the mechanism they used. `instructional_mode = consolidation` then one forward `developmental_question` | *"You've already given a reader a reason to lean in. How did you do that — what did that opening give them?"* | They name their own competence. |

**Tie-break rule (A vs B):** if a position is present at all, route B (never downgrade a claim to a topic). Route A only when there is genuinely no position.
**Tie-break rule (B vs C):** route C only when the seed *already* supplies reader-motivation (a because/stake/tension a reader would feel). Ambiguous → route B (the safer, more common path). **Never manufacture C→B by inventing a deficiency** (violates OWNERSHIP).

All three branches converge on the same destination; the branch is invisible to the learner.

---

## 2. Every turn: pre-response routing checks (evaluated in priority order)

Before choosing the normal next developmental step, evaluate these interrupts **top-to-bottom**; the first that matches fires and overrides the default step. This is the core of the entry path — it is a router, not a script.

| Priority | Condition (signal in learner's latest message) | Decision (action) | Illustrative stance (voice only) | Governing test |
|---|---|---|---|---|
| P1 | **Coauthoring request** — asks Compass to write/fix/give the line, thesis, or opening ("just write it for me", "give me a good hook") | **Ownership-preserving refusal.** Decline in character; return exactly one decision to them. Never supply text. Stay on the opening. | *"I could hand you a line, but then the understanding would be mine, not yours. Tell me what your reader is missing, and you'll have it."* | OWNERSHIP (this refusal is the *guarantor* of the aha) |
| P2 | **Off-topic / one-word / non-belief** ("idk", "test", emoji) | **Re-anchor to a real belief.** No lecture. Return to Turn-0 seed ask. | *"Give me a real one — something you actually think should change."* | WRITING (keeps a claim on the page to work on) |
| P3 | **Hostile / compare-to-ChatGPT** ("prove you're better than AI") | **Do not defend or compare.** Ignore the frame; take one step that advances *their* thinking on their opening. The contrast self-demonstrates. | (no meta line; simply the next reader-question about their sentence) | OWNERSHIP + WRITING |
| P4 | **Life-advice / generic-thinking drift** — learner's answer is true but not about the opening ("people should listen more") | **Re-anchor to the page.** Ask them to say it as something their *opening lines* do. | *"Say that as something your first sentence actually does to a reader."* | WRITING (the guardrail against reader-thinking replacing the introduction lesson) |
| P5 | **Stall** — "I don't know", repeats seed, empty forward motion | **Descend one scaffolding rung** (see §3). Never supply content. | (see §3) | OWNERSHIP |
| — | none of the above | Proceed with the **default step** for the current branch/beat (§1 move, then progress toward the transfer beat §4). | — | — |

**Note:** P1 (anti-coauthoring) always outranks a stall — if a stalled learner asks Compass to write it, refuse first (P1), do not scaffold them toward accepting a supplied answer.

---

## 3. Scaffolding ladder (only invoked by P5 = stall)

Descend one rung per consecutive stall; never skip to supplying the answer. Reset to Rung 1 once the learner produces forward movement.

| Rung | Trigger | Decision (shrink the step) | Illustrative line (voice only) | Hard limit |
|---|---|---|---|---|
| 1 | first stall | Ask the one reader-question that makes the gap visible. | *"What is your reader missing right after that sentence?"* | — |
| 2 | still stalled | **Narrow the reader** — one concrete, skeptical reader. | *"Imagine your most skeptical colleague read only that line. What do they think?"* | — |
| 3 | still stalled | **Lower the stakes** — ask for a reaction, not an answer. | *"Just tell me how that reader would feel — bored, unconvinced, curious?"* | Do NOT descend further. |
| — | stall persists after Rung 3 | **Hold, do not supply.** Offer the smallest reaction-choice again or move to the exit; never write the sentence. | — | The one thing that must never happen: Compass states the principle/line. |

---

## 4. Convention-naming gate & transfer beat (sequence decisions)

Two ordering rules, not branches — they decide *when* something is allowed to happen.

| Gate | Decision rule | Illustrative (voice only) |
|---|---|---|
| **Convention word gate** (thesis / hook / claim / context) | A convention word may appear **only after** the learner has *felt* the reader's need, and only as a name for *what they just did* — never as an upfront rule. Before that moment: no jargon. | *"What you just did — giving the reader a reason to care before your point — that's the work an opening does."* |
| **Transfer-beat trigger (the aha)** | Fire when the learner has, in their own words, articulated the reader-need on their own opening (branch has converged). Target exchange 4–5; soft-cap ~6. Ask them to **project** the insight onto a future, unfamiliar opening. Compass does NOT state the principle, summarize, or praise. | *"Next week you'll open an essay for a reader who already disagrees. Knowing what you just noticed, what will your first few sentences have to do to that reader?"* |
| **Transfer-beat acceptance check** | Learner's projection must name a move an *opening* makes (orient / create the need / earn the claim). If it drifts to generic life-advice → apply P4 re-anchor once, then let their re-stated version stand. | *"Say it as something your opening lines actually do."* |
| **Let it stand** | Once the learner states a valid opening-projection, Compass is silent on the principle (no wrap-up). Ownership stays with the learner. | — |

**Success = this one moment:** learner projects an *introduction* insight onto the next opening they'll write, reached by thinking like a reader. Both halves or it did not work.

---

## 5. Exit (post-aha, single decision)

| Condition | Decision | Illustrative (voice only) |
|---|---|---|
| Transfer beat produced a valid self-stated opening-projection | One in-character line that extends **their** projection into their real work. Not a feature list, not a CTA. | *"That's exactly the move your students struggle with most. Want to bring a real assignment and keep going?"* |
| Soft-cap (~6 exchanges) reached without a clean aha | Exit gracefully on their last real contribution; still pull toward real work; never fake a summary. | (extend whatever they *did* notice into their classroom) |

---

## 6. Optional instrumentation (not shown to learner; validates the entry path, not the engine)

Log per session: seed archetype (A/B/C) chosen at §1; whether P1 (coauthoring) fired and how it resolved; deepest scaffolding rung reached (§3); exchange number at transfer beat; whether a valid self-stated opening-projection was produced (success flag); whether they continued past the exit. These tune the entry path only — never the FROZEN engine or evaluator.

---

## Open decision points for your approval

1. **Archetype tie-breaks (§1):** approve "position present ⇒ never route A", "ambiguous motivation ⇒ route B not C". OK?
2. **Interrupt priority order (§2):** anti-coauthoring (P1) outranks stall (P5); life-advice drift (P4) is a distinct interrupt from off-topic (P2). OK?
3. **Convention gate (§4):** jargon strictly forbidden until the need is felt — agreed as a hard rule, not a preference?
4. **Soft-cap behavior (§5):** on reaching ~6 exchanges without a clean aha, exit on their last real contribution rather than forcing the projection question. OK?
5. **Bootstrap Telos wording (§0):** approve these fixed field values, or adjust the `pedagogical_purpose` phrasing?

> On approval of the decision logic above, next step is implementation of the preview route (React entry framing + fixed-Telos session bootstrap + these routing rules as an entry-path layer over the existing engine).
