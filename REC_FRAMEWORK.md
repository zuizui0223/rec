# REC framework — the record-entry shadow side of TNOA

Status: **working conceptual framework; not a novelty claim; empirical validation belongs to Paper 2**.

## 1. Working name

**REC = Record-Entry Censoring.**

REC studies how ecological exposure opportunities and events are selected into the scientific record **before** TNOA-style semantic adjudication begins.

- **TNOA asks:** once an observation has entered the record, which process distinctions should survive downstream representation?
- **REC asks:** which exposure opportunities/events did not enter that record, through which gate/entry mechanism, and does that selection alter ecological inference?

REC does not claim priority for imperfect detection, false negatives, camera trigger failure or missing-data theory.

## 2. What “shadow world” means

The shadow world is not a mystical or fundamentally unobservable state space.

REC distinguishes:

1. **latent biological world** — never exhaustively observable;
2. **master exposure universe `Omega`** — observation opportunities defined independently of the tested gate;
3. **reference-observable shadow world** — sampled exposures where independent reference truth can resolve events even when the tested system did not enter a record;
4. **primary recorded world** — exposures selected into the tested record;
5. **semantic world** — entered observations represented as B/T/N/U and later coarsened outputs.

Formal empirical target:

> **unseen by the tested record-entry system, but recoverable under an independent exposure/reference design.**

## 3. No record is not yet a state

A missing event-log row does not itself mean biological baseline.

To interpret “nothing was recorded,” REC first requires an exposure denominator:

`Omega = {i = 1, ..., N}`.

`Omega` must be generated independently of the tested event-entry gate, for example by:

- a fixed temporal clock;
- continuous reference audio/video partitioned into frozen windows;
- continuous primary acquisition with later event logging;
- another externally justified schedule.

Without `Omega`, the non-entered set is not empirically enumerable and event-log-only data cannot identify `P(event | no record)` without additional assumptions.

Foundational rule:

> **Define exposure before defining non-detection.**

## 4. Core variables

For `i in Omega`:

- `E_i`: independent event truth (`1`, `0`, unresolved);
- `S_i`: retained pre-gate evidence;
- `R_i`: registered-deviation indicator from frozen gate `G`;
- `K_i`: operational record-entry/archive indicator;
- `D_i`: process-resolved decision if represented (`B/T/N/U`);
- `Y_i`: later coarsened output such as target/not-target;
- `X_i`: ecological and measurement covariates defined independently of the tested gate where possible.

## 5. Separate gate censoring R from record-entry censoring K

### Gate censoring

`R_i=0` means the frozen gate did not register a deviation.

A **threshold-absorbed event** is:

`E_i=1, R_i=0`.

Logical registered-baseline contamination:

`q_B = P(E=1 | R=0, truth resolved)`.

Event absorption:

`a_R = P(R=0 | E=1, truth resolved)`.

### Record-entry censoring

`K_i=0` means the operational event/archive record contains no entry for exposure `i`.

Define:

`Omega_shadow = {i in Omega : K_i=0}`.

Shadow contamination:

`q_shadow = P(E=1 | K=0, truth resolved)`.

Event non-entry:

`a_K = P(K=0 | E=1, truth resolved)`.

`R` and `K` may differ. A fixed-schedule system can store `R=0` baseline windows (`K=1`), while an event-triggered system may produce `R=0, K=0`. An `R=1, K=0` row signals an archive/storage-stage loss rather than gate failure.

## 6. Full information-loss chain

```text
latent biological process
        |
        v
master exposure universe Omega
        |
        v
pre-gate evidence S
        |
        v
registration gate R                <- REC gate layer
        |
        v
archive / event-log entry K        <- REC entry layer
        |
        v
B / T / N / U                      <- TNOA semantic layer
        |
        v
target / not-target                <- later coarsening
        |
        v
downstream ecological inference
```

Each stage can remove information for a different reason. Later modeling cannot recover a distinction that never entered the record unless independent measurements or explicit assumptions supply it.

## 7. Why apparent ecology can be manufactured

Let

- `pi(x)=P(E=1 | X=x)` be biological event probability;
- `s(x)=P(R=1 | E=1, X=x)` be sensitivity to true events;
- `f(x)=P(R=1 | E=0, X=x)` be false registration probability.

Then

`P(R=1 | X=x) = s(x) pi(x) + f(x) [1-pi(x)]`.

A gradient in recorded events can therefore come from ecology `pi(x)`, measurement `s(x)`, false registration `f(x)`, or combinations.

Minimal causal picture:

```text
Ecological condition X ------> latent event E ------> reference truth
        |                           |
        +--> observability O ------+--> evidence S --> R --> K --> record
```

The core REC consequence hypothesis is not merely “events are missed,” but:

> **condition-dependent entry selection can be mistaken for ecology if the measurement path is not represented.**

This general possibility is established in imperfect-detection/observation-process literature; REC must measure it in its own frozen record-entry chain.

## 8. Empirical claim ladder

REC earns claims in order:

1. **denominator** — `Omega` exists independently of the tested entry rule;
2. **shadow existence** — reference-positive events are measured in `R=0`/`K=0` exposures;
3. **shadow structure** — event absorption/non-entry varies across predeclared conditions;
4. **ecological consequence** — the selection changes a frozen ecological estimand/ranking/contrast relative to reference truth;
5. **recoverability/redesign** — a frozen exposure-aware correction or acquisition design reduces that discrepancy;
6. **two-stage decomposition** — where identifiable, separate upstream REC loss from downstream TNOA coarsening;
7. **cross-system generality** — replicate a constrained version in another sensor/system.

Failure at one level constrains the next claim rather than licensing redesign on held-out truth.

## 9. REC versus TNOA

| Question | REC | TNOA |
| --- | --- | --- |
| Information-loss location | before/at record entry | after record representation |
| Missing object | exposure/event absent from record set | process distinction inside entered record |
| Core variables | `Omega`, `R`, `K`, entry provenance | evidence semantics, B/T/N/U |
| Anti-error rule | no record != no event | low T / not-T != biological absence |
| External requirement | gate-independent denominator + reference truth | calibrated evidence semantics; independent A- if absence claimed |
| Typical failure | selection/detection gradient masquerades as ecology | B/N/U collapsed into binary negative |

Together:

`world -> exposure Omega -> REC selection -> TNOA semantics -> downstream ecology`.

## 10. Prior-art boundary

REC explicitly surrenders priority for:

- nondetection != absence;
- occupancy/capture-recapture imperfect detection;
- condition-dependent detection;
- camera-trap pass/trigger/registration/quality decomposition;
- independent CCTV/double-observer missed-detection studies;
- automated acoustic FP/FN ecological inference;
- continuous-score/classification-aware occupancy;
- censoring/truncation/MNAR/preferential-sampling theory.

See `PRIOR_ART_BOUNDARY.md`.

The strongest currently defensible architectural target is:

> **an auditable record-entry contract connecting a gate-independent exposure denominator, retained pre-gate evidence, versioned registration/archive rules, probability-sampled non-entry truth and downstream ecological consequence before later semantic coarsening.**

This is a hypothesis about useful architecture until field evidence supports it.

## 11. External-system logic

Do not force one dataset to validate every layer.

- **Findlay CT-Detection:** closest public physical trigger/registration neighbour; supports event-conditioned missed-trigger analyses but not a full temporal `Omega`.
- **BirdVox-full-night:** current leading public algorithmic REC candidate because continuous audio defines an enumerable time denominator and expert event annotations exist.
- **WABAD:** later broad acoustic generalization candidate after sampling provenance review.
- **Snapshot Serengeti:** useful primarily for post-entry semantic/TNOA work; event-triggered imagery alone cannot enumerate animals that never triggered the camera.

See `SYSTEM_B_CANDIDATES.md`.

## 12. Executable implementation

REC now has two linked fail-closed contracts.

### Master exposure / entry ledger

- `EXPOSURE_LEDGER_SCHEMA.md`
- `scripts/validate_exposure_ledger.py`
- `examples/exposure_ledger.csv`
- `tests/test_exposure_ledger.py`

This validates the denominator `Omega` and operational entry indicator `K`.

### Chapter-2 gate / truth audit

- `CHAPTER2_THRESHOLD_CENSORING.md`
- `TRUTH_AND_WINDOW_SCHEMA.md`
- `scripts/validate_chapter2_windows.py`
- `examples/chapter2_windows.csv`
- `tests/test_chapter2_schema.py`

This validates gate `R`, truth sampling and absorbed/shadow-event derivations.

CI validates both contracts on each PR.

## 13. Hypothesis traceability

`HYPOTHESIS_RECOVERY.md` records how REC hypotheses descend from TNOA principles, which parts are already known from prior literature, falsifiers, and which empirical combinations remain credible novelty candidates.

## 14. Hard guardrails

REC must not:

- infer `E=0` because `R=0` or `K=0`;
- treat an event log as the exposure universe;
- estimate `q_shadow` without recoverable denominator/sampling design;
- define truth with the same gate being audited;
- preferentially inspect suspicious non-entry windows without accounting for inclusion probabilities;
- retune the gate on held-out truth and call the result confirmatory;
- call standard imperfect-detection findings novel;
- claim a universal optimal gate;
- claim ecological distortion without comparison to an independently supported ecological estimand;
- imply that a reference annotation on the same sensor stream establishes events the physical sensor never captured.
