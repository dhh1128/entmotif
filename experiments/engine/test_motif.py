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

# --- fw7 (this.i:d2k9m4p1, the conditional-DAG register fix): the lead's register is
#     CONDITIONED ON THE CHOSEN INSTRUMENT. The melodic window is the INTERSECTION of the
#     style register and the instrument's real tessitura, so every note sounded on the
#     lead program — the LEAD voice (chan 0) AND the antiphon/counter ANSWER voice
#     (chan 3), which share the lead's timbre — lies within that instrument's playable
#     range. Named failures: a flute salsa / a piccolo march whose line sat one-to-two
#     octaves BELOW the instrument's range. Probe the corpus + a wide spread of inputs. ---
_LEAD_RANGE_PROBE = CORPUS + ["probe-%d" % i for i in range(0, 4000, 3)]
for v in _LEAD_RANGE_PROBE:
    notes, m = motif.generate(v)
    prog = m["lead_prog"]
    rng = arr.LEAD_RANGE[prog]
    for n in notes:
        if int(n[0]) in (0, 3):                               # LEAD + ANSWER both sound on the lead instrument
            check(rng.lo <= n[1] <= rng.hi,
                  "lead %s note %d outside its tessitura [%d,%d]: %s"
                  % (arr.gm_name(prog), n[1], rng.lo, rng.hi, v))

# --- fw7 (this.i:d2k9m4p1 / z0m4p81q): STRONGER style->instrument CONVERGENCE. The lead
#     distribution was diluted by ~30 'weird-but-valid' capable timbres (each ~1 vs a
#     signature ~16), so per-style P(signature) was only 0.35-0.71 and barely half the
#     corpus leads were style-suited. The signature instruments must DOMINATE (genre-
#     typical common, weird-but-valid rare-but-reachable): per style P(signature) >= 0.75;
#     the per-style affinity (lead_w) biases WITHIN the signature set (the iconic timbre
#     most common); every offered lead stays reachable (weight >= 1); and a weird-but-
#     valid lead remains reachable so the full palette is not collapsed. ---
for st in arr.STYLE_NAMES:
    progs, wts = arr.lead_choices(st)
    sig = set(arr.STYLES[st]["leads"])
    total = sum(wts)
    sigmass = sum(w for p, w in zip(progs, wts) if p in sig)
    check(total > 0 and sigmass / total >= 0.75,
          "weak style->lead convergence: %s P(sig)=%.2f < 0.75" % (st, sigmass / max(1, total)))
    check(all(w >= 1 for w in wts), "a lead weight < 1 (unreachable): %s" % st)
    check(any(p not in sig for p in progs), "no weird-but-valid lead reachable (palette collapsed): %s" % st)
# the per-style affinity actually biases WITHIN the signature (lead_w is USED, not flat):
for st in arr.STYLE_NAMES:
    s = arr.STYLES[st]
    if len(set(s["lead_w"])) > 1:
        wmap = dict(zip(*arr.lead_choices(st)))
        top = s["leads"][s["lead_w"].index(max(s["lead_w"]))]
        bot = s["leads"][s["lead_w"].index(min(s["lead_w"]))]
        check(wmap[top] > wmap[bot], "lead_w affinity ignored within signature: %s" % st)
# corpus: most leads are now style-suited (the "only ~2/12 style-suited" failure) ---
_suited = 0
for v in CORPUS:
    _n, _m = motif.generate(v)
    if _m["lead_prog"] in set(arr.STYLES[_m["style"]]["leads"]):
        _suited += 1
check(_suited >= 9, "too few corpus leads style-suited: %d/12 (want >=9)" % _suited)

# --- fw7 (this.i:a7k0m3p9, EMOTION as the upstream master in the DAG d2k9m4p1): pick an
#     emotion, then COHERENTLY condition the affective cues (Gabrielsson precedence:
#     mode > tempo > register > dynamics > articulation > dissonance) so a motif feels
#     sad/happy/tense instead of emotionally flat. Emotion biases WITHIN-style choices,
#     it does not override the idiom (a sad samba is still a samba). ---
# (a) EMOTION is a reachable master and travels in the meta.
_emos_seen = {motif.generate("emo-probe-%d" % i)[1].get("emotion") for i in range(3000)}
check(len(arr.EMOTION_NAMES) >= 5, "fewer than 5 emotions: %d" % len(arr.EMOTION_NAMES))
check(_emos_seen == set(arr.EMOTION_NAMES),
      "not every emotion reachable: missing %s" % (set(arr.EMOTION_NAMES) - _emos_seen))
# (b) the CONDITIONAL distributions order correctly (pure functions; cue precedence).
def _pminor(st, emo):
    w = arr.mode_weights(st, emo); return w[1] / sum(w)
def _wmean_tempo(st, emo):
    ts, w = arr.STYLES[st]["tempos"], arr.tempo_weights(st, emo)
    return sum(t * x for t, x in zip(ts, w)) / sum(w)
def _pcolor2(st, emo):
    w = arr.color_weights(st, emo); return w[2] / sum(w)
for st in arr.STYLE_NAMES:
    check(_pminor(st, "sad") > _pminor(st, "happy"),
          "mode not conditioned: P(minor|sad) !> P(minor|happy) for %s" % st)
    check(_pcolor2(st, "tense") >= _pcolor2(st, "happy"),
          "dissonance not conditioned: P(color2|tense) < P(color2|happy) for %s" % st)
    if len(arr.STYLES[st]["tempos"]) > 1:
        check(_wmean_tempo(st, "happy") > _wmean_tempo(st, "sad"),
              "tempo not conditioned: mean(happy) !> mean(sad) for %s" % st)
# the emotion table itself ranks energy/register/loudness as the precedence demands
check(arr.EMOTIONS["happy"]["reg"] > arr.EMOTIONS["sad"]["reg"], "happy register !> sad")
check(arr.EMOTIONS["triumphant"]["dyn"] > arr.EMOTIONS["sad"]["dyn"], "triumphant !louder than sad")
# (c) REALIZED coherence: bucket a wide probe by chosen emotion; the aggregate cues align
#     (style is drawn independently of emotion, so the idiom confound averages out).
from collections import defaultdict as _dde
_etempo, _evel, _epitch = _dde(list), _dde(list), _dde(list)
for i in range(2400):
    n, m = motif.generate("emoreal-%d" % i)
    e = m.get("emotion")
    if e is None:
        continue
    _etempo[e].append(m["tempo"])
    lead = [x for x in n if int(x[0]) == 0]
    if lead:
        _evel[e].append(max(x[2] for x in lead))
        _epitch[e].append(sum(x[1] for x in lead) / len(lead))
def _mean(xs): return sum(xs) / len(xs) if xs else 0
check(_mean(_etempo["happy"]) > _mean(_etempo["sad"]),
      "realized tempo not coherent: happy %.0f !> sad %.0f" % (_mean(_etempo["happy"]), _mean(_etempo["sad"])))
check(_mean(_evel["triumphant"]) > _mean(_evel["sad"]),
      "realized loudness not coherent: triumphant %.0f !> sad %.0f" % (_mean(_evel["triumphant"]), _mean(_evel["sad"])))
check(_mean(_epitch["happy"]) > _mean(_epitch["sad"]),
      "realized register not coherent: happy %.1f !> sad %.1f" % (_mean(_epitch["happy"]), _mean(_epitch["sad"])))

# --- fw8 (this.i:d2k9m4p1, the emotion->STYLE DAG edge): emotion is UPSTREAM of style;
#     the affect tilts WHICH idiom is chosen (a tense tango / triumphant march common, a
#     peaceful funk rare) while every style stays reachable for every emotion. ---
# (a) pure: favoured styles lifted, all stay reachable, ordering holds.
for emo in arr.EMOTION_NAMES:
    sw = arr.style_weights(emo)
    check(len(sw) == len(arr.STYLE_NAMES) and all(w > 0 for w in sw),
          "style_weights malformed/unreachable for %s" % emo)
    for st, w, base in zip(arr.STYLE_NAMES, sw, arr.STYLE_W):
        check(w >= base, "style_weights dropped %s below base for %s" % (st, emo))
def _pstyle(emo, st):
    sw = arr.style_weights(emo); i = arr.STYLE_NAMES.index(st)
    return sw[i] / sum(sw)
check(_pstyle("sad", "tango") > _pstyle("happy", "tango"), "tango not lifted by sad vs happy")
check(_pstyle("happy", "ragtime") > _pstyle("sad", "ragtime"), "ragtime not lifted by happy vs sad")
check(_pstyle("triumphant", "march") > _pstyle("peaceful", "march"), "march not lifted by triumphant")
# (b) realized: bucket a probe by emotion; the affect-matched styles dominate their bucket.
from collections import defaultdict as _dds
_byemo = _dds(lambda: _dds(int))
for i in range(3000):
    _n, _m = motif.generate("estyle-%d" % i)
    _byemo[_m["emotion"]][_m["style"]] += 1
def _share(emo, styles):
    tot = sum(_byemo[emo].values())
    return sum(_byemo[emo][s] for s in styles) / max(1, tot)
for emo in arr.EMOTION_NAMES:                                 # the favoured set is over-represented in its bucket
    fav = arr.STYLE_AFFECT[emo]
    base_share = len(fav) / len(arr.STYLE_NAMES)
    check(_share(emo, fav) > base_share + 0.10,
          "emotion->style weak: %s favoured share %.2f <= base %.2f+0.10" % (emo, _share(emo, fav), base_share))

# --- fw8 (this.i:d2k9m4p1, emotion-conditioned GROOVE + DEVELOPMENT): the affect also
#     shapes HOW the groove syncopates and HOW the germ develops on restatement — a tense
#     affect leans syncopated + angular (invert/fragment), a sad/peaceful one steadier +
#     gentle (sequence/augment). Emotion conditions the variant/transform draws. ---
# (a) pure: groove-variant mass tilts with the emotion's groove energy.
def _var_share(fn, st, emo):
    names, wts = fn(st, emo)
    return None if len(wts) < 2 else sum(wts[1:]) / sum(wts)
for st in arr.STYLE_NAMES:
    ct, cs = _var_share(arr.comp_pat_weights, st, "tense"), _var_share(arr.comp_pat_weights, st, "sad")
    if ct is not None:
        check(ct > cs, "comp groove not conditioned: %s tense %.2f !> sad %.2f" % (st, ct, cs))
    bt, bs = _var_share(arr.bass_pat_weights, st, "tense"), _var_share(arr.bass_pat_weights, st, "sad")
    if bt is not None:
        check(bt > bs, "bass groove not conditioned: %s tense %.2f !> sad %.2f" % (st, bt, bs))
# (b) pure: development character tilts with the emotion's angular cue.
def _grp_mass(w, grp): return sum(x for t, x in zip(_mel.TRANSFORMS, w) if t in grp) / sum(w)
_wa, _wg, _wn = _mel.transform_weights(+1), _mel.transform_weights(-1), _mel.transform_weights(0)
check(_grp_mass(_wa, _mel.TRANSFORM_ANGULAR) > _grp_mass(_wn, _mel.TRANSFORM_ANGULAR),
      "angular development not lifted for a tense affect")
check(_grp_mass(_wg, _mel.TRANSFORM_GENTLE) > _grp_mass(_wn, _mel.TRANSFORM_GENTLE),
      "gentle development not lifted for a sad affect")
check(_mel.transform_weights(0)[0] == _mel.TRANSFORM_W[0], "identity weight changed (must stay rare)")
# (c) realized: a busy-groove affect uses a non-signature groove variant more often.
_busy = {e for e in arr.EMOTION_NAMES if arr.EMOTIONS[e]["groove"] > 0}
_calm = {e for e in arr.EMOTION_NAMES if arr.EMOTIONS[e]["groove"] < 0}
_bv = _bt = _cv = _ct = 0
for i in range(3000):
    _n, _m = motif.generate("groovecond-%d" % i)
    _isvar = _m["comp_pat"] != arr.STYLES[_m["style"]]["comp_pat"]
    if _m["emotion"] in _busy:
        _bt += 1; _bv += _isvar
    elif _m["emotion"] in _calm:
        _ct += 1; _cv += _isvar
check(_bt and _ct and _bv / _bt > _cv / _ct + 0.05,
      "realized comp groove not conditioned: busy %.3f !> calm %.3f +0.05" % (_bv / max(1, _bt), _cv / max(1, _ct)))

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

# --- fw6 (singability: "machine-gun repeated note" / unsingable patter, convergent
#     prior finding): the LEAD must never sound the SAME pitch 3+ times in a row. A run
#     of >=3 identical pitches is a register-stutter no voice would phrase. Cap at 2.
#     Probed across the golden corpus AND a wider spread of short inputs (which hit the
#     jumpy/patter generation paths the long high-entropy IDs happen to dodge). ---
_STUTTER_PROBE = CORPUS + ["hello", "world", "abc123", "test", "foobar", "xyz",
                           "The quick brown fox", "42", "deadbeef", "music",
                           "entmotif", "quux", "a", "ab", "zzz", "motif"]
for v in _STUTTER_PROBE:
    notes, m = motif.generate(v)
    lead = sorted((n for n in notes if int(n[0]) == 0), key=lambda n: n[3])
    run, worst = 1, 1
    for a, b in zip(lead, lead[1:]):
        run = run + 1 if b[1] == a[1] else 1
        worst = max(worst, run)
    check(worst <= 2,
          "lead stutters same pitch %d times in a row (unsingable patter): %s" % (worst, v))

print("CORPUS=%d   FAILURES=%d" % (len(CORPUS), len(fails)))
for f in fails[:50]:
    print("  -", f)
sys.exit(1 if fails else 0)
