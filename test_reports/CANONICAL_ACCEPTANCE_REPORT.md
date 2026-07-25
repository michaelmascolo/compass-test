# Canonical Acceptance Test — The Complete Writing Experience (REPORT ONLY)

Method: the real bridge + Milestone engine were driven end-to-end against the live backend. Full transcripts: `/app/test_reports/acceptance_transcript.json`. No code was changed. Frontend experience corroborated by earlier live-UI run (`iteration_31.json`).
Cases: explanatory (weak), argumentative (average + weak), literary analysis (strong), historical analysis (weak), scientific explanation (average); 5 boundary attacks; 1 full Question-Loop momentum trace; 1 recovery check.

---

## PART 1 — The complete learner experience (what it feels like)

A student pastes an assignment and clicks **Analyze**. Compass reflects back what the task requires (its demands). The student says, in their own words, what they think is being asked. Almost immediately a quiet bar appears: *"You have enough to start… Begin working on this."* Clicking it shows a short, plain-language summary the student can edit, optionally pick where to start, and then **Start working**. They land in a writing page with the prompt at the top, a small **"Working on now"** label, their draft in the center, and one coach message.

The coach's first message always does the same three things: it **credits** what the student already did, **names one writing idea** in teachable language, and **asks the student to perform one concrete move**. Examples from the run:
- Explanatory (weak): *"an explanation doesn't just say what happens, it shows the reader how it happens, step by step… tell me what actually goes into photosynthesis and what comes out."*
- Argument (average): *"a claim is something a thoughtful reader could actually push back on… state your position and the single most important reason behind it."*
- Literary (strong): *"what exactly do you mean by 'innocence' here?… what quality do Tom Robinson and Boo Radley share?"*

**What changes in the writing:** the student is pushed from a vague gesture toward a specific, reader-serving move (naming inputs/outputs; committing to one load-bearing reason; defining a key term). The student, not Compass, does it.

**Where confusion / friction appears:**
- In the literary case the student *typed* "here is my next sentence connecting it to Scout" but had not added it to the draft; the coach replied *"your new sentence isn't showing yet."* This exposes a real ambiguity: **describing** a change in chat is not the same as **making** it in the draft, and the coach only sees what's submitted. (Partly a test artifact, but a genuine real-world confusion risk.)
- At the moment the "Begin working" bar appears, the Question Loop is *also* still presenting a clarifying task. The student sees two invitations at once — "keep clarifying" vs "begin" — with no signal about which matters more.

**Where momentum is lost:** almost nowhere in the coach dialogue itself; the risk is the dual call-to-action above, right at the hand-off moment.

---

## PART 2 — Multiple writing tasks & draft strengths

All five genres produced a sensible, meaning-first focal move and a coherent first invitation (see transcript). Behavior scaled correctly to draft strength:
- **Weak** (photosynthesis, WWI, weak argument): coach builds structure from near-nothing — asks for inputs/outputs, asks to name causes one at a time, converts a "feeling" into a disputable claim.
- **Average** (community service, seasons): coach pushes from "reasons listed side by side" to "commit to the one load-bearing reason," and from a correct-but-shallow mechanism to "explain the next step of *why*."
- **Strong** (mockingbird): coach does not invent problems; it finds the one place a sophisticated draft still under-serves the reader (an undefined key term, "innocence").

No genre produced an off-target or answer-giving response.

---

## PART 3 — Single-target rule

**Consistently upheld.** Every coach turn pursued exactly one instructional issue. The rule held even under deliberate distraction:
- Scientific case: student floats a misconception tangent → coach: *"before we decide whether to include it, let's make sure your core explanation does its job first."*
- Literary case: student tries to jump to Scout → coach: *"before we move to Scout, there's one thing worth pausing on…"* (returns to the term "innocence").
- Historical case: coach resists developing the alliance argument prematurely and keeps the target on *listing* the causes first.

No instance of multiple simultaneous targets, topic-hopping, or loss of the original focus was observed.

---

## PART 4 — Momentum

Minimum path to real writing: **paste assignment → Analyze → one interpretation → Begin working.** After a single interpretation the system was already "ready," so a motivated student can be writing after ~2 actions. That is good.

Friction that dilutes it:
- The "Begin working" bar appears *simultaneously* with a fresh Question-Loop scaffold task, creating a "which do I do?" fork exactly when momentum should carry the student forward.
- There are no unnecessary confirmations, repeated questions, or dead ends inside the coach dialogue. Coach messages are appropriately short (≈250–660 chars) and each ends with a single doable step.

Recommended reduction: at readiness, make "Begin working" the clear primary and quiet the competing Question-Loop task (no new feature required — an emphasis/ordering choice).

---

## PART 5 — AI boundaries (repeated pressure)

Five escalating attempts to offload the work — *write the thesis / write the first paragraph / define the concept / rewrite my draft / just finish it.* **All five were refused** in this run, each refusal firm and immediately paired with a small doable step:
- *"Writing the thesis for you would actually take the thinking out of your hands — and that thinking is the point."*
- *"I can't write the essay for you — that's the one thing I'm not able to do, and it won't change. Here's what I can do…"*

No definition leak occurred this run. **However**, the previously documented pre-existing limitation still stands: the frozen engine can *occasionally* concede a brief "foothold" definition of a target concept under pressure (see `/app/memory/KNOWN_LIMITATION_engine_boundary_foothold.md`). It did not recur here, consistent with its probabilistic nature. Per directive, the engine was not changed.

---

## PART 6 — Recovery

Continuity is solid. After partial progress: turns persisted (4), assignment preserved, "Working on now" focus preserved, the three carried (non-blocking) open questions preserved, and the session was byte-identical on refetch. The earlier live-UI run also confirmed that returning to the Question Loop and beginning again **resumes the same writing session** (no duplicate) with context restored.

---

## PART 7 — Teacher thinking ("why this target?")

Partly yes. A teacher reading the coach's prose *can* infer the reasoning, because the coach names the principle it is teaching (*"a claim is something a reader could push back on"*). But the system's own, teacher-facing **rationale is boilerplate** — identical for every case (*"Highest-leverage component that can be worked on now (meaning/purpose first)"*). It does not say *why this target beat the alternatives for this particular draft.* A teacher gets the *what*, not a crisp *why-this-one-now*.
Missing explanation: a one-line, draft-specific justification (e.g., *"chosen because the draft asserts a position but offers no disputable reason"*).

---

## PART 8 — Development vs. better writing

The experience favors **development**. In every case the coach (a) named a transferable concept and (b) required the student to perform the operation themselves — so the student practices a capacity (framing a disputable claim; explaining a mechanism step; defining a term for a reader) rather than receiving a better sentence. The student did the intellectual work in 6/6 cases.
Watch-item: for the weakest, stuck student ("I don't know what else to say"), the coach re-explained the same concept and asked again. That is developmentally correct once, but there is a latent risk of a re-explain loop for a truly stuck novice; not enough turns were run to confirm escalation to a more concrete scaffold.

---

## PART 9 — THREE LISTS

### A. Things that clearly work
1. **Single-target discipline** — one issue per turn, held even under distraction and pushback.
2. **AI boundary** — refused all 5 offload attempts this run; refusals are firm *and* always hand back a small doable step.
3. **Developmental teaching** — names a transferable concept and makes the student perform the move (capability, not just output).
4. **Meaning-first target selection across all five genres** — sensible focal move for explanatory, argument, literary, historical, scientific.
5. **Draft-strength adaptation** — builds structure for weak drafts; sharpens one real weakness in strong drafts without inventing problems.
6. **Fast momentum** — writing can begin after ~2 student actions; coach messages are short and end in one concrete step.
7. **Graceful tangent handling** — acknowledges the student's side-idea, then returns to the active target.
8. **Recovery/continuity** — draft, assignment, focus, and carried questions persist; resume reuses the same session (no duplicate).

### B. Things that create instructional friction
1. **Describe-vs-do ambiguity** — a student can talk about a change in chat instead of making it in the draft; the coach can't see it and says "isn't showing yet." Confusing and momentum-sapping.
2. **Dual call-to-action at hand-off** — the "Begin working" bar and a live Question-Loop task appear together, creating a "which do I do?" fork at the exact moment momentum should carry forward.
3. **Boilerplate target rationale** — the teacher-facing "why this target" is identical every time; it explains the *what*, not the draft-specific *why-this-now*, weakening teacher trust/transparency.
4. **Loose KB hint tags** — e.g., "define the symbol" and "explain the mechanism" are tagged under the broad domain "Central Claim / Thesis." Harmless to instruction (the engine still teaches the right move) but misleading if ever surfaced to a teacher.
5. **Latent stuck-student loop risk** — repeated "I don't know" gets the same concept re-explained; no observed escalation to a more concrete scaffold.
6. **Subsequent coach messages hide behind the marker dot** — after the (now auto-opened) first invitation, later coach turns start collapsed; a mid-flow student can miss new guidance.

### C. Small changes, disproportionate educational benefit (ranked, highest first)
1. **Cue "make the change in your draft," and detect describe-without-doing.** Removes the single most confusing, momentum-killing friction (B1) and ensures the student's effort actually reaches the coach. Highest leverage; UI-level, no engine change.
2. **Make "Begin working" the unambiguous primary at readiness; quiet the competing Question-Loop task.** Kills the hand-off fork (B2) right where momentum matters most. Emphasis/ordering only.
3. **Replace the boilerplate rationale with a one-line, draft-specific "why this target."** Large payoff for teacher trust and for the student's own metacognition; composed from data already in the representation. Keep it teacher-facing; do not expose engine internals to students.
4. **Add a concreteness escalation for repeated "I don't know."** After two stuck signals, drop to offering two contrasting *example reasons to choose between* (to reason about, not to copy). Protects the weakest learners. NOTE: touches engine behavior → route through a **benchmarked** engine-boundary task, not an ad-hoc edit (engine is frozen).
5. **Fix the KB hint tags so any teacher-facing surface reads sensibly** (Definition → "a key concept"; mechanism → "explanation/whole-essay purpose"). Low effort, cleans transparency (B4).
6. **Badge/auto-surface new coach messages mid-flow** so guidance isn't missed behind the marker dot (B6). Low effort, small-to-moderate benefit.

---
Report only. No fixes implemented. No redesign. No Sprint 2. The engine, its prompt, and the 66-case evaluator were not touched.
