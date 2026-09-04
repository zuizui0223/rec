# Third-party data rights audit — REC H1–H5

Status: **BirdVox clear; Findlay reuse permission/licence clarification recommended before journal submission.**

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

- public GitHub repository `melaniefindlay/CT-Detection`;
- exact analysis commit `abc72f535bb59ebed202fb7acca852fc1647e97a`;
- source files are downloaded and hash-verified by the REC workflows.

GitHub repository metadata currently reports:

`license: null`.

The repository being publicly readable does not itself supply an explicit open-data/software licence. The current audit therefore does **not** establish that the data are published for unrestricted reuse under a standard licence.

Submission implication:

Methods in Ecology and Evolution asks authors to confirm that third-party datasets are either publicly available for unrestricted reuse or that permission for reuse has been obtained from the data owners. On the present evidence, it would be unsafe to make the unrestricted-reuse declaration solely from the public GitHub location.

Recommended action before MEE submission:

1. contact the Findlay data owner/corresponding author;
2. describe the files and exact public repository/commit being reanalysed;
3. request written confirmation that reuse in this reanalysis and publication of derived numerical summaries/figures is permitted;
4. ask how the data source should be cited/acknowledged and whether a preferred licence applies;
5. archive the permission email with the project submission records.

Status: **permission/licence clarification pending.**

## Important distinction

The REC repository does not need to redistribute the original Findlay CSV files in order to reproduce the analysis: CI downloads them from their original public location and verifies their Git blob identity. Nevertheless, journal third-party-data declarations concern rights to reuse the source data in the research, not only whether the raw bytes are republished in our repository.

## REC repository code

Separately, the REC repository currently has no root open-source `LICENSE` file. MEE's code policy requires code submitted with the manuscript to have an open-source licence.

This is a separate decision from third-party dataset rights:

- Findlay/BirdVox licences govern source data;
- the REC repository licence governs our analysis/code reuse.

Do not add a software licence without an explicit author choice.
