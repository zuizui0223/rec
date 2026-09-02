# System A — Raspberry Pi interaction-camera REC shadow pilot

Status: **instrumentation design; pilot only; not confirmatory; no field result yet**.

## 1. Purpose

System A maps the existing flower-visit Raspberry Pi pipeline onto REC’s pre-entry observation stages.

The current detector already contains sequential selection:

1. low-frequency flower YOLO establishes/stabilizes a flower ROI;
2. ROI motion is evaluated only when a flower ROI exists;
3. insect classification is evaluated only while motion activates the classifier;
4. insect-like evidence is thresholded and temporally smoothed by votes;
5. confirmed evidence starts an event video;
6. video stops after the insect-like signal disappears or the maximum duration is reached.

This means “no event clip” can arise at several distinct stages. REC must retain those stages instead of collapsing all of them into baseline/no-event.

## 2. System-A shadow chain

Use the following stage variables on a fixed exposure grid `Ω`:

```text
Ω fixed exposure window
      |
      v
F  flower/ROI eligibility
      |
      v
M  motion gate
      |
      v
C  classifier evaluated
      |
      v
I  insect-like evidence
      |
      v
V  temporal vote confirmation
      |
      v
K  event clip / archive coverage
```

Formal meanings:

- `F=1`: a stable flower ROI exists for at least part of the exposure window;
- `M=1`: the frozen ROI-motion rule fires at least once while the gate is evaluable;
- `C=1`: the insect classifier is actually invoked at least once;
- `I=1`: an allowed insect class reaches the frozen insect-score criterion at least once;
- `V=1`: the frozen temporal vote criterion is reached;
- `K=1`: the exposure window overlaps a persisted event clip.

These are **pipeline stages**, not biological truth.

Do not assume that a failure at one stage means no insect visit occurred.

## 3. Why flower eligibility is not baseline

The current detector stops downstream processing when no stable flower ROI exists. Therefore:

`F=0`

means the motion/insect gate is not evaluable for that exposure. It must **not** be encoded as `R=0 baseline`.

For System A, the generic REC gate result is:

- `gate_result = deviation` when the frozen registered-deviation rule fires;
- `gate_result = baseline` only when the gate was evaluable and the rule did not fire;
- `gate_result = not_evaluable` when prerequisite measurement support was absent.

The first pilot mapping uses the ROI-motion gate as the provisional REC registered-deviation gate:

- gate evaluable iff `F=1` and required motion inputs exist;
- `deviation` iff motion threshold and component rule fire;
- `baseline` iff the motion gate is evaluable but does not fire;
- `not_evaluable` iff flower/ROI prerequisites are unavailable.

This mapping is **pilot-only**. Confirmatory REC must freeze the final gate semantics after pilot feasibility review.

## 4. Existing detector configuration to preserve as provenance

The currently inspected detector uses, among other settings:

- camera preview `640 × 480`;
- flower YOLO confidence threshold `0.65`;
- flower detection every `120` frames;
- `2` stable flower detections required;
- flower loss after `4` misses;
- ROI motion ratio threshold `0.008`;
- minimum motion component area `80`;
- classifier active window `2.5 s` after motion;
- insect score threshold `0.70` for allowed Diptera/Hymenoptera/Lepidoptera labels;
- classification every `10` frames while active;
- vote window `8`, with `3` hits required to start recording;
- stop after `2.0 s` without insect-like evidence;
- maximum event clip `60 s`.

These values describe one software version and are **not ecological constants**. Record the complete configuration hash/version rather than copying numerical thresholds between deployments.

## 5. Master exposure grid for the pilot

### 5.1 Provisional grid

Use a fixed-clock exposure grid independent of flower, motion, classifier and recording outcomes.

Pilot default:

`2-second non-overlapping windows`.

Rationale: the current state machine contains 2–2.5 s persistence/stop times, so 2 s is short enough to expose stage changes while remaining tractable for logging. This is a **pilot engineering choice**, not the confirmatory window definition.

### 5.2 Grid generation

Create every window from a monotonic/frozen clock even when:

- no flower is detected;
- no motion occurs;
- classifier is never invoked;
- no video is written.

Every expected exposure gets a ledger row.

## 6. Shadow ledger

The detector must write a lightweight fixed-window ledger separate from its event log.

For each exposure window record at minimum:

### Exposure identity

- `exposure_grid_id`
- `window_id`
- `window_start`
- `window_end`
- `exposure_seconds`
- sensor/site/day/block identifiers

### Flower eligibility F

- `flower_eligible_any`
- `flower_eligible_fraction_frames`
- `flower_conf_max`
- `flower_conf_last`
- `flower_acquired_count`
- `flower_lost_count`

### Motion M

- `motion_gate_evaluable_any`
- `motion_triggered_any`
- `motion_ratio_max`
- `motion_ratio_mean_when_evaluable`
- `motion_boxes_max`

### Classifier C / insect-like I

- `classifier_invoked_count`
- `classifier_active_any`
- `insect_score_max`
- `insect_label_at_max`
- `insect_like_any`

### Vote/record stages V/K

- `vote_hits_max`
- `vote_confirmed_any`
- `event_clip_started_any`
- `recording_active_any`
- `event_clip_overlap_seconds`
- `event_clip_id` where applicable

### Version provenance

- detector code/version SHA;
- flower model/version;
- insect model/version;
- gate configuration ID;
- entry-policy version;
- shadow-ledger schema version.

The ledger is the operational bridge from existing detector state to REC `Ω/S/R/K`.

## 7. Mapping to generic REC variables

### Exposure universe

`Ω` = all fixed-clock shadow-ledger windows.

### Pre-gate evidence S

System A retains a vector, not one scalar:

`S = {flower evidence, motion ratio/components, classifier score/label, vote state}`.

### Registered-deviation result R

Pilot registered-deviation gate = ROI motion gate.

- `R = deviation` when motion rule fires;
- `R = baseline` when flower/ROI gate is evaluable but motion rule does not fire;
- `R = not_evaluable` when flower/ROI prerequisites are unavailable.

### Entry state K

For the event-video policy:

`K=1` when the fixed exposure overlaps persisted event-video content.

`K=0` otherwise.

Because event clips persist after a trigger, `K` is not identical to `V` or `R` on every fixed exposure window.

## 8. Stage-specific shadow estimands

Independent reference truth permits a stage waterfall without treating any stage failure as absence.

For true events `E=1`, estimate:

### Flower/eligibility loss

`a_F = P(F=0 | E=1)`.

### Motion-gate loss conditional on eligibility

`a_M = P(M=0 | E=1, F=1, motion gate evaluable)`.

### Classifier invocation loss conditional on motion

`a_C = P(C=0 | E=1, F=1, M=1)`.

### Insect-evidence failure conditional on classifier invocation

`a_I = P(I=0 | E=1, C=1)`.

### Vote-confirmation failure conditional on insect-like evidence

`a_V = P(V=0 | E=1, I=1)`.

### Operational event-log non-entry

`a_K = P(K=0 | E=1)`.

Report these as conditional stage losses. Do not multiply them into an “overall sensitivity decomposition” unless the frozen analysis demonstrates that such multiplication is appropriate for the actual state machine.

Sequential detection decomposition itself is not claimed as novel; its role is to expose where this interaction-camera pipeline loses ecological events and whether those losses alter downstream conclusions.

## 9. Truth architecture

### 9.1 Pilot feasibility truth

A pilot may save stratified same-camera shadow samples to verify instrumentation and estimate annotation burden.

This **does not provide independent confirmatory truth** because it derives from the same camera stream under study.

### 9.2 Confirmatory truth

Confirmatory `E` requires an independent reference channel capable of observing visits whether or not System A reaches `F/M/C/V/K`.

Preferred architecture:

- primary Pi interaction camera = tested stream;
- second synchronized wider/continuous reference camera = independent truth stream;
- reference annotations blinded to System-A score/gate/entry outputs.

The reference camera must cover the focal flower/interaction zone throughout the master exposure grid.

## 10. Shadow sampling policy

Full continuous high-resolution storage is not required for the primary stream if the independent reference channel provides truth.

For primary-stream audit/debug evidence, use stratified sampling from the fixed ledger.

Pilot example strata:

1. `F=0` not-evaluable windows;
2. `F=1, M=0` logical B;
3. `M=1, V=0, K=0` registered deviation but no event clip;
4. `V=1/K=1` event-positive archive;
5. hardware/reference failure.

Store inclusion probabilities and sampling weights.

Do not preferentially save “suspicious” non-events without recording their selection probability.

## 11. First ecological contrast

The pilot must identify exactly one feasible confirmatory ecological contrast without choosing it for maximum REC effect.

Good candidates are variables that can plausibly affect both ecology and measurement, because REC can then test whether the observed gradient decomposes into those paths. Examples include:

- morning versus later daytime;
- shaded versus exposed flower position;
- another independently measured habitat/light stratum.

Do not freeze the final contrast until pilot counts and measurability are known. Do not inspect confirmatory effects before freezing it.

## 12. Phase-0 outputs

System-A Phase 0 should produce:

1. master-grid completeness rate;
2. distribution of F/M/C/I/V/K states over all pilot exposure windows;
3. truth-sampling and annotation burden by stage;
4. preliminary `a_F`, `a_M`, `a_C`, `a_I`, `a_V`, `a_K` from pilot truth only;
5. reference synchronization/unresolved rate;
6. proposed frozen confirmatory window duration;
7. proposed frozen truth-sampling strata and inclusion probabilities;
8. proposed frozen ecological unit;
9. proposed one ecological contrast;
10. sample-size/precision simulation inputs.

No pilot effect becomes a confirmatory Paper-2 result.

## 13. Implementation rule

Do not replace the current event logger. Add the shadow ledger **in parallel**.

The event-video detector remains operationally unchanged during the pilot so that instrumentation does not silently change the selection mechanism being measured.

A later branch may evaluate redesigned gates/entry policies, but only after the baseline selection process has been frozen and measured.
