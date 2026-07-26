# Compass Knowledge Base v1.0 — Release Notes

**Tag:** `compass-kb-v1.0`  ·  **Date:** 2026-07-25  ·  **Status:** Sprint 3 complete & accepted

## What this release contains
The first fully-enriched Compass instructional-object knowledge base:
- **35 / 35 instructional objects enriched** from the canonical Writing Elements Chart (0 base remaining).
- Canonical fields verbatim; deeper Compass fields conservatively derived; per-field `field_provenance`.
- Frozen Milestone M1–M14 engine, prompts, evaluator, architecture, and retrieval network **unchanged**.

## Verification
- 66-case regression (frozen `exhaustive` path): **57 pass / 7 partial / 0 fail / 2 error (86.4%)** vs baseline **58/8/0/0 (87.9%)**.
- Zero engine regressions; zero hard failures; 6 baseline partials improved. The 2 errors are evaluator tooling crashes. Accepted as non-regressive and beneficial.

## Archived record (this folder)
- `CURRENT_STATE.md` — canonical implementation index at release.
- `INSTRUCTIONAL_OBJECT_SPECIFICATION.md` — permanent schema reference.
- `SPRINT3_CANONICAL_ENRICHMENT_REPORT.md` — per-object enrichment validation.
- `SPRINT3_REGRESSION_REPORT.md` — 66-case regression + classification.
- `SPRINT3_SUMMARY.md` — Sprint 3 closure summary.

## Source of truth
Live files remain at the repository root / `backend/` / `test_reports/`; this folder is a frozen snapshot for the v1.0 record.

> **Pushing the tag to GitHub:** repository tags/commits are pushed via the platform's **"Save to GitHub"** feature. A local annotated tag `compass-kb-v1.0` has been created as a marker; use Save to GitHub to publish the commit and tag to the remote.
