# Chapter 2 — threshold and record-entry censoring before B/T/N/U

Status: **design program; not preregistered; freeze before confirmatory field analysis**.

## 1. Core problem

The observation pipeline contains an information-loss step upstream of B/T/N/U:

```text
latent biological process
   |
   v
master exposure universe Ω
   |
   v
primary-stream evidence S
   |
   +-- gate registers deviation (R=1) --> registered deviation --> T / N / U
   |
   +-- gate registers no deviation (R=0) --> logical registered baseline B_reg
                                                |
                                                +-- true no-event
                                                +-- threshold-absorbed event
                                                |
                                                +-- may not be archived at all (K=0)
```

The logical baseline state is therefore not biological absence:

`B_reg = true no-event + event absorbed below the registered-deviation gate`.

Equivalently,

> **B means no registered deviation under the current measurement rule, not independently certified biological inactivity.**

A second distinction is even more upstream:

> **A missing event-log entry is not automatically a B observation. It becomes scientifically interpretable only relative to an independently defined exposure universe.**

This chapter is the first empirical REC chapter: the shadow-side companion to TNOA.

## 2. REC / TNOA relationship

### REC — pre-entry shadow side

REC asks which exposure windows/events fail to enter the usable scientific record, why, and whether that selection changes ecological inference.

### TNOA — post-entry semantic side

TNOA asks how to preserve target, nuisance, observability and attribution distinctions once an observation record exists.

### Chapter 1 — decision coarsening

Question: what is lost when an already represented process-resolved record

`B / T / N / U`

is coarsened to

`TARGET / not-TARGET`?

### Chapter 2 — threshold / record-entry censoring

Question: what is lost before that record exists, when a gate maps both true no-event windows and real events into `R=0`, and when an operational archive policy may omit those windows from the event log?

The stages are distinct:

`latent process -> exposure Ω -> evidence S -> gate R -> entry K -> B/T/N/U -> target/not-target`.

Do not use Chapter 1 to claim that Chapter-2 censoring has been measured. Chapter 2 requires an exposure denominator and independent reference truth upstream of the tested gate.

## 3. Foundational denominator: the master exposure universe

Define

`Ω = {i = 1, ..., N}`

as the set of exposure windows over which a record could have been created.

`Ω` must be defined independently of the tested registered-deviation gate. Acceptable examples include:

- fixed temporal windows from a continuous independent reference stream;
- a frozen periodic acquisition schedule;
- another externally justified exposure schedule that exists whether or not the event gate fires.

The event log itself cannot define `Ω` in an event-triggered system because the non-entered windows are exactly the population under study.

REC therefore adopts:

> **Define exposure before defining non-detection.**

Without `Ω`, quantities conditioned on “no record” are not identifiable from the event log alone.

## 4. Main scientific question

> How often do logical baseline or physically non-entered exposure windows contain real biological events, does that loss vary systematically across ecological or measurement conditions, and is the resulting record-entry selection strong enough to alter downstream ecological conclusions?

## 5. Definitions

For held-out exposure window `i ∈ Ω`, define:

- `E_i = 1`: independent reference truth confirms the focal biological event;
- `E_i = 0`: independent reference truth confirms no focal event;
- `E_i = unresolved`: independent truth cannot resolve the event;
- `S_i`: pre-gate primary-stream evidence retained before registration;
- `R_i = 1`: the primary-stream rule registers a deviation requiring T/N/U adjudication;
- `R_i = 0`: the primary-stream rule assigns logical registered baseline `B_reg`;
- `K_i = 1`: the operational event/archive record contains an entry for exposure `i`;
- `K_i = 0`: the exposure lies in the record-entry shadow set;
- `G`: frozen registered-deviation gate;
- `P_K`: frozen record-entry/archive policy.

A **threshold-absorbed event** is

`E_i = 1 and R_i = 0`.

A **true logical baseline** is

`E_i = 0 and R_i = 0`.

A **shadow event** is

`E_i = 1 and K_i = 0`.

The record-entry shadow set is

`Ω_shadow = {i ∈ Ω : K_i = 0}`.

Do not assume `K=R`. In a purely triggered event logger they may be tightly coupled; in a fixed-schedule recorder every exposure may be archived even when `R=0`.

## 6. Primary Chapter-2 estimands

### 6.1 Logical baseline contamination

`q_B = P(E=1 | R=0, reference truth resolved)`.

Empirical form:

`q_B = (# reference-positive windows with R=0) / (# reference-resolved windows with R=0)`.

This is the proportion of logical registered-baseline windows that contain independently verified events.

`q_B` is not automatically identical to a generic classifier false-negative rate. Report it under the Chapter-2 definition.

### 6.2 Event absorption rate

`a = P(R=0 | E=1, reference truth resolved)`.

Empirical form:

`a = (# reference-positive windows with R=0) / (# reference-positive resolved windows)`.

Keep `a` distinct from `q_B`; their denominators differ.

### 6.3 Record-entry shadow contamination

When `K=0` exposures are identifiable from the master exposure grid,

`q_shadow = P(E=1 | K=0, reference truth resolved)`.

This is the proportion of physically non-entered exposure windows containing real events.

Do not report `q_shadow` when the non-entered exposure population cannot be reconstructed or sampled with known inclusion probabilities.

### 6.4 Event non-entry rate

`a_K = P(K=0 | E=1, reference truth resolved)`.

This measures the fraction of independently verified events missing from the operational event/archive record.

### 6.5 Ecological-unit absorption burden

For independent ecological unit `g`:

`A_g = P(R=0 | E=1, ecological_unit=g)`.

and, where identifiable,

`A^K_g = P(K=0 | E=1, ecological_unit=g)`.

Use independent units such as site × day or focal-scene × day; never treat frames as independent replicates.

### 6.6 Contrast distortion

For one frozen ecological contrast, fit the same model form to:

1. reference-truth event record over `Ω`;
2. registered thresholded record;
3. event-log-only record if `K` removes windows;
4. a prespecified correction/uncertainty-aware record only if the method is frozen before held-out truth is opened.

Primary quantity is distance from each observation-derived effect to the reference-truth effect.

## 7. Primary hypotheses

### C2-H1 — the shadow side contains real events

Among held-out windows with resolved independent reference truth, estimate `q_B` and, where identifiable, `q_shadow`.

The confirmatory claim is estimation, not a requirement to reject exactly zero. If no absorbed/shadow events occur in a sufficiently informative held-out sample, that is a valid null result.

### C2-H2 — record-entry loss is condition dependent

The probability of gate absorption among true events,

`a(x) = P(R=0 | E=1, X=x)`,

and/or archive non-entry,

`a_K(x) = P(K=0 | E=1, X=x)`,

may vary across one or more **predeclared independent measurement/ecological strata** such as observability, target distance/scale, illumination, occlusion, masking, or another field-valid covariate.

The confirmatory condition set must be frozen after pilot feasibility work and before confirmatory labels are opened.

**Falsifier:** loss probability is approximately constant across the frozen strata or estimated differences are too small to matter at the ecological-unit level.

### C2-H3 — differential record entry can distort ecological contrasts

For one prespecified ecological contrast `X`, compare the reference-truth event effect with effects inferred after gate/entry selection.

Chapter-2 success does **not** require a dramatic sign reversal. The confirmatory target is distance to the reference-truth contrast.

**Falsifier:** baseline/shadow contamination has negligible effect on the prespecified ecological estimand/contrast.

### C2-H4 — changing the gate or entry policy changes observation semantics

If two frozen gate/entry configurations are compared on the same held-out exposure stream, changing `G` or `P_K` may change `q_B`, `q_shadow`, event absorption, review burden and downstream error even when the ordering of pre-gate evidence is unchanged.

This is the field analogue of the Paper-1 lesson that raw threshold values are not invariant semantics. Chapter 2 must not claim universal transfer of any numeric threshold or entry policy.

## 8. Why ecological gradients can be manufactured

Let

- `π(x) = P(E=1 | X=x)` be the true event probability;
- `s(x) = P(R=1 | E=1, X=x)` be gate sensitivity;
- `f(x) = P(R=1 | E=0, X=x)` be false registration probability.

Then

`P(R=1 | X=x) = s(x)π(x) + f(x)[1-π(x)]`.

Therefore a recorded gradient can arise from ecology `π(x)`, measurement `s(x)`, false registration `f(x)`, or all three.

This identity is not claimed as a new statistical theorem. It motivates the REC condition map and the requirement to compare downstream effects with independent truth.

## 9. Required measurement architecture

Chapter 2 cannot be established from the thresholded event log alone.

System A requires:

1. a **master exposure grid** independent of the tested gate;
2. a **primary stream** from which `S`, gate status and logical B/deviation are computed;
3. an **independent reference channel** capable of establishing event truth even when the primary stream assigns `R=0` or the event log has `K=0`;
4. synchronized window identifiers linking exposure, primary evidence, event-log entry and reference truth;
5. retained pre-gate evidence for all exposures or a frozen recoverable sampling design;
6. frozen gate-rule versioning;
7. frozen archive/event-entry policy versioning.

The reference channel must not be supplied to the tested gate/observer.

## 10. Critical anti-circularity rule

Do not define the biological event or exposure denominator using the same gate whose censoring is being tested.

Forbidden examples:

- `E=1` because `S > tau`;
- defining `Ω` as “all event-log rows” in an event-triggered system;
- defining reference presence from the primary classifier output;
- annotators seeing the tested score and using it to decide whether a weak event occurred;
- discarding logical B or non-entered windows from truth annotation because they appear uninteresting.

Reference annotators must be blind to `S`, gate result, record-entry status and TNOA decision during primary truth annotation whenever practical.

## 11. Gate and entry-policy representation

A gate may be scalar or composite. Record it explicitly rather than forcing every system into one scalar threshold.

### Scalar gate

`R = 1[S > tau]`.

### Composite gate

`R = G(S_1, ..., S_k; phi)`

where `phi` is a frozen configuration version.

For a composite gate, do not invent a pseudo-scalar `tau` unless the rule actually has one.

The archive/entry policy is separately represented as

`K = P_K(R, schedule, device state, policy inputs; psi)`

with version `psi`. This permits periodic recording, trigger-only recording, hybrid capture and later retention filters to be distinguished.

## 12. Pilot design

The pilot estimates feasibility only:

- completeness of the master exposure grid;
- frequency of reference-positive logical B windows;
- frequency of reference-positive non-entered windows;
- event rate;
- distribution of pre-gate evidence among reference-positive and reference-negative windows;
- candidate condition strata and whether they can be independently measured;
- annotation burden for B/shadow windows;
- synchronization/reference failure rate;
- independent-unit variance of `q_B`, `q_shadow`, `a`, `a_K`, and ecological-unit prevalence error.

Pilot data may be used to choose operational stratum definitions and sample size, but pilot units are excluded from confirmatory held-out inference.

## 13. Sampling requirement: sample the shadow deliberately

A review process that annotates only event-log entries cannot answer REC.

The truth sample must include a prespecified sample of:

- `R=1` registered deviations;
- `R=0` logical B windows;
- `K=0` non-entered exposure windows when archive non-entry exists.

If B/shadow windows are very common, use stratified sampling and retain inclusion probabilities/weights so population contamination estimates can be reconstructed.

At minimum preserve strata by:

- gate state `R`;
- entry state `K`;
- independent ecological unit;
- frozen measurement condition(s) relevant to C2-H2.

Never oversample suspicious shadow windows without retaining the sampling design.

## 14. Chapter-2 condition map

The final condition map must distinguish ecological covariates from measurement covariates.

### Measurement-side candidates

- reference-rated observability;
- occlusion;
- target image scale/distance proxy;
- illumination/exposure;
- masking/background motion;
- temporal support/gap;
- hardware state;
- archive/storage policy state where variable.

### Ecological-side candidates

Only include variables with a defensible biological interpretation and a frozen reason for inclusion, for example habitat, time of day, flower/plant state, treatment, or season.

A key risk is differential measurement: if an ecological covariate also changes observability or entry probability, apparent ecological effects may partly reflect REC selection. Chapter 2 should explicitly decompose or condition on that path when possible.

## 15. Causal/measurement diagram

The minimal structure is:

```text
Ecological condition X --------> latent event E --------> reference truth
          |                           |
          |                           v
          +------> observability O -> primary evidence S -> gate R -> entry K
```

This permits distinct paths from `X` to the event-log record:

1. biological path `X -> E`;
2. measurement path `X -> O/S/R/K`.

If the measurement path is ignored, record-entry censoring can be mistaken for ecology.

Chapter 2 therefore asks not merely whether the gate misses events, but whether **differential entry changes ecological inference**.

## 16. Relationship to absence

Neither logical baseline nor archive non-entry certifies biological absence.

- `R=0 / B_reg`: no registered deviation under the frozen gate;
- `K=0`: no operational record entry for an exposure window;
- `E=0`: independently supported no-event for the defined reference window;
- `A-`: if ever used, a separately justified independent absence-evidence concept.

Do not collapse these into one label.

## 17. Prior-art boundary

Chapter 2 does **not** claim novelty for imperfect detection, false negatives, camera-trigger failures, double-observer designs or occupancy detection modeling.

Findlay et al. (2020) are a close camera-trap neighbour because they explicitly decomposed pass, trigger, image registration and image-quality failures using CCTV reference data. Standard occupancy work also separates occurrence from detection.

REC’s narrower target is the **record-entry contract**: exposure denominator, pre-gate evidence, gate/entry provenance, deliberate shadow-set sampling, independent truth and downstream ecological consequence in one auditable pipeline.

See `PRIOR_ART_BOUNDARY.md`.

## 18. Null/adverse outcomes that remain publishable

Retain all of the following without redesign:

- `q_B` and `q_shadow` are essentially zero;
- loss occurs but is not condition dependent;
- loss is condition dependent but does not affect the prespecified ecological contrast;
- the event log has negligible additional non-entry beyond logical gate censoring;
- a simpler thresholded analysis matches reference truth as well as the uncertainty-aware alternative;
- finite annotation/calibration burden outweighs practical benefit;
- System B does not have a recoverable exposure denominator and therefore cannot support REC replication;
- System B fails to reproduce the System-A condition map.

## 19. Prohibited post-hoc rescue

After confirmatory reference truth is opened, do not:

- redefine the master exposure grid;
- change the event definition;
- change the primary gate or gate version;
- change the archive/entry policy under evaluation;
- redefine logical B;
- choose condition strata because they maximize loss differences;
- discard low-quality B/shadow windows without reporting them as unresolved reference truth;
- choose a new ecological contrast because the original one shows no distortion;
- tune a correction method on held-out truth and then call it confirmatory.

## 20. Chapter-2 promotion criterion

Chapter 2 materially strengthens the above-MEE program if it establishes all three layers:

1. **existence:** independently verified events occur inside logical B and/or the archive shadow set;
2. **structure:** record-entry loss varies predictably with independently measured conditions;
3. **consequence:** that differential loss measurably distorts at least one frozen ecological estimand/contrast or site ranking relative to reference truth.

If only layer 1 is established, Chapter 2 is mainly a measurement validation result. If layers 1–2 are established but 3 is null, report the condition map and constrain the ecological-consequence claim.
