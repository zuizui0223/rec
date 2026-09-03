# BirdVox unit10 real-data REC smoke result

Status: **real public-data smoke result; not the final three-sensor confirmatory REC result**.

Source: BirdVox-full-night v3.0, held-out sensor `10`, Zenodo record `1205569`. The workflow verified the released audio and annotation MD5s before analysis and used `annotation-naive-band-energy-v1`, which does not read BirdVox truth when constructing the pre-gate score.

The exact machine-readable output is `results/birdvox_unit10_real_data_smoke_v1.json`.

## Result

The first real-data run supports the existence of a REC record shadow under both frozen gates.

At robust-z threshold `2`:

- truth-positive one-second windows: `4,461 / 29,484` (`0.1513` prevalence);
- independently annotated events absorbed by the gate: `3,230`;
- `a_R = P(R=0 | E=1, gate evaluable) = 0.7241`;
- `q_B = P(E=1 | R=0) = 0.1448`;
- early-night event absorption: `0.6352`;
- late-night event absorption: `0.7633`.

At robust-z threshold `4`:

- absorbed truth-positive windows: `3,910`;
- `a_R = 0.8765`;
- `q_B = 0.1522`;
- early-night event absorption: `0.8582`;
- late-night event absorption: `0.8846`.

Thus REC-H1 is positive in this held-out smoke system: biological events independently present in the continuous reference record are common inside the registered baseline / non-entered world.

## Ecological consequence in the prespecified one-second event-window endpoint

The expert-truth late-minus-early prevalence contrast is positive:

`truth late - early = +0.1170`.

The recorded world reverses that direction under both frozen gates:

- z=2: `recorded late - early = -0.2756`, absolute contrast error `0.3926`;
- z=4: `recorded late - early = -0.1628`, absolute contrast error `0.2798`.

This is stronger than a simple downward count bias: in unit10, record-entry selection changes the direction of the frozen temporal ecological contrast.

However, the overall prevalence behavior shows why REC should not be reduced to false negatives. At z=2 the recorded prevalence is `0.2434` versus truth `0.1513`, so false/extra registrations dominate enough to produce overall overestimation even while `72.4%` of truth-positive windows are absorbed. At z=4, recorded prevalence is `0.1287`, closer to truth (`MAE 0.0226`) despite higher true-event absorption (`87.6%`).

This adverse tradeoff is a positive REC-H4 result: changing only the frozen gate changes the observed scientific world. Raising the threshold from 2 to 4 increases event absorption by `+0.1524` but decreases overall prevalence error by `0.0695`; it does not restore the temporal contrast sign.

## Interpretation boundary

This result demonstrates **algorithmic record-entry censoring after audio acquisition**. Expert truth comes from the same continuous audio, so it cannot identify calls that the microphone itself failed to acquire.

Only one held-out sensor is represented here. The early/late difference is therefore a within-sensor descriptive H2 signal, not a general condition-effect estimate. Sensor-level generality and grouped uncertainty require the frozen held-out trio `02/05/10`.

Accordingly:

- REC-H1: **positive smoke evidence**;
- REC-H2: **descriptive condition structure present, generality unresolved**;
- REC-H3: **positive smoke evidence, including temporal-contrast sign reversal**;
- REC-H4: **positive smoke evidence with a nontrivial FN/FP tradeoff**;
- publication-level generalization: **not yet promoted**.
