"""Feature: meter distribution — P(meter) and P(meter | genre).

Feeds the engine's METER node (currently 4/4-only; expansion is a deferred track).
Shows how often real corpora leave 4/4 and which genres carry 3/4, 6/8, 2/4, etc.
"""
from __future__ import annotations

from featlib import conditional, histogram

NAME = "meter"
DESC = "P(meter) overall and conditioned on genre"
REQUIRES = ("meter",)


def run(tunes):
    metered = [t for t in tunes if t.meter]
    overall = histogram(["%d/%d" % t.meter for t in metered])
    by_genre, support = conditional(
        [(t.genre, "%d/%d" % t.meter) for t in metered if t.genre])
    return {
        "n": len(metered),
        "overall": overall,
        "by_genre": by_genre,
        "by_genre_support": support,
    }
