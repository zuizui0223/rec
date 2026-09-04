# Third-party data rights audit — REC H1–H5

Status: **BirdVox clear; Findlay article is CC BY 4.0 and explicitly links the GitHub datasets as online resources, but repository-level licence clarification remains prudent before journal submission.**

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

- Findlay, Briers & White (2020), *Mammal Research* 65:167–180;
- public GitHub repository `melaniefindlay/CT-Detection`;
- exact REC analysis commit `abc72f535bb59ebed202fb7acca852fc1647e97a`;
- source files are downloaded and hash-verified by the REC workflows.

### Evidence supporting reuse

The Findlay article is published open access under **CC BY 4.0**. The publisher page explicitly states under Electronic Supplementary Material / Online resources that:

> the R file and datasets are available at the `melaniefindlay/CT-Detection` GitHub repository.

This strongly supports the interpretation that the repository is the authors' intended public research-data resource associated with the open-access article.

### Remaining ambiguity

GitHub repository metadata itself currently reports:

`license: null`.

Thus the repository does not independently display a machine-readable or root-file data/software licence. The publisher's CC BY statement clearly covers the article and material included under that licence, but the current audit does not attempt to give a legal ruling on whether every externally linked GitHub file inherits the article licence automatically.

### Submission implication

Methods in Ecology and Evolution asks authors to confirm that third-party datasets are either publicly available for unrestricted reuse or that permission for reuse has been obtained from the data owners.

The evidence is now stronger than public-GitHub availability alone because the CC BY article explicitly designates the repository as its online data resource. Nevertheless, the lowest-risk submission route is still to obtain a short written confirmation from the corresponding/data author that reuse of the linked CSV files in a methodological reanalysis and publication of derived summaries/figures is permitted.

Recommended action before MEE full submission:

1. contact the Findlay data owner/corresponding author;
2. identify the paper, public repository and exact two CSV files;
3. request confirmation that reanalysis and publication of derived numerical summaries/figures are permitted;
4. ask whether the authors consider the linked datasets covered by the article's CC BY 4.0 licence or prefer another citation/licence statement;
5. archive the confirmation with submission records.

Status: **strong public-reuse evidence; written clarification still recommended for submission certainty.**

## Important distinction

The REC repository does not redistribute the original Findlay CSV files. CI downloads them from the authors' original public repository and verifies Git blob identities. Nevertheless, third-party-data declarations concern rights to use the data in research, not only redistribution of raw files.

## REC repository code

Separately, the REC repository currently has no root open-source `LICENSE` file. MEE's code policy requires code submitted with the manuscript to have an open-source licence.

This is a separate decision from third-party dataset rights:

- Findlay/BirdVox terms govern source data;
- the REC repository licence governs our analysis/code reuse.

Do not add a software licence without an explicit author choice.
