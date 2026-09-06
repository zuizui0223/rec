# V3–REC–TNOA information-order architecture

Status: **future cross-paper architecture note. This document does not change the scientifically closed REC H1–H5 manuscript, its figures, submission claims, or the frozen TNOA Paper-1 claim.**

## 1. Why this note exists

REC and TNOA already identify two different ways ecological information can be lost:

- **REC:** exposure opportunities or biological events may fail to enter the scientific record at all;
- **TNOA:** information retained in an entered record may later be semantically collapsed into a coarser decision.

The V3/reference-guided theory adds a third operation of a different sign:

- **reference refinement:** an additional target-free reference can restrict the set of measurement-side states compatible with an observation, provided the primary observation is retained rather than replaced.

The three should not be merged into one method. They occupy different positions in an information-order architecture.

## 2. Full chain

For an exposure `i in Omega`, let:

- `S_i` be the target/process state of interest;
- `M_i` be measurement-side latent state (nuisance, geometry, visibility, sensor state, etc.);
- `Y_i = F(S_i, M_i)` be the primary measurement;
- `Q_i` be an optional target-free reference about `M_i`;
- `A_i/R_i/K_i` be REC acquisition / registration / entry provenance;
- `E_i` be the rich entered evidence representation used by TNOA;
- `c(E_i)` be any later deterministic semantic coarsening.

A useful schematic is

```text
world/process
  -> Omega exposure universe
  -> primary measurement Y + optional reference Q
  -> [reference refinement / reversible decomposition]
  -> REC acquisition / registration / entry A/R/K
  -> entered record
  -> TNOA process-preserving evidence / compatible semantic states
  -> later coarsening
  -> ecological inference
```

The bracketed reference-refinement step is **not REC**. It is an optional information-preserving measurement operation.

## 3. Three information operations

### 3.1 Reference refinement — compatible-set contraction

If retaining `(Y,Q)` restricts the measurement-state compatible set from `M(Y)` to `M(Y,Q)`, then

`M(Y,Q) subseteq M(Y)`.

For the general forward model `Y = F(S,M)`, the compatible target/process set

`S_F(Y,Q) = {s : exists m in M(Y,Q) with F(s,m)=Y}`

therefore satisfies

`S_F(Y,Q) subseteq S_F(Y)`.

This is an **information refinement**. It does not require a unique nuisance label and does not by itself license a semantic conclusion.

### 3.2 REC entry selection — support deletion in the exposure universe

REC maps a predefined `Omega` to the entered subset `K=1`.

If only the entered rows survive, the composition of `K=0` is not identified from the event table itself. The lost object is not merely a semantic label; it is support in the exposure universe / denominator.

The REC safeguard is therefore to retain:

- gate-independent `Omega`;
- A/R/K provenance;
- independent reference truth or explicit partial-identification bounds for shadow exposures.

### 3.3 TNOA semantic coarsening — compatible-state expansion

If a rich evidence record `E` is deterministically mapped to a coarser decision `c(E)`, then the set of worlds compatible with `c(E)` can only stay the same or expand relative to `E`.

The TNOA safeguard is therefore to retain positive target, nuisance, observability and attribution support separately and preserve `U` when unique interpretation is not justified.

## 4. The central asymmetry

The three operations are not three equivalent stages.

- reference refinement is potentially **information adding / identifying**;
- REC selection is potentially **row / denominator deleting**;
- semantic coarsening is potentially **state-space deleting**.

This gives a useful signed information view:

```text
reference refinement     : compatible set contracts
REC entry selection      : unentered exposure support can disappear
semantic coarsening      : compatible set expands
```

The sister-method relationship is therefore not that V3, REC and TNOA all solve the same problem. It is that each makes a different irreversible boundary explicit.

## 5. Where V3 belongs relative to REC

### Shadow-only / audit use

If a reference-derived representation is computed for every probe/exposure in `Omega` **without changing A/R/K or capture timing**, it is an auxiliary measurement channel. REC can later ask whether that channel helps explain or audit entry selection, but V3 is not part of the entry mechanism.

### Operational use

If a V3/reference-derived score changes whether an exposure is acquired, registered, saved or entered, then it becomes part of the tested REC entry policy.

In that case REC must version and audit the augmented entry function, for example

`K = g(Y, Q, provenance, policy)`.

The reference-derived gate must not be treated as an external truth source merely because it is upstream.

This distinction prevents a circular architecture in which a correction system modifies entry and is then used as the reference proving that entry was correct.

## 6. Relation to current REC H6

Current REC-H6 specifies the same-system chain

`Omega -> A/R/K [REC] -> TNOA -> binary/coarsened decision`.

The V3 theory can extend that future architecture without changing H6's current empirical contract:

```text
Omega
  -> (Y,Q) measurement record
  -> optional non-destructive reference refinement
  -> A/R/K [REC]
  -> entered rich evidence
  -> TNOA
  -> coarsening
```

For any future same-system decomposition, report the effect of each irreversible operation separately. Do not force stage errors to add algebraically for nonlinear ecological endpoints.

## 7. Strong common principle

The shared methodological rule is:

> **Do not manufacture certainty by deleting unresolved structure. Add independently justified information when available, retain provenance when rows can disappear, and preserve semantic multiplicity when evidence does not support a unique state.**

A compact formulation is:

> **Refine without discarding; audit selection before ignoring missing rows; interpret without forcing.**

## 8. What belongs in which repository / paper

### REC

Owns:

- `Omega`;
- A/R/K provenance;
- pre-entry selection and shadow composition;
- ecological estimand distortion caused by record entry;
- correction transportability for entry selection.

The current REC H1–H5 manuscript remains closed and should not absorb the new V3 theory.

### TNOA

Owns:

- positive non-complementary evidence semantics;
- T/N/U and observability / attribution boundaries;
- partial identification and safe decision coverage;
- consequences of semantic coarsening.

### V3 / reference-refinement theory

Owns:

- compatible measurement-state refinement by additional reference information;
- reversible decomposition and set-valued partial decomposition;
- conditions under which projection improves or harms target/nuisance separation;
- information-order and decision-risk corollaries.

The implementation currently lives in PolliPi because that repository supplies the executable V3 witnesses, but the theory is application-independent and should not be described as a PolliPi- or pollination-specific claim.

## 9. Empirical boundary

The structural information-order statements above do not require field data.

Empirical data are still needed to establish, in a particular system:

- whether a physical reference strictly contracts a scientifically relevant compatible set;
- calibration / coverage of the reference-derived compatible measurement-state set;
- finite-sample stability of a computational approximation;
- whether an operational reference-derived entry policy improves or worsens REC selection;
- transport across contexts or applications.

Thus the cross-layer theory can be mathematically closed before real-data transport validation, while REC and V3 application claims remain empirically testable.
