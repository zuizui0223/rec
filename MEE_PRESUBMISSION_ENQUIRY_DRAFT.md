# MEE pre-submission enquiry draft

Target: *Methods in Ecology and Evolution*

Purpose: ask whether the current contribution is appropriate as a Research Article **before** investing in full MEE-specific submission formatting.

Do not send until author list/title are finalized.

---

**Subject:** Pre-submission enquiry: auditing record-entry selection before ecological event-table analysis

Dear Editors of *Methods in Ecology and Evolution*,

I am writing to ask whether the manuscript described below would be suitable for consideration as a Research Article in *Methods in Ecology and Evolution*.

Our manuscript develops a reusable measurement contract for auditing **record-entry selection** in automated ecological monitoring. The method begins from an exposure/reference denominator defined independently of the tested event detector, links external truth to pre-entry gate and record-retention provenance, compares the same ecological estimand before and after record entry, tests whether downstream semantic accuracy could recover upstream omissions, and evaluates whether an entry-aware correction transports outside its calibration context.

We do **not** claim that imperfect detection, sequential camera-trap detection processes, independent reference cameras, inverse-probability weighting, or context-dependent detectability are new. Instead, the methodological contribution is the explicit linkage of these stages into an auditable pre-entry data contract and a fixed sequence of estimand, irreversibility and correction-transport audits. We provide schemas, validators, reproducible workflows and a minimum-information table specifying what monitoring systems must retain for each level of claim.

The method is evaluated in two distinct observation systems. In CCTV-referenced camera-trap data, record entry changes fox/badger species composition even after standardizing the reference and recorded worlds to the same camera-position distribution. Entry-aware correction reduces composition error in several held-out contexts, but a frozen simultaneous camera-plus-position transport test increases error, establishing an adverse applicability-domain result rather than universal correction. In protected continuous-acoustic data, an oracle-perfect downstream semantic stage cannot recover a temporal ecological contrast once true windows have been omitted upstream.

The manuscript is therefore intended as a general measurement/audit method rather than a camera-trap case study, but we recognize that the journal does not normally consider workflows that simply combine existing methods. We would be grateful for your view on whether the estimand-centred record-entry audit contract, together with its cross-system validation and falsified transport test, constitutes sufficient methodological advance for a Research Article in the journal.

A current working title is:

**“Record-entry selection changes ecological estimands and limits the transport of detection correction.”**

Thank you for considering this enquiry.

Sincerely,

[Corresponding author]
[Affiliation]
[Email]

---

## Optional one-paragraph attachment/summary if requested

The proposed method requires three linked data objects: (1) an exposure/reference ledger containing observation opportunities independently of detector output, (2) a pre-entry process table retaining gate/trigger and record-entry provenance, and (3) the conventional downstream event/semantic table linked back to the exposure identifier. Four audits then quantify non-entry against reference truth, ecological-estimand distortion, downstream irreversibility, and correction transport. The implementation is sensor-agnostic: the paper instantiates the same contract with a physical camera-trigger/capture chain and a digital acoustic-entry gate.

## Before sending

- [ ] finalize corresponding author and affiliation;
- [ ] confirm manuscript working title;
- [ ] provide private/public repository link if appropriate;
- [ ] decide whether to attach Fig. 1 or a 1-page method summary;
- [ ] choose repository open-source license before sharing code as publication-ready software;
- [ ] do not soften the statement that Findlay/imperfect-detection/IPW components are established prior art.
