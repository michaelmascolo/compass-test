# Sprint 1 — Testing & Refinement Log

Purpose: capture observations from real testing of the Question Loop so Sprint 2 is
driven by observed learner behavior, not additional theoretical design.
Rule: no new feature unless it solves a problem actually observed here.

## Instruments available for testing
- **Developer Mode** (hidden): toggle with `Ctrl/Cmd+Shift+D`, or open `?represent&dev`.
  Shows the Developmental Control Engine state (Current Loop, Dev. Operation, Target
  Demand, Scaffold Level, Instruction Type, Reason, Next-if-Successful/Unsuccessful,
  Requires Reconstruction). Never visible to students.
- **Developer Notes** (private, per session): editable in the Developer Mode panel.
- **Development Session record**: `GET /api/assignment/sessions/{id}/record?format=json|markdown`
  (also the JSON/MD buttons in the Developer panel). A complete research case:
  assignment, AI analysis (explicit/inferred demands + important distinctions + ambiguities),
  student (interpretation + every response + final restatement), developmental history
  (per scaffold: target, operation, level, performed?, reason, final status), final
  Question Map, and metadata (length, #scaffolds, #Level-3, "I don't know" occurred,
  restart occurred).

## Generalization sweep — analyze_assignment across the matrix (2026-06)
Ran the analysis stage on 8 assignments spanning Grade 4 → Graduate and Literature,
History, Biology, Chemistry, Psychology(reflective), Business, plus assignment types
short-answer / creative / argument / experiment-design / lab report / reflective /
synthesis / analysis.

Result: robust. 5–6 demands each; explicit/inferred split behaves sensibly (History &
Business correctly skew INFERRED because they demand argumentative structure that is not
literally stated); operation vocabulary stays varied and apt (Define, Explain, Compare,
Differentiate, Analyze, Evaluate, Exemplify, Relate); every case produced useful
important_distinctions and ambiguities.

Highlights of quality:
- Grade 4 ("draw + 2 sentences"): stayed simple; surfaced "describing the animal vs.
  explaining WHY you like it — sentences must give reasons, not just facts." Age-apt.
- History ("explain causes + evaluate most important"): surfaced "explaining a cause vs.
  evaluating its importance — description is not argument" and proximate-vs-underlying
  cause distinction; marked "define criteria for 'importance'" as an inferred demand.

## Observations / candidate issues (for Sprint 2 consideration — DO NOT build yet)
1. **Operation mislabel on pure constraints.** For "write two sentences", the analyzer
   tagged a length/format constraint with operation `Define`. Format/length constraints
   are not developmental operations. Sprint 2 candidate: a `constraint` demand kind that
   is tracked but not scaffolded as an operation.
2. **Verify young-learner scaffold register.** Analysis is age-appropriate; still need to
   run full multi-turn Grade-4 sessions to confirm scaffold LANGUAGE (not just demands)
   stays simple at levels 2–3.
3. **"I don't know" handling confirmed correct** on the mindset assignment: for a
   non-derivable demand it escalated to Level 3 direct teaching + mandatory own-words
   reconstruction, and never wrote the answer. Re-test across disciplines.
4. **Anti-trap** (≥3 failed attempts at Level 3 → mark demand 'developing' and advance)
   prevents dead-ends; watch whether it ever advances too early.

## Still to test (recommend doing interactively with real learners)
- Full multi-turn sessions for each of the 5 required mindset learner variants + the
  discipline matrix, watching whether the Question Loop consistently yields a MORE
  ADEQUATE representation (the real success criterion — not whether the AI is "right").
- Edit/restart mid-session; resume-after-refresh; long assignments; vague/1-line
  assignments; assignments with no clear operation.

_Log started 2026-06. Append findings here as sessions are reviewed._
