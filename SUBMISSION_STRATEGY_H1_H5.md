# Submission strategy — REC H1–H5 external-data manuscript

Status: **paper-facing venue decision after V4 logic, literature audit and full figure completion.**

## Recommended order

### 1. Methods in Ecology and Evolution — high-reward, higher framing risk

**Fit:** potentially strong if the paper is submitted explicitly as a **methodological measurement contract** rather than as a reanalysis showing camera-trap bias.

MEE states that its emphasis is on the description and analysis of new methodological approaches rather than the results of applying methods. It accepts analytical, practical and conceptual methods.

To make REC fit MEE, the paper must lead with:

- the auditable record-entry contract;
- the requirement for a gate-independent exposure/reference denominator;
- estimand closure before/after entry;
- the oracle downstream irreversibility diagnostic;
- transport validation as a required step for any entry correction.

Findlay and BirdVox are then **validation systems**, not the paper's subject matter.

Risk:

- imperfect detection and camera-trap process decomposition are prior art;
- if the editor sees REC mainly as relabelling established detection probability, desk rejection risk is substantial;
- the manuscript must therefore keep notation light but make the reusable workflow executable and sensor-agnostic.

Decision: **worth a first submission only if we finish the method-facing checklist and make Fig. 1 the paper's organizing object.**

### 2. Ecological Informatics — strongest natural scope fit

**Fit:** very strong.

The journal explicitly covers computational ecology and ecological data science, including novel concepts/tools for monitoring, sensor- and multimedia-based data acquisition, data management, uncertainty analysis, eco-acoustics, digital image processing and automated ecological workflows.

The present paper naturally fits as:

> an observation-pipeline audit showing how sensor record-entry transforms ecological data before downstream analysis, with reproducible diagnostics and correction-transport tests.

Advantages:

- the sensor/informatics framing does not require claiming a new general statistical theory;
- both camera and acoustic systems belong naturally in the scope;
- the practical metadata recommendation (exposure denominator, gate provenance, unresolved states, calibration/transport domain) becomes a direct contribution;
- adverse transport results are a strength rather than a distraction.

Decision: **best risk-adjusted target in the paper's current empirical form.**

### 3. Journal of Applied Ecology — only after adding a clearer management consequence

JAE emphasizes broad-reaching work at the interface of ecological science and management/policy.

The current manuscript has strong monitoring implications but does not yet demonstrate a management decision changing after correction. A JAE submission would need an additional applied bridge such as:

- species ranking or monitoring-priority changes;
- abundance/occupancy decision consequences;
- explicit implications for cross-program comparison or management thresholds.

Adding such an endpoint retrospectively to Findlay now would risk overfitting and is not recommended simply to target JAE.

Decision: **not the first target for the present version.**

## Recommended actual strategy

### Route A — ambitious

Submit first to **Methods in Ecology and Evolution** after one final method-facing revision.

Required before submission:

1. Fig. 1 becomes the organizing conceptual figure.
2. Methods opens with a reusable algorithm/contract, not with Findlay.
3. Add a compact table specifying required versus optional data fields for an auditable record-entry study.
4. Make the deterministic non-identifiability witness and validation scripts easy to run.
5. State explicitly how REC complements occupancy/detection models rather than replacing them.
6. Keep Findlay biological details concise enough that the paper does not read as a camera-trap case study.

If desk-rejected for insufficient methodological novelty, revise only the framing—not the results—and send to Ecological Informatics.

### Route B — fastest/cleanest

Target **Ecological Informatics** directly.

Use the current title family:

**Record-entry selection changes ecological estimands and limits the transport of detection correction**

Emphasize:

- automated monitoring pipelines;
- sensor-to-event-table transformation;
- reproducible data provenance;
- uncertainty/unresolved state handling;
- cross-modal camera/acoustic evidence;
- context-bounded correction transport.

This route requires less argument that the REC terminology itself is a novel method.

## Recommendation

**Prepare the manuscript at MEE methodological standard, but regard Ecological Informatics as the strongest natural venue.**

That strategy has two advantages:

1. the MEE preparation forces the method and reuse contract to be maximally clear;
2. if MEE judges the contribution too close to established imperfect-detection theory, the exact same strengthened manuscript remains highly suitable for Ecological Informatics with modest reframing.

## Do not change the science to fit the journal

Do not:

- invent another positive retrospective endpoint;
- hide the failed camera+position double holdout;
- re-promote pooled BS wet/dry as a robust mechanism;
- add H6 before the prospective field design is licensed;
- claim REC replaces occupancy or classification-error models.

The mixed transport result and position-standardized adverse cases are credibility assets.
