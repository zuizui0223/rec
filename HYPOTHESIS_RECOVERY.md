# REC hypothesis recovery — from TNOA to the record-entry shadow world

Status: **working hypothesis ledger; not preregistered**.

This document recovers the hypotheses that motivate REC, distinguishes inherited principles from genuinely new empirical questions, and marks which claims are already established by prior literature.

## 1. World layers

REC does **not** claim to observe the fundamentally unobservable biological world. It separates five layers:

1. **latent biological world** — the full process that exists whether or not any sensor measures it; never exhaustively observable;
2. **master exposure universe `Omega`** — externally defined observation opportunities, independent of the tested gate;
3. **reference-observable shadow world** — a probability sample or protected subset of `Omega` for which independent reference truth can resolve whether an event occurred;
4. **primary recorded world** — exposures that pass registration/archive rules and enter the operational record;
5. **semantic/downstream world** — entered observations converted to B/T/N/U and later coarsened records.

REC's empirical target is layer 3 versus layer 4: **unrecorded by the tested system, but recoverable by an independent reference design**.

Preferred wording:

> unseen by the tested record-entry system, not unobservable to science.

## 2. Hypothesis lineage from TNOA

### TNOA principle P1 — low support is not absence

Recovered REC principle:

**REC-R0 — record silence is not biological no-event.**

`K=0`, `R=0`, missing event-log row, registered baseline and independently supported `E=0` are distinct states.

This is a design rule, not a novelty claim. Occupancy theory already establishes nondetection != absence.

### TNOA principle P2 — observability is a separate measurement object

Recovered hypothesis:

**REC-H2 — record entry is condition dependent.**

Among independently verified events, `P(R=0 | E=1, X)` and/or `P(K=0 | E=1, X)` vary with predeclared measurement conditions such as occlusion, scale/distance, illumination, masking, temporal support or hardware state.

This direction is already supported in camera-trap literature; REC must estimate the condition map in its own systems rather than claim discovery of condition-dependent detection.

### TNOA principle P3 — raw thresholds do not carry invariant operating meaning

Recovered hypothesis:

**REC-H4 — different frozen gates create different recorded worlds.**

For the same held-out pre-gate evidence and independent truth, two fixed gate rules can yield different baseline contamination, event absorption, record-entry burden and downstream ecological estimates even when the evidence ranking is unchanged.

Threshold/FN tradeoffs are known in automated monitoring. REC's test is the full consequence on record-entry selection and downstream ecology.

### TNOA principle P4 — information discarded upstream cannot be reconstructed downstream without extra assumptions or measurements

Recovered hypotheses:

**REC-H1 — shadow existence.** Independently verified biological events occur in `R=0` and/or `K=0` exposures.

**REC-H5 — event-log-only non-identification.** Without a gate-independent exposure denominator or an explicit sampling model for non-entered windows, event-log data alone cannot empirically identify `P(E=1 | K=0)`.

H1 is an empirical quantity, not expected to be universally positive. H5 is primarily a design/identification statement; the empirical program demonstrates its practical consequence rather than claiming a new missing-data theorem.

### TNOA D5 lesson — category labels do not create semantic value by themselves

Recovered REC principle:

**REC-R1 — validate mechanisms, not names.**

REC does not gain credibility by naming more hidden states. A state enters confirmatory analysis only if its inclusion mechanism, denominator and truth relation are independently measurable or explicitly modeled.

## 3. Core confirmatory hypotheses

### REC-H1 — shadow existence

For held-out exposure windows sampled independently of the tested entry rule,

`q_shadow = P(E=1 | K=0, truth resolved)`

and/or

`q_B = P(E=1 | R=0, truth resolved)`

are estimated with uncertainty.

**Falsifier:** no reference-positive events are found in a sufficiently informative non-entered/baseline sample, or the estimated contamination is practically negligible.

**Prior-art status:** imperfect detection and missed trigger events are established; not a novelty claim.

### REC-H2 — structured selection

Event absorption/non-entry varies across a small frozen set of independently measured conditions.

Primary event-conditioned quantities:

`a_R(x) = P(R=0 | E=1, X=x)`

`a_K(x) = P(K=0 | E=1, X=x)`.

**Falsifier:** differences across frozen strata are negligible or unstable at the independent-unit level.

**Prior-art status:** condition-dependent detectability is established in camera and acoustic monitoring; REC must map its own mechanism.

### REC-H3 — ecological distortion

For one prespecified ecological contrast or unit-level prevalence estimand, the event-log-only workflow is farther from independent reference truth when entry propensity covaries with biological state or ecological/measurement covariates.

The target is distance to reference truth, not a required sign reversal.

**Falsifier:** shadow selection has negligible influence on the frozen ecological estimand/contrast.

**Prior-art status:** observation-process heterogeneity can bias ecological relationships is established. REC's stronger test is to attribute a measurable share of the distortion to the versioned record-entry mechanism itself.

### REC-H4 — gate semantics sensitivity

Two frozen gates applied to the same held-out evidence produce different `q_B`, `a_R`, record-entry burden and downstream error.

**Falsifier:** alternative gates produce practically equivalent selection and ecological consequences in the tested operating range.

**Prior-art status:** threshold tradeoffs are established; not a first-principles novelty claim.

### REC-H5 — exposure-ledger recoverability

A workflow that begins from `Omega`, retains entry provenance and samples the shadow set with known inclusion probabilities can estimate target event prevalence and entry loss against independent truth with valid uncertainty, whereas an event-log-only workflow cannot diagnose shadow contamination from its own rows.

**Falsifier:** the exposure-ledger design does not improve diagnosis/recovery relative to the frozen comparator, or required truth/entry assumptions fail.

**Novelty candidate:** the auditable architecture and empirical demonstration are stronger candidates than imperfect detection itself.

### REC-H6 — two-stage information loss

On the same held-out field evidence, decompose total downstream discrepancy into at least:

1. upstream record-entry/gate loss (REC);
2. later semantic coarsening loss (TNOA Chapter 1), where the decomposition is identifiable under the frozen design.

**Falsifier:** the stages cannot be separately identified with available measurements, in which case report only the identifiable total/partial effects.

**Novelty candidate:** a single empirical pipeline that audits both pre-entry selection and post-entry semantic coarsening is a central above-MEE target.

## 4. What has already been verified by prior literature

The following are **background facts, not REC discoveries**:

- nondetection does not imply absence when detection probability is below one;
- environmental/animal/sensor factors affect detection probability;
- camera-trap pass, trigger, registration and image-quality failures can be separated using independent reference video;
- camera traps can miss passing animals, sometimes substantially;
- automated acoustic detectors generate event-level false negatives and false positives that can affect occupancy inference;
- stricter detection thresholds can trade lower false positives for higher false negatives;
- imperfect observation can alter apparent ecological thresholds/relationships;
- preferential/non-random sampling can bias ecological status and trend estimates.

REC must cite these literatures and position itself downstream of them.

## 5. Remaining empirical gap REC should target

The strongest unresolved program is not "do sensors miss events?" but:

> **Can an automated ecological study make the record-entry selection mechanism itself auditable from a gate-independent exposure denominator, quantify which biological events never became records, and trace that selection into downstream ecological conclusions before later semantic coarsening?**

A strong result requires the chain:

`Omega -> E/S -> R -> K -> D -> Y -> ecological inference`

with independent truth and frozen provenance at the stages being claimed.

## 6. System implications

### System A — prospective interaction camera

Best for the full REC+TNOA chain because an independent reference stream and a master exposure clock can be designed prospectively.

### System B — continuous passive acoustics preferred for REC

For upstream REC replication, a continuous recording dataset is preferable to a purely event-triggered image archive because the exposure denominator exists independently of detector output.

Current leading candidate: **BirdVox-full-night** — continuous full-night recordings from six sensors with expert event timestamps. It can support an algorithmic record-entry gate experiment on a fully enumerable time grid.

Important boundary: human annotations on the same continuous audio are independent of the tested detector but do not recover biological calls that the microphone itself failed to sense. This validates **algorithmic/gate record-entry censoring**, not physical sensor acquisition completeness.

WABAD is a broader future acoustic replication candidate with expert species-level time-frequency annotations across many sites and biomes.

### Snapshot Serengeti

Still useful for Chapter-1 semantic/classification replication, but weak as the primary REC-H1/H5 dataset because an event-triggered image archive does not enumerate animals that never triggered the camera. Do not use it to estimate `q_shadow` without an external exposure/reference mechanism.

## 7. Promotion logic

REC should earn claims in this order:

1. **denominator:** `Omega` exists independently of gate output;
2. **existence:** shadow events are measured against independent truth;
3. **structure:** entry propensity varies under frozen conditions;
4. **consequence:** ecological inference changes relative to truth;
5. **recoverability:** exposure-ledger/uncertainty-aware workflow improves diagnosis or inference;
6. **decomposition:** upstream REC and downstream TNOA losses can be separated;
7. **generality:** at least one independent sensor/system replication.

Failure at any level constrains the next claim rather than triggering post-hoc redesign.
