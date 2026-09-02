# REC — the shadow side of TNOA

## Status

Planning/development track for Paper 2. This repository is deliberately separate from the frozen Paper-1 manuscript/provenance repository (`zuizui0223/tnoa`).

**Working expansion: REC = Record-Entry Censoring.** The name refers to the upstream process by which ecological exposures or events fail to enter the scientific record before TNOA-style semantic adjudication begins.

**Paper 1 remains frozen as the closed-world MEE methods paper.** REC may reuse Paper-1 definitions and software, but it must not retroactively promote new field evidence into Paper 1 unless that scope is explicitly reopened in a separate decision.

## TNOA and REC as paired worlds

The project now has a deliberate front-side / shadow-side architecture.

- **TNOA:** what happens to information **after an observation has entered the record** — target, nuisance, observability, attribution and later coarsening.
- **REC:** what happens **before or at record entry** — which exposure windows/events never become entries, why, and whether this selection changes ecological inference.

The foundational REC rule is:

> **No record is not yet a biological state. Define the exposure universe before defining non-detection.**

A missing event-log row cannot be called baseline until an independent exposure denominator exists. REC therefore requires a **master exposure universe/grid** that is defined independently of the tested gate.

Full conceptual definition: `REC_FRAMEWORK.md`.

Prior-art/novelty guardrails: `PRIOR_ART_BOUNDARY.md`.

## Paper-2 architecture

Paper 2 treats information loss as a staged observation pipeline.

```text
latent biological process
        |
        v
master exposure universe Ω               <- REC denominator
        |
        v
primary-stream evidence S
        |
        v
registered-deviation gate R              <- Chapter 2 / REC gate censoring
   |                 |
   v                 v
logical B          deviation
   |                 |
   |                 v
   |              T / N / U               <- Chapter 1 / TNOA-style semantics
   |                 |
   |                 v
   |          target / not-target          <- later coarsening
   |
   +---- possible archive non-entry K=0    <- REC shadow set
```

### Chapter 1 — decision coarsening

Chapter 1 asks what is lost when an already represented process-resolved record `B/T/N/U` is coarsened to `target/not-target`.

Primary document: `PREREGISTRATION_DRAFT.md`.

### Chapter 2 — threshold / record-entry censoring

Chapter 2 asks what is lost **before B/T/N/U exists**, when the registered-deviation gate maps both true no-event windows and real subthreshold events into logical registered baseline `B`, and when an operational acquisition policy may omit some of those windows from the event log entirely.

Its defining statements are:

> **B is no registered deviation under the current measurement rule; B is not independently certified biological inactivity or absence.**

and

> **A missing event-log entry is not a B observation unless the exposure window exists on an independently defined master grid.**

Primary document: `CHAPTER2_THRESHOLD_CENSORING.md`.

The two chapters are complementary but empirically distinct. Chapter 1 cannot be used as evidence that Chapter-2 censoring exists; Chapter 2 requires independent reference truth upstream of the tested gate.

## One-sentence Paper-2 question

> Does automated ecological observation lose inferentially important events before record entry and then lose additional process information through later coarsening, strongly enough to change real downstream ecological conclusions against independent field truth?

This is intentionally stronger than the Paper-1 question. Paper 1 establishes the closed-world information cost of garbling B/T/N/U to target/not-target and the non-portability of inherited raw thresholds. Paper 2 asks whether those observation-interface choices matter in real ecological inference.

## Target contribution

Paper 2 should not be sold as “field validation of TNOA accuracy” or as the discovery of imperfect detection. Occupancy, camera-trap false-negative and double-observer literatures already establish those problems.

The target contribution is narrower:

> **Observation entry and compression are measurement-design choices. REC makes the exposure universe, pre-gate evidence and entry policy auditable; TNOA preserves semantics after entry. Together they allow the ecological consequences of upstream selection and downstream coarsening to be separated against independent truth.**

A publishable null is allowed at either chapter. If record-entry contamination is negligible, or binary and process-resolved records give indistinguishable field conclusions, those results must remain reportable.

## Required evidence stack

### System A — prospective field interaction camera

Use a real sensor deployment with a primary stream under test and an **independent reference channel** that is never supplied to the tested observer.

Required truth layers:

1. biological target-event truth;
2. exogenous nuisance truth;
3. primary-stream observability truth;
4. target-coupled-response/attribution truth where a C channel is used.

For REC/Chapter 2, additionally retain or reconstruct:

- the master exposure grid independent of the tested gate;
- pre-gate evidence for every exposure window or a declared recoverable sampling design;
- registered-deviation status and gate version;
- archive/event-log entry status and entry-policy version;
- truth-sampling inclusion probability for any subsampled B/shadow windows.

The deployment begins in shadow mode. Adaptive TNOA/REC actions remain disabled until observation and entry semantics are frozen and held-out evaluation is complete.

### System B — independent cross-system replication

Preferred public candidate: **Snapshot Serengeti** because it provides raw camera-trap imagery/classifications and an expert gold-standard subset of 4,149 capture events, including expert `impossible` cases. It can therefore support an independently truth-labelled replication without reusing System-A biology.

Candidate sources:

- Snapshot Serengeti data descriptor / images: https://www.nature.com/articles/sdata201526
- Dryad dataset: https://doi.org/10.5061/dryad.5pt92

System B is a replication candidate, not yet a frozen design. Before confirmatory use we must establish whether a defensible **exposure universe** exists. An event-only dataset cannot by itself estimate the REC shadow set because non-entered windows have no denominator.

Fallback: Caltech Camera Traps / LILA. Use only if its truth, exposure and observability structure supports a cleaner confirmatory design.

## Chapter-1 primary comparison

For the same held-out observation windows and the same downstream analysis, compare at minimum:

1. `target / not-target` binary record;
2. process-resolved `B / T / N / U` record.

Do **not** make finer U-reason categories the primary comparison. Paper-1 D5 showed that their synthetic identification gain was not semantic-specific.

## Chapter-2 primary comparison

For the same master exposure windows with independent reference truth, quantify at minimum:

1. the fraction of logical registered-B windows containing a verified biological event: `q_B = P(E=1 | R=0)`;
2. the fraction of verified biological events absorbed into B: `P(R=0 | E=1)`;
3. when physical non-entry exists, the event fraction in the archive shadow set: `q_shadow = P(E=1 | K=0)`;
4. how gate/entry loss changes across frozen measurement/ecological strata;
5. whether differential record entry changes one prespecified ecological estimand or contrast.

Do not call B or non-entry biological absence.

## Shared primary ecological estimand

The default primary estimand is **target-event prevalence over fixed exposure windows within independent ecological units** (for example site × day or camera × sampling block), defined from independent reference truth.

Chapter 1 asks which retained decision vocabulary best preserves this quantity. Chapter 2 asks how much of the true event process disappeared before that vocabulary was even formed.

Key quantities include:

- paired absolute error in unit-level target-event prevalence relative to reference truth;
- Chapter-2 baseline contamination `P(event truth | registered B)`;
- Chapter-2 event absorption `P(registered B | event truth)`;
- REC shadow contamination `P(event truth | no event-log entry)` where identifiable;
- rank correlation of ecological units against reference-truth prevalence;
- frequency and magnitude of site-rank reversals;
- one prespecified ecological contrast/effect estimate, chosen before confirmatory labels are unblinded;
- review/annotation burden, reported separately from information gain rather than folded into an unvalidated utility score.

## Central hypotheses

### H1 — field consequence of decision coarsening

On held-out System-A ecological units, binary coarsening will have larger absolute error for the primary target-event-prevalence estimand than the process-resolved record.

**Falsifier:** the paired error difference is negligible or favours binary after the analysis plan is frozen.

### H2 — where decision coarsening matters

The error difference will be concentrated in ecological units with independently verified nuisance activity or compromised observability, not uniformly across all units.

**Falsifier:** the error difference is unrelated to independently labelled nuisance/observability strata.

### H3 — ecological-conclusion consequence

For one prespecified ecological contrast, process-resolved and binary records may yield materially different effect magnitude, rank ordering or qualitative conclusion when compared with the reference-truth analysis.

This is **not** preregistered as a guaranteed reversal. The confirmatory target is closeness to the reference-truth effect, not finding a dramatic sign flip.

### H4 — cross-system replication

The direction and magnitude of the core information-loss effects will be evaluated independently in System B where the required exposure and truth semantics can be established.

A failed cross-system replication remains a result and constrains generality.

### Chapter-2 hypotheses

Chapter-2 hypotheses `C2-H1` through `C2-H4` are defined in `CHAPTER2_THRESHOLD_CENSORING.md`. Their sequence is existence of threshold-absorbed events → condition dependence → ecological consequence → gate-semantics sensitivity.

## What would justify a journal above MEE

A stronger-journal submission requires all of the following, not merely more simulation:

- independently established field truth;
- an independently defined exposure universe rather than an event log used as its own denominator;
- a frozen held-out Chapter-1 comparison of binary versus process-resolved records;
- direct truth annotation of registered-B / shadow windows for REC;
- a real downstream ecological estimand, not only classifier accuracy;
- an explicit map of conditions where record-entry loss/coarsening do and do not matter;
- at least one independent biological/sensor replication or a comparably strong external dataset;
- no semantic-specific U-reason claim unless separately validated;
- annotation/calibration cost reported rather than ignored.

Without this evidence stack, Paper 1 should be submitted to MEE rather than delayed.

## Execution order

1. **Pilot System A in shadow mode**, defining the master exposure grid before inspecting gate outcomes.
2. Deliberately sample both registered deviations and logical B / non-entered windows for independent truth annotation.
3. Freeze the window definition, event truth, gate definition/version, archive-entry policy, Chapter-2 sampling design, grouping unit and primary estimand.
4. Freeze calibration criteria on development groups.
5. Collect/score new held-out field groups once.
6. Run REC/Chapter 2 first: baseline contamination, event absorption, archive-shadow contamination and condition map where identifiable.
7. Run Chapter 1 downstream on the same held-out exposure set: B/T/N/U versus binary ecological inference.
8. Run the one prespecified ecological contrast against reference truth and partition distortion attributable to gate/entry censoring versus later coarsening where identifiable.
9. In parallel, build the System-B replication only if its exposure denominator and protected truth can be frozen without circularity.
10. Only after both systems are resolved decide the journal tier.

## Hard separation from Paper 1

Paper-2 work in this repository must not change Paper-1 numerical claims, frozen synthetic outputs, D1-D5 status or current MEE package in `zuizui0223/tnoa`. Bug fixes to reusable software remain allowed if separately tested and do not change frozen Paper-1 evidence.
