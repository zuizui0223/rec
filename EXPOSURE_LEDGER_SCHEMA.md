# REC master exposure ledger schema

Status: **design contract; freeze before confirmatory use**.

## 1. Purpose

The REC shadow set cannot be reconstructed from an event log alone because non-entered exposures have no event-log row. REC therefore requires a **master exposure ledger** whose rows are created independently of the tested gate or archive policy.

The ledger is the empirical denominator for the record-entry process.

> **No exposure ledger, no confirmatory claim about the non-entered world.**

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
- `record_entry_present`
- `record_entry_policy_version`
- `record_entry_id`
- `record_entry_timestamp`
- `record_entry_reason`

`window_id` is the join key used by the Chapter-2 audit table.

## 3. Exposure source

`exposure_source` explains why the row exists independently of the tested record-entry mechanism. Examples:

- `fixed_clock`
- `continuous_reference_stream`
- `continuous_primary_stream`
- `external_schedule`
- another predeclared source.

The tested event gate itself cannot be the exposure source.

`exposure_source_version` freezes the rule used to generate the grid.

## 4. Record-entry indicator K

`record_entry_present` is the empirical `K` indicator.

- `True`: an operational record/event-log entry exists for this exposure;
- `False`: no operational record/event-log entry exists for this exposure.

If `record_entry_present=True`, both `record_entry_id` and `record_entry_timestamp` are required.

If `record_entry_present=False`, `record_entry_id` and `record_entry_timestamp` must be empty. Do not fabricate a placeholder event row.

`record_entry_reason` records only what is independently known about the entry mechanism. Recommended controlled values:

- `entered`
- `gate_rejected`
- `archive_policy_excluded`
- `storage_failure`
- `primary_stream_failure`
- `unknown`
- `not_applicable`

Do not infer `gate_rejected` simply because no record exists unless gate provenance establishes that fact.

## 5. Distinguish R from K

REC keeps the registration gate `R` and operational record entry `K` separate.

Examples:

- `R=0, K=1`: a fixed-schedule system stores a baseline window;
- `R=0, K=0`: an event-driven system stores nothing after gate rejection;
- `R=1, K=1`: registered deviation enters the log;
- `R=1, K=0`: possible downstream archive/storage failure and therefore a distinct failure mode.

The master ledger records `K`; the Chapter-2 window table records `R` where the gate can be reconstructed/audited.

## 6. Joining to Chapter-2 truth audit

The Chapter-2 truth/audit table may contain all exposures or a probability sample.

Every Chapter-2 `window_id` must exist in the master exposure ledger.

When truth annotation is sampled, inclusion probabilities belong to the Chapter-2 truth-sampling design, not to the exposure ledger itself.

Population quantities such as

`q_shadow = P(E=1 | K=0)`

must be estimated using the frozen truth-sampling design over the master ledger.

## 7. Required invariants

A valid ledger must satisfy:

1. `window_id` unique within the ledger;
2. every row has positive exposure duration;
3. `exposure_expected=True` for ledger members;
4. exposure source/version is present;
5. record-entry policy version is present;
6. entered rows have unique record-entry IDs and timestamps;
7. non-entered rows have no fabricated record-entry ID/timestamp;
8. `record_entry_reason=entered` iff `record_entry_present=True`;
9. a record cannot exist when `primary_stream_expected=False` unless a separately documented architecture permits it;
10. development/held-out assignment, if added later, must occur by independent grouping rather than individual event rows.

## 8. What the ledger does not establish

The ledger alone does not establish:

- biological event truth;
- why a gate failed;
- sensor observability;
- biological absence;
- whether a non-entered exposure contained an event.

Those require Chapter-2 independent truth/audit fields.

## 9. Continuous versus event-triggered systems

### Continuous system

A continuous audio/video stream can define `Omega` directly by a frozen time grid. Operational event detections become `K` or `R` overlays on that denominator.

### Event-triggered-only system

An event log cannot define `Omega` because exposures with no trigger are absent from the log. A separate fixed clock, independent reference stream, time-lapse channel or other exposure-accounting mechanism is required.

This is why a public event-triggered image archive may be sufficient for post-entry TNOA analyses but insufficient for REC shadow-world identification.

## 10. Executable validation

Validate a ledger with:

```bash
python scripts/validate_exposure_ledger.py exposures.csv
```

Optionally cross-check a Chapter-2 audit table:

```bash
python scripts/validate_exposure_ledger.py exposures.csv \
  --window-table chapter2_windows.csv
```

The validator is structural and fail-closed. It does not infer missing exposures or repair the record-entry process.
