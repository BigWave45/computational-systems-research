# Research Method and Evidence Standards

## Workflow

### 1. Define the claim

Identify the system, property, operating conditions, observation boundary, assumptions, and what would count as a counterexample. Avoid unqualified claims such as "the system is reliable."

### 2. Review prior work

Record publication/version date, authors, relevant claims, methods, assumptions, artifact availability, acknowledged limitations, and overlap with the proposed experiment. An abstract is not an implementation audit.

### 3. Inspect artifacts

Pin repository commits and releases. Record environment and dependency versions. Inspect test entry points, data provenance, measured quantities, and whether the ground-truth oracle is independent. Distinguish implemented behaviour from diagrams or stated intentions.

### 4. Reproduce

Reproduce a bounded subset before modifying the experiment. Record commands, environment, seeds, inputs, outputs, and deviations. A failed reproduction is a finding to investigate.

### 5. Extend

Change one major experimental variable at a time where practical. Explain which assumption or boundary the change tests. Compare with the reproduced baseline.

### 6. Report

Report positive, negative, and inconclusive results. State limits on generalization. Do not convert finite test results into universal guarantees.

## Evidence categories

1. **Author claim:** stated in a paper, README, or documentation.
2. **Artifact inspection:** confirmed by examining a specific code/data/protocol version.
3. **Local reproduction:** independently executed under a recorded environment.
4. **Independent extension:** a new experiment using a documented protocol.
5. **External validation:** tested under conditions materially different from the original setting.

Never describe category 1 as category 3 or 4.

## Three-valued evaluation

For a property (P):

- **SATISFIED:** evidence supports (P) under declared assumptions.
- **VIOLATED:** evidence demonstrates a counterexample to (P).
- **UNKNOWN:** evidence is insufficient to justify either result.

## Experimental controls

Where relevant, define fault classes in advance; use an independent target-side oracle for external effects; distinguish request dispatch from committed effects; separate runtime logs from ground truth; record crashes, timeouts, retries, and partial failures; preserve raw outputs; repeat trials when nondeterminism matters; and report denominators and uncertainty.

## Reproducibility record

Record protocol version, repository commits, hardware/OS, runtime and dependencies, data/model provenance, configuration and seeds, exact commands, trial counts and exclusions, raw results, analysis scripts, and protocol deviations.

## Integrity rules

Do not fabricate results or citations, infer production guarantees from toy simulations, treat hashes as proof of semantic truth, hide failed trials without a predeclared rule, claim novelty from a limited search, or present AI-generated summaries as source-level verification.
