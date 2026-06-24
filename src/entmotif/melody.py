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
from entmotif.theory import cpcs, snap, snap_chord_tone, step, scale_tones, degree

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


GRAVITY_PULL = 3        # register-gravity divisor: how strongly the line is drawn back to center
DRIFT_CLAMP = 2         # the center pull is capped to +-2 scale steps per note
LEAP_THRESHOLD = 3      # a step of this many scale degrees or more counts as a leap...
LEAP_RECOVERY = 2       # ...and the next note drifts this far the OTHER way (Huron's gap-fill)


def gravity_delta(cur, center, tendency, prevd, leap, ch, label):
    """Choose the next scale-step delta: a register-gravity DRIFT (pull toward the
    arc center, plus the global tendency and a post-leap recovery) biases a frozen
    integer Gaussian over the allowed steps, then the Chooser picks one."""
    pull = _round_div(center - cur, GRAVITY_PULL)
    drift = max(-DRIFT_CLAMP, min(DRIFT_CLAMP, pull)) + tendency
    if abs(prevd) >= LEAP_THRESHOLD:                          # after a leap, lean back to fill the gap
        drift += -LEAP_RECOVERY if prevd > 0 else LEAP_RECOVERY
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
                    if notes:
                        s = snap_chord_tone(cur, cp, scale_tones(mode, key, lo, hi),
                                            s, notes[-1][1])
                    cur = s
            notes.append(NoteEvent(chan, cur, vel, int((bar0 * BEATS_PER_BAR + pos) * DIV), int(dur * DIV)))
            pos += dur
    return notes


line = generate_melodic_line   # legacy alias (call sites migrate during engine extraction)


# --------------------------------------------------- phrasing / breath -------
# fw4 (Group B #4, this.i:b3r8k1m7, the #1 lyricism lever): a line BREATHES by phrase
# length, not form structure: a singable line BREATHES as a function of
# PHRASE LENGTH, not form structure. The engine used to pack bars wall-to-wall (lead
# runs of 24-48 sounded notes with a rest only at a form-template boundary), so the
# antecedent never breathed into the consequent mid-section. `breathe` inserts a
# comma-length rest after at most ~BREATH_EVERY sounded notes by SHORTENING a note
# (onsets are never moved), so the bar's total duration and the 16th grid are
# preserved (this.i:m9p3k7a2) — the rest is the silence the trim opens up before the
# next onset. The breath lands on the note ending a beat (so it falls between phrase
# limbs, not mid-figure) and only when trimming still leaves a sounding sixteenth.
BREATH_EVERY = 9                                               # comma after ~7-12 notes (singable phrase length)
BREATH_LEN = DIV // 2                                          # an eighth-rest comma (the breath we aim to open)
MIN_SOUND = DIV // 4                                           # always leave >= a sixteenth sounding
MIN_GAP = DIV // 4                                             # a real breath is at least a sixteenth of silence
#   (a sixteenth-rest is a genuine comma in a fast sixteenth run; we open a full eighth
#    whenever a note in the window can spare it, and fall back to a sixteenth otherwise)


def breathe(notes, every=BREATH_EVERY):
    """Open comma-length breaths in a single voice's line so no run of sounded notes
    (those with no following gap) exceeds `every`. Trims a note's duration only —
    onsets are untouched, so metric conservation and the 16th grid hold. Returns the
    (possibly modified) note list, sorted by onset.

    When overdue for a comma we breathe on a note in the recent run window that can
    spare a full eighth (preferring one ending on a beat boundary, so the rest falls
    between phrase limbs rather than mid-figure; then the longest). If no note can
    spare a full eighth we take the longest one that can spare a sixteenth — that
    note's run resets even though the gap is shorter, so the line still loosens; the
    next overdue point opens another. Shortening minimizes the audible loss while
    still opening a clear rest."""
    if len(notes) <= every:
        return notes
    seq = sorted(notes, key=lambda n: n.start)
    run, run_start = 0, 0
    for i in range(len(seq) - 1):
        gap = seq[i + 1].start - (seq[i].start + seq[i].dur)
        if gap >= MIN_GAP:                                    # an existing breath resets the run
            run, run_start = 0, i + 1
            continue
        run += 1
        if run >= every:                                      # overdue for a comma: open a rest in the window
            window = range(max(run_start, i - every + 1), i + 1)
            full = [j for j in window if seq[j].dur - BREATH_LEN >= MIN_SOUND]  # can spare a full eighth
            cands = full or [j for j in window if seq[j].dur - DIV // 4 >= MIN_SOUND]
            if cands:
                # prefer a beat-ending note (rest between limbs), then the LATEST one in
                # the window — keeping the reset close to here bounds the next run by `every`.
                j = max(cands, key=lambda j: ((seq[j].start + seq[j].dur) % DIV == 0, j))
                trim = min(BREATH_LEN, seq[j].dur - MIN_SOUND)
                seq[j] = seq[j]._replace(dur=seq[j].dur - trim)
                run, run_start = i - j, j + 1                  # notes after the breath are already a fresh run
    return seq


# --------------------------------------------------- de-stutter --------------
# fw6 (singability, convergent prior finding "machine-gun repeated note / unsingable
# patter"): even with the strong-beat anti-repeat (snap_chord_tone), the jumpy/patter
# generation paths and cell-tiling can leave a run of 3+ identical lead pitches
# ("=c =c =c", an octave-toggle that collapses, a re-snapped tag) — a register-stutter
# no voice would phrase. `destutter` is a PURE post-pass on one voice's line: when a
# 3rd consecutive identical pitch appears it nudges that note to an ADJACENT scale tone
# (onset + duration untouched, so the 16th grid and metric conservation hold,
# this.i:m9p3k7a2). It prefers the neighbour that moves TOWARD the register center
# (keeping the contour sane) and never re-collides with the note on either side, so the
# cap is a hard <=2 consecutive same-pitch repeats without disturbing rhythm.
def destutter(notes, scale, center):
    """Cap consecutive same-pitch repeats in one voice at 2 by nudging the 3rd+ note to
    an adjacent scale tone. Pure (pitch-only); onsets/durations are never touched."""
    if len(notes) < 3 or not scale:
        return notes
    seq = sorted(notes, key=lambda n: n.start)
    lo, hi = scale[0], scale[-1]
    for i in range(2, len(seq)):
        if seq[i].pitch != seq[i - 1].pitch or seq[i - 1].pitch != seq[i - 2].pitch:
            continue
        p = seq[i].pitch
        j = min(range(len(scale)), key=lambda k: abs(scale[k] - p))
        up = scale[min(len(scale) - 1, j + 1)]
        down = scale[max(0, j - 1)]
        nxt = seq[i + 1].pitch if i + 1 < len(seq) else None
        # prefer the neighbour toward the register center; fall back to the other; never
        # equal to the previous note (would extend the run) or the following note.
        order = [down, up] if center < p else [up, down]
        for cand in order:
            if cand != p and cand != seq[i - 1].pitch and cand != nxt:
                seq[i] = seq[i]._replace(pitch=cand)
                break
    return seq


def _lay_figure(figs, bar0, chan, vel):
    """Lay a sequence of ``(pitch, beats)`` onto consecutive onsets starting at
    ``bar0``, returning NoteEvents. Shared by the singable cells (`tag_call`,
    `cadence_bar`) that fill a bar from a fixed pitch/duration figure."""
    out, pos = [], 0.0
    for pitch, dur in figs:
        out.append(NoteEvent(chan, pitch, vel,
                             int((bar0 * BEATS_PER_BAR + pos) * DIV), int(dur * DIV)))
        pos += dur
    return out


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
    return _lay_figure(figs, bar0, chan, vel)


# fw5 (Group B #4, "cadential interchangeability is the #1 memorability killer"):
# the engine ended almost every piece with the IDENTICAL approach to the tonic (3-2-1:
# two stepwise quarters falling into the half-note tonic), so two inputs were
# indistinguishable by their endings. The cadence APPROACH is now a small FAMILY of
# valid, resolving figures, drawn per-input — so the cadence becomes a per-piece
# signature, not a shared stamp. Every authentic/plagal approach STILL lands on the
# tonic (degree 1) as its final note, so the resolved-final invariant is untouched; all
# figures fill exactly the bar (metric conservation, this.i:m9p3k7a2). Each figure is a
# list of (scale-degree, beats) pairs; the LAST pair is the half-note resolution tone.
# A "+7"/"-..." entry leaps from the leading-tone/lower neighbour for a pointed approach.
CADENCE_APPROACHES = {
    "authentic": [
        [(3, 1), (2, 1), (1, 2)],          # 0: stepwise descent (the canonical 3-2-1)
        [(5, 1), (3, 1), (1, 2)],          # 1: arpeggiated descent (5-3-1, gentle)
        [(2, 1), (-1, 1), (1, 2)],         # 2: leading-tone resolution (2-7-1, pointed)
        [(1, 0.5), (3, 0.5), (2, 1), (1, 2)],   # 3: anacrusis turn into 3-2-1
        [(5, 1), (-1, 1), (1, 2)],         # 4: leap down then leading-tone (5-7-1)
        [(4, 1), (2, 1), (1, 2)],          # 5: 4-2-1 falling-fourth approach
        [(2, 0.5), (1, 0.5), (3, 1), (1, 2)],   # 6: appoggiatura (lean 2->1, reach 3, settle 1)
        [(6, 1), (5, 1), (1, 2)],          # 7: high approach 6-5-1 (a reach before the close)
    ],
    "plagal": [
        [(4, 1), (2, 1), (1, 2)],          # 0: 4-2-1 "amen"
        [(6, 1), (4, 1), (1, 2)],          # 1: 6-4-1 plagal reach
        [(4, 1), (3, 1), (1, 2)],          # 2: 4-3-1 suspension-style
        [(4, 0.5), (5, 0.5), (4, 1), (1, 2)],   # 3: neighbour-decorated 4 into 1
        [(2, 1), (4, 1), (1, 2)],          # 4: rise to 4 then resolve
        [(4, 1), (6, 1), (1, 2)],          # 5: 4 up to 6 then settle (plagal arch)
        [(5, 1), (4, 1), (1, 2)],          # 6: 5-4-1 over IV-I
        [(4, 0.5), (3, 0.5), (2, 1), (1, 2)],   # 7: stepwise 4-3-2-1 amen descent
    ],
    "deceptive": [                          # deceptive ends OPEN on 6 (no tonic landing)
        [(2, 1), (3, 1), (6, 2)],
        [(1, 1), (2, 1), (6, 2)],
        [(3, 1), (4, 1), (6, 2)],
        [(5, 1), (4, 1), (6, 2)],
    ],
    "half": [                               # half cadence (mid-phrase only): ends open on 2
        [(1, 1), (3, 1), (2, 2)],
        [(3, 1), (1, 1), (2, 2)],
        [(1, 1), (4, 1), (2, 2)],
        [(4, 1), (3, 1), (2, 2)],
    ],
}


def cadence_bar(res, key, mode, lo, hi, bar0, chan, vel, approach=0):
    """Render the cadential bar. `approach` selects from a small family of valid,
    resolving approach figures (input-derived by the engine) so the cadence is a
    per-piece signature rather than a shared stamp. Authentic/plagal approaches all
    land on the tonic (degree 1); each figure fills exactly the bar."""
    d = lambda n: degree(n, key, mode, lo, hi)
    fam = CADENCE_APPROACHES.get(res, CADENCE_APPROACHES["half"])
    deg_figs = fam[approach % len(fam)]
    figs = [(d(n), beats) for n, beats in deg_figs]
    return _lay_figure(figs, bar0, chan, vel)


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

# Development character conditioned on emotion (this.i:d2k9m4p1 / a7k0m3p9): an ANGULAR
# affect (tense) develops the germ by inversion/fragmentation/diminution (restless,
# broken); a GENTLE affect (sad/peaceful/tender) prefers sequence + augmentation (smooth,
# stretched). identity stays rare regardless (never a verbatim restatement).
TRANSFORM_ANGULAR = {"invert", "fragment", "diminish"}
TRANSFORM_GENTLE = {"seq+2", "seq-2", "seq+3", "seq-3", "augment"}
TRANSFORM_EMPHASIS = 3                                         # how strongly the affect lifts its preferred group


def transform_weights(angular):
    """TRANSFORM_W tilted by an `angular` cue: +1 lifts the angular ops, -1 the gentle
    ops, 0 leaves the base. Every op stays reachable (entropy picks the CDF point)."""
    if angular == 0:
        return list(TRANSFORM_W)
    pref = TRANSFORM_ANGULAR if angular > 0 else TRANSFORM_GENTLE
    return [w * TRANSFORM_EMPHASIS if t in pref else w for t, w in zip(TRANSFORMS, TRANSFORM_W)]


def _nearest_index(scale, pitch):
    return min(range(len(scale)), key=lambda i: abs(scale[i] - pitch))


def _clamp_index(scale, i):
    """Keep a scale index in range (the contour walks off neither end of the scale)."""
    return max(0, min(len(scale) - 1, i))


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


def choose_transform(ch, label, weights=None):
    return ch.weighted(label, TRANSFORMS, TRANSFORM_W if weights is None else weights)


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
    start_idx = _clamp_index(scale, start_idx + _SEQ_SHIFT.get(op, 0))

    notes, pos, idx, i, first = [], 0.0, start_idx, 0, True
    while pos < span_beats - 1e-9:
        delta, dur = pat[i % len(pat)]
        if pos + dur > span_beats:
            dur = span_beats - pos
        if not first:
            idx = _clamp_index(scale, idx + delta)
        first = False
        pitch = scale[idx]
        beat = pos - int(pos // BEATS_PER_BAR) * BEATS_PER_BAR
        if beat in (0.0, 2.0):                                # strong beat: snap to a chord tone
            b = min(int(pos // BEATS_PER_BAR), len(chords2) - 1)
            cp = cpcs(chords2[b], mode, key)
            s = snap(pitch, cp, lo, hi)
            if notes:                                         # anti-repeat on strong beats
                s = snap_chord_tone(pitch, cp, scale, s, notes[-1].pitch)
            pitch = s
            idx = _nearest_index(scale, pitch)
        notes.append(NoteEvent(chan, pitch, vel,
                               int((bar0 * BEATS_PER_BAR + pos) * DIV), int(dur * DIV)))
        pos += dur
        i += 1
    return notes
