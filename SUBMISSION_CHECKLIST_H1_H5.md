# Submission checklist — REC H1–H5 manuscript

Status: **MEE-standard preparation checklist with Ecological Informatics fallback.**

## A. Scientific closure

- [x] Primary ecological endpoint fixed: fox/badger species composition.
- [x] CT-position standardization completed and adverse `SF` retained.
- [x] Otter wet/dry reinterpreted after position standardization; adverse BS retained.
- [x] BirdVox limited to protected upstream-irreversibility stress test.
- [x] H5 recovery reported as a transport ladder, not universal correction.
- [x] Frozen camera+position adverse transport result retained.
- [x] Further post-hoc Findlay biological slicing stopped.
- [x] H6/PolliPi kept outside current H1–H5 empirical claim.

## B. Reusable method deliverable

- [x] Paper-facing method contract: `PAPER_METHOD_CONTRACT_H1_H5.md`.
- [x] Minimum information table: `TABLE1_METHOD_REQUIREMENTS_H1_H5.md`.
- [x] Full exposure-ledger schema available.
- [x] Truth/gate validators and deterministic identification witness available.
- [x] Pinned external-data workflows preserve source identities.
- [x] Machine-readable canonical result summaries committed.
- [x] Main figures generated from committed evidence through CI.
- [ ] **Open-source software license added to repository.**

### License blocker

Methods in Ecology and Evolution requires an explicit open-source license for code submitted with a paper. The repository currently has no root `LICENSE` file. A license should **not** be chosen implicitly: MIT/BSD/GPL/etc. have different legal/reuse implications. Choose and add the intended license before MEE submission.

## C. Manuscript structure

Current source: `MANUSCRIPT_DRAFT_H1_H5_V2.md`.

MEE initial-submission requirements to satisfy:

- [x] standard scientific structure present: Abstract, Introduction, Materials/Methods, Results, Discussion;
- [ ] convert Abstract to MEE numbered `1–4` format;
- [ ] confirm Abstract remains ≤350 words after numbered conversion;
- [ ] add `Data/Code for peer review` statement immediately after Abstract;
- [ ] add up to 8 alphabetized keywords;
- [ ] create separate title page with authors, institutions, addresses, acknowledgements, contributions, conflicts and data availability;
- [ ] add continuous line/page numbering in submission PDF;
- [ ] final word count including references/captions/statements ≤7,000–8,000 for a Standard/Research Article;
- [ ] embed or place figures/tables near first citation for review readability;
- [x] main result hierarchy no longer depends on H1–H5 numbering in prose.

## D. Figures and tables

- [x] Figure 1: auditable record-entry pipeline.
- [x] Figure 2a: raw fox/badger composition.
- [x] Figure 2b: position-standardized species distortion.
- [x] Figure 2c: otter context dependence including adverse BS.
- [x] Figure 3: protected BirdVox truth / entered / oracle contrast.
- [x] Figure 4a: recovery transport ladder.
- [x] Figure 4b: sham-control comparison.
- [x] Figure captions drafted in `FIGURE_CAPTIONS_H1_H5.md`.
- [x] Table 1 method requirements drafted.
- [ ] decide whether Fig. 4b belongs in main text or supplement.
- [ ] build optional Supplement S2/S3/S4 only from already frozen results; no new hypothesis search.

## E. Literature positioning

- [x] MacKenzie et al. 2002 — imperfect detection / occupancy acknowledged.
- [x] Guillera-Arroita 2017 — observation-process informative design acknowledged.
- [x] Burton et al. 2015 — camera-trap process/design context acknowledged.
- [x] Hofmeester et al. 2019 — camera/setup/environment detectability acknowledged.
- [x] Findlay et al. 2020 — sequential trigger/registration false negatives and CCTV acknowledged as nearest empirical prior art.
- [x] Palencia et al. 2022 — camera model/settings/deployment dependence acknowledged.
- [x] Ogawa et al. 2025 — downstream AI classification/occupancy error acknowledged.
- [x] generic domain-shift novelty explicitly disclaimed.
- [x] paper contribution narrowed to estimand closure + stage separation + correction transport audit.

Primary positioning note: `LITERATURE_POSITIONING_H1_H5.md`.

## F. Reviewer-risk controls

See `REVIEWER_ATTACK_MATRIX_H1_H5.md`.

Critical statements that must remain visible:

- [x] REC does not discover imperfect detection.
- [x] Findlay's original false-negative patterns are not claimed as new.
- [x] repeated pass rows are not independent animals/populations.
- [x] CT-position standardization is robustness adjustment, not causal species identification.
- [x] BS and SF adverse contexts remain reported.
- [x] BirdVox gate has poor discrimination and is not representative detector performance.
- [x] IPW is not claimed as a new estimator.
- [x] H5 is retrospective; prospective correction confirmation remains open.

## G. MEE editorial-fit gate

MEE explicitly prioritizes new methods and notes that workflows linking existing methods generally do not constitute a new method by themselves. Before a full MEE submission:

- [x] convert REC from acronym-first framing to a reusable data/measurement contract;
- [x] make Fig. 1 the organizing methodological object;
- [x] show application across a physical camera process and an acoustic digital-entry process;
- [x] include a falsified transport case rather than only benchmark success;
- [ ] send a **pre-submission enquiry** asking whether the estimand-centred audit contract plus empirical transport/falsification evidence is suitable as a Research Article;
- [ ] proceed to full MEE submission only if editorial response is encouraging or the team accepts the desk-rejection risk.

## H. Ecological Informatics fallback

If MEE judges methodological novelty insufficient:

- [x] current sensor/informatics framing already fits Ecological Informatics naturally;
- [ ] retitle around automated monitoring / event-table selection if needed;
- [ ] shorten abstract emphasis on formal method novelty;
- [ ] foreground cross-modal sensor data provenance, uncertainty and transport limits;
- [ ] retain all adverse results unchanged.

## Current go/no-go

**Science: GO.**

**MEE full submission: HOLD pending pre-submission enquiry + open-source license selection + final MEE formatting.**

**Ecological Informatics submission: essentially GO after normal manuscript formatting and license/data availability cleanup.**
