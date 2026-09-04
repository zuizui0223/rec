# Findlay camera-type REC-H5 correction result

Status: **positive retrospective cross-camera recovery demonstration; not a protected confirmatory correction trial**.

Source: Findlay otter wet/dry trigger table at immutable upstream commit `abc72f535bb59ebed202fb7acca852fc1647e97a`, Git blob `1f2fef008470ad1263d76beeb5be2b7006ff85aa`.

The frozen contract is `H5_CORRECTION_PLAN.md`. The machine-readable result is `results/findlay_h5_correction_v1.json`.

## Question

After REC identifies that wet and dry otter passes enter camera records at different rates, can entry-probability information learned from **other camera types** improve the wet/dry composition estimated from a held-out camera's triggered records?

The held-out camera's trigger outcomes are not used to estimate its correction propensity.

## Result

The correction improved the wet-pass composition estimate for **all three held-out camera types**.

| held-out camera | truth wet proportion | raw trigger-world | cross-camera IPW | raw abs. error | corrected abs. error |
| --- | ---: | ---: | ---: | ---: | ---: |
| A | 0.438017 | 0.270270 | 0.351706 | 0.167746 | 0.086311 |
| BS | 0.459821 | 0.378788 | 0.520413 | 0.081034 | 0.060591 |
| BV | 0.445833 | 0.346667 | 0.476704 | 0.099167 | 0.030871 |

Mean absolute error decreased from:

`0.115982 -> 0.059258`.

That is an absolute reduction of `0.056725`, or a **48.91% relative reduction**.

Thus the frozen retrospective H5 success rule is met:

- cameras improved: `3 / 3`;
- all-camera improvement: `true`;
- mean error decreased: `true`.

## Reference-unresolved sensitivity

Missing trigger states are not recoded as no-trigger.

For held-out A, the correction learned from BS+BV has one unresolved dry trigger state. The corrected wet proportion changes only from `0.350807` to `0.352070` across the resulting training-propensity envelope, around the point estimate `0.351706`.

For held-out BS, the A+BV training envelope gives `0.519483–0.520692` around point estimate `0.520413`.

For held-out BV, the A+BS training set has no unresolved trigger states, so the correction envelope collapses to the point estimate `0.476704`. BV itself contains one unresolved dry trigger row; this remains held-out reference uncertainty and is not used in training.

The positive improvement therefore is not an artifact of coding unresolved trigger states as failures.

## Interpretation

This is the first REC result that moves from **diagnosis** to **recovery**:

`structured entry loss -> estimate entry probabilities -> reweight recorded rows -> ecological composition moves toward reference truth`.

The result is useful because the correction is transported across camera types rather than estimated from the held-out camera's own trigger outcomes.

It is not perfect. In BS the correction overshoots the true wet proportion (`0.5204` versus `0.4598`) while still reducing absolute error. The correct claim is therefore **partial recovery**, not unbiased reconstruction.

## Governance boundary

This H5 analysis is retrospective. The Findlay outcomes were public and had already been inspected before this correction analysis was designed. The analysis contract was frozen before this rerun, but the dataset is not newly protected.

Therefore:

- REC-H5: **positive retrospective cross-camera recovery evidence**;
- confirmatory/prospective H5: **still open**;
- no tuning of wet/dry strata, weighting rule or holdout unit is justified after seeing this result.

A prospective System-A experiment remains the route to a protected correction claim.
