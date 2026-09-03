# BirdVox unit10 real-data REC smoke result

Status: **real public-data smoke result; exploratory/pilot after inspection, not an independent replication unit**.

Source: BirdVox-full-night v3.0 sensor `10`, Zenodo record `1205569`. The workflow verified the released audio and annotation MD5s before analysis and used `annotation-naive-band-energy-v1`, which does not read BirdVox truth when constructing the pre-gate score.

The exact machine-readable H1-H4 output is `results/birdvox_unit10_real_data_smoke_v1.json`.

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

Thus REC-H1 is positive in this pilot system: biological events independently present in the continuous reference record are common inside the registered baseline / non-entered world.

## Ecological consequence in the prespecified one-second event-window endpoint

The expert-truth late-minus-early prevalence contrast is positive:

`truth late - early = +0.1170`.

The raw recorded world reverses that direction under both frozen gates:

- z=2: `recorded late - early = -0.2756`, absolute contrast error `0.3926`;
- z=4: `recorded late - early = -0.1628`, absolute contrast error `0.2798`.

This is stronger than a simple downward count bias: in unit10, record-entry selection changes the direction of the frozen temporal ecological contrast.

However, the overall prevalence behavior shows why REC should not be reduced to false negatives. At z=2 the recorded prevalence is `0.2434` versus truth `0.1513`, so false/extra registrations dominate enough to produce overall overestimation even while `72.4%` of truth-positive windows are absorbed. At z=4, recorded prevalence is `0.1287`, close to truth despite higher true-event absorption (`87.6%`). Aggregate agreement therefore hides strong composition errors.

This adverse tradeoff is a positive REC-H4 result: changing only the frozen gate changes the observed scientific world. Raising the threshold from 2 to 4 increases event absorption by `+0.1524` while reducing overall prevalence error; it does not restore the temporal contrast sign.

## Upstream omission survives perfect downstream semantics

A separate additive diagnostic asks what would remain if a hypothetical perfect downstream semantic stage removed **every false entry** using truth labels but could not restore any true event that failed to enter. This is the direct REC-to-TNOA bridge.

At z=2:

- early truth prevalence `0.09280`, late truth prevalence `0.20981`;
- early true-entered prevalence `0.03385`, late true-entered prevalence `0.04965`;
- truth contrast `+0.11701`;
- perfect-downstream / true-entry-only contrast `+0.01581`;
- only `13.51%` of the truth contrast remains after false entries are removed.

At z=4:

- early true-entered prevalence `0.01316`, late true-entered prevalence `0.02422`;
- perfect-downstream / true-entry-only contrast `+0.01106`;
- only `9.45%` of the truth contrast remains.

Therefore the sign reversal in the raw record is partly driven by false entry, but the central REC result does **not** depend on false entry: after granting a perfect downstream classifier, upstream omission alone still removes roughly `86.5%` to `90.6%` of the frozen ecological contrast. Information that never became a row is unavailable to a later TNOA semantic stage.

## Mechanism diagnostic

At z=2, truth prevalence rises from early `0.0928` to late `0.2098`, while raw registered prevalence falls from `0.3812` to `0.1055`. The false-registration rate among truth-negative windows is `0.3828` early versus `0.0707` late. Across 30-minute blocks, raw recorded prevalence tracks the block score baseline (`r≈0.97`) but is essentially unrelated to truth prevalence (`r≈-0.03`). Score discrimination also changes across the night (early AUC≈`0.487`, late AUC≈`0.693`).

The safe mechanism statement is therefore that the same frozen gate has strongly condition-dependent operating meaning, and this observation-process shift can overwrite the biological temporal gradient in the scientific record.

## Interpretation and governance boundary

This result demonstrates **algorithmic record-entry censoring after audio acquisition**. Expert truth comes from the same continuous audio, so it cannot identify calls that the microphone itself failed to acquire.

Unit10 has now been inspected and is explicitly a pilot/exploratory unit. No independent-generalization claim uses it. The score definition, one-second `Omega`, z=2/z=4 gates, H1-H4 estimands and late/early endpoint were frozen before opening protected sensors `02` and `05`, which remain the independent replication units.

Accordingly:

- REC-H1: **positive pilot evidence**;
- REC-H2: **strong within-unit condition structure, generality unresolved until 02/05**;
- REC-H3: **positive pilot evidence, including raw sign reversal and large upstream-only contrast attenuation**;
- REC-H4: **positive pilot evidence with a nontrivial omission/false-entry tradeoff**;
- independent replication: **reserved for protected unit02 and unit05**.
