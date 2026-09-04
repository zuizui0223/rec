# Findlay camera-type REC-H5 matched-context correction result

Status: **positive retrospective matched-context cross-camera recovery demonstration; later transport stress tests show this correction does not generalize automatically to new camera × position contexts.**

Source: Findlay otter wet/dry trigger table at immutable upstream commit `abc72f535bb59ebed202fb7acca852fc1647e97a`, Git blob `1f2fef008470ad1263d76beeb5be2b7006ff85aa`.

The machine-readable result is `results/findlay_h5_correction_v1.json`.

## Question

After REC identifies differential entry between wet and dry otter passes, can entry probabilities learned from **other colocated camera settings** improve the wet/dry composition estimated from a held-out camera's triggered records?

The held-out camera's trigger outcomes are not used to estimate its correction propensity. However, the camera streams share the broader encounter/position context, so this is a hardware holdout within a matched observation domain rather than an independent-context transport test.

## Result

The correction improved the wet-pass composition estimate for all three held-out camera settings.

| held-out camera | truth wet proportion | raw trigger-world | cross-camera IPW | raw abs. error | corrected abs. error |
| --- | ---: | ---: | ---: | ---: | ---: |
| A | 0.438017 | 0.270270 | 0.351706 | 0.167746 | 0.086311 |
| BS | 0.459821 | 0.378788 | 0.520413 | 0.081034 | 0.060591 |
| BV | 0.445833 | 0.346667 | 0.476704 | 0.099167 | 0.030871 |

Mean absolute error decreased from:

`0.115982 -> 0.059258`.

That is a **48.91% relative reduction**.

Thus the original retrospective success rule is met within this matched-context camera-holdout design:

- cameras improved: `3 / 3`;
- all-camera improvement: `true`;
- mean error decreased: `true`.

## Reference-unresolved sensitivity

Missing trigger states are not recoded as no-trigger.

For held-out A, the correction learned from BS+BV has one unresolved dry trigger state. The corrected wet proportion changes only from `0.350807` to `0.352070` across the training-propensity envelope, around the point estimate `0.351706`.

For held-out BS, the A+BV training envelope gives `0.519483–0.520692` around point estimate `0.520413`.

For held-out BV, the A+BS training set has no unresolved trigger states, so the correction envelope collapses to the point estimate `0.476704`. BV itself contains one unresolved dry trigger row; this remains held-out reference uncertainty and is not used in training.

The positive matched-context improvement is therefore not an artifact of coding unresolved trigger states as failures.

## Interpretation after later transport tests

This analysis established an important constructive result:

`structured entry loss -> estimate entry probabilities -> reweight recorded rows -> ecological composition can move toward reference truth`.

But it no longer carries the stronger interpretation that a wet/dry propensity learned from other cameras is broadly portable.

A later frozen camera-plus-position double holdout removed both the held-out camera and held-out physical CT position from training. In that harder transport regime, mean error **increased by 19.09%** (`0.068216 -> 0.081237`). See `results/FINDLAY_H5_TRANSPORT_BOUNDARY.md`.

A separate fox/badger species endpoint showed average leave-position-out recovery at trigger and final capture, but also retained an adverse position (`SF`). See `results/FINDLAY_SPECIES_POSITION_RECOVERY.md`.

The correct H5 conclusion is therefore:

> **Entry information can support partial recovery within some calibration domains, but correction transport is observation-context dependent and must be independently validated.**

## Position-standardization boundary for the wet/dry mechanism

A later frozen standardization analysis also showed that the pooled wet-underrepresentation pattern is not equally robust across all three camera settings:

- A remains strongly negative across position standardizations;
- BV remains negative overall;
- BS becomes approximately zero after placing truth and recorded worlds under the same CT-position distribution.

Therefore the BS matched-context correction result is best understood as recovery of the observed pooled composition distortion in that dataset, not as evidence for a position-invariant wetness selection mechanism.

See `results/FINDLAY_POSITION_STANDARDIZED_DISTORTION.md`.

## Governance boundary

This H5 analysis is retrospective. The Findlay outcomes were public and had already been inspected before the correction analysis was designed. The analysis contract was frozen before this rerun, but the dataset is not newly protected.

Therefore:

- H5 matched-context recoverability: **positive retrospective evidence**;
- broad correction transport: **not supported** by the harder frozen test;
- prospective/protected H5: **still open**;
- no post-result retuning of the failed transport test is justified.
