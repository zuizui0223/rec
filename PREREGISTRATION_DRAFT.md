# REC Paper 2 preregistration draft — record entry, observation semantics and ecological inference

Status: **design draft; not preregistered; not yet data-frozen**.

This file defines what must be frozen before confirmatory field truth is inspected. Pilot data may inform feasibility, annotation allocation and sample-size rules, but pilot ecological units may not be reused as confirmatory held-out evidence.

## 1. Program question

Paper 2 asks whether information loss at two distinct stages of automated ecological observation changes real downstream ecological inference against independent truth.

### REC / Chapter 2 — before semantic observation states

Does the tested gate/entry system systematically exclude real biological events from the usable record?

### Chapter 1 — after observation states exist

Does later coarsening of `B/T/N/U` to `target/not-target` discard additional information relevant to ecological estimands?

The two stages must be analyzed separately before any combined interpretation.

## 2. Master exposure universe

Before confirmatory scoring, freeze a master exposure universe

`Ω = {i = 1, ..., N}`

that is defined independently of the tested registered-deviation gate and event-log entry policy.

Freeze:

- exposure source;
- exposure-source version;
- window start/end rule;
- exposure duration rule;
- time-zone/clock synchronization rule;
- missing-reference/exposure failure policy.

An event-triggered event log cannot define `Ω` because non-entered exposures are exactly the population REC studies.

If a defensible exposure universe cannot be reconstructed, the system cannot support confirmatory `q_shadow` or event-nonentry claims.

## 3. Shared primary ecological estimand

For ecological unit `g` containing frozen exposure windows, define reference-truth target-event prevalence

`theta_g = (# reference-truth target-positive windows) / (# reference-truth resolved windows)`.

Reference-unresolved windows are excluded from numerator and denominator and their fraction is reported.

The ecological unit must be frozen before confirmatory scoring. Preferred System-A units are `site × day` or `focal scene × recording day`; frame-level units are forbidden.

## 4. Independent truth protocol

The tested observer cannot access the reference channel.

For every truth-sampled exposure, record separately:

- `target_truth`: positive / negative / unresolved;
- `nuisance_truth`: zero or more predeclared nuisance families / unresolved;
- `observability_truth`: observable / compromised / unobservable / unresolved;
- `coupled_response_truth`: positive / negative / unresolved, if applicable;
- `attribution_truth`: supported / unsupported / unresolved, if applicable.

Reference annotators should be blind to:

- tested pre-gate scores;
- gate result;
- event-log entry state;
- TNOA decision;
- binary comparator output.

At least one protected subset is independently double-annotated and adjudicated. Disagreement is reported and must not be silently converted into negative truth.

## 5. Development / pilot / held-out separation

Split at an independent grouping level before calibration, preferably:

1. recording day;
2. focal scene / camera placement;
3. continuous recording block.

No group may contribute to both development and held-out sets.

Pilot units are excluded from confirmatory held-out inference.

Development/pilot data may define:

- gate parameters and calibration criteria;
- nuisance families;
- observability criteria;
- entry-policy configuration under study;
- truth-sampling design;
- sample-size/precision rule;
- Chapter-2 condition strata;
- one ecological contrast.

Nothing above may be reselected after confirmatory truth is opened.

---

# Part A — REC / Chapter 2: record-entry censoring

## 6. Chapter-2 variables

For each held-out exposure `i ∈ Ω`, define:

- `E_i`: independent event truth;
- `S_i`: retained pre-gate primary evidence;
- `R_i`: frozen registered-deviation gate result (`1` deviation, `0` logical B);
- `K_i`: frozen archive/record-entry status (`1` entry present, `0` non-entered shadow exposure);
- `G`: frozen gate version/configuration;
- `P_K`: frozen entry-policy version/configuration;
- `X_i`: frozen ecological/measurement covariates.

Freeze the semantic statements:

`R=0` = **no registered deviation under the frozen gate**, not biological absence.

`K=0` = **no operational record entry for an exposure window**, not biological absence.

## 7. Primary REC estimands

### 7.1 Logical baseline contamination

`q_B = P(E=1 | R=0, reference truth resolved)`.

### 7.2 Event absorption

`a = P(R=0 | E=1, reference truth resolved)`.

### 7.3 Record-entry shadow contamination

Where `K=0` exposures are identifiable from `Ω`:

`q_shadow = P(E=1 | K=0, reference truth resolved)`.

### 7.4 Event non-entry

`a_K = P(K=0 | E=1, reference truth resolved)`.

### 7.5 Ecological-unit burden

For ecological unit `g`:

`A_g = P(R=0 | E=1, g)`

and, where identifiable,

`A^K_g = P(K=0 | E=1, g)`.

All uncertainty must respect the frozen truth-sampling design and independent ecological-unit structure.

## 8. REC hypotheses

### REC-H1 — the shadow side contains real events

Estimate `q_B` and, where identifiable, `q_shadow` on held-out data.

No requirement exists to reject exact zero. A near-zero estimate with informative uncertainty is a valid null result.

### REC-H2 — entry loss is condition dependent

Estimate

`a(x) = P(R=0 | E=1, X=x)`

and/or

`a_K(x) = P(K=0 | E=1, X=x)`

for a small frozen set of independently measurable strata.

**Falsifier:** loss is effectively constant or too small to matter at the ecological-unit level.

### REC-H3 — differential entry changes ecological inference

For one prespecified ecological contrast, compare the reference-truth effect with effects inferred from:

1. gate-thresholded record;
2. event-log-only record where `K` removes exposures;
3. any correction/uncertainty-aware record only if frozen before held-out truth.

Success does not require a sign reversal. The primary quantity is distance to the reference-truth effect.

### REC-H4 — gate/entry-policy semantics are configuration dependent

If multiple configurations are tested, apply all frozen configurations to the same held-out exposure/evidence stream.

Report their effects on:

- `q_B`;
- `q_shadow`;
- `a` and `a_K`;
- review/capture burden;
- downstream ecological error.

Do not select a “best” configuration on held-out truth and describe it as predeclared.

## 9. REC truth-sampling design

A confirmatory REC design must deliberately truth-sample non-positive parts of the pipeline.

The frozen design must include:

- registered deviations (`R=1`);
- logical B (`R=0`);
- non-entered shadow exposures (`K=0`) where they exist.

If exhaustive annotation is infeasible, freeze stratified inclusion probabilities and preserve inverse-probability weights.

At minimum stratify/reconstruct by:

- gate state `R`;
- record-entry state `K`;
- ecological unit;
- frozen REC condition strata.

Suspicious-looking B/shadow windows cannot be added preferentially without design weights or explicit exploratory status.

## 10. REC condition map

After pilot feasibility and before confirmatory truth, freeze a small condition set selected for measurability and scientific relevance, not effect size.

Preferred measurement-side candidates:

1. reference-rated observability;
2. occlusion;
3. target scale/distance proxy;
4. illumination/exposure;
5. masking/background motion;
6. temporal support/gap;
7. hardware or storage-policy state where relevant.

At most one or a small number of ecological variables should be tied to the prespecified ecological contrast.

All frozen strata are reported, including null/adverse strata.

## 11. REC ecological-consequence identity

For ecological condition `X=x`, define:

- `π(x)=P(E=1|X=x)`;
- `s(x)=P(R=1|E=1,X=x)`;
- `f(x)=P(R=1|E=0,X=x)`.

Then

`P(R=1|X=x) = s(x)π(x) + f(x)[1-π(x)]`.

This identity is used only to frame the measurement problem; it is not claimed as a novel theorem.

The confirmatory ecological question is whether variation in `s(x)`/entry selection materially changes the prespecified effect relative to reference truth.

## 12. REC pilot and sample-size freeze

Pilot-only quantities include:

- completeness of the exposure universe;
- event rate;
- logical-B frequency;
- non-entry frequency;
- reference-positive B/shadow frequency;
- unresolved-truth rate;
- candidate stratum prevalence;
- annotation seconds by gate/entry state;
- independent-unit variance of `q_B`, `q_shadow`, `a`, `a_K` and prevalence error.

After pilot, freeze separate rules for:

1. precision/sample size of REC contamination/non-entry estimates;
2. independent-unit sample size for ecological-consequence contrasts.

Do not choose confirmatory sample size based on observed confirmatory effect direction.

---

# Part B — Chapter 1: decision coarsening after entry

## 13. Observation records under comparison

Both records use the same frozen primary sensor evidence adapters and exposure set.

### Comparator A — binary

`TARGET / not-TARGET`.

### Comparator B — process resolved

`B / T / N / U`.

The binary record is a frozen deterministic coarsening of the process-resolved record.

Finer U reasons may remain metadata but are not a primary comparator because Paper-1 D5 did not establish a semantic-specific information premium.

## 14. Chapter-1 primary endpoint

For each held-out ecological unit `g`, derive `theta_hat_g` under both observation records using the same prespecified downstream analysis class.

Primary loss:

`L_g = |theta_hat_g - theta_g|`.

Primary contrast:

`Delta_g = L_binary,g - L_process,g`.

Positive `Delta` favours preserving B/T/N/U.

The inferential unit is the independent ecological unit, not frames/windows. Report effect estimate and interval, not only a p-value.

## 15. Chapter-1 condition map

Prespecified secondary strata:

- verified nuisance absent/present;
- fully observable versus compromised/unobservable primary stream;
- rare-target versus common-target units if adequately populated.

All predeclared strata are reported.

---

# Part C — shared ecological conclusion and replication

## 16. One ecological conclusion test

Before confirmatory labels are opened, freeze exactly one scientifically meaningful System-A contrast, for example:

- habitat A versus habitat B;
- morning versus afternoon;
- treatment versus control;
- another biologically justified environmental contrast.

Fit the same downstream model form to:

1. reference truth over the master exposure universe;
2. gate-thresholded record;
3. event-log-only record where relevant;
4. process-resolved B/T/N/U record;
5. binary record;
6. one correction/uncertainty-aware REC record only if frozen before held-out truth.

Primary interpretation is distance from each observation-derived effect to the reference-truth effect.

Do not select a different contrast because it produces a larger reversal.

## 17. Error-stage interpretation

Where the design permits, describe total observation distortion as arising from distinct stages:

1. gate censoring (`R`);
2. archive/entry censoring (`K`);
3. post-entry semantic coarsening.

Do **not** claim exact additive decomposition unless the frozen statistical analysis identifies it.

## 18. System-B replication

A System-B dataset is eligible for REC replication only if it has or permits reconstruction of:

- a defensible exposure denominator independent of the tested gate;
- protected independent truth for sampled exposure windows;
- frozen gate/entry semantics;
- independent grouping for development/held-out analysis.

Snapshot Serengeti remains a candidate for Chapter 1 and possibly parts of REC, but an event-only gold-standard subset does not by itself identify non-entered exposure windows. Do not force REC onto a dataset without the required denominator.

Before System-B confirmatory use, freeze:

- focal target/target set;
- exposure unit;
- ecological grouping unit;
- development/test partition;
- evidence adapter;
- gate/entry definition if REC is tested;
- nuisance/observability protocol;
- ecological estimand;
- binary/process-resolved mappings.

Replication success is not defined as reproducing System-A effect size. A failed replication constrains generality.

## 19. Null/adverse outcomes that remain publishable

Do not redesign confirmatory analysis if:

- `q_B`/`q_shadow` are near zero;
- gate/entry loss exists but is not condition dependent;
- condition dependence exists but ecological consequence is negligible;
- event-log non-entry adds little beyond gate censoring;
- binary performs equivalently to or better than B/T/N/U under finite calibration;
- the ecological conclusion does not change;
- annotation cost offsets information benefit;
- System B lacks an eligible exposure denominator;
- System B fails to replicate System A.

## 20. Prohibited post-hoc rescue

After held-out truth is opened, do not:

- redefine the master exposure grid;
- redefine the biological event;
- move groups between development and held-out sets;
- change the primary gate/entry policy under evaluation;
- retune thresholds on held-out truth;
- change truth-sampling strata or weights post hoc;
- redefine nuisance families to improve a result;
- change B/T/N/U or binary mapping;
- merge/split U reasons to improve the primary result;
- replace the ecological unit or primary estimand;
- choose a new condition stratum because it maximizes loss;
- choose a new ecological contrast because it changes sign;
- tune a correction model on held-out truth and call it confirmatory;
- silently drop reference-unresolved or hard shadow windows.

## 21. Promotion ladder

Report the highest REC layer supported:

- **Layer 0:** no material record-entry loss detected;
- **Layer 1:** independently verified events exist in logical B / non-entered shadow windows;
- **Layer 2:** record-entry loss is condition dependent;
- **Layer 3:** differential entry alters a frozen ecological estimand/contrast or unit ranking;
- **Layer 4:** a prespecified correction/redesign reduces that distortion on held-out data;
- **Layer 5:** an independent system supports a compatible direction/condition map.

Do not promote beyond the data.

## 22. Above-MEE promotion rule

A stronger-journal submission is justified only if the final evidence includes, at minimum:

- independent System-A field truth;
- independently defined exposure universe;
- frozen held-out REC comparison;
- frozen held-out Chapter-1 comparison;
- one real ecological estimand and prespecified ecological conclusion test;
- explicit finite calibration/annotation burden;
- condition map showing where information loss does and does not matter;
- independent System-B replication or an equivalently strong external validation.

Otherwise Paper 1 should remain the MEE submission and Paper 2 should be reported at the evidential tier actually achieved.
