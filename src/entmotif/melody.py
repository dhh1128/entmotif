"""entmotif melody — rhythmic vocabulary, dynamic arc, and line generation.

Renders a Phrase's melodic line: rhythm figures + a register-gravity contour
(`gravity_delta`) snapped to chord tones on strong beats, the signature opening
leap, and the cadential close (`cadence_bar`). Dynamics (`unit_dyn`/`DYN_VEL`)
shape the velocity/expression arc.

NOTE (refactor debt, deferred to the v0.8 onset-rhythm rewrite): the public
`generate_melodic_line` still takes the historical 18-argument clump rather than a
MelodyContext parameter object. Bundling it now would be churn — Phase 2 replaces
this rhythm model wholesale, which is the right moment to introduce the context.
"""
import math

from entmotif.model import DIV, BEATS_PER_BAR, NoteEvent
from entmotif.theory import cpcs, snap, step, scale_tones, degree

FIGURES = [
    [1, 1, 2], [2, 1, 1], [1, 2, 1], [1.5, 0.5, 2], [2, 1.5, 0.5],
    [0.5, 0.5, 1, 2], [1, 0.5, 0.5, 2], [0.5, 0.5, 1, 1, 1], [1, 1, 0.5, 0.5, 1],
    [0.75, 0.25, 1, 1, 1], [0.5, 0.5, 0.5, 0.5, 2], [2, 0.5, 0.5, 1],
]
HOOKS = [                                                      # signature idea-bar rhythms (dotted/syncopated)
    [1.5, 0.5, 1, 1], [0.5, 1.5, 1, 1], [1, 0.5, 0.5, 2],
    [0.75, 0.25, 1, 2], [0.5, 0.5, 1, 1.5, 0.5], [2, 0.5, 0.5, 1],
]
SIG_STEPS = {0: [2, -2, 3, -3], 1: [3, 4, -3, 5, -4], 2: [4, 5, 7, -5, -4]}
BREATHS = [0, 0, 0.5, 1, 1, 1.5]
MAXLEAP = {0: 3, 1: 5, 2: 8}
SIGMA = {0: 1.0, 1: 1.8, 2: 3.0}
LEAP_NAMES = {0: "stepwise", 1: "moderate", 2: "jumpy"}
DYN_VEL = {"p": 62, "mp": 78, "mf": 94, "f": 110, "ff": 120}   # dynamic mark -> MIDI velocity


def unit_dyn(u, nU, peak):
    """Dynamic arc: ramp into the placed climax, settle at the final cadence."""
    if u == peak:
        return "f"
    if u == nU - 1:
        return "mf"
    if u < peak:
        return "mf" if u == peak - 1 else "mp"
    return "mp"


def gravity_delta(cur, center, tendency, prevd, leap, ch, label):
    drift = max(-2, min(2, round((center - cur) / 3.0))) + tendency
    if abs(prevd) >= 3:
        drift += -2 * (1 if prevd > 0 else -1)
    ml, sig = MAXLEAP[leap], SIGMA[leap]
    opts = [d for d in range(-ml, ml + 1) if d != 0]
    wts = [math.exp(-((d - drift) ** 2) / (2 * sig * sig)) for d in opts]
    return ch.weighted(label, opts, wts)


def generate_melodic_line(figs, chords2, mode, key, base, lo, hi, bar0, center, tendency, leap, ch,
                          tag, offset, invert, sig, chan, vel):
    notes, cur, pos, k, prevd = [], None, 0.0, 0, 0
    for b, fig in enumerate(figs):
        cp = cpcs(chords2[b], mode, key)
        for dur in fig:
            beat = pos - b * BEATS_PER_BAR
            if cur is None:
                cur = snap(base, cp, lo, hi)
                if offset:
                    cur = snap(step(cur, offset, mode, key, lo, hi), cp, lo, hi)
            else:
                if k == 0 and sig is not None:                # signature opening leap (hook)
                    d = -sig if invert else sig
                else:
                    d = gravity_delta(cur, center, tendency, prevd, leap, ch,
                                      "%s_d%d" % (tag, k))
                    if invert:
                        d = -d
                cur = step(cur, d, mode, key, lo, hi)
                prevd = d
                k += 1
                if beat in (0.0, 2.0):
                    s = snap(cur, cp, lo, hi)
                    if notes and s == notes[-1][1]:
                        alt = [m for m in scale_tones(mode, key, lo, hi)
                               if m % 12 in [p % 12 for p in cp] and m != s]
                        if alt:
                            s = min(alt, key=lambda m: abs(m - cur))
                    cur = s
            notes.append(NoteEvent(chan, cur, vel, int((bar0 * BEATS_PER_BAR + pos) * DIV), int(dur * DIV)))
            pos += dur
    return notes


line = generate_melodic_line   # legacy alias (call sites migrate during engine extraction)


def cadence_bar(res, key, mode, lo, hi, bar0, chan, vel):
    d = lambda n: degree(n, key, mode, lo, hi)
    if res == "authentic":
        figs = [(d(3), 1), (d(2), 1), (d(1), 2)]
    elif res == "deceptive":
        figs = [(d(2), 1), (d(3), 1), (d(6), 2)]
    else:
        figs = [(d(1), 1), (d(3), 1), (d(2), 2)]
    out, pos = [], 0.0
    for pitch, dur in figs:
        out.append(NoteEvent(chan, pitch, vel, int((bar0 * BEATS_PER_BAR + pos) * DIV), int(dur * DIV)))
        pos += dur
    return out
