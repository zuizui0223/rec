# REC field truth and observation-window schema

Status: **design contract; freeze before confirmatory collection**.

## 1. Principle

REC separates the exposure universe, primary acquisition, gate evaluability, gate result, record entry, independent truth, and later TNOA semantics.

No field may be silently inferred from another.

The pre-TNOA chain is:

`Omega -> acquisition A -> gate evaluability -> gate R -> entry K -> entered record -> TNOA`.

A missing or non-evaluable stage is not encoded as a negative result at the next stage.

## 2. Master exposure provenance

Every row belongs to a frozen exposure universe generated independently of the tested gate.

Required:

- `exposure_grid_id`
- `exposure_source`
- `exposure_source_version`
- `exposure_defined_independently_of_gate`

Valid exposure sources include a fixed clock, continuous independent reference stream, continuous primary stream, or another predeclared schedule.

An event log alone is not a valid exposure denominator for an event-triggered system.

## 3. Required identifiers

- `system_id`
- `site_id`
- `camera_or_sensor_id`
- `recording_day`
- `recording_block_id`
- `window_id`
- `window_start`
- `window_end`
- `exposure_seconds`
- `development_or_heldout`

`window_id` is unique and joins the truth table to the master exposure ledger.

Development/held-out assignment is made at an independent grouping level, not frame by frame.

## 4. Primary acquisition A

Required:

- `primary_stream_expected`
- `primary_stream_available`
- `acquisition_status`
- `pregate_evidence_version`

Controlled `acquisition_status` values:

- `available`
- `planned_not_acquired`
- `hardware_failure`
- `corrupt_or_missing`
- `unknown_unavailable`

Rules:

- available primary stream -> `acquisition_status=available`;
- `planned_not_acquired` requires primary acquisition not expected and unavailable;
- expected-but-unavailable acquisition is an acquisition shadow;
- acquisition unavailable does not imply biological no-event.

Retain every pre-gate quantity used by the tested gate whenever technically available, including raw target/nuisance/observability/coupled-response diagnostics.

## 5. Gate evaluability and registered deviation R

Required:

- `gate_evaluable`
- `registered_deviation`
- `gate_type`
- `gate_version`
- `gate_configuration_id`
- `gate_threshold`
- `gate_inputs_complete`

Gate types:

- `scalar`
- `composite`

Semantics:

### Gate evaluable

If `gate_evaluable=True`:

- primary acquisition must be available;
- required gate inputs must be complete;
- `registered_deviation` must be explicitly `true` or `false`.

`registered_deviation=False` is logical registered baseline at the gate layer. It means **no registered deviation under that frozen rule**, not biological absence.

### Gate not evaluable

If `gate_evaluable=False`:

- `registered_deviation` must be blank/undefined;
- it must not be encoded as `false`;
- `threshold_absorbed_event` is undefined.

This rule prevents an unobservable or unavailable primary window from being silently transformed into baseline.

For a scalar gate, a real numeric threshold is required. For a composite gate, do not invent a pseudo-scalar threshold.

## 6. Record-entry layer K

Required:

- `record_entry_present`
- `entry_policy_version`
- `entry_policy_type`
- `entry_policy_inputs_complete`

Controlled entry-policy types:

- `trigger_only`
- `fixed_schedule`
- `hybrid`
- `postcapture_filter`
- `other`

Optional provenance:

- `record_entry_id`
- `entry_failure_reason`
- `storage_retention_stage`

Examples:

- gate false, entry true: stored baseline under fixed/hybrid acquisition;
- gate false, entry false: gate/entry shadow under an event-driven policy;
- gate true, entry false: archive/retention loss;
- acquisition unavailable: gate result undefined; do not call this gate rejection.

Record entry is a measurement-process state, not event truth.

## 7. Independent reference truth

Reference truth is established independently of the tested primary gate and entry policy.

Required:

- `target_truth`: `positive / negative / unresolved`
- `target_truth_source`
- `target_event_definition_version`

Optional:

- `target_count_or_event_count`
- nuisance truth families
- observability truth
- coupled-response truth
- attribution truth

Reference annotators should be blind to primary scores, gate status, entry status, and TNOA output whenever practical.

Reference unresolved is never converted to negative truth by default.

## 8. Derived REC event labels

These are derived, never primary hand annotations.

### Threshold-absorbed event

Defined only when the gate is evaluable:

`threshold_absorbed_event = target_truth=positive AND gate_evaluable=True AND registered_deviation=False`.

### Shadow event

`shadow_event = target_truth=positive AND record_entry_present=False`.

### Acquisition-shadow event

`acquisition_shadow_event = target_truth=positive AND primary_stream_available=False`.

The first is undefined if the gate was not evaluable. The second and third may still be established if independent reference truth resolves the event.

## 9. Truth-sampling provenance

Because B and non-entered exposures may dominate the denominator, probability sampling is allowed.

Required for every row:

- `truth_sampled`
- `truth_sampling_design_version`
- `truth_sampling_stratum`
- `truth_inclusion_probability`
- `truth_sampling_weight`

For sampled truth, `weight = 1 / inclusion_probability` under the current simple contract.

For unsampled truth:

- `target_truth` must remain `unresolved` in the audit table;
- sampling-specific numeric fields remain blank.

Suspicious shadow windows may not be added preferentially to confirmatory truth without recoverable inclusion probabilities or explicit exploratory status.

## 10. Annotation provenance

Required:

- `annotator_blinded_to_gate`
- `annotator_blinded_to_entry`
- `annotator_blinded_to_scores`

Recommended:

- primary/secondary annotator IDs
- adjudication status
- annotation duration
- annotation version

Protected double-annotation subsets are selected before adjudication.

## 11. Relation to TNOA

Where an observation enters the semantic record, downstream fields may include:

- `decision`: B/T/N/U
- `reason`
- `decision_rule_version`
- later `binary_target`
- `binary_mapping_version`

A physically non-entered exposure may have no TNOA decision at all. REC still retains the exposure through `Omega`.

Therefore:

- REC: `no record != no event`;
- TNOA: `not-target / low support != biological absence`.

## 12. REC estimands

### Acquisition-shadow contamination

`q_A = P(E=1 | primary unavailable, truth resolved)`.

### Event acquisition loss

`a_A = P(primary unavailable | E=1, truth resolved)`.

### Gate-baseline contamination

Conditional on gate evaluability:

`q_B = P(E=1 | R=0, gate evaluable, truth resolved)`.

### Event gate absorption

`a_R = P(R=0 | E=1, gate evaluable, truth resolved)`.

### Record-entry shadow contamination

`q_K = P(E=1 | K=0, truth resolved)`.

### Event non-entry

`a_K = P(K=0 | E=1, truth resolved)`.

Always state the conditioning set. Do not combine these into one generic false-negative rate unless the sensor architecture makes them identical by design.

## 13. Ecological-unit table

Aggregate only after window-level provenance is frozen.

Shared columns should include:

- `ecological_unit_id`
- `total_exposure_windows`
- `resolved_reference_windows`
- `unresolved_reference_windows`
- `reference_target_positive_windows`
- `reference_target_prevalence`
- acquisition-shadow fraction
- gate-unevaluable fraction
- registered-baseline fraction
- record-nonentry fraction
- reference-positive counts within each shadow layer
- prespecified ecological/measurement covariates

Chapter-1 downstream comparison may additionally store binary and process-resolved estimates.

Population estimates based on sampled truth use the frozen sampling design.

## 14. Fail-closed checks

A confirmatory row is invalid rather than silently repaired if:

- exposure denominator provenance is missing or gate-defined;
- development/held-out groups leak;
- primary acquisition state is internally inconsistent;
- gate is marked evaluable without available primary evidence and complete inputs;
- gate is not evaluable but `registered_deviation` is encoded as false/true;
- a scalar threshold is invented for a composite gate;
- record entry is present without available primary acquisition under the current architecture;
- resolved truth is attached to an unsampled row;
- sampling weight disagrees with the frozen inclusion probability;
- `threshold_absorbed_event` is supplied when gate is non-evaluable;
- any derived shadow flag disagrees with independently recorded truth and pipeline state;
- required reference evidence is missing for a biological claim.

Invalid rows are counted/reported; they are not silently repaired into baseline or no-event.

## 15. Executable contracts

Master exposure ledger:

```bash
python scripts/validate_exposure_ledger.py examples/exposure_ledger.csv
```

Truth/gate/entry audit:

```bash
python scripts/validate_chapter2_windows.py examples/chapter2_windows.csv
```

Joined layer analysis:

```bash
python scripts/analyze_shadow_selection.py \
  examples/exposure_ledger.csv \
  examples/chapter2_windows.csv
```
