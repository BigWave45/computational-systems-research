# Abstract State Machine: Distributed Evidence Protocol

**Target paper:** Kekatos et al., *Sound Distributed Runtime Verification under Incomplete Evidence*, arXiv:2611.32868  
**Status:** independent abstraction for protocol analysis; not a reproduction of the authors' code

## 1. Scope and trust boundary

This model covers four logical roles:

1. **Node:** emits a per-node contiguous event sequence and periodic beacons.
2. **Coordinator:** receives node events, assigns a durable ingest order/identifier, stores them in an outbox, and forwards them.
3. **Verifier:** consumes forwarded events, maintains per-node sequence coverage, checks order and liveness, and evaluates properties.
4. **Network/adversary:** may delay, drop, reorder, or suppress messages; under the paper's core model it cannot forge or alter emitted events.

The model does not implement MQTT, NATS JetStream, ROS 2, the actual property monitor, a real clock, or coordinator persistence semantics. It is a deliberately small transition-system abstraction.

## 2. State

For each node a:

- `next_seq[a]`: next sequence number to assign.
- `emitted[a]`: events emitted by the node.
- `retained[a]`: emitted events not yet acknowledged by the verifier.
- `beacon[a]`: most recent beacon known to the verifier, if any.

For each coordinator c:

- `alive[c]`: whether the coordinator remains available.
- `outbox[c]`: ingested events not yet durably forwarded.
- `ingest_order[c]`: observable order assigned at ingestion.

For the verifier:

- `held[a]`: received events indexed by sequence number.
- `beacon[a]=(h,u)`: latest received high-water/frontier commitment.
- `membership`: node set whose evidence is required for the property.
- `unavailable`: streams whose silence exceeded the configured timeout.
- `degraded`: streams with an ordering or commitment-integrity discrepancy.
- `frontier`: minimum beacon time across contributing streams, provided every stream is accounted for through its beacon high-water mark and none is unavailable/degraded.

## 3. Transitions

| Transition | State change | Required invariant |
|---|---|---|
| Emit event | Node assigns next contiguous sequence number and appends event | Per-node timestamps are non-decreasing; event is retained |
| Emit beacon | Node sends current high-water mark h and beacon emission time u | The beacon commitment must be final for its claimed window |
| Deliver event | Network delivers event to coordinator/verifier | No event contents may be forged or altered |
| Coordinator ingest | Coordinator stores event in outbox and assigns ingest order | Durable append precedes acknowledgement |
| Forward | Coordinator forwards outbox item; verifier consumes via durable cursor | At-least-once delivery; duplicates deduplicated |
| Receive beacon | Verifier records (h,u) and checks whether all sequence numbers through h are held | No negative verdict until coverage is complete |
| Detect gap | Verifier receives sequence j+2 without j+1 | Mark stream incomplete |
| Detect silence | Verifier-resident clock observes missing beacon past timeout | Mark stream unavailable; do not treat silence as idle |
| Advance frontier | All contributing streams have complete coverage through their beacon commitments | Frontier is minimum u across streams |
| Membership change | Join/leave record enters protected sequenced evidence path | Membership cannot silently change out of band |
| Coordinator destruction | Coordinator and unforwarded local state are lost | Node-retained unacknowledged evidence must survive for replay |
| Successor handover | Successor emits handover-gap marker; nodes replay from verifier acknowledgement | Keep affected streams unknown/incomplete until reconciled |
| Verifier acknowledgement | Node may discard events through acknowledged sequence | A coordinator's hop acknowledgement alone is insufficient |

## 4. Verdict rule

The paper's verdict has two axes:

- Security: `violation`, `no_violation`, `unknown`.
- Evidence completeness: `intact`, `degraded`, `incomplete`, `unavailable`.

A positive violation witness can be reported from received evidence. A negative `no_violation` result is downgraded to `unknown` unless completeness is `intact`. A composed verdict takes the least complete status among contributing streams.

A verdict is stamped at the evidence frontier, not the current wall-clock time. A stalled frontier makes the verdict stale, but does not extend its claim into uncovered time.

## 5. Safety properties to check

**S1 — No unsupported all-clear.** The verifier must never output `(no_violation, intact)` for a stamped interval in which the true trace contains a violation witness.

**S2 — Sequence completeness.** A stream is complete through h only if every sequence number 1..h is held and no known commitment contradiction exists.

**S3 — Beacon finality.** Once a beacon (h,u) is accepted, no later event from that node may have sequence >h and timestamp <=u. If such an event is delivered, the prior commitment must be invalidated and the affected stream degraded/unknown.

**S4 — Order integrity.** If coordinator ingest order disagrees with the paper's timestamp plus (node,sequence) emission order, the affected verdict must not remain intact.

**S5 — Silence safety.** A missing beacon past timeout makes the stream unavailable; before timeout, the evidence frontier must not advance beyond the last confirmed coverage.

**S6 — Membership integrity.** Threshold and coverage claims require sequenced join/leave evidence. Out-of-band membership divergence cannot support an intact negative verdict.

**S7 — Destruction recovery.** Evidence is not discarded at a coordinator hop acknowledgement. It remains available until verifier acknowledgement or acknowledgement by an independently surviving tier.

## 6. Initial model checks

The executable abstraction in `distributed_evidence_protocol_model.py` checks seven bounded scenarios:

1. Equal timestamp after beacon: a later event with sequence greater than h and timestamp equal to u invalidates the frontier.
2. Sequence gap: a missing sequence number prevents complete coverage.
3. Quiescent-tail loss: a beacon high-water mark exposes a missing final event even when no later event arrives.
4. Silence: no beacon or a timed-out stream prevents frontier advancement.
5. Coordinator destruction with end-to-end retention: the node replays the event through a successor and coverage can recover.
6. Coordinator destruction after hop-only acknowledgement: unforwarded evidence is lost and coverage cannot recover.
7. Ordering discrepancy: mismatch between ingest order and emission order degrades the affected composition.

All seven checks are small, constructed executions. They are not a proof of the protocol, an implementation test, a reproduction of the paper's experiments, or evidence of field reliability.

## 7. Main unresolved issue: beacon finality

The paper states that event timestamps do not decrease along a node's sequence. It also states that a beacon's u is its emission time and claims that no later event can carry a timestamp at or below u.

Non-decreasing timestamps alone permit equality. For example:

- Event (A, 1, timestamp 5)
- Beacon (A, high-water 1, frontier 5)
- Later event (A, 2, timestamp 5)

This is non-decreasing in event time and the later event lies in the closed interval ending at u. It conflicts with the commitment-finality rule.

The formal model therefore needs one additional, explicit mechanism: for example, strictly increasing timestamps across the beacon boundary, a composite frontier that includes sequence number, or a protocol rule that rejects/invalidates a later event at or below u. The paper's abstract model says commitments are final, but the implementation or a fuller protocol definition is needed to establish how that property is enforced.

## 8. What this model does not establish

- It does not show that the authors' implementation accepts an invalid beacon.
- It does not refute Proposition 5.1 or Theorem 3.1.
- It does not reproduce the paper's MQTT/NATS experiments.
- It does not model all timing, clock-skew, crash, retention, or membership corner cases.
- It does not establish novelty for a new research project.

The next validation step is to obtain the authors' promised implementation or a full protocol specification, map each transition above to actual code, and test the safety properties against that implementation. Until then, this remains an independent abstract model.
