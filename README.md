# REC — Record-Entry Censoring

**REC studies how biological exposures become—or fail to become—usable ecological records before downstream semantic analysis.**

Status: **external-data H1–H5 manuscript is draft-ready; prospective same-system REC→TNOA validation remains open.**

The frozen TNOA Paper 1 remains in `zuizui0223/tnoa`. This repository owns REC validation, correction, transport tests and prospective REC→TNOA work.

## Current paper claim

REC does **not** claim discovery of imperfect detection. The paper asks a narrower empirical question:

> **When record-entry selection is measurable against an external exposure/reference world, does it change the ecological estimand, can omitted information be repaired downstream, and over what observation domain can entry-aware correction be trusted?**

The current answer is mixed and therefore useful:

1. **record-entry selection can change ecological composition within observation strata;**
2. **downstream semantic perfection cannot recreate true rows removed upstream;**
3. **entry provenance can support partial recovery;**
4. **the selection function and its correction are context dependent and do not transport automatically.**

Canonical manuscript logic: `PAPER_LOGIC_H1_H5_V4.md`.

Current draft: `MANUSCRIPT_DRAFT_H1_H5.md`.

Readiness summary: `MANUSCRIPT_READINESS_H1_H5.md`.

## Strongest empirical result — fox/badger species composition

Findlay's CCTV-referenced camera-trap data provide 881 independently observed fox/badger passes followed by trigger and final-capture outcomes.

Overall:

- `P(no trigger | pass) = 0.514188`;
- bounded `P(no confirmed capture | pass) = 0.800227–0.802497`;
- badger proportion among true passes = `0.359818`;
- badger proportion among confirmed triggers = `0.439252`;
- badger proportion among confirmed captures = `0.482759`.

A frozen CT-position standardization test shows that the composition shift is not only a pooled position-mixture artifact.

At trigger:

- equal-position standardized shift = `+0.062413`;
- reference-pass-weighted shift = `+0.053498`;
- positive direction in `3/4` positions.

At final capture:

- equal-position standardized shift = `+0.149843`;
- reference-pass-weighted shift = `+0.139894`;
- positive direction in `3/4` positions.

`SF` remains the adverse position at both stages.

This is now the primary H2→H3 paper endpoint: **selective entry changes species composition within observation strata before downstream classification begins.**

See:

- `results/FINDLAY_CAMERA_TRAP_RESULT.md`;
- `results/FINDLAY_POSITION_STANDARDIZED_DISTORTION.md`;
- `results/findlay_position_standardized_distortion_summary_v1.json`.

## Otter wet/dry — mechanistic corroboration plus adverse context

The pooled otter data initially showed wet underrepresentation for camera settings A, BS and BV. Position standardization sharpened that interpretation:

- **A:** robust wet underrepresentation, negative in `4/4` positions;
- **BV:** robust overall, negative in `3/4` positions;
- **BS:** pooled effect disappears after standardization; standardized shift is approximately zero and the direction splits `2/4` vs `2/4`.

Therefore REC no longer treats all three otter settings as clean position-robust replications. BS is retained as an adverse aggregation-sensitive case.

This is scientifically important: **the operating record-entry selection function itself can depend on observation context.**

## BirdVox — protected irreversibility stress test

BirdVox-full-night supplies continuous audio and expert call annotations. The frozen annotation-naive gate generalizes poorly and is not a competent-detector benchmark.

Its useful result is narrower. In protected units 02/05:

- true late-minus-early event-window prevalence contrast = `+0.130820`;
- oracle true-entry-only contrast under the frozen z=2 gate ≈ `-0.000025`.

Even after granting a perfect downstream semantic stage that removes all false entered rows, the true ecological contrast is not recovered because truth-positive windows removed upstream no longer exist in the analysed record.

BirdVox therefore supplies the cross-modality REC→TNOA boundary:

> **better downstream classification cannot reconstruct omitted upstream rows without additional information or assumptions.**

See `results/BIRDVOX_PROTECTED_02_05_RESULT.md`.

## H5 — recovery exists, but transport is conditional

The correction result is now a hierarchy rather than one positive claim.

| Endpoint / transport regime | Raw MAE | Corrected MAE | Sham MAE | Relative change | Improved units |
| --- | ---: | ---: | ---: | ---: | ---: |
| Otter wet/dry: camera holdout, matched context | 0.115982 | 0.059258 | — | −48.91% | 3/3 |
| Otter wet/dry: within-camera position holdout | 0.068216 | 0.064250 | 0.150278 | −5.81% | 6/12 |
| Otter wet/dry: camera + position double holdout | 0.068216 | 0.081237 | 0.153652 | **+19.09%** | 6/12 |
| Fox/badger species: trigger, position holdout | 0.123093 | 0.090510 | 0.150218 | −26.47% | 3/4 |
| Fox/badger species: final capture, position holdout | 0.210807 | 0.167972 | 0.260198 | −20.32% | 3/4 |

The frozen camera+position double holdout is deliberately adverse: correction worsens average wet-composition error. It is retained unchanged.

The paper-level H5 conclusion is therefore:

> **entry information can reduce ecological error, but the entry model has a calibration and transport domain. A correction should not be exported across hardware or observation contexts without transport validation.**

See:

- `results/FINDLAY_H5_CORRECTION_RESULT.md`;
- `results/FINDLAY_H5_TRANSPORT_BOUNDARY.md`;
- `results/FINDLAY_SPECIES_POSITION_RECOVERY.md`.

## Core measurement distinction

TNOA starts **after a row exists** and asks whether process distinctions should be preserved or semantically coarsened.

REC starts **before record entry** and asks which exposures/events entered at all and whether that selection changed the ecological estimand.

```text
biological process
       |
       v
external exposure / reference world
       |
       v
pre-entry evidence / physical sensor process
       |
       v
trigger / registration / archive entry      <- REC
       |
       v
available event table
       |
       v
B / T / N / U and later coarsening          <- TNOA
       |
       v
ecological inference
```

Foundational rule:

> **Define exposure before defining non-detection.**

A final event table cannot empirically identify the biological composition of exposures that never became rows. REC therefore requires an external exposure/reference design for claims about the non-entered world.

See `IDENTIFIABILITY_BOUNDARY.md` and `EXPOSURE_LEDGER_SCHEMA.md`.

## Current H1–H6 status

- **H1 — shadow existence:** positive across camera-trap and acoustic systems; foundation, not novelty headline.
- **H2/H3 — structured entry changes ecology:** strongest in position-standardized fox/badger species composition; otter A/BV corroborate; BS is adverse/context sensitive.
- **H4 — gate sensitivity:** positive in BirdVox but treated as sensitivity/supporting evidence rather than a headline discovery.
- **H5 — recoverability:** retrospective partial recovery positive in matched/partly transported contexts; broad transport explicitly falsified by the frozen otter camera+position test.
- **H6 — REC→TNOA same-system decomposition:** architecture/readiness gates exist, but empirical prospective held-out scoring remains open.

## Prospective System A / PolliPi

PolliPi is the prospective route to a stronger future claim, not a prerequisite for the current H1–H5 manuscript.

The repository already contains:

- a same-system H6 contract;
- a fail-closed readiness checker;
- a prospective Phase-A development intake audit;
- provenance rules preventing held-out recordings from being retrospectively relabelled as development/calibration data.

The remaining empirical step is physical data collection with synchronized independent reference truth, development-only calibration, a frozen transport domain and untouched held-out scoring.

See:

- `H6_SAME_SYSTEM_CONTRACT.md`;
- `results/H6_POLLIPI_READINESS_AUDIT.md`;
- `POLLIPI_PHASE_A_DEVELOPMENT_COLLECTION.md`.

## Practical contribution

The manuscript's actionable recommendation is a measurement contract rather than new terminology.

Automated ecological monitoring should retain, when feasible:

- a gate-independent exposure/reference denominator;
- pre-entry evidence and diagnostics;
- versioned trigger/gate/archive-entry provenance;
- unresolved states rather than forced negatives;
- independent truth audits that include non-entered exposures;
- calibration context and a validated transport domain for any correction model.

A final event table alone discards exactly the information required to determine whether the recorded composition is representative and whether a proposed correction is transferable.

## Repository map

### Paper-facing

- `PAPER_LOGIC_H1_H5_V4.md` — canonical manuscript argument;
- `MANUSCRIPT_DRAFT_H1_H5.md` — working manuscript;
- `MANUSCRIPT_READINESS_H1_H5.md` — evidence/readiness matrix;
- `PRIOR_ART_BOUNDARY.md` — novelty boundary;
- `IDENTIFIABILITY_BOUNDARY.md` — identification limits.

### Main empirical results

- `results/FINDLAY_CAMERA_TRAP_RESULT.md`;
- `results/FINDLAY_POSITION_STANDARDIZED_DISTORTION.md`;
- `results/FINDLAY_H5_CORRECTION_RESULT.md`;
- `results/FINDLAY_H5_TRANSPORT_BOUNDARY.md`;
- `results/FINDLAY_SPECIES_POSITION_RECOVERY.md`;
- `results/BIRDVOX_PROTECTED_02_05_RESULT.md`.

### Prospective REC→TNOA

- `H6_SAME_SYSTEM_CONTRACT.md`;
- `POLLIPI_PHASE_A_DEVELOPMENT_COLLECTION.md`;
- `scripts/check_h6_readiness.py`;
- `scripts/audit_pollipi_phase_a_development.py`.

## Hard boundaries

Do not claim:

- discovery of imperfect detection;
- universal loss magnitudes;
- a universal wetness effect across all otter camera settings;
- universal IPW correction;
- independence of repeated Findlay passes as animals/populations;
- representative BirdVox detector performance;
- prospective H5 confirmation;
- empirical H6.

The current paper is strongest precisely because it retains both successful and failed transport tests rather than tuning the story after evaluation.