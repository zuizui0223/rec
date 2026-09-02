# Paper 2 field truth and observation-window schema

Status: design draft; freeze before confirmatory field collection.

## Principle

The primary sensor output, independent truth, the registered-deviation gate, and the downstream ecological unit must be separately addressable. No field can be inferred from another field by default.

## Required identifiers

Each observation window must include:

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

These are measurements, not truth, and must be retained for **all** windows including registered B:

- `target_raw_score`
- `nuisance_raw_score_*` for each predeclared nuisance family or adapter
- `observability_raw_*`
- `coupled_response_raw_*` if applicable
- `primary_stream_available`
- `pregate_evidence_version`

If the registered-deviation gate uses additional raw quantities, every gate input must be retained or reproducibly derivable from immutable raw data.

## Chapter 2 registered-deviation gate

Required fields:

- `registered_deviation`: boolean; `False` means registered baseline B at the gate layer
- `gate_type`: scalar / composite
- `gate_version`
- `gate_configuration_id`
- `gate_threshold` if and only if a real scalar threshold exists
- `gate_inputs_complete`: boolean

Optional but recommended for composite gates:

- `gate_component_result_*`
- `gate_margin` if the gate has a meaningful signed distance to its decision boundary

Do not invent a scalar threshold for a composite gate.

**Registered baseline semantics:**

`registered_deviation=False` means only **no registered deviation under the frozen gate rule**. It is not biological no-event or absence.

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

- `decision`: B / T / N / U
- `reason`: reusable API reason or frozen project-specific reason
- `decision_rule_version`

Do not infer biological absence from `B`, `N`, `U`, or low target score.

## Binary comparator

- `binary_target`
- `binary_mapping_version`

The binary mapping must be a frozen deterministic coarsening of the process-resolved record. It cannot be retuned on held-out truth.

## Independent reference truth

Reference annotators must not see model scores, gate outputs or TNOA decisions during primary truth annotation whenever practical.

### Biological event

- `target_truth`: positive / negative / unresolved
- `target_truth_source`
- `target_event_definition_version`
- `target_count_or_event_count` if relevant

Chapter-2 derived field:

- `threshold_absorbed_event`: derived only as `target_truth=positive AND registered_deviation=False`

Never manually label `threshold_absorbed_event`; derive it from separately recorded truth and gate status.

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

These fields must not be reverse-engineered from whether the gate fired.

### Coupled response and attribution

If used:

- `coupled_response_truth`: present / absent / unresolved
- `attribution_truth`: supported / unsupported / unresolved
- `attribution_reference_channel`

## Chapter-2 truth-sampling provenance

Because registered B may be extremely common, Chapter 2 may use prespecified stratified truth annotation instead of exhaustive review.

For every truth-annotated window store:

- `truth_sampled`: boolean
- `truth_sampling_design_version`
- `truth_sampling_stratum`
- `truth_inclusion_probability`
- `truth_sampling_weight`

Sampling strata must be defined before confirmatory truth is opened. Suspicious-looking B windows cannot be preferentially added without either inclusion-probability accounting or explicit exploratory status.

## Annotation provenance

- `annotator_id_primary`
- `annotator_id_secondary` where double-coded
- `adjudicated`
- `adjudication_status`
- `annotation_duration_seconds`
- `annotation_version`
- `annotator_blinded_to_gate`: boolean
- `annotator_blinded_to_scores`: boolean

Protected double-annotation subsets must be selected before adjudication.

## Ecological-unit table

A separate table aggregates windows to the frozen ecological unit, preferred `site_id × recording_day` for System A unless pilot data justify another grouping before confirmatory freeze.

Required Chapter-1 columns:

- `ecological_unit_id`
- `site_id`
- `recording_day`
- `resolved_reference_windows`
- `unresolved_reference_windows`
- `reference_target_positive_windows`
- `reference_target_prevalence`
- `binary_target_prevalence_or_model_estimate`
- `process_resolved_target_prevalence_or_model_estimate`
- `verified_nuisance_fraction`
- `compromised_observability_fraction`
- prespecified ecological covariate(s)

Required Chapter-2 columns where estimable:

- `registered_baseline_windows`
- `truth_sampled_registered_baseline_windows`
- `reference_positive_registered_baseline_windows`
- `baseline_contamination_estimate`
- `reference_positive_windows`
- `threshold_absorbed_positive_windows`
- `event_absorption_estimate`
- `gate_version`
- frozen Chapter-2 stratum summaries

Population estimates based on sampled B windows must use the frozen sampling weights/design.

## Chapter-2 derived quantities

Do not store these as primary hand-entered truth fields; compute them reproducibly.

### Baseline contamination

`q_B = P(target_truth=positive | registered_deviation=False, reference truth resolved)`.

### Event absorption

`a = P(registered_deviation=False | target_truth=positive, reference truth resolved)`.

### Ecological-unit absorption burden

`A_g = P(registered_deviation=False | target_truth=positive, ecological_unit=g)`.

Keep `q_B` and `a` separate; they condition on different denominators.

## Fail-closed validity checks

A confirmatory row is invalid rather than silently repaired if:

- a held-out group also appears in development;
- positive calibrated support appears with an internally contradictory gate/decision input;
- reference truth is unresolved but encoded as negative;
- exposure is zero or missing;
- binary mapping version is missing;
- calibration manifest was created after held-out labels were accessed;
- gate version/configuration is missing;
- a scalar `gate_threshold` is populated for a gate whose rule is not scalar without a documented mapping;
- required gate inputs are missing and the gate result cannot be reproduced;
- `threshold_absorbed_event` disagrees with the derivation from `target_truth` and `registered_deviation`;
- a truth-sampled window lacks sampling provenance when a non-exhaustive sampling design is used;
- required reference channel is missing for a truth claim that cannot be established from the primary stream.

Invalid rows and reasons are counted and reported; they are not silently dropped.

## Pilot-only fields

The pilot may additionally record:

- annotation difficulty score;
- candidate nuisance-family notes;
- candidate window-boundary notes;
- candidate Chapter-2 condition-stratum notes;
- candidate gate-component diagnostics;
- hardware failure diagnostics;
- proposed ecological grouping alternatives.

These exploratory fields may inform the frozen confirmatory schema but cannot be introduced after confirmatory labels are opened.
