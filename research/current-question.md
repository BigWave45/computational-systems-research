# Current Research Question

**Status: provisional candidate; not approved for implementation.**

## Candidate direction

Independent reproduction and external-validity testing of published AI-agent execution-assurance results.

## Candidate question

Do reliability and evidence guarantees reported by current AI-agent execution systems persist when their experiments are independently reproduced and when the execution architecture changes?

This wording does not assert novelty.

## Rationale

Existing work already examines agent behavioural regression, black-box workflow boundaries, authorization, fault injection, idempotency, recovery, and tamper-evident evidence. Building another general-purpose agent testing or payment-authorization framework would duplicate a crowded area.

A potential contribution may come from independently checking published results and testing a specific assumption under a materially different architecture.

## Candidate study sequence

1. Select a published system with an accessible, versioned artifact.
2. Inspect its paper, source, data, protocol, and limitations.
3. Reproduce a bounded subset without silently changing the protocol.
4. Record deviations, unavailable dependencies, and failures.
5. Only then design an architecture-change experiment.
6. Compare outcomes against independently established ground truth.
7. Report where results hold, fail, or remain inconclusive.

A possible architecture change is moving from a single-host local-database target to a target service separated from the agent runtime. This may expose assumptions about crash boundaries, durable state, network ambiguity, and reconciliation. It is only a candidate variable.

Transactional outbox patterns, idempotency, write-ahead logging, sagas, and distributed recovery are established topics. Relevant prior art must be reviewed before asserting a research gap.

## Feasibility questions

- Can the artifact be obtained and executed?
- Are dependencies and versions pinned?
- Can the baseline be reproduced without paid model/API access?
- Is ground truth independent of the system being evaluated?
- What distributed-systems literature already addresses the proposed change?
- What observation would falsify the hypothesis?
- Can the work be completed with available compute and connectivity?

## Decision gate

Do not begin framework development or submit a novelty-based proposal until artifact feasibility, prior art, hypothesis, and protocol have been established.
