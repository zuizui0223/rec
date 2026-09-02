# REC world partition — recorded versus reference-resolvable

Status: **working operational taxonomy; not a novelty claim**.

## Core 2×2

Within the frozen master exposure universe `Omega`, REC separates the tested primary record-entry process from the independent reference process.

For a probability-sampled reference audit:

| | Reference truth resolved | Reference truth unresolved |
| --- | --- | --- |
| **Primary record entered** | entered / truth-resolved world | entered / reference-dark world |
| **Primary record absent** | **REC recoverable shadow** | **REC dark shadow** |

Two additional bookkeeping states remain necessary:

- **reference not sampled / not audited** — not negative truth;
- **outside `Omega`** — outside the empirical study universe, not a shadow row.

## Interpretation

### REC recoverable shadow

The tested primary record is absent (`K=0`), but independent reference truth resolves the frozen biological event.

This is where REC can directly measure hidden event prevalence and record-entry selection.

### REC dark shadow

The tested primary record is absent and the sampled reference process remains unresolved.

REC cannot state whether an event occurred. This mass contributes partial-identification width or motivates a better reference design.

### Entered / reference-dark world

A primary scientific record exists, but the independent reference audit cannot resolve the biological truth. Entry into the dataset does not guarantee biological truth resolution.

## Why the axes must remain separate

`record_entry_present` describes the tested scientific pipeline.

`reference truth resolved/unresolved` describes the independent audit process.

Conflating them causes two symmetric errors:

- no primary record -> no event;
- reference unresolved -> no event.

REC prohibits both.

## Executable partition

```bash
python scripts/analyze_world_partition.py \
  examples/exposure_ledger.csv \
  examples/chapter2_windows.csv
```

The analyzer reports raw exposure counts and design-weighted audited counts for the record/reference partition. It treats missing or unsampled reference truth as `not_audited` / `not_sampled`, never as negative truth.

For event-prevalence bounds within reference-unresolved shadow, use `scripts/analyze_shadow_selection.py`, which reports resolved-only estimates plus worst/best-case identification bounds.

## Relationship to the project shorthand “unobservable world”

The phrase is useful only if qualified:

> **REC studies what is unobserved by the tested record-entry system, while explicitly marking what is also unresolved by the independent reference process.**

It does not claim access to events outside `Omega` or events invisible to every available measurement system.
