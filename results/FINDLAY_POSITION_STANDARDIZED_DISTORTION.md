# Findlay H2→H3 position-standardized distortion result

Status: **mixed robustness result. Fox/badger species distortion is robust to CT-position standardization; otter wet/dry distortion is robust for A and BV but not BS.**

Pre-result specification: `PAPER_H2_H3_POSITION_STANDARDIZATION.md`.

GitHub Actions run: `33834478272`.

Artifact digest: `sha256:397c6e7edba906173f7d6738071a6785c4079115cc35d636487ec4896325d1b7`.

## Why this test matters

The pooled Findlay results compare biological composition before and after camera entry. Because biological states are not distributed identically among physical CT positions, a pooled composition change can combine two sources:

1. within-position differential entry;
2. changing representation of positions in the recorded world.

The frozen robustness test therefore compares truth and recorded composition within each CT position and then standardizes both worlds to the **same** position distribution. Two weighting schemes were frozen:

- equal weight per evaluable CT position;
- weights fixed from the reference-pass position distribution.

No row-level significance test is used because repeated passes are not independent biological individuals.

## Fox/badger species composition: robust

The wild fox/badger system retains the same direction after position standardization.

### Trigger stage

Equal-position weighting:

- standardized truth badger proportion: `0.367406`;
- standardized triggered badger proportion: `0.429819`;
- shift: `+0.062413`.

Reference-pass weighting:

- truth: `0.359818`;
- triggered: `0.413316`;
- shift: `+0.053498`.

Three of four physical positions individually show positive badger composition shifts and positive badger-minus-fox trigger-probability differences. `SF` is the adverse position.

### Final confirmed capture

Equal-position weighting:

- standardized truth badger proportion: `0.367406`;
- standardized captured badger proportion: `0.517249`;
- shift: `+0.149843`.

Reference-pass weighting:

- truth: `0.359818`;
- captured: `0.499712`;
- shift: `+0.139894`.

Again, three of four positions show positive shifts, with `SF` reversed.

### Interpretation

The pooled fox/badger species-composition result is therefore not produced merely by changing the mixture of CT positions. Species-selective entry persists when reference and recorded worlds are placed under the same position distribution.

This makes fox/badger species composition the strongest primary H2→H3 empirical endpoint.

## Otter wet/dry: heterogeneous after position standardization

### A camera

Wet underrepresentation is robust at every position.

Equal-position weighting:

- truth wet proportion: `0.416768`;
- triggered wet proportion: `0.289774`;
- shift: `-0.126993`.

Reference-pass weighting:

- truth: `0.438017`;
- triggered: `0.303196`;
- shift: `-0.134821`.

All `4/4` positions show negative wet composition shifts and negative wet-minus-dry trigger-probability differences.

### BV camera

Wet underrepresentation is also robust overall.

Equal-position weighting:

- truth: `0.424105`;
- triggered: `0.377735`;
- shift: `-0.046370`.

Reference-pass weighting:

- truth: `0.445833`;
- triggered: `0.393347`;
- shift: `-0.052487`.

Three of four positions show the negative direction.

### BS camera

The pooled wet-underrepresentation result does **not** survive position standardization.

Equal-position weighting:

- truth: `0.446979`;
- triggered: `0.450000`;
- shift: `+0.003021`.

Reference-pass weighting:

- truth: `0.459821`;
- triggered: `0.460714`;
- shift: `+0.000893`.

Only `2/4` positions show negative wet composition shifts; the other two show positive shifts. The within-position wet-minus-dry trigger-probability direction is likewise split `2/4` vs `2/4`.

### Interpretation

The original pooled BS wet/dry shift cannot be interpreted as a position-invariant wetness effect. Its pooled underrepresentation reflects, at least in part, how wet/dry passes and position-specific trigger performance combine across the observation layout.

The frozen all-three-camera robustness criterion therefore **fails**.

## Revised H2→H3 conclusion

The strongest paper-level statement is now:

> **Record-entry selection changes ecological composition, but the operating selection function can be observation-context specific. Fox/badger species distortion remains after CT-position standardization, whereas the wet/dry mechanism is strong for A and BV but not BS.**

This result strengthens the paper by separating a robust ecological estimand shift from a pooled association that partly depends on observation context.

It also aligns with the H5 transport results: the same observation context that determines whether entry selection is present also determines whether an entry correction can be transported.

## Manuscript consequence

- Promote **fox/badger species composition** to the primary Findlay H2→H3 endpoint.
- Use **otter A/BV wetness** as mechanistic corroboration.
- Report **BS as an adverse/aggregation-sensitive case**, not as a third clean replication.
- Do not retain the earlier wording that wet underrepresentation is a position-robust effect in all three camera model/settings.

## Hard boundaries

Do not claim:

- all three otter camera settings show position-standardized wet selection;
- CT positions are independent animals or population replicates;
- the position-standardized result establishes a causal species effect;
- the BS pooled wet/dry contrast has the same operating meaning as A/BV.
