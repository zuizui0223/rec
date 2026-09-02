# REC framework — the shadow side of TNOA

Status: **working conceptual framework; not a novelty claim; empirical validation belongs to Paper 2**.

## 1. Working name

**REC = Record-Entry Censoring.**

The name is a project-level working label for the process by which ecological events or exposure windows fail to enter the scientific record before downstream semantic adjudication begins.

REC is deliberately paired with TNOA:

- **TNOA asks:** once an observation has entered the record, which process distinctions must be preserved before downstream ecological inference?
- **REC asks:** which ecological exposures or events never entered that record, why did they fail to enter, and what ecological information is therefore absent from the recorded world?

The manuscript-facing novelty must not be phrased as “the first framework for imperfect detection.” Imperfect detection, false negatives, trigger failures and occupancy models are established literatures. REC’s narrower target is an **auditable record-entry contract** linking the exposure universe, pre-gate evidence, entry/retention rules, independent truth and downstream ecological distortion.

## 2. Paired-world view

TNOA and REC examine opposite sides of the same observation interface.

```text
                         ecological world
                               |
                               v
                    master exposure universe Ω
                               |
                               v
                    primary-stream evidence S
                               |
                         registered gate G
                        /                 \
                       /                   \
               R = 0 /                     \ R = 1
                     v                       v
          logical registered baseline      registered deviation
                 B_reg                         |
                   |                           v
                   |                        T / N / U
                   |                           |
                   |                           v
                   |                    target / not-target
                   |
                   +---- REC shadow side

TNOA starts after a usable observation record exists.
REC reconstructs and audits the exposure set that was censored before or at record entry.
```

The key conceptual asymmetry is that the recorded world is directly enumerable, whereas the shadow world often is not.

## 3. Foundational principle: no record is not yet a state

A missing event-log entry is not automatically a biological baseline observation.

To say that “nothing was recorded” scientifically, one first needs a denominator: a set of exposure windows during which an observation could have entered the record.

Define a **master exposure universe**

`Ω = {i = 1, ..., N}`

whose windows are created independently of the tested event-entry gate. Examples include:

- a fixed temporal sampling clock;
- a continuous reference video divided into frozen windows;
- an independent acquisition stream with complete exposure accounting;
- another externally justified schedule that exists whether or not the tested gate fires.

Without `Ω`, the non-entered set is not observable as a population and quantities such as `P(event | no record)` are not identified from the event log alone.

REC therefore adopts the rule:

> **Define exposure before defining non-detection.**

This is the upstream analogue of TNOA’s rule that low target support is not biological absence.

## 4. Core variables

For exposure window `i ∈ Ω`, define:

- `E_i`: independent biological event truth (`1`, `0`, or unresolved);
- `S_i`: retained pre-gate primary-stream evidence;
- `R_i`: registered-deviation indicator produced by frozen gate `G`;
- `K_i`: archive/record-entry indicator — whether the tested operational record actually contains an entry for the window;
- `D_i`: process-resolved decision when the logical observation is represented (`B/T/N/U`, with `B` the no-registered-deviation state);
- `Y_i`: any later coarsened record supplied downstream, such as `target/not-target`;
- `X_i`: ecological and measurement covariates defined independently of the tested gate where possible.

These variables separate two upstream mechanisms that are often conflated.

### 4.1 Gate censoring

`R_i = 0` means the frozen measurement rule did not register a deviation.

A threshold-absorbed event is

`E_i = 1, R_i = 0`.

The logical baseline contamination is

`q_B = P(E=1 | R=0, truth resolved)`.

### 4.2 Archive/entry censoring

`K_i = 0` means the operational event record contains no stored entry for exposure window `i`.

In a purely event-triggered system, `K` may closely follow `R`. In a fixed-schedule system, `K` may equal one for every exposure even when `R=0`. REC keeps these mechanisms separate rather than assuming they are identical.

Define the **record-entry shadow set**

`Ω_shadow = {i ∈ Ω : K_i = 0}`.

Its event contamination is

`q_shadow = P(E=1 | K=0, truth resolved)`.

`q_shadow` is not estimable from the event log alone unless non-entered exposure windows can be reconstructed from an independent exposure universe.

## 5. The complete information-loss chain

REC and TNOA together describe a staged observation pipeline:

```text
latent biological process
        |
        v
exposure universe Ω
        |
        v
pre-gate evidence S
        |
        v
registration gate R              <- REC Chapter 2
        |
        v
archive / event-log entry K      <- REC record-entry layer
        |
        v
process-resolved B/T/N/U         <- TNOA / Paper-2 Chapter 1 interface
        |
        v
binary target/not-target         <- decision coarsening
        |
        v
downstream ecological inference
```

Each arrow can remove information for a different reason. Later modeling cannot reconstruct distinctions that were never entered into the data unless extra measurements or assumptions supply them.

## 6. Why environmental bias can appear

Let

- `π(x) = P(E=1 | X=x)` be the true ecological event probability;
- `s(x) = P(R=1 | E=1, X=x)` be gate sensitivity to true events;
- `f(x) = P(R=1 | E=0, X=x)` be false registration probability.

Then the observed registered-deviation rate satisfies

`P(R=1 | X=x) = s(x) π(x) + f(x) [1 - π(x)]`.

Therefore a gradient in the recorded event rate can arise from:

1. a real ecological gradient `π(x)`;
2. a measurement gradient `s(x)`;
3. a false-registration gradient `f(x)`;
4. combinations of all three.

This identity is not a new statistical discovery. Its role in REC is operational: every proposed ecological contrast should be checked for a plausible path through the record-entry mechanism.

The dangerous case is

`X -> observability/evidence -> R/K`

when the scientific analysis interprets the resulting record as if only

`X -> E`

were operating.

## 7. REC’s main empirical ladder

REC should earn claims in the following order.

### Level 1 — shadow existence

Show that independently verified biological events occur in `R=0` or `K=0` exposure windows.

Key quantities:

- `q_B = P(E=1 | R=0)`;
- event absorption `a = P(R=0 | E=1)`;
- `q_shadow = P(E=1 | K=0)` when archive non-entry exists.

A null result is valid.

### Level 2 — shadow structure

Show whether absorption/non-entry varies across predeclared measurement or ecological conditions.

Examples: observability, target scale/distance, occlusion, illumination, masking, hardware state.

### Level 3 — ecological consequence

Show whether differential record entry changes a prespecified ecological estimand, site ranking or effect estimate relative to independent truth.

### Level 4 — correction or redesign

Only after Levels 1–3 may REC test whether a frozen correction, uncertainty-aware model or acquisition redesign reduces that distortion.

### Level 5 — cross-system generality

Replicate the direction/condition map in an independent sensor or biological system. Failure to replicate constrains the scope and remains publishable.

## 8. The master exposure grid is non-negotiable

A confirmatory REC analysis must identify every target exposure window independently of the tested gate.

For each row, retain:

- `exposure_grid_id`;
- exposure-window start/end and duration;
- `exposure_source` and version;
- `registered_deviation` and gate version;
- `record_entry_present` and entry-policy version;
- pre-gate evidence version;
- truth-sampling inclusion probability when only a subset is reference-annotated.

If a system physically stores only event-triggered clips, an independent reference stream or fixed low-cost sampling channel is needed to reconstruct non-entered windows. Otherwise the shadow world is not empirically enumerable.

## 9. REC versus TNOA

| Question | REC | TNOA |
| --- | --- | --- |
| Where is information lost? | before/at record entry | after an observation is represented |
| Primary missing object | non-entered exposure/event | process distinction within entered record |
| Core audit variable | gate/entry indicator `R`, `K` | B/T/N/U and evidence semantics |
| Main anti-error rule | no record ≠ no event | low T / not-T ≠ biological absence |
| Required external support | master exposure grid + independent truth | calibrated evidence semantics; independent absence only for A− |
| Typical failure | event absorbed into baseline/no log entry | nuisance/U/B collapsed into binary negative |
| Main downstream risk | selection/detection gradient masquerades as ecology | coarsened observation record widens or biases ecological inference |

REC is therefore the **shadow-side companion** to TNOA, not a replacement for it.

## 10. Prior-art boundary

REC must explicitly surrender the following priority claims:

- nondetection is not absence;
- imperfect detection in occupancy or capture–recapture models;
- false-negative camera-trap detection;
- decomposition of camera-trap detection into encounter/trigger/registration/quality processes;
- paired or double-observer approaches;
- continuous-score or classification-aware occupancy modeling;
- generic censoring/truncation/missing-data theory.

The defensible REC contribution, if field evidence supports it, is narrower:

> **an auditable record-entry measurement contract that reconstructs the exposure universe, preserves pre-gate evidence and entry provenance, deliberately samples the non-entered set against independent truth, and traces condition-dependent record entry into downstream ecological conclusions before later TNOA-style semantic coarsening.**

This contribution is empirical and architectural. It is not established by the framework document alone.

## 11. Terminology discipline

Preferred manuscript terms:

- **master exposure universe/grid** — the denominator of windows independent of the tested gate;
- **registered deviation** — a window passing the frozen gate;
- **logical registered baseline** — exposure window with `R=0`;
- **record entry** — operational archival/log inclusion `K=1`;
- **record-entry shadow set** — exposure windows with `K=0`;
- **threshold-absorbed event** — independent event truth with `R=0`;
- **record-entry censoring** — the full pre-semantic selection mechanism under study.

“Shadow world” is useful project shorthand but should remain a pedagogical metaphor rather than the formal statistical term.

## 12. Hard guardrails

REC must not:

- infer `E=0` because `R=0` or `K=0`;
- treat the event log as the exposure universe;
- estimate `q_shadow` without a recoverable denominator/sampling design;
- define truth using the same gate being audited;
- retune the gate on held-out truth and then describe the result as confirmatory;
- call standard imperfect-detection ideas novel;
- claim a universal optimal gate;
- claim ecological distortion unless a downstream estimand is compared against independent truth;
- claim that every event-driven system needs the same B/T/N/U implementation.

## 13. Current implementation map

- `CHAPTER2_THRESHOLD_CENSORING.md` — gate-censoring chapter and confirmatory estimands;
- `TRUTH_AND_WINDOW_SCHEMA.md` — row-level data contract;
- `scripts/validate_chapter2_windows.py` — fail-closed structural validator;
- `PREREGISTRATION_DRAFT.md` — confirmatory freeze rules;
- issue #3 — Chapter-2 Phase-0 pilot.

The next implementation increment is to add master-exposure and archive-entry provenance to the schema/validator so Chapter 2 can distinguish a logical `B` from a physically absent event-log row.
