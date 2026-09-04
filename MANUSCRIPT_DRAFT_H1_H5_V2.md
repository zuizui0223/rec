# Manuscript draft v2 — REC H1–H5 external-data paper

## Working title

**Record-entry selection changes ecological estimands and limits the transport of detection correction**

Alternative:

**Auditing ecological record entry reveals estimand distortion, irreversibility and context-bounded recovery**

## Abstract

Automated ecological monitoring often begins analysis from event records produced by sensors, although the process determining which biological events become records can itself be selective. Imperfect detection and context-dependent detectability are well established, but a final event table cannot reveal the biological composition of exposures that never became rows. We asked whether externally auditable record-entry selection changes the ecological estimand available to downstream analysis, whether later classification can recover information removed upstream, and whether entry-aware correction transports across observation contexts. We combined CCTV-referenced camera-trap passes with a protected continuous-acoustic stress test. Among 881 independently observed fox and badger passes, 51.4% failed to trigger and approximately 80.0–80.2% failed to become confirmed captures. Badger representation increased from 0.360 among reference passes to 0.439 after triggering and 0.483 after confirmed capture. This distortion persisted after standardizing reference and recorded worlds to the same camera-position distribution, with badger shifts of +0.053 to +0.062 at trigger and +0.140 to +0.150 at final capture. Otter wet/dry analyses corroborated state-dependent entry for two camera settings but provided an adverse third setting in which pooled wet underrepresentation disappeared after position standardization. In protected continuous-acoustic data, a true late-minus-early event-window contrast of +0.131 was almost eliminated after upstream selection even when the downstream semantic stage was made oracle-perfect. Retaining entry-process information enabled partial recovery: matched-context weighting reduced wet-composition error by 48.9%, and species-specific weighting reduced fox/badger composition error by 26.5% at trigger and 20.3% at final capture across held-out positions on average. However, a frozen simultaneous camera-plus-position transport test worsened wet-composition error by 19.1%. Ecological event tables are therefore selected measurement products rather than neutral subsets of biological events. Entry provenance can make selection diagnosable and partly correctable, but both the selection function and the transport domain of its correction must be measured rather than assumed.

## 1. Introduction

### 1.1 Imperfect detection is established; the unresolved issue is where selection enters the scientific record

Nondetection has long been distinguished from biological absence. Occupancy and related observation-process models estimate ecological state while allowing detection probability to be below one and to depend on covariates (MacKenzie et al. 2002; Guillera-Arroita 2017). Camera-trap research has likewise emphasized that wildlife surveys must link sampling design and detection processes to the ecological quantities being inferred (Burton et al. 2015), and has identified animal characteristics, camera specifications, deployment protocols and environmental variables as sources of detectability variation (Hofmeester et al. 2019).

The physical camera-trap process can itself be decomposed. Using independent CCTV reference observations, Findlay et al. (2020) separated animal passes, sensor triggering, image registration and image quality, directly demonstrating sequential false-negative processes. Palencia et al. (2022) subsequently showed under field conditions that detection probability varies with camera model, species, distance, deployment height, activation sensitivity and day/night period. These results make two points clear. First, the existence of missed events is not a new phenomenon. Second, a detection or entry probability should not be treated as an invariant property of the biological event.

A remaining practical problem arises because many automated workflows preserve only the records that survive these processes. Once analysis begins from the final event table, events that failed before record entry are absent not only from the response variable but from the dataset itself. The event table cannot, from its own rows, identify the biological composition of exposures that never became records.

### 1.2 From detection error to ecological-estimand distortion

The key ecological question is therefore not only whether events were missed, but whether entry selection changes the ecological quantity represented by the retained records. If entry probability covaries with species identity, behavioural state, environmental condition or sensor context, the retained event table need not be a smaller neutral sample of the reference world. Its composition, temporal contrast or other ecological estimand can shift before downstream modelling begins.

This distinction is especially important as automated classification becomes part of biodiversity monitoring. Recent statistical models explicitly propagate false-negative detection and probabilistic false-positive classification from AI systems into occupancy inference (Ogawa et al. 2025). Such approaches address uncertainty among observations available to the downstream classification/inference stage. They do not, by themselves, recreate biological events that never reached that stage.

We use **record-entry selection** as a descriptive term for the measurable process between an independently defined exposure/reference world and the usable event table. The term is not intended to rename imperfect detection. Its purpose is to specify the measurement information required to compare the same ecological estimand before and after pre-entry selection.

### 1.3 Correction creates a transport problem

If entry selection is measured against external reference information, the estimated entry process may be used for correction. But such correction is useful only if its calibration remains meaningful in the target observation context. Camera-trap experiments already show that detectability depends strongly on hardware and deployment conditions (Hofmeester et al. 2019; Findlay et al. 2020; Palencia et al. 2022). In parallel, automated wildlife-recognition research treats cross-location or cross-environment performance loss as domain shift. Thus transport failure itself is not a novel machine-learning principle.

The open estimand-level question is narrower: **does an entry-propensity model that diagnoses ecological composition distortion also reduce that distortion outside its calibration rows, and how quickly does that correction fail as the observation domain changes?**

### 1.4 Study questions and design

We addressed three linked questions.

1. Can external exposure/reference information make biological events outside the final event table empirically auditable?
2. Does structured record entry change an ecological estimand within observation strata, and can perfect downstream semantic accuracy repair information already removed upstream?
3. Can entry-process information reduce ecological-estimand error outside the calibration rows, and over what observation domain does that correction transport?

We used two complementary systems. The Findlay camera-trap/CCTV data provide independently observed mammal passes followed by physical trigger and capture outcomes. Fox/badger species composition is the primary ecological endpoint because its distortion can be tested after reference and recorded worlds are standardized to the same physical camera-position distribution. Otter wet/dry state supplies mechanistic corroboration, an adverse aggregation-sensitive case, and a sequence of correction-transport tests. BirdVox-full-night supplies a continuous acoustic exposure universe with expert annotations and protected units, allowing a stress test in which upstream omission is compared with an oracle-perfect downstream semantic stage.

Our contribution is therefore not the observation that sensors miss events. It is an empirical measurement chain linking external reference truth, pre-entry selection, ecological-estimand distortion, downstream irreversibility, correction and correction transport.

## 2. Methods

### 2.1 Measurement framework

For each observation system we distinguish:

`external exposure/reference -> biological event/pre-entry evidence -> trigger/gate -> usable record entry -> downstream semantics -> ecological estimand`.

The external exposure/reference universe is defined independently of the tested record-entry rule. Unresolved reference or operational states remain unresolved and are bounded where required rather than converted to biological negatives.

The primary estimand comparison is:

`reference ecological estimand -> recorded ecological estimand`.

The recovery comparison is:

`reference -> raw recorded estimate -> entry-aware corrected estimate -> falsification/sham estimate`.

### 2.2 Event-log non-identifiability witness

We use a deterministic construction in which multiple biological completions produce the same final event log while assigning different event prevalence to non-entered exposures. The construction is used only to motivate the requirement for external exposure/reference information; it is not presented as a new missing-data theorem.

### 2.3 Findlay camera-trap reference data

We reanalyse the public CT-Detection data from Findlay et al. (2020), pinned to immutable upstream commit and Git-blob identities in the repository workflows. Each released row represents an independently observed animal pass-camera observation established by the original reference design.

The wild fox/badger experiment contains CCTV-confirmed passes followed by Bushnell-video trigger and final capture outcomes at four physical camera-trap positions. The otter wet/dry experiment contains CCTV-confirmed pass-camera observations evaluated with three camera model/settings across four physical positions.

A confirmed non-trigger cannot generate a final camera record from that pass. Missing trigger or capture states remain unresolved at their respective stages. Repeated passes are not promoted to independent animals or population replicates.

### 2.4 Primary endpoint: fox/badger species composition

The primary estimand is badger proportion among CCTV-confirmed fox/badger passes. We compare the reference proportion with badger composition among confirmed triggered records and confirmed captures.

To separate within-position entry selection from changes in the mixture of physical positions, we compute reference and recorded composition within each CT position and standardize both worlds to the same position distribution using two frozen schemes:

1. equal weight per evaluable CT position;
2. weights defined by the reference-pass position distribution.

We also report the direction of species-specific entry-probability differences and composition shifts within each position. We do not use row-level tests that would treat repeated passes as independent animals.

### 2.5 Otter wet/dry mechanism and position standardization

For each otter camera setting, we compare wet and dry trigger probabilities and the wet proportion among reference versus triggered observations. We then standardize reference and triggered worlds to the same CT-position distribution under the two schemes above.

This analysis distinguishes a position-robust state-dependent entry pattern from a pooled association generated partly by the joint distribution of wet/dry state and physical camera position.

### 2.6 BirdVox protected irreversibility test

BirdVox exposure windows are defined as one-second intervals from continuous audio duration before application of the tested gate. Unit10 was inspected as a pilot. Units 02 and 05 were protected when the one-second denominator, annotation-naive score, robust scaling, thresholds and late-minus-early ecological contrast were frozen.

We report the reference late-minus-early event-window prevalence contrast, the contrast in the raw entered record and an oracle downstream contrast that retains only true-positive windows that actually entered. The oracle removes all downstream false entries but cannot add rows absent upstream.

The frozen score discriminated poorly in protected units. BirdVox is therefore interpreted as an irreversibility stress test, not as representative performance of competent acoustic detectors.

### 2.7 Matched-context wet/dry recovery

Each otter camera model/setting is held out in turn. Wet/dry trigger propensities are estimated from the other colocated camera streams and applied to the held-out triggered composition using self-normalized inverse-probability weighting. Error is the absolute difference from the CCTV pass-world wet proportion.

Because the cameras share the broader encounter context, this is a matched-context hardware-transport test, not independent encounter validation.

### 2.8 Frozen camera-plus-position transport test

For each camera × CT-position test cell, calibration excludes both the held-out camera and held-out physical position. Wet/dry propensities are therefore estimated from neither the target hardware nor target position. We compare raw composition, correct IPW and a swapped wet/dry propensity sham. Unresolved training trigger states are propagated through bounds.

This transport test was frozen in the repository before the harder result was evaluated, and its adverse result is retained unchanged.

### 2.9 Fox/badger position-transport recovery

Using the single Bushnell-video system, we leave one CT position out. Species-specific trigger probabilities and final-entry probabilities are estimated from the other three positions and used to correct the held-out badger composition. A species-swapped sham is evaluated in parallel. This is a retrospective position-transport analysis rather than prospective or independent-animal confirmation.

## 3. Results

### 3.1 External reference information makes pre-entry loss auditable

The deterministic witness shows that the biological content of non-entered exposures is not identified from the event table alone. Both empirical systems supply the missing external structure: CCTV-observed animal passes in Findlay and a continuous audio exposure universe with expert event annotations in BirdVox (Fig. 1).

### 3.2 Species-selective entry changes ecological composition within camera-position strata

Among 881 CCTV-confirmed fox/badger passes, 51.4% failed to trigger. The bounded probability of failing to become a confirmed capture was approximately 80.0–80.2%. Badgers represented 35.98% of reference passes, 43.93% of triggered records and 48.28% of confirmed captures (Fig. 2a).

The direction remained after standardizing reference and recorded worlds to the same CT-position distribution. At trigger, equal-position standardization shifted badger proportion from 0.3674 to 0.4298 (+0.0624), while reference-pass weighting gave a +0.0535 shift. At final capture, the corresponding shifts were +0.1498 and +0.1399 (Fig. 2b). Three of four positions showed positive badger composition shifts and positive badger-minus-fox entry differences at both stages; SF was adverse.

Thus the species-composition distortion is not merely a consequence of changing the mixture of camera positions. Differential entry within position changes the ecological estimand available to downstream analysis.

### 3.3 Otter wet/dry selection is context dependent

The pooled otter data initially showed wet underrepresentation for all three camera settings, but position standardization separated robust from aggregation-sensitive cases (Fig. 2c).

For camera A, standardized recorded-minus-reference wet-composition shifts were -0.1270 under equal-position weighting and -0.1348 under reference-pass weighting; all four positions had the negative direction. For BV, the shifts were -0.0464 and -0.0525, with three of four positions negative.

BS did not retain the pooled pattern. Its standardized shifts were +0.0030 and +0.0009, with two positions negative and two positive. The pooled BS association therefore does not represent a position-invariant wetness effect. This adverse case shows that the operating entry-selection function depends on observation context.

### 3.4 Perfect downstream semantics cannot restore upstream-omitted events

In protected BirdVox units 02/05, the pooled reference late-minus-early event-window prevalence contrast was +0.130820. Under the frozen z=2 gate, the raw entered contrast was -0.005034 and the oracle downstream contrast, after removing every false entered row, was approximately -0.000025 (Fig. 3). The true temporal gradient was therefore not recovered by perfect downstream semantic accuracy because the relevant true windows had already been omitted upstream.

The extreme amount of omission is system- and gate-specific: the frozen annotation-naive score generalized poorly. The result is evidence of information irreversibility after upstream omission, not a general acoustic-detector performance estimate.

### 3.5 Entry information enables partial recovery in some calibration domains

In the matched-context otter camera holdout, entry-aware weighting reduced mean absolute wet-composition error from 0.115982 to 0.059258, a 48.91% reduction, and improved all three held-out camera settings.

Fox/badger species composition independently showed average recovery across held-out positions. At trigger, species-specific correction reduced mean absolute error from 0.123093 to 0.090510 (26.47%), improving three of four positions. At final capture, error declined from 0.210807 to 0.167972 (20.32%), again improving three of four. Correct weighting beat the species-swapped sham in three of four positions at both stages. SF was adverse at both stages.

### 3.6 Correction transport fails under a harder context shift

The frozen simultaneous camera-plus-position otter holdout reversed the matched-context result. Across 12 camera × position cells, raw mean absolute error was 0.068216 and correct IPW error was 0.081237, a 19.09% increase. Only six of 12 cells improved. Correct IPW nevertheless remained much better than the direction-reversed sham overall (sham MAE 0.153652), indicating that the direction of selection contained information even though its magnitude did not transport adequately (Fig. 4).

A later explicitly exploratory within-camera position diagnostic produced only a 5.81% mean improvement and improved six of 12 cells. Together with the BS standardization result and the adverse fox/badger SF position, these results show that both selection and recovery have observation-context domains.

## 4. Discussion

### 4.1 Record-entry selection changes the estimand before ecological modelling begins

Decades of ecological methods already show why imperfect detection matters (MacKenzie et al. 2002; Guillera-Arroita 2017), and camera-trap studies explicitly document multi-stage and context-dependent detection (Hofmeester et al. 2019; Findlay et al. 2020; Palencia et al. 2022). Our contribution is not to re-establish those facts. It is to close the measurement chain between an independently observed reference world and the ecological estimand delivered by the selected event table.

The fox/badger result is central because the composition shift remains after standardizing reference and recorded data to the same physical camera-position distribution. Record entry therefore changes species composition within the observation strata rather than acting only through an aggregate change in where observations were obtained.

### 4.2 The selection function belongs to the observation context

The otter analysis shows why a single pooled detection contrast is not enough. A and BV preserve wet underrepresentation after position standardization, whereas BS does not. This agrees with prior experimental evidence that camera model, deployment, species and environmental conditions affect detectability (Hofmeester et al. 2019; Palencia et al. 2022), but extends the consequence to the ecological composition represented by retained rows.

The practical implication is that entry probability should be treated as a property of an observation system operating in a context, not as a fixed attribute of a species or behavioural state.

### 4.3 Upstream omission and downstream classification error are different measurement problems

Automated-classification models can propagate false-positive and false-negative uncertainty into ecological inference (e.g. Ogawa et al. 2025). Such methods are essential when available records are semantically uncertain. The BirdVox oracle analysis demonstrates a complementary boundary: making downstream semantics perfect cannot recreate true events that were never supplied to that stage.

The distinction is operational. Improving a classifier can alter the interpretation of existing rows; recovering upstream omission requires additional exposure/reference information or assumptions about the missing process.

### 4.4 Recovery is possible, but its transport must be validated

Entry-aware correction reduced composition error in matched or partly transported contexts and for two biological endpoints. This provides evidence that retaining entry provenance is useful for more than diagnosis. However, the correction was not universally beneficial. The frozen simultaneous camera-plus-position shift worsened error, and adverse contexts recurred in both wet/dry and species analyses.

This result should not be interpreted as a failure of correction in general. It identifies the limit of a simple transported propensity model. Detection experiments already caution against comparing different camera configurations as though their operating properties were interchangeable (Palencia et al. 2022). Our results show the corresponding estimand-level consequence: importing an entry correction outside its validated domain can increase ecological error.

The calibration provenance and transport domain of an entry model should therefore be retained as part of the ecological measurement metadata.

### 4.5 Practical measurement contract

For automated ecological monitoring, a final event table should not be the only preserved scientific product. Where feasible, monitoring systems should retain:

- an exposure/reference denominator defined independently of the tested event gate;
- pre-entry evidence or diagnostics;
- versioned trigger/gate/archive-entry provenance;
- unresolved operational states rather than forced negatives;
- independent truth audits that include non-entered exposures;
- calibration context and an explicitly tested transport domain for any correction model.

This recommendation is consistent with broader calls for transparent camera-trap methodology and observation-process-aware design (Burton et al. 2015; Hofmeester et al. 2019). The added reason is estimand-specific: these retained data determine whether record-entry selection can be diagnosed, attributed and safely corrected.

### 4.6 Limitations and scope

The Findlay component false-negative patterns are prior empirical findings, not REC discoveries. The present reanalyses use released data retrospectively and do not provide prospective independent-animal validation. CT positions are observation strata rather than population replicates. The otter experiments involve a restricted study system and should not be generalized to wild otter populations. BirdVox expert truth is defined within recorded audio and therefore evaluates algorithmic/digital entry after microphone acquisition, not biological calls physically absent from the microphone signal. Its frozen score performs poorly and is retained as an adverse stress-test gate.

The strongest next test is prospective: freeze an external exposure/reference design, calibration domain, ecological estimand and correction before opening a physically independent held-out field context. PolliPi/System A is reserved for that test and for a later same-system REC-to-TNOA decomposition.

## 5. Conclusion

Ecological event tables are selected measurement products. External exposure or reference information can reveal when pre-entry selection changes the ecological estimand represented by those records, and downstream semantic accuracy cannot restore information already omitted upstream. Retaining entry provenance can support partial recovery, but correction is not invariant across hardware and physical context. Observation-system calibration and its validated transport domain should therefore be treated as part of the ecological measurement model rather than as implementation details of the sensor.

## References used in the current positioning

- Burton, A. C., Neilson, E., Moreira, D., Ladle, A., Steenweg, R., Fisher, J. T., Bayne, E. & Boutin, S. (2015). Wildlife camera trapping: a review and recommendations for linking surveys to ecological processes. *Journal of Applied Ecology* 52:675–685. DOI `10.1111/1365-2664.12432`.
- Findlay, M. A., Briers, R. A. & White, P. J. C. (2020). Component processes of detection probability in camera-trap studies: understanding the occurrence of false-negatives. *Mammal Research* 65:167–180. DOI `10.1007/s13364-020-00478-y`.
- Guillera-Arroita, G. (2017). Modelling of species distributions, range dynamics and communities under imperfect detection: advances, challenges and opportunities. *Ecography* 40:281–295. DOI `10.1111/ecog.02445`.
- Hofmeester, T. R. et al. (2019). Framing pictures: A conceptual framework to identify and correct for biases in detection probability of camera traps enabling multi-species comparison. *Ecology and Evolution* 9:2320–2336. DOI `10.1002/ece3.4878`.
- MacKenzie, D. I., Nichols, J. D., Lachman, G. B., Droege, S., Royle, J. A. & Langtimm, C. A. (2002). Estimating site occupancy rates when detection probabilities are less than one. *Ecology* 83:2248–2255. DOI `10.1890/0012-9658(2002)083[2248:ESORWD]2.0.CO;2`.
- Ogawa, R., Gosselin, F., Darras, K. F. A., Roilo, S. & Cord, A. F. (2025). A classification-occupancy model based on automatically identified species data. *Ecology* 106:e70086. DOI `10.1002/ecy.70086`.
- Palencia, P., Vicente, J., Soriguer, R. C. & Acevedo, P. (2022). Towards a best-practices guide for camera trapping: assessing differences among camera trap models and settings under field conditions. *Journal of Zoology* 316:197–208. DOI `10.1111/jzo.12945`.
