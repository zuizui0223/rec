# Findlay REC-H5 transport robustness boundary

Status: **mixed/adverse robustness result that narrows H5 from generic correction to context-dependent recoverability.**

Source data: `melaniefindlay/CT-Detection` commit `abc72f535bb59ebed202fb7acca852fc1647e97a`, blob `1f2fef008470ad1263d76beeb5be2b7006ff85aa` (`TRIGGER_OTTER_WET.DRY.csv`).

Frozen paper-facing robustness rule: `PAPER_LOGIC_H1_H5.md`.

GitHub Actions run: `33833692837`.

Inspectable artifact digest: `sha256:8b83ffe4676afc19d3ec1f0f674dd4f60e8baed68af443942810f605c076da10`.

## Why this validation was necessary

The first H5 result held out one camera model/setting at a time and estimated wet/dry trigger propensities from the other two camera streams. That analysis improved wet-composition error in all three held-out cameras and reduced mean absolute error by 48.91%.

However, the three camera streams were colocated within the same otter experiment. Thus a stronger test must ask whether the correction transports when the evaluation data also come from a physical CT position excluded from propensity estimation.

The frozen double-holdout therefore tests every evaluable `(camera, CT position)` cell using training rows with:

`CAMERA.ID != heldout camera` **and** `CT.POS != heldout position`.

The target remains wet proportion among independently observed otter passes.

Three estimators are compared:

1. raw triggered-record composition;
2. correct wet/dry entry-aware IPW;
3. direction-reversed sham IPW with wet/dry propensities swapped.

Missing trigger states remain unresolved and are propagated through a training-propensity envelope.

## Frozen double-holdout result: broad transport is not supported

Across 12 camera x position cells:

- raw mean absolute error: `0.068216`;
- correct IPW mean absolute error: `0.081237`;
- swapped-sham mean absolute error: `0.153652`;
- correct IPW changed error by `+19.09%` relative to raw, i.e. **worsened** aggregate error;
- correct IPW improved only `6/12` cells;
- correct IPW beat the direction-reversed sham in `8/12` cells;
- worst-case mean corrected error under unresolved-training bounds was `0.081457`, still worse than raw.

The frozen promotion rule therefore fails.

### By camera model/setting

| held-out camera | raw MAE | correct IPW MAE | sham MAE | correct vs raw |
| --- | ---: | ---: | ---: | --- |
| A | 0.126993 | 0.053219 | 0.199446 | improves |
| BS | 0.022881 | 0.110358 | 0.110088 | worsens |
| BV | 0.054774 | 0.080136 | 0.151424 | worsens |

The correction is therefore not failing because the direction of wet/dry selection is meaningless: it strongly improves A and usually beats a reversed-direction sham. It fails because the magnitude of the selection function is not sufficiently transportable across camera x position combinations.

### By CT position

| held-out position | raw MAE | correct IPW MAE | sham MAE | correct vs raw |
| --- | ---: | ---: | ---: | --- |
| A | 0.074315 | 0.083499 | 0.223803 | worsens |
| BL | 0.026002 | 0.020343 | 0.029935 | improves |
| BW | 0.072942 | 0.122375 | 0.158355 | worsens |
| C | 0.099606 | 0.098733 | 0.202516 | improves slightly |

Thus the failure is also not attributable to a single physical position.

## Exploratory position-only diagnostic

After the frozen double-holdout failed, an explicitly exploratory diagnostic asked a narrower transport question: within each camera model/setting, can wet/dry propensities estimated from the other CT positions improve a held-out position?

Across the same 12 camera x position evaluation cells:

- raw mean absolute error: `0.068216`;
- position-holdout correct IPW mean absolute error: `0.064250`;
- swapped-sham mean absolute error: `0.150278`;
- aggregate relative improvement: **5.81%**;
- cells improved: `6/12`;
- cells beating sham: `8/12`.

This is weak average improvement, not robust transport. Camera A improves strongly, but BS and BV do not improve on their camera-level macro averages. Positions BL and C improve, whereas A and BW do not.

Because this diagnostic was added after seeing the double-holdout result, it is a mechanism/transport diagnosis only and cannot replace the frozen adverse result.

## Revised H5 conclusion

The evidence now supports a narrower and more useful statement:

> **Record-entry information can enable partial ecological recovery when calibration and target data share enough observation context, but a simple wet/dry propensity correction is not invariant across simultaneous changes in camera model/setting and physical recording position.**

This result strengthens the measurement argument rather than supporting a generic IPW claim.

The practical lesson is that an entry correction must carry its calibration provenance and transport domain. A detection/entry probability estimated in one observation context should not be treated as a universal property of the biological event.

## Relation to the earlier positive H5 result

The original `3/3` camera-holdout result remains valid as a retrospective **matched-context hardware-transport** demonstration:

`mean error 0.115982 -> 0.059258` (`48.91%` reduction).

It should no longer be described as evidence of broadly transportable correction. The combined interpretation is:

1. entry-aware correction can be useful;
2. its direction is mechanistically meaningful relative to a reversed sham;
3. its magnitude is context dependent;
4. prospective/local calibration or a richer propensity model is required before correction is exported to new observation contexts.

## Hard boundary

Do not claim from Findlay H5 that:

- IPW universally reconstructs the pass-world composition;
- wet/dry trigger propensity is invariant across camera types or positions;
- the public retrospective data provide protected confirmatory recovery;
- CT positions or rows are independent animals.

The next confirmatory recovery claim must come from prospectively designated calibration and held-out data, with the transport domain frozen before held-out outcomes are opened.
