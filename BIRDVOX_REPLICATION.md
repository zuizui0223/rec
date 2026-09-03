# BirdVox-full-night REC replication

Status: **executable replication scaffold; real-data result not yet claimed**.

This module is the shortest current path from the REC theory/contract to a public continuous-recording experiment. It targets **algorithmic record-entry censoring after audio acquisition**. It does not claim to recover calls that were physically absent from the microphone signal.

## 1. Frozen public dataset

Use **BirdVox-full-night v3.0**, Zenodo record `1205569`, DOI `10.5281/zenodo.1205569`.

The released dataset contains six continuous mono recordings from sensors `01, 02, 03, 05, 07, 10`, about 62 hours total, with 35,402 expert flight-call annotations. The v3.0 release is CC BY 4.0.

Reference record:

- https://zenodo.org/records/1205569

Pin the six annotation CSV files before analysis:

| file | MD5 |
| --- | --- |
| `BirdVox-full-night_csv-annotations_unit01.csv` | `a8955d08b24a41496be7b91499f18f97` |
| `BirdVox-full-night_csv-annotations_unit02.csv` | `831f62043b2c404cedb7004032905408` |
| `BirdVox-full-night_csv-annotations_unit03.csv` | `1369f241442550601280eec013add2cd` |
| `BirdVox-full-night_csv-annotations_unit05.csv` | `b1aeb87763990856d92d6db162a8c5a0` |
| `BirdVox-full-night_csv-annotations_unit07.csv` | `b14c409077c86ada07a7c22a4f7749bb` |
| `BirdVox-full-night_csv-annotations_unit10.csv` | `bfe4a6e45731f468cc6dbea0a7968c1c` |

The v3.0 release also gives MD5s for the audio files. Use the released audio duration or duration read directly from the FLAC files, not the final annotation time or detector output, to define the exposure denominator.

## 2. REC object

For sensor `s`, define a one-second master exposure grid before thresholding:

`Omega_s = { [0,1), [1,2), ..., duration_s }`.

The denominator therefore exists even when no detector event is emitted.

Within each window retain:

- expert truth: at least one released flight-call annotation in the window;
- full pre-gate score stream: maximum score in the window;
- gate evaluability: whether a score was available in the window;
- frozen threshold result `R`, defined only when the gate is evaluable;
- operational record entry `K`, with `K=1` only when the gate is evaluable and passes.

For this external replication, a gate-evaluable failure is `R=0, K=0`; a gate-unevaluable window has `R` undefined and `K=0`. There is no separate archive-loss stage. This distinction is retained so score/acquisition failure is not silently counted as threshold absorption.

## 3. Frozen development / held-out split

Freeze the alternating sorted-sensor split before reading detector outcomes:

- **development:** `01, 03, 07`
- **held-out:** `02, 05, 10`

This split is an arbitrary provenance rule, not an optimized balance. Do not move sensors after viewing truth/gate results.

A runtime manifest must contain:

```csv
sensor_id,duration_seconds,split
01,<audio duration>,development
02,<audio duration>,heldout
03,<audio duration>,development
05,<audio duration>,heldout
07,<audio duration>,development
10,<audio duration>,heldout
```

Durations must come from the continuous audio files or trusted audio metadata. The annotation tables and detector events must not define duration.

## 4. Primary annotation-naive score path

The primary self-run gate uses `scripts/score_birdvox_band_energy.py`. It never reads the BirdVox annotations.

For each one-second audio block it computes a fixed spectral-energy contrast:

- target band: `2–10 kHz`;
- reference band: `0.2–2 kHz`;
- raw score: `10 log10(target power / reference power)`;
- operational score: per-sensor robust z score using median/MAD, with standard-deviation fallback only when MAD is degenerate.

The frequency bands and robust scaling are fixed measurement rules, not fit to BirdVox truth. This score is intentionally simple: its purpose is to create a reproducible, annotation-naive gate whose missed-event structure can be audited, not to claim state-of-the-art flight-call detection.

Generate both the continuous score stream and the audio-duration manifest directly from the six FLAC files:

```bash
python scripts/score_birdvox_band_energy.py \
  BirdVox-full-night_flac-audio_unit01.flac \
  BirdVox-full-night_flac-audio_unit02.flac \
  BirdVox-full-night_flac-audio_unit03.flac \
  BirdVox-full-night_flac-audio_unit05.flac \
  BirdVox-full-night_flac-audio_unit07.flac \
  BirdVox-full-night_flac-audio_unit10.flac \
  --window-seconds 1 \
  --scores-output birdvox_scores.csv \
  --manifest-output birdvox_manifest.csv
```

The normalized output includes:

```csv
sensor_id,time_seconds,score,raw_band_contrast_db,score_source
02,0.5,2.31,12.8,annotation-naive-band-energy-v1
...
```

A missing score does **not** become a negative window. It becomes `gate_evaluable=false` after the exposure grid is built.

## 5. Alternative detector-score anti-leakage rule

Any alternative detector used for confirmatory held-out analysis must supply a **continuous pre-threshold score stream whose model/gate construction did not use the held-out annotations**.

Acceptable examples:

1. out-of-fold scores where the model for sensor `s` was fit without sensor `s` truth;
2. another annotation-naive fixed signal detector frozen before BirdVox truth is opened;
3. an externally trained detector with documented non-use of BirdVox-full-night held-out truth.

Do **not** automatically treat the packaged BirdVoxDetect model as confirmatory held-out evidence merely because it is pretrained. BirdVoxDetect was developed using BirdVox data; a full-data pretrained checkpoint can leak evaluation truth unless sensor-exclusion provenance is established.

BirdVoxDetect is still useful as an exploratory score source or if genuine out-of-fold score provenance is reconstructed. Its source exposes a continuous `confidence` HDF5 output with `--export-confidence`, which is preferable to thresholded checklist rows because the checklist itself is already gate-selected.

## 6. Build the gate-independent exposure grid

```bash
python scripts/build_birdvox_exposure_grid.py \
  birdvox_manifest.csv \
  birdvox_scores.csv \
  BirdVox-full-night_csv-annotations_unit01.csv \
  BirdVox-full-night_csv-annotations_unit02.csv \
  BirdVox-full-night_csv-annotations_unit03.csv \
  BirdVox-full-night_csv-annotations_unit05.csv \
  BirdVox-full-night_csv-annotations_unit07.csv \
  BirdVox-full-night_csv-annotations_unit10.csv \
  --window-seconds 1 \
  --output birdvox_exposure_grid.csv
```

The builder fails closed if an annotation/score lies outside the frozen audio duration. It preserves windows without scores as gate-unevaluable rather than silently removing them.

## 7. Frozen first-pass gates

For the primary annotation-naive robust-z score, freeze two gates before opening held-out truth:

- moderate anomaly gate: `z >= 2`;
- strict anomaly gate: `z >= 4`.

These are prespecified measurement gates, not development-optimized performance thresholds. Development sensors may be used to diagnose catastrophic scale/sign errors, but held-out thresholds must not be moved to rescue H1–H4.

Run:

```bash
python scripts/analyze_birdvox_exposure_grid.py \
  birdvox_exposure_grid.csv \
  --threshold 2 \
  --threshold 4 \
  --output birdvox_rec_results.json
```

If a BirdVoxDetect 0–100 confidence stream is used exploratorily, `50` is its documented default and `70` can be retained as a stricter comparison; those thresholds belong to that score scale and must not be mixed with the robust-z path.

Only rows marked `heldout` enter the reported H1–H4 summaries.

## 8. What the executable result tests

### REC-H1 — shadow existence and layer separation

Report separately:

`q_B = P(E=1 | R=0, gate evaluable)`

`a_R = P(R=0 | E=1, gate evaluable)`

`q_shadow = P(E=1 | K=0)`

`a_K = P(K=0 | E=1)`.

Gate-unevaluable true-event windows contribute to `a_K` but never to `a_R`. A positive REC shadow result requires independently annotated flight-call windows that fail to enter the frozen record; gate absorption is claimed only for the gate-evaluable subset.

### REC-H2 — structured selection

The first condition map is deliberately small:

- held-out sensor;
- early versus late half of the continuous night.

The analyzer reports both `a_R` and `a_K` by these conditions. These are descriptive held-out maps until grouped uncertainty is added; individual one-second windows must not be treated as independent ecological replicates.

### REC-H3 — ecological distortion

The frozen downstream endpoint is **one-second flight-call event-window prevalence**, not abundance or species richness.

Compare recorded versus expert-truth worlds using:

- sensor-specific prevalence error;
- sensor ranking (Spearman correlation where defined);
- late-minus-early prevalence contrast and its absolute error.

The claim is that record-entry selection can distort this prespecified acoustic migration-intensity proxy, not that the proxy is a complete ecological state variable.

### REC-H4 — gate semantics sensitivity

Apply both frozen gates to the same held-out pre-gate score stream and compare:

- gate absorption `a_R`;
- total event non-entry `a_K`;
- shadow contamination;
- downstream sensor-rate error.

This tests whether changing the gate changes the scientific record even though the underlying continuous audio/truth world is unchanged.

## 9. Promotion rule

Do not call the synthetic unit-test fixture a BirdVox result.

Promotion requires a committed real-data result artifact with:

1. Zenodo v3.0 file hashes verified;
2. frozen audio-duration manifest;
3. score provenance proving held-out truth was not used to create held-out scores;
4. committed one-second exposure grid or deterministic recipe/hash;
5. H1/H2/H3/H4 held-out JSON;
6. grouped uncertainty at sensor/night-block level where the inferential claim requires it;
7. explicit statement that same-audio expert truth does not identify microphone-level missed calls.

Until then the BirdVox code is an **executable REC replication contract**, not empirical confirmation.
