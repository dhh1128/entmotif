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
