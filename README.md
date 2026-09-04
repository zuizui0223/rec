# REC — Record-Entry Censoring

**REC studies the shadow side of TNOA: ecological exposures and events that existed before downstream analysis but never became usable records.**

Status: **active Paper-2 research program; external real-data mechanism validation and retrospective correction achieved, prospective same-system field validation still open.**

The frozen MEE Paper 1 remains in `zuizui0223/tnoa`. This repository owns forward validation/generalization work.

## Current evidence snapshot

REC is no longer only a design/exploration scaffold.

Two distinct real observation systems support the central pre-entry mechanism, and one of them now also supplies a retrospective recovery test:

1. **BirdVox-full-night — continuous algorithmic exposure experiment.** A gate-independent one-second `Omega` is defined from continuous audio. A frozen annotation-naive gate produced real shadow events, condition-dependent operating meaning and severe distortion of a prespecified temporal flight-call contrast. Unit10 was retained as a pilot; protected units 02/05 independently reproduced the upstream-omission result. The frozen score itself generalized poorly, so the extreme miss-rate magnitude is an adverse result, not a claim about competent bird detectors. Even an oracle-perfect downstream semantic stage could not reconstruct truth-positive windows that never entered.
2. **Findlay camera traps — external physical-sensor process validation and retrospective recovery.** Among 881 independently observed fox/badger passes, `a_R=P(no trigger|pass)=0.514188`; bounded final non-capture is about `0.800227–0.802497`. Loss varies strongly with biological/observation conditions, and true-pass species composition shifts at trigger and capture. In the separate otter wet/dry table, wet passes have higher trigger loss than dry passes in all three camera types. A leave-one-camera-type-out IPW correction learned entry probabilities only from the other camera types and improved held-out wet-composition error in `3/3` cameras; mean absolute error fell from `0.115982` to `0.059258` (`48.91%` relative reduction).

Current claim status:

- **REC-H1 shadow existence:** positive in two real observation modalities;
- **REC-H2 structured selection:** positive descriptive evidence across temporal, biological and sensor-condition axes;
- **REC-H3 ecological distortion:** positive for a temporal ecological contrast in BirdVox and composition endpoints in camera traps;
- **REC-H4 gate semantics sensitivity:** positive in BirdVox;
- **REC-H5 correction/recoverability:** **positive retrospective cross-camera partial-recovery evidence** in Findlay; protected prospective H5 remains open;
- **REC-H6 REC→TNOA decomposition:** same-system PolliPi architecture is now pinned and guarded by an executable readiness gate, but the current field calibration is intentionally unfrozen and held-out scoring remains forbidden; empirical H6 remains open.

Canonical result summaries:

- `results/BIRDVOX_UNIT10_SMOKE_RESULT.md` — pilot/mechanism unit;
- `results/BIRDVOX_PROTECTED_02_05_RESULT.md` — protected independent BirdVox replication;
- `results/FINDLAY_CAMERA_TRAP_RESULT.md` — camera-trap external validation;
- `results/FINDLAY_H5_CORRECTION_RESULT.md` — retrospective cross-camera correction;
- `results/H6_POLLIPI_READINESS_AUDIT.md` — same-system H6 readiness boundary.

## Core distinction

TNOA starts **after an observation has entered the record** and asks which process distinctions should be preserved.

REC starts **before record entry** and asks which exposures/events never became records, why, and whether that selection changes ecological inference.

```text
latent biological process
        |
        v
master exposure universe Omega
        |
        v
pre-gate evidence S
        |
        v
registration gate R
        |
        v
archive / record entry K        <- REC shadow side
        |
        v
B / T / N / U                   <- TNOA semantic side
        |
        v
target / not-target
        |
        v
downstream ecological inference
```

The phrase **shadow world** is project shorthand. REC does not claim access to a fundamentally unobservable biological world. Its empirical target is:

> **unseen by the tested record-entry system, but recoverable under an independent exposure/reference design.**

## Foundational rule

> **Define exposure before defining non-detection.**

A missing event-log row is not a biological baseline state. To study what did not enter the record, REC first defines a gate-independent master exposure universe `Omega`.

If the event log itself defines the denominator, exposures that never triggered/entered are absent by construction and `P(event | no record)` is not empirically identified from that log alone.

## Identifiability boundary

REC distinguishes three levels that must not be conflated:

1. an **event log** shows only entered rows and cannot identify the biological composition of rows that never existed;
2. a **master exposure ledger** makes non-entry enumerable but still does not reveal biological truth inside the shadow set;
3. **probability-sampled independent reference truth** can identify shadow composition over the audited exposure universe, while unresolved reference truth remains unresolved or bounded.

The formal note is `IDENTIFIABILITY_BOUNDARY.md`.

A deterministic witness is executable with:

```bash
python scripts/demonstrate_eventlog_nonidentifiability.py --pretty
```

It constructs multiple shadow-world completions with **the same observed event log** but different `q_shadow`, demonstrating why event-log-only shadow prevalence is not identified.

The real-data program follows the same discipline. BirdVox has an enumerable continuous-time denominator and can identify `q_shadow` inside recorded audio. Findlay camera-trap tables are conditioned on independently observed animal passes, so they identify event-conditioned `a_R/a_K` but intentionally do not report a continuous-time `q_shadow`.

## Paper-2 chapter architecture

### Chapter 1 — post-entry decision coarsening

Question:

`B/T/N/U -> target/not-target`

How much ecological information is lost when an already entered, process-resolved observation record is coarsened?

Primary design: `PREREGISTRATION_DRAFT.md`.

### Chapter 2 — pre-entry threshold / registration censoring

Question:

`event -> evidence -> gate -> registered B/deviation`

A registered baseline can contain both true no-event windows and real events that failed the registered-deviation gate.

Primary document: `CHAPTER2_THRESHOLD_CENSORING.md`.

Key quantities:

- `q_B = P(E=1 | R=0)` — event contamination of logical registered baseline;
- `a_R = P(R=0 | E=1)` — event absorption by the gate;
- `q_shadow = P(E=1 | K=0)` — event contamination of the non-entered record set when `K` is observable from a master exposure ledger.

### Full REC question

> Does condition-dependent record-entry selection, followed by later semantic coarsening, change real ecological estimands, site rankings or effect estimates relative to independent truth?

## Hypotheses

The recovered hypothesis ladder is in `HYPOTHESIS_RECOVERY.md`.

Main targets:

1. **REC-H1 — shadow existence:** independently verified events occur in baseline/non-entered exposures;
2. **REC-H2 — structured selection:** entry/absorption varies across frozen measurement conditions;
3. **REC-H3 — ecological distortion:** differential entry changes a prespecified ecological estimand or contrast;
4. **REC-H4 — gate semantics sensitivity:** different frozen gates create measurably different recorded worlds;
5. **REC-H5 — exposure-ledger recoverability:** a gate-independent denominator plus independent reference information can diagnose and, where transport assumptions are defensible, partially correct entry loss that event-log-only workflows cannot diagnose from their own rows;
6. **REC-H6 — two-stage decomposition:** where identifiable, separate upstream REC loss from later TNOA semantic coarsening on the same held-out evidence.

Null/adverse outcomes remain publishable and do not trigger post-hoc redesign. The BirdVox frozen score is itself an example: poor protected discrimination is retained as an adverse operating-rule result rather than tuned away after protected outcomes were opened.

## Novelty boundary

REC is **not** a claim to have discovered imperfect detection.

Already established literatures include:

- nondetection != absence and occupancy models with imperfect detection;
- condition-dependent detectability;
- camera-trap pass/trigger/registration/image-quality failure;
- double-observer/reference-camera approaches;
- false-positive/false-negative automated acoustic monitoring;
- classification-aware ecological inference;
- generic missing-data, censoring and preferential-sampling theory.

See `PRIOR_ART_BOUNDARY.md`.

The defensible REC target is narrower:

> **an auditable record-entry measurement contract linking an exposure universe, pre-gate evidence, versioned gate/entry rules, independent shadow truth, downstream ecological consequence and correction before later semantic coarsening.**

The real-data results support that mechanism across acoustic and camera-trap systems. They do not make the component false-negative patterns themselves novel.

## Data contracts

### Master exposure ledger

`EXPOSURE_LEDGER_SCHEMA.md`

Every exposure opportunity exists as a row independently of the tested record-entry rule. `record_entry_present` overlays the operational event log on that denominator.

Validate with:

```bash
python scripts/validate_exposure_ledger.py examples/exposure_ledger.csv \
  --window-table examples/chapter2_windows.csv
```

### Chapter-2 truth / gate audit

`TRUTH_AND_WINDOW_SCHEMA.md`

Contains pre-gate evidence, versioned gate provenance, independent event truth, probability-sampling provenance and derived absorbed/shadow-event flags.

Validate with:

```bash
python scripts/validate_chapter2_windows.py examples/chapter2_windows.csv
```

Missing reference truth is not converted to a negative state. The same rule is exercised in the Findlay external validation and H5 correction: missing `TRIGGER` or `CAPTURE` values remain process-specific unresolved mass and generate resolved-only estimates plus partial-identification/sensitivity bounds.

CI runs schema and analysis regression tests on every PR.

## Current empirical program

### System A / PolliPi — prospective same-system interaction camera

Goal: complete the full prospective chain from gate-independent exposure clock/reference channel through physical/algorithmic entry to field-calibrated TNOA representation, binary coarsening and downstream ecology.

PolliPi already provides real-camera Phase-A T/N/O shadow logging, separate operational capture records and a blinded Phase-B independent-truth annotation contract. REC now pins this as the primary H6 same-system candidate in `H6_SAME_SYSTEM_CONTRACT.md`.

Current blocker: the PolliPi field-calibration manifest is deliberately `unfrozen_predata`, with null target/nuisance/observability decision criteria and `heldout_scoring_allowed=false`. `scripts/check_h6_readiness.py` therefore correctly blocks H6 held-out scoring.

Required next steps:

- collect fixed-interval Phase-A probe logs plus synchronized independent reference truth;
- finish development/calibration annotation under the grouped split;
- freeze target, nuisance and observability field criteria without opening held-out groups;
- version and join REC `Omega/A/R/K` rows to the same probes;
- freeze one ecological endpoint and target/not-target coarsening;
- enable held-out scoring in a new frozen field-calibration manifest;
- score untouched held-out groups once and run the four-stage H6 decomposition.

Phase-0 REC work is tracked in issue #3. A dedicated H6 execution issue should own the field-calibration-to-heldout transition.

### External physical-sensor validation — Findlay CT-Detection

**Completed external H1/H2/H3 validation plus retrospective H5 recovery.**

The public Findlay et al. camera/CCTV data provide true animal passes followed by trigger and registration/capture outcomes. REC maps these onto event-conditioned `R/K` estimands without pretending that the tables provide a complete temporal exposure denominator.

Key validation result: substantial pre-entry loss is accompanied by strong condition dependence and measurable composition shifts in the recorded world. Wet-pass underrepresentation repeats across all three otter camera types.

H5 result: leave-one-camera-type-out self-normalized IPW estimated wet/dry trigger propensities from the other two camera types only. Held-out wet-composition error improved in all three cameras, and mean absolute error fell by `48.91%`. This is retrospective partial-recovery evidence, not a protected confirmatory correction trial.

See:

- `scripts/analyze_findlay_ct_shadow.py`;
- `results/findlay_camera_trap_real_data_v1.json`;
- `results/FINDLAY_CAMERA_TRAP_RESULT.md`;
- `H5_CORRECTION_PLAN.md`;
- `scripts/analyze_findlay_h5_correction.py`;
- `results/findlay_h5_correction_v1.json`;
- `results/FINDLAY_H5_CORRECTION_RESULT.md`.

### External algorithmic REC replication — BirdVox-full-night

**Completed pilot plus protected replication for the frozen annotation-naive gate.**

BirdVox-full-night supplies continuous audio from six sensors, roughly 62 hours of enumerable time and 35,402 expert flight-call annotations. `Omega` is defined from continuous audio duration before gate evaluation.

Unit10 was inspected first and is retained as a pilot/mechanism unit. Units 02/05 were then protected. The protected result is positive but adverse: the frozen score generalized poorly and absorbed nearly all truth-positive windows. Crucially, the prespecified temporal ecological contrast was almost erased even after granting an oracle-perfect downstream semantic stage. This supports the upstream-omission mechanism but does not imply that competent bird detectors generally have the same miss rate.

Boundary: expert truth is based on the same recorded audio, so this tests **algorithmic/digital entry censoring**, not calls physically absent from the microphone signal.

See:

- `BIRDVOX_REPLICATION.md`;
- `results/BIRDVOX_UNIT10_SMOKE_RESULT.md`;
- `results/BIRDVOX_PROTECTED_02_05_RESULT.md`.

### Later broad acoustic candidate — WABAD

Potential multi-site/biome generalization after its released-recording selection provenance is audited. A stronger provenance-safe recording rule on a new protected system remains useful if REC needs representative-performance evidence beyond the deliberately adverse BirdVox gate.

### Snapshot Serengeti

Retain primarily for **post-entry Chapter-1/TNOA replication**. An event-triggered image archive cannot reveal animals that never triggered a camera without an external exposure/reference mechanism.

See `SYSTEM_B_CANDIDATES.md`.

## Promotion ladder

The evidence ladder is:

1. gate-independent exposure denominator;
2. independently measured shadow events;
3. condition-dependent entry structure;
4. downstream ecological consequence;
5. correction/redesign evaluation;
6. upstream REC versus downstream TNOA decomposition on the same held-out evidence;
7. independent sensor/system replication.

**Current state:** steps 1–4 are empirically supported in the external program, and step 7 has been reached across acoustic and camera-trap modalities. Step 5 now has positive retrospective cross-camera partial-recovery evidence, but prospective confirmatory recovery remains open. Step 6 has an oracle-downstream impossibility bridge in BirdVox and an implementation-ready PolliPi same-system contract, but no licensed held-out field decomposition yet.

The next major promotion is therefore not another demonstration that events can be missed. It is the prospective PolliPi/System-A transition from shadow logging and independent truth to a frozen field calibration, untouched held-out scoring and four-stage REC→TNOA decomposition.

## Repository map

- `REC_FRAMEWORK.md` — formal shadow-side architecture;
- `REC_STATE_MODEL.md` — recorded, reference-observable shadow and reference-unresolved worlds;
- `REC_POSITIONING_NOTE.md` — short TNOA/REC conceptual pairing;
- `IDENTIFIABILITY_BOUNDARY.md` — what event logs, exposure ledgers and reference truth can/cannot identify;
- `HYPOTHESIS_RECOVERY.md` — recovered hypotheses, falsifiers and prior-art status;
- `CHAPTER2_THRESHOLD_CENSORING.md` — gate-censoring chapter;
- `PREREGISTRATION_DRAFT.md` — prospective confirmatory freeze plan;
- `TRUTH_AND_WINDOW_SCHEMA.md` — truth/gate audit table contract;
- `EXPOSURE_LEDGER_SCHEMA.md` — master exposure / record-entry contract;
- `PRIOR_ART_BOUNDARY.md` — nearest-neighbour audit;
- `SYSTEM_B_CANDIDATES.md` — external replication suitability;
- `BIRDVOX_REPLICATION.md` — frozen acoustic replication contract and boundaries;
- `H5_CORRECTION_PLAN.md` — retrospective cross-camera correction freeze;
- `H6_SAME_SYSTEM_CONTRACT.md` — PolliPi same-system four-stage H6 contract;
- `results/` — committed real-data evidence, correction and readiness summaries;
- `scripts/` and `tests/` — executable validation, real-data analyses, recovery tests and readiness gates.

## Hard boundary with TNOA Paper 1

REC development does not alter Paper-1 frozen synthetic results, D1-D5 status, numerical claims or MEE submission package in `zuizui0223/tnoa`.
