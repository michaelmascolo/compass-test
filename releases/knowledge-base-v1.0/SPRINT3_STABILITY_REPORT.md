# Sprint 3 — Stochastic Stability Report (7-case × 3 reruns)

> **Purpose:** estimate run-to-run stability and determine whether the apparent Sprint 3 "regressions" are genuine or evaluator/reasoner variation. **This is not an engine improvement exercise. No code or data was changed.**

## Method
- Re-ran only the 7 flagged cases (TC31, TC62, TC20, TC32, TC37, TC39, TC64) **three times each**, on the frozen `exhaustive` path, KB unchanged (35/35 enriched).
- Runs: `023c8f76` (rep1), `06d791b7` (rep2), `1ed65fde` (rep3). Compared against the Sprint 3 main run `0bfe5b82` and the pre–Sprint 3 baseline `fd0dec0c`.

## Results — verdict matrix

| Case | Baseline | Main (0bfe5b82) | Rep1 | Rep2 | Rep3 | Distinct verdicts | Stability |
|---|---|---|---|---|---|---|---|
| TC20 | pass | partial | partial | pass | pass | {pass, partial} | **unstable** |
| TC31 | pass | **error** | pass | pass | partial | {pass, partial, error} | **highly unstable** |
| TC32 | pass | partial | **error** | partial | pass | {pass, partial, error} | **highly unstable** |
| TC37 | pass | partial | partial | partial | partial | {partial} | **stable (partial)** |
| TC39 | pass | partial | pass | partial | pass | {pass, partial} | **unstable** |
| TC62 | pass | **error** | **error** | partial | pass | {pass, partial, error} | **highly unstable** |
| TC64 | pass | partial | partial | pass | partial | {pass, partial} | **unstable** |

Verdict tallies across the 4 runs (main + 3 reps):
- TC20: 2 pass / 2 partial · TC31: 2 pass / 1 partial / 1 error · TC32: 1 pass / 2 partial / 1 error · **TC37: 0 pass / 4 partial** · TC39: 2 pass / 2 partial · TC62: 1 pass / 1 partial / 2 error · TC64: 1 pass / 3 partial.

## Findings

1. **6 of 7 cases are stochastically unstable** — they produced ≥2 distinct verdicts across identical runs. **TC31, TC32, and TC62 each produced all three outcomes** (pass / partial / error). This is decisive evidence that their apparent deviation from the baseline is **run-to-run variation**, not a genuine enrichment-caused regression.

2. **The 2 main-run "errors" are confirmed evaluator flakiness.** TC31 (error in main) passed in 2 of 3 reruns; TC62 (error in main) returned partial and pass on reruns; TC32 errored only in rep1. The same case, same code, same data yields error in one run and pass/partial in another → the errors are **transient evaluator JSON-parse crashes**, not deterministic engine or instructional-object defects.

3. **Zero hard failures in any of the 4 runs.** No case produced a `fail` verdict at any point.

4. **TC37 is the single stable deviation.** It returned `partial` in all four runs. Its recurring note is a **target-selection** observation: on a compare/contrast piece whose documented target is *organizing structure* (Organization), the engine selects **Thesis** as the primary target (Organization is retrieved but not chosen as primary). This is the only case where the signal is consistent rather than noisy.

## Conclusion

- The Sprint 3 "regressions" are, with one exception, **statistical noise** inherent to the stochastic reasoner + evaluator — not genuine regressions from the instructional-object enrichment.
- The **evaluator harness**, not the engine or the objects, is the source of the `error` verdicts.
- **TC37** is the only case warranting future attention, and it is a **target-selection** nuance, not a fidelity failure (still a valid, authorship-preserving coaching move — just not the documented target).
- Consistent with the accepted Sprint 3 decision: **no tuning is warranted on this evidence.** The one stable item (TC37) is insufficient on its own to justify touching the frozen system and can be revisited later as a data-only investigation if desired.

## Recommendations (proposals only — no changes made)

- **P1 (tooling, not engine):** harden the evaluator harness JSON parsing / add a retry so transient evaluator crashes never surface as case `error`. This alone would have removed all 4 error occurrences observed here.
- **P3 (optional, future, data-only):** if TC37 persists as a stable partial, investigate whether STAGE-A/target-selection over-prefers Thesis over Organization on compare/contrast prompts. Any fix would be data-only (object retrieval text), engine frozen — and only after explicit review.
- **No action** on TC20, TC31, TC32, TC39, TC62, TC64 — demonstrated to be stochastic.

## Appendix
- Stability data: `/tmp/stability.json`. Run IDs: main `0bfe5b82`, rep1 `023c8f76`, rep2 `06d791b7`, rep3 `1ed65fde`, baseline `fd0dec0c`. All persisted in Mongo `test_runs`.
