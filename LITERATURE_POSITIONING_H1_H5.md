# Literature positioning for the REC H1–H5 manuscript

Status: **targeted paper-facing positioning audit; not a systematic review.**

This note updates the prior-art boundary after the position-standardization and transport analyses. It is intentionally conservative: the paper does not claim discovery of imperfect detection, condition-dependent detectability, camera-trap process decomposition, external reference cameras, classifier error models, or domain shift.

## 1. Imperfect detection is the starting point, not the contribution

MacKenzie et al. (2002) established the modern occupancy-model formulation in which nondetection does not imply absence and detection probability is estimated jointly with ecological state.

Guillera-Arroita (2017) reviewed extensions of this observation-process framework and emphasized that inference under imperfect detection requires data collected in a way that is informative about the observation process, for example repeated visits, multiple observers/detection methods, or within-survey detection information.

REC therefore does **not** claim that an external observation model is a new need. Its narrower question is what can be learned when the unit that fails to enter the event table is itself explicitly enumerated or externally referenced before downstream inference.

References:

- MacKenzie, D. I., Nichols, J. D., Lachman, G. B., Droege, S., Royle, J. A. & Langtimm, C. A. (2002). Estimating site occupancy rates when detection probabilities are less than one. *Ecology* 83:2248–2255. DOI `10.1890/0012-9658(2002)083[2248:ESORWD]2.0.CO;2`.
- Guillera-Arroita, G. (2017). Modelling of species distributions, range dynamics and communities under imperfect detection: advances, challenges and opportunities. *Ecography* 40:281–295. DOI `10.1111/ecog.02445`.

## 2. Camera-trap detection is already known to be a multi-stage, context-dependent process

Burton et al. (2015) called for camera-trap survey designs to be linked explicitly to ecological processes and for better treatment of imperfect detection, spatial variability and methodological assumptions.

Hofmeester et al. (2019) organized camera-trap detectability across animal characteristics, camera specifications, setup protocols and environmental variables, explicitly motivating correction and transparent reporting of these factors.

Findlay, Briers & White (2020) are the closest empirical neighbour. They used independent CCTV truth and decomposed the physical camera process into sequential pass, trigger, registration and quality components. The present REC reanalysis therefore must not claim novelty for sequential detection probabilities, false negatives, independent reference video, or condition-dependent trigger/capture failure.

Palencia et al. (2022) further showed in a gold-standard remote-video field experiment that detection probability depends on camera model, species, distance, deployment height, activation sensitivity and day/night period, and warned against direct comparison across differently configured experiments.

These studies directly support the paper's conservative interpretation of the new transport result: an entry propensity is not an intrinsic invariant property of a species or event.

References:

- Burton, A. C. et al. (2015). Wildlife camera trapping: a review and recommendations for linking surveys to ecological processes. *Journal of Applied Ecology* 52:675–685. DOI `10.1111/1365-2664.12432`.
- Hofmeester, T. R. et al. (2019). Framing pictures: A conceptual framework to identify and correct for biases in detection probability of camera traps enabling multi-species comparison. *Ecology and Evolution* 9:2320–2336. DOI `10.1002/ece3.4878`.
- Findlay, M. A., Briers, R. A. & White, P. J. C. (2020). Component processes of detection probability in camera-trap studies: understanding the occurrence of false-negatives. *Mammal Research* 65:167–180. DOI `10.1007/s13364-020-00478-y`.
- Palencia, P., Vicente, J., Soriguer, R. C. & Acevedo, P. (2022). Towards a best-practices guide for camera trapping: assessing differences among camera trap models and settings under field conditions. *Journal of Zoology* 316:197–208. DOI `10.1111/jzo.12945`.

## 3. Downstream AI/classification uncertainty is also established

Automated biodiversity monitoring creates a later error layer after a sensor has produced candidate observations. Ogawa et al. (2025) integrated false-negative detection and probabilistic false-positive classification in a classification-occupancy model using AI confidence scores and external evaluation.

REC should therefore not claim priority for propagating AI uncertainty into ecological inference. The manuscript should use this literature to sharpen the layer boundary:

`pre-entry selection -> available rows -> semantic/classification uncertainty -> ecological model`.

The BirdVox oracle analysis contributes only the empirical statement that making the **later** semantic stage perfect cannot recreate true events that were removed **before** that stage.

Reference:

- Ogawa, R., Gosselin, F., Darras, K. F. A., Roilo, S. & Cord, A. F. (2025). A classification-occupancy model based on automatically identified species data. *Ecology* 106:e70086. DOI `10.1002/ecy.70086`.

## 4. Domain shift is known; REC's transport result concerns a different object

Recent wildlife-computer-vision work explicitly treats location/environment changes as domain shift and evaluates generalization to unseen camera-trap domains. This means the REC paper should not present "context dependence" or "transport failure" as a newly discovered machine-learning principle.

The distinction is the object being transported. In REC H5, the transported object is not a species classifier but an **entry-propensity calibration used to reconstruct an ecological composition estimand**. The frozen camera-plus-position holdout asks whether a selection correction learned in one observation domain remains valid when both hardware and physical context change.

This is why the adverse H5 result belongs in the paper: it converts generic context dependence into an estimand-level measurement consequence.

Useful contemporary neighbours:

- Santamaria, J. D., Isaza, C. & Giraldo, J. H. (2025). CATALOG: A Camera Trap Language-Guided Contrastive Learning Model. *WACV 2025*, 1197–1206. DOI `10.1109/WACV61041.2025.00124`.
- Yang, Z., Tian, Y., Wang, L. & Zhang, J. (2025). Enhancing generalization in camera trap image recognition: Fine-tuning visual language models. *Neurocomputing* 634:129826. DOI `10.1016/j.neucom.2025.129826`.

These are downstream recognition/domain-shift papers, not direct methodological predecessors of REC correction.

## 5. What the current manuscript can defensibly claim

The safest contribution statement is:

> **We connect independently observed exposure/reference events to pre-entry selection, the ecological estimand available after that selection, downstream irreversibility, and out-of-sample correction transport in one auditable measurement workflow.**

The empirical additions relative to the nearest neighbours are:

1. **estimand closure:** the same external-reference passes are used to show how species-selective entry changes the composition that downstream ecology receives;
2. **within-context robustness:** fox/badger species distortion remains after standardizing reference and recorded worlds to the same CT-position distribution;
3. **stage separation:** the protected BirdVox oracle comparison demonstrates that downstream semantic perfection cannot restore upstream-omitted rows;
4. **recovery evaluation:** entry-propensity information is used to attempt ecological-estimand recovery outside the calibration rows;
5. **transport falsification:** a frozen harder transport test is retained when correction worsens rather than being retuned away.

## 6. What the manuscript should explicitly concede

State in the Introduction or Discussion that:

- occupancy and related models already formalize imperfect detection;
- camera-trap studies already decompose and experimentally measure trigger/registration failures;
- external reference video is established;
- camera model/setup/environment dependence is established;
- automated-classification ecological models already propagate FP/FN uncertainty;
- cross-domain generalization failure is widely recognized in automated recognition.

The paper's practical novelty is therefore not the acronym REC. It is the **measurement contract and the empirical estimand/transport audit built from it**.
