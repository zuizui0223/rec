# Third-party data rights audit — REC H1–H5 / M4

Status: **BirdVox clear; Findlay article is CC BY 4.0 and explicitly identifies the public GitHub repository as the online resource for its R file and datasets. Repository-level licensing remains ambiguous, so raw-file redistribution stays blocked pending clarification.**

This is a submission-governance note, not legal advice.

## BirdVox-full-night

Source:

- Zenodo record `1205569`, BirdVox-full-night v3.0.

The Zenodo record explicitly states that the dataset is offered under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** licence.

Submission implication:

- reuse, analysis and redistribution are permitted subject to attribution under the licence terms;
- cite the BirdVox dataset/paper and retain the licence acknowledgement in Data Availability / Data Sources.

Status: **clear for reuse with attribution.**

## Findlay CT-Detection

Source:

- Findlay, Briers & White (2020), *Mammal Research* 65:167–180, DOI `10.1007/s13364-020-00478-y`;
- public GitHub repository `melaniefindlay/CT-Detection`;
- exact REC analysis commit `abc72f535bb59ebed202fb7acca852fc1647e97a`;
- source files are downloaded and hash-verified by the REC workflows.

### Evidence supporting methodological reanalysis

The publisher page for the Findlay article states that the article is open access under **CC BY 4.0**. It also explicitly identifies the GitHub repository as the paper's online resource and says that the R file and datasets are available there.

This is stronger evidence than public-GitHub visibility alone: the source article itself designates `melaniefindlay/CT-Detection` as the associated research-data/code location.

The Edinburgh Napier institutional repository independently records the same article as CC BY 4.0 and links the publisher licence.

### Remaining ambiguity

The GitHub repository itself does not currently display a root licence / machine-readable GitHub licence. Therefore this audit does **not** make the legal inference that every externally linked GitHub file automatically inherits the article licence.

That distinction matters most for **redistribution of the original repository files**. M4 does not need to redistribute those CSV files in order to report the reanalysis: the original public repository can remain the source location, while our code downloads the pinned files and verifies their identities.

### M4 submission implication

For the current `V3 + REC -> Ecological Informatics` route:

- the Findlay analysis is **not treated as a missing scientific-validation blocker**;
- the source paper and associated online-data location are public and citable;
- derived numerical summaries, figures, code and provenance can be prepared while the final rights wording is clarified;
- **do not redistribute the original Findlay CSV files inside our public or anonymous reviewer archive unless the data owner confirms the terms or an explicit repository/data licence is established**;
- use download/reproduction instructions that obtain the source files from the authors' repository and verify the frozen commit/blob identities.

A short written confirmation from the corresponding/data author remains the lowest-risk way to remove the residual repository-level ambiguity. The existing request draft is `FINDLAY_REUSE_PERMISSION_REQUEST_DRAFT.md`.

Recommended confirmation request:

1. permission to analyse `REGISTRATION_FOX_BADGER.csv` and `TRIGGER_OTTER_WET.DRY.csv` for the methodological reanalysis;
2. permission to publish derived numerical summaries and figures;
3. permission to provide reproducible code that downloads the original data from the authors' public repository without republishing the source CSV files;
4. preferred data citation/licence wording.

Status: **reanalysis/publication preparation may proceed; original-file redistribution remains fail-closed pending repository-level rights clarification.**

## Important distinction

The REC/M4 analysis does not claim ownership of the original camera-trap datasets or the original detection-process findings. Findlay et al. remain the source owners of the camera-trap/CCTV design and original data. M4 owns only the declared reanalysis questions and derived results.

## REC repository code

Separately, repository-level software licensing for our own analysis code should be resolved before a permanent public version-of-record software archive is fixed. This is independent of Findlay/BirdVox data rights.

Do not add a software licence without an explicit author choice.
