# REC paper logic — H1–H5 as one empirical argument

Status: **paper-facing logic freeze for the current external-data manuscript; H6/PolliPi is deliberately outside the main H1–H5 paper claim.**

## Central question

The paper should not ask whether ecological sensors miss events. That is established prior art.

The paper asks:

> **When record-entry selection is measurable against an exposure/reference world, does it alter the ecological estimand available to downstream analysis, and can retaining that entry-process information partially recover the estimand out of sample?**

This turns H1–H5 from five parallel hypotheses into one measurement argument.

## Three claims, not five headline hypotheses

### Claim 1 — Auditability

A scientific event log is not sufficient to characterize the biological content of exposures that never became records. A gate-independent exposure/reference design makes that missing world empirically auditable.

Evidence used here:

- the deterministic event-log non-identifiability witness;
- BirdVox continuous audio as an enumerable algorithmic exposure universe;
- Findlay CCTV-confirmed animal passes as an independently observed event denominator.

H1 is therefore a **measurement prerequisite**, not the novelty headline.

### Claim 2 — Ecological consequence

Record-entry loss matters scientifically when it is structured by biological or observation state and therefore changes an ecological estimand, not merely sample size.

The main empirical chain is:

`true encounter composition -> condition-dependent entry -> changed recorded composition`

Findlay is the primary system because the entry process is physical and externally observed:

- 881 fox/badger passes show substantial trigger and final-capture loss;
- loss varies with species and pass/observation conditions;
- species and gait compositions shift between the pass world and recorded world;
- wet otter passes have lower trigger success than dry passes in all three camera model/settings, producing wet underrepresentation in all three recorded worlds.

H2 is the **selection mechanism** and H3 is the **ecological result**. H3 is the main biological/methodological punch of the paper.

### Claim 3 — Recoverability

Entry-process information is useful only if it can improve an ecological estimate outside the rows used to estimate selection.

Current H5 evidence:

- leave-one-camera-out IPW improves wet-composition error in 3/3 held-out camera model/settings;
- mean absolute error falls from 0.115982 to 0.059258 (48.91% reduction);
- unresolved trigger states are retained and bounded rather than coded as failures.

Because the three camera streams observed the same underlying otter-pass process, the current H5 result is a hardware-transport demonstration, not a fully independent encounter-level validation. The next validation therefore removes both camera overlap and recording-position/pass overlap.

## H4 moves out of the headline

H4 (different frozen gates create different recorded worlds) is useful, but threshold sensitivity is established and should not be sold as a central discovery.

Use H4 as:

- a sensitivity/falsification analysis showing that the observed world is partly policy-defined;
- a bridge to the practical recommendation that gate version and pre-gate evidence must be retained;
- supporting evidence in BirdVox, not a standalone headline result.

## Roles of the empirical systems

### Findlay camera traps — primary empirical system

Use for the main H1/H2/H3/H5 chain because CCTV supplies true passes and the sensor process itself is real.

Primary estimand for the cleanest paper story:

`wet proportion among independently observed otter passes`.

Why this endpoint works:

- biological state (wet/dry) is independently determined before camera output;
- wetness has a physically plausible PIR-trigger mechanism;
- the direction of entry loss repeats in all three camera model/settings;
- the resulting composition distortion is directly interpretable;
- the same entry information can be used in a correction test.

Fox/badger species composition remains a second ecological endpoint demonstrating that the problem is not unique to wet otters.

### BirdVox — cross-modality irreversibility stress test

Do not use BirdVox to claim representative detector performance. The frozen score generalizes poorly.

Use BirdVox for one narrow point:

> **Once truth-positive windows are removed upstream, even an oracle-perfect downstream semantic stage cannot reconstruct the ecological contrast from rows that never entered.**

That makes BirdVox a mechanistic stress test of information irreversibility, not the main performance system.

### PolliPi/H6 — next paper / prospective confirmation

Do not make the current H1–H5 manuscript wait for H6. PolliPi is the prospective same-system confirmation route and REC–TNOA synthesis.

## Additional validation V2 — double holdout on Findlay wet/dry

### Why needed

The current leave-one-camera-out H5 analysis holds out camera model/setting, but all three camera streams were colocated and observed the same encounter process. A reviewer can therefore argue that biological conditions represented in the held-out stream are still represented in training.

### Frozen double-holdout unit

Use the natural study design axes already present in the released table:

- `CAMERA.ID`: A, BS, BV;
- `CT.POS`: the physical camera-trap recording position.

For each `(heldout camera, heldout CT.POS)` cell:

- **training rows:** `CAMERA.ID != heldout camera` **and** `CT.POS != heldout CT.POS`;
- **test rows:** `CAMERA.ID == heldout camera` **and** `CT.POS == heldout CT.POS`.

Thus the correction is learned from neither the held-out camera model/setting nor the held-out physical recording position. Because colocated cameras share the same pass process, excluding the entire held-out position is the conservative step that prevents same-position/pass information from entering training.

### Frozen estimand and correction

For every evaluable test cell:

1. truth = wet proportion among all independently observed passes in that cell;
2. raw = wet proportion among confirmed triggered records;
3. corrected = self-normalized IPW using wet/dry trigger propensities estimated only from the double-excluded training rows.

Unresolved trigger states remain unresolved. Point propensities are resolved-only and the same worst/best training-propensity envelope is retained.

### Falsification controls

Run three estimators on every cell:

- **raw/unweighted** — the observed trigger world;
- **correct entry-aware IPW** — wet/dry propensities in their observed direction;
- **sham swapped IPW** — wet and dry propensities deliberately exchanged.

A useful mechanism should not merely move estimates arbitrarily. The entry-aware correction should outperform raw and should outperform the direction-reversed sham correction on aggregate.

A uniform-propensity weighting is algebraically identical to the raw composition and is retained as a code-level sanity test, not a separate result.

### Aggregate reporting

Report without treating all camera-position cells as independent biological replicates:

- cell-level raw, corrected and sham errors;
- macro-average error by held-out camera;
- macro-average error by held-out position;
- overall macro-average across evaluable cells;
- number/proportion of cells improved;
- number of physical positions whose camera-averaged error improves;
- unresolved-state sensitivity bounds.

Any formal sign/permutation result is secondary because this remains retrospective reanalysis of public outcomes.

### Promotion rule

H5 is strengthened if:

1. corrected aggregate error < raw aggregate error;
2. corrected aggregate error < sham aggregate error;
3. improvement is not driven by a single camera model/setting;
4. improvement is not driven by a single CT position;
5. unresolved-trigger bounds do not reverse the aggregate conclusion.

Failure of any item is retained and narrows the recovery claim rather than triggering a new post-hoc split.

## Additional validation V3 — composition-distortion closure

The H2 -> H3 connection should be explicit rather than presented as two unrelated descriptive findings.

For each otter camera model/setting, report together:

- truth wet composition;
- wet and dry trigger probabilities;
- observed recorded wet composition;
- direction and magnitude of composition error.

The paper should state the mechanism in words:

> wet passes are less likely to enter; therefore wet passes are underrepresented in the recorded composition.

Do not call this a new causal theorem; the value is that the same independently observed pass data close the mechanism-to-estimand chain.

## Additional validation V4 — second-endpoint guard against endpoint cherry-picking

Keep fox/badger species composition as an independent second endpoint.

The primary recovery analysis remains wet/dry because that table supports a clean entry correction. But the paper should show that entry selection also moves species composition in a separate wild system component:

- true badger proportion 0.359818;
- triggered badger proportion 0.439252;
- captured badger proportion 0.482759.

This guards against the paper being interpreted as a wet-otter-only artifact while avoiding post-hoc claims that every ecological endpoint must distort equally.

## Results architecture

### Result 1 — What the event log cannot show

Establish the exposure/reference requirement and H1 briefly. Do not spend the paper proving that false negatives exist.

### Result 2 — Entry is selective, and the selection changes ecology

Make Findlay the center:

`true passes -> trigger/capture selection -> species and wet/dry composition shift`.

This combines H2 and H3 into one result rather than two disconnected sections.

### Result 3 — Upstream omission is irreversible downstream

Use protected BirdVox only as the cross-modality stress test. The oracle downstream comparison is the key result; extreme miss-rate magnitude is explicitly adverse and system-specific.

### Result 4 — Retaining entry information enables partial recovery

Lead with H5 and the new double-holdout/sham validation. This is the constructive ending of the paper.

## Figure architecture

### Figure 1 — Measurement contrast

`exposure/reference world -> record-entry selection -> event log`

Show exactly what an event-log-only workflow loses and what the independent reference design recovers.

### Figure 2 — Selective entry changes ecological composition

Findlay wet/dry as primary panel, species composition as secondary panel.

Avoid a generic forest of detection rates; plot truth composition next to recorded composition and the entry probabilities that generate the shift.

### Figure 3 — Irreversibility stress test

BirdVox truth temporal contrast -> entered contrast -> oracle-downstream contrast.

The point is not detector quality; it is that perfect downstream semantics cannot restore omitted rows.

### Figure 4 — Recovery

For each double-holdout camera x position cell, plot absolute error for:

`raw -> correct IPW -> swapped sham`.

Add camera- and position-level macro summaries.

## Discussion claim hierarchy

Strongest defensible conclusion:

> **Record-entry selection can change the ecological composition available to analysis, but the distortion is not necessarily irrecoverable: when exposure/reference and entry provenance are retained, selection-aware correction can partially restore the target estimand outside the data used to estimate the entry process.**

Do not claim:

- discovery of imperfect detection;
- universal magnitudes of record loss;
- that IPW fully reconstructs truth;
- that BirdVox represents competent acoustic detector performance;
- prospective confirmation of H5;
- empirical H6.

## Practical contribution

The actionable recommendation is a data-design rule:

> **Automated ecological monitoring should retain an exposure denominator, pre-entry evidence, versioned entry/gate provenance and an independent truth audit of non-entered exposures, rather than preserving only the final event table.**

That recommendation is stronger than introducing REC terminology because the H1–H5 results show why the retained process information changes what can be diagnosed and what can be corrected.
