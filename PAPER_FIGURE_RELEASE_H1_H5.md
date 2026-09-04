# Paper figure release — REC H1–H5

Status: **visual-QA passed manuscript figure set.**

Latest figure workflow:

- GitHub Actions run: `33866742662`
- source commit: `a93e01ca89297ff8e46c981ece055d00f3417406`
- artifact id: `9934254727`
- artifact name: `rec-h1-h5-paper-figures`
- artifact SHA-256 digest: `1c4103d3abfac48420e0a7763f4e59af889f1ba463a5db385fea7e255c87edef`

The workflow regenerates all empirical plots from committed machine-readable evidence, then applies layout-only polishing to Figures 1, 3 and 4. No result selection or model re-estimation occurs in figure generation.

## Released files

1. `fig1_auditable_record_entry_pipeline.png`
   - schematic measurement contract;
   - external exposure/reference → pre-entry process → usable record → downstream semantics → ecological estimand;
   - explicitly marks the non-entered branch invisible to an event-table-only analysis.

2. `fig2a_badger_composition.png`
   - reference / trigger / capture badger composition.

3. `fig2b_position_standardized_badger.png`
   - common-position standardized badger-composition shifts at trigger and final capture.

4. `fig2c_otter_position_standardization.png`
   - A/BV robust wet underrepresentation and adverse BS context after position standardization.

5. `fig3_birdvox_irreversibility.png`
   - reference truth / entered record / oracle-downstream temporal contrast for protected unit02, unit05 and pooled protected units;
   - explicitly notes poor gate discrimination and stress-test interpretation.

6. `fig4_recovery_transport_ladder.png`
   - horizontal raw-versus-corrected error ladder across matched and shifted calibration domains;
   - relative error changes printed directly;
   - exploratory within-camera position diagnostic explicitly marked with an asterisk.

7. `fig4b_sham_controls.png`
   - raw / correct / swapped-sham errors for harder transport tests.

## Visual QA

The released set was inspected after generation.

- Figure 1: right boundary no longer clipped; non-entered branch and event-table-visible region are readable.
- Figure 2 panels: scales and labels readable; adverse contexts remain visible.
- Figure 3: near-zero raw/oracle values use dedicated labels and no longer overlap; interpretation footnote is visible.
- Figure 4: horizontal layout removes crowded category labels; legend moved below plotting region; maximum bar and relative-change labels remain inside plotting margin.
- Figure 4b: sham comparison remains readable as a secondary main/supplement candidate.

## Reproduction

The figure CI runs:

```bash
python scripts/build_paper_figures_h1_h5.py --output-dir <dir>
python scripts/polish_fig1_fig3_h1_h5.py --output-dir <dir>
python scripts/polish_fig4_h1_h5.py --output-dir <dir>
```

Primary machine-readable inputs:

- `results/findlay_camera_trap_real_data_v1.json`
- `results/findlay_position_standardized_distortion_summary_v1.json`
- `results/birdvox_protected_02_05_real_data_v1.json`
- `results/findlay_h5_transport_boundary_v1.json`
- `results/findlay_species_position_recovery_summary_v1.json`

Caption source: `FIGURE_CAPTIONS_H1_H5.md`.
