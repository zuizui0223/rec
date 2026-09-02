# External data audit notes

## Findlay CT-Detection

Public repository confirmed: `melaniefindlay/CT-Detection`.

Released materials include:

- R analysis code;
- trigger datasets for fox/badger and otter;
- registration datasets for fox/badger and otter;
- wet/dry otter trigger dataset.

The trigger tables are event-conditioned on independently observed animal passes and contain trigger outcome plus covariates such as distance, gait/orientation and camera identity. This is suitable for reproducing event-conditioned trigger loss, not for estimating a complete time-denominator `P(event | no record)`.

## BirdVox-full-night

Continuous recordings from six sensors, about 62 hours total, with 35,402 expert flight-call annotations. This provides a natural time-domain exposure denominator for an algorithmic gate experiment.

The expert annotations are independent of a future tested detector but use the same recorded audio. Therefore they validate algorithmic record-entry censoring after acquisition, not physical microphone misses.

## WABAD

Large expert-annotated multi-site acoustic collection. Potential generalization resource, but released-file selection/sampling provenance must be audited before treating it as a population exposure denominator.

## Snapshot Serengeti

Large event-triggered image archive with expert truth resources. Strong for post-entry semantic/classification work; structurally weak for REC shadow identification because non-triggered animal passes have no row unless an independent exposure/reference process is added.
