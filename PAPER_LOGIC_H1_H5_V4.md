# REC H1–H5 manuscript logic v4 — position-standardized primary endpoint

Status: **canonical paper logic after the frozen CT-position standardization test.**

This version supersedes the endpoint hierarchy in `PAPER_LOGIC_H1_H5_V3.md`. H6/PolliPi remains a prospective follow-on and is not required for the external-data manuscript.

## Central contribution

> **Ecological event tables are selected measurement products. Independent exposure/reference information can reveal when pre-entry selection changes the ecological estimand, but both the selection mechanism and any correction have an observation-context domain that must be tested rather than assumed.**

The paper does not claim discovery of imperfect detection. Its contribution is the empirical chain:

`external reference -> record-entry selection -> ecological estimand distortion -> downstream irreversibility -> context-bounded recovery`.

## Primary empirical hierarchy

### Primary H2→H3 endpoint — fox/badger species composition

Promote the wild fox/badger system to the main ecological result because its composition distortion survives a frozen CT-position standardization test.

Across 881 CCTV-confirmed passes:

- `P(no trigger | pass) = 0.514188`;
- bounded `P(no confirmed capture | pass) = 0.800227–0.802497`;
- raw reference badger proportion = `0.359818`;
- triggered badger proportion = `0.439252`;
- confirmed-capture badger proportion = `0.482759`.

The crucial robustness result is that the direction remains after placing reference and recorded worlds under the **same CT-position distribution**.

Trigger stage:

- equal-position standardized truth = `0.367406`;
- equal-position standardized recorded = `0.429819`;
- standardized shift = `+0.062413`;
- reference-pass-weighted shift = `+0.053498`;
- positions with positive composition shift = `3/4`.

Final-capture stage:

- equal-position standardized truth = `0.367406`;
- equal-position standardized recorded = `0.517249`;
- standardized shift = `+0.149843`;
- reference-pass-weighted shift = `+0.139894`;
- positions with positive composition shift = `3/4`.

`SF` is the retained adverse position at both stages.

Interpretation: the species-composition distortion is not simply a consequence of changing the mixture of physical camera positions. Differential entry within position contributes directly to the changed estimand.

### Mechanistic corroboration — otter wet/dry

Retain wet/dry because it provides a physically interpretable state-dependent trigger mechanism and supports the recovery experiments, but no longer present all three camera settings as clean position-robust replications.

Position-standardized results:

- A: wet composition shift `-0.126993` under equal-position weighting and `-0.134821` under reference-pass weighting; negative in `4/4` positions.
- BV: shift `-0.046370` and `-0.052487`; negative in `3/4` positions.
- BS: shift `+0.003021` and `+0.000893`; direction split `2/4` negative vs `2/4` positive.

Therefore the earlier pooled BS underrepresentation cannot be interpreted as a position-invariant wetness effect. It is an aggregation-sensitive/adverse case.

This is useful rather than damaging: it demonstrates that the operating selection function itself depends on observation context.

## Paper result sequence

### Result 1 — Event tables cannot audit their own missing world

Use the deterministic identification witness briefly, then establish the two empirical external-reference designs:

- Findlay: CCTV-confirmed passes before camera trigger/capture;
- BirdVox: continuous audio exposure universe plus expert event truth.

H1 is a prerequisite, not the novelty headline.

### Result 2 — Record-entry selection changes ecological composition within observation strata

Lead with fox/badger species composition.

Show:

`CCTV pass composition -> species-selective trigger/capture -> position-standardized recorded composition`.

Then show otter A/BV as a second biological-state mechanism and BS as the adverse context where pooled wet underrepresentation disappears after standardization.

This section combines H2 and H3. Do not present a long list of detection-rate differences detached from the ecological estimand.

### Result 3 — Upstream omission cannot be repaired downstream

Use protected BirdVox 02/05 only as an irreversibility stress test.

Protected pooled truth late-minus-early contrast = `+0.130820`; oracle true-entry-only contrast under the frozen z=2 gate is approximately `-0.000025`.

The gate has poor discrimination and is explicitly adverse. The conclusion is only that perfect downstream semantics cannot recreate true windows that never entered.

### Result 4 — Entry provenance enables partial recovery, but correction transport is conditional

Present H5 as a transport ladder rather than a universal success claim.

1. **Otter matched-context camera holdout:** MAE `0.115982 -> 0.059258`, `48.91%` reduction, `3/3` cameras improved.
2. **Otter within-camera unknown-position diagnostic:** MAE `0.068216 -> 0.064250`, `5.81%` reduction, `6/12` cells improved; explicitly exploratory after the harder test.
3. **Otter camera + position double holdout:** MAE `0.068216 -> 0.081237`, `19.09%` worsening, `6/12` cells improved; frozen adverse test. Correct IPW remains much better than swapped sham (`0.153652`), showing that the selection direction contains information even when propensity magnitude does not transport.
4. **Fox/badger leave-position-out recovery:** trigger MAE `0.123093 -> 0.090510` (`26.47%` improvement) and final-capture MAE `0.210807 -> 0.167972` (`20.32%` improvement), each with `3/4` positions improved; `SF` remains adverse.

The constructive conclusion is therefore:

> **Entry information can reduce ecological error, but an entry model is not a universal property of the biological event. Its calibration and transport domain are part of the observation model.**

## Figure hierarchy

### Figure 1 — Auditable observation pipeline

`reference/exposure -> record-entry process -> event table -> downstream semantics -> ecological estimand`

Keep formal notation light. Make the event-log-only blind spot visually obvious.

### Figure 2 — Primary ecological result: position-robust species distortion

Main panel: fox/badger badger proportion at reference, trigger and capture stages.

Robustness panel: within-position shifts and the two position-standardized estimates.

Secondary inset/panel: otter A/BV wet underrepresentation and BS adverse standardization result.

### Figure 3 — Irreversibility

BirdVox protected units: `truth temporal contrast -> raw entered contrast -> oracle true-entry-only contrast`.

### Figure 4 — Recovery transport ladder

Show raw/correct/sham error under progressively different calibration domains:

- matched-context otter camera holdout;
- otter camera+position double holdout;
- fox/badger leave-position-out trigger and capture.

Put the exploratory within-camera position diagnostic in supplement or a muted secondary panel, not as a rescuing main result.

## Abstract-ready results logic

A defensible abstract should lead with the position-robust species result, not the pooled wet/dry result:

> In CCTV-referenced camera-trap data, 51.4% of fox/badger passes failed to trigger and approximately 80.0–80.2% failed to become confirmed captures. This selection changed species composition before downstream classification: badger representation rose from 0.360 among true passes to 0.439 after triggering and 0.483 after confirmed capture. The distortion remained after standardizing reference and recorded worlds to the same physical camera-position distribution. Wet/dry otter analyses showed the same mechanism for two camera settings but also an adverse third setting in which the pooled effect disappeared after position standardization, demonstrating context dependence. Protected continuous-acoustic data further showed that oracle-perfect downstream semantics could not reconstruct a temporal ecological contrast after truth-positive windows were omitted upstream. Entry-aware correction reduced composition error in matched or partly transported contexts, but a frozen simultaneous camera-plus-position shift worsened error, showing that correction transport must itself be validated.

## Discussion hierarchy

1. **Record-entry selection can alter the ecological estimand within observation strata, not only through aggregate sampling composition.**
2. **Upstream omission and downstream classification error are not interchangeable.**
3. **Entry provenance creates a real but context-bounded opportunity for recovery.**
4. **Observation context determines both the selection function and the transportability of its correction.**
5. **The practical contribution is an auditable measurement contract, not the REC terminology itself.**

## Practical measurement contract

For automated ecological monitoring, retain when feasible:

- an exposure/reference denominator defined independently of the tested event gate;
- pre-entry evidence or diagnostics;
- versioned gate/trigger/archive-entry provenance;
- unresolved states rather than forced negatives;
- independent truth audits that include non-entered exposures;
- calibration context and explicitly tested transport domain for any correction model.

## Claims excluded

Do not claim:

- discovery of imperfect detection;
- a universal wetness effect across all Findlay otter camera settings;
- universal IPW recovery;
- independence of repeated Findlay passes as animals/populations;
- representative acoustic detector performance from BirdVox;
- prospective H5 confirmation;
- empirical H6.

## Current manuscript decision

**Draft on H1–H5 now.** The primary empirical claim is the position-robust fox/badger species-composition distortion. Otter wet/dry supplies mechanistic corroboration, adverse aggregation sensitivity and the transport ladder. BirdVox supplies the independent irreversibility stress test. Further retrospective Findlay slicing should stop unless needed to answer a specific reviewer question.