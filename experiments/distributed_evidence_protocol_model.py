#!/usr/bin/env python3
"""Small explicit-state model of the evidence protocol in arXiv:2611.32868.

This is an independent abstraction, NOT the authors' implementation.
It models node sequence numbers, events, beacons, coordinator outboxes,
verifier receipt, evidence-frontier calculation, and selected faults.

It deliberately separates:
- event emission from event delivery;
- coordinator durability from verifier acknowledgement;
- a node's sequence high-water mark from the verifier's received prefix;
- a beacon's own emission timestamp from event timestamps.

This is a test harness for protocol obligations, not a faithful
reproduction of MQTT, NATS JetStream, ROS 2, or the paper's monitor code.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple


@dataclass(frozen=True)
class Event:
    node: str
    seq: int
    ts: int
    kind: str = "ordinary"


@dataclass(frozen=True)
class Beacon:
    node: str
    high_water: int
    frontier: int


@dataclass
class Node:
    node_id: str
    next_seq: int = 1
    emitted: List[Event] = field(default_factory=list)
    retained: Dict[int, Event] = field(default_factory=dict)

    def emit(self, ts: int, kind: str = "ordinary") -> Event:
        if self.emitted and ts < self.emitted[-1].ts:
            raise ValueError("event timestamps must be non-decreasing")
        event = Event(self.node_id, self.next_seq, ts, kind)
        self.next_seq += 1
        self.emitted.append(event)
        self.retained[event.seq] = event
        return event

    def beacon(self, ts: int) -> Beacon:
        if self.emitted and ts < self.emitted[-1].ts:
            raise ValueError("beacon timestamp precedes last event")
        return Beacon(self.node_id, self.next_seq - 1, ts)

    def verifier_ack(self, seq: int) -> None:
        for number in list(self.retained):
            if number <= seq:
                del self.retained[number]


@dataclass
class Coordinator:
    outbox: Dict[Tuple[str, int], Event] = field(default_factory=dict)
    ingest_order: List[Event] = field(default_factory=list)
    alive: bool = True

    def ingest(self, event: Event) -> None:
        if not self.alive:
            raise RuntimeError("coordinator is destroyed")
        self.outbox[(event.node, event.seq)] = event
        self.ingest_order.append(event)

    def destroy(self) -> None:
        self.alive = False
        self.outbox.clear()
        self.ingest_order.clear()


@dataclass
class Verifier:
    held: Dict[str, Dict[int, Event]] = field(default_factory=dict)
    beacons: Dict[str, Beacon] = field(default_factory=dict)
    membership: Set[str] = field(default_factory=set)
    unavailable: Set[str] = field(default_factory=set)
    degraded: Set[str] = field(default_factory=set)

    def receive_event(self, event: Event) -> None:
        self.held.setdefault(event.node, {})[event.seq] = event
        beacon = self.beacons.get(event.node)
        if (
            beacon is not None
            and event.seq > beacon.high_water
            and event.ts <= beacon.frontier
        ):
            self.degraded.add(event.node)

    def receive_beacon(self, beacon: Beacon) -> None:
        self.beacons[beacon.node] = beacon
        # Delivery may be reordered: a later-sequence event can arrive first.
        conflicts = [
            event
            for event in self.held.get(beacon.node, {}).values()
            if event.seq > beacon.high_water and event.ts <= beacon.frontier
        ]
        if conflicts:
            self.degraded.add(beacon.node)

    def contiguous_through(self, node: str, high_water: int) -> bool:
        held = self.held.get(node, {})
        return all(seq in held for seq in range(1, high_water + 1))

    def coverage_frontier(self):
        if not self.membership:
            return None
        if self.membership & (self.unavailable | self.degraded):
            return None
        if any(node not in self.beacons for node in self.membership):
            return None
        for node in self.membership:
            beacon = self.beacons[node]
            if not self.contiguous_through(node, beacon.high_water):
                return None
        return min(self.beacons[node].frontier for node in self.membership)

    def post_beacon_boundary_conflicts(self, node: str) -> List[Event]:
        """Events beyond h whose timestamps still fall inside closed [0,u]."""
        beacon = self.beacons.get(node)
        if beacon is None:
            return []
        return [
            event
            for event in self.held.get(node, {}).values()
            if event.seq > beacon.high_water and event.ts <= beacon.frontier
        ]


def check_timestamp_equality():
    node = Node("A")
    verifier = Verifier(membership={"A"})
    first = node.emit(5)
    beacon = node.beacon(5)
    later = node.emit(5)  # legal under non-decreasing timestamps
    verifier.receive_event(first)
    verifier.receive_beacon(beacon)
    frontier_before_later_arrival = verifier.coverage_frontier()
    verifier.receive_event(later)
    conflicts = verifier.post_beacon_boundary_conflicts("A")
    assert frontier_before_later_arrival == 5
    assert conflicts == [later]
    assert verifier.coverage_frontier() is None
    return "PASS: equal-timestamp later event invalidates the previously accepted frontier"


def check_sequence_gap():
    verifier = Verifier(membership={"A"})
    verifier.receive_event(Event("A", 2, 2))
    verifier.receive_beacon(Beacon("A", 2, 3))
    assert verifier.coverage_frontier() is None
    return "PASS: sequence gap blocks complete coverage"


def check_quiescent_tail_loss():
    verifier = Verifier(membership={"A"})
    verifier.receive_event(Event("A", 1, 1))
    verifier.receive_beacon(Beacon("A", 2, 3))
    assert verifier.coverage_frontier() is None
    return "PASS: beacon high-water mark exposes missing tail event"


def check_silence():
    verifier = Verifier(membership={"A"})
    assert verifier.coverage_frontier() is None
    verifier.unavailable.add("A")
    assert verifier.coverage_frontier() is None
    return "PASS: no beacon / timed-out stream cannot advance frontier"


def check_coordinator_destruction_and_replay():
    node = Node("A")
    coordinator = Coordinator()
    verifier = Verifier(membership={"A"})
    event = node.emit(10)
    beacon = node.beacon(11)
    coordinator.ingest(event)
    assert event.seq in node.retained
    coordinator.destroy()
    assert event not in coordinator.outbox.values()
    assert verifier.coverage_frontier() is None
    successor = Coordinator()
    successor.ingest(node.retained[event.seq])
    verifier.receive_event(successor.outbox[("A", event.seq)])
    verifier.receive_beacon(beacon)
    assert verifier.coverage_frontier() == 11
    node.verifier_ack(event.seq)
    assert event.seq not in node.retained
    return "PASS: end-to-end retention permits recovery after coordinator destruction"


def check_hop_ack_loss():
    node = Node("A")
    coordinator = Coordinator()
    verifier = Verifier(membership={"A"})
    event = node.emit(10)
    beacon = node.beacon(11)
    coordinator.ingest(event)
    node.verifier_ack(event.seq)  # intentionally simulate unsafe hop acknowledgement
    coordinator.destroy()
    verifier.receive_beacon(beacon)
    assert verifier.coverage_frontier() is None
    assert not node.retained
    return "PASS: deleting on hop ack makes destroyed unforwarded evidence unrecoverable"


def check_order_discrepancy():
    a = Event("A", 1, 10)
    b = Event("B", 1, 9)
    ingest_order = [a, b]
    emission_order = sorted(ingest_order, key=lambda e: (e.ts, e.node, e.seq))
    assert ingest_order != emission_order
    verifier = Verifier(membership={"A", "B"}, degraded={"A", "B"})
    assert verifier.coverage_frontier() is None
    return "PASS: observable ordering disagreement degrades the affected composition"


def run_checks():
    checks = [
        check_timestamp_equality,
        check_sequence_gap,
        check_quiescent_tail_loss,
        check_silence,
        check_coordinator_destruction_and_replay,
        check_hop_ack_loss,
        check_order_discrepancy,
    ]
    for check in checks:
        print(check())


if __name__ == "__main__":
    run_checks()
