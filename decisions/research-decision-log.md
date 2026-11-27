# Research Decision Log

## 2026-11-26 — Establish programme repository

**Decision:** Use this repository as the durable record for the Computational Systems Research programme.

**Reason:** Keep programme definition, literature, source audits, experiments, and decisions together. Preserve abandoned questions and negative findings.

## 2026-11-26 — Withdraw broad black-box agent regression as a novelty claim

**Rejected candidate:** "Can independent black-box tests detect consequential behavioural changes in AI agents?"

**Reason:** Existing systems and papers cover behavioural regression, stochastic testing, workflow boundary testing, execution assurance, authorization, and agent tool-action fault injection.

**Consequence:** Do not build a generic agent regression framework on the assumption that this is unexplored.

## 2026-11-26 — Consider independent reproduction and external-validity testing

**Candidate:** Independently reproduce a published agent-execution assurance result, then test a carefully selected assumption under a materially different execution architecture.

**Status:** Provisional. No novelty claim and no implementation commitment.

**Required before approval:** source-level artifact inspection, reproduction feasibility, independent ground-truth analysis, distributed-systems prior-art review, and a falsifiable hypothesis with a predeclared protocol.

## Operating rule

Record future changes to the question, scope, method, and funding strategy with date, evidence, and rationale. Do not erase superseded decisions; add a new entry.


## 2026-11-27 — Classify ground-truth versus online-evidence toy experiment

**Experiment:** Enumerated 20 small trace/delivery schedules comparing a privileged evaluator, a naive online observer without a completion commitment, and an online observer with a trusted sequence high-water mark.

**Observed in this bounded model:** two false all-clears from the deliberately unsafe no-beacon observer; zero false all-clears from the beacon-aware observer; seven beacon-aware incomplete outcomes. A safe no-beacon observer abstains. These are constructed-model counts, not empirical rates.

**Prior-art finding:** This is not a novel result. Kekatos et al. (arXiv:2611.32868), Theorem 3.1 and Section 4, already formalize indistinguishable executions, abstention, sequence gaps, and high-water beacons. Earlier runtime-verification literature also studies incomplete traces and three-valued monitoring.

**Decision:** Keep the code as a sanity-check artifact. Do not claim novelty or use it as a standalone study or funding proposal.

**Next candidate for review:** Audit selected published runtime-verification evaluation harnesses to determine whether they distinguish experimenter-known ground truth from evidence available to an online monitor. This candidate remains unapproved and requires a defined sample, coding protocol, and prior-art review.
