# Findlay camera-trap REC external validation

Status: **positive external real-world validation of record-entry loss and ecological composition distortion; later CT-position standardization sharpens which composition effects are robust. This is not a novelty claim for camera-trap false negatives.**

Source: public `melaniefindlay/CT-Detection` repository at immutable commit `abc72f535bb59ebed202fb7acca852fc1647e97a`.

The original real-data workflow verified exact upstream Git blob identities and completed successfully. Machine-readable raw validation evidence is in `results/findlay_camera_trap_real_data_v1.json`.

A later frozen robustness workflow standardized reference and recorded worlds to the same CT-position distribution. Its summary is `results/FINDLAY_POSITION_STANDARDIZED_DISTORTION.md` and `results/findlay_position_standardized_distortion_summary_v1.json`.

## Why this system matters for REC

Every released row is an independently observed **true animal pass** before camera-trap trigger/capture. For the fox/badger registration table:

`CCTV-confirmed pass -> camera trigger R -> confirmed capture / usable record K`.

This directly identifies event-conditioned loss such as `P(R=0 | pass)` and bounded `P(K=0 | pass)`. It does **not** enumerate non-pass time, so continuous-time `q_shadow=P(event | no record)` is not identified and is intentionally not reported.

## H1 — real record shadow: positive

Across 881 fox/badger passes:

- confirmed triggered passes: `428`;
- confirmed captured passes: `174`;
- `a_R = P(no trigger | pass) = 0.514188`;
- resolved-only `a_K = P(no capture | pass) = 0.802048`;
- partial-identification bounds for `a_K`: `0.800227–0.802497`;
- conditional registration failure after an evaluable confirmed trigger: `0.591549`.

Only two passes (`0.23%`) have unresolved CAPTURE, and they remain explicit unresolved mass rather than being recoded as failures.

## H2/H3 primary endpoint — fox/badger species composition

### Raw composition shift

In the true pass world:

- badger proportion: `0.359818`;
- fox proportion: `0.640182`.

After confirmed trigger:

- badger: `0.439252`;
- fox: `0.560748`.

Among confirmed captures:

- badger: `0.482759`;
- fox: `0.517241`.

Total-variation distance from the reference pass composition is `0.079434` at trigger and `0.122940` at confirmed capture.

### CT-position-standardized robustness

A frozen follow-up tested whether this pooled shift was simply caused by changing representation of physical CT positions. Reference and recorded composition were standardized to the **same** position distribution using both equal-position and reference-pass weighting.

At trigger:

- equal-position standardized truth badger proportion: `0.367406`;
- standardized recorded badger proportion: `0.429819`;
- shift: `+0.062413`;
- reference-pass-weighted shift: `+0.053498`;
- positive direction in `3/4` positions.

At final capture:

- equal-position standardized truth: `0.367406`;
- standardized recorded: `0.517249`;
- shift: `+0.149843`;
- reference-pass-weighted shift: `+0.139894`;
- positive direction in `3/4` positions.

`SF` is the retained adverse position at both stages.

### Interpretation

The fox/badger species-composition distortion therefore survives control of the aggregate CT-position mixture. This is now the strongest primary Findlay H2→H3 endpoint:

> **species-selective record entry changes the ecological composition available to downstream analysis within observation strata.**

This is still a retrospective observational measurement result. CT positions are not independent animals or population replicates, and the analysis does not establish a causal species effect.

## Otter wet/dry — useful but context dependent

The otter table contains 706 pass-camera observations and again shows substantial trigger loss: resolved-only `a_R=0.390071`, with bounds `0.389518–0.390935`.

### Raw pooled result

Wet passes have greater pooled trigger loss than dry passes in each camera setting:

| camera | dry `a_R` | wet `a_R` | wet − dry |
| --- | ---: | ---: | ---: |
| A | 0.205882 | 0.622642 | +0.416759 |
| BS | 0.322314 | 0.514563 | +0.192249 |
| BV | 0.257576 | 0.514019 | +0.256443 |

Accordingly, pooled wet representation changes from reference pass world to triggered record world:

- A: `0.438017 -> 0.270270`;
- BS: `0.459821 -> 0.378788`;
- BV: `0.445833 -> 0.346667`.

### CT-position-standardized follow-up

The later frozen robustness test shows that these pooled contrasts do not all have the same interpretation.

**A** remains strongly position-robust:

- equal-position standardized shift: `-0.126993`;
- reference-pass-weighted shift: `-0.134821`;
- negative direction in `4/4` positions.

**BV** remains negative overall:

- standardized shifts: `-0.046370` and `-0.052487`;
- negative direction in `3/4` positions.

**BS** does **not** retain the pooled wet-underrepresentation pattern:

- equal-position standardized shift: `+0.003021`;
- reference-pass-weighted shift: `+0.000893`;
- negative vs positive direction split `2/4` vs `2/4` positions.

### Revised interpretation

The earlier statement that wet underrepresentation cleanly repeats across all three camera settings is too strong after standardization.

The safe interpretation is:

> **A and BV support a position-robust wet/dry entry mechanism, whereas BS is an aggregation-sensitive adverse case. The operating selection function itself can depend on observation context.**

This mixed result directly motivates the later H5 transport tests.

## Other structured entry dimensions

The fox/badger table also shows large descriptive differences in event-conditioned loss across recorded pass/observation categories.

Observed ranges in `a_R` include:

- distance: `0.507853`;
- camera position: `0.316828`;
- loitering: `0.196951`;
- species: `0.167528`;
- gait: `0.165709`;
- orientation: `0.164520`.

For final non-capture `a_K`, the largest resolved-only ranges include orientation (`0.457079`), loitering (`0.283612`) and camera position (`0.219133`). These remain descriptive condition maps, not row-level independent inferential tests.

## Relation to BirdVox and H5

**BirdVox** provides the cross-modality irreversibility stress test: even oracle-perfect downstream semantics cannot restore truth-positive windows removed upstream.

**Findlay** provides the physical-sensor estimand result: record entry changes species composition, with a position-standardized primary endpoint and an otter mechanism that explicitly reveals context dependence.

**H5** then asks whether retained entry information can reduce the resulting composition error. Matched-context and species position-holdout analyses show partial recovery, while a frozen simultaneous camera+position shift shows that correction does not transport automatically.

See:

- `results/FINDLAY_H5_CORRECTION_RESULT.md`;
- `results/FINDLAY_H5_TRANSPORT_BOUNDARY.md`;
- `results/FINDLAY_SPECIES_POSITION_RECOVERY.md`.

## Positioning and hard boundaries

Findlay, Briers and White explicitly studied component detection probabilities and false negatives. REC does **not** claim that camera-trap detection failure, or its dependence on distance/wetness/species/etc., is newly discovered.

The paper-level contribution is the estimand-centered measurement chain:

`external reference -> pre-entry selection -> changed ecological composition -> correction and transport test`.

Do not claim from this dataset:

- `q_shadow=P(event | no record)` over continuous time;
- animal occurrence or abundance bias directly;
- independence of every pass row as a biological replicate;
- universal wetness effects across all camera settings;
- causal species-specific detectability;
- novelty of the original Findlay false-negative patterns.
