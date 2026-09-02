# Paper 2 preregistration draft — observation coarsening and field ecological inference

Status: **design draft; not preregistered, not yet data-frozen**.

This file defines what must be frozen before confirmatory field labels are inspected. It is intentionally conservative: pilot data may inform sample-size and logistics decisions but may not be mixed into the confirmatory held-out test.

## 1. Primary question

For the same real ecological observation windows, does preserving independently calibrated B/T/N/U observation-process states recover a reference-truth ecological estimand better than early target/not-target coarsening?

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

At least one protected subset is independently double-annotated and adjudicated. Inter-annotator agreement is reported but is not used to silently convert unresolved truth to negative truth.

## 5. Development / held-out split

Splitting is performed before calibration at an independent grouping level, not by frame.

Preferred grouping hierarchy:

1. recording day;
2. focal scene / camera placement;
3. continuous recording block.

No group may contribute windows to both development and held-out sets.

Calibration, threshold selection, nuisance-family definitions and observability criteria use development groups only.

## 6. Pilot phase and sample-size freeze

The pilot exists only to estimate:

- target-event rate;
- nuisance-family frequencies;
- unresolved-reference-truth rate;
- annotation time per window;
- variance of unit-level prevalence error;
- expected number of independent ecological units per field day.

After the pilot, freeze a power/simulation-based sample-size rule for the paired unit-level primary comparison. Pilot ecological units are excluded from the confirmatory held-out test.

Do not choose final sample size by looking at confirmatory effect direction.

## 7. Primary endpoint

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
2. binary observation record;
3. process-resolved observation record.

Primary interpretation is **distance to the reference-truth effect estimate**. A sign reversal is reported if it occurs but is not required for success.

The ecological contrast cannot be selected after viewing which contrast produces the largest binary/process difference.

## 10. H2 condition map

Estimate the primary error contrast separately in predeclared strata:

- no verified nuisance versus nuisance present;
- fully observable versus compromised/unobservable primary stream;
- rare-target versus common-target units, if enough independent units exist.

This section is a condition map, not a search for the most favourable subgroup. All predeclared strata are reported.

## 11. System-B replication

Preferred candidate: Snapshot Serengeti expert gold standard.

Before using it confirmatorily, freeze:

- focal target or target set;
- observation unit (capture event, not individual image unless justified);
- train/development/test partition at camera/location or another independent grouping level;
- automated/raw evidence adapter used to construct target support;
- any nuisance/observability annotation protocol;
- primary ecological estimand (preferred: camera × temporal-block encounter prevalence);
- exact binary and process-resolved mappings.

The existing expert gold-standard subset is protected truth. If exploratory model or vocabulary development uses any gold-standard event, that event cannot remain in the confirmatory test set.

Replication success is not defined as reproducing the System-A effect size. The key report is the direction and magnitude of binary-versus-process-resolved error under the independently frozen System-B design.

## 12. Null/adverse outcomes that must remain publishable

The following do not trigger redesign of the confirmatory analysis:

- binary performs equivalently to B/T/N/U;
- binary performs better after accounting for finite calibration data;
- the effect exists only under nuisance/observability stress;
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
- discard difficult/reference-unresolved cases without reporting their rate.

## 14. Promotion rule for an above-MEE paper

A stronger-journal submission is justified only if the final evidence includes:

- independent field truth in System A;
- a frozen held-out field comparison;
- a real ecological estimand and one prespecified ecological conclusion test;
- explicit finite-calibration/annotation burden;
- independent System-B replication or an equivalently strong external validation.

Otherwise the field work should be reported as a separate validation study and should not delay the frozen MEE Paper 1.
