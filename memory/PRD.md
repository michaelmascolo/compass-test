# PRD — Developmental Writing Studio (Milestone 1)

## Original Problem Statement
Build Milestone 1 ONLY of an AI writing app that develops students as writers through scaffolded conversation (never editing, grading, or writing for them). Validate the loop: Teacher defines purpose → Student submits writing → AI evaluates organization relative to purpose → AI gives ONE focused developmental invitation → student responds/revises → AI updates internal developmental theory → AI generates next invitation.

## Architecture
- **Backend** (FastAPI + MongoDB): `/api/sessions` (create), `/api/sessions/{id}` (get), `/api/sessions/{id}/interact` (run engine). Developmental engine uses Claude **claude-sonnet-4-6** via emergentintegrations (EMERGENT_LLM_KEY), returns structured JSON: one student-facing invitation + a fully updated internal `DevelopmentalState`. State is UPDATED (merged), not appended, each turn. Sessions + turns + dev_state persisted in `sessions` collection.
- **Frontend** (React): 3 screens on a single continuous page. `App.js` state machine (setup → workspace) with localStorage session persistence (`dws_session_id`). Academic/editorial theme (Cormorant Garamond + IBM Plex Sans/Mono, cream/ink/terracotta).

## Screens Implemented (2026-07-17)
1. **Teacher Setup** — Assignment, Pedagogical Purpose, Current Writing Task, Optional Teacher Notes, Begin Session.
2. **Student Workspace** — assignment/task header, large writing canvas + Continue/Send revised draft, continuous conversation thread with answer/explain reply modes. No page transitions.
3. **Hidden Development Panel** — collapsible dark "terminal" drawer showing purpose, developmental theory, primary tension, alternative interpretations, selected scaffold + rationale, candidate scaffolds, developmental movement, uncertainties.

## Verified
- Multi-turn loop works: dev_state visibly evolves (developmental_movement ≠ initial), invitations are single-focus, never rewrite student work, never list errors. Persistence across reload confirmed. Testing agent: backend 6/6, frontend critical flows 100%.

## Backlog / Next Actions (deferred — out of Milestone 1 scope by instruction)
- P2 polish: return 201 from create; disable writing area during loading; shift main pane when panel opens; retry on transient LLM 5xx; word cap on submissions; toast on expired session.
- Future milestones (NOT to build now): multiple tasks/sessions list, teacher review of student progress, export transcript.
