# REC H1–H5 manuscript readiness

Status: **draft-ready external-data paper; strongest remaining upgrade is prospective/independent correction confirmation, not more retrospective slicing of Findlay.**

Canonical logic: `PAPER_LOGIC_H1_H5_V3.md`.

## What is already strong enough to write

### 1. The paper has a narrow question that is not prior-art duplication

Do not ask whether imperfect detection exists.

Ask:

> When pre-entry selection is measurable against an external exposure/reference world, does it change the ecological estimand, is that loss recoverable downstream, and under what observation contexts can entry-aware correction be trusted?

### 2. The main empirical chain closes in a physical sensor system

Findlay provides:

`CCTV true passes -> trigger/capture selection -> changed ecological composition`.

Two ecological composition endpoints now support the chain:

- otter wet/dry;
- fox/badger species.

### 3. Cross-modality irreversibility is independently demonstrated

Protected BirdVox shows that an oracle downstream semantic stage cannot recreate truth-positive windows removed upstream.

This is useful because it separates REC's problem from classifier-only methods papers.

### 4. Recovery is tested rather than merely proposed

Positive evidence:

- wet/dry matched-context camera holdout: 48.91% MAE reduction, 3/3 cameras;
- fox/badger leave-position-out trigger composition: 26.47% mean MAE reduction, 3/4 positions;
- fox/badger final-capture composition: 20.32% mean MAE reduction, 3/4 positions.

Adverse transport evidence:

- wet/dry camera+position double holdout: 19.09% aggregate error increase;
- within-camera position-only wet/dry transport: only 5.81% mean improvement and 6/12 cells;
- fox/badger position `SF` worsens at both trigger and final capture.

This makes the paper's practical conclusion stronger: correction requires a validated transport domain.

## Evidence-strength matrix

| Paper claim | Evidence | Current strength | Manuscript role |
| --- | --- | --- | --- |
| Event-log-only data cannot characterize non-entered biology | deterministic identification witness + external denominators | strong methodological | Result 1 / Fig. 1 |
| True events fail before usable record entry | Findlay + BirdVox | strong cross-modality | brief foundation |
| Entry is structured | Findlay wet/dry, species, distance/conditions; BirdVox time/gate | strong descriptive/mechanistic | Result 2 |
| Entry selection changes ecological estimands | wet/dry composition, fox/badger species composition, BirdVox temporal contrast | strong multi-endpoint | central result |
| Downstream perfection cannot restore upstream omission | BirdVox oracle true-entry-only analysis | strong stress-test | Result 3 |
| Entry information can support recovery | wet/dry camera holdout + fox/badger position holdout | positive but retrospective | Result 4 |
| Correction transports broadly | frozen wet/dry camera+position double holdout | **falsified** | central transport boundary |
| Prospective correction improves untouched field data | not yet available | open | future / PolliPi |
| Same-system REC→TNOA decomposition | architecture only | open | future H6 |

## What not to add now

Avoid more post-hoc Findlay splits simply to find another positive subset. Additional retrospective slicing after the transport result will have diminishing evidential value and risks making the paper look tuned.

Do not attempt to rescue the failed double-holdout by replacing it with the positive exploratory position diagnostic.

Do not add H6 merely to make the paper look larger. It asks a different prospective integration question.

## One high-value additional validation, if available

The strongest next upgrade is an **independent or prospective correction test** with a frozen transport domain.

Ideal design:

1. define external exposure/reference truth;
2. designate development/calibration units before scoring;
3. freeze entry model and ecological estimand;
4. designate a physically separate held-out context;
5. compare raw vs corrected error exactly once;
6. retain a sham/direction-reversed or no-correction comparator;
7. report null/adverse outcome unchanged.

PolliPi is already being prepared for this role, but the current H1–H5 manuscript should not wait for it unless aiming for a substantially higher-risk/higher-reward venue.

## Recommended manuscript emphasis

Allocate space roughly as follows:

- 10–15%: identification / why an exposure denominator is required;
- 40–45%: physical Findlay selection → ecological distortion;
- 15–20%: BirdVox irreversibility stress test;
- 25–30%: recovery and transport boundary.

Do not let formal state notation dominate the empirical paper.

## Main figures

1. **Auditable pipeline** — reference/exposure world, entry selection, event table, downstream semantics.
2. **Selection changes composition** — otter wet/dry + fox/badger species.
3. **Irreversibility** — BirdVox truth contrast vs entered/oracle contrast.
4. **Recovery transport ladder** — matched context, position shift, camera+position shift, second-endpoint species recovery; raw/correct/sham errors.

## Main-table recommendation

One compact table should report every recovery validation without hiding adverse tests:

| Endpoint / transport regime | Raw MAE | Corrected MAE | Sham MAE | Relative change | Units improved |
| --- | ---: | ---: | ---: | ---: | ---: |
| Otter wet/dry: camera holdout, matched context | 0.115982 | 0.059258 | — | −48.91% | 3/3 |
| Otter wet/dry: within-camera position holdout | 0.068216 | 0.064250 | 0.150278 | −5.81% | 6/12 |
| Otter wet/dry: camera + position double holdout | 0.068216 | 0.081237 | 0.153652 | +19.09% | 6/12 |
| Fox/badger species: trigger, position holdout | 0.123093 | 0.090510 | 0.150218 | −26.47% | 3/4 |
| Fox/badger species: final capture, position holdout | 0.210807 | 0.167972 | 0.260198 | −20.32% | 3/4 |

This table is a major credibility asset: it shows that the correction was subjected to conditions where it could fail, and did fail.

## Current decision

**Start drafting the paper now.**

The external evidence is no longer just a collection of H1–H5 positives. It supports a coherent claim with both confirmation and falsification:

> selective record entry changes ecological estimands; entry provenance can enable partial recovery, but the recovery model has an observation-specific transport domain.

The next development branch should therefore be manuscript/figures rather than another exploratory Findlay hypothesis branch.
