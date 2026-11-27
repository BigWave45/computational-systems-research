# Investigation Note: Beacon Timestamp Finality

**Paper:** Nikolaos Kekatos et al., *Sound Distributed Runtime Verification under Incomplete Evidence*  
**Preprint:** https://arxiv.org/abs/2611.32868  
**Investigation date:** 2026-11-27  
**Status:** unresolved formalization question; no implementation defect established

## 1. Question

Does the paper's stated assumption of non-decreasing per-node event timestamps suffice to establish the finality of a beacon commitment identified by a sequence high-water mark and a timestamp frontier?

## 2. Relevant claims in the paper

The paper describes per-node events with sequence numbers and timestamps that do not decrease along a node's sequence. A beacon carries a high-water mark h and a time frontier u. The Section 4 explanation says that, under the non-Byzantine and non-decreasing-timestamp assumptions, every event with timestamp at most u has sequence number at most h, and no later event carries a timestamp at most u.

Separately, the paper defines a commitment as final for its node and window: no subsequent event may appear within the committed sequence prefix/window.

These statements need to be distinguished. Non-decreasing timestamps permit equal timestamps. Equality alone does not imply that a later sequence number must have a timestamp greater than u.

## 3. Minimal abstract trace

Consider one node:

| Item | Sequence | Timestamp |
|---|---:|---:|
| Event A | 1 | 5 |
| Beacon | high-water = 1 | frontier = 5 |
| Event B | 2 | 5 |

The event timestamps are non-decreasing. Event B nevertheless has a timestamp at or below the beacon frontier while its sequence number exceeds the beacon high-water mark.

This trace violates the finality condition if that condition is independently imposed as an invariant. It therefore does not, by itself, establish that the paper's protocol admits the trace. It shows that non-decreasing timestamps alone do not derive the stated finality property.

## 4. Bounded enumeration

The independent model in `experiments/beacon_timestamp_boundary_check.py` enumerates four-event, non-decreasing timestamp sequences over the alphabet {0,1,2,3}. For each sequence, it places a beacon after each non-final event and checks whether a later event has timestamp less than or equal to the beacon frontier.

Results:

- 35 non-decreasing sequences.
- 30 sequences contain at least one problematic beacon boundary.
- 60 problematic sequence/boundary pairs in total.
- Only one four-event sequence over this alphabet is strictly increasing; it has no problematic boundary.

These are exhaustive counts for the finite model only. They are not probabilities, empirical deployment measurements, or results from the authors' implementation.

## 5. Artifact search

As of the investigation date, GitHub repository searches for the paper title and arXiv identifier did not identify a repository for this paper's promised monitors, drivers, and finite-model checker.

The author's public repositories include related work, including:

- https://github.com/nikos-kekatos/hierarchical-edge-iot-monitoring
- https://github.com/nikos-kekatos/evidence-aware-rv-isr-swarms
- https://github.com/nikos-kekatos/formal-rv-tool-using-llm-agents

These are related artifacts, not the implementation of arXiv:2611.32868. They must not be represented as a reproduction target for that paper.

## 6. What remains unresolved

The decisive question is whether beacon generation and verification enforce commitment finality independently of timestamp monotonicity.

To resolve it, we need the paper's actual implementation or a sufficiently detailed formal specification of:
1. how a node chooses h and u;
2. whether timestamp equality is allowed;
3. what prevents a later event from appearing at or below u;
4. how a verifier treats a commitment contradicted by a later event;
5. whether the completeness verdict is invalidated, downgraded, or retained.

Possible protocol designs include strict timestamp progression, a composite timestamp/sequence frontier, or an explicitly exclusive upper timestamp boundary. These are candidate design alternatives, not claims about the authors' implementation.

## 7. Research classification

- **Reproduction:** not performed.
- **Independent bounded model:** performed.
- **Formal implication check:** the stated non-decreasing condition alone is insufficient for the claimed no-later-event implication when the interval is closed and equality is allowed.
- **Protocol defect:** not established.
- **Theorem refutation:** not established.
- **Novelty:** not claimed.

The next step is artifact inspection or a complete formal reconstruction of the beacon protocol. If independent finality enforcement is specified and shown to exclude the trace, this concern should be closed rather than promoted into a research claim.
