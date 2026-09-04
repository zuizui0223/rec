# Paper-facing method contract — auditing record-entry selection

Status: **compact reusable method specification for the H1–H5 manuscript.**

This document is the manuscript-facing reduction of the fuller REC schemas. It is designed to answer a reviewer’s practical question:

> What exactly must another ecological monitoring study preserve in order to reproduce the audit?

## 1. Minimum data objects

An auditable study requires **three linked objects**.

### Object A — exposure/reference ledger

One row per observation opportunity, created independently of the tested event gate.

Minimum required fields:

| Field | Purpose |
| --- | --- |
| `exposure_id` | stable join key that exists even if no event record is produced |
| `system_id` | observation system or deployment |
| `context_id` | hardware/position/site/block context used for calibration/transport tests |
| `exposure_time` or interval | defines the denominator before gate output |
| `primary_available` | separates acquisition failure from later gate rejection |
| `reference_sampled` | whether independent truth was attempted for this exposure |
| `reference_event_state` | event / no-event / unresolved when reference sampled |
| `reference_inclusion_probability` | required when truth auditing is subsampled rather than complete |

Acceptable exposure sources include a fixed clock, continuous primary/reference stream, independent observer schedule, or another predeclared denominator. The tested event detector itself cannot define this ledger.

### Object B — pre-entry process table

One row per exposure_id for which the tested entry process is evaluable.

Minimum required fields:

| Field | Purpose |
| --- | --- |
| `exposure_id` | join to Object A |
| `pre_entry_evidence` or evidence provenance | score/features available before record creation |
| `gate_version` | exact rule applied to the evidence |
| `gate_result` | pass / reject / unresolved-not-evaluable |
| `record_entry` | whether a usable event record was actually created |
| `entry_policy_version` | distinguishes gate passage from later archive/retention policy |
| `entry_reason` | entered / gate-rejected / storage/archive exclusion / unresolved |

For systems such as physical camera traps where separate raw score evidence does not exist, the observed trigger/registration stages themselves form the pre-entry process table.

### Object C — downstream ecological table

The conventional event table or semantic/classification output used for ecological inference.

Minimum required fields:

| Field | Purpose |
| --- | --- |
| `record_id` | conventional entered-row identifier |
| `exposure_id` | back-link to the exposure ledger |
| downstream semantic/classification state | what later inference sees |
| frozen ecological endpoint/estimand contribution | quantity ultimately summarized or modelled |

The key methodological requirement is the `exposure_id` bridge: a scientific row must be traceable to the exposure opportunity that could also have produced no row.

## 2. Four audit outputs

### Audit 1 — existence / enumerability

Question:

> Are independently verified events present among exposures that did not enter the final record?

Report event-conditioned non-entry or, when a full exposure denominator exists, the composition of the non-entered set.

Do not estimate the biology of non-entered rows from an event table that never enumerated them.

### Audit 2 — estimand distortion

Freeze an ecological estimand `theta` before correction.

Compute:

- `theta_reference` from the external exposure/reference world;
- `theta_record` from the rows available to the conventional workflow;
- `distortion = theta_record - theta_reference` or another frozen distance metric.

Where observation contexts differ in composition, standardize reference and recorded worlds to the same context distribution before claiming within-context selective entry.

### Audit 3 — downstream irreversibility

Construct the best admissible downstream semantic result **without adding rows that failed entry**.

For a binary truth setting this can be an oracle that removes all false entered rows while retaining every true entered row.

Compare:

`theta_reference -> theta_raw_record -> theta_oracle_downstream`.

If the oracle remains far from reference, the discrepancy cannot be solved solely by improving downstream classification of existing rows.

### Audit 4 — correction and transport

Estimate an entry model using only designated calibration contexts. Apply a frozen correction to a target context not used for estimating its entry propensity.

Always compare:

1. raw recorded estimate;
2. entry-aware corrected estimate;
3. a frozen falsification comparator where feasible, such as a direction-swapped propensity model;
4. independent reference truth.

Report both positive and adverse target contexts. The calibration context and tested transport domain are part of the result.

## 3. Required separation of stages

Do not collapse the following into one generic nondetection flag when the data can distinguish them:

`exposure unavailable -> gate not evaluable -> gate rejected -> archive/record not retained -> downstream semantic error`.

A later stage cannot be assigned a negative outcome when the earlier information needed to evaluate it does not exist.

## 4. Unresolved states

Reference, trigger, registration or archive states may be unresolved.

Rules:

- unresolved is never silently recoded as no-event or failure;
- report resolved-only estimates plus partial-identification or sensitivity bounds when unresolved mass can affect the result;
- if unresolved mass is large enough to reverse the scientific conclusion, the conclusion remains unresolved.

## 5. Calibration and transport metadata

Any entry model used for correction should carry:

- training/calibration system IDs;
- hardware model/settings;
- position/deployment context;
- temporal/environmental scope when available;
- entry-rule version;
- biological strata included in calibration;
- held-out transport domains actually tested;
- adverse domains where correction worsened error.

This metadata is scientifically analogous to the applicability domain of a predictive model.

## 6. Claim ladder by available data

| Available data | Defensible claim |
| --- | --- |
| final event table only | downstream record description; no empirical claim about biological content of missing rows |
| gate-independent exposure ledger | non-entry is enumerable; biological composition still unknown without truth |
| exposure ledger + independent reference sample | shadow/event absorption estimable over the audited universe |
| above + context metadata | structured entry and within-context estimand distortion testable |
| above + downstream semantic truth | upstream vs downstream discrepancy can be separated where identifiable |
| above + frozen out-of-context calibration test | correction transport can be evaluated |

## 7. Minimal algorithm

1. **Define the denominator before event detection.**
2. **Join external truth to exposure IDs without conditioning sampling on event entry.**
3. **Record each evaluable gate/entry decision and its version.**
4. **Freeze an ecological estimand and context-standardization rule.**
5. **Compare reference and event-table estimands.**
6. **If semantic labels are available, run an oracle/best-downstream irreversibility audit.**
7. **Fit an entry model only in designated calibration contexts.**
8. **Apply the frozen correction to held-out contexts and retain null/adverse outcomes.**
9. **Publish the calibration and transport domain with the corrected estimate.**

## 8. Relationship to existing methods

This contract complements rather than replaces occupancy, detection, classification-error or preferential-sampling models.

Those models can be used downstream once the survey/record data structure is defined. The present contract asks what provenance must be preserved **before and during record creation** so that the observation process represented in those later models can be audited against an external denominator and its ecological consequence measured directly.

## 9. Current empirical instantiations

- **Findlay fox/badger:** CCTV pass = external reference; trigger/final capture = entry stages; species composition = ecological estimand; CT position = context/transport domain.
- **Findlay otter:** CCTV pass-camera observations = reference; wet/dry-specific trigger = entry process; wet composition = estimand; camera setting + CT position = calibration/transport context.
- **BirdVox:** continuous one-second audio grid = exposure denominator; expert annotation = event truth within recorded audio; frozen digital gate = record-entry rule; late-minus-early event-window prevalence = estimand; oracle true-entry-only record = downstream irreversibility test.

The same contract is intended for prospective PolliPi/System A with independently recorded field truth and predesignated development/held-out groups.
