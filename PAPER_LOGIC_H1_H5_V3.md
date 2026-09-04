# REC H1–H5 manuscript logic v3 — integrated evidence

Status: **canonical manuscript logic after H5 transport stress tests and the fox/badger second-endpoint recovery analysis.**

H6/PolliPi remains prospective follow-on work. The H1–H5 paper no longer depends on H6.

## Candidate title

**Auditing record-entry selection reveals ecological estimand distortion and context-dependent recovery**

Alternative:

**Ecological records are selected before analysis: estimand distortion, irreversibility and limits to correction transport**

## Central contribution

> **Ecological event tables are selected measurement products rather than neutral subsets of nature. Independent exposure/reference information makes pre-entry selection auditable, shows when that selection changes ecological estimands, and can support partial recovery—but the entry model itself has a calibration and transport domain that must be validated.**

This framing does not claim discovery of imperfect detection. Its contribution is to connect record-entry selection to the ecological estimand, downstream irreversibility, correction, and correction transport under one auditable measurement design.

## Four moves

### 1. Audit the world that the event table cannot contain

A final event log cannot identify the biological composition of exposures that never became rows. REC therefore starts from an independently defined exposure/reference world.

Evidence:

- deterministic event-log non-identifiability witness;
- BirdVox: continuous audio-defined time universe plus expert call truth;
- Findlay: CCTV-confirmed animal passes before camera-trap trigger/capture.

H1 is a prerequisite and empirical anchor, not the novelty headline.

### 2. Show that record entry changes ecology, not merely sample size

Findlay is the main empirical system.

#### Fox/badger

Among 881 CCTV-confirmed passes:

- no-trigger probability: `0.514188`;
- bounded final non-capture: approximately `0.800227–0.802497`;
- true badger proportion: `0.359818`;
- triggered badger proportion: `0.439252`;
- confirmed-capture badger proportion: `0.482759`.

Thus species composition changes before any downstream species-classification analysis begins.

#### Otter wet/dry

Wet passes have greater trigger loss than dry passes for every camera model/setting and are consequently underrepresented in every triggered record:

- A: truth `0.438017` -> recorded `0.270270`;
- BS: `0.459821 -> 0.378788`;
- BV: `0.445833 -> 0.346667`.

This is the central H2→H3 chain:

`biological/observation state -> entry probability -> changed ecological composition`.

Do not separate H2 and H3 into two disconnected lists of positive tests.

### 3. Show that omitted rows cannot be repaired downstream

BirdVox is a protected cross-modality stress test, not a detector-performance benchmark.

Protected pooled units 02/05:

- truth late-minus-early event-window prevalence contrast: `+0.130820`;
- oracle true-entry-only contrast at z=2: approximately `-0.000025`.

The frozen gate itself discriminates poorly and that adverse result remains explicit. The useful inference is narrower:

> A perfect downstream semantic stage can remove false entered rows but cannot reconstruct true rows removed upstream.

This establishes the practical REC→TNOA boundary without waiting for same-system H6.

### 4. Recovery exists, but transport is part of the problem

H5 should now be presented as a hierarchy of increasingly difficult transport tests rather than one positive correction claim.

#### 4.1 Matched-context camera holdout — strong positive

Otter wet/dry, leave one camera model/setting out while learning wet/dry entry propensities from the other colocated camera streams:

- raw MAE: `0.115982`;
- corrected MAE: `0.059258`;
- relative reduction: **48.91%**;
- held-out cameras improved: `3/3`.

Interpretation: entry information can materially improve an ecological composition estimate when calibration and target data share the broader observation context.

#### 4.2 Unknown camera + unknown physical position — frozen adverse test

The stronger preregistered-in-repo robustness test excluded both the held-out camera and held-out CT position from propensity training.

Across 12 camera × position cells:

- raw MAE: `0.068216`;
- correct IPW MAE: `0.081237`;
- swapped-direction sham MAE: `0.153652`;
- correct IPW worsened error by **19.09%** relative to raw;
- cells improved: `6/12`;
- cells beating sham: `8/12`.

By camera, A improved strongly while BS and BV worsened. By position, BL and C improved while A and BW worsened. Unresolved-state bounds do not reverse the adverse aggregate result.

Interpretation: the sign of structured selection is meaningful, but a simple two-stratum propensity magnitude is not invariant to simultaneous hardware/context shift.

#### 4.3 Within-camera unknown-position transport — weak/mixed

An explicitly exploratory diagnostic after the double-holdout failure:

- raw MAE: `0.068216`;
- corrected MAE: `0.064250`;
- relative reduction: **5.81%**;
- improved cells: `6/12`.

This does not rescue broad transport. It diagnoses that transport is heterogeneous even when camera model/setting is held fixed.

#### 4.4 Second endpoint: fox/badger species composition — positive but heterogeneous

This test asks whether partial recovery is unique to wet/dry otters. Fox/badger use one Bushnell-video system at four physical CT positions. Species-specific entry probabilities are learned from the other three positions and applied to the held-out position.

**Trigger stage:**

- raw MAE: `0.123093`;
- corrected MAE: `0.090510`;
- swapped sham: `0.150218`;
- relative reduction: **26.47%**;
- positions improved: `3/4`;
- positions beating sham: `3/4`.

**Final capture stage:**

- raw MAE: `0.210807`;
- corrected MAE: `0.167972`;
- swapped sham: `0.260198`;
- relative reduction: **20.32%**;
- positions improved: `3/4`;
- positions beating sham: `3/4`.

The same held-out position (`SF`) worsens at both stages and is better served by the sham direction, so the result cannot be sold as universal recovery.

Interpretation: **partial recovery generalizes to a second ecological composition endpoint, while context-specific transport failure also generalizes.**

## The H5 result is now stronger because it is mixed

The manuscript should not say:

> “IPW fixes record-entry bias.”

It should say:

> **Entry-process information can reduce ecological error, and this is reproduced for wet/dry and species composition, but correction performance is context dependent. The calibration provenance and transport domain of the entry model are therefore part of the ecological measurement model.**

The adverse tests are part of the result, not limitations to hide in the Discussion.

## Why this is more than re-labelling detection probability

Existing work establishes imperfect and condition-dependent detection. This paper adds an estimand-centered measurement workflow:

1. define the exposure/reference world before observing entry outcomes;
2. preserve where in the pre-entry process an exposure is lost or unresolved;
3. compare the same ecological estimand in reference and recorded worlds;
4. distinguish upstream omission from downstream semantic error;
5. use entry provenance for correction;
6. test whether that correction transports to new observation contexts;
7. retain adverse transport results rather than retuning after evaluation.

The paper's practical unit is not the name REC; it is the **auditable observation contract**.

## Manuscript results structure

### Result 1 — The event table cannot audit its own missing world

Short foundation:

- identification witness;
- BirdVox continuous denominator;
- Findlay CCTV pass denominator.

### Result 2 — Selective record entry changes ecological composition

Main Findlay figure/result:

- wet/dry entry probabilities and composition shifts;
- fox/badger pass → trigger → capture species composition.

This is the main ecological result.

### Result 3 — Upstream omission survives perfect downstream semantics

Protected BirdVox oracle analysis.

Explicitly label the gate as an adverse/simple recording rule; emphasize irreversibility rather than detector performance.

### Result 4 — Recovery is real but transport-limited

Present the transport ladder:

1. matched-context camera holdout: `-48.91%` error;
2. same-camera position holdout: `-5.81%` average error, mixed;
3. camera+position double holdout: `+19.09%` error, adverse;
4. fox/badger second endpoint: `-26.47%` trigger error and `-20.32%` final-capture error, but only `3/4` positions improve.

The contrast among these tests is the result: correction quality decays or changes sign as the calibration domain is shifted.

## Figure plan

### Figure 1 — Auditable measurement pipeline

`reference/exposure -> entry process -> event table -> downstream semantics -> ecological estimand`

Show the event-log-only blind spot.

### Figure 2 — Selection changes the ecological world

Panel A: otter A/BS/BV wet-vs-dry trigger probabilities plus truth-vs-recorded wet composition.

Panel B: fox/badger truth -> trigger -> capture species composition.

### Figure 3 — Upstream omission is irreversible downstream

BirdVox units 02/05:

`truth contrast -> raw entered contrast -> oracle true-entry-only contrast`.

### Figure 4 — Recovery and transport domain

A transport-ladder plot, not four unrelated correction panels.

For each validation regime show error relative to the reference composition:

- matched camera holdout;
- within-camera position holdout;
- camera+position double holdout;
- fox/badger leave-position-out at trigger and capture.

For cell-level panels, show raw / correct IPW / swapped sham.

This figure should make the paper's practical conclusion visible without prose: **correction can help, but its validity is local to a tested domain.**

## Abstract-ready result paragraph

> In CCTV-referenced camera-trap data, more than half of fox/badger passes failed to trigger and roughly four-fifths failed to become confirmed captures, with selective entry shifting both species and wet/dry composition. In protected continuous-acoustic data, an oracle-perfect downstream stage could not restore a temporal ecological contrast after truth-positive windows were removed upstream. Entry-aware weighting reduced wet-composition error by 48.9% in a matched-context camera holdout and reduced fox/badger species-composition error by 26.5% at trigger and 20.3% at final capture across held-out positions on average. However, a frozen camera-plus-position double holdout worsened wet-composition error by 19.1%, showing that entry propensities do not transport automatically across observation contexts.

## Discussion hierarchy

1. **Record-entry selection can alter ecological estimands before downstream analysis begins.**
2. **Improved downstream classification cannot recover omitted rows.**
3. **Entry provenance creates an opportunity for correction, but not a universal correction law.**
4. **Calibration provenance and transport domain should be stored and validated as part of ecological sensor metadata.**

## Practical recommendation

For automated ecological monitoring, preserve:

- a gate-independent exposure denominator when feasible;
- pre-entry evidence/diagnostics;
- gate and archive-entry version;
- unresolved states rather than forced negatives;
- independent truth audits of entered and non-entered exposures;
- calibration context and transport domain for any correction model.

A final event table alone discards exactly the information needed to diagnose whether its composition is representative and whether a correction is transferable.

## Claims explicitly excluded

- discovery of imperfect detection;
- universal loss rates;
- universal IPW recovery;
- independent-animal validation of the Findlay position holdouts;
- representative BirdVox detector performance;
- prospective H5 confirmation;
- empirical H6.

## Current manuscript-readiness diagnosis

The external-data H1–H5 paper is now logically closed enough to draft without waiting for PolliPi. The strongest remaining improvement would be a genuinely prospective or independent-system correction test, but it is no longer required to make the existing paper coherent.
