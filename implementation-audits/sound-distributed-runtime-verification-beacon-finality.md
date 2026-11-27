# Investigation Note: Beacon Timestamp Finality

**Paper:** Nikolaos Kekatos et al., *Sound Distributed Runtime Verification under Incomplete Evidence*  
**Preprint:** https://arxiv.org/abs/2611.32868  
**Investigation date:** 2026-11-27  
**Status:** unresolved formalization question; no implementation defect established

## 1. Question

Does the paper's stated assumption of non-decreasing per-node event timestamps suffice to establish the finality of a beacon commitment identified by a sequence high-water mark and a timestamp frontier?

## 2. Relevant claims in the paper

Section 2 defines each event as carrying a per-node monotone sequence number and a timestamp that does not decrease along that node's sequence. Section 4 says a beacon carries a sequence high-water mark h and a time frontier u, where u is the time at which the beacon was emitted. It then states that every event emitted with timestamp at most u has a sequence number at most h, and no later event carries a timestamp at most u. The verifier treats the interval up to u as complete once it holds every number up to h.

Section 2 also says commitments must be final for their node and window. The protocol must therefore justify why a later event cannot fall inside the already committed time interval.

The relevant distinction is that **u is the beacon's emission timestamp**, not necessarily the timestamp of the last event before the beacon. The experiment below models that distinction.

## 3. Minimal abstract trace

Consider one node with a non-decreasing clock:

| Item | Sequence | Timestamp |
|---|---:|---:|
| Event A | 1 | 5 |
| Beacon | high-water = 1 | 5 |
| Event B | 2 | 5 |

The beacon is emitted after Event A. Event B is emitted later. All timestamps are non-decreasing in execution order. Event B nevertheless has a timestamp at or below the beacon frontier while its sequence number exceeds the beacon high-water mark.

This trace violates the commitment-finality condition if that condition is independently imposed as an invariant. It does not, by itself, establish that the protocol admits the trace. It shows that non-decreasing timestamps alone do not derive the stated no-later-event implication when equality is allowed.

## 4. Corrected bounded enumeration

The independent model in `experiments/beacon_timestamp_boundary_check.py` represents four events and one beacon. The beacon is inserted after at least one event and before the final event. It has its own timestamp. All five timestamps (four event timestamps and the beacon timestamp) are non-decreasing and drawn from {0,1,2,3}.

Results:

- 224 timestamp-assignment/beacon-position combinations.
- 105 combinations contain a later event with timestamp at or below the beacon frontier.
- In every problematic combination, the later event's timestamp equals the beacon timestamp; monotonicity excludes a decrease but permits equality.
- No counterexample remains when all post-beacon events are required to have timestamps strictly greater than the beacon timestamp.

These are exhaustive counts for this finite model only. They are not probabilities, empirical deployment measurements, or results from the authors' implementation.

**Correction to the first model:** The initial version incorrectly used the timestamp of the last pre-beacon event as the beacon frontier. That is not the paper's stated definition of u. Its earlier counts (35 sequences and 60 boundaries) are superseded and must not be cited. The current script models the beacon's own emission timestamp.

## 5. Artifact search

As of the investigation date, GitHub repository searches for the paper title and arXiv identifier did not identify a repository for this paper's promised monitors, drivers, and finite-model checker.

The author's public repositories include related artifacts, including:

- https://github.com/nikos-kekatos/hierarchical-edge-iot-monitoring
- https://github.com/nikos-kekatos/evidence-aware-rv-isr-swarms
- https://github.com/nikos-kekatos/formal-rv-tool-using-llm-agents

These are related artifacts, not the implementation of arXiv:2611.32868. They must not be represented as a reproduction target for that paper.

## 6. What remains unresolved

The decisive question is whether beacon generation and verification enforce commitment finality independently of timestamp monotonicity.

The paper's stated core model assumes authenticated non-Byzantine nodes and non-decreasing per-node timestamps. Its threat-to-validity section says the experiments script the timestamp assumption but do not enforce it. The implementation artifact is therefore needed to establish how the assumption is operationalized.

To resolve the issue, we need the implementation or a sufficiently detailed formal specification of:
1. how a node chooses h and u;
2. whether timestamp equality across a beacon boundary is possible;
3. what prevents a later event from appearing at or below u;
4. how a verifier treats a commitment contradicted by a later event;
5. whether the completeness verdict is invalidated, downgraded, or retained.

Possible protocol designs include strict timestamp progression after a beacon, a composite timestamp/sequence frontier, or an explicitly exclusive upper timestamp boundary. These are candidate design alternatives, not claims about the authors' implementation.

## 7. Research classification

- **Reproduction:** not performed.
- **Independent bounded model:** performed; corrected to model the beacon's own timestamp.
- **Formal implication check:** non-decreasing timestamps alone do not establish the stated no-later-event implication for a closed interval when equality is allowed.
- **Protocol defect:** not established.
- **Theorem refutation:** not established.
- **Novelty:** not claimed.

The next step is artifact inspection or a complete formal reconstruction of the beacon protocol. If independent finality enforcement is specified and shown to exclude the trace, this concern should be closed rather than promoted into a research claim.
