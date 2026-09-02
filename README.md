# TNOA Paper 2 — field ecological consequence program

## Status

Planning track only. This repository is deliberately separate from the Paper-1 manuscript/provenance repository (`zuizui0223/tnoa`).

**Paper 1 remains frozen as the closed-world MEE methods paper.** Paper 2 may reuse Paper-1 definitions and software, but it must not retroactively promote new field evidence into Paper 1 unless the Paper-1 scope is explicitly reopened in a separate decision.

## One-sentence Paper-2 question

> Does early coarsening of automated ecological observations change real downstream ecological conclusions when evaluated against independent field truth?

This is intentionally stronger than the Paper-1 question. Paper 1 establishes the closed-world information cost of garbling B/T/N/U to target/not-target and the non-portability of inherited raw thresholds. Paper 2 asks whether those observation-interface choices matter in real ecological inference.

## Target contribution

Paper 2 should not be sold as “field validation of TNOA accuracy.” Its target contribution is:

> **Observation coarsening is a measurement-design choice that can alter ecological estimands, site rankings or ecological effect estimates; preserving independently calibrated process-resolved observation states reduces that distortion under specified conditions.**

A publishable null is allowed. If binary and process-resolved records give indistinguishable field conclusions, that result must remain reportable.

## Required evidence stack

### System A — prospective field interaction camera

Use a real sensor deployment with a primary stream under test and an **independent reference channel** that is never supplied to the tested observer.

Required truth layers:

1. biological target-event truth;
2. exogenous nuisance truth;
3. primary-stream observability truth;
4. target-coupled-response/attribution truth where a C channel is used.

The deployment begins in shadow mode. Adaptive TNOA actions remain disabled until the observation semantics are frozen and held-out evaluation is complete.

### System B — independent cross-system replication

Preferred public candidate: **Snapshot Serengeti** because it provides raw camera-trap imagery/classifications and an expert gold-standard subset of 4,149 capture events, including expert `impossible` cases. It can therefore support an independently truth-labelled replication without reusing System-A biology.

Candidate sources:

- Snapshot Serengeti data descriptor / images: https://www.nature.com/articles/sdata201526
- Dryad dataset: https://doi.org/10.5061/dryad.5pt92

System B is a replication candidate, not yet a frozen design. Before confirmatory use we must establish that each proposed T/N/O field has defensible observation semantics and is not derived circularly from the gold-standard outcome.

Fallback: Caltech Camera Traps / LILA, which provides 243,100 images, 140 camera locations, empty/species labels and ~66,000 bounding boxes. Use only if its truth/observability structure supports a cleaner confirmatory design.

## Primary comparison

For the same held-out observation windows and the same downstream analysis, compare at minimum:

1. `target / not-target` binary record;
2. process-resolved `B/T/N/U` record.

Do **not** make finer U-reason categories the primary comparison. Paper-1 D5 showed that their synthetic identification gain was not semantic-specific.

## Primary ecological estimand

The default primary estimand is **target-event prevalence over fixed exposure windows within independent ecological units** (for example site × day or camera × sampling block), defined from the independent reference truth.

The confirmatory field analysis compares how well each observation record recovers this known held-out estimand.

Primary performance quantity:

- paired absolute error in unit-level target-event prevalence relative to reference truth.

Key secondary quantities:

- calibration/coverage of compatible intervals or model uncertainty where applicable;
- rank correlation of ecological units against reference-truth prevalence;
- frequency and magnitude of site-rank reversals;
- one prespecified ecological contrast/effect estimate, chosen before confirmatory labels are unblinded;
- review/annotation burden, reported separately from information gain rather than folded into an unvalidated utility score.

## Central hypotheses

### H1 — field consequence of coarsening

On held-out System-A ecological units, binary coarsening will have larger absolute error for the primary target-event-prevalence estimand than the process-resolved record.

**Falsifier:** the paired error difference is negligible or favours binary after the analysis plan is frozen.

### H2 — where coarsening matters

The error difference will be concentrated in ecological units with independently verified nuisance activity or compromised observability, not uniformly across all units.

**Falsifier:** the error difference is unrelated to independently labelled nuisance/observability strata.

### H3 — ecological-conclusion consequence

For one prespecified ecological contrast, process-resolved and binary records may yield materially different effect magnitude, rank ordering or qualitative conclusion when compared with the reference-truth analysis.

This is **not** preregistered as a guaranteed reversal. The confirmatory target is closeness to the reference-truth effect, not finding a dramatic sign flip.

### H4 — cross-system replication

The direction of the core coarsening effect (binary no better than process-resolved on the prespecified field estimand, with effect magnitude estimated rather than assumed) will be evaluated independently in System B.

A failed cross-system replication remains a result and constrains generality.

## What would justify a journal above MEE

A stronger-journal submission requires all of the following, not merely more simulation:

- independently established field truth;
- a frozen held-out comparison of binary versus process-resolved records;
- a real downstream ecological estimand, not only classifier accuracy;
- an explicit map of conditions where coarsening does and does not matter;
- at least one independent biological/sensor replication or a comparably strong external dataset;
- no semantic-specific U-reason claim unless separately validated;
- annotation/calibration cost reported rather than ignored.

Without this evidence stack, Paper 1 should be submitted to MEE rather than delayed.

## Execution order

1. **Pilot System A in shadow mode** to estimate event/nuisance rates and annotation burden; pilot data cannot be used as confirmatory held-out evidence.
2. Freeze the window definition, truth protocol, grouping unit and primary estimand.
3. Freeze calibration criteria on development groups.
4. Collect/score new held-out field groups and run the binary versus B/T/N/U comparison once.
5. In parallel, build the System-B public-data replication and freeze its analysis before evaluating its protected test portion.
6. Only after both systems are resolved decide the journal tier.

## Hard separation from Paper 1

Paper-2 work in this repository must not change Paper-1 numerical claims, frozen synthetic outputs, D1-D5 status or current MEE package in `zuizui0223/tnoa`. Bug fixes to reusable software remain allowed if separately tested and do not change frozen Paper-1 evidence.
