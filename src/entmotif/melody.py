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
SIGMA = {0: 1.0, 1: 1.8, 2: 3.0}                               # documented Gaussian widths (GAUSS is the frozen form)
LEAP_NAMES = {0: "stepwise", 1: "moderate", 2: "jumpy"}

# Frozen integer Gaussian weight tables: round(exp(-e^2 / (2*sigma^2)) * 1000) for
# e = (delta - drift), one per leap setting (sigma 1.0 / 1.8 / 3.0). HARDCODED (not
# computed at import) so contour weighting is byte-identical on every platform/libm
# — this replaces math.exp(), the step-17 cross-platform determinism repair. Bump
# GRAVITY_TABLE_VERSION if these values change (it re-baselines the golden corpus).
GRAVITY_TABLE_VERSION = 1
GAUSS = {
    0: {-3: 11, -2: 135, -1: 607, 0: 1000, 1: 607, 2: 135, 3: 11},
    1: {-7: 1, -6: 4, -5: 21, -4: 85, -3: 249, -2: 539, -1: 857, 0: 1000,
        1: 857, 2: 539, 3: 249, 4: 85, 5: 21, 6: 4, 7: 1},
    2: {-11: 1, -10: 4, -9: 11, -8: 29, -7: 66, -6: 135, -5: 249, -4: 411,
        -3: 607, -2: 801, -1: 946, 0: 1000, 1: 946, 2: 801, 3: 607, 4: 411,
        5: 249, 6: 135, 7: 66, 8: 29, 9: 11, 10: 4, 11: 1},
}


def _round_div(a, b):
    """round(a / b) to the nearest integer (half away from zero), PURE INTEGER —
    no float, so the contour drift is identical on every platform."""
    if a >= 0:
        return (a + b // 2) // b
    return -((-a + b // 2) // b)
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
    drift = max(-2, min(2, _round_div(center - cur, 3))) + tendency
    if abs(prevd) >= 3:
        drift += -2 * (1 if prevd > 0 else -1)
    ml, table = MAXLEAP[leap], GAUSS[leap]
    opts = [d for d in range(-ml, ml + 1) if d != 0]
    wts = [table.get(d - drift, 0) for d in opts]             # frozen integer Gaussian (no math.exp)
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


def tag_call(center, chords2_sym, mode, key, lo, hi, bar0, chan, vel):
    """A singable CALL figure for the antiphony ('tag') bar of a call/response form.

    Replaces the dead whole-bar sustain (the v12 / earworm "static held-note bars
    read as filler" complaint: =E16 / =B16 / ^F16 carry no melodic info). The lead
    now articulates the held tone with a scale neighbour and returns to it — a real
    'calling' gesture that keeps moving while V:4 answers — instead of dwelling on one
    pitch for the whole bar. Metric-conserving (fills exactly the bar: 1+1+2 beats);
    the figure sits on chord tones at the seams so it stays consonant over the comp."""
    cp = cpcs(chords2_sym, mode, key)
    tag = snap(center, cp, lo, hi)
    nbr = step(tag, 1, mode, key, lo, hi)                     # upper scale neighbour
    if nbr == tag:                                            # at the ceiling: lean down instead
        nbr = step(tag, -1, mode, key, lo, hi)
    figs = [(tag, 1), (nbr, 1), (tag, 2)]                     # call: tone, neighbour, settle back (no dead hold)
    out, pos = [], 0.0
    for pitch, dur in figs:
        out.append(NoteEvent(chan, pitch, vel, int((bar0 * BEATS_PER_BAR + pos) * DIV), int(dur * DIV)))
        pos += dur
    return out


def cadence_bar(res, key, mode, lo, hi, bar0, chan, vel):
    d = lambda n: degree(n, key, mode, lo, hi)
    if res == "authentic":
        figs = [(d(3), 1), (d(2), 1), (d(1), 2)]
    elif res == "deceptive":
        figs = [(d(2), 1), (d(3), 1), (d(6), 2)]
    elif res == "plagal":
        figs = [(d(4), 1), (d(2), 1), (d(1), 2)]              # 4-2-1 over IV-I: resolved "amen"
    else:                                                    # half (mid-phrase only): ends open on 2
        figs = [(d(1), 1), (d(3), 1), (d(2), 2)]
    out, pos = [], 0.0
    for pitch, dur in figs:
        out.append(NoteEvent(chan, pitch, vel, int((bar0 * BEATS_PER_BAR + pos) * DIV), int(dur * DIV)))
        pos += dur
    return out


# --------------------------------------------------- motivic transformation --
# v0.8 headline: every restatement is an EXPLICIT operation on the germinal cell's
# realized shape (its scale-step intervals + rhythm), not a re-derived near-copy.
# This forbids "verbatim + cadence-swap" as the only return type (canon prior:
# compact germ, then TRANSFORM). The op is a DISCRETE, bit-bearing decision (an
# untrained ear hears "it went up / mirrored / sped up / shrank to a fragment"):
# ~2-3 reliable bits across a multi-restatement period.
TRANSFORMS = ["identity", "seq+2", "seq-2", "seq+3", "seq-3",
              "invert", "fragment", "augment", "diminish"]
TRANSFORM_W = [1, 3, 3, 2, 2, 3, 2, 2, 2]                      # identity rare; sequence/inversion favored
_SEQ_SHIFT = {"seq+2": 2, "seq-2": -2, "seq+3": 3, "seq-3": -3}


def _nearest_index(scale, pitch):
    return min(range(len(scale)), key=lambda i: abs(scale[i] - pitch))


def motif_shape(germ_notes, mode, key, lo, hi):
    """Extract the germ's reusable shape: (scale-step deltas, durations-in-beats).

    Deltas are differences of scale indices between consecutive germ notes (so the
    signature opening leap is captured as the first delta); durations are in beats.
    """
    scale = scale_tones(mode, key, lo, hi)
    idx = [_nearest_index(scale, n.pitch) for n in germ_notes]
    deltas = [idx[i] - idx[i - 1] for i in range(1, len(idx))]
    durs = [n.dur / DIV for n in germ_notes]                  # beats; germ durs are 0.25-multiples (exact)
    return deltas, durs


def choose_transform(ch, label):
    return ch.weighted(label, TRANSFORMS, TRANSFORM_W)


def _q16(beats):
    """Snap a duration to the sixteenth-note grid (>= one sixteenth). Halving an
    odd value (0.75 -> 0.375) would otherwise land OFF the grid and the tiling would
    accumulate the fraction, drifting every later onset off the beat."""
    return max(0.25, round(beats * 4) / 4.0)


def render_transform(shape, op, mode, key, lo, hi, bar0, chords2, chan, vel,
                     register_center, climax=False):
    """Realize a restatement: apply `op` to the germ shape, place it near
    `register_center` (or at the registral peak if `climax`), tile/truncate to fill
    the spanned bars, and snap strong beats to chord tones for singability.
    Returns NoteEvents; durations stay >= a 16th so the ABC tokenizer is valid."""
    deltas, durs = shape
    scale = scale_tones(mode, key, lo, hi)
    if not scale or not durs:
        return []
    span_beats = len(chords2) * BEATS_PER_BAR
    d = [-x for x in deltas] if op == "invert" else list(deltas)
    du = list(durs)
    if op == "augment":
        du = [min(BEATS_PER_BAR * 1.0, x * 2) for x in du]    # doubling stays on-grid
    elif op == "diminish":
        du = [_q16(x * 0.5) for x in du]                      # halving must re-snap to the 16th grid
    pat = [(0, du[0])] + [(d[i], du[i + 1]) for i in range(len(d))]
    if op == "fragment":
        pat = pat[:3] if len(pat) >= 3 else pat
    if climax:                                                # rhythmic activity at the peak (grid-quantized)
        pat = [(dl, _q16(dr * 0.5)) for dl, dr in pat]
    # METRIC ANCHOR: pad/trim the statement to a whole, strong-beat-aligned length
    # (1/2/4/8 beats) so when it repeats to fill the span, every repeat starts on a
    # down/strong beat — otherwise a compressed cell (e.g. 4.25 beats) shifts the
    # accents off the beat on each repeat (the "stressed<->unstressed flip").
    total = sum(dr for _, dr in pat)
    target = min((1.0, 2.0, 4.0, 8.0), key=lambda t: abs(t - total))
    pat[-1] = (pat[-1][0], max(0.25, pat[-1][1] + (target - total)))
    start_idx = (len(scale) - 1) if climax else _nearest_index(scale, register_center)
    start_idx = max(0, min(len(scale) - 1, start_idx + _SEQ_SHIFT.get(op, 0)))

    notes, pos, idx, i, first = [], 0.0, start_idx, 0, True
    while pos < span_beats - 1e-9:
        delta, dur = pat[i % len(pat)]
        if pos + dur > span_beats:
            dur = span_beats - pos
        if not first:
            idx = max(0, min(len(scale) - 1, idx + delta))
        first = False
        pitch = scale[idx]
        beat = pos - int(pos // BEATS_PER_BAR) * BEATS_PER_BAR
        if beat in (0.0, 2.0):                                # strong beat: snap to a chord tone
            b = min(int(pos // BEATS_PER_BAR), len(chords2) - 1)
            cp = cpcs(chords2[b], mode, key)
            s = snap(pitch, cp, lo, hi)
            if notes and s == notes[-1].pitch:               # anti-repeat on strong beats
                alt = [m for m in scale if m % 12 in [p % 12 for p in cp] and m != s]
                if alt:
                    s = min(alt, key=lambda m: abs(m - pitch))
            pitch = s
            idx = _nearest_index(scale, pitch)
        notes.append(NoteEvent(chan, pitch, vel,
                               int((bar0 * BEATS_PER_BAR + pos) * DIV), int(dur * DIV)))
        pos += dur
        i += 1
    return notes
