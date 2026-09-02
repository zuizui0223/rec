# REC — Record-Entry Censoring

**REC studies the shadow side of TNOA: ecological exposures and events that existed before downstream analysis but never became usable records.**

Status: active Paper-2 research program; design and exploration stage; confirmatory claims not yet preregistered or field-validated.

The frozen MEE Paper 1 remains in `zuizui0223/tnoa`. This repository owns forward field validation/generalization work.

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

The current recovered hypothesis ladder is in `HYPOTHESIS_RECOVERY.md`.

Main confirmatory targets:

1. **REC-H1 — shadow existence:** independently verified events occur in baseline/non-entered exposures;
2. **REC-H2 — structured selection:** entry/absorption varies across frozen measurement conditions;
3. **REC-H3 — ecological distortion:** differential entry changes a prespecified ecological estimand or contrast;
4. **REC-H4 — gate semantics sensitivity:** different frozen gates create measurably different recorded worlds;
5. **REC-H5 — exposure-ledger recoverability:** a gate-independent denominator plus probability-sampled truth can diagnose/recover entry loss that event-log-only workflows cannot diagnose from their own rows;
6. **REC-H6 — two-stage decomposition:** where identifiable, separate upstream REC loss from later TNOA semantic coarsening on the same held-out evidence.

Null/adverse outcomes remain publishable and do not trigger post-hoc redesign.

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

> **an auditable record-entry measurement contract linking an exposure universe, pre-gate evidence, versioned gate/entry rules, probability-sampled shadow truth and downstream ecological consequence before later semantic coarsening.**

That contribution must be earned empirically.

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

CI runs all schema regression tests on every PR.

## Current empirical program

### System A — prospective interaction camera

Goal: complete chain from gate-independent exposure clock/reference channel through physical/algorithmic entry to B/T/N/U and downstream ecology.

Required:

- independent master exposure grid;
- synchronized reference truth;
- pre-gate evidence retained for all auditable exposures;
- versioned gate and archive-entry policy;
- deliberate truth sampling of registered B and non-entered exposures;
- grouped development/held-out split;
- one prespecified ecological estimand/contrast.

Phase-0 work is tracked in issues #1 and #3.

### External physical-sensor neighbour — Findlay CT-Detection

The public Findlay et al. camera/CCTV datasets are the closest prior/replication system for event-conditioned trigger and registration loss. They are useful for `P(no trigger | true pass)`-type quantities, but do not by themselves provide a complete fixed temporal exposure denominator for `P(event | no record)`.

### External algorithmic REC replication — BirdVox-full-night

Current leading public candidate for a complete algorithmic exposure-denominator experiment:

- continuous full-night audio from six sensors;
- roughly 62 hours of enumerable time;
- 35,402 expert flight-call annotations;
- detector gates can be applied after `Omega` is frozen.

Boundary: expert truth is based on the same recorded audio, so this tests **algorithmic/digital entry censoring**, not calls physically absent from the microphone signal.

### Later broad acoustic candidate — WABAD

Potential multi-site/biome generalization after its released-recording selection provenance is audited.

### Snapshot Serengeti

Retain primarily for **post-entry Chapter-1/TNOA replication**. An event-triggered image archive cannot reveal animals that never triggered a camera without an external exposure/reference mechanism.

See `SYSTEM_B_CANDIDATES.md`.

## Promotion ladder

An above-MEE paper should not be promoted merely because REC has a compelling diagram.

The evidence should progress through:

1. gate-independent exposure denominator;
2. independently measured shadow events;
3. condition-dependent entry structure;
4. downstream ecological consequence;
5. frozen correction/redesign evaluation;
6. upstream REC versus downstream TNOA decomposition where identifiable;
7. independent sensor/system replication.

If only missed events are demonstrated, the result is a measurement-validation study rather than the full REC claim.

## Repository map

- `REC_FRAMEWORK.md` — formal shadow-side architecture;
- `REC_POSITIONING_NOTE.md` — short TNOA/REC conceptual pairing;
- `HYPOTHESIS_RECOVERY.md` — recovered hypotheses, falsifiers and prior-art status;
- `CHAPTER2_THRESHOLD_CENSORING.md` — gate-censoring chapter;
- `PREREGISTRATION_DRAFT.md` — confirmatory freeze plan;
- `TRUTH_AND_WINDOW_SCHEMA.md` — truth/gate audit table contract;
- `EXPOSURE_LEDGER_SCHEMA.md` — master exposure / record-entry contract;
- `PRIOR_ART_BOUNDARY.md` — nearest-neighbour audit;
- `SYSTEM_B_CANDIDATES.md` — external replication suitability;
- `scripts/` and `tests/` — executable fail-closed validation.

## Hard boundary with TNOA Paper 1

REC development does not alter Paper-1 frozen synthetic results, D1-D5 status, numerical claims or MEE submission package in `zuizui0223/tnoa`.
