# Findlay fox/badger species-composition recovery across CT positions

Status: **positive but heterogeneous retrospective secondary-endpoint recovery result; supports partial local transport, not universal correction.**

Source: `melaniefindlay/CT-Detection` commit `abc72f535bb59ebed202fb7acca852fc1647e97a`, file `REGISTRATION_FOX_BADGER.csv`, Git blob `d2dc9852ca1f2a1380b991acba425d16e12327d5`.

GitHub Actions run: `33834062924`.

Artifact digest: `sha256:61383744ec7babac2327a3c391717ec95b81e56d0fcb31172265a37d2c610692`.

## Question

Does the H5 recovery pattern extend beyond the otter wet/dry endpoint?

Fox and badger were observed with the same Bushnell video camera system at four physical CT positions (`AP`, `FF`, `SF`, `SNIG`). For each held-out position, species-specific entry probabilities were estimated from all other positions and used to reweight the held-out recorded badger/fox composition toward the CCTV-confirmed pass composition.

The target estimand is:

`badger proportion among CCTV-confirmed fox/badger passes within the held-out CT position`.

The analysis was run separately for:

1. trigger entry (`R=1`);
2. final confirmed capture / record entry (`K=1`).

For each stage, compare:

- raw recorded species composition;
- correct species-specific IPW;
- swapped-species sham IPW.

This is retrospective secondary-endpoint robustness analysis, not prospective or independent-animal confirmation.

## Trigger-stage result

Across four leave-one-position-out tests:

- raw mean absolute error: `0.123093`;
- correct IPW mean absolute error: `0.090510`;
- swapped-sham mean absolute error: `0.150218`;
- relative error reduction: **26.47%**;
- positions improved: `3/4`;
- positions where correct IPW beat sham: `3/4`.

Position-specific errors:

| held-out CT position | raw error | correct IPW error | sham error | result |
| --- | ---: | ---: | ---: | --- |
| AP | 0.141960 | 0.084761 | 0.199930 | improves |
| FF | 0.086713 | 0.010680 | 0.165289 | strongly improves |
| SF | 0.121361 | 0.191415 | 0.029265 | worsens; sham is better |
| SNIG | 0.142339 | 0.075182 | 0.206390 | improves |

Thus species-specific trigger correction is useful on average but not invariant across physical positions.

## Final-capture result

Across the same four held-out positions:

- raw mean absolute error: `0.210807`;
- correct IPW mean absolute error: `0.167972`;
- swapped-sham mean absolute error: `0.260198`;
- relative error reduction: **20.32%**;
- positions improved: `3/4`;
- positions where correct IPW beat sham: `3/4`.

Position-specific errors:

| held-out CT position | raw error | correct IPW error | sham error | result |
| --- | ---: | ---: | ---: | --- |
| AP | 0.337553 | 0.248130 | 0.416399 | improves |
| FF | 0.153233 | 0.047025 | 0.258202 | strongly improves |
| SF | 0.121928 | 0.233591 | 0.059042 | worsens; sham is better |
| SNIG | 0.230514 | 0.143143 | 0.307150 | improves |

Two unresolved final-capture states occur in the training material for some held-out positions. Propensity bounds were propagated rather than coded as failures. The mean worst-case corrected error under those bounds is `0.169423`, still below the raw mean `0.210807`; unresolved states therefore do not explain the aggregate improvement.

## Interpretation

This second ecological endpoint reproduces the same qualitative H5 boundary seen in the otter analysis:

1. record-entry information can improve an ecological composition estimate outside the physical position used to estimate it;
2. the improvement is not universal;
3. one position (`SF`) reverses the benefit at both trigger and final-capture stages;
4. calibration context is therefore part of the entry model rather than a nuisance detail that can be ignored.

The species result is valuable because it is distinct from wet/dry otter composition and uses a wild fox/badger system with one camera model/setting. It therefore reduces the chance that H5 is only a wet-otter artifact, while independently showing that spatial transport remains heterogeneous.

## Combined H5 message

The full Findlay evidence now supports:

> **Entry-aware correction can partially recover ecological composition in multiple endpoints, but its operating meaning is context dependent. Correction performance must therefore be validated across the hardware/position domain to which it will be transported.**

This is stronger and safer than a generic claim that IPW or a single detection probability reconstructs the truth world.

## Hard boundaries

Do not claim:

- independent-animal validation from the four CT positions;
- universal species-specific detectability across locations;
- prospective H5 confirmation;
- that every held-out context improves;
- that the swapped sham is always worse (it wins at SF).
