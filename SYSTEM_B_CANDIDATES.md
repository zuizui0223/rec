# REC external replication candidates

Status: **exploratory candidate audit; no confirmatory dataset frozen**.

REC and TNOA do not require the same external dataset. A dataset can be strong for post-entry semantic coarsening while being unable to identify the pre-entry shadow world.

## Evaluation criteria

A strong REC replication candidate should provide as many of the following as possible:

1. a gate-independent exposure denominator;
2. retained continuous/pre-gate evidence;
3. independent or detector-blind event truth;
4. both entered and non-entered exposures;
5. condition covariates relevant to entry loss;
6. independent grouping for held-out analysis;
7. enough provenance to reproduce the gate/entry mechanism.

## Candidate A — Findlay CT-Detection

Source: Findlay, Briers & White (2020), *Mammal Research*, DOI `10.1007/s13364-020-00478-y`; public repository `melaniefindlay/CT-Detection`.

### Strengths

- independent CCTV reference relative to camera traps;
- true animal passes can be compared with trigger success;
- public trigger and registration datasets plus analysis code;
- directly measures physical sensor failures rather than only classifier errors;
- condition variables include factors such as distance, gait/speed proxies, camera identity and other setup/animal variables.

### Limits

- the released tables are organized around observed animal passes/processes rather than a complete fixed temporal exposure universe;
- therefore they are strong for event-conditioned absorption such as `P(no trigger | true pass)` but may not identify `P(event | no record)` over all no-entry time windows;
- ecological downstream contrasts/site rankings were not the primary design target.

### REC role

**Best current external physical-sensor neighbour / partial replication.** Use to test whether REC's event-conditioned gate-loss quantities can reproduce known trigger/registration effects and to sharpen the boundary against prior art. Do not present reanalysis as a novel discovery of camera false negatives.

## Candidate B — BirdVox-full-night

Source: Lostanlen et al. BirdVox-full-night, Zenodo DOI `10.5281/zenodo.1172143` / versioned record `10.5281/zenodo.1205569`.

### Strengths

- six full-night continuous recordings, roughly 62 hours total;
- 35,402 expert-pinned avian flight calls;
- continuous time allows a master exposure grid to be defined independently of a tested detection algorithm;
- detector thresholds/gates can be applied after the exposure universe is frozen;
- non-detected time windows remain enumerable;
- six sensors provide natural grouping/replication structure.

### Limits

- expert truth comes from the same recorded audio stream, so calls physically missed by the microphone cannot be recovered;
- validates algorithmic/digital record-entry censoring, not the full physical sensor acquisition chain;
- species identity is not the primary label in the full-night dataset;
- confirmatory detector choice and development/test separation must be frozen without reusing protected annotations improperly.

### REC role

**Best current public candidate for a complete algorithmic REC denominator experiment.** A master time grid can exist before any detector fires.

## Candidate C — WABAD

WABAD provides thousands of minutes of expert-annotated passive-acoustic recordings from many sites/biomes and many bird species.

### Strengths

- broad geography and taxonomic coverage;
- expert time-frequency annotations;
- useful for cross-condition and cross-site generalization.

### Limits

- REC must first verify how the released audio segments were selected; a dataset of selected recordings/clips is not automatically a population exposure denominator;
- heterogeneous sites and recording protocols complicate a single frozen gate comparison.

### REC role

**Later generalization candidate**, after provenance/sampling review. Do not use for `q_shadow` until the exposure denominator represented by released files is explicit.

## Candidate D — Snapshot Serengeti

### Strengths

- very large ecological camera-trap resource;
- raw imagery/classifications and an expert gold-standard subset;
- strong for post-entry classification/semantic analyses and ecological aggregation.

### Limits for REC

- primarily event-triggered imagery;
- animals that never triggered the camera generally leave no image row;
- the archive therefore does not itself enumerate the non-triggered exposure set;
- `P(event | no trigger/no record)` is not identifiable without an external exposure/reference mechanism.

### REC role

**Retain for Chapter-1 / post-entry TNOA replication, not as the primary upstream REC-H1/H5 dataset.**

## Candidate E — Caltech Camera Traps / similar event-triggered image archives

Same structural issue as Snapshot Serengeti: large and valuable for post-entry recognition/occupancy analyses, but event-triggered rows do not by themselves define the missed-event denominator.

## Current preferred external evidence stack

### Physical entry process

Findlay CT-Detection or a new paired-reference camera experiment.

Target quantity:

`P(gate/registration failure | independently verified animal pass)`.

### Algorithmic entry process

BirdVox-full-night.

Target quantities:

- `P(expert event | detector non-entry window)`;
- `P(detector non-entry | expert event)`;
- condition/time/sensor dependence;
- effect of alternative frozen gates on downstream event-rate contrasts.

### Post-entry semantic process

Snapshot Serengeti or another well-labelled camera dataset.

Target: Chapter-1 process-resolved versus coarsened record comparison where defensible.

## Decision rule

Do not force one external dataset to validate every layer. REC's strongest cross-system story is likely:

1. prospective System A for the complete physical+algorithmic+semantic chain;
2. public physical-sensor partial replication (Findlay);
3. public continuous-acoustic algorithmic replication (BirdVox);
4. optional post-entry camera semantic replication (Snapshot Serengeti).

This is stronger than pretending an event-triggered archive can reveal exposures it never recorded.
