# Enhanced Instructional Review — Failed & Ambiguous Cases
Run: `2598c428-3a60-408b-9acd-313d319262f7`  ·  Engine state: UNCHANGED (baseline)
1 failed · 8 ambiguous, of 32 cases.

> Purpose: give the instructional architect enough verbatim evidence to independently judge whether the evaluator's criticism is justified. Each case carries the exact Compass text, the principle at stake, a classification (hard constraint violation / developmental concern / stylistic preference / reasonable pedagogical disagreement), a single stronger move, other acceptable moves, and a root-cause verdict.

=======================================================================
TC03 — No thesis
=======================================================================

### CASE SUMMARY

- **Test Case ID:** TC03
- **Instructional Object:** Thesis
- **Evaluation Result:** PARTIAL
- **Confidence (in the result):** medium
- **Primary weakness:** sentence-starter templates supply the thesis skeleton rather than eliciting it

### INTERACTION

**Assignment:** Argue whether homework should be limited.

**Student input:** Homework. Students get a lot of homework. Some people like it and some people don't. There are many opinions about homework.

**Compass response:** You've started by naming the topic — homework — and that's a real starting point. Here's a writing concept that will make the next step clear: a thesis is the one idea you want your reader to accept or understand, not just the subject you're writing about. Right now your draft tells us the topic but not your position on it. So try this: in one sentence, finish this thought — 'Homework should be limited because...' or 'Homework should NOT be limited because...' — whichever side you actually want to argue. What's your sentence?

### EVALUATOR ANALYSIS

**Weakness 1 — [reasonable pedagogical disagreement]**
1. Compass text: "try this: in one sentence, finish this thought — 'Homework should be limited because...' or 'Homework should NOT be limited because...' — whichever side you actually want to argue."
2. Why problematic: The two starters pre-package the exact syntactic structure of a thesis (claim + causal connector) and even pre-select the precise proposition words ('limited'). A student can produce a compliant, copyable thesis by filling in one blank without doing the cognitive work of discovering that a thesis needs a claim AND a reason. The structural and lexical scaffolding Compass is supposed to withhold has already been provided; only the 'because' clause remains for the student.
3. Instructional principle: anti-coauthoring boundary — Compass must not supply finished/copyable text or sentence shapes
4. Classification: **reasonable pedagogical disagreement**

### BETTER ALTERNATIVE

CURRENT
> "try this: in one sentence, finish this thought — 'Homework should be limited because...' or 'Homework should NOT be limited because...' — whichever side you actually want to argue. What's your sentence?"

RECOMMENDED
> "Instead of offering the fill-in starters, ask a reflective stance question: 'Before you write anything, tell me in plain words — do you think homework should be limited, kept the same, or expanded? And what's the main reason you believe that?' Then, after the student states a position, coach them to collapse their own words into one sentence rather than handing them the sentence frame."

Why stronger: This move forces the student to generate both the claim and the rationale from scratch, preserving the cognitive challenge that produces genuine learning. Compass still guides (by asking for a claim and a reason separately), but the syntactic shape of the thesis comes entirely from the student's own language — no fill-in-the-blank shortcut exists.

### ALTERNATIVE ACCEPTABLE MOVES

- **Option A — Stance-first question** — Asks the student to commit to a side in their own words before any sentence structure is introduced; keeps structural authorship fully with the student; naturally reveals whether the student understands what 'taking a position' means.
- **Option B — Conceptual contrast + student drafts** — Explain the difference between a topic sentence ('Homework is common in schools') and a thesis ('Homework should be limited / should not be limited') without supplying the exact wording; ask the student to write their own thesis sentence from scratch; this preserves the anti-coauthoring boundary while still teaching the concept explicitly.

_Multiple developmentally-reasonable paths?_ false — at this level, with a student who has produced only topic announcement and no discernible position, thesis formation is the only defensible primary target; pivoting to evidence, structure, or style before any stance exists would be developmentally premature.

### ARCHITECT REVIEW

**What should the system designer learn from this case?**

Root cause: poor calibration. The evaluator's 'partial' verdict is defensible but only mildly so. The sentence starters are a widely used scaffolding technique (Hillocks, Graff & Birkenstein) and many experienced writing teachers would consider them appropriate for grade 9 — they do reduce cognitive load without eliminating the student's authorial decision. What the evaluator correctly identified is a genuine tension between two legitimate pedagogical values: reducing friction (good for student confidence and forward momentum) versus preserving full authorial ownership of form (the explicit constraint). The system designer should learn: (1) the anti-coauthoring constraint needs more granular specification — does it prohibit sentence-frame scaffolds or only completed sentences? Sentence starters occupy a grey zone the current constraint language does not resolve; (2) the evaluator's 'partial' rather than 'fail' rating is appropriately calibrated — this is not a hard violation but a calibration question about how much structural pre-loading is too much; (3) Compass should be prompted to elicit the student's own language before offering any syntactic scaffold, not as a rule derived from first principles each turn but as an encoded sequence: stance → rationale → student drafts sentence → coach toward thesis shape.


=======================================================================
TC07 — Strong thesis that should not be over-taught
=======================================================================

### CASE SUMMARY

- **Test Case ID:** TC07
- **Instructional Object:** Thesis
- **Evaluation Result:** PARTIAL
- **Confidence (in the result):** high
- **Primary weakness:** inventing a scope problem on a strong, deliberate thesis

### INTERACTION

**Assignment:** Argue a position on remote work.

**Student input:** Remote work does not erode collaboration; it exposes how much of our old collaboration was proximity mistaken for teamwork. When presence is no longer automatic, teams must design connection deliberately—and the deliberate version is usually better.

**Compass response:** Your opening move is sharp — it reframes the common objection and commits immediately to a position. Before you draft the body, it's worth naming what you want the reader to accept by the end: what specifically does 'the deliberate version is usually better' mean for this essay — better in what ways, for whom, under what conditions? Holding that question in front of you as you draft will help you decide which evidence and arguments actually belong.

### EVALUATOR ANALYSIS

**Weakness 1 — [hard constraint violation]**
1. Compass text: "what specifically does 'the deliberate version is usually better' mean for this essay — better in what ways, for whom, under what conditions?"
2. Why problematic: The thesis is intentionally constructed with productive openness — the phrase 'usually better' is a claim that invites body development, not a deficiency. By interrogating its boundaries with three nested sub-questions, Compass frames a deliberate rhetorical choice as a gap needing repair, inventing a scope problem where the ground truth says none exists. This is precisely the forbidden behavior ('inventing a thesis problem') flagged in the case.
3. Instructional principle: restraint on strong writing — when a thesis is genuinely strong, the instructional obligation is to affirm and advance, not to subject it to diagnostic questioning that signals deficiency
4. Classification: **hard constraint violation**

**Weakness 2 — [developmental concern]**
1. Compass text: "Before you draft the body, it's worth naming what you want the reader to accept by the end"
2. Why problematic: The student has already named what they want the reader to accept — the thesis does exactly that. This framing implies the thesis is incomplete or under-specified, reinforcing the invented problem. It also subtly nudges the student to pre-commit to a narrower claim before they have explored their evidence, which can constrain body development unnecessarily.
3. Instructional principle: consolidation-before-advance — Compass should first consolidate what is genuinely working before directing attention to any forward-looking move
4. Classification: **developmental concern**

### BETTER ALTERNATIVE

CURRENT
> "Before you draft the body, it's worth naming what you want the reader to accept by the end: what specifically does 'the deliberate version is usually better' mean for this essay — better in what ways, for whom, under what conditions? Holding that question in front of you as you draft will help you decide which evidence and arguments actually belong."

RECOMMENDED
> "Consolidate the genuine success explicitly — name why the reframe structure (not X; it exposes Y) is powerful — then invite the student to describe the body of evidence they are considering, so the next turn can target the genuinely next developmental challenge rather than an invented one."

Why stronger: It honors the constraint to consolidate success, avoids fabricating a problem, and opens a diagnostic channel (what evidence are you thinking about?) that lets Compass identify a real next target rather than imposing one.

### ALTERNATIVE ACCEPTABLE MOVES

- **Option A — Affirm and advance to evidence selection** — Respects the strong thesis, consolidates the student's rhetorical success, and pivots immediately to the next genuine challenge (selecting and sequencing body evidence), which is where most college writers need help after a strong opening claim.
- **Option B — Affirm and raise genre/audience awareness** — Acknowledges the thesis is ready, then surfaces a productive forward question about audience skepticism (who is most likely to push back and where in the essay should you anticipate that?), which is a high-leverage college-level move that does not imply the thesis is deficient.

_Multiple developmentally-reasonable paths?_ false — given the ground truth (thesis is strong, expected move is light/consolidate or move forward), the range of defensible targets is narrow; nearly any next move that treats the thesis as needing work is unjustified, and the right next target is consolidation followed by body-level scaffolding.

### ARCHITECT REVIEW

**What should the system designer learn from this case?**

What should the system designer learn from this case? Root cause: poor calibration. Compass correctly identified the thesis as 'sharp' in its opening praise, then immediately undermined that judgment by treating the claim's intentional breadth as a scope deficiency. This is a calibration failure: the system's praise-then-probe pattern fires by default even when the probe step is contraindicated. The fix is not new instructional knowledge — Compass demonstrably knows what a strong thesis looks like — but a tighter calibration rule: when the active instructional element is Thesis AND the system's own opening evaluation is positive, the decision gate must require an affirmative justification for any interrogative follow-up before it is delivered. Without that gate, the system will routinely over-teach strong work by treating thoroughness (covering all possible angles of a claim) as a proxy for good instruction.


=======================================================================
TC18 — Effective introduction
=======================================================================

### CASE SUMMARY

- **Test Case ID:** TC18
- **Instructional Object:** Thesis
- **Evaluation Result:** PARTIAL
- **Confidence (in the result):** medium
- **Primary weakness:** mild problem-invention on an effective intro — asking the student to pre-explain a distinction the intro already establishes

### INTERACTION

**Assignment:** Argue a position on universal basic income.

**Student input:** Every automation debate eventually arrives at the same anxious question: what happens to people when the work runs out? Universal basic income is the boldest answer on offer—not a safety net but a floor. This essay argues that a floor, not a net, is what a post-automation economy actually requires.

**Compass response:** Your introduction does real work: it frames automation as the context, names UBI as the answer, and lands a thesis that draws a clear distinction between a 'floor' and a 'net.' That distinction is doing a lot of persuasive weight. Before you move into the body, what does your reader need to understand about that floor/net distinction in order to follow the argument you're about to make?

### EVALUATOR ANALYSIS

**Weakness 1 — [developmental concern]**
1. Compass text: "Before you move into the body, what does your reader need to understand about that floor/net distinction in order to follow the argument you're about to make?"
2. Why problematic: The intro already performs the floor/net distinction clearly and purposefully ('not a safety net but a floor'). By asking what the reader 'needs to understand' before the body, Compass implies a gap or deficiency that the intro has already closed, thereby manufacturing a readiness concern on writing the evaluator's ground truth marks as effective. This subtly signals to the student that something is incomplete when nothing is.
3. Instructional principle: restraint on strong writing / consolidation-before-advance — when an intro is working, the correct move is genuine affirmation followed by forward momentum, not a probing question that re-opens settled ground
4. Classification: **developmental concern**

### BETTER ALTERNATIVE

CURRENT
> "Before you move into the body, what does your reader need to understand about that floor/net distinction in order to follow the argument you're about to make?"

RECOMMENDED
> "Ask a forward-facing question that bridges the effective intro to the body's first obligation, e.g., 'That distinction is doing real work—what claim or evidence does your first body paragraph use to start making the case that a floor (rather than a net) is what a post-automation economy requires?'"

Why stronger: It consolidates the intro's success without implying incompleteness, preserves forward momentum consistent with the 'light / move forward' target, and redirects energy toward the next developmental challenge (building the body) rather than re-examining settled introductory work.

### ALTERNATIVE ACCEPTABLE MOVES

- **Option A — Affirm and pivot to body structure** — Explicitly names what the intro accomplishes, then asks the student to describe how the body will develop the floor/net argument—maintains momentum and shifts the instructional focus forward without re-opening the intro.
- **Option B — Affirm and invite the student to draft or describe the first body paragraph** — The cleanest 'light / move forward' execution: brief genuine recognition of what is working, then an open invitation to continue—least likely to be read as signaling a gap and most aligned with the expected target.

_Multiple developmentally-reasonable paths?_ true — both a pure 'move forward' pivot and a transitional bridge question that genuinely serves body development are defensible; the issue is that the chosen question points backward at the intro rather than forward at the body.

### ARCHITECT REVIEW

**What should the system designer learn from this case?**

What should the system designer learn from this case? Root cause: poor calibration. Compass correctly identified what the intro accomplishes and correctly resisted rewriting or supplying content, but then selected a question whose frame implied the intro left something unfinished. The evaluator's 'partial' judgment is largely justified, though 'mild' is the right severity qualifier—this is not a hard constraint violation. The calibration failure is that Compass has a tendency to generate a probing question even when the correct pedagogical move is brief consolidation plus a clean forward pivot. The system designer should add a decision rule: when the ground truth marks a piece of writing as effective for its purpose, Compass's consolidation step must be genuinely terminal for that element—the follow-up question must address the next stage of the draft, not probe the adequacy of the element just praised.


=======================================================================
TC21 — Unclear pronoun reference
=======================================================================

### CASE SUMMARY

- **Test Case ID:** TC21
- **Instructional Object:** Sentence
- **Evaluation Result:** FAIL
- **Confidence (in the result):** low
- **Primary weakness:** none — evaluator over-reached on the rewrite prohibition

### INTERACTION

**Assignment:** Explain a conflict between two characters.

**Student input:** When John talked to his father about his car, he told him that he had ruined it and that he would have to pay him back for it, which made him angry.

**Compass response:** Your sentence has a pronoun problem: 'he,' 'him,' and 'him' each appear more than once, and a reader can't tell which 'he' is John and which is his father. Pronoun reference means each pronoun must point clearly to one and only one person. Look at your sentence and ask yourself: at each moment you wrote 'he' or 'him,' which person do you actually mean? Try rewriting the sentence so a reader who knows nothing else can follow exactly who said what and who owes whom.

### EVALUATOR ANALYSIS

**Weakness 1 — [reasonable pedagogical disagreement]**
1. Compass text: "Try rewriting the sentence so a reader who knows nothing else can follow exactly who said what and who owes whom."
2. Why problematic: The evaluator claims this 'explicitly instructs the student to rewrite the sentence with name substitutions, which directs the student's revision choices.' However, the phrase 'Try rewriting the sentence' is a generic invitation to revise — it neither supplies wording, prescribes a specific strategy (name substitution is the evaluator's invention; Compass never mentions it), nor hands the student a finished product. Asking a student to revise their own sentence is a foundational scaffolding move, not a rewrite performed by the tutor.
3. Instructional principle: anti-coauthoring boundary
4. Classification: **reasonable pedagogical disagreement**

### BETTER ALTERNATIVE

CURRENT
> "Try rewriting the sentence so a reader who knows nothing else can follow exactly who said what and who owes whom."

RECOMMENDED
> "Replace the directive frame with a reflective question that surfaces the student's own repair strategy before committing to any approach: e.g., 'Before you revise, what are some different ways a writer might solve a pronoun-reference problem like this one?'"

Why stronger: Eliciting revision strategies first (name substitution, sentence splitting, restructuring the scene, changing speaker attribution) widens authorial agency and teaches the concept more explicitly before the student picks up their pen. The current move is not wrong, but this sequence would more clearly demonstrate teaching HOW writing works rather than just pointing at the problem and asking for a fix.

### ALTERNATIVE ACCEPTABLE MOVES

- **Option A — Guided self-diagnosis** — Ask the student to underline each pronoun and write the intended referent beside it before deciding how to revise. This keeps the student doing the analytical work and surfaces exactly where confusion lives, without prescribing any surface-level solution.
- **Option B — Strategy enumeration** — Ask the student to brainstorm two or three different techniques a writer could use to fix unclear pronoun reference in any sentence, then apply whichever they find most natural. This teaches a transferable principle and maximizes authorial choice.

_Multiple developmentally-reasonable paths?_ false — the pedagogical target is tightly constrained by the known issue (ambiguous pronoun reference) and the assignment genre; there is no credible competing primary target here, though the revision invitation could legitimately be executed in several ways.

### ARCHITECT REVIEW

**What should the system designer learn from this case?**

What the system designer should learn: this is an evaluator problem, specifically poor calibration of the anti-coauthoring rule. The evaluator conflated 'directing the student to revise their own sentence' with 'rewriting the sentence for the student' or 'supplying finished/copyable text.' Compass's response contains no tutor-authored prose the student could lift, no prescribed sentence shape, no name substitutions (the evaluator invented that characterization), and no finished thesis or argument. The non-negotiable constraint prohibits Compass from rewriting the student's work — asking a student to attempt a revision of their own sentence is the opposite of that. The evaluator's logic, if applied consistently, would prohibit any revision prompt whatsoever, making Compass unable to function as a writing tutor. The root cause is insufficient calibration of where the anti-coauthoring boundary actually sits: it bars tutor-generated replacement text, not student-directed revision tasks. The designer should sharpen the evaluator's definition of 'directs a rewrite' to require that the tutor either (a) produces substitute text or (b) so narrowly prescribes the surface form that only one acceptable output exists. A generic 'revise so readers can follow who does what' does neither.


=======================================================================
TC28 — Student successfully performs the requested act
=======================================================================

### CASE SUMMARY

- **Test Case ID:** TC28
- **Instructional Object:** Central Claim / Thesis / Thesis / Central Claim
- **Evaluation Result:** PARTIAL
- **Confidence (in the result):** medium
- **Primary weakness:** premature advance without explicit consolidation beat after student success

### INTERACTION

**Assignment:** Argue whether social media harms teen friendships.

**Student input:** Social media is both good and bad for friendships.

**Compass response:** You've identified the topic — social media and friendships — but a thesis needs to go one step further: it takes a position a reader could actually push back on. Right now, 'both good and bad' tells the reader the topic has two sides, but not what *you* are arguing. What is the one thing you most want your reader to accept or understand about whether social media harms teen friendships?

**Simulated student reply 1:** Social media mostly harms close teen friendships, because it replaces deep face-to-face time with shallow likes and comments that don't build real trust.

**Compass follow-up:** That's a real claim now — it takes a position a reader can push back on. You've also begun to hint at your reasoning (shallow interaction doesn't build trust). Before you draft further, look at the two parts of what you wrote: the position itself ('mostly harms close friendships') and the reason you gave ('replaces deep time with shallow likes'). Which of those belongs in the thesis, and which is the first supporting reason that belongs in the body? Deciding that will help you write a tight thesis sentence that does exactly one job: tell the reader the position the whole essay will defend.

### EVALUATOR ANALYSIS

**Weakness 1 — [reasonable pedagogical disagreement]**
1. Compass text: "Before you draft further, look at the two parts of what you wrote: the position itself ('mostly harms close friendships') and the reason you gave ('replaces deep time with shallow likes'). Which of those belongs in the thesis, and which is the first supporting reason that belongs in the body? Deciding that will help you write a tight thesis sentence that does exactly one job: tell the reader the position the whole essay will defend."
2. Why problematic: Compass opens with a brief acknowledgment ('That's a real claim now') but immediately pivots to a new analytical task — differentiating thesis from supporting reason — without pausing to let the student's success land. The 'consolidate genuine success before advancing' constraint requires more than a one-line nod; it expects the tutor to affirm what the student has genuinely achieved, name the skill demonstrated, and signal readiness before introducing the next demand. Here the praise occupies roughly one sentence and the new structural question occupies three, making the turn feel primarily like an advance rather than a consolidation-then-advance sequence.
3. Instructional principle: consolidation-before-advance
4. Classification: **reasonable pedagogical disagreement**

### BETTER ALTERNATIVE

CURRENT
> "That's a real claim now — it takes a position a reader can push back on. You've also begun to hint at your reasoning (shallow interaction doesn't build trust). Before you draft further, look at the two parts of what you wrote: the position itself ('mostly harms close friendships') and the reason you gave ('replaces deep time with shallow likes'). Which of those belongs in the thesis, and which is the first supporting reason that belongs in the body? Deciding that will help you write a tight thesis sentence that does exactly one job: tell the reader the position the whole essay will defend."

RECOMMENDED
> "Spend more of Turn 2 consolidating the success before advancing: name the specific craft move the student made (e.g., that they identified a debatable claim and a mechanism in a single sentence), ask the student to articulate in their own words what makes their new claim arguable — to internalize the concept — and only after that reflection introduce the thesis-vs.-body distinction as the next step. This keeps the advance but earns it through consolidation."

Why stronger: Explicit consolidation builds the student's metacognitive awareness of what a successful argumentative claim looks like, making the skill transferable rather than one-time. It also respects the documented developmental profile by ensuring the student owns the thesis concept before being asked to refine it structurally. The advance itself (thesis vs. body) is appropriate; it simply needs a broader consolidation frame around it.

### ALTERNATIVE ACCEPTABLE MOVES

- **Option A — Reflect-and-name consolidation** — Ask the student to articulate, in their own words, what makes their claim arguable ('Why could a reader push back on this?'). This consolidates the thesis skill metacognitively and confirms mastery before any advance, satisfying the constraint fully while keeping authorship entirely with the student.
- **Option B — Confirm-then-defer advance** — Celebrate the success explicitly, affirm the specific craft achievement (debatable position + embedded reasoning), and close the turn there — deferring the thesis-vs.-body distinction to Turn 3. This maximizes consolidation time and avoids any risk of the student feeling rushed past their achievement.

_Multiple developmentally-reasonable paths?_ true — both staying on thesis consolidation and gently introducing thesis-vs.-body structure are developmentally defensible for a grade-10 student who has just produced a well-formed argumentative claim; the question is sequencing and pacing, not target choice.

### ARCHITECT REVIEW

**What should the system designer learn from this case?**

The evaluator's 'partial' judgment is defensible but slightly over-strict. The root cause is poor calibration: the evaluator applies the consolidation-before-advance rule as if any advance in the same turn after a success constitutes a violation, when in fact Compass does acknowledge the success and the advance it introduces is closely tied to the same thesis target (it refines what a thesis does, not a wholly new skill). A better-calibrated rubric would distinguish between a thin acknowledgment followed by an unrelated demand (clear violation) and a thin acknowledgment followed by a directly related structural refinement (reasonable pedagogical disagreement). The system designer should learn to build evaluator rubrics that capture the weight and nature of the consolidation beat, not just its presence or absence, and should flag cases like this as 'consolidation underweight' rather than 'consolidation missing,' which is a meaningfully different severity level.


=======================================================================
TC29 — Student needing the same scaffold repeatedly
=======================================================================

### CASE SUMMARY

- **Test Case ID:** TC29
- **Instructional Object:** Thesis
- **Evaluation Result:** PARTIAL
- **Confidence (in the result):** medium
- **Primary weakness:** sentence-starter template edges toward supplying copyable structural scaffold

### INTERACTION

**Assignment:** Argue whether students should choose their own books.

**Student input:** Books are good to read. Reading helps you learn things.

**Compass response:** You're starting to think about reading — that's a useful place to begin. The assignment asks you to argue one side: should students choose their own books, or not? A thesis gives your reader one clear position to follow. What do you think — should students choose their own books, or not? Try writing one sentence that says exactly what you believe.

**Simulated student reply 1:** I like reading books about dragons and space.

**Compass follow-up:** Your assignment asks you to argue whether students should get to pick their own books — not just any books, but whether the choice belongs to them. A thesis for this essay needs to answer that question directly: should students choose their own books, yes or no? Try writing one sentence that gives your answer to that question.

**Simulated student reply 2:** Reading is fun and my favorite books are long ones.

**Compass follow-up:** The assignment asks you to argue whether students should choose their own books — yes or no. Try writing one sentence that gives your answer to that question. You can start with 'Students should...' or 'Students should not...' and see where it takes you.

### EVALUATOR ANALYSIS

**Weakness 1 — [reasonable pedagogical disagreement]**
1. Compass text: "You can start with 'Students should...' or 'Students should not...' and see where it takes you."
2. Why problematic: Providing explicit sentence-starter templates reduces the student's generative load by handing them a ready-made syntactic and argumentative frame. The student need only fill in a few words to produce a thesis, meaning the structural authorship is partly Compass's rather than theirs. This is borderline but real: the two starters also implicitly narrow the thesis to a binary framing, removing the possibility of a nuanced position the student might discover independently.
3. Instructional principle: anti-coauthoring boundary — Compass must not supply finished or copyable text, sentence shapes, or structural frames that effectively draft the work for the student
4. Classification: **reasonable pedagogical disagreement**

### BETTER ALTERNATIVE

CURRENT
> "You can start with 'Students should...' or 'Students should not...' and see where it takes you."

RECOMMENDED
> "Ask a narrowing question instead: 'If a teacher told you tomorrow that you had no choice in what you read this year, how would you feel — and do you think that feeling is right or wrong?' This surfaces the student's actual belief without supplying syntactic scaffolding."

Why stronger: A reflective question activates the student's genuine opinion (the root problem — they are avoiding taking a position) and requires them to generate both the content and the form of their response. It does not gift a sentence frame, preserving fuller authorship while still scaffolding toward position-taking.

### ALTERNATIVE ACCEPTABLE MOVES

- **Option A — Opinion-surfacing question** — Asks the student to locate a real personal belief first; once they articulate it conversationally, translating it into a thesis sentence is their own act of authorship. Avoids any template risk entirely.
- **Option B — Acknowledge avoidance explicitly** — Name the pattern directly ('I notice you keep telling me what you enjoy rather than what you think should happen — what's making it hard to pick a side?'). This metacognitive move addresses the root avoidance behavior, which is the documented known issue, and may unlock the logjam more efficiently than another structural prompt.

_Multiple developmentally-reasonable paths?_ false — given the documented known issue (repeatedly avoids taking a position) and only three turns elapsed, persisting on thesis is the only defensible primary target; the only question is how to scaffold it.

### ARCHITECT REVIEW

**What should the system designer learn from this case?**

What should the system designer learn? The evaluator's 'partial' verdict is defensible but slightly over-weighted against a mild scaffold. Sentence starters like 'Students should...' are a widely accepted low-scaffold technique for stuck writers at grade 8; they are not equivalent to writing the thesis. However, the evaluator is right that repeated use at escalating specificity (Turn 3 adds starters after two failed re-prompts) should be flagged. The root cause is poor calibration: the evaluator applied the anti-coauthoring constraint without sufficiently distinguishing between 'supplies the argument' (hard violation) and 'supplies a syntactic frame' (softer, context-dependent concern). The system designer should clarify in the rubric that sentence-starter scaffolds are a 'caution zone' rather than a categorical violation, and that the relevant test is whether the student still generates the position/content — not whether the surface syntax was suggested.


=======================================================================
TC30 — Returning student showing increased independent control
=======================================================================

### CASE SUMMARY

- **Test Case ID:** TC30
- **Instructional Object:** Purpose
- **Evaluation Result:** PARTIAL
- **Confidence (in the result):** medium
- **Primary weakness:** profile-ignoring target selection — pivoting to audience awareness over the documented growth edge of evidence/explanation

### INTERACTION

**Assignment:** Argue whether AI should be allowed for homework.

**Student input:** AI should be allowed for homework only as a tutor, not a ghostwriter, because a tool that explains builds skill while a tool that answers replaces it — and the difference is who does the thinking.

**Compass response:** You've written a thesis that already draws a real line — AI as tutor vs. ghostwriter — and gives a reason for it. That's a strong start. Now, to set up your argument: who is the reader you're trying to convince, and what do you think they currently believe about AI and homework? Knowing that will help you see what your argument needs to do next.

### EVALUATOR ANALYSIS

**Weakness 1 — [developmental concern]**
1. Compass text: "Now, to set up your argument: who is the reader you're trying to convince, and what do you think they currently believe about AI and homework? Knowing that will help you see what your argument needs to do next."
2. Why problematic: The student's documented developmental profile identifies evidence/explanation as the growth edge, not audience awareness. By redirecting to audience analysis at Turn 1, Compass delays engagement with the known high-leverage skill gap. Audience awareness is a legitimate rhetorical concept, but it is not what this student's profile says they need next, and choosing it consumes the turn's single instructional slot on a lower-priority target.
3. Instructional principle: profile-aware target selection
4. Classification: **developmental concern**

### BETTER ALTERNATIVE

CURRENT
> "Now, to set up your argument: who is the reader you're trying to convince, and what do you think they currently believe about AI and homework? Knowing that will help you see what your argument needs to do next."

RECOMMENDED
> "Redirect the student toward evidence/explanation: e.g., 'Your thesis draws a clear line between explaining and answering — now think about what a skeptical reader would need to see to believe that line is real. What kind of evidence or reasoning would actually demonstrate that a tool that explains builds skill while one that answers replaces it? What have you seen, read, or experienced that could test that claim?'"

Why stronger: This move honors the thesis without re-teaching it, keeps authorship with the student (no content is supplied), and directly targets the documented growth edge — moving the student toward developing and explaining evidence rather than pausing on audience framing that the student may be ready to handle implicitly.

### ALTERNATIVE ACCEPTABLE MOVES

- **Option A — Evidence/Explanation Prompt** — Directly addresses the documented growth edge; keeps the instructional arc aligned with the developmental profile; pushes the student to substantiate the thesis claim they've already mastered constructing.
- **Option B — Audience Awareness (current move)** — Rhetorically coherent — knowing the audience genuinely shapes what evidence will be persuasive; could indirectly scaffold evidence selection; is a defensible Turn 1 move when profile data is not weighted heavily, particularly if the instructor believes audience framing is prerequisite to purposeful evidence choice.

_Multiple developmentally-reasonable paths?_ true — audience awareness and evidence/explanation are both defensible Turn 1 targets, but only evidence/explanation is aligned with this student's documented developmental profile, making it the clearly preferred choice given Compass's scaffolding mandate.

### ARCHITECT REVIEW

**What should the system designer learn from this case?**

What should the system designer learn from this case? Root cause: poor calibration. Compass correctly reads the thesis as strong, correctly avoids re-teaching it, and correctly limits itself to one target — so the constraint engine is functioning. The failure is that the target-selection module did not weight the documented developmental profile heavily enough when choosing between two otherwise legitimate rhetorical moves. Audience awareness is not wrong in the abstract; it is wrong here because the profile explicitly flags evidence/explanation as the growth edge. The system designer should ensure that when a student profile contains an explicit growth-edge annotation, that annotation functions as a strong prior that overrides generic next-step heuristics (like 'audience framing often comes early in argumentative planning'). The evaluator's 'partial' verdict is justified, though 'meaningful instructional mistarget' is a fair but slightly strong characterization given that audience awareness can plausibly feed into evidence selection — hence medium rather than high confidence.


=======================================================================
TC31 — Ambiguous: both-sides could be a legitimate nuanced thesis
=======================================================================

### CASE SUMMARY

- **Test Case ID:** TC31
- **Instructional Object:** Central Claim / Thesis
- **Evaluation Result:** PARTIAL
- **Confidence (in the result):** medium
- **Primary weakness:** consolidation-before-advance skipped: Compass probed for a 'governing claim' instead of first affirming that the thesis may already be complete

### INTERACTION

**Assignment:** Evaluate whether remote learning is effective.

**Student input:** Remote learning is effective for motivated, self-regulating students and ineffective for those who depend on external structure; its value is therefore not a property of the medium but of the match between medium and learner.

**Compass response:** You've written a genuinely arguable claim — one that takes a position a reader could push back on. Notice that your thesis does two things at once: it limits who remote learning works for, and it makes a broader point about the medium-learner match. That broader point is doing real intellectual work. Before drafting further, can you name — in your own words — what you want your reader to walk away believing? That will help you decide which of those two moves is the governing one.

### EVALUATOR ANALYSIS

**Weakness 1 — [reasonable pedagogical disagreement]**
1. Compass text: "Before drafting further, can you name — in your own words — what you want your reader to walk away believing? That will help you decide which of those two moves is the governing one."
2. Why problematic: This question presupposes that the two moves in the thesis are in tension and that one must be selected as dominant, implying the thesis is structurally incomplete. The student's thesis is, in fact, logically coherent: the limiting condition (motivated/self-regulating vs. structure-dependent) is the evidence that supports the broader medium-learner-match claim. Asking the student to choose between them risks causing unnecessary self-doubt about a defensible thesis, and it nudges the student toward resolving a problem that may not exist — the definition of over-teaching on strong writing.
3. Instructional principle: consolidation-before-advance; restraint on strong writing
4. Classification: **reasonable pedagogical disagreement**

### BETTER ALTERNATIVE

CURRENT
> "Before drafting further, can you name — in your own words — what you want your reader to walk away believing? That will help you decide which of those two moves is the governing one."

RECOMMENDED
> "Affirm explicitly that the thesis already does the two-part structural work cleanly, then ask a light forward-looking question such as: 'Given that your thesis makes a claim about medium-learner match, what kinds of evidence would most directly test that claim as you draft?'"

Why stronger: This move consolidates genuine success (the nuanced thesis is strong) before inviting the student to think about what comes next, which honors the instructional principle of consolidation-before-advance and avoids implying the thesis needs structural repair. It also keeps the student moving forward rather than circling back to re-examine something that is working.

### ALTERNATIVE ACCEPTABLE MOVES

- **Option A — Pure consolidation** — Explicitly validates the thesis as a complete, arguable claim, reinforcing the student's understanding of what a nuanced position looks like without introducing any destabilizing doubt. Appropriate when the known issue is 'nuanced position may be adequate.'
- **Option B — Consolidate then bridge to evidence** — Affirms the thesis strength and immediately pivots to the next developmental challenge (what evidence supports the medium-learner-match claim), maintaining momentum while teaching something genuinely useful rather than reopening a resolved structural question.

_Multiple developmentally-reasonable paths?_ true — both pure consolidation and a light pivot to evidence planning are developmentally defensible here, since the thesis is strong and the student is ready to draft.

### ARCHITECT REVIEW

**What should the system designer learn from this case?**

The root cause is poor calibration. Compass correctly identified that the thesis was 'genuinely arguable' and avoided all hard constraint violations, but it failed to calibrate the degree of intervention to the strength of the student's work. The known ground truth ('nuanced position may be adequate, not evasive') required the system to default to restraint when the thesis was strong, yet the response still applied a standard 'resolve the tension' probe as though the thesis were unfinished. The evaluator's 'partial' judgment is largely justified: the instructional move was not wrong in kind (it stayed on one target, preserved authorship, asked rather than told) but was miscalibrated in degree — it treated a healthy thesis as a problem. System designers should learn that calibration logic must include a 'do less' branch triggered when incoming work meets or exceeds the threshold for the target skill; without that branch, the engine systematically over-probes strong writing, which is itself listed as a behavior Compass must avoid.


=======================================================================
TC32 — Ambiguous: reflective piece not needing a thesis
=======================================================================

### CASE SUMMARY

- **Test Case ID:** TC32
- **Instructional Object:** Hook / Opening Move
- **Evaluation Result:** PARTIAL
- **Confidence (in the result):** medium
- **Primary weakness:** reader-orientation framing nudges toward explanatory/argumentative elaboration rather than deepening reflective meaning

### INTERACTION

**Assignment:** Reflect on something a job taught you.

**Student input:** The night shift taught me that calm isn't the absence of fear. I was terrified most nights, but I learned to do the next necessary thing anyway, and somehow that became its own kind of steadiness.

**Compass response:** This opening does real work fast — you've landed on something genuinely surprising: calm as action rather than the absence of fear. As you move into drafting the rest, it helps to ask yourself what a reader who hasn't worked a night shift would need in order to follow you into that insight. What is it about that specific job or situation that made 'doing the next necessary thing' feel different from simply enduring fear?

### EVALUATOR ANALYSIS

**Weakness 1 — [reasonable pedagogical disagreement]**
1. Compass text: "it helps to ask yourself what a reader who hasn't worked a night shift would need in order to follow you into that insight"
2. Why problematic: This framing subtly imports an argumentative/expository obligation — satisfying a skeptical or uninitiated external reader — into what is a reflective genre. Reflection's primary job is to deepen the writer's own understanding of significance, not to build a bridge for a naive audience. The question quietly reorients the writer away from inward excavation and toward outward justification, which is the first step toward the claim-evidence pattern Compass is supposed to avoid imposing.
3. Instructional principle: genre honoring — reflective writing prioritizes meaning-making and significance over reader persuasion or orientation
4. Classification: **reasonable pedagogical disagreement**

**Weakness 2 — [reasonable pedagogical disagreement]**
1. Compass text: "What is it about that specific job or situation that made 'doing the next necessary thing' feel different from simply enduring fear?"
2. Why problematic: This follow-up question is well-intentioned and could serve reflection, but framed after the reader-orientation setup it functions more as a prompt to explain the distinction to an audience than to discover what that distinction meant to the writer. The student's opening already contains a rich insight; the move that would honor reflective purpose would invite the student to explore what that insight reveals about themselves or their experience, not to clarify it for outsiders.
3. Instructional principle: genre honoring / scaffold from developmental profile — the student has already demonstrated the insight; deepening rather than explaining is the appropriate next move
4. Classification: **reasonable pedagogical disagreement**

### BETTER ALTERNATIVE

CURRENT
> "it helps to ask yourself what a reader who hasn't worked a night shift would need in order to follow you into that insight. What is it about that specific job or situation that made 'doing the next necessary thing' feel different from simply enduring fear?"

RECOMMENDED
> "Invite the student to linger inside the insight rather than explain it outward: e.g., 'You've named something precise — calm as action. As you draft further, it might be worth sitting with: what did you notice in yourself when that steadiness arrived? What surprised you most about what the night shift revealed about how you work, or who you are?'"

Why stronger: This move honors the reflective genre by directing attention inward — toward significance and self-discovery — rather than outward toward audience accessibility. It consolidates the strong insight already present and scaffolds the student toward the deeper meaning-making that reflection, as a form, actually demands.

### ALTERNATIVE ACCEPTABLE MOVES

- **Option A — Significance excavation** — Ask the student what surprised them most about the insight ('calm as action') and what it changed about how they understand themselves. Keeps focus purely on personal meaning-making, honors reflective purpose, avoids any explanatory or argumentative pressure.
- **Option B — Memory/Scene anchoring** — Ask the student to recall the single moment or night when the steadiness first registered as real. Scene-based prompting generates concrete material that reflective essays need while keeping the writer's own experience — not a reader's comprehension — at the center.

_Multiple developmentally-reasonable paths?_ true — reader orientation, significance deepening, and scene anchoring are all defensible next moves for this piece; the case is genuinely ambiguous because helping a reader 'follow' the insight can overlap with helping the writer understand what they are saying, and the evaluator's preference for meaning/significance is legitimate but not the only defensible choice.

### ARCHITECT REVIEW

**What should the system designer learn from this case?**

Root cause: poor calibration (evaluator side) combined with unavoidable pedagogical ambiguity. Compass's move is not a hard constraint violation — it avoids thesis-forcing, argumentative structure, and coauthoring — and reader orientation is a legitimate scaffold in many reflective genres. The evaluator correctly identifies that meaning/significance is the expected primary target and that the reader-framing subtly tilts toward explanation, but classifying this as 'partial' rather than 'pass with note' may be too strict given the genuine overlap between 'helping a naive reader follow' and 'helping the writer articulate what the experience meant.' The system designer should learn: (1) evaluator rubrics for reflective genre need a clearer threshold distinguishing reader-accessibility moves (which can serve reflection) from full argumentative-structure imposition (which violates it); (2) the evaluator's confidence in a 'partial' verdict should be gated on whether the move meaningfully redirected the student away from reflective depth, not merely whether the framing language could theoretically do so.

