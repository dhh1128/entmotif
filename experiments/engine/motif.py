#!/usr/bin/env python3
"""entmotif motif engine — v0.7 prototype (zero dependencies).

v0.7 fixes teaching round 3 + the canon-calibration priors (docs/canon-calibration.md):
 (1) BASS CHORD-QUALITY [Codex bug] — bass figuration now derives every tone from
     the actual chord pitch-classes (root/third/fifth of `cpcs`), not hardcoded
     +4/+7 intervals; minor/dim/applied chords get a quality-correct bass.
 (2) LEAD NEVER SILENCED — in call_resp the principal voice (V:1) carries the call
     AND resolves every answer (cadence); the antiphonal response moves to V:4, so
     the lead is never tacet for a whole unit (fixes the v0.6 "melody dying" z16).
 (3) V:4 DEVELOPS — the call_resp antiphon is a SEQUENCED FRAGMENT of the hook (up
     a third), not a verbatim echo; lead_counter keeps its contrary-motion counter.
 (4) FINAL CADENCE ALWAYS RESOLVES — the terminal cadence is forced authentic (V-I,
     lands on the tonic); half/abrupt non-resolving finals are gone (canon: "clean
     cadential closure"; resolves the maintainer's "incompleteness" open question).
 (5) PLACED CLIMAX ~2/3 THROUGH (Huron arch) — register arc peaks at the 2/3 unit,
     reached by the signature leap, reserved (earlier units sit lower).
 (6) DYNAMICS ARC — an entropy/arc-driven dynamic (mp..f..mf) is emitted in ABC
     (!mf! !f! marks on the lead) AND drives MIDI velocity: crescendo into the
     climax, settle at the cadence. (Analog layer: casual avalanche + emotion cue.)
 (7) SIGNATURE RHYTHM HOOK — stronger dotted/syncopated idea-bar cells, reused on
     every idea statement, give a clappable recurring identity.

Carries forward from v0.6: key-transposition, tasteful secondary-dominant color,
signature opening leap, motivic transforms, spread voicings, arrangement templates.

Determinism + avalanche preserved (see test_motif.py). Prototype to be HEARD + GRADED.
Run:  python3 motif.py   |   Test:  python3 test_motif.py
"""

import hashlib
import os
import struct
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "src"))
from entmotif.model import (  # noqa: E402
    DIV, BEATS_PER_BAR, WEIGHT_SCALE, NoteEvent, VoiceRole, PitchRange, Development, Phrase)
from entmotif.theory import *  # noqa: E402,F401,F403
from entmotif.melody import *  # noqa: E402,F401,F403
from entmotif.arrangement import *  # noqa: E402,F401,F403

TEMPOS = [60, 72, 84, 96, 108, 120, 138, 160, 184]
TEMPO_W = [1, 2, 3, 4, 4, 3, 2, 2, 1]


class Chooser:
    def __init__(self, fp):
        self.fp = fp

    def v(self, label):
        return int.from_bytes(hashlib.sha512(self.fp + label.encode()).digest(), "big")

    def int(self, label, n):
        return self.v(label) % n

    def choice(self, label, seq):
        return seq[self.v(label) % len(seq)]

    def weighted(self, label, opts, wts):
        total = float(sum(wts))
        r = (self.v(label) % WEIGHT_SCALE) / float(WEIGHT_SCALE) * total
        acc = 0.0
        for o, w in zip(opts, wts):
            acc += w
            if r <= acc:
                return o
        return opts[-1]


def cadc(res):
    return {"authentic": ["V", "I"], "deceptive": ["V", "vi"], "half": ["IV", "V"]}[res]


def build_form(form, res, ch, color):
    P = cadc(res)
    sd = {0: 0, 1: 25, 2: 60}[color]                          # 2(d) secondary-dominant prob %, by color dial
    if P[1] == "V" and ch.int("sd", 100) < sd:
        P = ["VsV", "V"]
    pre = ["VsV", "V"] if ch.int("sd2", 100) < sd else ["IV", "V"]
    if form == "sentence":
        units = [("idea", ["I", "I"], None, 0), ("answer", P, res, 0)]
    elif form == "period":
        units = [("idea", ["I", "vi"], None, 0), ("answer", pre, "half", 0),
                 ("idea", ["I", "vi"], None, 1), ("answer", P, res, 0)]
    elif form == "period_tag":
        units = [("idea", ["I", "vi"], None, 0), ("answer", pre, "half", 0),
                 ("idea", ["I", "vi"], None, 1), ("answer", ["ii", "V"], "half", 0),
                 ("idea", ["I", "vi"], None, 2), ("answer", P, res, 0)]
    else:
        units = [("idea", ["I", "vi"], None, 0), ("answer", pre, "half", 0),
                 ("idea", ["I", "vi"], None, 1), ("answer", ["ii", "V"], "half", 0),
                 ("contrast", ["IV", "I"], None, 0), ("contrast", ["ii", "V"], None, 0),
                 ("idea", ["I", "vi"], None, 2), ("answer", P, res, 0)]
    units = [Phrase(*u) for u in units]
    role, _chs, _cad, dv = units[-1]                           # round 4: terminal cadence ALWAYS resolves
    units[-1] = Phrase(role, ["V", "I"], "authentic", dv)      # (clean closure; no half/abrupt final)
    return units


def transform_for(devslot, ch):
    if devslot == 0:
        return Development(0, False)
    return Development(*ch.weighted("dev%d" % devslot, [(2, False), (-2, False), (0, True), (1, False)],
                                    [3, 2, 2, 1]))


def generate(value):
    # ~4eu7: prototype hashes the RAW input; the real impl must normalize and
    # strip prefix/suffix EXACTLY as entviz before hashing (see this.i:81pz4m0v).
    fp = hashlib.sha512(value.encode("utf-8")).digest()
    ch = Chooser(fp)
    mode = ch.choice("mode", ["major", "minor"])
    key = ch.int("key", 12)
    lead = ch.choice("lead", LEADS)
    ilo, ihi, icen = LEAD_RANGE[lead]
    tonic = snap(icen, [key], ilo, ihi - 12)
    lo, hi = max(ilo, tonic - 3), min(ihi, tonic + 15)
    base = lo + (hi - lo) // 4
    tempo = ch.weighted("tempo", TEMPOS, TEMPO_W)
    leap = ch.weighted("leap", [0, 1, 2], [3, 4, 2])
    tendency = ch.weighted("tend", [-1, 0, 1], [2, 3, 2])
    resolution = ch.weighted("res", ["authentic", "deceptive", "half"], [3, 2, 2])
    form = ch.weighted("form", ["sentence", "period", "period_tag", "aaba"], [2, 4, 2, 2])
    fat = ch.weighted("fat", [0, 1, 2, 3], [2, 3, 2, 1])
    figr = ch.weighted("figr", ["block", "stabs", "arp", "alberti"], [2, 2, 2, 1])
    bassfig = ch.weighted("bass", ["root5", "walking", "pedal"], [3, 2, 1])
    template = ch.weighted("arr", ["solo_bed", "lead_counter", "call_resp", "groove_first"],
                           [3, 2, 2, 1])
    color = ch.weighted("color", [0, 1, 2], [3, 4, 1])        # harmonic adventurousness dial
    sig = ch.choice("sig", SIG_STEPS[leap])                   # signature opening interval

    idea = [ch.choice("hook", HOOKS), ch.choice("im1", FIGURES)]
    other = [ch.choice("om0", FIGURES), ch.choice("om1", FIGURES)]
    ans_fig = ch.choice("ansfig", FIGURES)
    ans_instr = ANSWER_INSTR[lead]

    units = build_form(form, resolution, ch, color)
    nU = len(units)
    peak = max(1, int(round((nU - 1) * 2.0 / 3.0)))           # placed climax ~2/3 through (Huron arch)
    span = float(max(1, max(peak, nU - 1 - peak)))
    dyn_bars = {}
    notes, used_v4 = [], False
    for u, (role, chs, cad, devslot) in enumerate(units):
        chm = [sym(c, mode) for c in chs]
        bar0 = u * 2
        frac = 1 - abs(u - peak) / span                       # register arc, =1 at the climax unit
        center = int(base + (hi - 2 - base) * frac)
        dyn = unit_dyn(u, nU, peak)
        vel = DYN_VEL[dyn]
        dyn_bars[bar0] = dyn
        offset, invert = transform_for(devslot, ch)
        cr_answer = template == "call_resp" and role == "answer"
        if template == "groove_first" and u == 0:
            mel = []
        elif role == "idea":
            mel = line(idea, chm, mode, key, base, lo, hi, bar0, center, tendency, leap, ch,
                       "idea", offset, invert, sig, VoiceRole.LEAD, vel)
        elif role == "answer":
            if cr_answer:                                     # lead RESOLVES the phrase (never tacet);
                mel = cadence_bar(cad, key, mode, lo, hi, bar0 + 1, VoiceRole.LEAD, vel)   # antiphon answers below
            else:
                mel = line([ans_fig], [chm[0]], mode, key, base, lo, hi, bar0, center, tendency,
                           leap, ch, "idea", offset, invert, sig, VoiceRole.LEAD, vel)
                mel += cadence_bar(cad, key, mode, lo, hi, bar0 + 1, VoiceRole.LEAD, vel)
        else:
            mel = line(other, chm, mode, key, base, lo, hi, bar0, center, tendency, leap, ch,
                       "other", 0, False, None, VoiceRole.LEAD, max(40, vel - 6))
        if u != nU - 1 and mel:                               # breath: trim the LAST note (phrase boundary only)
            br = ch.choice("breath%d" % u, BREATHS)
            if br and mel[-1].dur - int(br * DIV) >= int(0.5 * DIV):
                mel[-1] = mel[-1]._replace(dur=mel[-1].dur - int(br * DIV))
        notes += mel

        if cr_answer:                                         # antiphonal DEVELOPED response on V:4:
            frag = idea[0][:3] or idea[0]                     #   a hook fragment SEQUENCED up a third
            ans = line([frag], [chm[0]], mode, key, base, lo, hi, bar0, center, tendency, leap,
                       ch, "ans%d" % u, 2, False, sig, VoiceRole.ANSWER, max(40, vel - 18))
            used_v4 = used_v4 or bool(ans)
            notes += ans

        comp_on = template in ("solo_bed", "lead_counter", "call_resp")
        bass_on = True
        if template == "groove_first":
            comp_on = u >= 1
        if template == "call_resp":
            comp_on = role != "idea"
        notes += arrange_unit(chm, mode, key, lo, bar0, fat, figr, bassfig, comp_on, bass_on)
        if template == "lead_counter" and role == "idea":     # real contrary-motion counter (V:4)
            cm = line([idea[0]], [chm[0]], mode, key, base, lo - 7, hi - 9, bar0,
                      center - 9, -tendency, 0, ch, "ctr", 0, True, None, VoiceRole.ANSWER, 72)
            used_v4 = used_v4 or bool(cm)
            notes += cm

    meta = {"mode": mode, "key": key, "tonic": tonic, "tempo": tempo, "lead": LEAD_NAMES[lead],
            "lead_prog": lead, "ans_prog": ans_instr, "leap": LEAP_NAMES[leap], "res": resolution,
            "form": form, "bars": nU * 2, "fat": fat, "figr": figr, "arr": template,
            "bar_chords": [c for _, chs, _, _ in units for c in (sym(x, mode) for x in chs)],
            "color": color, "v4": used_v4, "dyn_bars": dyn_bars}
    return notes, meta


# --------------------------------------------------------------- ABC ---------
ABC_PC = {0: "=C", 1: "^C", 2: "=D", 3: "^D", 4: "=E", 5: "=F",
          6: "^F", 7: "=G", 8: "^G", 9: "=A", 10: "^A", 11: "=B"}


def abc_pitch(m):
    acc, letter = ABC_PC[m % 12][0], ABC_PC[m % 12][1]
    octv = m // 12 - 1
    if octv >= 5:
        return acc + letter.lower() + "'" * (octv - 5)
    return acc + letter + "," * (4 - octv)


def _dtok(ticks):
    n = int(round(ticks / (DIV // 4)))
    return str(n) if n != 1 else ""


def _rest(ticks):
    n = int(round(ticks / (DIV // 4)))
    return ("z" + (str(n) if n != 1 else "")) if n >= 1 else ""


def _voice(ch_notes, total_bars, chords=None, dyns=None):
    out = []
    for b in range(total_bars):
        lo_t, hi_t = b * BEATS_PER_BAR * DIV, (b + 1) * BEATS_PER_BAR * DIV
        toks = ['"%s"' % chords[b]] if chords else []
        if dyns and b in dyns:
            toks.append("!%s!" % dyns[b])
        evs = sorted([n for n in ch_notes if lo_t <= n[0] < hi_t])
        t, i = lo_t, 0
        while i < len(evs):
            st = evs[i][0]
            r = _rest(st - t) if st > t else ""
            if r:
                toks.append(r)
            grp = [e for e in evs if e[0] == st]
            dur = grp[0][1]
            if len(grp) > 1:
                toks.append("[" + "".join(abc_pitch(g[2]) for g in grp) + "]" + _dtok(dur))
            else:
                toks.append(abc_pitch(grp[0][2]) + _dtok(dur))
            t = st + dur
            i += len(grp)
        r = _rest(hi_t - t) if t < hi_t else ""
        if r:
            toks.append(r)
        out.append(" ".join(toks))
    return " | ".join(out) + " |]"


def abc_export(value, notes, meta):
    nb, key, mode = meta["bars"], meta["key"], meta["mode"]
    chords = [chord_name(s, key, mode) for s in meta["bar_chords"]]

    def pick(chs):
        return [(n[3], n[4], n[1]) for n in notes if n[0] in chs]

    header = ["X:1", "T:%s" % value,
              "C:entmotif %s %s, %dbpm, %s, arr=%s, fat=%d" %
              (KEY_NAMES[key], mode, meta["tempo"], meta["form"], meta["arr"], meta["fat"]),
              "M:4/4", "L:1/16", "Q:1/4=%d" % meta["tempo"]]
    voices = [("1", "lead", pick([0])), ("2", "comp", pick([1])), ("3", "bass", pick([2]))]
    if meta["v4"]:
        voices.append(("4", "answer/counter", pick([3])))
    header += ['V:%s name="%s"' % (n, nm) for n, nm, _ in voices] + ["K:C"]
    dyns = meta.get("dyn_bars")
    body = []
    for n, _nm, data in voices:
        body += ["V:%s" % n, _voice(data, nb, chords if n == "1" else None,
                                    dyns if n == "1" else None)]
    return "\n".join(header) + "\n" + "\n".join(body) + "\n"


# --------------------------------------------------------------- MIDI --------
def encode_midi(notes, tempo, lead_prog, ans_prog):
    """Pure: render notes to the canonical MIDI file bytes (no file I/O)."""
    ev = [(0, 0, b"\xff\x51\x03" + struct.pack(">I", int(60_000_000 / tempo))[1:]),
          (0, 1, bytes([0xC0, lead_prog])), (0, 1, bytes([0xC1, COMP_PROGRAM])),
          (0, 1, bytes([0xC2, BASS_PROGRAM])), (0, 1, bytes([0xC3, ans_prog]))]
    for chn, pitch, vel, start, dur in notes:
        ev.append((start, 2, bytes([0x90 | chn, pitch, vel])))
        ev.append((start + max(1, dur), 0, bytes([0x80 | chn, pitch, 0])))
    track, last = bytearray(), 0
    for tick, _p, data in sorted(ev):
        d = tick - last
        last = tick
        q = bytearray([d & 0x7F])
        d >>= 7
        while d:
            q.append((d & 0x7F) | 0x80)
            d >>= 7
        q.reverse()
        track += bytes(q) + data
    track += b"\x00\xff\x2f\x00"
    return (b"MThd" + struct.pack(">IHHH", 6, 0, 1, DIV) +
            b"MTrk" + struct.pack(">I", len(track)) + bytes(track))


def write_midi(notes, tempo, lead_prog, ans_prog, path):
    with open(path, "wb") as f:
        f.write(encode_midi(notes, tempo, lead_prog, ans_prog))


def slug(s):
    return "".join(c if c.isalnum() else "-" for c in s)[:24].strip("-")


if __name__ == "__main__":
    demo = ["did:example:alice", "did:example:alife",
            "550e8400-e29b-41d4-a716-446655440000",
            "0x89205A3A3b2A69De6Dbf7f01ED13B2108B2c43e7",
            "GhostKey-2026", "did:example:alice"]
    print("entmotif v0.7 — chord-quality bass, lead never tacet, developed antiphony, "
          "resolved finals, 2/3 climax, dynamics:\n")
    print("  # | input              | key/mode | tempo | lead    | form        | bars "
          "| arr          | fat | res")
    print("  --+--------------------+----------+-------+---------+-------------+------+-"
          "-------------+-----+----")
    for i, v in enumerate(demo, 1):
        notes, m = generate(v)
        write_midi(notes, m["tempo"], m["lead_prog"], m["ans_prog"],
                   "motif_%d_%s.mid" % (i, slug(v)))
        print("  %d | %-18s | %-2s %-5s | %5d | %-7s | %-11s | %4d | %-12s | %3d | %s"
              % (i, v[:18], KEY_NAMES[m["key"]], m["mode"], m["tempo"], m["lead"],
                 m["form"], m["bars"], m["arr"], m["fat"], m["res"]))
    print("\n  #1 vs #2: one-char input change.   #1 vs #6: identical input.")
