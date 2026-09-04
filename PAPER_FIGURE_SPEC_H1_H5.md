# REC H1–H5 main figure specification

Status: **paper-facing figure contract aligned to `PAPER_LOGIC_H1_H5_V4.md`.**

The figures should show the argument, not reproduce every H1–H5 diagnostic. Formal notation and exhaustive condition tables belong in Methods/Supplement.

## Figure 1 — Why the event table cannot audit its own missing world

### Purpose

Establish the measurement problem in one glance.

### Layout

Single horizontal pipeline:

`external exposure/reference -> pre-entry evidence -> trigger/registration/archive -> event table -> downstream semantics -> ecological estimand`

Show an explicit branch from pre-entry exposures to `not entered`, visible only because an external reference/exposure system exists.

### Empirical anchors

- Findlay: CCTV-confirmed pass -> trigger -> capture;
- BirdVox: continuous audio window -> frozen gate -> entered window.

### Message

**Rows that never entered cannot be characterized from the final event table alone.**

Do not use Figure 1 to claim novelty of imperfect detection.

## Figure 2 — Record-entry selection changes ecological composition within observation strata

### Panel A — Raw fox/badger composition trajectory

Plot badger proportion at:

- CCTV reference passes: `0.359818`;
- confirmed trigger world: `0.439252`;
- confirmed-capture world: `0.482759`.

Use the same y-axis across stages and visually connect the three measurement worlds.

Source: `results/FINDLAY_CAMERA_TRAP_RESULT.md`.

### Panel B — CT-position-standardized fox/badger distortion

Show standardized recorded-minus-reference badger shifts at trigger and capture under both weighting schemes:

- trigger, equal-position: `+0.062413`;
- trigger, reference-pass weighted: `+0.053498`;
- capture, equal-position: `+0.149843`;
- capture, reference-pass weighted: `+0.139894`.

Add the four position-specific shift points behind or beside the standardized summaries so the retained adverse `SF` position is visible rather than hidden.

Source: `results/FINDLAY_POSITION_STANDARDIZED_DISTORTION.md` and `results/findlay_position_standardized_distortion_summary_v1.json`.

### Panel C — Otter mechanistic corroboration/adverse context

Plot position-standardized wet recorded-minus-reference shifts by camera setting:

- A: `-0.126993` equal-position; `-0.134821` reference-pass weighted;
- BS: `+0.003021`; `+0.000893`;
- BV: `-0.046370`; `-0.052487`.

The point is not "3/3 wet effects". The point is **A/BV retain the mechanism while BS demonstrates context/aggregation sensitivity**.

### Figure 2 message

**Pre-entry selection can change ecological composition within observation strata, while the selection function itself can vary across observation contexts.**

## Figure 3 — Upstream omission is irreversible downstream

### Purpose

Separate REC from a classifier-performance paper.

### Main quantities

For protected BirdVox 02/05 show:

- truth late-minus-early event-window prevalence contrast: `+0.130820`;
- raw entered contrast at z=2: `-0.005034`;
- oracle true-entry-only contrast at z=2: approximately `-0.000025`.

Optionally show units 02 and 05 as small points behind the pooled values.

### Required annotation

State directly on the figure or caption:

- the frozen annotation-naive score generalized poorly;
- this is an irreversibility stress test, not a representative detector benchmark.

Source: `results/BIRDVOX_PROTECTED_02_05_RESULT.md`.

### Figure 3 message

**Perfect downstream semantics can remove false entered rows but cannot recreate true rows removed upstream.**

## Figure 4 — Recovery is real but transport-limited

### Purpose

End constructively while showing the failed test.

### Panel A — Transport ladder summary

Plot macro mean absolute error for raw and correct entry-aware correction across regimes:

| Regime | Raw | Correct |
| --- | ---: | ---: |
| Otter camera holdout, matched context | 0.115982 | 0.059258 |
| Otter within-camera position holdout | 0.068216 | 0.064250 |
| Otter camera+position double holdout | 0.068216 | 0.081237 |
| Fox/badger trigger leave-position-out | 0.123093 | 0.090510 |
| Fox/badger capture leave-position-out | 0.210807 | 0.167972 |

Use an explicit zero-change/reference line if plotting relative error change instead:

- `-48.91%`;
- `-5.81%`;
- `+19.09%` adverse;
- `-26.47%`;
- `-20.32%`.

### Panel B — Falsification control

For the two analyses with frozen swapped-label sham controls, show raw / correct / sham together:

- otter camera+position: `0.068216 / 0.081237 / 0.153652`;
- fox/badger trigger: `0.123093 / 0.090510 / 0.150218`;
- fox/badger capture: `0.210807 / 0.167972 / 0.260198`.

### Panel C — Heterogeneity must remain visible

Show cell/position-level paired errors for the main transport tests, including:

- the `6/12` improved cells in otter double holdout;
- fox/badger `SF`, where correct correction worsens at both trigger and capture and sham is better.

Do not average these adverse cases away.

Sources:

- `results/FINDLAY_H5_CORRECTION_RESULT.md`;
- `results/FINDLAY_H5_TRANSPORT_BOUNDARY.md`;
- `results/FINDLAY_SPECIES_POSITION_RECOVERY.md`.

### Figure 4 message

**Entry provenance can support recovery, but correction validity is local to a tested calibration/transport domain.**

## Supplementary figures/tables

Move the following out of the four main figures:

- full H2 condition maps for distance/orientation/gait/loitering;
- BirdVox z=2 vs z=4 burden details;
- all unresolved-state partial-identification envelopes;
- exploratory within-camera position recovery details;
- complete camera × position cell table;
- event-log non-identifiability witness internals.

## Visual hierarchy rule

The main figures should make this sequence readable without the text:

`selected record -> changed estimand -> irreversible omission -> local recovery / failed transport`.

If a panel does not advance one of those four moves, move it to Supplement.