# REC prior-art boundary and nearest neighbours

Status: targeted positioning audit for the REC / Paper-2 program. This is **not** a systematic review.

## 1. Why this boundary is necessary

The core REC observation — a biological event can occur without appearing in the recorded data — is not historically novel. Ecology has long treated nondetection as distinct from absence, and camera-trap studies have directly measured multiple failure stages in the detection process.

REC should therefore be positioned around **where the selection mechanism is represented and audited in an automated observation pipeline**, not around the existence of imperfect detection itself.

## 2. Established ecological detection literature

### Occupancy with imperfect detection

MacKenzie et al. (2002) established the canonical point that nondetection at a site does not imply absence when detection probability is below one and jointly modeled occupancy and detection.

REC does **not** claim priority for:

- nondetection ≠ absence;
- latent ecological state plus observation process;
- covariate-dependent detection probability;
- repeated-observation correction of imperfect detection.

Relevant source:

- MacKenzie, D. I. et al. 2002. *Estimating Site Occupancy Rates When Detection Probabilities Are Less Than One*. Ecology 83:2248–2255. DOI: `10.1890/0012-9658(2002)083[2248:ESORWD]2.0.CO;2`.

### Ecological thresholds under imperfect detection

Jones et al. (2011) showed that ignoring variation in the observation process can alter inference about ecological threshold relationships.

REC does **not** claim priority for the general idea that an environmental relationship can be distorted by detection heterogeneity.

Relevant source:

- Jones, J. E. et al. 2011. *Estimating thresholds in occupancy when species detection is imperfect*. Ecology 92:2299–2309. DOI: `10.1890/10-2403.1`.

## 3. Camera-trap detection-process literature

### Multi-scale factors affecting camera-trap detection

Hofmeester et al. (2019) organized animal, camera, setup and environmental factors that affect camera-trap detectability and emphasized the need to account for species- and study-specific detection variation.

REC does **not** claim that distance, body size, environment, setup or camera properties are newly recognized drivers of detection.

Relevant source:

- Hofmeester, T. R. et al. 2019. *Framing pictures: A conceptual framework to identify and correct for biases in detection probability of camera traps enabling multi-species comparison*. Ecology and Evolution. DOI: `10.1002/ece3.4878`.

### Sequential component processes and independent CCTV truth

Findlay, Briers & White (2020) are a particularly close neighbour. They decomposed camera-trap detection into sequential processes including pass, trigger, image registration and image quality, and used CCTV with camera-trap arrays to quantify false negatives and their drivers. They reported substantial data loss, including trigger failures, and showed effects of distance, speed, species, model and settings.

This means REC must **not** claim to be the first to:

- decompose an automated sensor’s detection process;
- use an independent visual reference channel to find events missed by the tested sensor;
- quantify trigger/registration false negatives;
- show condition-dependent sensor loss.

Relevant source:

- Findlay, M. A., Briers, R. A. & White, P. J. C. 2020. *Component processes of detection probability in camera-trap studies: understanding the occurrence of false-negatives*. Mammal Research 65:167–180. DOI: `10.1007/s13364-020-00478-y`.

### Double-observer correction

Paired-camera/double-observer approaches have also been used to correct imperfect detection in density estimation.

REC does not claim priority for using a second observer/sensor to estimate missed detections.

Example:

- *Double-observer approach with camera traps can correct imperfect detection and improve the accuracy of density estimation of unmarked animal populations*. Scientific Reports 12, 2011 (2022).

## 4. Automated-classification and continuous-score ecological inference

Automated species recognition creates an additional threshold/classification layer after sensor acquisition.

Ogawa et al. (2025) explicitly compared occupancy models that account for false negatives and/or false positives in AI-identified species data, including thresholded confidence-score alternatives. Continuous-score occupancy work likewise avoids treating a single classifier threshold as the only route to ecological inference.

REC therefore does **not** claim priority for:

- integrating classifier error into occupancy;
- false-positive/false-negative ecological inference;
- avoiding hard classifier thresholds;
- propagating continuous classifier scores into ecological models.

Relevant source:

- Ogawa, R. et al. 2025. *A classification-occupancy model based on automatically identified species data*. Ecology 106:e70086. DOI: `10.1002/ecy.70086`.

Paper 1 (`zuizui0223/tnoa`) already positions against continuous-score ecological inference and related work; REC should reuse that bibliography rather than claiming a separate priority.

## 5. What REC adds as an architectural target

The potentially defensible REC contribution is the **record-entry selection layer as a versioned scientific object**.

The framework requires the following to be connected in one auditable chain:

1. a master exposure universe independent of the tested gate;
2. retained pre-gate evidence for every exposure or a declared recoverable sampling design;
3. a versioned registration gate;
4. a separate archive/event-log entry indicator;
5. deliberate truth sampling of logical baseline and/or non-entered windows;
6. explicit inclusion probabilities when the shadow set is subsampled;
7. an independent event-truth channel;
8. downstream comparison against reference-truth ecological estimands;
9. later TNOA-style semantic coarsening treated as a distinct information-loss stage.

This is a narrower claim than “model imperfect detection,” but broader than a camera-specific trigger-efficiency experiment.

## 6. Nearest-neighbour comparison

| Line of work | Main object | What is observed/estimated | REC distinction to test empirically |
| --- | --- | --- | --- |
| MacKenzie occupancy | latent occupancy + detection | site occupancy and detection probability from repeats | reconstructs the sensor’s record-entry mechanism and exposure denominator before downstream ecological model |
| Jones threshold occupancy | ecological threshold + imperfect detection | ecological breakpoints accounting for detection | audits whether the sensor gate itself manufactures/distorts a contrast before model fitting |
| Hofmeester camera framework | factors affecting camera detectability | conceptual/empirical detectability drivers | versioned exposure/gate/entry provenance and shadow-set sampling contract |
| Findlay et al. | sequential camera detection processes | pass/trigger/registration/quality false negatives using CCTV | generalizes the record-entry contract beyond a specific camera chain and explicitly links it to later semantic coarsening / ecological estimands |
| Double-observer camera methods | imperfect detection correction | density/detection from paired sensors | REC reference channel is primarily a truth/audit device; correction is a later, separately frozen step |
| Classification-occupancy | AI classification + occupancy | FP/FN-aware ecological inference | REC begins before event-log/classifier inclusion and asks which exposures never reached the classifier at all |
| TNOA Paper 1 | entered observation semantics | B/T/N/U, threshold semantics, coarsening information loss | REC is the pre-entry shadow side; TNOA is the post-entry semantic side |

The final paper should treat these distinctions as hypotheses about scope, not as established novelty until field results demonstrate them.

## 7. Strongest novelty wording currently allowed

Before field validation, the strongest safe wording is:

> REC is a proposed record-entry audit framework for automated ecological observation. It makes the exposure universe, pre-gate evidence, registration/retention rules and non-entered sampling design explicit so that condition-dependent event loss can be measured against independent truth before downstream observation semantics are analyzed.

After successful field evidence and cross-system replication, this may be strengthened to:

> REC provides a sensor-agnostic measurement contract for tracing how automated record-entry rules select the ecological events available to downstream inference, complementing imperfect-detection models that operate on already defined survey records.

Do not strengthen beyond this without a fresh prior-art audit.

## 8. Forbidden novelty claims

Do not write:

- “REC is the first framework to recognize false negatives.”
- “REC is the first method to separate detection from ecological state.”
- “REC is the first camera-trap framework to decompose detection.”
- “REC is the first use of an independent reference camera to find missed animals.”
- “REC solves imperfect detection.”
- “Standard occupancy cannot handle REC.”
- “All existing ecological monitoring assumes perfect detection.”

## 9. Research implication

The closest prior art makes Chapter 2 harder but scientifically better.

A publishable REC result should not stop at “we found missed events.” It should show at least one of:

1. record-entry loss occurs at a pipeline stage not represented in the downstream event log;
2. the loss is condition dependent in a way that changes a prespecified ecological estimand;
3. preserving the exposure universe and entry provenance reveals or corrects a conclusion that an event-log-only workflow cannot diagnose;
4. the same contract transfers to a second sensor/system even though its raw gate mechanism differs.

That is the standard REC should now be designed to meet.
