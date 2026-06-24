"""Feature: register-per-instrument — P(pitch | GM program) (the other clear first win).

Directly fixes the flute-salsa failure (this.i:d2k9m4p1): a lead's register must be
CONDITIONED on the chosen instrument's real tessitura. For every GM program seen in the
corpus, emits the pitch percentiles (p5..p95) and the playing-range center — exactly the
(lo, hi, center) the engine's PitchRange wants, but data-derived per instrument instead
of hand-set per style.
"""
from __future__ import annotations

from collections import defaultdict

from featlib import percentiles

NAME = "register"
DESC = "P(pitch | GM program): per-instrument tessitura percentiles from real parts"
REQUIRES = ("notes",)


def run(tunes):
    by_prog = defaultdict(list)
    for t in tunes:
        for n in t.notes:
            if n.program is not None:           # channel 9 (drums) carries program=None
                by_prog[n.program].append(n.pitch)
    out = {"n_tunes": len(tunes), "by_program": {}}
    for prog, pitches in sorted(by_prog.items()):
        if len(pitches) < 20:                   # too thin to trust a tessitura
            continue
        pct = percentiles(pitches)
        out["by_program"][str(prog)] = {
            "n_notes": len(pitches),
            "lo": pct.get("p5"),
            "center": pct.get("p50"),
            "hi": pct.get("p95"),
            "percentiles": pct,
        }
    return out
