# Experiment Record: Privileged Ground Truth vs Online Evidence

**Date:** 2026-11-27  
**Status:** exploratory bounded model; not a research result  
**Code:** `experiments/ground_truth_vs_online_evidence.py`

## Question

Can a verifier that sees only delivered events distinguish a genuinely quiet execution from an execution in which a final violation event was emitted but suppressed? Does a trusted sequence high-water commitment expose the missing tail event?

## Model

Three two-event-or-shorter traces are used:

1. One ordinary event.
2. Two ordinary events.
3. One ordinary event followed by one violation event.

For each trace, enumerate every subset of delivered events and both beacon-delivery states. This produces 20 trace/schedule combinations.

The comparison has three observers:

- **Privileged evaluator:** knows the generated trace and which events were delivered. It can determine actual property truth and whether transport loss occurred.
- **Naive online observer without a commitment:** sees only delivered events and returns no-violation when it has seen no violation witness.
- **Commitment-aware observer:** also receives a trusted high-water mark and returns unknown if any sequence number through that mark is absent.

A safe no-commitment observer must abstain because it cannot know whether an unseen event exists. The script reports this separately from the deliberately unsafe naive observer.

## Results

| Measure | Count |
|---|---:|
| Enumerated trace/schedule combinations | 20 |
| Schedules with at least one undelivered event (privileged evaluator knows) | 14 |
| Beacon-aware incomplete outcomes | 7 |
| Beacon-aware false all-clears | 0 |
| Naive no-beacon false all-clears | 2 |
| Safe no-beacon abstentions | 10 |

The counts are exhaustive only for this tiny trace set and delivery model. They are not failure probabilities, performance measurements, or estimates of real deployment reliability.

## Interpretation

The experiment illustrates the information asymmetry:

- A privileged evaluator can compare the delivered subset with the complete generated trace.
- An online observer without a commitment cannot distinguish some clean traces from traces with a suppressed final event.
- A trusted high-water mark exposes a missing event in the committed prefix, forcing an unknown result rather than an unsupported all-clear.

The result is expected from the model's construction. The beacon-aware observer is given a correct, trusted high-water mark, and the property is a simple existential violation witness. No cryptographic compromise, faulty node, incorrect beacon, clock issue, coordinator crash, membership change, or recovery race is modelled.

## Prior-art assessment

This experiment is not novel as a general result.

Kekatos et al., *Sound Distributed Runtime Verification under Incomplete Evidence* (arXiv:2611.32868), already formalizes indistinguishable executions in Theorem 3.1, defines a silent false all-clear, and shows why a sound monitor must abstain under suppressed evidence. Section 4 explains sequence gaps and high-water beacons for missing events, including losses in a quiescent tail. The present toy model is a small executable illustration of those claims, not an independent contribution.

The 2023 survey by Taleb, Hallé and Khoury, *Uncertainty in Runtime Verification*, reviews monitoring over incomplete and imprecise traces. Earlier work on runtime verification under access restrictions and failure-aware distributed runtime verification also covers partial observation, knowledge gaps and three-valued verdicts.

The author's related ISR-swarm repository has a different methodological arrangement: its in-process harness constructs expected sequence numbers from the complete raw event list before injecting drops. That is legitimate for controlled fault injection, but it gives the harness privileged ground truth. It does not, by itself, demonstrate how a deployed verifier discovers an unknown missing tail. This distinction is recorded in `implementation-audits/related-isr-swarm-artifact.md`.

## Limitations

1. Single stream only.
2. No event reordering or duplicate delivery.
3. No delayed-but-not-lost messages.
4. No beacon forgery, corruption, omission by a faulty node, or equivocation.
5. No timestamp semantics or beacon-finality test.
6. No coordinator/outbox crash boundary.
7. No verifier restart or durable cursor.
8. No dynamic membership.
9. No probabilistic fault model or performance measurement.
10. The oracle and online monitor are deliberately simplified.

## Decision

Do not claim novelty, publish this as a standalone study, or use it as the basis for a funding proposal.

Retain it as a sanity-check artifact. The next candidate study must identify a specific, unresolved operational or methodological question not already answered by the target paper and the incomplete-trace runtime-verification literature. In particular, investigate whether published evaluation harnesses distinguish ground-truth knowledge available to the experimenter from evidence available to the online monitor, and whether their reported metrics measure the latter.
