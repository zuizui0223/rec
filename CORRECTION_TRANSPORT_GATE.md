# Correction transport gate

REC's H5 result is deliberately conditional: entry-aware correction can reduce ecological error in matched or partly transported settings, but the frozen camera + position double holdout worsened average error. A correction model therefore has a **validated transport domain** rather than a universal right to be applied.

This note makes that operational rule executable.

## Core transition rule

A proposed correction is admissible only when both conditions hold:

```text
1. the correction/transport validation has passed;
2. the query lies inside an explicitly validated
   hardware x observation-context cell.
```

Otherwise the transition from raw estimate to corrected estimate is withheld.

Implementation:

- `scripts/correction_transport_gate.py`
- `scripts/verify_correction_transport_gate.py`

The gate is intentionally simple and exact. It does not estimate detection probability, fit inverse-probability weights, or decide how broad a transport domain should be. Those are empirical/modeling tasks upstream of the gate.

## Why exact cells first?

The current REC evidence already shows that correction portability can fail when both hardware and observation context change. The safest initial contract is therefore finite and fail-closed:

```text
validated cell
-> correction may be applied

new hardware
-> withhold until transport is validated

new observation context
-> withhold until transport is validated

validation failed
-> withhold even inside a nominally familiar cell.
```

A later model may replace exact cells with a prospectively validated metric neighbourhood or transport model. That extension must itself demonstrate held-out transport performance; the current gate does not infer neighbourhood similarity automatically.

## Relation to REC's identifiability boundary

The gate does not repair records that never entered. It operates only after a correction model has been estimated using appropriate exposure/reference information.

Thus the existing REC rule remains:

```text
better downstream semantics
!= reconstruction of upstream omitted rows without additional information.
```

The new rule adds:

```text
correction successful somewhere
!= correction licensed everywhere.
```

## Verification

Run from `scripts/`:

```bash
python verify_correction_transport_gate.py
```

The verifier checks:

1. validated hardware + validated context + passed validation -> admissible;
2. new hardware -> withheld;
3. new context -> withheld;
4. failed validation -> withheld even for a listed cell.

This is an implementation of REC's existing transport-boundary logic, not a new empirical H5 result.
