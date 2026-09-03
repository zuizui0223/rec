# BirdVox protected unit02/unit05 REC replication

Status: **protected independent replication of the frozen REC BirdVox analysis; system-specific proof of record-entry failure, not validation of a generally useful bird-call detector**.

The protected units were `02` and `05`. Unit `10` had already been inspected as a pilot and is excluded from the independent-replication claim. Before opening 02/05 outcomes, the following were frozen: one-second audio-defined `Omega`, annotation-naive 2–10 kHz versus 0.2–2 kHz band-energy score, per-sensor robust scaling, thresholds z=2/z=4, H1-H4 estimands, and the late-minus-early event-window prevalence endpoint.

The source workflow verified the released BirdVox-full-night v3.0 audio/annotation hashes and completed successfully. Machine-readable evidence is in `results/birdvox_protected_02_05_real_data_v1.json`.

## H1 — protected record shadow independently replicated

At z=2:

- **unit02:** 3,722 truth-positive windows / 39,302 total; only 6 truth-positive windows entered; `a_R = 0.998388`.
- **unit05:** 4,127 truth-positive windows / 39,357 total; only 3 truth-positive windows entered; `a_R = 0.999273`.
- protected pooled: 7,849 truth-positive windows / 78,659 total; only 9 truth-positive windows entered; `a_R = 0.998853`.

At z=4, both protected units produced zero entries and therefore `a_R = 1.0`.

Thus the existence of a large record-entry shadow is independently replicated on both protected units for the frozen gate.

## H3 — ecological temporal contrast is independently destroyed

### Unit02

Truth late-minus-early one-second event-window prevalence:

`+0.105135`.

At z=2:

- raw recorded contrast: `+0.000254`;
- perfect-downstream true-entry-only contrast: `+0.000102`;
- fraction of the truth contrast retained after perfect downstream semantics: `0.000968` (`0.097%`).

At z=4 both recorded and true-entry-only contrasts are zero.

### Unit05

Truth late-minus-early prevalence:

`+0.156471`.

At z=2:

- raw recorded contrast: `-0.010316` — direction reversed;
- perfect-downstream true-entry-only contrast: `-0.000152`;
- retained fraction: `-0.000974`.

At z=4 both recorded and true-entry-only contrasts are zero.

### Protected pooled 02+05

Truth contrast:

`+0.130820`.

At z=2:

- raw recorded contrast: `-0.005034`;
- perfect-downstream true-entry-only contrast: `-0.000025`;
- retained fraction: approximately `-0.000194`.

Therefore H3 independently replicates in the protected units: the frozen biological temporal gradient is almost entirely absent from the scientific record. The result persists after an oracle downstream stage removes every false entry, because that stage cannot recreate truth-positive windows that never entered.

## H4 — gate choice changes the recorded world, but does not rescue ecology

Moving from z=2 to z=4 changes unit02 from 49 total entries to 0 and unit05 from 203 entries to 0, while the continuous audio and expert truth are unchanged. The stricter gate therefore creates a measurably different recorded world but does not recover the ecological contrast; it eliminates the record entirely in both protected units.

This is a positive gate-semantics result but also an adverse result for the chosen gate family: neither frozen threshold is an adequate ecological recording rule on 02/05.

## H2 and the operating-meaning mechanism

The protected score itself is strongly condition/system dependent.

- unit02 score median shifts from `+0.687` early to `-0.624` late; AUC is `0.468` early and `0.348` late.
- unit05 score median shifts from `+0.677` early to `-0.452` late; AUC is `0.377` early and `0.351` late.

Because event absorption is already near a ceiling, a_R is not a useful calibrated H2 condition-effect endpoint in these units. The safe H2 conclusion is narrower: **the frozen score/gate has highly nonportable operating meaning across sensor/time conditions**, but the present protected run does not establish a general quantitative model of condition-dependent detection.

## What this does and does not prove

The protected result is stronger than the unit10 pilot in one respect: the central H1/H3 phenomenon was reproduced on two units whose outcomes were unopened when the analysis contract was frozen.

But the extreme magnitude also exposes an important limitation. The annotation-naive band-energy score has poor truth discrimination on unit02/unit05 (AUC below 0.5), so this experiment must not be sold as evidence that a competent acoustic detector necessarily loses 99–100% of events. It is evidence that:

1. an exposure-defined audit can reveal biological events that a frozen record-entry rule effectively erases;
2. aggregate recorded prevalence is insufficient to diagnose the composition of that loss;
3. a downstream semantic system, even if perfect, cannot recover upstream omissions;
4. the operating meaning of a frozen score/gate can fail catastrophically across observation conditions.

The next promotion step is therefore not to tune this gate on 02/05 after seeing the results. It is to preserve these protected results as-is and test REC with a stronger provenance-safe recording rule on a **new protected system or dataset**, or with a genuinely out-of-fold/external detector whose held-out truth was not used in model construction.
