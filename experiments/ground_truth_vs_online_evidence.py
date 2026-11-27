#!/usr/bin/env python3
"""Compare privileged-ground-truth and protocol-visible evidence.

This is an independent toy experiment, not a reproduction of any paper.
It isolates one question: can an online verifier distinguish a complete
quiet execution from an execution whose final event was suppressed?

The experiment uses the same underlying traces and delivery schedules for:
1. an oracle that sees the full generated trace;
2. an online verifier that sees only delivered events and no commitment;
3. an online verifier that also receives a sequence high-water beacon.

The property is deliberately simple: event kind == "VIOLATION" means the
trace violates the monitored property. A negative verdict is safe only
when the verifier can establish coverage of the claimed trace prefix.
"""
from dataclasses import dataclass
from itertools import product
from typing import FrozenSet, Tuple


@dataclass(frozen=True)
class Event:
    seq: int
    kind: str


@dataclass(frozen=True)
class Observation:
    delivered_events: Tuple[Event, ...]
    beacon_high_water: int | None


def truth(trace: Tuple[Event, ...]) -> str:
    return "VIOLATION" if any(e.kind == "VIOLATION" for e in trace) else "NO_VIOLATION"


def oracle_verdict(trace: Tuple[Event, ...], delivered: FrozenSet[int]):
    """Privileged evaluator sees full truth and separately knows delivery loss."""
    complete = delivered == frozenset(e.seq for e in trace)
    return truth(trace), complete


def online_without_commitment(observation: Observation, safe: bool) -> str:
    """No trusted expected sequence count/high-water mark is available."""
    if safe:
        return "UNKNOWN"
    return (
        "VIOLATION"
        if any(e.kind == "VIOLATION" for e in observation.delivered_events)
        else "NO_VIOLATION"
    )


def online_with_beacon(observation: Observation) -> str:
    if observation.beacon_high_water is None:
        return "UNKNOWN_NO_COMMITMENT"
    received = {e.seq for e in observation.delivered_events}
    expected = set(range(1, observation.beacon_high_water + 1))
    if not expected.issubset(received):
        return "UNKNOWN_INCOMPLETE"
    return (
        "VIOLATION"
        if any(e.kind == "VIOLATION" for e in observation.delivered_events)
        else "NO_VIOLATION"
    )


def run_indistinguishability_case():
    quiet_trace = (Event(1, "ORDINARY"),)
    hidden_violation_trace = (
        Event(1, "ORDINARY"),
        Event(2, "VIOLATION"),
    )

    # Event 2 is suppressed. In both executions the verifier receives only E1.
    obs_without_beacon_quiet = Observation((Event(1, "ORDINARY"),), None)
    obs_without_beacon_violation = Observation((Event(1, "ORDINARY"),), None)
    assert obs_without_beacon_quiet == obs_without_beacon_violation

    # With a delivered beacon, the verifier learns that two events were emitted.
    obs_with_beacon = Observation((Event(1, "ORDINARY"),), 2)

    print("INDISTINGUISHABILITY")
    print(f"  quiet trace truth: {truth(quiet_trace)}")
    print(f"  hidden-violation trace truth: {truth(hidden_violation_trace)}")
    print(f"  same no-beacon observation: {obs_without_beacon_quiet == obs_without_beacon_violation}")
    print(f"  naive online verdict: {online_without_commitment(obs_without_beacon_violation, safe=False)}")
    print(f"  safe online verdict: {online_without_commitment(obs_without_beacon_violation, safe=True)}")
    print(f"  beacon-aware verdict: {online_with_beacon(obs_with_beacon)}")

    assert truth(quiet_trace) != truth(hidden_violation_trace)
    assert obs_without_beacon_quiet == obs_without_beacon_violation
    assert online_without_commitment(obs_without_beacon_violation, safe=False) == "NO_VIOLATION"
    assert online_without_commitment(obs_without_beacon_violation, safe=True) == "UNKNOWN"
    assert online_with_beacon(obs_with_beacon) == "UNKNOWN_INCOMPLETE"


def enumerate_delivery_schedules():
    """Enumerate all event-delivery subsets and beacon delivery outcomes."""
    traces = [
        (Event(1, "ORDINARY"),),
        (Event(1, "ORDINARY"), Event(2, "ORDINARY")),
        (Event(1, "ORDINARY"), Event(2, "VIOLATION")),
    ]
    rows = []
    for trace in traces:
        seqs = tuple(e.seq for e in trace)
        for mask in product((False, True), repeat=len(trace)):
            delivered = frozenset(seq for seq, keep in zip(seqs, mask) if keep)
            events = tuple(e for e in trace if e.seq in delivered)
            for beacon_delivered in (False, True):
                beacon = len(trace) if beacon_delivered else None
                observation = Observation(events, beacon)
                rows.append((trace, delivered, observation))
    return rows


def run_sweep():
    rows = enumerate_delivery_schedules()
    oracle_incomplete = 0
    online_beacon_unknown = 0
    online_beacon_false_clear = 0
    online_no_beacon_false_clear = 0
    online_no_beacon_safe_unknown = 0
    no_beacon_ambiguous_observation_groups = set()

    for trace, delivered, observation in rows:
        oracle_truth, oracle_delivery_complete = oracle_verdict(trace, delivered)
        if not oracle_delivery_complete:
            oracle_incomplete += 1

        if observation.beacon_high_water is not None:
            verdict = online_with_beacon(observation)
            if verdict == "UNKNOWN_INCOMPLETE":
                online_beacon_unknown += 1
            if verdict == "NO_VIOLATION" and truth(trace) == "VIOLATION":
                online_beacon_false_clear += 1
        else:
            verdict = online_without_commitment(observation, safe=False)
            if verdict == "NO_VIOLATION" and truth(trace) == "VIOLATION":
                online_no_beacon_false_clear += 1
            safe_verdict = online_without_commitment(observation, safe=True)
            if safe_verdict == "UNKNOWN":
                online_no_beacon_safe_unknown += 1
            no_beacon_ambiguous_observation_groups.add(
                tuple((e.seq, e.kind) for e in observation.delivered_events)
            )

    print("BOUNDED DELIVERY SWEEP")
    print(f"  executions/schedules: {len(rows)}")
    print(f"  oracle sees full truth; schedules with transport loss: {oracle_incomplete}")
    print(f"  beacon-aware incomplete outcomes: {online_beacon_unknown}")
    print(f"  beacon-aware false all-clears: {online_beacon_false_clear}")
    print(f"  no-beacon naive false all-clears: {online_no_beacon_false_clear}")
    print(f"  no-beacon safe abstentions: {online_no_beacon_safe_unknown}")
    print(f"  distinct no-beacon observations: {len(no_beacon_ambiguous_observation_groups)}")

    assert online_beacon_false_clear == 0
    assert online_no_beacon_false_clear > 0
    assert online_no_beacon_safe_unknown > 0
    assert oracle_incomplete > 0
    assert online_beacon_unknown > 0


if __name__ == "__main__":
    run_indistinguishability_case()
    run_sweep()
