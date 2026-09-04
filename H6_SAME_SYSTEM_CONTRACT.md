# REC-H6 same-system REC -> TNOA contract

Status: **architecture ready; field inference not yet licensed**.

REC-H6 asks for a single held-out observation system in which upstream record-entry selection and downstream TNOA semantics can be evaluated on the same independently referenced exposure universe.

The current best candidate is PolliPi Phase A/B, pinned here at PolliPi `main` commit:

`88630139953ff28f0396a4a80f54cf4087fb0f25`.

Relevant pinned PolliPi files at that commit:

- `packages/analysis/src/pollipi_analysis/tnoa_shadow.py` — Git blob `5c6d2c85c39c073383092eec68391d8204e6ca2f`;
- `docs/TNOA_SHADOW_PHASE_A.md` — Git blob `ee06e5f6b29b2e4cf86c6331cf87e8b88ea02cd1`;
- `docs/TNOA_FIELD_ANNOTATION_PHASE_B.md` — Git blob `b506b98c14f18da54c784c6b48ecf4ea771d03e8`;
- `calibration/tnoa_field_calibration_unfrozen_v1.json` — Git blob `12b12cf3aec2e58de9574b5c2fc5a9d5022d2508`.

## Why PolliPi is structurally suitable

PolliPi already separates the pieces H6 needs:

1. every low-resolution probe can be logged independently of a high-resolution saved record;
2. Phase-A `tnoa_observation_v1_<run_id>.csv` stores target, nuisance and observability evidence without changing capture timing;
3. the existing adaptive/capture log remains a separate operational entry process;
4. Phase B defines blinded independent biological-event, nuisance and observability truth;
5. join keys connect run/probe evidence to saved still/video records and independent annotation.

This permits a same-system chain of the form:

`Omega -> A/R/K [REC] -> process-preserving TNOA evidence/state -> binary/coarsened decision`.

## Frozen H6 stage comparison

A future held-out H6 analysis must evaluate the **same ecological endpoint** at four paired stages.

### Stage 0 — reference world

`theta_truth`

Compute the prespecified ecological endpoint from independently referenced, reference-resolved exposures over the frozen `Omega`.

### Stage 1 — entry-selected truth world

`theta_Ktruth`

Apply the same truth labels and same endpoint after restricting to operational `K=1` rows.

The difference between `theta_Ktruth` and `theta_truth` isolates upstream REC record-entry selection without semantic classification error.

### Stage 2 — frozen TNOA world

`theta_TNOA`

On the identical `K=1` rows, use only a **frozen field-calibrated** TNOA state/representation. No synthetic V14/V15 threshold may be substituted for field calibration.

The difference between Stage 2 and Stage 1 measures the consequence of downstream field semantic representation/classification on the already entered record.

### Stage 3 — coarsened decision world

`theta_binary`

Apply the predeclared target/not-target coarsening to the same entered TNOA rows and recompute the same endpoint.

This stage quantifies the additional decision-coarsening loss after both record entry and process-semantic observation.

## Reporting rule

Do **not** force these stage errors to add algebraically. Ecological endpoints can be nonlinear.

Report:

- all four stage estimates or identification sets;
- `theta_Ktruth - theta_truth` as the REC entry shift;
- `theta_TNOA - theta_Ktruth` as the post-entry semantic shift where a point estimand is licensed;
- `theta_binary - theta_TNOA` as the additional coarsening shift where defined;
- total `theta_binary - theta_truth`;
- the corresponding absolute errors relative to `theta_truth`.

If the TNOA representation yields an identification set rather than a point estimate, compare interval width/coverage rather than inventing a point value.

## Hard readiness gate

H6 held-out scoring is forbidden unless **all** are true:

1. PolliPi/field calibration manifest has `status = frozen_field_calibration`;
2. `heldout_scoring_allowed = true`;
3. independent reference truth is required and available;
4. target high/low field thresholds are frozen;
5. nuisance field error criterion is frozen;
6. observability support rules are frozen;
7. the held-out grouping unit is frozen and development/calibration groups do not overlap held-out groups;
8. REC `Omega`, A/R/K and record-entry policy are versioned for the same probes;
9. the TNOA log joins one-to-one or explicitly many-to-one to REC exposure rows without outcome-dependent row creation;
10. the ecological endpoint and target/not-target coarsening are frozen before held-out scoring.

## Current PolliPi status

At the pinned commit, the field calibration manifest is deliberately **not ready**:

- `status = unfrozen_predata`;
- target thresholds are `null`;
- nuisance familywise alpha is `null`;
- observability support rule is `null`;
- `heldout_scoring_allowed = false`;
- `live_tnoa_capture_actions_allowed = false`.

Therefore H6 has an implementation-ready data architecture but **no licensed empirical same-system decomposition yet**.

This is a positive readiness result, not a positive H6 biological/inferential result.

## Promotion rule

The next H6 promotion event is not another simulation. It is:

1. collect Phase-A PolliPi probe logs plus independent Phase-B truth;
2. calibrate only on development/calibration groups;
3. freeze a new field-calibration manifest;
4. verify the readiness checker passes;
5. score untouched held-out groups once;
6. run the four-stage decomposition above on the same joined evidence.

Until then REC-H6 remains **open but operationally specified**.
