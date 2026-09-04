# Table 1 — Minimum information for an auditable record-entry study

Status: **paper-facing table draft derived from `PAPER_METHOD_CONTRACT_H1_H5.md`.**

| Information object | Minimum field / provenance | Required? | What it identifies or enables | If absent |
| --- | --- | --- | --- | --- |
| Exposure denominator | stable `exposure_id` generated independently of tested detector/gate | **Required for pre-entry claims** | enumerates observation opportunities including those that create no event row | non-entered opportunities are absent by construction; their frequency cannot be audited |
| Exposure timing/context | time/window plus `system_id` and `context_id` | **Required** | aligns reference, entry process and transport context | entry rates and estimands cannot be compared on a common observation universe |
| Primary acquisition availability | whether tested primary evidence existed and was usable | **Required when acquisition can fail** | separates acquisition failure from gate rejection | upstream hardware loss is silently mixed with gate nondetection |
| Independent event truth | event / no-event / unresolved from an external reference mechanism | **Required for empirical shadow composition** | identifies true events among entered and non-entered exposures | only non-entry is enumerable; biological content of missing rows remains unidentified |
| Reference sampling probability | inclusion probability for externally audited exposures | **Required if truth is subsampled** | permits weighted inference from sampled reference truth | reference audit can be selection-biased and cannot be generalized to the exposure universe |
| Pre-entry evidence | score/features or stage-specific physical evidence available before final record creation | Recommended / required for gate analysis | diagnoses where and why entry changes; allows alternative frozen gates | only aggregate entry/no-entry can be studied |
| Gate / trigger version | exact rule, threshold, firmware/settings or physical trigger configuration | **Required for reproducibility** | attributes recorded-world selection to a versioned operating rule | observed entry propensity cannot be reproduced or compared across deployments |
| Gate result | pass / reject / unresolved-not-evaluable | **Required when separable from final entry** | separates gate rejection from later archive/retention loss | distinct failure stages are collapsed |
| Record-entry indicator | usable record created: yes/no | **Required** | defines the scientific rows available to conventional downstream analysis | no direct bridge exists between exposure opportunities and the final event table |
| Archive / retention provenance | entry-policy version and reason for exclusion | Recommended when post-gate loss occurs | separates sensor/gate failure from deliberate or accidental retention loss | final missingness is misattributed to detection |
| Unresolved-state flag | explicit unresolved state for reference/trigger/entry fields | **Required when ambiguity exists** | supports resolved-only estimates and partial-identification/sensitivity bounds | unknown states are silently converted into biological or operational negatives |
| Downstream record link | `record_id` linked back to `exposure_id` | **Required for upstream/downstream decomposition** | traces each analysed row to the exposure process that created it | downstream semantic accuracy cannot be separated from entry selection |
| Frozen ecological estimand | predefined composition, contrast, prevalence or other target | **Required for H3/H5-style claims** | measures whether selection changes the scientific quantity of interest | study reduces to sensor-performance reporting without ecological consequence |
| Context-standardization rule | frozen hardware/position/site weighting or comparable adjustment | Required when context composition differs | tests whether estimand distortion persists within a common observation-context distribution | pooled shifts may be artifacts of changing context mixtures |
| Calibration provenance | contexts used to estimate entry propensities | **Required for correction** | defines where the correction model learned its operating meaning | a corrected estimate has no auditable applicability domain |
| Held-out transport domain | contexts excluded from calibration and evaluated once | **Required for transport claim** | tests whether entry correction generalizes beyond calibration rows | correction success may be in-sample or matched-context only |
| Falsification comparator | raw estimate and, where meaningful, sham/direction-reversed correction | Recommended | distinguishes useful entry information from arbitrary reweighting | movement toward truth can be difficult to interpret mechanistically |

## Caption-ready text

**Table 1. Minimum information required to audit ecological record-entry selection.** A final event table is sufficient for describing entered records but not for empirical claims about biological events that never became rows. Pre-entry claims require an exposure denominator generated independently of the tested gate and, for biological composition, an independent reference-truth mechanism. Correction additionally requires calibration provenance and an explicitly evaluated transport domain. Fields are required only when the corresponding stage exists in the observation system; for example, a physical camera trigger can serve directly as the pre-entry gate outcome when no continuous score is available.

## Mapping to the current validation systems

| Contract component | Findlay fox/badger | Findlay otter | BirdVox protected |
| --- | --- | --- | --- |
| external denominator/reference | CCTV-confirmed animal passes | CCTV-confirmed pass-camera observations | continuous one-second audio grid |
| biological truth | fox/badger pass and species | pass plus wet/dry state | expert event annotations within recorded audio |
| pre-entry process | trigger → confirmed capture | camera-specific trigger | frozen digital band-energy gate |
| observation context | CT position | camera setting × CT position | protected sensor/unit and time block |
| ecological estimand | badger proportion | wet proportion | late-minus-early event-window prevalence contrast |
| downstream oracle | not required for main species result | not required | true-entry-only record after removing false entries |
| correction transport | leave-position-out species propensities | camera / position transport ladder | not attempted because gate is deliberately adverse |
