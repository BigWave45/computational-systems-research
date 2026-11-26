# Pilot Corpus: Candidate Computational Claims

## Status

Provisional shortlist drawn from the official ACM SIGMOD 2025 Availability & Reproducibility Initiative (ARI) results page. The official page lists the selected papers as having Results Reproduced, Artifacts Available, and Artifacts Evaluated - Reusable badges. This is the committee's reported status, not a finding from our own audit.

Official source:
- https://reproducibility.sigmod.org/reports.html

## Candidate cases

| # | Paper | Candidate claim class | Audit interest |
|---|---|---|---|
| 1 | Live Patching for Distributed In-Memory Key-Value Stores | Distributed systems performance and correctness | Large raw/transformed data, custom kernel, VM and hardware sensitivity. |
| 2 | CRDV: Conflict-free Replicated Data Views | Replicated data / consistency | Separate formal convergence claims from implementation and experimental evidence. |
| 3 | InTime: Towards Performance Predictability In Byzantine Fault Tolerant Proof-of-Stake Consensus | Distributed consensus performance | Trace performance-predictability claims to workloads, configurations and output. |
| 4 | H-Rocks: CPU-GPU accelerated Heterogeneous RocksDB on Persistent Memory | Heterogeneous systems performance | Hardware, memory configuration and workload provenance may be material. |
| 5 | HotStuff-1: Linear Consensus with One-Phase Speculation | Consensus protocol performance | Distinguish theoretical properties from empirical latency/throughput results. |
| 6 | Memento Filter: A Fast, Dynamic, and Robust Range Filter | Data structure performance | Trace benchmark comparisons and workload assumptions. |
| 7 | An Elephant Under the Microscope: Analyzing the Interaction of Optimizer Components in PostgreSQL | Database optimizer evaluation | Trace optimizer configuration, query workloads and measured effects. |
| 8 | Disco: A Compact Index for LSM-trees | Storage/index performance | Trace space/performance claims to data, configuration and result artifacts. |
| 9 | Constant Optimization Driven Database System Testing | Database testing | Trace bug-detection and coverage claims to test cases and database versions. |
| 10 | Are Database System Researchers Making Correct Assumptions about Transaction Workloads? | Empirical workload characterization | Trace dataset provenance, sampling, transformations and statistical claims. |

All ten titles appear on the official SIGMOD 2025 ARI results page. The first case is selected for initial inspection because its reproduction package is publicly documented and its artifact award provides an unusually strong baseline.

## Sampling caveat

This is a deliberately high-artifact-quality, positive-outcome cohort. It is useful for asking whether claim-level inspection reveals evidence limitations even after formal artifact evaluation and reproduction. It cannot estimate how often computational papers generally are independently verifiable.

The shortlist is not yet the final ten-case dataset. Each case must pass a paper/version check, public artifact access check, claim isolation check, and lawful inspection check. Exclusions must be logged rather than silently replaced.

## Selection and analysis rule

For each case:
1. Freeze the paper version, artifact repository commit and external data versions.
2. Record the official ARI verdict and obtain the report if publicly accessible.
3. Select one central claim tied to a table, figure, theorem or quantitative result.
4. Build the claim-to-evidence graph using the protocol in `claim-evidence-audit-protocol.md`.
5. Record which evidence links are explicit, inferred, inaccessible or absent.
6. Compare our observations with the committee report. The report is a comparison source, not infallible ground truth.
7. Record auditor time, required compute/storage, access constraints and unresolved uncertainty.

## No claims yet

No case in this shortlist has been fully audited under our protocol. The first-case reconnaissance is recorded separately in `case-studies/live-patching-sigmod-2025.md`. No conclusion about the correctness of any paper is being made.
