# REC reference-dark-mass boundary

Status: **working measurement boundary; not a novelty claim**.

## 1. REC does not observe the fundamentally unobservable

The project shorthand “shadow world” means **excluded from the tested scientific record**, not “invisible to every possible observer.”

A confirmatory REC analysis starts from a gate-independent exposure universe `Omega` and then separates three domains:

1. **reference-resolved record shadow** — the tested primary system excluded the exposure/record, but independent reference truth resolves the focal event;
2. **reference-unresolved shadow** — the exposure is known to exist, but available reference truth cannot resolve the focal event;
3. **outside `Omega`** — no frozen exposure opportunity was defined, so the study has no empirical denominator for that region.

Only domain 1 directly identifies hidden events. Domain 2 contributes uncertainty. Domain 3 is outside the empirical target population unless a new exposure design is defined prospectively.

## 2. State diagram

```text
biological world
    |
    v
master exposure universe Omega
    |
    +------------------------------ outside Omega
    |                               (not empirically enumerated)
    v
REC operational state: entered / acquisition shadow / gate shadow / archive shadow
    |
    v
independent reference process
    |
    +-- truth resolved ----------> positive / negative
    |
    +-- truth unresolved --------> reference-dark mass
```

The final branch must never be converted to negative truth by default.

## 3. Two different kinds of “not seen”

### Primary-system unseen

The tested observation system failed to create the target scientific record. This is the operational REC shadow.

It may still be independently observable by the reference design.

### Reference unresolved

The reference design cannot establish target truth for the frozen event/window definition.

This is epistemically different. REC cannot claim whether the event occurred without extra assumptions or additional measurement.

Therefore:

> **no primary record != no event, and no reference resolution != no event.**

## 4. Resolved-only estimates are conditional claims

For a shadow class `H`, a resolved-only estimate

`q_H,res = P(E=1 | H=1, reference truth resolved)`

is a claim about the reference-resolved subpopulation.

It is not automatically a claim about all `H` exposures when reference resolution is incomplete or condition dependent.

Every confirmatory result must therefore report the weighted unresolved fraction in the same denominator.

## 5. Worst/best-case bounds

Let, within shadow class `H`:

- `p_H`: weighted resolved positive truth;
- `n_H`: weighted resolved negative truth;
- `u_H`: weighted unresolved truth.

Without assuming anything about unresolved truth,

`P(E=1 | H)` lies in

`[ p_H / (p_H+n_H+u_H), (p_H+u_H) / (p_H+n_H+u_H) ]`.

REC reports these bounds rather than imputing `u_H` as negative.

For an absorption quantity `P(H | E=1)` with parent population `P`, lower and upper bounds assign unresolved truth adversarially across `H` and `P\H`:

- lower: unresolved `H` are negative, unresolved `P\H` are positive;
- upper: unresolved `H` are positive, unresolved `P\H` are negative.

These are identification bounds under binary unknown event status, not sampling-confidence intervals. Confirmatory sampling uncertainty must be added separately at the independent ecological-unit level.

## 6. Layer-specific denominators

Do not double-count upstream loss as downstream loss.

- **acquisition shadow**: primary acquisition unavailable;
- **gate-unevaluable shadow**: primary acquisition available, but gate cannot be evaluated;
- **gate shadow**: primary acquisition available, gate evaluable, registered deviation absent;
- **record-entry shadow**: operational record entry absent, regardless of which pre-entry stage caused it.

In particular, acquisition failure is not also counted as gate-unevaluable failure merely because the gate has no result.

## 7. Condition-dependent unresolved mass is itself a result

If reference-unresolved mass varies across habitat, time, illumination, occlusion or another frozen covariate, the reference process itself has a structured observation problem.

REC must then distinguish:

`ecological process -> primary record selection`

from

`ecological process -> reference resolvability`.

A strong claim about primary-system distortion requires either:

- sufficiently small/stable reference-unresolved mass;
- improved independent reference measurement;
- or explicit partial-identification/sensitivity analysis.

## 8. Outside-Omega boundary

REC cannot recover events from times/places for which the study never defined an exposure opportunity.

Examples:

- periods outside the fixed recording schedule;
- areas outside the defined sensor/reference field;
- event-triggered archives with no independent clock or reference denominator.

Those are not `negative`, `B`, or even `shadow` rows. They are outside the study universe.

This is why the REC foundational rule is:

> **Define exposure before defining non-detection.**

## 9. Executable implementation

`scripts/analyze_shadow_selection.py` reports:

- resolved-only layer-specific estimates;
- weighted reference-unresolved mass;
- worst/best-case identification bounds for event contamination and absorption;
- separate acquisition, gate-unevaluable, gate-baseline and no-entry layers.

The output bounds expose what the current reference design cannot determine. They do not make that hidden truth observable.
