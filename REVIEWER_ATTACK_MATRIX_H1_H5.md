# Reviewer attack matrix — REC H1–H5 manuscript

Status: **pre-submission pre-mortem.**

The purpose is not to write rebuttal language in advance. It is to identify which criticisms are already answered by the current design and which remain genuine limits.

## 1. "This is just imperfect detection renamed"

### Risk

High, especially at Methods in Ecology and Evolution.

### What is already conceded

- imperfect detection is foundational prior art;
- camera-trap multi-stage detection and CCTV false-negative audits are established;
- condition-dependent detectability is established;
- AI FP/FN ecological models are established.

### What the paper must show instead

- same ecological estimand before and after entry selection;
- position-standardized evidence that composition distortion is not only a pooled mixture artifact;
- oracle downstream analysis separating pre-entry loss from semantic/classification error;
- correction evaluated outside calibration rows;
- adverse transport result retained rather than tuned away.

### Action

Lead with `PAPER_METHOD_CONTRACT_H1_H5.md`, not the acronym REC.

## 2. "Findlay already published these false-negative effects"

### Risk

High if the manuscript treats raw trigger/capture loss as a discovery.

### Current answer

Findlay's original empirical process results are explicitly prior art and are used as an external reference system. The reanalysis asks different estimand questions:

- how pass-world species composition changes at trigger/capture;
- whether that shift survives common-position standardization;
- whether entry information improves held-out composition estimates;
- whether that correction transports.

### Action

Keep raw false-negative percentages brief and cite Findlay immediately.

## 3. "Rows are repeated passes, not independent animals"

### Risk

High if inferential p-values are built from rows.

### Current answer

The manuscript does not treat pass rows, camera-position cells or CT positions as independent population replicates. Results are descriptive/estimand-level and macro-averaged across observation contexts. Position-standardization and transport tests are used as robustness designs rather than pseudoreplicated biological hypothesis tests.

### Action

Retain this boundary in Methods and Discussion. Do not add row-level significance stars to figures.

## 4. "Species composition differences are just camera-position confounding"

### Risk

Originally high; now substantially reduced.

### Current answer

Frozen CT-position standardization places reference and recorded worlds under the same position distribution. Badger overrepresentation remains:

- trigger shift +0.053 to +0.062;
- final-capture shift +0.140 to +0.150;
- positive direction in 3/4 positions.

SF is retained as adverse.

### Remaining limit

Standardization addresses measured CT position, not all possible encounter-level covariates or causal species effects.

### Action

Use language "species-selective entry / species-composition distortion" rather than "causal effect of species identity".

## 5. "The otter result is cherry-picked"

### Risk

Reduced because the adverse BS result is retained.

### Current answer

After position standardization:

- A remains negative in 4/4 positions;
- BV remains negative in 3/4;
- BS collapses to approximately zero and is explicitly adverse.

### Action

Do not state all three camera settings replicate a universal wetness effect. Use otter primarily for context dependence and correction transport.

## 6. "The BirdVox detector is bad, so the result is trivial"

### Risk

High if BirdVox is presented as detector benchmarking.

### Current answer

The manuscript explicitly reports poor protected discrimination and does not generalize miss rates. BirdVox has one narrow role: after a frozen entry rule removes truth-positive windows, an oracle downstream stage that perfectly cleans existing rows still cannot reconstruct the true temporal contrast.

### Action

Keep Fig. 3 subtitle/footnote and Discussion wording focused on irreversibility, not detector quality.

## 7. "The correction result is post-hoc and not confirmatory"

### Risk

Real and cannot be removed with current data.

### Current answer

- H5 is labelled retrospective;
- the harder camera+position transport test was frozen in-repo before its result was evaluated;
- that test failed and is retained;
- sham/direction-reversed comparators are reported;
- no post-failure split is promoted to replace the adverse result.

### Remaining limit

There is no prospective physically independent correction test.

### Action

Keep prospective PolliPi/System A as future validation rather than importing it prematurely.

## 8. "IPW is standard; where is the new method?"

### Risk

High at MEE.

### Current answer

IPW is not claimed as novel. The method contribution is the observation contract defining what must be preserved before record creation so any correction can be evaluated against an external denominator and explicit transport domain.

### Action

Do not title a section "new correction method". Call it an entry-aware correction test or recovery audit.

## 9. "Correction fails under the most independent test"

### Risk

This is scientifically positive if framed correctly.

### Current answer

The simultaneous camera+position shift worsens mean error by 19.1%, while the direction-swapped sham is worse still. This identifies a calibration-domain boundary rather than universal recovery.

### Action

Make the failure central to Fig. 4 and the title/Discussion. Do not bury it as a limitation.

## 10. "Why not just fit occupancy/detection models?"

### Risk

Moderate.

### Current answer

Occupancy and detection models are complementary. They require a survey/data structure informative about the observation process. The paper asks what pre-entry provenance is needed to know how event-table construction itself selected the rows later supplied to those models, and uses external truth to compare the same estimand before and after selection.

### Action

State explicitly that the proposed audit can feed occupancy/detection models rather than replace them.

## 11. "The event-log non-identifiability witness is mathematically obvious"

### Risk

Low if kept short; high if oversold.

### Current answer

It is a design motivation, not a theorem claim.

### Action

One figure/supplement example is enough. Do not center novelty on it.

## 12. "Two sensor modalities do not establish generality"

### Risk

Real.

### Current answer

The systems play distinct roles, not statistical replications of one universal effect:

- Findlay = physical-sensor selection, composition distortion, recovery/transport;
- BirdVox = continuous-denominator digital-entry irreversibility stress test.

### Action

Use "cross-modality mechanism evidence" rather than universal sensor generality.

## 13. "Why should ecologists care about an engineering metadata problem?"

### Risk

Important editorial risk.

### Current answer

Because the retained event table changes ecological quantities:

- species composition shifts materially before classification;
- temporal contrast can collapse upstream;
- exporting a correction outside its calibration domain can increase ecological error.

### Action

Keep every methods recommendation tied to an ecological estimand, not software provenance for its own sake.

## 14. "Where is the reusable deliverable?"

### Current answer

The repository now contains:

- `PAPER_METHOD_CONTRACT_H1_H5.md`;
- exposure-ledger and truth/gate schemas;
- deterministic validators;
- pinned external-data workflows;
- correction/transport tests with sham controls;
- figure generation from committed machine-readable results.

### Action

For MEE submission, package this into a short Methods box/table and make the repository entry path obvious.

## Current readiness verdict

### Science

Strong enough for external-data manuscript drafting.

### Main unresolved weakness

Prospective correction confirmation is absent. This should be acknowledged, not patched with additional retrospective Findlay slicing.

### Highest-value remaining pre-submission work

1. finalize all four main figures and captions;
2. reduce manuscript to one reusable method + two validation systems;
3. create a one-page required/optional data-field table from the method contract;
4. choose MEE-first versus Ecological-Informatics-first strategy;
5. do not add new biological hypotheses before submission.
