#!/usr/bin/env python3
"""Bounded check of the beacon timestamp/high-water-mark implication.

Independent abstract model of Section 4 of Kekatos et al.,
arXiv:2611.32868. This is NOT the authors' implementation and does not
model the complete monitoring protocol.

A one-node execution contains four events and one beacon. The beacon is
inserted after h events. Its timestamp u is its own emission time, not
the timestamp of the preceding event. All five timestamps are drawn
from {0,1,2,3} and are non-decreasing in execution order.

The check asks whether non-decreasing timestamps alone guarantee that
every event emitted after the beacon has timestamp > u. A later event
with timestamp == u has sequence > h but lies in the paper's closed
interval [0,u].
"""

from itertools import combinations_with_replacement


def enumerate_executions(alphabet_size=4, event_count=4):
    """Yield (timestamps, beacon_position) for every ordered execution.

    beacon_position is the number of events emitted before the beacon,
    ranging from 1 to event_count - 1.
    """
    for timestamps in combinations_with_replacement(
        range(alphabet_size), event_count + 1
    ):
        for beacon_position in range(1, event_count):
            yield timestamps, beacon_position


def later_events_inside_closed_frontier(timestamps, beacon_position):
    beacon_time = timestamps[beacon_position]
    # Event timestamps after the beacon occupy the remaining positions.
    return [
        (sequence, timestamp)
        for sequence, timestamp in enumerate(
            timestamps[beacon_position + 1 :],
            start=beacon_position + 1,
        )
        if timestamp <= beacon_time
    ]


def main():
    executions = list(enumerate_executions())
    problematic = [
        (timestamps, h, later_events_inside_closed_frontier(timestamps, h))
        for timestamps, h in executions
        if later_events_inside_closed_frontier(timestamps, h)
    ]

    # The failure is specifically equality: monotonicity excludes < u,
    # but permits a later event to share the beacon's timestamp.
    equality_only = all(
        timestamp == timestamps[h]
        for timestamps, h, later in problematic
        for _, timestamp in later
    )

    # A strict post-beacon timestamp condition rules out the counterexample.
    strict_after_beacon = [
        (timestamps, h)
        for timestamps, h in executions
        if all(
            timestamp > timestamps[h]
            for timestamp in timestamps[h + 1 :]
        )
    ]
    strict_counterexamples = [
        (timestamps, h)
        for timestamps, h in strict_after_beacon
        if later_events_inside_closed_frontier(timestamps, h)
    ]

    print(f"Timestamp assignments with beacon positions: {len(executions)}")
    print(f"Assignments with a later event inside [0, u]: {len(problematic)}")
    print(
        "Problematic assignments where the later event equals u: "
        f"{len(problematic) if equality_only else 'not equality-only'}"
    )
    print(
        "Assignments satisfying strict timestamp increase after beacon: "
        f"{len(strict_after_beacon)}"
    )
    print(
        "Counterexamples under strict post-beacon increase: "
        f"{len(strict_counterexamples)}"
    )

    assert len(executions) == 224
    assert len(problematic) == 105
    assert equality_only
    assert len(strict_counterexamples) == 0
    print("PASS: bounded enumeration reproduced expected counts.")


if __name__ == "__main__":
    main()
