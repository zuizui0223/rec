# Manuscript draft — REC H1–H5 external-data paper

## Working title

**Auditing record-entry selection reveals ecological estimand distortion and context-dependent recovery**

## Abstract

Automated ecological monitoring usually begins analysis from records produced by sensors, although the process determining which biological events become records can itself be selective. Imperfect detection is well established, but an event table alone cannot reveal the biological composition of exposures that never became rows, making it difficult to determine when pre-entry loss changes the ecological estimand available to downstream analysis. We treated record entry as an auditable measurement process and evaluated it in two observation systems with external exposure or reference information: continuous expert-annotated acoustic recordings and CCTV-referenced camera-trap passes. In the camera-trap system, 51.4% of independently observed fox and badger passes failed to trigger and approximately 80.0–80.2% failed to become confirmed captures. Entry was structured by biological and observation state and changed ecological composition: badger representation increased from 0.360 among true passes to 0.439 after triggering and 0.483 among confirmed captures, while wet otters were underrepresented in all three triggered camera records. In protected continuous-acoustic data, a true late-minus-early event-window contrast of +0.131 was almost eliminated after upstream selection even when downstream semantic classification was assumed to be oracle-perfect, showing that downstream accuracy cannot reconstruct omitted rows. Retaining entry-process information nevertheless enabled partial recovery. Entry-aware weighting reduced wet-composition error by 48.9% in a matched-context camera holdout and reduced fox/badger species-composition error by 26.5% at trigger and 20.3% at final capture across held-out positions on average. However, a frozen camera-plus-position double holdout increased wet-composition error by 19.1%, demonstrating that entry propensities did not transport automatically across observation contexts. These results show that ecological event tables are selected measurement products rather than neutral subsets of biological events. Preserving exposure denominators, entry provenance and calibration context can make selection both diagnosable and partly correctable, but the transport domain of any correction must itself be validated.

## 1. Introduction

### 1.1 The problem starts before downstream analysis

Ecological sensors increasingly convert continuous biological activity into discrete event records that are subsequently classified, summarized and modelled. The statistical consequences of imperfect detection are well established, and extensive work has shown that environmental conditions, animal behaviour, sensor hardware and algorithmic thresholds affect whether events are detected. Yet most downstream workflows still begin from the event table produced by the observation system. Once analysis starts from those rows, events that never became records are absent not only from the response variable but from the dataset itself.

This creates a measurement problem that is related to, but not identical with, estimating a conventional detection probability. The relevant question for downstream ecology is not only whether events were missed, but whether the process selecting events into the record changes the ecological quantity that the recorded data appear to estimate. If entry probability covaries with biological state, environmental condition or sensor context, record loss can alter composition, temporal contrasts or other estimands rather than merely reducing sample size.

### 1.2 Why an external exposure or reference world is required

An event log cannot empirically characterize the biological content of rows that were never created. Studying pre-entry selection therefore requires a denominator or reference world defined independently of the tested record-entry rule. Such a design may be provided by continuous recordings, synchronized reference sensors, fixed exposure clocks or independent observer systems. Missing or unresolved reference states must remain explicit rather than being converted to biological negatives.

We use the term **record-entry selection** for the measurable process between an independently defined exposure/reference world and the usable event table. The terminology is not intended to rename imperfect detection as a new phenomenon. Instead, it specifies the measurement information required to connect known detection failures to their downstream ecological consequence.

### 1.3 From diagnosis to recovery

If record entry is selective, retaining its provenance may also create an opportunity for correction. However, a correction model is useful only if the entry probabilities estimated during calibration remain meaningful in the target observation context. Detection or entry probability should therefore not be assumed to be an invariant property of the biological event; its transport across hardware, position or environmental context is itself an empirical question.

This leads to three linked questions. First, can an external exposure/reference design reveal true biological events that are absent from the tested record? Second, does structured entry selection change ecological estimands available to downstream analysis, including after downstream classification is made arbitrarily accurate? Third, can entry-process information reduce that distortion outside the data used to estimate the selection process, and over what observation domain does such correction transport?

### 1.4 Study design

We addressed these questions using two complementary systems. Findlay et al.'s camera-trap/CCTV data provide independently observed mammal passes followed by physical trigger and capture outcomes, allowing direct measurement of pre-entry selection and ecological composition changes. BirdVox-full-night provides a continuous acoustic exposure universe with expert call annotations, allowing a protected algorithmic stress test in which upstream omission can be separated from a hypothetical oracle-perfect downstream semantic stage. We then used the camera-trap reference data to evaluate entry-aware correction under progressively harder transport regimes, including a frozen test in which both camera model/setting and physical recording position were excluded from calibration.

Our contribution is therefore not the observation that sensors miss events. It is an empirical measurement chain linking external reference truth, record-entry selection, ecological estimand distortion, downstream irreversibility, and the conditions under which entry-aware recovery does or does not transport.

## 2. Methods

### 2.1 General measurement framework

For each system, define an exposure/reference universe independently of the tested event-entry rule. Distinguish biological truth, gate/trigger state, final usable record entry and downstream semantic processing. Treat unresolved reference or operational states as unresolved and report bounds where appropriate.

Primary comparison:

`reference ecological estimand -> recorded ecological estimand`.

Recovery comparison:

`reference -> raw record -> entry-aware corrected record -> falsification/sham correction`.

### 2.2 Event-log identifiability witness

Describe deterministic construction showing that identical observed event logs are compatible with different biological compositions of the non-entered world. Use this only to motivate the need for external exposure/reference information, not as a claimed new missing-data theorem.

### 2.3 Findlay camera-trap reference system

Source and provenance:

- public CT-Detection repository pinned by commit and Git blob;
- wild fox/badger experiment with CCTV-confirmed passes and Bushnell video cameras;
- captive otter experiment with CCTV-confirmed passes and three camera model/settings;
- physical CT positions treated as observation-context strata.

Define trigger and final-capture states. A confirmed non-trigger implies no final camera record from that pass. Missing trigger or capture truth is never silently coded as failure when its stage is unresolved.

### 2.4 Ecological estimands in Findlay

Primary mechanistic endpoint:

- wet proportion among independently observed otter passes.

Second endpoint:

- badger proportion among independently observed fox/badger passes.

For each endpoint compare composition in the reference pass world with composition among confirmed triggered and, where available, confirmed captured records.

### 2.5 BirdVox protected irreversibility stress test

Define one-second exposure windows from continuous audio duration before applying the frozen annotation-naive score gate. Unit10 remains the pilot; units 02/05 are protected replication units. Emphasize that the frozen gate generalized poorly and is not a representative detector benchmark.

Compute the true late-minus-early event-window prevalence contrast, the contrast after record-entry selection, and an oracle true-entry-only contrast in which all downstream false entries are removed. The oracle comparison asks whether perfect downstream semantics could restore truth after upstream omission.

### 2.6 Matched-context wet/dry recovery

Leave one camera model/setting out. Estimate wet/dry trigger propensities from the other camera streams and apply self-normalized inverse-probability weighting to the held-out triggered composition. Compare absolute error against the CCTV pass composition.

### 2.7 Frozen camera-plus-position transport test

For each held-out camera × CT-position cell, estimate propensities only from rows using neither the held-out camera nor the held-out physical position. Compare raw composition, correct wet/dry IPW and a swapped-direction sham IPW. Aggregate by held-out camera and position without treating cells as independent animals. Propagate unresolved training trigger states through propensity bounds.

### 2.8 Fox/badger second-endpoint recovery

Within the single Bushnell-video system, leave one physical CT position out. Estimate species-specific trigger and final-entry probabilities from the other positions. Correct held-out badger composition using self-normalized IPW and compare with a species-swapped sham. This is a retrospective secondary-endpoint test of position transport, not independent-animal confirmation.

## 3. Results

### 3.1 External reference information exposes a record world that the event log cannot audit

The deterministic witness confirms that the biological composition of non-entered exposures is not identified from an event table alone. Both empirical systems provide the missing external structure: continuous audio in BirdVox and CCTV-observed true passes in Findlay.

### 3.2 Record entry selectively changes ecological composition

Among 881 CCTV-confirmed fox/badger passes, 51.4% did not trigger. The bounded probability of failing to become a confirmed capture was approximately 80.0–80.2%. These losses were not composition-neutral. Badgers represented 35.98% of true passes, 43.93% of triggered records and 48.28% of confirmed captures.

The otter system showed a second structured composition shift. Wet passes had greater trigger loss than dry passes for all three camera model/settings. Consequently, wet representation declined from 43.80% to 27.03% for A, 45.98% to 37.88% for BS, and 44.58% to 34.67% for BV. Thus the observation process changed the biological composition available to downstream analysis before any later classification step.

### 3.3 Perfect downstream semantics cannot reconstruct upstream-erased information

In protected BirdVox units 02/05, the true late-minus-early event-window prevalence contrast was +0.130820. Under the frozen z=2 entry rule, restricting analysis to true positive windows that had actually entered produced an oracle downstream contrast of approximately -0.000025. Removing downstream false entries therefore did not restore the true temporal signal: the missing biological information had already been removed upstream.

The magnitude of omission in this experiment should not be generalized to competent acoustic detectors because the frozen annotation-naive score generalized poorly. The result is a stress test of irreversibility, not a detector-performance estimate.

### 3.4 Entry-aware correction helps within some calibration domains

In the matched-context wet/dry camera holdout, entry-aware weighting reduced mean absolute composition error from 0.115982 to 0.059258, a 48.91% reduction, with improvement in all three held-out camera model/settings.

The independent species-composition endpoint also showed average recovery across held-out physical positions. At the trigger stage, species-specific weighting reduced mean absolute error from 0.123093 to 0.090510 (26.47%), improving three of four positions. At final capture, error declined from 0.210807 to 0.167972 (20.32%), again improving three of four positions. Correct weighting beat the species-swapped sham in three of four positions at both stages.

### 3.5 Correction does not transport automatically across observation contexts

The frozen wet/dry camera-plus-position double holdout reversed the positive matched-context result. Across 12 camera × position cells, raw mean absolute error was 0.068216 whereas correct IPW error was 0.081237, a 19.09% increase. Correct IPW improved only six of 12 cells, although it remained substantially better than the direction-reversed sham overall (sham MAE 0.153652). Camera A improved strongly, whereas BS and BV worsened; BL and C positions improved while A and BW worsened. Worst-case propagation of unresolved trigger states did not reverse the adverse aggregate result.

A post-result exploratory within-camera position holdout produced only a small 5.81% average error reduction and improved six of 12 cells. The fox/badger second endpoint also contained a consistent adverse position: SF worsened at both trigger and final-capture stages and was better served by the sham direction. Together these results show that entry-aware correction can be useful while its transport remains observation-context dependent.

## 4. Discussion

### 4.1 The event table is a measurement product, not the biological denominator

The central empirical result is not that camera traps or acoustic detectors miss events. It is that the process determining which events become records can alter the ecological composition or contrast available to later analysis. Once this occurs, treating the final event table as though it were merely a smaller random sample of the exposure world can change the ecological estimand itself.

### 4.2 Upstream and downstream observation errors are not interchangeable

The BirdVox oracle analysis demonstrates why improving downstream classification is insufficient when true events never enter the analysed record. Classification methods can improve semantic accuracy among available rows; they cannot reconstruct omitted rows without additional measurements or assumptions. This distinction motivates preserving pre-entry evidence rather than treating observation quality as a single downstream classifier metric.

### 4.3 Recovery requires a calibrated observation domain

The recovery experiments provide both constructive and adverse evidence. Under a matched observation context, entry-aware weighting substantially reduced wet-composition error. A second species-composition endpoint also showed average improvement across held-out positions. Yet the deliberately harder camera-plus-position transport test failed. The implication is not that entry-aware correction is ineffective, but that the entry probability used for correction is itself conditional on observation context.

This is important for automated monitoring practice. A detection or entry probability estimated for one hardware, placement or environmental regime should not be exported as though it were an intrinsic property of the animal or behaviour. Correction models require the same type of transport validation that would be expected of any predictive model.

### 4.4 A practical record-entry measurement contract

The analyses suggest a practical data-design principle. Automated monitoring should preserve, where feasible, an exposure denominator independent of the event detector, pre-entry evidence or diagnostics, gate and archive-entry provenance, unresolved operational states, and independent truth audits that include non-entered exposures. If correction is applied, the calibration context and validated transport domain should also be stored.

These records are often discarded because the final event table is treated as the scientific dataset. Our results show that they are precisely the information required to diagnose whether the event table has changed the ecological estimand and whether any proposed correction is transferable.

### 4.5 Boundaries

The component false-negative processes measured here are established in the detection literature and are not presented as new biological phenomena. The Findlay recovery analyses are retrospective and do not provide independent-animal or prospective confirmation. BirdVox uses expert truth within recorded audio and therefore tests algorithmic entry, not calls physically absent from the microphone signal. The next strongest test is a prospectively frozen exposure/reference and calibration design evaluated once on physically independent held-out field data.

## 5. Conclusion

Ecological records can be selectively transformed before downstream analysis begins. External exposure or reference data make that selection auditable, and the resulting differences can be large enough to change ecological composition and temporal contrasts. Preserving record-entry provenance can enable partial correction, but correction performance is not invariant across observation contexts. The calibration and transport domain of the observation process should therefore be treated as part of the ecological measurement model rather than as an implementation detail of the sensor.
