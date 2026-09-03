# Findlay camera-trap REC external validation

Status: **positive external real-world validation of REC record-entry loss and ecological composition distortion; not a novelty claim for camera-trap false negatives**.

This analysis uses the public `melaniefindlay/CT-Detection` repository at immutable commit `abc72f535bb59ebed202fb7acca852fc1647e97a`. GitHub Actions run `33775481327` verified the exact upstream Git blob identities before analysis and completed successfully. The machine-readable evidence is `results/findlay_camera_trap_real_data_v1.json`; the source artifact digest is `sha256:70d5aec4e8fa1c234d382555eac1707aa0f820fdf9683174e7eaaeff523205fd`.

## Why this system matters for REC

BirdVox provided a continuous time-domain exposure denominator but used an intentionally simple annotation-naive score whose protected discrimination was poor. Findlay provides a complementary system: every row is an independently observed **true animal pass**, and the recording process is the real camera-trap chain studied by the original authors.

For the registration table:

`true pass -> camera trigger R -> capture / registered record K`.

This directly identifies event-conditioned loss such as `P(R=0 | pass)` and bounded `P(K=0 | pass)`. It does **not** enumerate non-pass time, so full-denominator `q_shadow=P(event | no record)` is not identified and is intentionally not reported.

## REC-H1 — real record shadow: positive

Across 881 fox/badger passes:

- confirmed triggered passes: `428`;
- confirmed captured passes: `174`;
- `a_R = P(no trigger | pass) = 0.514188`;
- resolved-only `a_K = P(no capture | pass) = 0.802048`;
- partial-identification bounds for `a_K`: `0.800227–0.802497`;
- conditional registration failure after an evaluable confirmed trigger: `0.591549`.

Only two passes (`0.23%`) have unresolved CAPTURE, and they remain explicit dark mass rather than being recoded as failures.

The event-conditioned REC shadow is therefore not specific to the BirdVox score experiment: in an independently studied camera-trap process, substantial loss occurs both before trigger and between trigger and final capture.

## REC-H2 — structured selection: positive

Loss is strongly non-uniform across the pass and observation conditions represented in the released fox/badger table.

The observed range in `a_R` across levels is:

- distance: `0.507853`;
- camera position: `0.316828`;
- loitering: `0.196951`;
- species: `0.167528`;
- gait: `0.165709`;
- orientation: `0.164520`.

For final non-capture `a_K`, the largest resolved-only range is orientation (`0.457079`), followed by loitering (`0.283612`) and camera position (`0.219133`). These are descriptive condition maps, not row-level independent inferential tests.

Species illustrates the structure directly:

- badger: `a_R=0.406940`, resolved-only `a_K=0.733333`;
- fox: `a_R=0.574468`, `a_K=0.840426`.

Thus a scientific record produced by the same camera process does not preserve true passes uniformly across ecological categories.

## Independent wet/dry mechanism check within otters

The otter wet/dry trigger table contains 706 known pass-camera observations and again shows substantial trigger loss: resolved-only `a_R=0.390071` with bounds `0.389518–0.390935`.

More importantly, wet passes are missed more often than dry passes in **all three camera types**:

| camera | dry `a_R` | wet `a_R` | wet − dry |
| --- | ---: | ---: | ---: |
| A | 0.205882 | 0.622642 | +0.416759 |
| BS | 0.322314 | 0.514563 | +0.192249 |
| BV | 0.257576 | 0.514019 | +0.256443 |

This provides a particularly clear real-world example of REC-H2: record entry depends on the state/condition of the biological encounter, not merely on whether the encounter occurred.

## REC-H3 — ecological composition distortion: positive

### Species composition

In the true fox/badger pass world:

- badger proportion: `0.359818`;
- fox proportion: `0.640182`.

After trigger:

- badger: `0.439252`;
- fox: `0.560748`.

Among confirmed captures:

- badger: `0.482759`;
- fox: `0.517241`.

Total-variation distance from the true pass composition increases from `0.079434` at the trigger world to `0.122940` at the confirmed-capture world. Gait composition changes little at trigger (`TV=0.015965`) but substantially by confirmed capture (`TV=0.118785`).

### Wet/dry composition

Because wet passes have higher trigger loss, the recorded world systematically underrepresents them in every camera type:

- camera A: wet `0.438017` of true passes but `0.270270` of confirmed triggers (`TV=0.167746`);
- camera BS: `0.459821 -> 0.378788` (`TV=0.081034`);
- camera BV: `0.445833 -> 0.346667` (`TV=0.099167`).

This is the REC ecological consequence in a real sensor system: **selection before record entry changes the composition of the ecological world available to downstream analysis**.

## Relation to BirdVox and TNOA

The two real systems now play different roles.

**BirdVox** supplies the complete continuous exposure universe and directly demonstrates that upstream omission can almost erase a prespecified temporal ecological contrast even after granting a perfect downstream semantic stage.

**Findlay camera traps** show that event-conditioned trigger and registration shadows, structured by biological/observation conditions, occur in a real sensor process already studied independently of REC. The same mechanism changes species and wet/dry composition before downstream inference begins.

Together they support the REC→TNOA decomposition:

`ecological exposure -> pre-entry selection [REC] -> recorded rows -> semantic/coarsening loss [TNOA]`.

A perfect TNOA stage can improve the meaning of rows that exist; it cannot restore true encounters removed upstream.

## Positioning and hard boundaries

Findlay, Briers and White explicitly studied component detection probabilities and false negatives. REC does **not** claim that camera-trap detection failure, or its dependence on distance/wetness/etc., is newly discovered here. The contribution is the cross-system framework and estimand decomposition that places those losses in the same pre-entry information-loss architecture as BirdVox and connects them formally to the downstream TNOA problem.

Do not claim from this dataset:

- `q_shadow=P(event | no record)` over continuous time;
- animal occurrence or abundance bias directly;
- independence of every pass row as a biological replicate;
- novelty of the original camera-trap detectability patterns.

Safe status after this validation:

- REC-H1: **positive across two distinct real observation systems**;
- REC-H2: **positive real-world structured selection, with especially consistent wet > dry trigger loss across three camera types**;
- REC-H3: **positive composition distortion in camera traps plus temporal-gradient destruction in BirdVox**;
- REC/TNOA boundary: **empirically sharpened: downstream semantic perfection cannot restore upstream missing rows**.
