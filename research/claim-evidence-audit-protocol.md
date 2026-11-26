# Claim-to-Evidence Audit Protocol (Pilot v0.1)

## Status

Exploratory protocol. This is a pilot method for investigating published computational claims, not a claim of methodological novelty. It is not a reproduction protocol and does not certify the scientific truth of a paper.

## 1. Purpose

Test whether a reviewer can trace a narrowly stated computational claim to inspectable evidence in a public research artifact package without rerunning the full experiment.

The pilot asks:

1. Can the claim be stated precisely enough to check?
2. Can the evidence required to support it be located?
3. Can the evidence be linked to the exact reported table, figure, or statistic?
4. Which parts can be checked mechanically without rerunning the main experiment?
5. Which uncertainties remain after the audit?

## 2. Unit of analysis

The unit is one **claim**, not one paper or repository.

For each paper, select one central quantitative or algorithmic claim that is:
- explicitly stated in the paper;
- tied to a table, figure, theorem, benchmark result, or measured outcome;
- important to the paper's stated contribution;
- potentially checkable from its public artifacts.

Do not select a claim merely because it is easy to verify. Record why it is central.

## 3. Evidence model

Represent the claim as a directed evidence chain:

Claim -> reported result -> analysis procedure -> raw or intermediate output -> execution configuration -> code -> input data / workload.

Add environment, model/checkpoint, random seed, hardware, external API, and version dependencies when relevant.

For every node, record:
- exact artifact name and stable URL;
- version, commit, DOI, or content hash where available;
- access status;
- license or access restriction where relevant;
- whether the paper explicitly links it to the claim;
- whether the auditor inferred the relationship.

For every edge, record the evidence that justifies the connection. A repository existing is not evidence that it generated a particular table.

## 4. Audit dimensions

Score each dimension using:
- 0 = absent or contradicted;
- 1 = partial, ambiguous, or manually inferred;
- 2 = explicit and inspectable;
- N/A = genuinely not applicable, with explanation.

Dimensions:

A. Claim precision: operational definition, units, comparison, population/workload, and scope are clear.

B. Input provenance: dataset/workload identity, version, source, preprocessing and splits can be established.

C. Method traceability: relevant code, algorithm, parameters and analysis steps are identifiable.

D. Configuration integrity: versions, seeds, model/checkpoint, hardware and other outcome-relevant settings are recorded.

E. Execution evidence: logs, traces, intermediate outputs or run manifests connect the declared procedure to the reported run.

F. Result linkage: the paper's table/figure/statistic can be mapped to a specific output artifact.

G. Independent checkability: at least one material part of the claim can be checked from the artifacts without rerunning the full experiment.

H. Scope alignment: the evidence supports the breadth and wording of the claim, rather than only a narrower result.

Do not collapse the dimensions into a single opaque score. Report the vector and explain any weighting if a composite is later tested.

## 5. Permitted checks

Classify every check as one of:

1. **Metadata check** — inspect repository, versions, licenses, file manifests and documentation.
2. **Static trace check** — inspect code and scripts to establish whether the described procedure appears to be implemented.
3. **Integrity check** — verify hashes, signatures, immutable versions or manifest consistency.
4. **Deterministic recomputation** — recompute a statistic, aggregate, table, or figure from preserved outputs or data where feasible.
5. **Bounded execution** — run a small smoke test or a subset, explicitly not a full reproduction.
6. **Full reproduction** — rerun the full experiment. This is outside the core pilot and must be labelled separately.

Never describe static inspection or a bounded execution as reproduction of the paper.

## 6. Verdicts

Assign one verdict to the selected claim:

- **SUPPORTED_WITHIN_SCOPE**: inspected evidence supports the precisely stated claim within its declared scope.
- **CONTRADICTED**: inspected evidence conflicts with a material part of the claim.
- **INDETERMINATE**: evidence is missing, inaccessible, ambiguous, or insufficient to decide.
- **NOT_CHECKED**: the audit did not attempt the relevant check.

A verdict is about the evidence available to the auditor, not a declaration that the paper is true or false. A missing artifact is not proof that the reported result is false.

## 7. Discrepancy register

For each discrepancy, record:
- ID;
- claim text and location;
- artifact and exact location;
- expected relationship;
- observed relationship;
- severity: blocking, material, minor, or documentation-only;
- confidence: high, medium, or low;
- whether the discrepancy was directly observed or inferred;
- what additional evidence would resolve it.

Do not call a difference a bug unless its effect is demonstrated.

## 8. Procedure

1. Freeze the paper version, repository commit and artifact versions.
2. Extract the central claim verbatim and rewrite it as a checkable proposition without changing its scope.
3. Identify the result location in the paper.
4. Build the claim-to-evidence graph.
5. Run the permitted checks in increasing order of cost.
6. Record all failed, blocked and successful checks.
7. Assign the verdict and explain uncertainty.
8. Compare the audit with any independent artifact-evaluation report, but do not treat the report as infallible ground truth.
9. Record time spent by stage.
10. Preserve an audit log sufficient for another reviewer to inspect the reasoning.

## 9. Pilot measurements

Report, at minimum:
- claim trace coverage: proportion of required evidence links explicitly established;
- evidence completeness by dimension;
- number and severity of discrepancies;
- proportion of the claim mechanically checkable without full rerun;
- time spent per audit stage;
- number of checks blocked by access, compute, licensing or missing artifacts;
- agreement or disagreement with the published artifact-evaluation verdict, where available.

With ten cases, results are descriptive. Do not make population-wide prevalence claims or infer causation.

## 10. Reliability safeguards

- One auditor cannot establish inter-rater reliability. A later validation phase requires a second human auditor working independently on a subset.
- LLM-generated findings must be labelled as leads until manually verified against source artifacts.
- Do not treat repository stars, badges, author claims, or self-reported checklists as evidence of a specific result.
- Preserve negative findings and unknowns; do not silently convert missing evidence into failure.
- Record selection exclusions to expose sampling bias.

## 11. Pilot stopping rules

Stop auditing a case if the paper or artifact is unavailable, the claim cannot be isolated, the license prohibits inspection, or the required expertise is beyond the audit team's competence. Record the reason and retain the case in the sampling log rather than silently replacing it.

The pilot is useful only if it reveals repeatable failure modes or a measurable gap not already covered by existing artifact-evaluation and evidence-verification methods. Otherwise, this research direction should be abandoned or reframed.
