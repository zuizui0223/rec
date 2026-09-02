# Paper 2 field truth and REC observation-window schema

Status: design draft; freeze before confirmatory field collection.

## Principle

The exposure universe, primary sensor output, registered-deviation gate, archive/record-entry policy, independent truth and downstream ecological unit must be separately addressable. No field may be silently inferred from another.

## Master exposure universe

REC requires an exposure denominator independent of the tested gate.

Each row belongs to a frozen master exposure grid and must include:

- `exposure_grid_id`
- `exposure_source`
- `exposure_source_version`
- `exposure_defined_independently_of_gate`: boolean

Examples of acceptable exposure sources include a fixed sampling clock or a continuous independent reference stream partitioned into frozen windows.

An event log is **not** an acceptable exposure source for an event-triggered system because non-entered windows are missing from that log by construction.

## Required identifiers

Each exposure window must include:

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

These are measurements, not truth, and must be retained for all windows where technically available, including logical B and non-entered windows:

- `target_raw_score`
- `nuisance_raw_score_*` for each predeclared nuisance family or adapter
- `observability_raw_*`
- `coupled_response_raw_*` if applicable
- `primary_stream_available`
- `pregate_evidence_version`

If a physically non-entered window has no full-resolution primary record, preserve whatever pre-gate evidence actually drove the gate. Do not fabricate unavailable evidence.

If the registered-deviation gate uses additional raw quantities, every gate input must be retained or reproducibly derivable from immutable raw data.

## Chapter 2 registered-deviation gate

Required fields:

- `registered_deviation`: boolean; `False` means logical registered baseline at the gate layer
- `gate_type`: scalar / composite
- `gate_version`
- `gate_configuration_id`
- `gate_threshold` if and only if a real scalar threshold exists
- `gate_inputs_complete`: boolean

Optional but recommended for composite gates:

- `gate_component_result_*`
- `gate_margin` if the gate has a meaningful signed distance to its decision boundary

Do not invent a scalar threshold for a composite gate.

**Logical baseline semantics:**

`registered_deviation=False` means only **no registered deviation under the frozen gate rule**. It is not biological no-event or absence.

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

Interpretation:

- `registered_deviation=False, record_entry_present=True`: logical B exists and is physically represented in the stored record.
- `registered_deviation=False, record_entry_present=False`: exposure lies in the REC record-entry shadow set.
- `registered_deviation=True, record_entry_present=False`: a registered deviation failed later archival/retention and must be treated as a distinct pipeline failure, not baseline.

Do not assume `record_entry_present == registered_deviation` unless a versioned trigger-only policy actually defines that equality.

## Frozen calibrated support fields

Produced only after development calibration is frozen:

- `target_supported`
- `nuisance_supported`
- `observable_supported`
- `coupled_response_supported`
- `attribution_supported`
- `calibration_manifest_id`

The exact calibration rule for each field is versioned separately.

Calibrated T/N/U adjudication is applied only after the registered-deviation gate. Positive support with `registered_deviation=False` is an internal contradiction unless the project has explicitly defined and versioned a different pipeline.

## TNOA record

Where a logical observation record is represented:

- `decision`: B / T / N / U
- `reason`: reusable API reason or frozen project-specific reason
- `decision_rule_version`

Do not infer biological absence from `B`, `N`, `U`, no record entry, or low target score.

A physically non-entered exposure may have no TNOA `decision` because TNOA begins after record representation. REC still retains the exposure row through the independent master grid.

## Binary comparator

Where Chapter 1 is evaluated:

- `binary_target`
- `binary_mapping_version`

The binary mapping must be a frozen deterministic coarsening of the process-resolved record. It cannot be retuned on held-out truth.

## Independent reference truth

Reference annotators must not see model scores, gate outputs, entry status or TNOA decisions during primary truth annotation whenever practical.

### Biological event

- `target_truth`: positive / negative / unresolved
- `target_truth_source`
- `target_event_definition_version`
- `target_count_or_event_count` if relevant

Chapter-2 derived fields:

- `threshold_absorbed_event`: derive only as `target_truth=positive AND registered_deviation=False`
- `shadow_event`: derive only as `target_truth=positive AND record_entry_present=False`

Never manually label these fields; derive them from separately recorded truth and pipeline state.

### Nuisance

For each predeclared family:

- `nuisance_truth_<family>`: present / absent / unresolved
- `nuisance_effect_<family>`: masks_target / mimics_target / attribution_conflict / acquisition_fault / none / unresolved

Nuisance is multilabel.

### Observability

- `observability_truth`: observable / compromised / unobservable / unresolved
- `observability_reason`: occlusion / blur / exposure / framing / temporal_gap / hardware / masking / other / none

Recommended Chapter-2 measurements when independently defensible:

- `occlusion_grade`
- `target_scale_or_distance_proxy`
- `illumination_grade`
- `masking_grade`

These fields must not be reverse-engineered from whether the gate fired or an entry exists.

### Coupled response and attribution

If used:

- `coupled_response_truth`: present / absent / unresolved
- `attribution_truth`: supported / unsupported / unresolved
- `attribution_reference_channel`

## Chapter-2 truth-sampling provenance

Because logical B and shadow windows may be extremely common, REC may use prespecified stratified truth annotation instead of exhaustive review.

For every exposure row store:

- `truth_sampled`: boolean
- `truth_sampling_design_version`
- `truth_sampling_stratum`
- `truth_inclusion_probability`
- `truth_sampling_weight`

Sampling strata must be defined before confirmatory truth is opened. Suspicious-looking B/shadow windows cannot be preferentially added without inclusion-probability accounting or explicit exploratory status.

At minimum, the frozen sampling design should allow reconstruction across:

- `registered_deviation` state;
- `record_entry_present` state;
- independent ecological unit;
- frozen Chapter-2 measurement strata.

## Annotation provenance

- `annotator_id_primary`
- `annotator_id_secondary` where double-coded
- `adjudicated`
- `adjudication_status`
- `annotation_duration_seconds`
- `annotation_version`
- `annotator_blinded_to_gate`: boolean
- `annotator_blinded_to_entry`: boolean
- `annotator_blinded_to_scores`: boolean

Protected double-annotation subsets must be selected before adjudication.

## Ecological-unit table

A separate table aggregates exposure windows to the frozen ecological unit, preferred `site_id × recording_day` for System A unless pilot data justify another grouping before confirmatory freeze.

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

Required Chapter-1 columns:

- `binary_target_prevalence_or_model_estimate`
- `process_resolved_target_prevalence_or_model_estimate`
- `verified_nuisance_fraction`
- `compromised_observability_fraction`

Required REC/Chapter-2 columns where estimable:

- `registered_baseline_windows`
- `truth_sampled_registered_baseline_windows`
- `reference_positive_registered_baseline_windows`
- `baseline_contamination_estimate`
- `reference_positive_windows`
- `threshold_absorbed_positive_windows`
- `event_absorption_estimate`
- `nonentered_exposure_windows`
- `truth_sampled_nonentered_windows`
- `reference_positive_nonentered_windows`
- `shadow_contamination_estimate`
- `event_nonentry_estimate`
- `gate_version`
- `entry_policy_version`
- frozen Chapter-2 stratum summaries

Population estimates based on sampled B/shadow windows must use the frozen sampling weights/design.

## REC derived quantities

Do not store these as primary hand-entered truth fields; compute them reproducibly.

### Logical baseline contamination

`q_B = P(target_truth=positive | registered_deviation=False, reference truth resolved)`.

### Event absorption

`a = P(registered_deviation=False | target_truth=positive, reference truth resolved)`.

### Shadow contamination

`q_shadow = P(target_truth=positive | record_entry_present=False, reference truth resolved)`.

### Event non-entry

`a_K = P(record_entry_present=False | target_truth=positive, reference truth resolved)`.

### Ecological-unit absorption burden

`A_g = P(registered_deviation=False | target_truth=positive, ecological_unit=g)`.

Keep `q_B`, `a`, `q_shadow`, and `a_K` separate; they condition on different denominators.

## Fail-closed validity checks

A confirmatory row is invalid rather than silently repaired if:

- the master exposure grid identifier/source/version is missing;
- exposure is not defined independently of the tested gate;
- a held-out group also appears in development;
- positive calibrated support appears with an internally contradictory gate/decision input;
- reference truth is unresolved but encoded as negative;
- exposure is zero or missing;
- gate version/configuration is missing;
- entry policy version/type is missing;
- a scalar `gate_threshold` is populated for a composite gate without a documented mapping;
- required gate inputs are missing and the gate result cannot be reproduced;
- `registered_deviation=True` while primary stream or gate inputs are unavailable;
- `record_entry_present=True` while the entry policy inputs needed to reproduce that entry are declared incomplete;
- `threshold_absorbed_event` disagrees with the derivation from `target_truth` and `registered_deviation`;
- `shadow_event` disagrees with the derivation from `target_truth` and `record_entry_present`;
- a truth-sampled window lacks sampling provenance when a non-exhaustive sampling design is used;
- a truth-unsampled row carries resolved truth;
- required reference channel is missing for a truth claim that cannot be established from the primary stream.

Invalid rows and reasons are counted and reported; they are not silently dropped.

## Pilot-only fields

The pilot may additionally record:

- annotation difficulty score;
- candidate nuisance-family notes;
- candidate window-boundary notes;
- candidate exposure-grid alternatives;
- candidate Chapter-2 condition-stratum notes;
- candidate gate-component diagnostics;
- candidate entry-policy diagnostics;
- hardware failure diagnostics;
- proposed ecological grouping alternatives.

These exploratory fields may inform the frozen confirmatory schema but cannot be introduced after confirmatory labels are opened.
