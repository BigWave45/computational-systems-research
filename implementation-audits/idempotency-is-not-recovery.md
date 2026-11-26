# Artifact Audit: Idempotency Is Not Recovery

**Paper:** Song Xu, *Idempotency Is Not Recovery: A Fault-Injection Study of Language-Model Agent Tool Actions*  
**Preprint:** https://arxiv.org/abs/2611.23353  
**Audit date:** 2026-11-26  
**Audit status:** public artifact availability checked; full reproduction blocked

## 1. Question

Can an independent researcher obtain the materials needed to reproduce the paper's reported fault-injection experiments?

## 2. Publicly available material

The public preprint and third-party indexed copies expose the paper's description of its runtime, fault classes, configurations, reported results, and limitations.

The paper's data/code availability statement says that only the manuscript is deposited with the preprint. It states that aggregate analysis tables, experimental code, full original records, and the execution environment are not publicly deposited, and that access is subject to author authorization and privacy review.

A third-party index surfaces DOI https://doi.org/10.5281/zenodo.24268830 as a related citation. This audit has not verified that DOI's contents or established that it contains the paper's code, data, or execution environment. Do not treat the DOI as a reproducibility artifact until its record and files are inspected directly.

## 3. Reproduction decision

**Decision: do not claim an independent reproduction is currently possible from public materials.**

The manuscript alone does not provide the executable runtime, complete trial-level records, aggregate analysis tables, and environment needed to verify the reported results. A prose reconstruction would be a new implementation of the described design, not a reproduction of the authors' implementation.

## 4. What can be assessed from the paper

The paper reports a controlled study combining authorization, a durable action ledger, target-side idempotency, reconciliation, and evidence sealing. It describes ten single-host fault classes, four configurations, and three ablations. The abstract reports 7,513 trials per platform, using 96 captured model responses from 24 constructed cases.

The reported results include:
- 0/200 repeated effects for the full configuration in known original crash/replay pairs, compared with 117/200 for each simpler baseline;
- 100/100 ambiguous outcomes when reconciliation was disabled in a known post-effect crash comparison;
- approximately one-seventh the fail-open throughput for the full runtime;
- 75/100 unresolved trials per platform under injected evidence-write faults.

These are author-reported findings, not independently reproduced measurements.

## 5. Limitations relevant to a follow-up study

The paper itself bounds its evidence to one runtime, a controlled target, reused inputs, and single-host faults. Its two operating systems demonstrate consistency of one implementation across environments; they are not independent replications of the research.

The paper identifies multi-host deployments, production targets, independently sampled cases, and policies for handling evidence-write failures as directions for future investigation.

These limitations are not automatically research gaps. They must be compared against prior work in distributed systems and fault-tolerant services before a follow-up question is selected.

## 6. What would be needed from the authors

A meaningful reproduction request should seek:
1. Exact source repository or archived source bundle and commit.
2. Full trial-level records, with sensitive fields removed or safely transformed.
3. Aggregate analysis tables and analysis scripts.
4. Fault-injection scripts, schedules, and fault-activation receipts.
5. Exact runtime, dependency, and operating-system versions.
6. Configuration files and captured proposal/input corpus, with provenance and reuse permissions.
7. Instructions for rebuilding the target-side oracle and validating its independence from the runtime ledger.
8. The pre-specified analysis plan and any post-hoc analyses clearly distinguished.

If these materials cannot be shared, a researcher may still implement a separately specified conceptual replication, but must label it as an independent implementation and must not claim to have reproduced the authors' numerical results.

## 7. Research decision

The proposed full reproduction is blocked pending artifact access. Do not build an agent framework around this paper yet.

The next defensible action is to inspect the paper's complete methods and related work, verify the surfaced Zenodo record directly, and determine whether the authors provide an accessible artifact elsewhere. In parallel, map established distributed-systems literature on idempotency, transactional outbox, write-ahead logging, crash consistency, sagas, and reconciliation.

Only after that review should we decide whether an independently implemented multi-service experiment tests a meaningful unresolved assumption.

## 8. Evidence classification

- Paper existence and abstract: publicly discoverable.
- Experimental design and reported counts: author-reported in manuscript.
- Code and raw data availability: manuscript states these are not publicly deposited with the preprint.
- Zenodo DOI contents: not yet verified.
- Independent reproduction: not performed.
- Independent extension: not designed or performed.
