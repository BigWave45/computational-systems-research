# Pilot Corpus: Candidate Computational Claims

## Status

Provisional shortlist, not yet the final sample. All ten candidates below appear on the official ACM SIGMOD 2025 Availability & Reproducibility Initiative page as papers awarded the Results Reproduced, Artifacts Available, and Artifacts Evaluated - Reusable badges. The official page reports the badge status; it does not, by itself, establish that our independent audit has checked the artifacts.

Official sources:
- SIGMOD 2025 badge and report listing: https://reproducibility.sigmod.org/reports.html
- SIGMOD 2025 reproducibility reports proceedings: https://doi.org/10.1145/3785021
- SIGMOD ARI process and criteria: https://reproducibility.sigmod.org/

## Candidate cases

| # | Paper | Candidate claim class | Why include it |
|---|---|---|---|
| 1 | Live Patching for Distributed In-Memory Key-Value Stores | Distributed systems performance and correctness | Dynamic patching claims may depend on workload, failure and latency evidence. |
| 2 | CRDV: Conflict-free Replicated Data Views | Replicated data / consistency | Useful for tracing formal properties and experimental evidence separately. |
| 3 | InTime: Towards Performance Predictability In Byzantine Fault Tolerant Proof-of-Stake Consensus | Distributed consensus performance | Tests whether performance-predictability claims are linked to workload and configuration evidence. |
| 4 | HotStuff-1: Linear Consensus with One-Phase Speculation | Consensus protocol performance | A distinct consensus design with claims that may combine theoretical and empirical support. |
| 5 | H-Rocks: CPU-GPU accelerated Heterogeneous RocksDB on Persistent Memory | Heterogeneous systems performance | Hardware, memory configuration and workload provenance are likely material. |
| 6 | Constant Optimization Driven Database System Testing | Testing / optimization | Allows inspection of whether test-generation and bug-detection claims map to evidence. |
| 7 | Fast and Scalable Data Transfer Across Data Systems | Data movement performance | Useful for checking benchmark definitions, system configurations and measured throughput. |
| 8 | Online Marketplace: A Benchmark for Data Management in Microservices | Benchmark validity and coverage | Tests whether benchmark claims are supported by workload definitions and artifact contents. |
| 9 | Self-Enhancing Video Data Management System for Compositional Events with Large Language Models | LLM-enabled system evaluation | Prompts, model versions, output traces and evaluation criteria may be important evidence. |
| 10 | Are Database System Researchers Making Correct Assumptions about Transaction Workloads? | Empirical workload characterization | Tests source-data provenance, sampling and statistical claim traceability. |

## Sampling caveat

This is a deliberately high-artifact-quality, positive-outcome cohort. It is useful for testing whether an evidence audit can find limitations even in papers that passed a formal reproducibility process. It cannot estimate how often computational papers are independently verifiable.

The official SIGMOD 2025 proceedings report states that 107 of 250 papers submitted artifacts, 50 targeted the Results Reproduced badge, and 35 were judged fully reproducible. This gives a possible later comparison group, but the ten-case pilot should not be presented as representative of all SIGMOD papers.

## Selection rule for the final ten

Before finalizing:
1. Confirm the full paper and artifact package for each candidate.
2. Confirm that the selected claim can be isolated and tied to a result location.
3. Confirm that the artifacts are publicly accessible and lawful to inspect.
4. Obtain the official reproducibility report where available.
5. Replace any case that fails these checks, documenting the exclusion.
6. For a stronger follow-up sample, add a comparison stratum of artifact-available papers that did not receive a Results Reproduced badge. Do not mix the strata without recording them.

## No claims yet

No artifact has been independently audited under this protocol. No conclusion about the correctness, reproducibility, or evidence quality of these papers is being made here.
