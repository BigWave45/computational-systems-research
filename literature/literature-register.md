# Literature Register

Initial register from the first prior-art review. This is not an exhaustive systematic review. Reported results are author claims unless independently reproduced in this programme.

| Work | Area | Relevance / overlap | Status |
|---|---|---|---|
| [AgentAssay](https://arxiv.org/abs/2603.02601) / [code](https://github.com/qualixar/agentassay) | Agent regression testing | Repeated stochastic trials, coverage, mutation/metamorphic testing, CI gates, cost-aware selection | Identified; artifact audit pending |
| [BehavTest](https://github.com/dhrumilbhut/behavtest) | Behavioural regression | Repeated runs, statistical baseline comparison, traces, tool calls, CI gating | Identified; artifact audit pending |
| [Mining Workflow Graphs for Black-Box Boundary Testing of Conversational LLM Agents](https://arxiv.org/abs/2607.06873) | Black-box agent testing | Workflow graph discovery and hidden stateful boundary testing | Identified; methods review pending |
| [Agentic Execution Assurance](https://saridakisstamatischristos.github.io/publications/agentic-execution-assurance/agentic-execution-assurance.pdf) | Execution assurance | Observation-bounded certification, three-valued outcomes, runtime enforcement, evidence profiles, AEGISRUN | Paper/source audit partially completed; reproduction pending |
| [Idempotency Is Not Recovery](https://arxiv.org/abs/2611.23353) | Fault injection and recovery | Agent tool-action faults, idempotency, reconciliation, evidence sealing | Identified; artifact audit priority |
| [Auditable Authorization for LLM Agents](https://arxiv.org/abs/2611.19237) | Agent authorization | Authorization across model, harness, and workflow layers | Identified; methods review pending |
| [Evaluating More with Less](https://arxiv.org/abs/2611.34617) | Test selection | Cost-aware black-box test selection across agent benchmarks | Identified; methods review pending |

## Interpretation

This work already covers much of the original proposal to build a general black-box behavioural-change detector or agent execution guard. That broad direction is not being treated as novel.

The next review must include distributed-systems work on transactional outbox, idempotency, write-ahead logging, sagas, crash consistency, and recovery. Agent papers cannot be evaluated in isolation from established systems research.

## Required audit fields

For each work, add exact version/date and commit; research question and claims; experimental design; dataset and ground-truth construction; artifact availability and license; reproduction instructions; observed implementation behaviour; assumptions and limitations; overlap; and independent reproduction status.

## Source caution

Trial counts, percentages, speedups, and coverage figures in these works are not independent findings of this programme. Attribute them to their authors and verify them against the papers and artifacts before comparison.


## Distributed runtime verification and incomplete evidence

| Work | Area | Relevance / overlap | Status |
|---|---|---|---|
| [Uncertainty in Runtime Verification: A Survey](https://doi.org/10.1016/j.cosrev.2023.100594) (Taleb, Hallé & Khoury, 2023) | Incomplete/imprecise traces | Direct survey of uncertainty sources and sound monitoring methods | Identified; full taxonomy review pending |
| [Runtime Verification Under Access Restrictions](https://constellation.uqac.ca/id/eprint/7361/1/paper.pdf) | Partial observability | Models incomplete/uncertain monitor inputs and sound loss-tolerant monitoring | Identified; methods review pending |
| [Failure-aware Runtime Verification of Distributed Systems](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.FSTTCS.2015.590) | Distributed monitoring under failures | Out-of-order delivery, failures, three-valued MTL semantics, soundness and completeness | Identified; methods review pending |
| [Runtime Verification over Out-of-order Streams](https://people.inf.ethz.ch/basin/pubs/tocl19.pdf) | Out-of-order stream monitoring | Three-valued semantics for knowledge gaps and conservative verdicts | Identified; methods review pending |
| [Sound Distributed Runtime Verification under Incomplete Evidence](https://arxiv.org/abs/2611.32868) (Kekatos et al., 2026) | Evidence completeness and distributed monitoring | Directly covers indistinguishable executions, abstention, sequence gaps, beacons, silence, membership, coordinator failure and recovery | Paper inspected; target implementation not located; independent toy model is illustrative only |

### Consequence for the current experiment

The bounded ground-truth-versus-online experiment is not a novelty result. The target paper's Theorem 3.1 already formalizes indistinguishable executions and the need for abstention; Section 4 covers sequence gaps and high-water beacons. The 2023 survey and earlier papers cover incomplete traces and three-valued monitoring.

The remaining possible question is narrower and empirical: whether evaluation harnesses in selected published systems clearly separate privileged experimenter ground truth from the information available to the online monitor, and whether reported metrics measure online detection rather than harness-side fault knowledge. This is only a candidate for a structured artifact audit, not an approved research question.
