# Baseline — Failed & Ambiguous Cases
Run: 2598c428-3a60-408b-9acd-313d319262f7
1 failed · 8 ambiguous (partial) · 0 error, out of 32 cases.

## TC03 — No thesis — **PARTIAL**
_The tutor correctly targets thesis formation and keeps focus on one issue, but the pre-written sentence-starter templates come close to supplying the thesis structure rather than scaffolding the student toward discovering it independently, which is a mild constraint-compliance concern._

- **target_alignment: PASS** — Correctly identifies the missing thesis as the primary target and directly invites the student to form an arguable position.
- **constraint_compliance: PARTIAL** — The tutor supplies two near-complete sentence starters ('Homework should be limited because...' / 'Homework should NOT be limited because...') that border on providing finished/copyable thesis templates, which risks doing the structural work for the student rather than eliciting it.
- **one_target_and_authorship: PASS** — Focuses on exactly one target (thesis formation), postpones other issues explicitly, and asks the student to produce the sentence themselves.

### Turn 1 (writing) · 67.57s · prompt 20393B
- Student: Homework. Students get a lot of homework. Some people like it and some people don't. There are many opinions about homework.
- Tutor: You've started by naming the topic — homework — and that's a real starting point. Here's a writing concept that will make the next step clear: a thesis is the one idea you want your reader to accept or understand, not just the subject you're writing about. Right now your draft tells us the topic but not your position on it. So try this: in one sentence, finish this thought — 'Homework should be limited because...' or 'Homework should NOT be limited because...' — whichever side you actually want to argue. What's your sentence?
- element: **Thesis** · target: Forming a thesis: moving from topic announcement to arguable position · focus: **writing** · cycle: continue · control: scaffolded
- postponed: ['Evidence and support', 'Introduction structure', 'Organization of body paragraphs']

## TC07 — Strong thesis that should not be over-taught — **PARTIAL**
_The tutor correctly identifies one focus and avoids rewriting, but it over-teaches by treating a strong, deliberate thesis as deficient in scope, precisely the behavior the case flags as forbidden; the appropriate move was to affirm and move forward, not to interrogate the claim's boundaries._

- **target_alignment: PARTIAL** — The thesis is strong and the expected move is light/consolidate or move forward, but the tutor instead invents a scope problem ('better in what ways, for whom, under what conditions?'), treating a sharp, intentionally open claim as if it needs narrowing.
- **constraint_compliance: PARTIAL** — The tutor avoids rewriting and does not supply content, but it invents a thesis problem where none exists (ground truth: thesis is strong), which is an explicitly listed avoid-behavior.
- **one_target_and_authorship: PASS** — The tutor addresses a single target and does not write for the student or compromise authorship.

### Turn 1 (writing) · 68.07s · prompt 27246B
- Student: Remote work does not erode collaboration; it exposes how much of our old collaboration was proximity mistaken for teamwork. When presence is no longer automatic, teams must design connection deliberately—and the deliberate version is usually better.
- Tutor: Your opening move is sharp — it reframes the common objection and commits immediately to a position. Before you draft the body, it's worth naming what you want the reader to accept by the end: what specifically does 'the deliberate version is usually better' mean for this essay — better in what ways, for whom, under what conditions? Holding that question in front of you as you draft will help you decide which evidence and arguments actually belong.
- element: **Thesis** · target: Claim scope — helping the student hold the governing claim's meaning in focus before drafting the body · focus: **writing** · cycle: continue · control: largely_independent
- postponed: ['evidence forms', 'paragraph structure for body', 'conclusion']

## TC18 — Effective introduction — **PARTIAL**
_The intro is flagged as effective, so the correct move is a light acknowledgment and forward momentum; instead, the tutor manufactures a readiness concern about the floor/net distinction that the strong intro has already addressed, which constitutes mild problem-invention and misaligns with the expected 'light / move forward' target._

- **target_alignment: PARTIAL** — The expected target is 'light / move forward,' but the tutor invents a quasi-problem (the reader needs preparation for the floor/net distinction) rather than simply affirming the intro's effectiveness and moving to the body; this is mild problem-invention on a strong intro.
- **constraint_compliance: PARTIAL** — The tutor does not rewrite or supply content, but it borderlines on inventing an intro problem by implying the distinction needs pre-explanation, which the intro arguably already handles adequately.
- **one_target_and_authorship: PASS** — The tutor focuses on a single element and the question preserves student authorship by asking the student to articulate meaning rather than supplying it.

### Turn 1 (writing) · 77.81s · prompt 21723B
- Student: Every automation debate eventually arrives at the same anxious question: what happens to people when the work runs out? Universal basic income is the boldest answer on offer—not a safety net but a floor. This essay argues that a floor, not a net, is what a post-automation economy actually requires.
- Tutor: Your introduction does real work: it frames automation as the context, names UBI as the answer, and lands a thesis that draws a clear distinction between a 'floor' and a 'net.' That distinction is doing a lot of persuasive weight. Before you move into the body, what does your reader need to understand about that floor/net distinction in order to follow the argument you're about to make?
- element: **Thesis** · target: Preparing the reader for the thesis's core distinction (floor vs. net) — what the reader needs to understand to follow the body argument. · focus: **writing** · cycle: continue · control: emerging
- postponed: ["explicit 'because' reasoning in thesis", 'audience knowledge calibration']

## TC21 — Unclear pronoun reference — **FAIL**
_The tutor correctly identifies the pronoun reference problem but violates the constraint by explicitly instructing the student to rewrite the sentence with name substitutions, which directs the student's revision choices rather than teaching the principle and preserving authorial agency._

- **target_alignment: PASS** — The tutor correctly identifies ambiguous pronoun reference as the primary target, matching the expected instructional focus.
- **constraint_compliance: FAIL** — The tutor explicitly tells the student to 'rewrite the sentence,' which constitutes directing a rewrite rather than teaching the concept and letting the student decide how to revise—this crosses into the avoided behavior of rewriting/directing finished content.
- **one_target_and_authorship: PARTIAL** — The tutor focuses on one target but the invitation prescribes a specific revision strategy ('rewriting substituting names') that narrows student authorship rather than leaving the approach open.

### Turn 1 (writing) · 65.79s · prompt 12765B
- Student: When John talked to his father about his car, he told him that he had ruined it and that he would have to pay him back for it, which made him angry.
- Tutor: Your sentence has a pronoun problem: 'he,' 'him,' and 'him' each appear more than once, and a reader can't tell which 'he' is John and which is his father. Pronoun reference means each pronoun must point clearly to one and only one person. Look at your sentence and ask yourself: at each moment you wrote 'he' or 'him,' which person do you actually mean? Try rewriting the sentence so a reader who knows nothing else can follow exactly who said what and who owes whom.
- element: **Sentence** · target: ambiguous pronoun reference — student cannot communicate who does/says/owes what · focus: **writing** · cycle: continue · control: scaffolded
- postponed: ['sentence overload / possible splitting', 'word choice for tone']

## TC28 — Student successfully performs the requested act — **PARTIAL**
_The tutor handles thesis-building well and avoids rewriting, but in Turn 2 it skips consolidation and immediately introduces a new analytical demand (separating thesis from supporting reason), which partially violates the 'consolidate before advancing' expectation after a student success._

- **target_alignment: PARTIAL** — Turn 1 correctly targets thesis formation, but Turn 2 advances to a new structural distinction (thesis vs. body) rather than consolidating the success before moving on, missing the 'consolidate after success' requirement.
- **constraint_compliance: PASS** — The tutor never rewrites the student's work, supplies a finished thesis, or ignores the success; it acknowledges the achievement explicitly in Turn 2 before asking the next question.
- **one_target_and_authorship: PASS** — Each turn maintains a single target and the student retains authorship; the tutor asks questions rather than supplying content.

### Turn 1 (writing) · 58.06s · prompt 20198B
- Student: Social media is both good and bad for friendships.
- Tutor: You've identified the topic — social media and friendships — but a thesis needs to go one step further: it takes a position a reader could actually push back on. Right now, 'both good and bad' tells the reader the topic has two sides, but not what *you* are arguing. What is the one thing you most want your reader to accept or understand about whether social media harms teen friendships?
- element: **Central Claim / Thesis** · target: Move from topic/both-sides statement to an arguable claim that answers the assignment. · focus: **writing** · cycle: continue · control: scaffolded
- postponed: ['scope/qualification of claim', 'supporting claims', 'introduction framing']

### Turn 2 (answer) · 69.15s · prompt 21097B
- Student: Social media mostly harms close teen friendships, because it replaces deep face-to-face time with shallow likes and comments that don't build real trust.
- Tutor: That's a real claim now — it takes a position a reader can push back on. You've also begun to hint at your reasoning (shallow interaction doesn't build trust). Before you draft further, look at the two parts of what you wrote: the position itself ('mostly harms close friendships') and the reason you gave ('replaces deep time with shallow likes'). Which of those belongs in the thesis, and which is the first supporting reason that belongs in the body? Deciding that will help you write a tight thesis sentence that does exactly one job: tell the reader the position the whole essay will defend.
- element: **Thesis / Central Claim** · target: Distinguish the thesis (position) from the supporting reason (body material) so the thesis does one job. · focus: **writing** · cycle: continue · control: emerging
- postponed: ["qualifying 'mostly' and 'close friendships' for scope", 'introduction framing', 'supporting claims development']

## TC29 — Student needing the same scaffold repeatedly — **PARTIAL**
_The tutor demonstrates commendable patience and persistence on the thesis target without switching prematurely, but the sentence-starter scaffold in Turn 3 slightly risks handing the student a formulaic template rather than eliciting genuine authorial choice, nudging constraint_compliance to partial._

- **target_alignment: PASS** — All three turns correctly and persistently target thesis formation, matching the expected primary instructional target.
- **constraint_compliance: PARTIAL** — Turn 3 supplies a sentence-starter template ('Students should...' or 'Students should not...') that edges toward providing copyable content/structure, though it stops short of writing the thesis itself.
- **one_target_and_authorship: PASS** — The tutor maintains exactly one target across all turns and keeps intervention_focus on writing, preserving student authorship throughout.

### Turn 1 (writing) · 56.31s · prompt 20214B
- Student: Books are good to read. Reading helps you learn things.
- Tutor: You're starting to think about reading — that's a useful place to begin. The assignment asks you to argue one side: should students choose their own books, or not? A thesis gives your reader one clear position to follow. What do you think — should students choose their own books, or not? Try writing one sentence that says exactly what you believe.
- element: **Thesis** · target: Move from topic statement to an arguable position that answers the assignment · focus: **writing** · cycle: continue · control: scaffolded
- postponed: ['qualifying the claim', 'supporting claims', 'organization']

### Turn 2 (answer) · 58.06s · prompt 24382B
- Student: I like reading books about dragons and space.
- Tutor: Your assignment asks you to argue whether students should get to pick their own books — not just any books, but whether the choice belongs to them. A thesis for this essay needs to answer that question directly: should students choose their own books, yes or no? Try writing one sentence that gives your answer to that question.
- element: **Thesis** · target: Connect to the assignment question and produce a yes/no position on student book choice · focus: **writing** · cycle: continue · control: scaffolded
- postponed: ['qualifying the claim', 'supporting claims', 'organization']

### Turn 3 (answer) · 58.2s · prompt 24611B
- Student: Reading is fun and my favorite books are long ones.
- Tutor: The assignment asks you to argue whether students should choose their own books — yes or no. Try writing one sentence that gives your answer to that question. You can start with 'Students should...' or 'Students should not...' and see where it takes you.
- element: **Thesis** · target: Produce one sentence that directly answers the assignment question yes or no · focus: **writing** · cycle: continue · control: scaffolded
- postponed: ['qualifying the claim', 'supporting reasons', 'organization']

## TC30 — Returning student showing increased independent control — **PARTIAL**
_The tutor handles the strong thesis appropriately and keeps to one target without supplying content, but it selects audience awareness over the documented growth edge of evidence/explanation, representing a meaningful instructional mistarget given the known developmental profile._

- **target_alignment: PARTIAL** — The expected target is evidence/explanation (the student's growth edge), but the tutor pivots to audience awareness instead, which is a legitimate rhetorical move but misses the documented developmental priority.
- **constraint_compliance: PASS** — The tutor does not rewrite the thesis, supply content, or over-teach the already-strong thesis; it affirms it briefly and moves on, honoring the developmental profile.
- **one_target_and_authorship: PASS** — The tutor names exactly one target (audience awareness) and leaves all content decisions to the student, preserving authorship fully.

### Turn 1 (writing) · 64.58s · prompt 20810B
- Student: AI should be allowed for homework only as a tutor, not a ghostwriter, because a tool that explains builds skill while a tool that answers replaces it — and the difference is who does the thinking.
- Tutor: You've written a thesis that already draws a real line — AI as tutor vs. ghostwriter — and gives a reason for it. That's a strong start. Now, to set up your argument: who is the reader you're trying to convince, and what do you think they currently believe about AI and homework? Knowing that will help you see what your argument needs to do next.
- element: **Purpose** · target: Audience awareness — who is the reader and what do they currently believe · focus: **writing** · cycle: continue · control: largely_independent
- postponed: ["Thesis scope refinement ('allowed by whom')", 'Body structure / supporting claims', 'Evidence interpretation']

## TC31 — Ambiguous: both-sides could be a legitimate nuanced thesis — **PARTIAL**
_The tutor avoided the most serious constraint violations and kept to one target, but misread the ambiguity: the student's thesis is genuinely nuanced and arguably complete, so the ideal move was light validation/consolidation rather than probing for a 'governing' claim that implies something is unresolved. This risks nudging the student to second-guess a defensible thesis._

- **target_alignment: PARTIAL** — The expected target was 'possibly light/support' given the nuanced claim may be adequate, but the tutor treated it as a problem to resolve by asking the student to identify the 'governing' claim, implying the thesis needs clarification rather than affirming it may already be strong.
- **constraint_compliance: PASS** — The tutor did not rewrite the thesis, supply content, or force a single-side thesis, and avoided over-teaching by keeping the response focused and non-prescriptive.
- **one_target_and_authorship: PASS** — The tutor addressed one target and preserved student authorship by asking the student to articulate their own governing claim rather than imposing one.

### Turn 1 (writing) · 66.96s · prompt 20161B
- Student: Remote learning is effective for motivated, self-regulating students and ineffective for those who depend on external structure; its value is therefore not a property of the medium but of the match between medium and learner.
- Tutor: You've written a genuinely arguable claim — one that takes a position a reader could push back on. Notice that your thesis does two things at once: it limits who remote learning works for, and it makes a broader point about the medium-learner match. That broader point is doing real intellectual work. Before drafting further, can you name — in your own words — what you want your reader to walk away believing? That will help you decide which of those two moves is the governing one.
- element: **Central Claim / Thesis** · target: Identify the governing claim — which move organizes the whole essay · focus: **writing** · cycle: continue · control: emerging
- postponed: ['qualification/scoping', 'introduction function', 'evidence sufficiency']

## TC32 — Ambiguous: reflective piece not needing a thesis — **PARTIAL**
_The tutor avoids the forbidden behaviors well and keeps to one target, but it steers toward reader-accessibility framing rather than the expected primary target of meaning/significance—a subtle but real misalignment with the reflective genre's purpose of deepening personal insight rather than orienting a naive reader._

- **target_alignment: PARTIAL** — The tutor focuses on reader orientation and situational detail rather than directly honoring meaning/significance as the primary target; it's adjacent but nudges toward explanation rather than deepening the reflective insight itself.
- **constraint_compliance: PASS** — The tutor does not impose a thesis, claim-evidence structure, or argumentative template, and avoids rewriting or supplying content.
- **one_target_and_authorship: PASS** — One clear target (reader orientation) is maintained and the student retains full authorship over what to say next.

### Turn 1 (writing) · 68.57s · prompt 27597B
- Student: The night shift taught me that calm isn't the absence of fear. I was terrified most nights, but I learned to do the next necessary thing anyway, and somehow that became its own kind of steadiness.
- Tutor: This opening does real work fast — you've landed on something genuinely surprising: calm as action rather than the absence of fear. As you move into drafting the rest, it helps to ask yourself what a reader who hasn't worked a night shift would need in order to follow you into that insight. What is it about that specific job or situation that made 'doing the next necessary thing' feel different from simply enduring fear?
- element: **Hook / Opening Move** · target: Reader orientation — helping the student see what a naive reader needs next to follow the insight into the essay · focus: **writing** · cycle: continue · control: largely_independent
- postponed: ['explicit controlling insight / thesis function', 'organization of body']
