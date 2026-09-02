# REC identifiability boundary — what can be learned about the unrecorded world

Status: **working theory note; standard identification logic, not a novelty claim**.

## 1. Empirical object

REC does not claim access to a fundamentally unobservable biological world. Its empirical object is the part of a **predefined exposure universe** that did not enter the tested scientific record.

For exposure `i in Omega`:

- `E_i`: independent event truth (`1`, `0`, unresolved);
- `K_i`: operational record-entry indicator;
- `R_i`: registered-deviation result when the gate is evaluable;
- `A_i`: primary acquisition availability;
- `S_i`: retained pre-gate evidence where available.

Define the operational shadow set

`Omega_shadow = {i in Omega : K_i = 0}`.

The target

`q_shadow = P(E=1 | K=0)`

is a property of the exposure universe, not of the event log alone.

## 2. Proposition 1 — event-log-only shadow prevalence is not identified

Suppose the available data are only rows that entered the event log (`K=1`). Exposures with `K=0` have no rows.

Then `q_shadow` is not identified without additional information or assumptions.

Reason: the same entered event log is compatible with arbitrarily different biological contents of the non-entered set. For any chosen `q in [0,1]`, a latent completion can assign an appropriate fraction of shadow exposures `E=1` while leaving every entered row unchanged.

If even the number of non-entered exposures is unknown, both the size and composition of the shadow world are unconstrained by the event log.

If the number of `K=0` exposures is known but their event truth is not, `q_shadow` can still range from 0 to 1 absent additional assumptions.

This is the foundational REC warning:

> **An event log cannot use its own missing rows to identify what never entered the log.**

The deterministic witness in `scripts/demonstrate_eventlog_nonidentifiability.py` constructs multiple shadow-world completions with the same observed event log and different `q_shadow`.

## 3. Proposition 2 — an exposure ledger identifies the denominator, not the biology

A gate-independent master exposure universe `Omega` plus record-entry indicator `K` makes the non-entered set enumerable.

This solves the denominator problem:

- total exposure count is known;
- `K=0` exposures have explicit rows;
- acquisition/gate/archive provenance can be overlaid.

But an exposure ledger alone does **not** identify `E` inside the shadow set.

Therefore:

> **Omega is necessary for a confirmatory shadow-world claim, but Omega alone is not sufficient.**

Independent reference truth, repeated observation, a justified model, or another explicit assumption is still required to learn event content.

## 4. Proposition 3 — probability-sampled reference truth can identify shadow composition

Let shadow exposures be truth-sampled with known inclusion probabilities `pi_i > 0`, and let resolved reference truth be valid for the target event definition.

A design-weighted estimator of shadow event prevalence is the ratio

`q_hat_shadow = sum_i w_i 1(K_i=0, E_i=1) / sum_i w_i 1(K_i=0, E_i in {0,1})`,

where `w_i = 1/pi_i` for truth-sampled exposures.

The same logic applies to layer-specific REC quantities such as:

- gate-baseline contamination `q_B = P(E=1 | R=0, gate evaluable)`;
- acquisition-shadow contamination `P(E=1 | A=0)` where the reference can still resolve truth;
- event non-entry `a_K = P(K=0 | E=1)`.

Confirmatory uncertainty must resample or model **independent ecological units**, not individual frames/windows as if independent.

## 5. Proposition 4 — unresolved reference truth creates an identification interval

Reference systems are also imperfect. If some truth-sampled shadow exposures remain unresolved, REC must report the unresolved mass.

Let weighted shadow truth mass be:

- `P`: resolved event-positive mass;
- `N`: resolved event-negative mass;
- `U`: unresolved mass.

Without additional assumptions about unresolved truth, the worst-case shadow prevalence lies in

`P / (P + N + U) <= q_shadow <= (P + U) / (P + N + U)`.

This is a simple partial-identification bound, not a calibrated probabilistic interval.

If `U` is condition dependent, a complete-case estimate `P/(P+N)` may be misleading for the full shadow population. REC must then restrict the claim to the reference-resolved subpopulation, report bounds/sensitivity, or improve the reference design.

## 6. Operational shadows are not one state

REC separates at least:

1. **acquisition shadow** — primary acquisition unavailable;
2. **gate-unevaluable shadow** — acquisition exists but the frozen gate cannot be evaluated;
3. **gate shadow** — gate evaluable but no registered deviation / entry occurs;
4. **archive shadow** — a deviation/record should enter but is lost downstream;
5. **unknown shadow** — non-entry stage cannot be established.

These are measurement-process states. Each can cross event truth `E=1`, `E=0`, or unresolved.

Do not collapse them into one generic false-negative rate unless the sensor architecture makes them identical by construction.

## 7. Mirror relation to TNOA

TNOA and REC have symmetric identification warnings at different stages.

- **REC:** `no record != no event` because selection into the record is an observation process.
- **TNOA:** `not-target / low support != biological absence` because semantic coarsening inside the record is an observation process.

Full chain:

`world -> Omega -> REC acquisition/gate/entry -> entered record -> TNOA semantics -> later coarsening -> ecological inference`.

REC studies information that may disappear **before a row exists**. TNOA studies information that may disappear **after a row exists**.

## 8. What is fundamentally outside empirical REC

REC cannot identify events that are invisible to both the tested system and every available reference system without additional assumptions.

That domain is **reference-unresolved**, not a hidden population REC has somehow observed.

Safe wording:

> **REC studies the world excluded from a tested record insofar as an independently defined exposure universe and reference process make that exclusion auditable.**

## 9. Consequence for study design

A valid confirmatory REC study therefore requires, in order:

1. define `Omega` independently of the tested entry rule;
2. preserve A/R/K provenance for every exposure;
3. probability-sample or exhaustively annotate shadow exposures;
4. establish independent reference truth without using the gate being audited;
5. retain unresolved truth as unresolved;
6. estimate layer-specific shadow composition with the sampling design;
7. only then test whether condition-dependent shadow selection changes ecological inference.

Skipping step 1 turns the event log into both numerator and denominator and makes the core REC shadow question unidentifiable from the observed rows alone.
