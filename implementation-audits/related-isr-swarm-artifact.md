# Related-Artifact Audit: Evidence-Aware ISR Swarm Repository

**Repository:** https://github.com/nikos-kekatos/evidence-aware-rv-isr-swarms  
**Files inspected:** `code/swarm_rv.py`, `code/ros2_realism/mission_monitor.py`, `code/ros2_realism/platform_node.py`, `code/e2e_latency.py`, `code/exp_skew.py)  
**Audit date:** 2026-11-27  
**Relation to target paper:** related work by an overlapping author; NOT the artifact for arXiv:2611.32868

## 1. Why inspect this repository

The target paper's promised implementation was not located. This repository is relevant because it implements evidence-aware verdicts, event identifiers, event-loss injection, clock-order checks, and an MQTT/NATS pipeline. It can help identify design choices and test assumptions, but it cannot be substituted for the target paper's implementation.

## 2. Findings from the in-process core

### 2.1 Event IDs and sequence-gap detection

`swarm_rv.py` models event IDs as strings of the form `<agent>-<seq>`. Its `_stream_gaps` function detects gaps by comparing IDs in the consumed event list with an `expected_seq` set.

In `Fabric.evaluate`, that expected set is constructed from `self.raw`, the complete in-memory event list supplied to the fabric, before injected drops are removed by `consumed()`.

This is useful for a controlled fault-injection harness: the harness knows which events it originally generated and can identify which were subsequently dropped. It is not equivalent to a deployed verifier learning the expected sequence frontier solely from messages received over an unreliable network. In a live protocol, a verifier needs a trusted high-water commitment, an independent schedule, or another explicit source of expected sequence coverage.

### 2.2 Silence handling

The in-process fabric has a `silenced` set populated by explicit test injection. It converts those entries into missing evidence and an unavailable verdict. This is a controlled input to the test harness, not a demonstrated timeout/beacon implementation.

### 2.3 Ordering

The in-process fabric exposes a Boolean `order_ok`. The skew experiment changes event timestamps and manually sets this Boolean according to the scenario. The core then downgrades order-sensitive properties when the Boolean is false.

This tests the monitor's response to an externally supplied order-integrity signal. It does not itself implement distributed clock synchronization, per-node timestamp monotonicity enforcement, beacon commitments, or a proof that the signal is sound.

## 3. Findings from the ROS 2 integration

`platform_node.py` publishes scripted actions. `mission_monitor.py` receives them and assigns a shared incrementing local counter as the event timestamp, plus per-platform counters as event IDs.

The counters are assigned in callback/receipt order. The integration does not show the per-node beacon, high-water mark, timestamp frontier, or end-to-end acknowledgement protocol specified in the target paper.

This is an integration of the ISR-swarm monitor over ROS 2/DDS, not a validation of the target paper's distributed evidence protocol.

## 4. Findings from the latency experiment

`e2e_latency.py` defaults to an offline synthetic per-hop latency model with a fixed seed. Its output is explicitly labelled synthetic and not a live measurement.

Its optional `--real` path uses MQTT QoS 1, a sidecar JSONL outbox with flush/fsync, and NATS JetStream publish acknowledgement. The inspected path demonstrates a durable local write before JetStream publish, but does not establish the target paper's verifier-level end-to-end acknowledgement and node-retention semantics. In particular, the script's shown sidecar flow does not acknowledge the originating node after verifier receipt.

The synthetic default must not be described as a live end-to-end broker measurement.

## 5. Consequence for our investigation

The related repository demonstrates several relevant implementation patterns, but it does not resolve the target paper's beacon-finality question.

It also highlights a useful distinction for future experiments:

- **Known-ground-truth fault injection:** the harness knows the original event set and can label omissions.
- **Online evidence completeness:** the verifier must infer what it has not received using protocol commitments, timing assumptions, acknowledgements, and membership evidence.

Those are different experimental conditions. A test of the first does not automatically validate the second.

## 6. Research classification

- Target-paper artifact located: no.
- Related author's artifact inspected: yes.
- Target-paper implementation reproduced: no.
- Target-paper beacon protocol validated by related repository: no.
- Specific methodological distinction identified: harness-known expected events versus verifier-observable sequence commitments.
- Novelty claim: none.

The next step remains obtaining the target artifact or formalizing a separate protocol specification and explicitly testing the distinction between known-ground-truth fault injection and online evidence completeness.
