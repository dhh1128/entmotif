#!/usr/bin/env python3
"""entmotif engine tests (zero-dep, assert-based). Run: python3 test_motif.py

Pins the SACRED invariants (determinism, avalanche) and the round-4 (v0.7)
fixes: bass chord-quality, lead never over-silent, final cadence resolves,
dynamics emitted. Exits nonzero on any failure.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import motif                                                    # noqa: E402

DIV = motif.DIV
CORPUS = [ln.strip() for ln in open(os.path.join(HERE, "..", "teaching", "corpus.txt"))
          if ln.strip() and not ln.startswith("#")]

fails = []
def check(cond, msg):
    if not cond:
        fails.append(msg)


def bar_chord_pcs(m, bar):
    s = m["bar_chords"][bar]
    return [p % 12 for p in motif.cpcs(s, m["mode"], m["key"])]


# --- SACRED: determinism (same input -> identical notes, meta, MIDI bytes) ---
for v in CORPUS:
    n1, m1 = motif.generate(v)
    n2, m2 = motif.generate(v)
    check(n1 == n2 and m1 == m2, "determinism(notes/meta): %s" % v)
    motif.write_midi(n1, m1, "/tmp/_a.mid")
    motif.write_midi(n2, m2, "/tmp/_b.mid")
    check(open("/tmp/_a.mid", "rb").read() == open("/tmp/_b.mid", "rb").read(),
          "determinism(midi bytes): %s" % v)

# --- SACRED: avalanche (one-char change -> different motif) ---
na, _ = motif.generate("did:example:alice")
nb, _ = motif.generate("did:example:alife")
check(na != nb, "avalanche: alice vs alife identical")

# --- round-4 (v0.9-relaxed): the bass DOWNBEAT grounds the harmony (a chord tone).
#     Mid-bar bass may use idiomatic 6th/b7/passing tones (boogie, walking, funk). ---
for v in CORPUS:
    notes, m = motif.generate(v)
    for (chan, pitch, vel, start, dur) in notes:
        if int(chan) == 2 and start % (4 * DIV) == 0:
            bar = start // (4 * DIV)
            if bar < m["bars"]:
                pcs = bar_chord_pcs(m, bar)
                check(pitch % 12 in pcs,
                      "bass downbeat non-chord-tone: %s bar%d pc%d not in %s" % (v, bar, pitch % 12, pcs))

# --- v0.10: an AUTHENTIC final resolves to the tonic triad; half/deceptive finals
#     are deliberately open (maintainer wants cadence variety, not always a full close) ---
for v in CORPUS:
    notes, m = motif.generate(v)
    if m.get("final_cad") not in ("authentic", "plagal"):     # deceptive (V->vi) deliberately doesn't land on I
        continue
    mel = [n for n in notes if int(n[0]) in (0, 3)]
    last = max(mel, key=lambda n: n[3])
    tonic = [p % 12 for p in motif.cpcs("I" if m["mode"] == "major" else "i", m["mode"], m["key"])]
    check(last[1] % 12 in tonic,
          "resolved final (%s) not on tonic: %s ends on pc%d (tonic triad %s)"
          % (m["final_cad"], v, last[1] % 12, tonic))

# --- v0.8: lead (chan 0) present in EVERY bar (per-BAR, tighter than round-4's
#          per-unit check) except the groove_first 2-bar intro (fixes the z16 hole) ---
for v in CORPUS:
    notes, m = motif.generate(v)
    for b in range(m["bars"]):
        if m["arr"] == "groove_first" and b < 2:
            continue
        lo, hi = b * 4 * DIV, (b + 1) * 4 * DIV
        check(any(int(n[0]) == 0 and lo <= n[3] < hi for n in notes),
              "lead silent in bar %d: %s (arr=%s)" % (b, v, m["arr"]))

# --- round-4: dynamics emitted in ABC ---
for v in CORPUS:
    notes, m = motif.generate(v)
    check("!" in motif.abc_export(v, notes, m), "no dynamics in ABC: %s" % v)


def lead_per_unit(notes, m):
    """(pitch, dur) tuples of the lead (chan 0), grouped per 2-bar unit."""
    out = []
    for u in range(m["bars"] // 2):
        lo, hi = u * 2 * 4 * DIV, (u + 1) * 2 * 4 * DIV
        out.append(tuple((n[1], n[4]) for n in sorted(notes) if int(n[0]) == 0 and lo <= n[3] < hi))
    return out


# --- v0.8 (THE change): real motivic transformation — restatements are NOT verbatim.
#     With >=2 non-empty lead units, at least two distinct realized shapes must appear. ---
for v in CORPUS:
    notes, m = motif.generate(v)
    units = [u for u in lead_per_unit(notes, m) if u]
    if len(units) >= 2:
        check(len(set(units)) >= 2, "verbatim restatement (no transform): %s" % v)

# --- v0.8: V:4 (chan 3) DEVELOPS when present — a real line (>=2 distinct pitches),
#     not a static echo; and not pitch-identical to the whole lead. ---
for v in CORPUS:
    notes, m = motif.generate(v)
    if m["v4"]:
        v4 = [n[1] for n in sorted(notes) if int(n[0]) == 3]
        lead = [n[1] for n in sorted(notes) if int(n[0]) == 0]
        check(len(set(v4)) >= 2, "V:4 static (not developed): %s" % v)
        check(v4 != lead, "V:4 is a verbatim echo of the lead: %s" % v)

# --- fw3 (Group B #4, earworm "static held-note bars read as filler, not hook"):
#     the lead never DEAD-HOLDS one pitch for a whole bar. A whole-bar single sustain
#     (the call_resp "tag" bar emitted =E16 / =B16 / ^F16 etc., and any augmented
#     restatement that tiled to one long note) carries no melodic info — cap a single
#     held lead note below the full bar and give the long value a neighbour/turn so the
#     line keeps moving. Allowed ONLY at the placed climax bar (a deliberate peak). ---
for v in CORPUS:
    notes, m = motif.generate(v)
    nU = m["bars"] // 2
    peak = max(1, ((nU - 1) * 2 + 1) // 3)
    bar = 4 * DIV
    for b in range(m["bars"]):
        if b == peak * 2:                                     # the placed climax may dwell on its peak
            continue
        lo, hi = b * bar, (b + 1) * bar
        ld = [n for n in notes if int(n[0]) == 0 and lo <= n[3] < hi]
        if len(ld) == 1 and ld[0][4] >= bar:
            check(False, "lead dead-holds a whole bar (static, not a hook): %s bar%d pitch%d"
                  % (v, b, ld[0][1]))

# --- fw4 (Group B #4, the #1 lyricism lever: "BREATH IS AN AFTERTHOUGHT, NOT PHRASING").
#     The engine packed bars wall-to-wall (lead runs of 24-48 sounded notes with no rest;
#     breath only landed at a form-template boundary). A singable line BREATHES as a
#     function of PHRASE LENGTH: after at most ~12 sounded notes the line must take a
#     comma-length rest (a sixteenth-rest comma in a fast run, a full eighth wherever
#     a note can spare it) so the antecedent breathes into the consequent even
#     mid-section. Assert the lead never runs more than BREATH_MAX consecutive sounded
#     notes without an intra-line breath gap. A breath is a SHORTENED note (onsets
#     unchanged), so metric conservation / the 16th grid are untouched. ---
BREATH_MAX = 12
COMMA = DIV // 4                                               # a sixteenth-rest is the minimum audible comma
for v in CORPUS:
    notes, m = motif.generate(v)
    lead = sorted((n for n in notes if int(n[0]) == 0), key=lambda n: n[3])
    run, worst = 0, 0
    for a, b in zip(lead, lead[1:]):
        gap = b[3] - (a[3] + a[4])
        if gap >= COMMA:
            run = 0
        else:
            run += 1
            worst = max(worst, run + 1)                        # +1: the run includes the note we land on
    check(worst <= BREATH_MAX,
          "lead runs %d notes with no breath (>%d): %s — breath must phrase, not pack" % (worst, BREATH_MAX, v))

# --- v0.8: unified climax — exactly ONE bar carries !f!, and it is the placed peak
#     unit (~2/3 through, Huron arch), with lead activity there. ---
for v in CORPUS:
    notes, m = motif.generate(v)
    nU = m["bars"] // 2
    peak = max(1, ((nU - 1) * 2 + 1) // 3)
    f_bars = [b for b, d in m["dyn_bars"].items() if d == "f"]
    check(len(f_bars) == 1, "climax !f! not unique: %s (%s)" % (v, f_bars))
    if f_bars:
        check(f_bars[0] == peak * 2, "climax !f! not at the placed peak: %s" % v)
    lo, hi = peak * 2 * 4 * DIV, (peak + 1) * 2 * 4 * DIV
    check(any(int(n[0]) == 0 and lo <= n[3] < hi for n in notes),
          "no lead activity at the climax: %s" % v)

# --- v0.11: the groove/comp is CONSTANT (present in every unit, except at most a
#     single groove_first/art-style intro unit) — v0.10's flickering broke the groove. ---
for v in CORPUS:
    notes, m = motif.generate(v)
    nU = m["bars"] // 2
    comp_units = sum(1 for u in range(nU)
                     if any(int(n[0]) == 1 and u * 2 * 4 * DIV <= n[3] < (u + 1) * 2 * 4 * DIV
                            for n in notes))
    check(comp_units >= nU - 1, "comp/groove not constant: %s (%d/%d units)" % (v, comp_units, nU))

# --- v0.9: STYLE is a real, varied master dimension (>=14 idioms, all reachable). ---
import entmotif.arrangement as arr  # noqa: E402
seen_styles = {motif.generate("style-probe-%d" % i)[1]["style"] for i in range(3000)}
check(len(arr.STYLE_NAMES) >= 14, "fewer than 14 styles: %d" % len(arr.STYLE_NAMES))
check(seen_styles == set(arr.STYLE_NAMES),
      "not every style reachable from the fingerprint: missing %s" % (set(arr.STYLE_NAMES) - seen_styles))

# --- c2k9p0a4: comp/bass INSTRUMENT variety + capability gate (mirror the LEAD model).
#     comp/bass are no longer one fixed program per style: a capability-tagged pool +
#     per-style affinity + a role capability gate. An offbeat/plucked groove (reggae
#     skank, funk, walking, stride...) REQUIRES a sharp-attack timbre; a sustained
#     organ/pad can't articulate it, so it must never be offered for that role. ---
SHARP_BASS_PATS = {"reggae", "funk", "tumbao", "samba", "boogie"}
SHARP_COMP_PATS = {"skank", "funk16", "montuno"}
for st in arr.STYLE_NAMES:
    bprogs, bwts = arr.bass_choices(st)
    cprogs, cwts = arr.comp_choices(st)
    check(len(bprogs) == len(bwts) and len(bprogs) >= 1, "bass_choices malformed: %s" % st)
    check(len(cprogs) == len(cwts) and len(cprogs) >= 1, "comp_choices malformed: %s" % st)
    # capability gate: a sharp-attack groove never offers a sustained-only timbre
    if arr.STYLES[st]["bass_pat"] in SHARP_BASS_PATS:
        for p in bprogs:
            check(arr.BASS_ATTACK.get(p, 2) >= 1,
                  "sustained bass offered for sharp groove: %s prog%d (%s)" % (st, p, arr.gm_name(p)))
    if arr.STYLES[st]["comp_pat"] in SHARP_COMP_PATS:
        for p in cprogs:
            check(arr.COMP_ATTACK.get(p, 2) >= 1,
                  "sustained comp offered for sharp groove: %s prog%d (%s)" % (st, p, arr.gm_name(p)))

# --- c2k9p0a4: comp/bass programs VARY across inputs within a style (not one fixed
#     program), and the signature stays dominant (affinity). Probe many inputs. ---
from collections import defaultdict as _ddv  # noqa: E402
comp_seen, bass_seen = _ddv(set), _ddv(set)
for i in range(1500):
    _n, _m = motif.generate("cb-probe-%d" % i)
    comp_seen[_m["style"]].add(_m["comp_prog"])
    bass_seen[_m["style"]].add(_m["bass_prog"])
multi_comp = sum(1 for st in comp_seen if len(comp_seen[st]) >= 2)
multi_bass = sum(1 for st in bass_seen if len(bass_seen[st]) >= 2)
check(multi_comp >= 8, "comp instrument barely varies: only %d styles show >=2 comp programs" % multi_comp)
check(multi_bass >= 8, "bass instrument barely varies: only %d styles show >=2 bass programs" % multi_bass)

# --- c2k9p0a4 / v12 #03: the MARCH comp "pah" must not be a brass stab ("collection of
#     horns" oom-pah is ugly) — make it a lighter/lower voice, not brass/trumpet. ---
march_cprogs, _ = arr.comp_choices("march")
for p in march_cprogs:
    check(p not in (56, 57, 59, 61),
          "march comp is a brass stab (ugly oom-pah): prog%d (%s)" % (p, arr.gm_name(p)))

# --- A3 (v12 #03): the oom-pah "pah" is LIGHTER than the full block chord — the bass
#     plays the "oom" low, so the comp "pah" drops its lowest voice (no doubling into
#     the tuba register that muddied the "collection of horns") and sounds fewer voices
#     than the full voicing. Metric conservation is unaffected (same onsets/durations). ---
_full = arr.voice_chord([0, 4, 7], 2, 72)                       # a 4-voice voicing
check(len(_full) >= 3, "test setup: voicing too thin to lighten")
for _pat in ("oompah", "oompah_push"):
    _ev = arr.comp_groove(_pat, _full, 0, 80, False)
    _bottom = min(_full)
    check(all(n.pitch != _bottom for n in _ev),
          "oom-pah '%s' still doubles the bass-register bottom voice (%d): %s"
          % (_pat, _bottom, sorted({n.pitch for n in _ev})))
    # the pah sounds strictly fewer voices than the full block chord (it is lighter)
    _pah_voices = len({n.pitch for n in _ev})
    check(0 < _pah_voices < len(_full),
          "oom-pah '%s' pah is not lighter than the full chord: %d of %d voices"
          % (_pat, _pah_voices, len(_full)))

# --- A2 (v12 #08, this.i:r4d8m1k6): comp/bass RHYTHM-pattern variety. The groove is
#     no longer one fixed rhythm per style: each style's signature comp/bass pattern
#     belongs to a small family of idiomatic, metric-CONSERVING variants, chosen by
#     the fingerprint (signature dominant, variants reachable-but-rare). So the same
#     style's groove rhythm differs across inputs instead of always strong/weak. ---
#  (a) every declared variant conserves the bar's total duration (this.i:m9p3k7a2) and
#      stays on the 16th grid; the signature base pattern is always in its own family.
_VOIC = arr.voice_chord([0, 4, 7], 1, 72)
_BAR = 4 * DIV
for base, variants in arr.COMP_PAT_VARIANTS.items():
    pats, wts = variants
    check(base in pats, "comp base pattern not in its own family: %s" % base)
    check(len(pats) == len(wts) and len(pats) >= 1, "COMP_PAT_VARIANTS malformed: %s" % base)
    for pat in pats:
        ev = arr.comp_groove(pat, _VOIC, 0, 80, False)
        for n in ev:
            check(n[3] % (DIV // 4) == 0, "comp variant %s off-grid onset %d" % (pat, n[3]))
            check(n[3] + n[4] <= _BAR + 1, "comp variant %s overruns the bar" % pat)
for base, variants in arr.BASS_PAT_VARIANTS.items():
    pats, wts = variants
    check(base in pats, "bass base pattern not in its own family: %s" % base)
    check(len(pats) == len(wts) and len(pats) >= 1, "BASS_PAT_VARIANTS malformed: %s" % base)
    for pat in pats:
        ev = arr.bass_groove(pat, [0, 4, 7], 7, 0, 80)
        tot = 0
        for n in ev:
            check(n[3] % (DIV // 4) == 0, "bass variant %s off-grid onset %d" % (pat, n[3]))
            check(n[3] + n[4] <= _BAR + arr.SUSTAIN_GAP + 1, "bass variant %s overruns the bar" % pat)
        check(any(n[3] == 0 for n in ev), "bass variant %s has no downbeat note" % pat)
#  (b) at least one variant exists beyond the signature for several styles, and the
#      rendered comp/bass rhythm actually VARIES across inputs within a style.
multi_fam_comp = sum(1 for b in arr.COMP_PAT_VARIANTS if len(arr.COMP_PAT_VARIANTS[b][0]) >= 2)
multi_fam_bass = sum(1 for b in arr.BASS_PAT_VARIANTS if len(arr.BASS_PAT_VARIANTS[b][0]) >= 2)
check(multi_fam_comp >= 4, "too few comp pattern families have a variant: %d" % multi_fam_comp)
check(multi_fam_bass >= 4, "too few bass pattern families have a variant: %d" % multi_fam_bass)
_cpat_seen, _bpat_seen = _ddv(set), _ddv(set)
for i in range(1500):
    _n, _m = motif.generate("rhythm-probe-%d" % i)
    _cpat_seen[_m["style"]].add(_m.get("comp_pat"))
    _bpat_seen[_m["style"]].add(_m.get("bass_pat"))
multi_cpat = sum(1 for st in _cpat_seen if len(_cpat_seen[st]) >= 2)
multi_bpat = sum(1 for st in _bpat_seen if len(_bpat_seen[st]) >= 2)
check(multi_cpat >= 4, "comp rhythm barely varies: only %d styles show >=2 comp patterns" % multi_cpat)
check(multi_bpat >= 4, "bass rhythm barely varies: only %d styles show >=2 bass patterns" % multi_bpat)

# --- fw5 (Group B #4, "Cadential interchangeability is the #1 memorability killer"):
#     the engine ended almost every piece with the IDENTICAL approach to the tonic — a
#     two-stepwise-quarters-falling-into-a-half-note-tonic cell (3-2-1: down-2, down-2).
#     A listener could not tell two inputs apart by their endings. The final cadence's
#     APPROACH must be INPUT-DERIVED (vary the approach interval / leap-to-tonic /
#     leading-tone / appoggiatura) so the cadence is a per-piece signature, not a shared
#     stamp — while STILL resolving (the resolved-final invariant above is unchanged:
#     authentic/plagal land on the tonic). Assert: (a) the cadence figure is a pure
#     function of an input-derived "cadence approach" id, so cadence_bar takes one and
#     distinct ids give distinct approaches; (b) across the corpus's resolving finals,
#     the realized final-bar APPROACH SHAPE (the interval into the tonic) is not a single
#     shared cell — at least 3 distinct approach shapes appear.
import entmotif.melody as _mel  # noqa: E402
_capp = set()
for _i in range(8):
    _fig = tuple(_mel.cadence_bar("authentic", 0, "major", 52, 79, 0, 0, 80, approach=_i))
    _capp.add(_fig)
check(len(_capp) >= 4, "cadence approach not input-derived: only %d distinct approaches over 8 ids" % len(_capp))
# determinism: same approach id -> identical figure
check(_mel.cadence_bar("authentic", 0, "major", 52, 79, 0, 0, 80, approach=3)
      == _mel.cadence_bar("authentic", 0, "major", 52, 79, 0, 0, 80, approach=3),
      "cadence_bar not deterministic for a fixed approach id")
# every authentic/plagal approach still RESOLVES on the tonic (last note = degree 1)
for _i in range(8):
    for _res in ("authentic", "plagal"):
        _fig = _mel.cadence_bar(_res, 0, "major", 52, 79, 0, 0, 80, approach=_i)
        _tonic = motif.snap((52 + 79) // 2, [0], 52, 79)
        check(_fig[-1].pitch == _tonic,
              "cadence approach %d (%s) does not resolve on tonic: ends %d (tonic %d)"
              % (_i, _res, _fig[-1].pitch, _tonic))
# on the corpus: resolving finals show >=3 distinct approach interval-shapes (not one stamp)
_shapes = set()
for v in CORPUS:
    notes, m = motif.generate(v)
    if m.get("final_cad") not in ("authentic", "plagal"):
        continue
    lead = sorted((n for n in notes if int(n[0]) == 0), key=lambda n: n[3])
    lastbar = (m["bars"] - 1) * 4 * DIV
    cell = [n[1] for n in lead if n[3] >= lastbar]
    if len(cell) >= 2:
        _shapes.add(tuple(b - a for a, b in zip(cell, cell[1:])))   # interval shape into the tonic
check(len(_shapes) >= 3,
      "cadence interchangeable: corpus resolving finals show only %d distinct approach shapes %s"
      % (len(_shapes), _shapes))

# --- v0.9: harmony overhaul invariants on the corpus ---
for v in CORPUS:
    notes, m = motif.generate(v)
    comp = [n for n in notes if int(n[0]) == 1]
    lead_v = [n[2] for n in notes if int(n[0]) == 0]
    # (a) comp velocity sits WITH the melody (not the v0.8 ~30 below): within ~22 of lead avg
    if comp:
        lavg = sum(lead_v) // max(1, len(lead_v))
        cmax = max(n[2] for n in comp)
        check(cmax >= lavg - 22, "comp too quiet vs lead: %s (compMax %d vs leadAvg %d)" % (v, cmax, lavg))
    # (b) cluster-free voicings: simultaneous comp tones never < 3 semitones apart
    from collections import defaultdict as _dd
    byon = _dd(list)
    for n in comp:
        byon[n[3]].append(n[1])
    for st, ps in byon.items():
        ps = sorted(ps)
        check(all(b - a >= 3 for a, b in zip(ps, ps[1:])),
              "clustered comp voicing: %s at %d -> %s" % (v, st, ps))
    # (c) percussion present (chan 9) whenever the style declares a groove
    if m["percussion"] != "none":
        check(any(int(n[0]) == 9 for n in notes), "percussion declared but absent: %s (%s)" % (v, m["percussion"]))

# --- v0.9: register varies across inputs (not all stuck in one ~C4-C6 window) ---
lows = []
for v in CORPUS:
    notes, m = motif.generate(v)
    lows.append(min(n[1] for n in notes if int(n[0]) == 0))
check(max(lows) - min(lows) >= 7, "melodic register barely varies across inputs (range %d)" % (max(lows) - min(lows)))

# --- v0.12 regression (metric conservation, this.i:m9p3k7a2): no PITCHED-voice
#     onset is off the sixteenth grid. The diminution/climax halving 0.75->0.375
#     used to drift every later onset off the beat. Percussion (ch9) may swing. ---
for v in CORPUS:
    notes, m = motif.generate(v)
    for n in notes:
        if int(n[0]) in (0, 1, 2, 3):
            check(n[3] % (DIV // 4) == 0,
                  "off-grid onset: %s chan%d tick %d" % (v, int(n[0]), n[3]))

# --- v0.12 regression: a diminished cell that tiles must be metrically ANCHORED so
#     its repeat starts on the downbeat (else stressed<->unstressed flips each repeat).
#     A germ with a 0.75 note (halves to an off-integer total) is the failing case. ---
_germ = ([1, -1, 1, -1, 1, -1, 1, -1, 1], [0.5, 0.5, 1, 1.5, 0.5, 0.75, 0.25, 1, 1, 1])
_dn = motif.render_transform(_germ, "diminish", "major", 0, 48, 84, 0, ["I", "I"], 0, 80, 64)
_bar = 4 * DIV
_first = sorted(n[3] for n in _dn if n[3] < _bar)
_second = sorted(n[3] - _bar for n in _dn if n[3] >= _bar)
check(len(_first) > 0 and _first == _second,
      "diminished cell not bar-aligned (stress drift): bar0=%s bar1=%s" % (_first, _second))

print("CORPUS=%d   FAILURES=%d" % (len(CORPUS), len(fails)))
for f in fails[:50]:
    print("  -", f)
sys.exit(1 if fails else 0)
