"""Feature: dynamics arc — P(velocity | phrase position).

For corpora that carry real MIDI velocities, mines how loudness tracks position within a
piece (onset time normalized 0..1, bucketed into tenths). Feeds the engine's DYNAMICS
node so an entropy-chosen dynamic shape can follow a real human arc (typical swell to a
~2/3 peak) instead of a flat or independent-per-note velocity.
"""
from __future__ import annotations

from collections import defaultdict

from featlib import percentiles

NAME = "dynamics"
DESC = "P(velocity | normalized phrase position) — the loudness arc across a piece"
REQUIRES = ("notes",)


def run(tunes):
    buckets = defaultdict(list)
    n = 0
    for t in tunes:
        vels = [(n_.onset, n_.velocity) for n_ in t.notes if n_.velocity is not None]
        if len(vels) < 8:
            continue
        n += 1
        span = max(o for o, _ in vels) or 1
        for onset, vel in vels:
            buckets[round(onset / span, 1)].append(vel)
    return {
        "n_tunes": n,
        "by_position": {str(k): percentiles(v) for k, v in sorted(buckets.items())},
    }
