# Paper 2 field truth and REC observation-window schema

Status: design draft; freeze before confirmatory field collection.

## Principle

The exposure universe, gate evaluability, gate result, archive/record-entry policy, independent truth and downstream ecological unit must be separately addressable. No field may be silently inferred from another.

The crucial distinction for staged sensors is:

> **not-evaluable is not baseline.**

A prerequisite failure can prevent a downstream gate from being evaluated at all. Such windows remain in the master exposure universe but must not be counted as logical baseline.

## Master exposure universe

REC requires an exposure denominator independent of the tested gate.

Each row belongs to a frozen master exposure grid and includes:

- `exposure_grid_id`
- `exposure_source`
- `exposure_source_version`
- `exposure_defined_independently_of_gate`: boolean

An event-triggered event log is not an acceptable exposure source because non-entered windows are missing from that log by construction.

## Required identifiers

Each exposure window includes:

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

`window_id` must be unique. `development_or_heldout` is assigned at the group level before calibration.

## Primary-stream pre-gate evidence

These are measurements, not truth, and should be retained for all windows where technically available:

- `target_raw_score`
- `nuisance_raw_score_*`
- `observability_raw_*`
- `coupled_response_raw_*` if applicable
- `primary_stream_available`
- `pregate_evidence_version`

If a physically non-entered or not-evaluable window lacks some primary evidence, preserve that missingness explicitly. Do not fabricate unavailable evidence.

## REC gate layer

Required fields:

- `gate_evaluable`: boolean
- `registered_deviation`: boolean
- `gate_not_evaluable_reason`
- `gate_type`: scalar / composite
- `gate_version`
- `gate_configuration_id`
- `gate_threshold` if and only if a real scalar threshold exists
- `gate_inputs_complete`: boolean

The Boolean `registered_deviation` is meaningful **only when `gate_evaluable=True`**. For row-oriented storage, not-evaluable windows use `registered_deviation=False` as a placeholder, but they are excluded from logical-baseline denominators.

Semantics:

- `gate_evaluable=True, registered_deviation=True` → registered deviation;
- `gate_evaluable=True, registered_deviation=False` → logical registered baseline `B_reg`;
- `gate_evaluable=False` → prerequisite/measurement path prevented gate evaluation; this is **not B**.

If `gate_evaluable=False`, `gate_not_evaluable_reason` is required, for example:

- `missing_focal_roi`
- `primary_stream_unavailable`
- `insufficient_gate_inputs`
- `hardware_state`
- `other`

If `gate_evaluable=True`, `gate_inputs_complete=True` is required.

Do not invent a scalar threshold for a composite gate.

## REC archive / record-entry layer

Gate state and physical record entry are separate objects.

Required fields:

- `record_entry_present`: boolean
- `entry_policy_version`
- `entry_policy_type`: `trigger_only` / `fixed_schedule` / `hybrid` / `postcapture_filter` / `other`
- `entry_policy_inputs_complete`: boolean

Optional fields:

- `record_entry_id`
- `entry_failure_reason`
- `storage_retention_stage`

Interpretation examples:

- evaluable logical B + entry present: baseline exposure is stored;
- evaluable logical B + no entry: logical B also lies in the archive shadow set;
- not-evaluable + no entry: pre-gate measurement shadow;
- registered deviation + no entry: later archival/retention loss, not baseline.

Do not assume `record_entry_present == registered_deviation` unless a versioned policy actually defines that equality.

## Frozen calibrated support fields

Produced only after development calibration is frozen:

- `target_supported`
- `nuisance_supported`
- `observable_supported`
- `coupled_response_supported`
- `attribution_supported`
- `calibration_manifest_id`

Calibrated T/N/U adjudication occurs only after the registered-deviation gate. Positive post-gate support while `gate_evaluable=False` or while the pipeline defines logical B is an internal contradiction unless a different pipeline is explicitly versioned.

## TNOA record

Where a logical observation record is represented:

- `decision`: B / T / N / U
- `reason`
- `decision_rule_version`

Do not infer biological absence from B, N, U, not-evaluable, no record entry, or low target score.

A not-evaluable or physically non-entered exposure may have no TNOA decision because TNOA begins after record representation. REC still retains the exposure through the independent master grid.

## Binary comparator

Where Chapter 1 is evaluated:

- `binary_target`
- `binary_mapping_version`

The binary mapping must be a frozen deterministic coarsening of the process-resolved record. It cannot be retuned on held-out truth.

## Independent reference truth

Reference annotators must not see model scores, gate evaluability/result, entry status or TNOA decisions during primary truth annotation whenever practical.

### Biological event

- `target_truth`: positive / negative / unresolved
- `target_truth_source`
- `target_event_definition_version`
- `target_count_or_event_count` if relevant

Derived REC fields:

- `threshold_absorbed_event`: `target_truth=positive AND gate_evaluable=True AND registered_deviation=False`
- `gate_unevaluable_event`: `target_truth=positive AND gate_evaluable=False`
- `shadow_event`: `target_truth=positive AND record_entry_present=False`

Never manually define these from algorithm output; derive them from separately recorded truth and pipeline state.

### Nuisance

For each predeclared family:

- `nuisance_truth_<family>`: present / absent / unresolved
- `nuisance_effect_<family>`: masks_target / mimics_target / attribution_conflict / acquisition_fault / none / unresolved

### Observability

- `observability_truth`: observable / compromised / unobservable / unresolved
- `observability_reason`: occlusion / blur / exposure / framing / temporal_gap / hardware / masking / other / none

Recommended independently defensible measurements:

- `occlusion_grade`
- `target_scale_or_distance_proxy`
- `illumination_grade`
- `masking_grade`

### Coupled response and attribution

If used:

- `coupled_response_truth`: present / absent / unresolved
- `attribution_truth`: supported / unsupported / unresolved
- `attribution_reference_channel`

## Truth-sampling provenance

Because baseline, not-evaluable and shadow windows may be common, REC may use prespecified stratified truth annotation.

For every exposure row store:

- `truth_sampled`: boolean
- `truth_sampling_design_version`
- `truth_sampling_stratum`
- `truth_inclusion_probability`
- `truth_sampling_weight`

At minimum, the design must permit reconstruction across:

- gate evaluability;
- registered-deviation state among evaluable windows;
- record-entry state;
- independent ecological unit;
- frozen REC condition strata.

## Annotation provenance

- `annotator_id_primary`
- `annotator_id_secondary` where double-coded
- `adjudicated`
- `adjudication_status`
- `annotation_duration_seconds`
- `annotation_version`
- `annotator_blinded_to_gate`
- `annotator_blinded_to_entry`
- `annotator_blinded_to_scores`

## Ecological-unit table

A separate table aggregates master exposure windows to the frozen ecological unit.

Required shared columns:

- `ecological_unit_id`
- `site_id`
- `recording_day`
- `total_exposure_windows`
- `resolved_reference_windows`
- `unresolved_reference_windows`
- `reference_target_positive_windows`
- `reference_target_prevalence`
- prespecified ecological covariate(s)

Required REC/Chapter-2 columns where estimable:

- `gate_not_evaluable_windows`
- `registered_baseline_windows`
- `registered_deviation_windows`
- `truth_sampled_registered_baseline_windows`
- `reference_positive_registered_baseline_windows`
- `baseline_contamination_estimate`
- `reference_positive_gate_not_evaluable_windows`
- `gate_unevaluable_event_fraction`
- `reference_positive_windows`
- `threshold_absorbed_positive_windows`
- `event_baseline_absorption_estimate`
- `nonentered_exposure_windows`
- `truth_sampled_nonentered_windows`
- `reference_positive_nonentered_windows`
- `shadow_contamination_estimate`
- `event_nonentry_estimate`
- `gate_version`
- `entry_policy_version`

Required Chapter-1 columns:

- `binary_target_prevalence_or_model_estimate`
- `process_resolved_target_prevalence_or_model_estimate`
- `verified_nuisance_fraction`
- `compromised_observability_fraction`

Population estimates based on sampled baseline/not-evaluable/shadow windows must honor the frozen sampling design.

## REC derived quantities

### Logical baseline contamination

`q_B = P(target_truth=positive | gate_evaluable=True, registered_deviation=False, truth resolved)`.

### Baseline absorption among true events

`a_B = P(gate_evaluable=True, registered_deviation=False | target_truth=positive)`.

### Gate-not-evaluable event loss

`a_U = P(gate_evaluable=False | target_truth=positive)`.

### Total failure to register deviation

`a_pre = P(gate_evaluable=False OR registered_deviation=False | target_truth=positive)`.

Report `a_B` and `a_U` separately even if `a_pre` is also shown.

### Shadow contamination

`q_shadow = P(target_truth=positive | record_entry_present=False, truth resolved)`.

### Event non-entry

`a_K = P(record_entry_present=False | target_truth=positive)`.

Keep these quantities separate; they condition on different stages and denominators.

## Fail-closed validity checks

A confirmatory row is invalid rather than silently repaired if:

- the master exposure identifier/source/version is missing;
- exposure is not defined independently of the tested gate;
- a held-out group also appears in development;
- exposure is zero or missing;
- gate version/configuration is missing;
- `gate_evaluable=False` but `registered_deviation=True`;
- `gate_evaluable=False` without a not-evaluable reason;
- `gate_evaluable=True` but required gate inputs are incomplete;
- scalar/composite threshold representation is inconsistent;
- entry policy version/type is missing;
- `record_entry_present=True` while required entry-policy inputs are incomplete;
- resolved truth appears on a truth-unsampled row;
- sampling weight is inconsistent with inclusion probability;
- any derived absorbed/unevaluable/shadow flag disagrees with separately recorded truth and pipeline state;
- no truth-sampled evaluable logical-B window exists;
- not-evaluable windows exist but the frozen design requires their estimation and none are truth-sampled;
- non-entered exposures exist but none are truth-sampled;
- required independent reference channel is missing.

Invalid rows and reasons are counted and reported; they are not silently dropped.

## Pilot-only fields

The pilot may additionally record:

- annotation difficulty score;
- candidate nuisance-family notes;
- candidate window-boundary notes;
- candidate exposure-grid alternatives;
- candidate not-evaluable reason refinements;
- candidate REC condition-stratum notes;
- candidate gate-component diagnostics;
- candidate entry-policy diagnostics;
- hardware failure diagnostics;
- proposed ecological grouping alternatives.

These may inform the frozen confirmatory schema but cannot be introduced after confirmatory truth is opened.
