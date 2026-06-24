"""entmotif ABC exporter — multi-voice lead-sheet notation.

Renders the generated notes + meta into ABC: a header (key/mode/tempo/arrangement),
then one ``V:`` body per active voice (lead carries chord symbols + dynamics). This
is the human-readable, diffable grading surface (MIDI is the byte source of truth).

Consumes the ``(value, notes, meta)`` produced by the engine. (Migrating it onto a
Motif aggregate is deferred; meta already carries everything it needs.)
"""
from entmotif.model import DIV, BEATS_PER_BAR
from entmotif.theory import chord_name, KEY_NAMES

ABC_PC = {0: "=C", 1: "^C", 2: "=D", 3: "^D", 4: "=E", 5: "=F",
          6: "^F", 7: "=G", 8: "^G", 9: "=A", 10: "^A", 11: "=B"}


def abc_pitch(m):
    acc, letter = ABC_PC[m % 12][0], ABC_PC[m % 12][1]
    octv = m // 12 - 1
    if octv >= 5:
        return acc + letter.lower() + "'" * (octv - 5)
    return acc + letter + "," * (4 - octv)


def _sixteenths(ticks):
    """Tick duration -> count of sixteenth notes (the ABC unit note length L:1/16)."""
    return int(round(ticks / (DIV // 4)))


def _dtok(ticks):
    n = _sixteenths(ticks)
    return str(n) if n != 1 else ""


def _rest(ticks):
    n = _sixteenths(ticks)
    return ("z" + (str(n) if n != 1 else "")) if n >= 1 else ""


def _split_at_bars(evs):
    """Split any note that crosses a bar line into per-bar segments, marking every
    segment but the last as TIED (rendered with ABC '-'). A long note (e.g. an
    augmented motif) thus notates correctly across the barline. evs: (start, dur,
    pitch) tuples; returns (start, dur, pitch, tied) sorted by start."""
    bar = BEATS_PER_BAR * DIV
    out = []
    for st, dur, pitch in evs:
        while True:
            bar_end = (st // bar + 1) * bar
            if st + dur <= bar_end:
                out.append((st, dur, pitch, False))
                break
            out.append((st, bar_end - st, pitch, True))
            dur -= bar_end - st
            st = bar_end
    return sorted(out)


def _voice(ch_notes, total_bars, chords=None, dyns=None):
    evs_all = _split_at_bars(sorted(ch_notes))
    out = []
    for b in range(total_bars):
        lo_t, hi_t = b * BEATS_PER_BAR * DIV, (b + 1) * BEATS_PER_BAR * DIV
        toks = ['"%s"' % chords[b]] if chords else []
        if dyns and b in dyns:
            toks.append("!%s!" % dyns[b])
        evs = [e for e in evs_all if lo_t <= e[0] < hi_t]
        t, i = lo_t, 0
        while i < len(evs):
            st = evs[i][0]
            r = _rest(st - t) if st > t else ""
            if r:
                toks.append(r)
            grp = [e for e in evs if e[0] == st]
            dur = grp[0][1]
            tie = "-" if any(e[3] for e in grp) else ""       # carry the note across the barline
            if len(grp) > 1:
                toks.append("[" + "".join(abc_pitch(g[2]) for g in grp) + "]" + _dtok(dur) + tie)
            else:
                toks.append(abc_pitch(grp[0][2]) + _dtok(dur) + tie)
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
              "C:entmotif [%s] %s %s, %dbpm, lead=%s, perc=%s, form=%s, arr=%s" %
              (meta.get("style", "?"), KEY_NAMES[key], mode, meta["tempo"], meta.get("lead", "?"),
               meta.get("percussion", "none"), meta["form"], meta["arr"]),
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
