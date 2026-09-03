# White Sands 2023 × Nighthawk — realistic-detector REC audit

Status: **protected count-level external validation contract; outcomes unopened when this contract was written**.

## Why this system

The first BirdVox REC experiment deliberately used an annotation-naive band-energy rule to make score provenance unambiguous. That experiment established an auditable upstream-omission proof, but the protected BirdVox score had poor discrimination. The next question is therefore whether REC has explanatory reach when the recorded world is produced by a detector that is actually used in ecological field studies.

The White Sands system provides that test. Nighthawk was fine-tuned using 2021/2022 recordings from the study system, while the associated 2025 study reports an independent manual validation on **50 randomly selected 15-minute segments from new 2023 recordings**, with a reported manual-versus-Nighthawk count correlation of about `r=0.97`.

Public data source: Dryad DOI `10.5061/dryad.w6m905r26`, file `Nighthawk_Testing.xlsx`.

## Identification boundary

This validation table is **count-level truth**, not timestamped event-level truth.

It can test whether the scientific record preserves an ecological count endpoint at the 15-minute segment scale. It cannot identify which individual calls were missed or falsely entered. In particular, count agreement does not identify

`q_shadow = P(E=1 | K=0)`

because false entries and missed calls can cancel within a segment.

Therefore this module is an external **REC-H3 ecological-consequence / calibration audit**, not a REC-H1 shadow-prevalence analysis.

## Frozen unit and endpoint

- independent analysis row: one manually screened 15-minute segment;
- reference endpoint: `ManualCalls` (or an explicitly equivalent released column);
- recorded-world endpoint: `NighthawkCalls` (or an explicitly equivalent released column);
- all released validation rows are retained;
- no outlier removal or threshold tuning after outcomes are opened.

## Frozen primary diagnostics

The analysis reports, before any outcome-driven model choice:

1. number of validation segments;
2. total manual and Nighthawk counts and their ratio;
3. Pearson correlation;
4. Spearman rank correlation;
5. OLS slope and intercept for `NighthawkCalls ~ ManualCalls`;
6. mean signed error, MAE and RMSE;
7. manual-zero versus manual-positive segment summaries;
8. descriptive fixed quartiles of positive manual-call intensity.

The quartile summaries are descriptive only and do not replace the full-sample diagnostics.

## Fail-closed rules

The analyzer fails if:

- a manual-count or Nighthawk-count column cannot be identified from the released table;
- counts are missing, non-numeric, negative or non-finite;
- duplicate physical rows are silently removed;
- the file contains no validation rows.

The code must not infer event-level missed-call prevalence from count differences.

## Promotion logic

Three outcomes are all informative:

- **high global agreement but structured count distortion:** realistic-detector support for REC-H3 despite an apparently strong overall performance statistic;
- **large global distortion:** stronger REC-H3 support, subject to the published detector/validation boundary;
- **agreement and ecological ordering preserved:** an important boundary showing that REC failure is not inevitable for a realistic, well-matched recording rule.

Any light-versus-dark error comparison is added only if site/light status can be joined deterministically from released identifiers without changing strata after viewing the validation outcomes.

## Relationship to TNOA

This experiment asks whether a realistic record-entry system preserves a downstream ecological count before TNOA semantics are considered. It does not test TNOA classification vocabulary itself. If count structure is already distorted at record entry, later semantic refinement cannot reconstruct the missing count information without additional measurements or assumptions.
