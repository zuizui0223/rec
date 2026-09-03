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

The v3.0 release also gives MD5s for the audio files. Use the released audio duration, not the final annotation time or detector output, to define the exposure denominator.

## 2. REC object

For sensor `s`, define a one-second master exposure grid before thresholding:

`Omega_s = { [0,1), [1,2), ..., duration_s }`.

The denominator therefore exists even when no detector event is emitted.

Within each window retain:

- expert truth: at least one released flight-call annotation in the window;
- full pre-gate detector score stream: maximum score in the window;
- gate evaluability: whether a score was available in the window;
- frozen threshold result `R`;
- for this replication only, `K = R`.

`K = R` is a deliberate restriction. BirdVox-full-night can test algorithmic gate censoring, but there is no separate archive-loss layer in this external replication.

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

## 4. Detector-score anti-leakage rule

The confirmatory held-out analysis requires a **continuous pre-threshold score stream whose model/gate construction did not use the held-out annotations**.

Acceptable examples:

1. out-of-fold scores where the model for sensor `s` was fit without sensor `s` truth;
2. an annotation-naive fixed signal detector frozen before BirdVox truth is opened;
3. another externally trained detector with documented non-use of BirdVox-full-night held-out truth.

Do **not** automatically treat the packaged BirdVoxDetect model as confirmatory held-out evidence merely because it is pretrained. BirdVoxDetect was developed using BirdVox data; a full-data pretrained checkpoint can leak the evaluation truth unless sensor-exclusion provenance is established.

BirdVoxDetect is still useful as an exploratory score source or if genuine out-of-fold score provenance is reconstructed. Its source exposes a continuous `confidence` HDF5 output with `--export-confidence`, which is preferable to thresholded checklist rows because the checklist itself is already gate-selected.

The normalized score CSV consumed by REC is:

```csv
sensor_id,time_seconds,score
02,0.025,12.3
02,0.075,10.8
...
```

A missing score does **not** become a negative window. It becomes `gate_evaluable=false`.

## 5. Build the gate-independent exposure grid

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

## 6. Frozen first-pass gates

For a detector confidence on a 0–100 scale, the first exploratory pair is:

- threshold `50`;
- threshold `70`.

The value 50 corresponds to the documented BirdVoxDetect default and 70 is a prespecified stricter comparison. If another score scale is used, thresholds must be frozen on development sensors and documented before held-out truth is opened.

Run:

```bash
python scripts/analyze_birdvox_exposure_grid.py \
  birdvox_exposure_grid.csv \
  --threshold 50 \
  --threshold 70 \
  --output birdvox_rec_results.json
```

Only rows marked `heldout` enter the reported H1–H4 summaries.

## 7. What the executable result tests

### REC-H1 — shadow existence

Primary event-conditioned quantity:

`a_R = P(R=0 | E=1)`.

Also report:

`q_shadow = P(E=1 | K=0)`.

A positive H1 requires at least one independently annotated flight-call window that the frozen gate does not enter.

### REC-H2 — structured selection

The first condition map is deliberately small:

- held-out sensor;
- early versus late half of the continuous night.

The current script reports sensor-specific event absorption. Grouped uncertainty is a later confirmatory extension; individual one-second windows must not be treated as independent ecological replicates.

### REC-H3 — ecological distortion

The frozen downstream endpoint is **one-second flight-call event-window prevalence**, not abundance or species richness.

Compare recorded versus expert-truth worlds using:

- sensor-specific prevalence error;
- sensor ranking (Spearman correlation where defined);
- late-minus-early prevalence contrast and its absolute error.

The claim is that record-entry selection can distort this prespecified acoustic migration-intensity proxy, not that the proxy is a complete ecological state variable.

### REC-H4 — gate semantics sensitivity

Apply both frozen gates to the same held-out pre-gate score stream and compare:

- event absorption;
- shadow contamination;
- downstream sensor-rate error.

This tests whether changing the gate changes the scientific record even though the underlying continuous audio/truth world is unchanged.

## 8. Promotion rule

Do not call the synthetic unit-test fixture a BirdVox result.

Promotion requires a committed real-data result artifact with:

1. Zenodo v3.0 file hashes verified;
2. frozen audio-duration manifest;
3. detector/score provenance proving held-out truth was not used to create held-out scores;
4. committed one-second exposure grid or deterministic recipe/hash;
5. H1/H2/H3/H4 held-out JSON;
6. grouped uncertainty at sensor/night-block level where the inferential claim requires it;
7. explicit statement that same-audio expert truth does not identify microphone-level missed calls.

Until then the BirdVox code is an **executable REC replication contract**, not empirical confirmation.
