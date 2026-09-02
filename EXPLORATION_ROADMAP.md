# REC verification and exploration roadmap

Status: active exploratory roadmap. No confirmatory outcome is implied.

## Workstream A — prior-art reproduction / physical sensor loss

### Dataset

Findlay et al. public `CT-Detection` repository.

### Questions

1. Can published trigger/registration results be reconstructed from released tables/code?
2. Re-express the closest quantities in REC notation without relabelling them as novel:
   - true animal pass as event-conditioned reference;
   - trigger failure as an `R=0 | E=1` analogue;
   - registration failure as a later entry-stage analogue.
3. Which covariates drive event-conditioned loss?
4. Which REC quantities are **not** identified because a full temporal master exposure universe is absent?

### Success criterion

A reproducible boundary analysis that shows exactly which parts of REC are already instantiated by prior camera work and which require a new exposure-ledger design.

## Workstream B — algorithmic shadow world on continuous audio

### Dataset

BirdVox-full-night.

### Design

1. freeze a time-grid `Omega` over continuous recordings;
2. protect at least one sensor/night partition from gate development;
3. construct or reuse a detector score without tuning on protected truth;
4. freeze multiple gate rules/thresholds on development data;
5. overlay detector entry `K/R` on the same `Omega`;
6. use expert call timestamps as detector-independent event truth within the recorded audio;
7. estimate `q_shadow`, `a_K`, `q_B/a_R` where definitions apply;
8. test whether gate selection varies by frozen measurable conditions such as sensor, time, local signal support/background level;
9. compare downstream call-rate/time-block estimates against expert truth.

### Critical boundary

This experiment cannot establish calls missed by the microphone itself. It tests censoring **after physical acquisition but before algorithmic record entry**.

## Workstream C — prospective System A full chain

Interaction camera with independent reference channel and master exposure clock.

Target chain:

`Omega -> physical acquisition -> pre-gate evidence -> R -> K -> B/T/N/U -> binary -> ecological inference`.

This is the only current workstream intended to support the full REC+TNOA two-stage decomposition.

## Workstream D — identifiability / design controls

Before field confirmation, construct a transparent design analysis showing:

1. event-log-only records do not empirically enumerate `K=0` exposures;
2. adding an external exposure ledger makes the shadow sampling frame explicit;
3. probability sampling of `K=0`/`R=0` windows permits design-weighted estimation of contamination quantities under the declared reference-truth assumptions;
4. finite reference-sampling burden creates an information-cost tradeoff.

Do not oversell this as a new missing-data theorem. Its purpose is to make the measurement design auditable and to derive the exact assumptions under which REC field estimands are identified.

## Priority order

1. merge the exposure-ledger contract and weighted shadow analyzer;
2. reproduce Findlay released results/quantities;
3. prototype BirdVox exposure-grid experiment;
4. use those results to simplify/freeze prospective System-A field protocol;
5. preregister the confirmatory System-A analysis;
6. collect held-out System-A groups;
7. only then evaluate the full REC-H3/H5/H6 claim stack.
