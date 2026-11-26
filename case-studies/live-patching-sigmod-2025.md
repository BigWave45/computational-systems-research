# Case Study 01: Live Patching for Distributed In-Memory Key-Value Stores

## Audit status

**Reconnaissance only.** This is an initial inspection of the public paper and reproduction-package metadata. It is not a reproduction, independent verification of the results, or a completed claim-level audit.

## Identification

- Paper: Michael Fruth and Stefanie Scherzinger, *Live Patching for Distributed In-Memory Key-Value Stores*.
- Venue/version: Proceedings of the ACM on Management of Data, Volume 2, Issue 6 (2024); included in the SIGMOD 2025 reproducibility process.
- Paper DOI: https://doi.org/10.1145/3698816
- Reproduction package: https://github.com/sdbs-uni-p/sigmod25-distributed-imkvs-live-patching
- Data DOI: https://doi.org/10.5281/zenodo.13729902
- QEMU VM DOI: https://doi.org/10.5281/zenodo.13765240
- Official ARI results: https://reproducibility.sigmod.org/reports.html
- Official status shown: Results Reproduced; Artifacts Available; Artifacts Evaluated - Reusable.
- SIGMOD Best Artifact award: https://www.sigmod.org/sigmod-awards/sigmod-best-artifact-award/

## Candidate claim

The paper's abstract reports that live patching can update a Redis Cluster in memory without restarting nodes, and that in one scenario the whole cluster is updated orders of magnitude faster than conventional rolling updates without unfavorable trade-offs in throughput, tail latency or network consumption.

This is a broad abstract-level claim. The formal audit must select a narrower, table/figure-level proposition from the paper's experiments before assigning a verdict. No quantitative result is declared verified at this stage.

## Public artifact observations

The package README states:

1. The package includes reproduction instructions and scripts.
2. Reproduction requires a modified Linux kernel, pinned to commit `ecfcf9142ada6047b07643e9fa2afe439b69a5f0` in the `luhsra/linux-mmview` repository.
3. A preconfigured QEMU VM is supplied, but the authors caution that VM overhead may affect results and recommend direct server execution for more accurate reproduction.
4. Raw experiment data is 232 GB unpacked.
5. Transformed experiment data is 82 GB unpacked.
6. Most raw experiment data is transformed into DuckDB databases used for analysis and plotting; some data is used directly.
7. The README documents measurement-noise controls, including fixed CPU frequency, disabled Turbo Boost and Hyper-Threading, CPU pinning, and Redis configuration choices.
8. The README includes supplemental explanations and plots, including network-overhead results.

These are observations about what the package documentation declares. We have not downloaded or inspected the complete data, run the scripts, inspected every analysis file, or independently confirmed the declared setup.

## Initial claim-to-evidence graph

| Link | Public evidence located | Current assessment |
|---|---|---|
| Paper -> package | README names the paper and describes accompanying materials | Explicit |
| Package -> reproduction instructions | README links a reproduction directory | Explicit at documentation level; scripts not yet inspected |
| Reproduction -> kernel dependency | Exact kernel repository and commit are stated | Explicit |
| Reproduction -> VM | README identifies a QEMU image on Zenodo | Explicit; VM not downloaded or inspected |
| Reported results -> transformed data | README says transformed data is used for analysis and plotting | Explicit at documentation level; exact figure mapping still to be checked |
| Raw -> transformed data | README describes conversion to DuckDB for most experiments | Partial; transformation scripts and coverage not yet audited |
| Result -> execution logs/configuration | README describes selected setup and noise controls | Partial; completeness and run-to-result linkage not yet established |
| Artifact -> independent reproduction report | Official SIGMOD ARI page lists the reproduced badge; report metadata is identifiable | Committee outcome located; report content not yet inspected |

## Constraints discovered

- Storage burden: 232 GB unpacked raw data and 82 GB unpacked transformed data.
- Environment burden: modified Linux kernel and hardware-sensitive performance measurements.
- VM caveat: the authors explicitly warn that VM overhead can affect measurements.
- External dependency: the reproduction package depends on a separately maintained kernel repository and a pinned commit.
- License: the GitHub repository metadata identifies GPL-3.0. Confirm individual artifact/data licenses before redistribution or modification.

These constraints do not invalidate the paper or its reproduction status. They matter to the cost and portability of an independent claim-level audit.

## Next checks

1. Obtain the paper PDF and identify one specific central numerical claim, with page/table/figure reference.
2. Inspect the reproduction scripts and map the selected result to exact script, input and output paths.
3. Inspect the SIGMOD reproducibility report and compare the committee's scope with our claim-level evidence graph.
4. Inspect Zenodo metadata for data versions, sizes, checksums and license.
5. Determine whether the transformed dataset and plotting scripts permit deterministic recomputation of the selected statistic without downloading the full raw dataset.
6. Record the smallest feasible audit environment and whether it can be executed without a dedicated server.

## Current verdict

**NOT_CHECKED.** The initial reconnaissance confirms that a detailed public reproduction package is documented. It does not yet establish whether a selected central claim can be independently checked from the preserved artifacts without a full experiment rerun.
