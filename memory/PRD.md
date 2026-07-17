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

## Milestone — Developmental Guide Engine + Canonical Writing Model (2026-07-17)
- Reasoning engine is now domain-independent; domain knowledge lives in `backend/canonical_writing_model.json` (13 domains) loaded as DATA. Engine selects currently-relevant domains (no forced sequence) via the inside-outside coordination rule.
- Working theory (component C) persisted with `theory_history` snapshots (previous versions preserved, never overwritten), per-interaction candidate invitations (2-3, one selected), telos (A), participation/interaction records (B), teacher_edits.
- `/api/sessions/{id}/interact` converted to **SSE streaming** (heartbeats + terminal `event: done`) to stay under Cloudflare's ~60s edge cap; prompts slimmed + BREVITY rules → ~20-40s/turn. PATCH `/telos` lets the teacher revise the telos.
- Verified: testing agent iteration_4 — backend 8/8, frontend 100%. No stages/scores, AI never rewrites, theory evolves each turn.

## Multi-turn performance fix — two-stage domain selection (2026-07-17)
- Full 13-domain model no longer sent per turn. STAGE A: a compact index (name + 1-sentence function + relationships) drives an LLM selection of 1-3 relevant domains; STAGE B: only those domains' FULL records are sent to the reasoner via `get_relevant_domain_data()` (single source of truth, no code duplication). Prompt now includes telos + compact theory + interaction summary (no full transcript) + previous draft when comparing.
- Added one retry (~3s) on transient/unreadable LLM failures for both stages; no duplicate student turn / theory snapshot on retry.
- Verified (iteration_5): 4-turn session all HTTP 200, ~20-40s/turn, reasoner prompt ~4.6-7.8KB, domains shift with the writing, theory_history v1..v4 preserved, revisions recognized, no stages/scores, AI never rewrites.

## Backlog / Next (deferred)
- P2: return 201 from create; offset dev panel at ~1920px; expose teacher_notes in telos editor.
- NEXT MILESTONE (await review): populate real domain field data (Openings etc.) — NOT started.
