# Figure captions — REC H1–H5 manuscript

Status: **paper-facing caption draft aligned with V4 logic and generated figure artifacts.**

## Figure 1. Auditable record-entry measurement pipeline

**An ecological event table begins after a selection process that it cannot audit from its own rows.** External exposure or reference information defines observation opportunities independently of the tested event gate. Biological events and pre-entry evidence are then filtered by a trigger/gate and archive or record-entry step before becoming rows available to downstream semantic or AI classification and ecological inference. True events lost before usable record entry are absent from the event-table-visible world and cannot be characterized empirically from the final event table alone. REC uses external exposure/reference information to enumerate or sample this pre-entry branch and links it to the same downstream ecological estimand. The diagram is a measurement contract, not a claim that imperfect detection is newly recognized.

Generated panel: `fig1_auditable_record_entry_pipeline.png`.

## Figure 2. Record-entry selection changes ecological composition before downstream classification

### Figure 2a. Fox/badger composition across record-entry stages

Badger proportion among 881 CCTV-confirmed fox/badger passes is compared with badger proportion among confirmed triggered records and confirmed final captures. Badgers comprise `0.3598` of reference passes, `0.4393` of confirmed triggered records and `0.4828` of confirmed captures. These values describe composition among independently observed passes and entered camera records; they are not population abundance estimates.

Generated panel: `fig2a_badger_composition.png`.

### Figure 2b. Species distortion after CT-position standardization

Recorded-minus-reference badger-composition shifts after forcing reference and recorded worlds to share the same physical camera-trap position distribution. At the trigger stage, the standardized shift is `+0.0624` under equal CT-position weights and `+0.0535` under weights defined by the reference-pass position distribution. At final capture, corresponding shifts are `+0.1498` and `+0.1399`. Three of four CT positions show positive species-composition shifts; `SF` is retained as the adverse position. Standardization addresses measured CT-position mixture but does not establish a causal effect of species identity independent of all encounter covariates.

Generated panel: `fig2b_position_standardized_badger.png`.

### Figure 2c. Otter wet/dry selection depends on observation context

Position-standardized recorded-minus-reference wet-composition shifts for camera settings A, BS and BV under equal CT-position weighting and reference-pass weighting. A retains strong wet underrepresentation under both schemes (`-0.1270` and `-0.1348`); BV retains weaker underrepresentation (`-0.0464` and `-0.0525`). BS is approximately zero after standardization (`+0.0030` and `+0.0009`), showing that its pooled wet underrepresentation was aggregation-sensitive. The BS result is retained as an adverse context rather than excluded.

Generated panel: `fig2c_otter_position_standardization.png`.

## Figure 3. Upstream omission persists after oracle-perfect downstream semantics

Late-minus-early event-window prevalence contrasts in protected BirdVox units 02 and 05 and their pooled result under the frozen `z=2` digital entry gate. Reference truth is compared with the contrast in the entered record and with an oracle downstream record in which every false entered window is removed while no upstream-missing row is added. Reference contrasts are `+0.1051`, `+0.1565` and `+0.1308` for unit02, unit05 and pooled protected units, respectively. The corresponding oracle contrasts are approximately `+0.00010`, `-0.00015` and `-0.00003`. Thus semantic perfection among available rows does not reconstruct the temporal signal once true windows have been omitted upstream. The annotation-naive frozen score discriminated poorly in protected units; this panel is an irreversibility stress test and must not be interpreted as representative acoustic-detector performance.

Generated panel: `fig3_birdvox_irreversibility.png`.

## Figure 4. Entry-aware correction is context bounded

### Figure 4a. Recovery transport ladder

Mean absolute composition error in the raw record and after entry-aware inverse-probability correction under progressively different calibration/transport regimes. Matched-context otter camera holdout reduces error by `48.9%`. An explicitly exploratory within-camera position diagnostic reduces mean error by `5.8%`. The frozen simultaneous camera-plus-position otter holdout **increases** error by `19.1%`. Fox/badger species correction reduces mean held-out-position error by `26.5%` at trigger and `20.3%` at final capture. The contrast across regimes, rather than universal improvement, is the result: an entry model has a calibration and transport domain.

Generated panel: `fig4_recovery_transport_ladder.png`.

### Figure 4b. Direction-reversed sham controls

Raw error, correct entry-aware correction and a deliberately direction-swapped propensity correction for the harder otter camera-plus-position test and the fox/badger trigger and capture position-transport tests. The sham checks whether arbitrary reweighting can create apparent improvement. Correct weighting is substantially better than the swapped sham on aggregate, but the otter double-holdout still performs worse than leaving the record uncorrected. This indicates that the observed direction of selection contains information while its transported magnitude can be wrong enough to increase ecological error.

Generated panel: `fig4b_sham_controls.png`.

## Suggested supplementary figures

### Figure S1. Findlay entry-loss structure

Descriptive event-conditioned non-trigger and non-capture estimates across species, distance, orientation, gait, camera position and loitering. Use as mechanism support only; do not promote row-level strata to independent biological replicates.

### Figure S2. Position-specific species composition

Reference, triggered and captured badger proportion within AP, FF, SF and SNIG CT positions, paired with species-specific trigger/capture probabilities. This exposes the retained adverse SF context and visually supports the standardization analysis.

### Figure S3. Otter camera × position wet/dry shifts

Cell-level reference-minus-triggered wet-composition differences for A, BS and BV across physical positions. Retain BS sign heterogeneity.

### Figure S4. H5 cell-level transport outcomes

Raw, correct-IPW and sham errors for all 12 otter camera × position double-holdout cells and all four fox/badger position holdouts. This figure should show every adverse cell rather than only aggregate means.
