# REC H1–H5 manuscript logic v2 — post-validation

Status: **canonical paper-facing logic after the frozen H5 double-holdout robustness test.**

This supersedes the pre-result framing in `PAPER_LOGIC_H1_H5.md` for manuscript construction. H6/PolliPi remains a prospective follow-on and is not required to close this paper.

## Candidate title

**Auditing record-entry selection in ecological monitoring reveals estimand distortion and limits to correction transport**

Alternative:

**Ecological records are selected before analysis: auditing record entry, ecological distortion and recovery limits**

## One-sentence contribution

> **An ecological event table is already a selected view of nature: independent exposure/reference data reveal which true events fail to enter, show that this selection changes ecological estimands, and show that entry-aware correction can help only within a validated calibration domain rather than transporting automatically across observation contexts.**

## The paper is not H1 + H2 + H3 + H4 + H5

Use four scientific moves.

### Move 1 — Make the missing world auditable

The paper does not claim discovery of imperfect detection.

Instead it establishes the measurement requirement:

`independent exposure/reference world -> record-entry process -> event table`.

An event table alone cannot reveal the biological composition of rows that never existed. BirdVox continuous audio and Findlay CCTV-confirmed animal passes demonstrate two ways to create an external denominator/reference world.

This absorbs H1 plus the identifiability result.

**Role in paper:** short conceptual/result foundation, not headline novelty.

### Move 2 — Show that selection changes ecology, not merely sample size

This is the central empirical result.

Findlay provides the clean chain:

`true animal pass -> condition-dependent trigger/capture -> changed ecological composition`.

Key observations:

- among 881 fox/badger passes, no-trigger probability is 0.514188 and bounded final non-capture is approximately 0.800227–0.802497;
- entry loss differs across species and observation/pass conditions;
- badger composition changes from 0.359818 in the true-pass world to 0.439252 after trigger and 0.482759 among confirmed captures;
- wet otter passes have higher trigger loss than dry passes for all three camera model/settings;
- wet composition consequently shifts downward in every recorded camera world:
  - A: 0.438017 -> 0.270270;
  - BS: 0.459821 -> 0.378788;
  - BV: 0.445833 -> 0.346667.

This joins H2 and H3 into one mechanism-to-estimand result.

**Do not write separate sections called “H2 supported” and “H3 supported”.** The logical statement is:

> entry is selective **therefore** the recorded ecological composition differs from the reference composition.

### Move 3 — Show why downstream perfection cannot solve upstream omission

BirdVox is not the main detector-performance system.

Use the protected 02/05 experiment only as an irreversibility stress test.

The frozen annotation-naive gate performed poorly, which is retained as an adverse system-specific result. Yet this makes one point unambiguous: after truth-positive windows fail to enter, an oracle-perfect downstream semantic stage still cannot reconstruct the true temporal ecological contrast.

Protected pooled truth late-minus-early prevalence contrast:

`+0.130820`.

At z=2, the oracle true-entry-only contrast is approximately:

`-0.000025`.

The downstream stage can remove false entries; it cannot manufacture omitted true rows.

This is the REC-to-TNOA bridge without needing H6.

### Move 4 — Show both recovery and its transport boundary

This is now the strongest constructive result because it includes a success and a falsification.

#### 4A. Matched-context recovery is positive

Original leave-one-camera-out H5:

- correction propensities estimated only from the other camera model/settings;
- held-out wet-composition error improves for 3/3 cameras;
- mean absolute error: `0.115982 -> 0.059258`;
- relative reduction: `48.91%`.

This demonstrates that retaining entry-process information can be useful for ecological recovery.

But it is a **matched-context retrospective calibration**: the camera streams arise from the same overall otter experiment and observation context.

#### 4B. Broad transport is falsified

The frozen robustness test excluded both the held-out camera and held-out physical CT position from propensity training.

Across 12 camera x position cells:

- raw MAE: `0.068216`;
- correct entry-aware IPW MAE: `0.081237`;
- swapped-direction sham MAE: `0.153652`;
- correct IPW worsens error by `19.09%` relative to raw;
- only `6/12` cells improve;
- `8/12` cells still beat the direction-reversed sham.

By camera:

- A improves: `0.126993 -> 0.053219`;
- BS worsens: `0.022881 -> 0.110358`;
- BV worsens: `0.054774 -> 0.080136`.

The unresolved-trigger worst-case mean remains worse than raw, so missing trigger states do not rescue the claim.

#### 4C. Position-only transport is weak, not robust

An exploratory within-camera leave-one-position-out diagnostic gives only a small average improvement:

`0.068216 -> 0.064250` (`5.81%`).

Again only `6/12` cells improve.

This diagnostic cannot replace the frozen adverse double-holdout result because it was added after that result was observed.

#### Final H5 interpretation

Do not claim “REC correction generalizes”.

Claim:

> **Entry-process information enables partial recovery when calibration and target data share sufficient observation context, but the selection function is itself context dependent and must carry a validated transport domain.**

This is scientifically stronger than a generic IPW success claim because it explains when correction should and should not be trusted.

## What becomes novel enough to defend

The component facts are known:

- nondetection is not absence;
- camera traps have trigger/registration failures;
- wetness, distance and movement can alter detectability;
- thresholds trade false positives and false negatives.

The paper contribution is their integration around the **ecological estimand and measurement provenance**:

1. define an external exposure/reference world before studying non-entry;
2. measure the selection function between true exposure and usable record;
3. quantify the ecological estimand before and after that selection;
4. test whether downstream processing can recover omitted information;
5. use selection information for correction;
6. explicitly test whether the correction transports outside its calibration context.

The adverse transport result is essential to this contribution. It prevents REC from becoming another paper that estimates one detection probability and silently exports it as universal.

## System roles

### Primary: Findlay camera/CCTV

Main paper system for selective entry, composition distortion and correction/transport.

Use wet/dry otter as the primary mechanistic endpoint because:

- state is defined independently of camera output;
- PIR mechanism is physically interpretable;
- direction repeats across all three camera model/settings;
- it produces a clean ecological composition estimand;
- correction and transport can be tested on the same reference world.

Use fox/badger composition as a second-endpoint guard against a wet-otter-only story.

### Secondary: BirdVox protected replication

Use only for:

- complete continuous exposure denominator;
- cross-modality replication of upstream omission;
- oracle-downstream irreversibility.

Keep detector discrimination failure explicit.

### Future: PolliPi

PolliPi is the prospective confirmation of the measurement contract and the same-system REC→TNOA decomposition. It strengthens the research program but should not delay this paper.

## Results structure

### Result 1. Event logs cannot audit their own missing rows

Very short.

- non-identifiability witness;
- exposure/reference design requirement;
- two empirical denominator designs.

### Result 2. Record entry selectively changes the ecological world

Main Findlay result.

Combine:

- trigger/capture loss;
- wet vs dry entry probabilities;
- wet composition distortion;
- fox/badger species-composition distortion.

Avoid presenting a long catalogue of detection-rate ranges.

### Result 3. Downstream semantics cannot restore omitted events

Protected BirdVox stress test.

Focus on truth contrast vs oracle-entered contrast.

### Result 4. Recovery is possible, but calibration does not transport automatically

Present in this order:

1. matched-context leave-one-camera recovery: positive 3/3, -48.91% MAE;
2. frozen camera+position double holdout: fails, +19.09% MAE;
3. sham direction reversal is substantially worse overall;
4. exploratory position-only transport is weak (+5.81% improvement) and heterogeneous.

End result:

**use entry-aware correction, but validate its transport domain.**

## Figure plan

### Figure 1 — Auditable observation pipeline

Two worlds:

`reference/exposure world -> entry selection -> event table -> downstream analysis`.

Mark what event-log-only data cannot identify.

### Figure 2 — Selective entry creates ecological distortion

Primary panel:

For A / BS / BV show:

- wet and dry trigger probabilities;
- truth wet composition;
- triggered wet composition.

Secondary panel:

fox/badger truth -> trigger -> capture composition.

### Figure 3 — Omission is irreversible downstream

BirdVox 02/05:

`truth temporal contrast -> raw entered contrast -> oracle true-entry-only contrast`.

Make the annotation-naive gate limitation visible in the caption.

### Figure 4 — Recovery and transport boundary

Panel A: original camera-holdout recovery.

Panel B: 12 double-holdout camera x position cells, plotting error for:

`raw | correct IPW | swapped sham`.

Panel C: camera-level and position-level macro summaries.

The visual message should be obvious: correction helps in a matched calibration context but is not invariant to context shift.

## Abstract logic

### Background

Automated ecological studies usually analyse the records produced by sensors, although the process determining which biological events become records may itself be selective.

### Question

Does measurable pre-entry selection alter ecological estimands, and does recording the entry process make the distortion recoverable?

### Methods

Audit two independent observation systems with external exposure/reference information: continuous annotated acoustic recordings and CCTV-observed camera-trap passes. Compare ecological estimands across reference and recorded worlds, then test entry-probability correction and its transport across camera/position contexts.

### Results

Camera-trap entry loss is large and condition dependent; selective loss changes species and wet/dry composition. Protected acoustic analyses show that an oracle-perfect downstream stage cannot reconstruct an upstream-erased temporal contrast. Entry-aware weighting reduces wet-composition error by 48.91% in a matched-context camera holdout, but a frozen camera+position double holdout worsens aggregate error by 19.09%, demonstrating that correction propensities do not transport automatically.

### Conclusion

The scientific record is a selected measurement product rather than a neutral subset of biological events. Retaining exposure, entry provenance and independent truth makes this selection auditable and sometimes correctable, but calibration provenance and transport domain must be treated as part of the ecological measurement model.

## Discussion hierarchy

### First conclusion

**Selective record entry changes ecological estimands.**

That is more important than “some events are missed”.

### Second conclusion

**Upstream loss and downstream classification are different problems.**

Improving downstream semantics cannot recover missing rows.

### Third conclusion

**Correction requires transport validation.**

A locally useful entry model can fail when hardware and observation context both change.

### Practical recommendation

Automated monitoring should archive more than event detections:

- a gate-independent exposure denominator where feasible;
- pre-entry evidence or diagnostics;
- gate/entry rule and version;
- unresolved operational states;
- calibration context/provenance;
- independent truth audits, including non-entered exposures;
- the domain over which any correction model was validated.

## Claims to avoid

Do not claim:

- discovery of imperfect detection;
- universal record-loss magnitude;
- that all ecological endpoints are strongly distorted;
- that BirdVox represents competent detector performance;
- universal or unbiased IPW recovery;
- independent-animal replication from the captive otter positions;
- prospective H5 confirmation;
- empirical H6.

## Current paper-status diagnosis

H1–H5 are sufficient for a coherent methods/ecological-measurement paper **without H6**, provided the recovery result is reported together with its failed transport test.

The paper is stronger after the adverse robustness result because its final contribution is not “we invented a correction that works on our example”. It is:

> **measure the record-entry process, quantify what it does to ecology, use it for correction, and never assume that the correction transports beyond the observation context in which its operating meaning was established.**
