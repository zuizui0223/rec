# REC master exposure ledger schema

Status: **design contract; freeze before confirmatory use**.

## 1. Purpose

The REC shadow set cannot be reconstructed from an event log alone because non-entered exposures have no event-log row. REC therefore requires a **master exposure ledger** whose rows are created independently of the tested gate, acquisition failure, or archive policy.

> **No exposure ledger, no confirmatory claim about the non-entered world.**

The ledger separates three pre-TNOA questions:

- `A`: was the primary acquisition available?
- `R`: was the registered-deviation gate evaluable?
- `K`: did an operational scientific record enter the archive/event log?

Do not collapse acquisition failure, gate rejection, and archive loss into one generic nondetection.

## 2. One row = one exposure opportunity

Each row represents a frozen observation opportunity in the master exposure universe `Omega`.

Required fields:

- `exposure_grid_id`
- `window_id`
- `system_id`
- `site_id`
- `camera_or_sensor_id`
- `recording_day`
- `recording_block_id`
- `window_start`
- `window_end`
- `exposure_seconds`
- `exposure_source`
- `exposure_source_version`
- `exposure_expected`
- `primary_stream_expected`
- `primary_stream_available`
- `acquisition_status`
- `gate_evaluable`
- `record_entry_present`
- `record_entry_policy_version`
- `record_entry_id`
- `record_entry_timestamp`
- `record_entry_reason`

`window_id` is the join key used by the Chapter-2 truth/gate audit table.

## 3. Exposure source and denominator

`exposure_source` explains why the row exists independently of the tested record-entry mechanism. Examples:

- `fixed_clock`
- `continuous_reference_stream`
- `continuous_primary_stream`
- `external_schedule`
- another predeclared source.

The tested event gate itself cannot be the exposure source.

`exposure_source_version` freezes the rule used to generate `Omega`.

A missing event-log row is not allowed to define the denominator.

## 4. Primary acquisition A

`primary_stream_available=True` means the primary evidence needed by the tested observation pipeline exists and is usable enough to attempt the frozen gate logic.

`acquisition_status` must be one of:

- `available`
- `planned_not_acquired`
- `hardware_failure`
- `corrupt_or_missing`
- `unknown_unavailable`

Rules:

- `primary_stream_available=True` requires `acquisition_status=available`;
- `planned_not_acquired` requires `primary_stream_expected=False` and `primary_stream_available=False`;
- failure/unavailable statuses require `primary_stream_available=False`;
- if the primary stream was expected but unavailable, this is an **acquisition shadow**, not a gate miss.

## 5. Gate evaluability R

`gate_evaluable=True` means the frozen registered-deviation rule can be evaluated from the retained primary inputs.

- `gate_evaluable=True` requires `primary_stream_available=True`;
- if primary acquisition is unavailable, the gate result is undefined rather than negative;
- if acquisition exists but required gate inputs are incomplete, use `gate_evaluable=False` and preserve the reason in the Chapter-2 gate table.

The actual registered-deviation result belongs to the Chapter-2 window table. The exposure ledger only establishes whether that result could legitimately exist.

## 6. Record-entry indicator K

`record_entry_present` is the empirical `K` indicator.

- `True`: an operational record/event-log entry exists for this exposure;
- `False`: no operational record/event-log entry exists for this exposure.

If `record_entry_present=True`, both `record_entry_id` and `record_entry_timestamp` are required.

If `record_entry_present=False`, those fields must be empty. Do not fabricate placeholder event rows.

`record_entry_reason` controlled values:

- `entered`
- `gate_rejected`
- `gate_not_evaluable`
- `archive_policy_excluded`
- `storage_failure`
- `primary_stream_failure`
- `unknown`
- `not_applicable`

Guardrails:

- `gate_rejected` requires available primary acquisition and an evaluable gate;
- `gate_not_evaluable` requires available primary acquisition and a non-evaluable gate;
- `primary_stream_failure` requires unavailable primary acquisition;
- `record_entry_reason=entered` iff `record_entry_present=True`.

Do not infer `gate_rejected` merely because no record exists.

## 7. REC shadow classes

The ledger permits reproducible operational shadow classes.

### Entered world

`K=1`.

### Planned non-acquisition shadow

`A=0` because the frozen design did not schedule primary acquisition for that exposure.

### Acquisition-failure shadow

`A=0` despite primary acquisition being expected.

### Gate shadow

`A=1`, gate evaluable, `K=0`, with independently established `record_entry_reason=gate_rejected`.

### Gate-unevaluable shadow

`A=1`, gate not evaluable, `K=0`.

### Archive shadow

Primary acquisition exists and entry is lost after gate/registration because of archive policy or storage failure.

### Unknown shadow

`K=0` but the responsible pre-entry stage cannot be established.

These are measurement-process states, not biological states.

## 8. Relationship between R and K

REC keeps the registered-deviation gate and operational record entry separate.

Examples:

- gate says no deviation, `K=1`: fixed-schedule system stores a baseline window;
- gate says no deviation, `K=0`: event-driven system stores nothing after gate rejection;
- gate says deviation, `K=1`: registered deviation enters the log;
- gate says deviation, `K=0`: downstream archive/storage loss;
- acquisition unavailable: gate is not evaluable at all.

Never code the last case as `registered_deviation=False`.

## 9. Joining to Chapter-2 truth audit

Every Chapter-2 `window_id` must exist in the master exposure ledger.

The Chapter-2 table may contain all exposures or a probability sample. When truth annotation is sampled, inclusion probabilities belong to the Chapter-2 truth-sampling design.

The ledger should cross-check acquisition/gate-evaluability fields when they are also present in the Chapter-2 table.

Population quantities such as

`q_shadow = P(E=1 | K=0)`

must use the frozen truth-sampling design over the master ledger.

Chapter-2 gate absorption such as

`P(R=0 | E=1)`

must be conditioned on gate-evaluable primary acquisition. Acquisition failures are a separate REC layer.

## 10. Required invariants

A valid ledger must satisfy:

1. `window_id` unique;
2. positive exposure duration;
3. `exposure_expected=True` for ledger members;
4. exposure source/version present;
5. acquisition state internally consistent;
6. gate cannot be evaluable without primary acquisition;
7. record-entry policy version present;
8. entered rows have unique record-entry IDs and timestamps;
9. non-entered rows have no fabricated record-entry ID/timestamp;
10. record-entry reason is compatible with acquisition and gate-evaluability state;
11. development/held-out assignment, if added later, occurs by independent grouping rather than event rows.

## 11. What the ledger does not establish

The ledger alone does not establish:

- biological event truth;
- biological absence;
- why a gate rejected an event unless gate provenance is separately available;
- observability truth;
- whether a non-entered exposure contained an event.

Those require independent reference truth/audit data.

## 12. Continuous versus event-triggered systems

### Continuous system

A continuous audio/video/reference stream can define `Omega` by a frozen time grid. Acquisition, gate and event-entry states are overlays on that denominator.

### Event-triggered-only system

An event log cannot define `Omega` because exposures with no trigger are absent from the log. A separate fixed clock, independent reference stream, time-lapse channel or other exposure-accounting mechanism is required.

This is why event-triggered image archives may support post-entry TNOA analyses but not full REC shadow-world identification.

## 13. Executable validation

```bash
python scripts/validate_exposure_ledger.py exposures.csv
```

Optional Chapter-2 join check:

```bash
python scripts/validate_exposure_ledger.py exposures.csv \
  --window-table chapter2_windows.csv
```

The validator is structural and fail-closed. It does not infer missing exposures, biological truth, or missing gate results.
