# Paper 2 preregistration draft — observation coarsening and field ecological inference

Status: **design draft; not preregistered, not yet data-frozen**.

This file defines what must be frozen before confirmatory field labels are inspected. It is intentionally conservative: pilot data may inform sample-size and logistics decisions but may not be mixed into the confirmatory held-out test.

## 1. Primary question

For the same real ecological observation windows, does preserving independently calibrated B/T/N/U observation-process states recover a reference-truth ecological estimand better than early target/not-target coarsening?

Paper 2 also contains a distinct upstream Chapter-2 question: does the registered-deviation gate absorb real events into B before B/T/N/U is formed? Chapter 1 and Chapter 2 must be analyzed separately before their consequences are combined.

## 2. Primary estimand

For ecological unit `g` containing fixed-exposure observation windows `i=1..n_g`, define reference-truth target-event prevalence

`theta_g = (# reference-truth target-positive windows) / (# reference-truth resolved windows)`.

Windows with unresolved reference truth are excluded from both numerator and denominator and their fraction is reported.

The ecological unit must be frozen before confirmatory scoring. Preferred grouping for System A is `site × day` or `focal scene × recording day`; frame-level units are forbidden.

## 3. Observation records under comparison

Both records are constructed from the same primary sensor stream and the same frozen evidence adapters.

### Comparator A — binary

`TARGET / not-TARGET`.

The binary record is a deterministic coarsening of the process-resolved record. Its exact mapping must be frozen before held-out analysis.

### Comparator B — process resolved

`B / T / N / U`.

Finer U reasons may be retained as metadata but are not a primary inferential comparator. Paper-1 D5 prohibits treating category count or reason labels as intrinsically informative.

## 4. Independent truth protocol

The tested observer cannot access the reference channel.

For every sampled window the truth table contains:

- `target_truth`: positive / negative / unresolved;
- `nuisance_truth`: zero or more predeclared nuisance families / unresolved;
- `observability_truth`: observable / compromised / unobservable / unresolved;
- `coupled_response_truth`: positive / negative / unresolved, if applicable;
- `attribution_truth`: supported / unsupported / unresolved, if applicable.

Annotation is blind to algorithm scores, TNOA decisions and binary comparator output.

For Chapter 2, the truth sample must deliberately include registered-B windows. Reference annotators should also be blind to the tested pre-gate score/gate result whenever practical.

At least one protected subset is independently double-annotated and adjudicated. Inter-annotator agreement is reported but is not used to silently convert unresolved truth to negative truth.

## 5. Development / held-out split

Splitting is performed before calibration at an independent grouping level, not by frame.

Preferred grouping hierarchy:

1. recording day;
2. focal scene / camera placement;
3. continuous recording block.

No group may contribute windows to both development and held-out sets.

Calibration, threshold selection, nuisance-family definitions, observability criteria, registered-deviation gate rules and any Chapter-2 correction method use development groups only.

## 6. Pilot phase and sample-size freeze

The pilot exists only to estimate:

- target-event rate;
- nuisance-family frequencies;
- unresolved-reference-truth rate;
- annotation time per window;
- variance of unit-level prevalence error;
- expected number of independent ecological units per field day;
- frequency of reference-positive registered-B windows;
- event-absorption frequency among reference-positive windows;
- prevalence of candidate Chapter-2 measurement strata;
- sampling fraction required to annotate B without reviewing every B window.

After the pilot, freeze a power/simulation-based sample-size rule for the paired unit-level primary comparison and a separate precision/sample-size rule for Chapter-2 baseline contamination/event absorption. Pilot ecological units are excluded from the confirmatory held-out test.

Do not choose final sample size by looking at confirmatory effect direction.

## 7. Chapter-1 primary endpoint

For each held-out ecological unit `g`, derive an estimate `theta_hat_g` from each observation record using the same prespecified downstream analysis class.

Primary loss:

`L_g = |theta_hat_g - theta_g|`.

Primary contrast:

`Delta_g = L_binary,g - L_process,g`.

Positive `Delta` favours preserving B/T/N/U.

The primary inferential analysis is a paired group-level comparison with uncertainty obtained by resampling **independent ecological units**, not windows/frames. The exact estimator (paired bootstrap, hierarchical model or permutation-compatible paired statistic) must be frozen after the pilot and before confirmatory labels are inspected.

Report the full effect estimate and interval; do not reduce the result to a binary p-value.

## 8. Secondary endpoints

Prespecified secondary endpoints:

1. Spearman/Pearson rank agreement between estimated and reference-truth unit prevalence;
2. number and magnitude of pairwise unit-rank reversals;
3. absolute error stratified by independently labelled nuisance presence;
4. absolute error stratified by observability truth;
5. false biological-absence declarations where reference truth is target-positive;
6. review/annotation time and calibration sample count for each observation vocabulary.

Annotation burden is a separate outcome. Do not combine information and cost into a scalar utility without a separately declared utility function.

## 9. One ecological conclusion test

Before confirmatory labels are unblinded, choose exactly one ecological contrast that is scientifically meaningful in System A and estimable from reference truth, for example:

- habitat A versus habitat B;
- morning versus afternoon;
- treatment versus control;
- high versus low environmental stratum.

Fit the same downstream model to:

1. reference truth;
2. thresholded/process-resolved observation record;
3. binary observation record;
4. a Chapter-2 uncertainty-aware or gate-corrected record only if that method was frozen before held-out truth was opened.

Primary interpretation is **distance to the reference-truth effect estimate**. A sign reversal is reported if it occurs but is not required for success.

The ecological contrast cannot be selected after viewing which contrast produces the largest threshold/binary/process difference.

## 10. H2 condition map

Estimate the Chapter-1 primary error contrast separately in predeclared strata:

- no verified nuisance versus nuisance present;
- fully observable versus compromised/unobservable primary stream;
- rare-target versus common-target units, if enough independent units exist.

This section is a condition map, not a search for the most favourable subgroup. All predeclared strata are reported.

Chapter-2 measurement strata are frozen separately under Section 15 below.

## 11. System-B replication

Preferred candidate: Snapshot Serengeti expert gold standard.

Before using it confirmatorily, freeze:

- focal target or target set;
- observation unit (capture event, not individual image unless justified);
- train/development/test partition at camera/location or another independent grouping level;
- automated/raw evidence adapter used to construct target support;
- any nuisance/observability annotation protocol;
- any registered-deviation gate to be treated as a Chapter-2 object;
- primary ecological estimand (preferred: camera × temporal-block encounter prevalence);
- exact binary and process-resolved mappings.

The existing expert gold-standard subset is protected truth. If exploratory model or vocabulary development uses any gold-standard event, that event cannot remain in the confirmatory test set.

Replication success is not defined as reproducing the System-A effect size. The key report is the direction and magnitude of information loss under the independently frozen System-B design. If System B cannot support an independently defined pre-gate truth/gate analysis, Chapter 2 is not forced onto it.

## 12. Null/adverse outcomes that must remain publishable

The following do not trigger redesign of the confirmatory analysis:

- binary performs equivalently to B/T/N/U;
- binary performs better after accounting for finite calibration data;
- Chapter-2 baseline contamination is effectively zero;
- threshold-absorbed events exist but are not condition dependent;
- threshold absorption is condition dependent but does not affect the ecological conclusion;
- the ecological conclusion does not change;
- System B fails to replicate System A;
- annotation cost offsets part or all of the process-resolved information advantage.

These outcomes constrain the generality of the observation-contract principle and must be retained.

## 13. Prohibited post-hoc rescues

After held-out labels are opened, do not:

- redefine nuisance families to improve TNOA;
- merge or split U reasons to improve the primary result;
- change binary mapping;
- move windows between development and held-out groups;
- change the primary ecological unit;
- replace the primary estimand;
- choose a different ecological contrast because it reverses sign;
- add a new score threshold selected on held-out truth;
- change the Chapter-2 event definition or registered-deviation gate;
- choose new Chapter-2 condition strata because they maximize absorption differences;
- tune a Chapter-2 correction on held-out truth and call it confirmatory;
- discard difficult/reference-unresolved cases without reporting their rate.

## 14. Promotion rule for an above-MEE paper

A stronger-journal submission is justified only if the final evidence includes:

- independent field truth in System A;
- a frozen held-out field comparison;
- direct truth annotation of registered-B windows;
- a real ecological estimand and one prespecified ecological conclusion test;
- explicit finite-calibration/annotation burden;
- independent System-B replication or an equivalently strong external validation.

Otherwise the field work should be reported as a separate validation study and should not delay the frozen MEE Paper 1.

---

## 15. Chapter 2 confirmatory module — threshold censoring

Full scientific rationale: `CHAPTER2_THRESHOLD_CENSORING.md`.

### 15.1 Registered-baseline semantics

Freeze the statement:

`B = no registered deviation under the frozen primary-stream rule`.

Do not define B as biological no-event or absence.

### 15.2 Chapter-2 variables

For each held-out reference-resolved window:

- `E`: independent event truth, positive/negative;
- `R`: registered-deviation gate result, 1 deviation / 0 B;
- `S`: retained pre-gate primary-stream evidence;
- `gate_version`: frozen scalar/composite rule identifier.

Primary Chapter-2 event:

`threshold_absorbed = 1[E=1 and R=0]`.

### 15.3 Primary Chapter-2 estimands

1. Baseline contamination:

`q_B = P(E=1 | R=0, reference truth resolved)`.

2. Event absorption:

`a = P(R=0 | E=1, reference truth resolved)`.

3. Ecological-unit absorption burden:

`A_g = P(R=0 | E=1, ecological unit g)`.

All are estimated with uncertainty at the independent ecological-unit level.

### 15.4 Chapter-2 sampling design

The confirmatory truth sample must include B windows by design.

If B is too common for exhaustive annotation, freeze a stratified sampling scheme before truth annotation. Preserve for every sampled window:

- sampling stratum;
- inclusion probability;
- sampling weight;
- ecological unit;
- registered B/deviation state.

Population-level `q_B` estimates must respect the frozen sampling design.

### 15.5 Chapter-2 condition strata

After pilot feasibility and before confirmatory labels are opened, freeze a small set of independently measurable strata. Preferred order of consideration:

1. reference-rated observability;
2. occlusion;
3. target image scale/distance proxy;
4. illumination/exposure;
5. masking/background motion;
6. one ecological covariate tied to the prespecified ecological contrast.

Do not retain a candidate merely because pilot data show a large effect; retain it only if independently measurable, biologically/measurement-wise interpretable and sufficiently populated for confirmatory estimation.

### 15.6 Chapter-2 primary contrasts

For each frozen stratum `X`, estimate

`a(X=x) = P(R=0 | E=1, X=x)`.

Report pairwise/structured differences with intervals. The primary interpretation is effect magnitude and condition map, not a search for a significant subgroup.

### 15.7 Gate sensitivity

If more than one gate is evaluated, all gate versions must be frozen before held-out truth is opened and applied to the **same retained pre-gate evidence stream**.

Report for each gate:

- `q_B`;
- event absorption `a`;
- registered-deviation burden;
- downstream ecological error;
- annotation/review burden if gate choice changes review volume.

Do not select the “best” gate on confirmatory truth and then present it as predeclared.

### 15.8 Chapter-2 ecological consequence

For the single prespecified ecological contrast, estimate the reference-truth effect first. Then compare the distance of:

- the frozen thresholded record;
- any frozen Chapter-2 uncertainty-aware/corrected record;
- Chapter-1 binary and process-resolved records;

from the reference effect.

Where identifiable, decompose total observation error conceptually into:

1. upstream gate censoring;
2. downstream decision coarsening.

Do not claim exact additive decomposition unless the frozen analysis establishes it.

### 15.9 Chapter-2 success ladder

Report the highest layer supported without promoting beyond the data:

- **Layer 0:** no detectable threshold absorption;
- **Layer 1:** threshold-absorbed events exist;
- **Layer 2:** absorption is condition dependent;
- **Layer 3:** differential absorption alters a frozen ecological estimand/contrast or unit ranking relative to reference truth.

Layer 3 is the strongest above-MEE contribution; Layers 1–2 remain valid measurement results.
