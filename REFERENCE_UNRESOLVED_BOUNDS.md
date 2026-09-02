# REC reference-unresolved bounds

Status: **design analysis; not a confidence interval; freeze before confirmatory use**.

## 1. Why this layer exists

REC can audit only the shadow world made visible by an independent exposure/reference design. Some truth-sampled exposures may still remain biologically unresolved.

Those exposures must not be silently encoded as no-event.

Instead, REC reports two distinct uncertainties:

1. **sampling/statistical uncertainty** — finite independent ecological units and a truth-sampling design;
2. **reference-resolution uncertainty** — the biological event status of truth-sampled but unresolved exposures is genuinely unknown.

This document addresses only layer 2.

## 2. Design-weighted ignorance bounds

For a prespecified operational state `H`, let design-weighted truth totals be:

- `P_H`: resolved event-positive weight inside `H`;
- `N_H`: resolved event-negative weight inside `H`;
- `U_H`: reference-unresolved weight inside `H`.

The event prevalence/contamination within `H` is bounded by assigning every unresolved exposure first to no-event and then to event:

`q_H_lower = P_H / (P_H + N_H + U_H)`

`q_H_upper = (P_H + U_H) / (P_H + N_H + U_H)`.

The resolved-only descriptive estimate

`q_H_resolved = P_H / (P_H + N_H)`

is reported separately and is **not** substituted for the full target when unresolved mass is non-zero.

## 3. Bounds on event loss into a shadow state

Suppose `H` is the shadow state of interest and `C` is its prespecified complement within the relevant target population.

Let:

- `P_H`, `U_H`: resolved-positive and unresolved weight inside H;
- `P_C`, `U_C`: resolved-positive and unresolved weight inside C.

For

`a_H = P(H | E=1)`

no assumptions about unresolved event status give:

`a_H_lower = P_H / (P_H + P_C + U_C)`

`a_H_upper = (P_H + U_H) / (P_H + U_H + P_C)`.

The lower bound assigns unresolved H exposures to no-event and unresolved complement exposures to event. The upper bound does the reverse.

This is a worst-case missing-truth envelope, not a confidence interval and not a distribution-free risk guarantee.

## 4. REC layers analyzed separately

### Acquisition shadow

`H_A = {primary_stream_available=False}`.

Complement: primary stream available.

Report:

- `q_A = P(E=1 | H_A)` bounds;
- `a_A = P(H_A | E=1)` bounds.

Planned non-acquisition and acquisition failure may be split later if frozen before confirmatory truth is opened.

### Gate-unevaluable shadow

To avoid double-counting acquisition failure:

`H_G = {primary_stream_available=True, gate_evaluable=False}`.

Complement for its event-loss estimand: all other target exposures in the master truth-sampling target.

Report `q_G` and `a_G` separately from gate absorption.

### Gate baseline / threshold absorption

This analysis is conditional on gate evaluability.

`H_R = {gate_evaluable=True, registered_deviation=False}`

`C_R = {gate_evaluable=True, registered_deviation=True}`.

Report:

- `q_B = P(E=1 | R=0, gate evaluable)` bounds;
- `a_R = P(R=0 | E=1, gate evaluable)` bounds.

Acquisition and gate-unevaluable exposures are outside this denominator rather than being treated as `R=0`.

### Record-entry shadow

`H_K = {record_entry_present=False}`

`C_K = {record_entry_present=True}`.

Report `q_K` and `a_K` bounds.

This layer may contain acquisition, gate, or archive mechanisms; the exposure ledger is used to decompose them.

## 5. Sampling-design boundary

The implementation uses `truth_sampling_weight` from the frozen probability-sampling design.

These weighted bounds describe the audited target represented by that design. They are not automatically exact finite-population identification intervals merely because inverse-inclusion weights are present.

A confirmatory paper must separately state:

- the target exposure population;
- the sampling design;
- how design uncertainty is handled;
- the independent ecological unit used for inferential uncertainty.

Do not call the worst-case unresolved envelope a confidence interval.

## 6. Unresolved-mass diagnostics

For every layer report:

- total design weight in H;
- resolved-positive, resolved-negative, unresolved weight;
- unresolved fraction in H;
- resolved-only estimate;
- lower/upper ignorance bounds;
- bound width.

For event-loss estimands also report unresolved weight in both H and its complement.

Large or condition-dependent unresolved mass is itself a measurement result. It may justify improving the reference system or restricting claims to a reference-resolved subpopulation.

## 7. Interpretation ladder

### Width approximately zero

Reference truth is effectively resolved for the target quantity under the audited design.

### Non-zero but narrow width

Point conclusions may be relatively insensitive to unresolved truth, subject to ordinary sampling uncertainty.

### Wide width

REC should not present a precise event-loss/contamination rate. The correct result is that the available reference design does not identify the quantity tightly enough.

### Bounds cross an ecological decision threshold

The downstream ecological conclusion is not robust to unresolved truth. Do not choose the favourable endpoint.

## 8. Relationship to TNOA

This is the upstream analogue of TNOA preserving `U` rather than forcing uncertain observations into a negative class.

- TNOA: unresolved semantic evidence stays unresolved.
- REC: unresolved reference truth contributes identification width rather than being imputed as no-event.

The common principle is:

> **uncertainty is represented where it arises instead of being converted into absence.**

## 9. Executable analysis

```bash
python scripts/analyze_unresolved_bounds.py examples/chapter2_windows.csv
```

The output must be interpreted together with the validated master exposure ledger and the frozen truth-sampling design.
