"""Feature: mode distribution — P(mode) and P(mode | genre).

Feeds the engine's MODE node (currently major/minor via ``mode_w``). Real folk corpora
also carry dorian/mixolydian/etc. in quantity — this shows how much modal weight a
genre actually wants, beyond the binary major/minor knob.
"""
from __future__ import annotations

from featlib import conditional, histogram

NAME = "mode"
DESC = "P(mode) overall and conditioned on genre (major/minor/modal)"
REQUIRES = ("mode",)


def run(tunes):
    moded = [t for t in tunes if t.mode]
    overall = histogram([t.mode for t in moded])
    by_genre, support = conditional(
        [(t.genre, t.mode) for t in moded if t.genre])
    return {
        "n": len(moded),
        "overall": overall,
        "by_genre": by_genre,
        "by_genre_support": support,
    }
