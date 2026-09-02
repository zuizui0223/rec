# Chapter 2 — threshold censoring before B/T/N/U

Status: **design program; not preregistered; freeze before confirmatory field analysis**.

## 1. Core problem

The observation pipeline contains an information-loss step upstream of B/T/N/U:

```text
latent event
   |
   v
primary-stream evidence S
   |
   +-- S passes registered-deviation gate --> registered deviation --> T / N / U
   |
   +-- S does not pass gate -------------> registered baseline B
                                               |
                                               +-- true no-event
                                               +-- subthreshold event
```

The observed baseline state is therefore not biological absence:

`B_obs = true no-event + event absorbed below the registered-deviation gate`.

Equivalently,

> **B means no registered deviation under the current measurement rule, not independently certified biological inactivity.**

This distinction is upstream of the Chapter-1 comparison between process-resolved B/T/N/U and target/not-target coarsening.

## 2. Chapter relationship

### Chapter 1 — decision coarsening

Question: what is lost when an already registered process-resolved record

`B / T / N / U`

is coarsened to

`TARGET / not-TARGET`?

### Chapter 2 — threshold censoring

Question: what is lost before that record exists, when the registered-deviation gate maps both true no-event windows and subthreshold biological events into `B`?

The two chapters therefore analyze two distinct garbling steps:

`latent event -> threshold/gate -> B versus registered deviation -> B/T/N/U -> target/not-target`.

Do not use Chapter 1 to claim that Chapter-2 censoring has been measured. Chapter 2 requires independent reference truth upstream of the primary-stream gate.

## 3. Main scientific question

> How often does a registered baseline contain a real biological event that failed the primary-stream deviation gate, and does this threshold absorption vary systematically across ecological or measurement conditions strongly enough to bias downstream ecological conclusions?

## 4. Definitions

For held-out window `i`, define:

- `E_i = 1`: independent reference truth confirms the focal biological event;
- `E_i = 0`: independent reference truth confirms no focal event;
- `R_i = 1`: the primary-stream rule registers a deviation requiring T/N/U adjudication;
- `R_i = 0`: the primary-stream rule assigns registered baseline `B`;
- `S_i`: pre-gate primary-stream evidence retained before thresholding;
- `tau`: frozen registered-deviation threshold or gate rule.

A **threshold-absorbed event** is

`E_i = 1 and R_i = 0`.

A **true registered baseline** is

`E_i = 0 and R_i = 0`.

The central contamination quantity is

`q_B = P(E=1 | R=0, reference truth resolved)`.

This is the proportion of registered-baseline windows that contain independently verified events.

`q_B` is not classifier false-negative rate unless the exact event definition, exposure window and gate semantics make those quantities identical. Report it under the Chapter-2 name rather than silently translating it into a generic accuracy metric.

## 5. Primary hypotheses

### C2-H1 — registered baseline is not pure no-event

Among held-out windows with resolved independent reference truth, `q_B` is greater than zero and estimated with uncertainty.

This is primarily an estimation target, not a test that must reject exactly zero. If no threshold-absorbed events occur in a sufficiently informative held-out sample, that is a valid null result.

### C2-H2 — threshold absorption is condition dependent

The probability of threshold absorption among true events,

`a(x) = P(R=0 | E=1, X=x)`,

will vary across one or more **predeclared independent measurement/ecological strata** such as observability, target distance/scale, illumination, occlusion, masking, or other field-valid covariates.

The first confirmatory condition set must be frozen after pilot feasibility work and before confirmatory labels are opened.

**Falsifier:** absorption probability is approximately constant across the frozen strata or estimated differences are too small to matter at the ecological-unit level.

### C2-H3 — condition-dependent absorption can distort ecological contrasts

For one prespecified ecological contrast `X`, compare the reference-truth event effect with the effect inferred from the registered primary-stream record.

Chapter-2 success does **not** require a dramatic sign reversal. The confirmatory target is whether the thresholded record is farther from the reference-truth contrast than an analysis that explicitly models/retains gate uncertainty or pre-gate evidence according to a frozen method.

**Falsifier:** the registered-baseline contamination has negligible effect on the prespecified ecological contrast.

### C2-H4 — changing the gate changes observation semantics

If two frozen gate rules are compared on the same held-out evidence stream, changing the gate may change `q_B`, event absorption, registered-deviation burden and downstream error even when the ordering of `S` is unchanged.

This is the field analogue of the Paper-1 lesson that raw threshold values are not invariant semantics. Chapter 2 must not claim universal transfer of any numeric threshold.

## 6. Primary Chapter-2 estimands

### 6.1 Baseline contamination

`q_B = (# reference-positive windows assigned B) / (# reference-resolved windows assigned B)`.

Report overall and by frozen strata.

### 6.2 Event absorption rate

`a = (# reference-positive windows assigned B) / (# reference-positive resolved windows)`.

This differs from `q_B`: one conditions on observed B, the other on true events. Report both.

### 6.3 Ecological-unit absorption burden

For independent ecological unit `g`:

`A_g = (# reference-positive windows assigned B in g) / (# reference-positive resolved windows in g)`.

Use independent units such as site × day or focal-scene × day; never treat frames as independent replicates.

### 6.4 Contrast distortion

For one frozen ecological contrast, fit the same model form to:

1. reference-truth event record;
2. registered thresholded record;
3. a prespecified Chapter-2 correction/uncertainty-aware record, only if that method is frozen before held-out truth is opened.

Primary quantity is distance from each observation-derived effect to the reference-truth effect.

## 7. Required measurement architecture

Chapter 2 cannot be established from the thresholded primary stream alone.

System A requires:

1. a **primary stream** from which `S`, gate status and B/deviation are computed;
2. an **independent reference channel** capable of establishing event truth even when the primary stream assigns B;
3. synchronized window identifiers so B windows can be checked against reference truth;
4. retained pre-gate evidence `S` for all windows, including B;
5. frozen gate-rule versioning.

The reference channel must not be supplied to the tested gate/observer.

## 8. Critical anti-circularity rule

Do not define the biological event using the same score or threshold whose censoring is being tested.

Forbidden examples:

- `E=1` because `S > tau`;
- defining reference presence from the primary classifier output;
- annotators seeing the tested score and using it to decide whether a weak event occurred;
- discarding B windows from truth annotation because they appear uninteresting.

Reference annotators must be blind to `S`, `tau`, registered B/deviation state and TNOA decision during primary truth annotation whenever practical.

## 9. Gate representation

A gate may be scalar or composite. Record it explicitly rather than forcing every system into one scalar threshold.

### Scalar gate

`R = 1[S > tau]`.

### Composite gate

`R = G(S_1, ..., S_k; phi)`

where `phi` is a frozen rule/configuration version.

For a composite gate, Chapter 2 still defines a threshold-absorbed event as `E=1, R=0`; do not invent a pseudo-scalar `tau` unless the rule actually has one.

## 10. Pilot design

The pilot estimates feasibility only:

- frequency of reference-positive B windows;
- event rate;
- distribution of pre-gate evidence among reference-positive and reference-negative windows;
- candidate condition strata and whether they can be independently measured;
- annotation burden specifically for B windows;
- synchronization/reference failure rate;
- independent-unit variance of `q_B`, `a`, and ecological-unit prevalence error.

Pilot data may be used to choose operational stratum definitions and sample size, but pilot units are excluded from confirmatory held-out inference.

## 11. Sampling requirement: annotate B deliberately

A naive review process that annotates only registered deviations cannot answer Chapter 2.

The truth sample must include a prespecified sample of registered-B windows. If B is very common, use stratified sampling and retain inclusion probabilities/weights so contamination estimates can be reconstructed for the target population.

At minimum preserve strata by:

- registered state: B versus registered deviation;
- independent ecological unit;
- frozen measurement condition(s) relevant to C2-H2.

Never oversample suspicious B windows without retaining the sampling design.

## 12. Chapter-2 condition map

The final condition map must distinguish ecological covariates from measurement covariates.

### Measurement-side candidates

- reference-rated observability;
- occlusion;
- target image scale/distance proxy;
- illumination/exposure;
- masking/background motion;
- temporal support/gap;
- hardware state.

### Ecological-side candidates

Only include variables with a defensible biological interpretation and a frozen reason for inclusion, for example habitat, time of day, flower/plant state, treatment, or season.

A key risk is differential measurement: if an ecological covariate also changes observability, apparent ecological effects may partly reflect gate absorption. Chapter 2 should explicitly decompose or condition on that path when possible.

## 13. Causal/measurement diagram

The minimal conceptual structure is:

```text
Ecological condition X --------> latent event E --------> reference truth
          |                           |
          |                           v
          +------> observability O -> primary evidence S -> gate R -> B/deviation
```

This diagram permits two distinct paths from `X` to the recorded event process:

1. a biological path `X -> E`;
2. a measurement path `X -> O/S/R`.

If the measurement path is ignored, threshold censoring can be mistaken for ecology.

Chapter 2 therefore asks not merely whether the gate misses events, but whether **differential gate absorption changes ecological inference**.

## 14. Relationship to absence

Neither registered baseline nor subthreshold evidence certifies biological absence.

- `B`: no registered deviation under the frozen primary-stream rule;
- `E=0`: independently supported no-event for the defined reference window;
- `A-`: if ever used, a separately justified independent absence-evidence concept.

Do not collapse these into one label.

## 15. Null/adverse outcomes that remain publishable

Retain all of the following without redesign:

- `q_B` is essentially zero;
- absorption occurs but is not condition dependent;
- absorption is condition dependent but does not affect the prespecified ecological contrast;
- a simpler thresholded analysis matches reference truth as well as the uncertainty-aware alternative;
- finite annotation/calibration burden outweighs practical benefit;
- System B does not support an equivalent Chapter-2 gate analysis.

## 16. Prohibited post-hoc rescue

After confirmatory reference truth is opened, do not:

- change the event definition;
- change the primary gate or gate version;
- redefine B;
- choose condition strata because they maximize absorption differences;
- discard low-quality B windows without reporting them as unresolved reference truth;
- choose a new ecological contrast because the original one shows no distortion;
- tune a correction method on held-out truth and then call it confirmatory.

## 17. Chapter-2 promotion criterion

Chapter 2 materially strengthens the above-MEE program if it establishes all three layers:

1. **existence:** independently verified events occur inside registered B;
2. **structure:** absorption varies predictably with independently measured conditions;
3. **consequence:** that differential absorption measurably distorts at least one frozen ecological estimand/contrast or site ranking relative to reference truth.

If only layer 1 is established, Chapter 2 is mainly a measurement validation result. If layers 1–2 are established but 3 is null, report the condition map and constrain the ecological-consequence claim.
