# MEE submission text — REC H1–H5

Status: **draft submission components; do not submit until repository licence and Findlay data-permission blockers are resolved.**

## Candidate title

**Record-entry selection changes ecological estimands and limits the transport of detection correction**

Alternative:

**Auditing ecological record entry reveals estimand distortion and context-bounded recovery**

## Numbered abstract

**1.** Ecological methods account for imperfect detection, but automated monitoring often preserves only event records that survive sensor triggering, registration and retention. A final event table cannot reveal the biological composition of exposure opportunities that never became rows. We developed an auditable record-entry contract linking an externally defined exposure/reference world to pre-entry selection, the ecological estimand represented by retained records, downstream semantic error and correction transport.

**2.** We evaluated the contract in two systems with external reference information. CCTV-referenced camera-trap data provided true fox/badger and otter passes before physical trigger/capture, while protected continuous BirdVox recordings provided an acoustic exposure grid with expert event truth. We compared reference and recorded estimands, standardized camera-trap composition to common physical-position distributions, constructed an oracle downstream semantic stage, and evaluated entry-aware inverse-probability correction under harder held-out contexts with direction-swapped sham controls.

**3.** Among 881 CCTV-confirmed fox/badger passes, 51.4% failed to trigger and approximately 80.0–80.2% failed to become confirmed captures. Badger representation increased from 0.360 among reference passes to 0.439 after triggering and 0.483 after confirmed capture; distortion persisted after standardizing both worlds to the same camera-position distribution. Otter wet/dry selection remained after position standardization for two camera settings but disappeared for a third. In protected acoustic data, a reference late-minus-early contrast of +0.131 was nearly eliminated after upstream selection even with oracle-perfect downstream semantics. Entry-aware correction reduced composition error by 48.9% in a matched-context otter holdout and by 26.5% and 20.3% for fox/badger trigger and final-capture composition across held-out positions, but a frozen camera-plus-position transport test worsened otter error by 19.1%.

**4.** Ecological event tables are selected measurement products rather than neutral subsets of biological events. Preserving exposure denominators, entry provenance and independent reference audits makes selection diagnosable and can support partial correction, but both the selection function and its correction have an observation-context domain that must be tested. The contract complements occupancy and classification-error models by retaining the pre-entry information needed to determine what ecological estimand downstream methods receive.

Word count of the numbered abstract text: approximately **325 words**.

## Keywords

1. acoustic monitoring
2. automated monitoring
3. camera traps
4. ecological estimands
5. imperfect detection
6. observation process
7. sensor bias
8. transportability

## Data/Code for peer review statement — draft

All analysis code, validation scripts, schemas, machine-readable result summaries and figure-generation workflows are maintained in the public version-controlled repository `zuizui0223/rec`. Analyses pin external source versions and verify source-file identities before execution. The BirdVox-full-night source data are publicly archived on Zenodo under CC BY 4.0. The camera-trap reanalysis uses the public `melaniefindlay/CT-Detection` repository and downloads the source CSV files from their original location rather than redistributing them. **Written reuse/licence clarification from the Findlay data owner is being obtained before full manuscript submission.** A permanent version-of-record archive of the analysis repository should be created for the accepted/submitted release once the software licence has been chosen.

## Data availability statement — submission-ready template after rights resolution

The analyses use two previously collected third-party datasets. BirdVox-full-night v3.0 is available from Zenodo (doi: `10.5281/zenodo.1205569`) under the Creative Commons Attribution 4.0 International licence. The Findlay camera-trap/CCTV source tables are hosted in the public `melaniefindlay/CT-Detection` repository; the analyses use immutable commit `abc72f535bb59ebed202fb7acca852fc1647e97a` and verify the Git blob identity of each source table before analysis. [INSERT documented reuse-permission/licence statement after confirmation.] The REC analysis code, schemas, tests and derived machine-readable summaries will be archived at [INSERT permanent DOI/version archive] and are developed under [INSERT chosen open-source software licence].

## Code availability statement — template

The complete analysis and validation code is available in the version-controlled REC repository and will be archived as a DOI-bearing version of record at submission/acceptance. The repository includes deterministic schema validators, pinned external-data workflows, correction/transport tests, machine-readable results and scripts that regenerate manuscript figures from committed evidence. Code is released under [INSERT chosen open-source licence].

## MEE-specific remaining fields

### Running headline ≤45 characters

Candidate:

**Auditing ecological record entry**

### Author contributions

Pending final author list. Do not infer contributions from repository commits alone.

### Acknowledgements

Must distinguish:

- original data creators/collectors;
- REC reanalysis authors;
- any permission/communication from Findlay et al.;
- BirdVox dataset creators and required attribution.

### Ethics statement

The manuscript is a secondary analysis of previously released data and does not itself conduct new animal manipulation. Confirm whether the journal requests the original source-study permit/ethics information to be summarized or only cited; do not invent permit numbers not present in the source papers.

## Submission blockers

- [ ] explicit open-source REC software licence chosen and added;
- [ ] written Findlay data reuse/licence clarification obtained;
- [ ] permanent archived release/DOI planned;
- [ ] final author list and contribution statements completed;
- [ ] final word count checked against MEE Standard Article limit;
- [ ] MEE pre-submission enquiry sent and response reviewed.
