# REC H1–H5 manuscript readiness

Status: **draft-ready external-data paper with a position-robust primary ecological endpoint.**

Canonical logic: `PAPER_LOGIC_H1_H5_V4.md`.

Current draft: `MANUSCRIPT_DRAFT_H1_H5.md`.

## Current paper-level conclusion

> **Record-entry selection can change an ecological estimand within observation strata; entry provenance can support partial recovery, but both the selection function and the correction have an observation-context domain that must be validated.**

This is stronger and narrower than the earlier all-positive H1–H5 framing.

## What is now strongest

### 1. Primary H2→H3 result: fox/badger species composition

Among 881 CCTV-confirmed passes, 51.4% fail to trigger and roughly 80.0–80.2% fail to become confirmed captures. Badger representation rises from 0.3598 in the reference pass world to 0.4393 after trigger and 0.4828 after confirmed capture.

The frozen CT-position standardization test shows that this is not only a pooled position-mixture artifact:

- trigger standardized shift: `+0.0624` under equal-position weighting and `+0.0535` under reference-pass weighting;
- capture standardized shift: `+0.1498` and `+0.1399`;
- `3/4` positions retain the positive direction at both stages;
- `SF` is the adverse position.

This should be the central empirical result and Figure 2 main panel.

### 2. Otter wet/dry is now mechanistic corroboration, not the primary endpoint

Position standardization reveals real heterogeneity:

- A: robust wet underrepresentation, negative in `4/4` positions;
- BV: robust overall, negative in `3/4` positions;
- BS: pooled effect disappears after standardization, with approximately zero standardized shift and a `2/4` vs `2/4` directional split.

Therefore do **not** describe all three camera settings as position-robust wetness replications. BS is a useful adverse case demonstrating context dependence.

### 3. BirdVox remains the independent irreversibility stress test

Protected units 02/05 show that a true temporal contrast of `+0.130820` is essentially absent after upstream omission even under an oracle true-entry-only downstream stage. The frozen detector is poor and is explicitly not a representative performance benchmark.

### 4. H5 is a transport hierarchy, not a universal correction claim

| Endpoint / transport regime | Raw MAE | Corrected MAE | Sham MAE | Relative change | Units improved |
| --- | ---: | ---: | ---: | ---: | ---: |
| Otter wet/dry: camera holdout, matched context | 0.115982 | 0.059258 | — | −48.91% | 3/3 |
| Otter wet/dry: within-camera position holdout | 0.068216 | 0.064250 | 0.150278 | −5.81% | 6/12 |
| Otter wet/dry: camera + position double holdout | 0.068216 | 0.081237 | 0.153652 | **+19.09%** | 6/12 |
| Fox/badger species: trigger, position holdout | 0.123093 | 0.090510 | 0.150218 | −26.47% | 3/4 |
| Fox/badger species: final capture, position holdout | 0.210807 | 0.167972 | 0.260198 | −20.32% | 3/4 |

The adverse double holdout is a central result, not a limitation to bury. It shows that the correct direction of selection can contain information while the propensity magnitude fails to transport across simultaneous hardware/context shift.

## Evidence-strength matrix

| Paper claim | Evidence | Current strength | Manuscript role |
| --- | --- | --- | --- |
| Event-log-only data cannot characterize non-entered biology | deterministic witness + external denominators | strong methodological | Result 1 / Fig. 1 |
| True events fail before usable record entry | Findlay + BirdVox | strong cross-modality | foundation |
| Entry selection changes ecological composition within observation strata | fox/badger CT-position standardization | **strongest empirical result** | Result 2 / Fig. 2 |
| Biological-state entry selection can be context dependent | otter A/BV positive; BS adverse after standardization | strong mixed mechanism | Result 2 secondary |
| Downstream perfection cannot restore upstream omission | BirdVox oracle analysis | strong stress test | Result 3 / Fig. 3 |
| Entry information can support recovery | matched-context otter + fox/badger position holdout | positive retrospective | Result 4 |
| Correction transports broadly | frozen otter camera+position double holdout | **falsified** | Result 4 central boundary |
| Prospective correction improves untouched field data | not yet available | open | future / PolliPi |
| Same-system REC→TNOA decomposition | architecture only | open | future H6 |

## Main figures

1. **Auditable pipeline** — external reference/exposure, pre-entry selection, event table, downstream semantics.
2. **Position-robust ecological distortion** — fox/badger reference → trigger → capture plus CT-position-standardized shifts; otter A/BV/BS as corroboration/adverse inset.
3. **Irreversibility** — BirdVox truth contrast vs raw entered/oracle true-entry-only contrast.
4. **Recovery transport ladder** — matched context through camera+position shift and second-endpoint species recovery; raw/correct/sham errors.

## What not to do now

- Do not run more Findlay subsets looking for positive results.
- Do not rescue BS by redefining the position grouping.
- Do not rescue the failed double holdout with the post-result exploratory within-camera diagnostic.
- Do not make H6 a condition for this manuscript.
- Do not return to a five-independent-hypothesis narrative.

The retrospective analysis phase is sufficiently saturated. Further slicing now has lower evidential value than drafting, figure construction and literature positioning.

## Highest-value remaining upgrade

A genuinely prospective or independent-system correction test with a frozen transport domain would materially upgrade H5. PolliPi is being prepared for that role, but the present H1–H5 manuscript is already coherent without it.

## Submission-readiness decision

**Proceed to manuscript and figure production now.**

The paper has both confirmation and falsification:

- a robust within-position ecological distortion;
- a second mechanism that exposes context dependence;
- independent cross-modality irreversibility;
- partial recovery under some calibration domains;
- explicit failure of broad correction transport.

That mixed structure is the paper's credibility asset rather than a defect.