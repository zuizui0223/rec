# Paper 2 field truth and observation-window schema

Status: design draft; freeze before confirmatory field collection.

## Principle

The primary sensor output, independent truth, and downstream ecological unit must be separately addressable. No field can be inferred from another field by default.

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

## Primary-stream raw evidence

These are measurements, not truth:

- `target_raw_score`
- `nuisance_raw_score_*` for each predeclared nuisance family or adapter
- `observability_raw_*`
- `coupled_response_raw_*` if applicable
- `primary_stream_available`

Raw values must be retained even after calibrated support flags are created.

## Frozen calibrated support fields

Produced only after development calibration is frozen:

- `target_supported`
- `nuisance_supported`
- `observable_supported`
- `coupled_response_supported`
- `attribution_supported`
- `calibration_manifest_id`

The exact calibration rule for each field is versioned separately.

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

Reference annotators must not see model scores or TNOA decisions.

### Biological event

- `target_truth`: positive / negative / unresolved
- `target_truth_source`
- `target_count_or_event_count` if relevant

### Nuisance

For each predeclared family:

- `nuisance_truth_<family>`: present / absent / unresolved
- `nuisance_effect_<family>`: masks_target / mimics_target / attribution_conflict / acquisition_fault / none / unresolved

Nuisance is multilabel.

### Observability

- `observability_truth`: observable / compromised / unobservable / unresolved
- `observability_reason`: occlusion / blur / exposure / framing / temporal_gap / hardware / masking / other / none

### Coupled response and attribution

If used:

- `coupled_response_truth`: present / absent / unresolved
- `attribution_truth`: supported / unsupported / unresolved
- `attribution_reference_channel`

## Annotation provenance

- `annotator_id_primary`
- `annotator_id_secondary` where double-coded
- `adjudicated`
- `adjudication_status`
- `annotation_duration_seconds`
- `annotation_version`

Protected double-annotation subsets must be selected before adjudication.

## Ecological-unit table

A separate table aggregates windows to the frozen ecological unit, preferred `site_id × recording_day` for System A unless pilot data justify another grouping before confirmatory freeze.

Required columns:

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

## Fail-closed validity checks

A confirmatory row is invalid rather than silently repaired if:

- a held-out group also appears in development;
- positive calibrated support appears with an internally contradictory decision input;
- reference truth is unresolved but encoded as negative;
- exposure is zero or missing;
- binary mapping version is missing;
- calibration manifest was created after held-out labels were accessed;
- required reference channel is missing for a truth claim that cannot be established from the primary stream.

Invalid rows and reasons are counted and reported; they are not silently dropped.

## Pilot-only fields

The pilot may additionally record:

- annotation difficulty score;
- candidate nuisance-family notes;
- candidate window-boundary notes;
- hardware failure diagnostics;
- proposed ecological grouping alternatives.

These exploratory fields may inform the frozen confirmatory schema but cannot be introduced after confirmatory labels are opened.
