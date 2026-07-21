# Compass — Canonical Student Workspace Design (Phase 3)

> The heart of Compass. Everything else exists to create, support, or understand what happens here. Design only — no build. The instructional engine, decision model, and developmental method are unchanged; this maps a document-first experience onto the existing turn kinds (`writing`, `revise`, `answer`, `explain`) and durable polling.

## First principle
**The writing is the primary object; the conversation exists only to improve it.** The student writes and revises ONE continuously visible, continuously editable document. The coach lives at the margin, offering one focused invitation at a time and reacting to each revision. The student must never lose sight of the current draft, and never revise by re-typing into a chat box.

## The canonical cycle
Write → Compass coaches → **revise the document in place** → Compass responds to the revision → revise again. The document evolves; it is not re-created each turn. Chat replies (answer/explain) are a *side channel* for thinking, never the way revision happens.

---

## 1. Layout (desktop)
A document-dominant two-region canvas — NOT a 50/50 split, NOT chat-first.

- **Top bar (slim):** assignment title + current writing task (compact, one line each), and a quiet **revision progress** indicator ("Revision 1 of 2"). No dev tools, no score.
- **Document region (dominant, ~65–70% width, left/center):** the living draft on a paper surface — large serif body type, generous margins, live word count, autosave indicator. This is the same text object across the whole session; the student edits *here*, in place. A **primary action bar** anchors the bottom of the document: **"Send to coach"** (first pass) / **"Send revision"** (after edits).
- **Coach rail (~30–35%, right):** quiet secondary surface with three stacked zones:
  1. **Current invitation (pinned, the single accent element):** one developmental invitation tied to the current draft.
  2. **Reply affordance (small):** a compact input with `Answer` / `Explain` modes — for thinking aloud to the coach *without* changing the document.
  3. **History (recessed, collapsible):** prior invitations and the student's replies, muted so they never compete with the draft.

## 2. Visual hierarchy
Document is unmistakably dominant: largest type, brightest surface, most space. The coach rail is quieter and cooler. Within the rail, only the **current invitation** carries the terracotta accent; history is muted stone. Nothing visually competes with the draft. Motion is minimal: a new invitation fades in; a revision the coach is reacting to gets a brief highlight.

## 3. Primary controls
- The **editable document** (always focusable, always editable — even while the coach is thinking).
- **Send to coach / Send revision** button (bottom of document). First submission → `writing`; every later submission of the edited document → `revise`.
- **Revision progress** (reads the assignment's revision expectations from the saved configuration).

## 4. Secondary controls
- **Reply to coach** (`Answer` / `Explain`) in the rail → engine kinds `answer` / `explain`; used to respond to a question or explain a decision *without* a document submission.
- **"What changed since my last revision"** — highlights the diff in the document so the student sees their own movement.
- **"I'm stuck / show me more support"** — a gentle nudge that lets the student ask for more scaffolding (engine still decides how); never produces text for them.
- **Assignment details** expander; **collapse/expand** coach history.

## 5. Empty states
- **No writing yet:** document shows a calm placeholder ("Begin your draft here — write what you actually think."). Coach rail shows a single quiet line: *"Write something and I'll read it as a reader would. I won't write it for you."* No invitation appears until the first submission.
- **Coach thinking (durable polling):** rail shows an in-character indicator ("Reading your draft…"); the document stays fully editable so the student can keep writing while waiting.
- **After first revision, no coach reply yet:** current invitation remains visible (not cleared) until the new one arrives — the student is never left with an empty rail.

## 6. Error states (never destroy the draft)
- **Submission/engine failure:** the draft is preserved (local + autosave); the rail shows a non-destructive retry ("I couldn't read that just now — try again"). No content is lost, no partial coach message shown.
- **Anti-coauthoring request** (student asks the coach to write/fix/rewrite it): the coach declines in character and returns exactly one decision to the student; the document is never auto-filled or auto-edited.
- **Empty or unchanged submission:** the Send button is disabled with a hint ("Add or change something in your draft first") — this protects the meaning of the revise loop.
- **Connectivity loss:** autosave keeps the draft; a quiet banner notes unsynced changes; submissions queue and send on reconnect.

## 7. Mobile considerations
The document and coach cannot both be dominant on a small screen — so the **document is the default full-screen surface**. The coach's **current invitation** appears as an anchored, pull-up card / bottom sheet (dismissible); the reply modes and history live behind a single tab. The editable document is always one tap away and is never hidden behind the conversation. **Send revision** is a sticky bottom button. The "what changed" highlight works inline.

## 8. Mapping to the (frozen) engine — no engine change
- First document submission → `writing`; each subsequent submission of the edited document → `revise` (engine's previous-draft detection compares versions).
- Rail replies → `answer` / `explain`.
- Durable polling drives the coach's response; the document remains editable throughout.
- The document is a client-persistent, autosaved evolving object; each *submitted* version becomes a versioned turn server-side — consistent with the current architecture, requiring no engine or API change.

## 9. Future expansion points
- **Anchored margin notes:** invitations pinned to the specific span of the draft they refer to (highlight-on-hover).
- **Draft timeline / version scrubber:** step through revisions; feeds Revision Analytics (S9).
- **Span highlighting:** the coach visually points at the sentence/paragraph in question without editing it.
- **Long-document navigation:** section outline for multi-paragraph essays.
- **Accommodations:** adjustable type size, read-aloud, dyslexia-friendly font (support access, not lower expectations).
- **Teacher replay:** the same document+revision record powers the Teacher Dashboard and Revision Analytics.

---

## What must never appear
Scores/grades/rubric-as-verdict; Compass writing, rewriting, auto-editing, or auto-correcting the draft; engine internals or a Dev Panel; a chat stream that displaces or hides the document; any implication that revision is optional.

## Deliverable status
Phase 3 canonical Student Workspace — **for approval.** On approval: Phase 4 redesigns the Public Preview as a faithful miniature of this workspace (document-first, same cycle, shortened), then the remaining product (Teacher Home, authoring flow, Dashboard, Analytics) is designed around it.
