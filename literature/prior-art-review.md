# Prior-Art Review: Computational Claim Verification

## Assessment

The broad question "Can a published computational claim be independently verified from public evidence without rerunning the full experiment?" is not novel on its own. Closely related methods and institutional processes already exist.

## Directly relevant work

### Evidence-Ready Experiments for Verifiable LLM Pipelines

A 2026 empirical software engineering paper proposes an artifact boundary for post-hoc verification of LLM pipelines without mandatory model re-execution. Its five hooks cover configuration integrity, prompt traceability, log completeness, deterministic processing and metric recomputation. It is a direct overlap with the proposed evidence-centric audit idea.

Source: https://ppee.unb.br/wp-content/uploads/2026/06/SBES2026___A_Blueprint_for_Evidence_Ready_Experiments_in_Verifiable_LLM_Based_Analysis_Pipelines__A_Case_Study_in_Source_Code_Pri.pdf

### AuditOwl: Evaluating the evidence trace of NeurIPS 2025 contributions with agentic code auditing

A 2026 manuscript under review proposes an agentic pipeline to compare paper claims against code repositories. It reports an audit of 100 NeurIPS 2025 empirical papers. It is a direct overlap with automated claim-to-code auditing. Its status is under review in the surfaced manuscript, so reported results should be treated as author-reported, not established consensus.

Source: https://openreview.net/pdf?id=xjCJY8Xxcm

### Computational reproducibility in computational social science

Schoch et al. (2024) argue for a tiered definition of computational reproducibility that explicitly accounts for who performs verification and which computational environment is available. The paper also discusses external dependencies, API reliance and computational literacy as barriers.

Source: https://doi.org/10.1140/epjds/s13688-024-00514-w

### ACM SIGMOD Availability & Reproducibility Initiative

SIGMOD's established process evaluates artifact availability, functionality and reproduction of central results. Its criteria include code/configuration/build environment, input data, experiment setup, scripts and transformation of raw data into paper figures. Independent reviewers produce reports and badges.

Sources:
- https://reproducibility.sigmod.org/
- https://reproducibility.sigmod.org/reports.html
- https://doi.org/10.1145/3785021

### Other established standards

- Center for Open Science TOP Guidelines distinguish computational reproducibility from replication and define independent verification practices: https://www.cos.io/initiatives/top-guidelines
- ACM SIGMOD's artifact criteria require evidence that central claims are supported by experiments: https://reproducibility.sigmodconf.hosting.acm.org/
- Nature's Machine Learning Checklist covers code, data and reproducibility reporting: https://www.nature.com/documents/machine-learning-checklist.pdf

## What remains unestablished

The existence of prior art does not prove that every useful question is closed. But the current broad framing is too close to existing work to justify a novelty claim.

A potentially narrower empirical question is:

**When a computational paper has already passed an independent artifact-reproduction process, what additional claim-level evidence gaps, scope mismatches, or unverifiable assumptions remain detectable through a structured post-hoc audit that does not rerun the full experiment?**

This is only a candidate. The SIGMOD 2025 pilot cohort can test it descriptively. A contribution would require showing that the audit finds material information not captured by the existing review reports, or that it does so with a demonstrable cost or coverage advantage. If it merely restates the committee's findings, it is not a research contribution.

## Decision

Proceed only with a small exploratory pilot. Do not describe the audit checklist, claim-evidence graph, or no-rerun verification idea as novel. Reassess after the ten cases and after reading the full related work of the closest papers.
