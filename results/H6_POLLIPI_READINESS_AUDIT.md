# PolliPi same-system REC -> TNOA H6 readiness audit

Status: **data architecture structurally suitable; held-out H6 scoring correctly blocked**.

Pinned source: PolliPi `main` commit `88630139953ff28f0396a4a80f54cf4087fb0f25`.

The exact audited manifest is `calibration/tnoa_field_calibration_unfrozen_v1.json`, pinned by Git blob `12b12cf3aec2e58de9574b5c2fc5a9d5022d2508`.

Machine-readable REC audit: `results/h6_pollipi_readiness_audit_v1.json`.

## What is already ready

The current PolliPi contract already passes the structural prerequisites that should exist **before** field scoring:

- recognized field-calibration schema;
- independent reference truth explicitly required;
- grouped split declared as `recording_day x focal_scene_id x recording_block`;
- minimum double-annotation fraction is valid (`0.20`);
- TNOA source observation, source log and truth-annotation schemas are declared;
- nuisance families are predeclared;
- Phase-A probe-level T/N/O evidence is stored separately from operational capture timing;
- Phase-B independent truth annotation is defined and blinded to algorithm evidence.

This means PolliPi is not missing the conceptual or logging architecture needed for same-system H6.

## Why H6 is not yet licensed

The readiness audit correctly returns:

`ready_for_h6_heldout_scoring = false`.

Nine hard gates remain open:

1. field calibration status is not `frozen_field_calibration`;
2. `heldout_scoring_allowed` is still `false`;
3. target high threshold is not frozen;
4. target low threshold is not frozen;
5. target operational error criterion is not frozen;
6. nuisance field error criterion is not frozen;
7. observability support rule is not frozen;
8. observable thresholds are not frozen;
9. unobservable thresholds are not frozen.

The current manifest status is deliberately:

`unfrozen_predata`.

`live_tnoa_capture_actions_allowed` is also `false`, but live action is **not** required merely to perform an offline held-out H6 evaluation. The readiness checker keeps those permissions separate.

## Scientific interpretation

This is not a positive empirical H6 result. It is a positive **governance/readiness** result: the candidate same-system pipeline exists and the repository now has an executable rule that prevents premature held-out scoring.

The next empirical H6 result requires a new, frozen field calibration created from development/calibration truth only. After that freeze, untouched held-out recording groups can be scored once and compared at the four predeclared stages:

1. independent reference truth;
2. truth restricted to operational `K=1` rows — upstream REC selection;
3. frozen field TNOA representation on those same entered rows — post-entry semantic effect;
4. predeclared target/not-target coarsening — additional decision loss.

The ecological endpoint must remain identical across all four stages.

## Current H6 claim

- same-system candidate architecture: **available**;
- real-camera TNOA shadow logging: **available**;
- independent truth contract: **available**;
- field calibration: **not frozen**;
- held-out H6 scoring: **forbidden by executable gate**;
- empirical REC-H6 decomposition: **open**.

This boundary is intentional. H6 should be promoted only after untouched held-out field evidence exists, not by importing synthetic TNOA thresholds or reusing previously inspected outcomes.

Source CI run: `33830301060`; artifact `9921424764`; artifact digest `sha256:876f8c03e4eb244d4f557f9a98e73b251104d7a39082fdffb855cb3bf0ea373a`.
