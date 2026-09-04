# REC-H5 correction plan — Findlay otter wet/dry camera types

Status: **frozen retrospective cross-camera evaluation contract**.

This analysis asks a narrow H5 question: after REC diagnoses condition-dependent trigger entry, can entry-probability information learned from other camera types improve the ecological composition estimated from a held-out camera's triggered records?

## Estimand

For each held-out camera type, estimate the proportion of independently observed otter passes that are `wet`.

The pass-world proportion is reference truth for evaluation. The raw scientific record is the composition among confirmed triggered rows.

## Correction

For each held-out camera type `c`:

1. estimate resolved-only `P(TRIGGER=1 | wet)` and `P(TRIGGER=1 | dry)` using only rows from the other camera types;
2. retain trigger-reference-unresolved rows separately and report propensity lower/upper bounds;
3. apply self-normalized inverse-probability weights to confirmed triggered rows from camera `c`;
4. compare absolute error of raw trigger-world wet proportion versus corrected wet proportion against the known pass-world proportion.

No held-out trigger outcome is used to estimate its entry propensity.

## Success criterion

Retrospective H5 support requires:

- corrected absolute error < raw absolute error for every held-out camera type; and
- mean absolute error across held-out camera types decreases.

The effect size is the mean absolute-error reduction and its relative reduction.

## Governance boundary

The Findlay outcomes were public and had already been inspected before this H5 analysis was designed. Therefore this is **not** a protected confirmatory correction test. It is a reproducible cross-camera transport demonstration.

No post-hoc tuning is allowed after this contract: the conditioning variable is only `wet/dry`, the correction is self-normalized IPW, and the holdout unit is camera type.

A future prospective System-A test is still required for a confirmatory H5 claim.
