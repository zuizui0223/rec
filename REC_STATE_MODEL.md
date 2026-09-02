# REC state model — recorded, shadow, and unresolved worlds

Status: **working design contract; not a novelty claim**.

## 1. Why “unobservable world” is too strong

REC does not claim access to a fundamentally unobservable biological world. Empirical claims require some independently justified reference or exposure design.

REC therefore separates three domains:

1. **recorded world** — the tested primary system produces an entered scientific record;
2. **reference-observable shadow world** — the primary system does not produce the relevant record, but an independent reference design can establish exposure/event truth;
3. **reference-unresolved world** — neither the tested primary system nor the available reference design resolves the biological event sufficiently for the target claim.

The third domain is not converted to biological absence.

## 2. Master exposure universe

Let `Omega` be the set of exposure opportunities generated independently of the tested record-entry rule.

For each `i in Omega` define:

- `A_i`: primary acquisition available/evaluable;
- `R_i`: registered-deviation gate result when evaluable;
- `K_i`: operational record entry/archive present;
- `E_i`: independent biological event truth (`1`, `0`, unresolved);
- `D_i`: semantic observation state after entry, where defined;
- `Y_i`: later coarsened output.

A useful sequence is:

```text
exposure Omega
    |
    +--> primary acquisition A
            |
            +-- unavailable ------------------------> acquisition shadow
            |
            +-- available --> gate R
                              |
                              +-- no deviation ------> gate shadow / registered B
                              |
                              +-- deviation --> entry K
                                               |
                                               +-- no entry --> archive shadow
                                               |
                                               +-- entry --> TNOA semantic world
```

The exact state machine varies by sensor architecture. A fixed-schedule system may archive baseline windows even when `R=0`; an event-triggered system may create no record at all. REC records the actual architecture rather than forcing one pattern.

## 3. Four operational pre-TNOA states

At minimum distinguish:

### A. Acquisition shadow

The exposure opportunity exists in `Omega`, but the primary stream needed for the tested observation is unavailable or not evaluable.

Examples: hardware outage, missing frame/audio block, corrupted primary file, acquisition disabled under a frozen schedule.

This is **not** a threshold miss because no valid gate evaluation exists.

### B. Gate shadow

Primary evidence is available and the gate is evaluable, but no registered deviation occurs.

If independent truth gives `E=1`, this is a gate-absorbed event.

### C. Archive shadow

A deviation was registered or a record should otherwise have entered, but no operational scientific record exists because of downstream storage/archive/policy loss.

### D. Entered world

A record enters the scientific dataset. TNOA then governs semantic preservation inside that entered record.

## 4. Truth status crosses every operational state

Each operational state may pair with:

- `E=1`: independently verified event;
- `E=0`: independently verified no-event for the frozen exposure definition;
- `E=?`: reference unresolved.

Therefore:

- acquisition shadow != no-event;
- gate shadow != no-event;
- archive shadow != no-event;
- entered baseline != biological absence;
- reference unresolved != negative truth.

## 5. REC estimands by loss layer

### Acquisition loss

`a_A = P(A=0 | E=1, truth resolved)`.

### Gate absorption

Conditional on acquisition/gate evaluability:

`a_R = P(R=0 | E=1, A=1, gate evaluable, truth resolved)`.

### Record non-entry

`a_K = P(K=0 | E=1, truth resolved)`.

### Shadow contamination

For an explicitly defined shadow set `H`:

`q_H = P(E=1 | H=1, truth resolved)`.

Always name the denominator: acquisition shadow, gate shadow, archive shadow, or their prespecified union.

## 6. Unresolved mass must be reported

For any REC estimand report the fraction of target exposures whose reference truth remains unresolved.

If unresolved mass is large or condition dependent, point estimates over resolved truth alone may not represent the entire exposure universe. REC must then either:

- restrict its claim to the reference-resolved subpopulation;
- provide explicit sensitivity/partial-identification bounds;
- improve the reference design before confirmatory inference.

Do not impute unresolved truth as no-event by default.

## 7. Relationship to TNOA

TNOA and REC meet at record entry.

```text
physical/ecological world
        |
        v
exposure universe Omega
        |
        v
REC: acquisition / gate / archive selection
        |
        v
entered record
        |
        v
TNOA: target / nuisance / observability / attribution semantics
        |
        v
later coarsening and ecological inference
```

The mirror principle is:

- **REC:** no record != no event.
- **TNOA:** not-target / low support != biological absence.

## 8. What REC can and cannot learn

REC can learn about the shadow world only to the extent that exposure accounting and independent reference truth make it observable.

REC cannot empirically identify events that are invisible to both the primary and reference systems without additional assumptions.

Therefore the strongest safe framing is:

> **REC studies the world excluded from the tested scientific record, insofar as that exclusion can be audited against an independently defined exposure universe and reference observation process.**
