#!/usr/bin/env python3
"""Bounded check of the timestamp-to-beacon-finality implication.

This is an independent model of one sentence in Section 4 of
Kekatos et al., arXiv:2611.32868. It is NOT the authors' implementation
and does not model the complete monitoring protocol.

Model:
- one node emits four events with contiguous sequence numbers 1..4;
- event timestamps are non-decreasing;
- a beacon after event h commits (high_water=h, frontier=timestamp[h-1]);
- a boundary is problematic if a later event has timestamp <= frontier.

The check asks whether non-decreasing timestamps alone imply that no
later event can fall inside the committed closed interval.
"""

from itertools import combinations_with_replacement


def enumerate_sequences(alphabet_size=4, event_count=4):
    return list(combinations_with_replacement(range(alphabet_size), event_count))


def problematic_boundaries(timestamps):
    problems = []
    for high_water in range(1, len(timestamps)):
        frontier = timestamps[high_water - 1]
        later = [
            (seq, timestamp)
            for seq, timestamp in enumerate(timestamps[high_water:], start=high_water + 1)
            if timestamp <= frontier
        ]
        if later:
            problems.append((high_water, frontier, later))
    return problems


def main():
    nondecreasing = enumerate_sequences()
    nondecreasing_counterexamples = [
        (timestamps, problematic_boundaries(timestamps))
        for timestamps in nondecreasing
        if problematic_boundaries(timestamps)
    ]

    strictly_increasing = [
        timestamps
        for timestamps in nondecreasing
        if all(left < right for left, right in zip(timestamps, timestamps[1:]))
    ]
    strict_counterexamples = [
        (timestamps, problematic_boundaries(timestamps))
        for timestamps in strictly_increasing
        if problematic_boundaries(timestamps)
    ]

    print(f"Non-decreasing sequences: {len(nondecreasing)}")
    print(
        "Sequences with at least one problematic beacon boundary: "
        f"{len(nondecreasing_counterexamples)}"
    )
    print(
        "Problematic beacon boundaries (counted per sequence and high-water mark): "
        f"{sum(len(problems) for _, problems in nondecreasing_counterexamples)}"
    )
    print(f"Strictly increasing sequences: {len(strictly_increasing)}")
    print(
        "Strictly increasing sequences with problematic boundaries: "
        f"{len(strict_counterexamples)}"
    )

    assert len(nondecreasing) == 35
    assert len(nondecreasing_counterexamples) == 30
    assert sum(len(problems) for _, problems in nondecreasing_counterexamples) == 60
    assert len(strictly_increasing) == 1
    assert len(strict_counterexamples) == 0

    print("PASS: bounded enumeration reproduced expected counts.")


if __name__ == "__main__":
    main()
