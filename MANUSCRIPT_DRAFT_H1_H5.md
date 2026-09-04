# Manuscript draft — REC H1–H5 external-data paper

## Working title

**Auditing record-entry selection reveals ecological estimand distortion and limits to correction transport**

## Abstract

Automated ecological monitoring usually begins analysis from records produced by sensors, although the process determining which biological events become records can itself be selective. Imperfect detection is well established, but an event table alone cannot reveal the biological composition of exposures that never became rows, making it difficult to determine when pre-entry loss changes the ecological estimand available to downstream analysis. We treated record entry as an auditable measurement process and evaluated it in two observation systems with external exposure or reference information: CCTV-referenced camera-trap passes and continuous expert-annotated acoustic recordings. In the camera-trap system, 51.4% of independently observed fox and badger passes failed to trigger and approximately 80.0–80.2% failed to become confirmed captures. This selection changed species composition before downstream classification: badger representation increased from 0.360 among true passes to 0.439 after triggering and 0.483 among confirmed captures. The distortion remained after standardizing reference and recorded worlds to the same physical camera-position distribution, with standardized badger shifts of +0.053 to +0.062 at trigger and +0.140 to +0.150 at final capture. Wet/dry otter analyses provided a second state-dependent mechanism for two camera settings, but a third setting lost its pooled wet-underrepresentation after position standardization, demonstrating context dependence. In protected continuous-acoustic data, a true late-minus-early event-window contrast of +0.131 was almost eliminated after upstream selection even when downstream semantic classification was assumed to be oracle-perfect, showing that downstream accuracy cannot reconstruct omitted rows. Retaining entry-process information nevertheless enabled partial recovery: entry-aware weighting reduced wet-composition error by 48.9% in a matched-context camera holdout and reduced fox/badger species-composition error by 26.5% at trigger and 20.3% at final capture across held-out positions on average. However, a frozen camera-plus-position double holdout increased wet-composition error by 19.1%. Ecological event tables are therefore selected measurement products rather than neutral subsets of biological events, and both the entry process and any correction have an observation-context domain that must be measured and validated.

## 1. Introduction

### 1.1 The problem starts before downstream analysis

Ecological sensors increasingly convert continuous biological activity into discrete event records that are subsequently classified, summarized and modelled. The statistical consequences of imperfect detection are well established, and extensive work has shown that environmental conditions, animal behaviour, sensor hardware and algorithmic thresholds affect whether events are detected. Yet most downstream workflows still begin from the event table produced by the observation system. Once analysis starts from those rows, events that never became records are absent not only from the response variable but from the dataset itself.

This creates an estimand problem in addition to a detection problem. The relevant question for downstream ecology is not only whether events were missed, but whether the process selecting events into the record changes the ecological quantity that the recorded data appear to estimate. If entry probability covaries with biological state, environmental condition or sensor context, record loss can alter composition, temporal contrasts or other estimands rather than merely reducing sample size.

### 1.2 Why an external exposure or reference world is required

An event log cannot empirically characterize the biological content of rows that were never created. Studying pre-entry selection therefore requires a denominator or reference world defined independently of the tested record-entry rule. Such a design may be provided by continuous recordings, synchronized reference sensors, fixed exposure clocks or independent observer systems. Missing or unresolved reference states must remain explicit rather than being converted to biological negatives.

We use the term **record-entry selection** for the measurable process between an independently defined exposure/reference world and the usable event table. The terminology is not intended to rename imperfect detection as a new phenomenon. Instead, it specifies the measurement information required to connect known detection failures to their downstream ecological consequence.

### 1.3 From distortion to transportable recovery

If record entry is selective, retaining its provenance may create an opportunity for correction. However, a correction model is useful only if the entry probabilities estimated during calibration remain meaningful in the target observation context. Entry probability should therefore not be assumed to be an invariant property of a species, behaviour or event. Its transport across sensor hardware, placement and environmental context is itself an empirical question.

This leads to three linked questions. First, can an external exposure/reference design reveal true biological events that are absent from the tested record? Second, does structured entry selection change ecological estimands within observation strata rather than only through aggregate sampling composition, including after downstream classification is made arbitrarily accurate? Third, can entry-process information reduce that distortion outside the data used to estimate selection, and over what observation domain does such correction transport?

### 1.4 Study design

We addressed these questions using two complementary systems. Findlay et al.'s camera-trap/CCTV data provide independently observed mammal passes followed by physical trigger and capture outcomes, allowing direct measurement of pre-entry selection and ecological composition changes. We use fox/badger species composition as the primary ecological endpoint because its distortion can be tested after standardizing reference and recorded worlds to the same physical camera-position distribution. Otter wet/dry state supplies a mechanistic second system and a series of correction-transport tests. BirdVox-full-night provides a continuous acoustic exposure universe with expert call annotations, allowing a protected algorithmic stress test in which upstream omission can be separated from a hypothetical oracle-perfect downstream semantic stage.

Our contribution is therefore not the observation that sensors miss events. It is an empirical measurement chain linking external reference truth, record-entry selection, within-context ecological estimand distortion, downstream irreversibility, and the conditions under which entry-aware recovery does or does not transport.

## 2. Methods

### 2.1 General measurement framework

For each system, define an exposure/reference universe independently of the tested event-entry rule. Distinguish biological truth, gate/trigger state, final usable record entry and downstream semantic processing. Treat unresolved reference or operational states as unresolved and report bounds where appropriate.

Primary comparison:

`reference ecological estimand -> recorded ecological estimand`.

Recovery comparison:

`reference -> raw record -> entry-aware corrected record -> falsification/sham correction`.

### 2.2 Event-log identifiability witness

We use a deterministic construction showing that identical observed event logs are compatible with different biological compositions of the non-entered world. This motivates the need for external exposure/reference information and is not presented as a new missing-data theorem.

### 2.3 Findlay camera-trap reference system

The analyses use the public CT-Detection repository at a pinned upstream commit and Git-blob identity. The wild fox/badger experiment provides CCTV-confirmed passes followed by Bushnell-video trigger and final capture outcomes at four physical camera-trap positions. The captive otter experiment provides CCTV-confirmed passes evaluated by three camera model/settings across four physical positions.

For fox/badger, a confirmed non-trigger implies no final camera record from that pass. Missing trigger or capture states remain unresolved at their respective process stage and are not silently coded as failures. The released rows are treated as pass-camera observations, not as independent animals or population replicates.

### 2.4 Primary ecological endpoint: fox/badger species composition

The primary estimand is the badger proportion among independently observed fox/badger passes. We compare this reference composition with badger composition among confirmed triggered records and among confirmed captures.

To test whether pooled composition shifts are explained only by changes in the mixture of physical camera positions, we calculate truth and recorded badger composition within each CT position and then standardize both worlds to the same position distribution using two prespecified schemes: equal weight per evaluable CT position and weights defined by the reference-pass position distribution. We also report the direction of species-specific entry-probability differences and composition shifts within each position. We do not use row-level significance tests that would treat repeated passes as independent biological individuals.

### 2.5 Otter wet/dry mechanism and aggregation robustness

The secondary mechanistic estimand is the wet proportion among independently observed otter pass-camera observations. We compare wet and dry trigger probabilities and the wet composition of reference versus triggered records for camera settings A, BS and BV.

We repeat the composition comparison within CT position and standardize reference and triggered worlds to the same position distribution using the same two weighting schemes. This distinguishes a position-robust biological-state selection pattern from a pooled contrast generated partly by the joint distribution of wet/dry state and physical position.

### 2.6 BirdVox protected irreversibility stress test

We define one-second exposure windows from continuous audio duration before applying the frozen annotation-naive score gate. Unit10 remains the pilot; units 02/05 are protected replication units. The frozen gate generalized poorly and is not treated as a representative detector benchmark.

We compute the true late-minus-early event-window prevalence contrast, the contrast after record-entry selection, and an oracle true-entry-only contrast in which downstream false entries are removed. The oracle comparison asks whether perfect downstream semantics could restore truth after upstream omission.

### 2.7 Matched-context wet/dry recovery

We leave one camera model/setting out, estimate wet/dry trigger propensities from the other camera streams, and apply self-normalized inverse-probability weighting to the held-out triggered composition. Absolute error is calculated against the CCTV pass composition. Because colocated cameras share the broader encounter context, this test evaluates hardware transport within a matched observation domain rather than independent encounter transport.

### 2.8 Frozen camera-plus-position transport test

For each held-out camera × CT-position cell, propensities are estimated only from rows using neither the held-out camera nor the held-out physical position. We compare raw composition, correct wet/dry IPW and a swapped-direction sham IPW. Results are aggregated by held-out camera and position without treating cells as independent animals. Unresolved training trigger states are propagated through propensity bounds.

### 2.9 Fox/badger second-endpoint recovery

Within the single Bushnell-video system, we leave one physical CT position out, estimate species-specific trigger and final-entry probabilities from the other positions, and correct held-out badger composition using self-normalized IPW. A species-swapped sham provides a falsification comparator. This is a retrospective position-transport analysis, not independent-animal or prospective confirmation.

## 3. Results

### 3.1 External reference information exposes a record world that the event log cannot audit

The deterministic witness confirms that the biological composition of non-entered exposures is not identified from an event table alone. Both empirical systems provide the missing external structure: CCTV-observed true passes in Findlay and continuous audio in BirdVox.

### 3.2 Species-selective record entry changes composition within camera positions

Among 881 CCTV-confirmed fox/badger passes, 51.4% did not trigger. The bounded probability of failing to become a confirmed capture was approximately 80.0–80.2%. Badgers represented 35.98% of true passes, 43.93% of triggered records and 48.28% of confirmed captures.

The direction remained after standardizing reference and recorded worlds to the same CT-position distribution. At the trigger stage, equal-position standardization gave a truth badger proportion of 0.3674 and a recorded proportion of 0.4298, a shift of +0.0624; reference-pass weighting gave a shift of +0.0535. At final capture, the corresponding standardized shifts were +0.1498 and +0.1399. Three of four physical positions showed positive badger composition shifts and positive badger-minus-fox entry-probability differences at both stages; SF was the retained adverse position.

Thus the species-composition distortion is not produced merely by changing the mixture of physical CT positions. Differential record entry within position contributes directly to the changed ecological estimand.

### 3.3 The wet/dry mechanism is real but observation-context dependent

The pooled otter data showed wet underrepresentation in triggered records for all three camera settings, but position standardization separated robust from aggregation-sensitive cases.

For camera A, wet composition remained lower after standardization under both weighting schemes: the standardized recorded-minus-truth shift was -0.1270 under equal-position weighting and -0.1348 under reference-pass weighting, with the negative direction in all four positions. For BV, the shifts were -0.0464 and -0.0525, with the negative direction in three of four positions.

BS did not retain the pooled pattern. The standardized shifts were +0.0030 under equal-position weighting and +0.0009 under reference-pass weighting, with two positions negative and two positive. The earlier pooled BS wet underrepresentation therefore cannot be interpreted as a position-invariant wetness effect. This adverse case demonstrates that the operating entry-selection function itself can depend on observation layout.

### 3.4 Perfect downstream semantics cannot reconstruct upstream-erased information

In protected BirdVox units 02/05, the true late-minus-early event-window prevalence contrast was +0.130820. Under the frozen z=2 entry rule, restricting analysis to true-positive windows that had actually entered produced an oracle downstream contrast of approximately -0.000025. Removing downstream false entries therefore did not restore the true temporal signal: the missing biological information had already been removed upstream.

The magnitude of omission in this experiment should not be generalized to competent acoustic detectors because the frozen annotation-naive score generalized poorly. The result is a stress test of irreversibility, not a detector-performance estimate.

### 3.5 Entry-aware correction helps within some calibration domains

In the matched-context wet/dry camera holdout, entry-aware weighting reduced mean absolute composition error from 0.115982 to 0.059258, a 48.91% reduction, with improvement in all three held-out camera settings.

The species-composition endpoint also showed average recovery across held-out physical positions. At the trigger stage, species-specific weighting reduced mean absolute error from 0.123093 to 0.090510 (26.47%), improving three of four positions. At final capture, error declined from 0.210807 to 0.167972 (20.32%), again improving three of four positions. Correct weighting beat the species-swapped sham in three of four positions at both stages. The same adverse position, SF, worsened at both stages.

### 3.6 Correction does not transport automatically across observation contexts

The frozen wet/dry camera-plus-position double holdout reversed the positive matched-context result. Across 12 camera × position cells, raw mean absolute error was 0.068216 whereas correct IPW error was 0.081237, a 19.09% increase. Correct IPW improved only six of 12 cells, although it remained substantially better than the direction-reversed sham overall (sham MAE 0.153652). Camera A improved strongly whereas BS and BV worsened; BL and C positions improved while A and BW worsened. Worst-case propagation of unresolved trigger states did not reverse the adverse aggregate result.

A post-result exploratory within-camera position holdout produced only a small 5.81% average error reduction and improved six of 12 cells. Together with the BS standardization result and the adverse fox/badger SF position, the transport analyses show that entry-aware correction can be useful while both the selection function and its correction remain observation-context dependent.

## 4. Discussion

### 4.1 The event table is a selected measurement product

The central empirical result is not that camera traps or acoustic detectors miss events. It is that the process determining which events become records can alter an ecological estimand before downstream analysis begins. The fox/badger result remains after reference and recorded worlds are standardized to the same physical camera-position distribution, showing that the effect is not solely an aggregate mixture artifact.

### 4.2 Observation context can change the selection function itself

The otter results reveal why pooled detection contrasts require care. A and BV retain wet underrepresentation within standardized position distributions, whereas BS does not. Thus a biological label such as wet/dry does not carry a universal entry probability independent of sensor placement and context. The observation system and biological state jointly define the operating selection process.

### 4.3 Upstream and downstream observation errors are not interchangeable

The BirdVox oracle analysis demonstrates why improving downstream classification is insufficient when true events never enter the analysed record. Classification methods can improve semantic accuracy among available rows; they cannot reconstruct omitted rows without additional measurements or assumptions. This distinction motivates preserving pre-entry evidence rather than treating observation quality as a single downstream classifier metric.

### 4.4 Recovery requires a calibrated observation domain

The recovery experiments provide both constructive and adverse evidence. Under a matched observation context, entry-aware weighting substantially reduced wet-composition error. Species-specific correction also reduced average fox/badger composition error across held-out positions. Yet the deliberately harder simultaneous camera-plus-position transport test failed, and adverse individual contexts recurred across endpoints.

The implication is not that entry-aware correction is ineffective. It is that the entry model is itself conditional on observation context. A selection model estimated for one hardware, placement or environmental regime should not be exported as though it were an intrinsic property of the animal, species or behaviour. Correction models require explicit transport validation.

### 4.5 A practical record-entry measurement contract

Automated monitoring should preserve, where feasible, an exposure denominator independent of the event detector, pre-entry evidence or diagnostics, gate and archive-entry provenance, unresolved operational states, and independent truth audits that include non-entered exposures. If correction is applied, the calibration context and validated transport domain should also be stored.

These records are often discarded because the final event table is treated as the scientific dataset. Our results show that they are precisely the information required to diagnose whether the event table has changed the ecological estimand and whether a proposed correction is transferable.

### 4.6 Boundaries

The component false-negative processes measured here are established in the detection literature and are not presented as new biological phenomena. The Findlay recovery analyses are retrospective and do not provide independent-animal or prospective confirmation. CT positions are observation strata, not population replicates. BirdVox uses expert truth within recorded audio and therefore tests algorithmic entry, not calls physically absent from the microphone signal. The next strongest test is a prospectively frozen exposure/reference and calibration design evaluated once on physically independent held-out field data.

## 5. Conclusion

Ecological records can be selectively transformed before downstream analysis begins. External exposure or reference data make that selection auditable, and position-standardized camera-trap results show that the resulting selection can change species composition within observation strata rather than merely through aggregate sampling composition. Preserving record-entry provenance can enable partial correction, but neither the selection function nor correction performance is invariant across observation contexts. The calibration and transport domain of the observation process should therefore be treated as part of the ecological measurement model rather than as an implementation detail of the sensor.