"""Tolerant ABC-notation parser → IR (no third-party deps).

ABC is the native format for the permissive melody corpora we vendor/fetch (TheSession,
Nottingham). This parser is deliberately *tolerant*: real-world ABC is messy, so we
extract what we can (melody pitches + durations, meter, key/mode, inline chord symbols)
and skip what we cannot, rather than failing a whole tune. Features downstream report
how many tunes survived parsing, per the sample-size caveat discipline.

Pitch convention (ABC standard 2.1): capital ``C`` = MIDI 60 (middle C); lowercase
``c`` = 72; each ``,`` drops an octave, each ``'`` raises one. Key signature is applied
so contour/interval features see real sounding pitches.
"""
from __future__ import annotations

import re

from ir import Note, Tune

# ---- key signature: tonic pitch-class + mode → default accidental per letter --------
# Fifths position of each pitch class treated as a MAJOR tonic (+sharps / -flats).
_FIFTHS_MAJOR = {0: 0, 7: 1, 2: 2, 9: 3, 4: 4, 11: 5, 6: 6, 1: 7,
                 8: -4, 3: -3, 10: -2, 5: -1}
# Mode offset along the circle of fifths relative to its parallel major.
_MODE_OFFSET = {"maj": 0, "ion": 0, "dor": -2, "phr": -4, "lyd": 1,
                "mix": -1, "min": -3, "aeo": -3, "loc": -5}
_SHARP_ORDER = [5, 0, 7, 2, 9, 4, 11]   # F C G D A E B (pitch classes)
_FLAT_ORDER = [11, 4, 9, 2, 7, 0, 5]    # B E A D G C F
_LETTER_PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
_TONIC_PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def _key_signature(key_field: str):
    """Parse an ABC ``K:`` value → (tonic_pc, mode_simple, {letter: accidental})."""
    if not key_field:
        return None, None, {}
    m = re.match(r"\s*([A-Ga-g])\s*([#b♯♭]?)\s*([A-Za-z]*)", key_field.strip())
    if not m:
        return None, None, {}
    tonic = _TONIC_PC[m.group(1).upper()]
    if m.group(2) in ("#", "♯"):
        tonic = (tonic + 1) % 12
    elif m.group(2) in ("b", "♭"):
        tonic = (tonic - 1) % 12
    mode_raw = (m.group(3) or "maj").lower()[:3]
    mode = mode_raw if mode_raw in _MODE_OFFSET else "maj"
    fifths = _FIFTHS_MAJOR.get(tonic, 0) + _MODE_OFFSET[mode]
    acc = {}
    if fifths > 0:
        for pc in _SHARP_ORDER[:fifths]:
            acc[_pc_letter(pc)] = 1
    elif fifths < 0:
        for pc in _FLAT_ORDER[:-fifths]:
            acc[_pc_letter(pc)] = -1
    mode_simple = {"maj": "major", "ion": "major", "min": "minor", "aeo": "minor"}.get(
        mode, {"dor": "dorian", "phr": "phrygian", "lyd": "lydian",
               "mix": "mixolydian", "loc": "locrian"}.get(mode))
    return tonic, mode_simple, acc


def _pc_letter(pc):
    for letter, p in _LETTER_PC.items():
        if p == pc:
            return letter
    # F#/C# etc. fall on a letter via the sharp/flat order lists already, so this is safe
    return {1: "C", 3: "D", 6: "F", 8: "G", 10: "A"}[pc]


def _meter(text):
    if not text:
        return None
    text = text.strip()
    if text in ("C", "C|"):
        return (4, 4) if text == "C" else (2, 2)
    m = re.match(r"(\d+)\s*/\s*(\d+)", text)
    return (int(m.group(1)), int(m.group(2))) if m else None


def parse_abc(abc, source="abc", ident=""):
    """Parse one ABC tune (header + body string) into a :class:`Tune`, or None."""
    meter = mode = None
    tonic = None
    unit = None                       # L: default note length in quarter-beats
    body_lines = []
    key_field = ""
    for line in abc.splitlines():
        s = line.strip()
        if len(s) > 1 and s[1] == ":" and s[0].isalpha():
            field, val = s[0], s[2:].strip()
            if field == "M":
                meter = _meter(val)
            elif field == "L":
                mm = re.match(r"(\d+)\s*/\s*(\d+)", val)
                if mm:
                    unit = 4.0 * int(mm.group(1)) / int(mm.group(2))
            elif field == "K":
                key_field = val
                tonic, mode, _acc = _key_signature(val)
            elif field in ("Q",):
                pass
            # other header lines (T,R,X,...) ignored
        elif s and not s.startswith("%"):
            body_lines.append(s)
    _, _, acc = _key_signature(key_field)
    if unit is None:
        # ABC default: 1/8 if meter < 0.75, else 1/4 (standard rule)
        unit = 2.0 if (meter and meter[0] / meter[1] < 0.75) else 1.0
    notes, chords = _parse_body(" ".join(body_lines), acc, unit)
    if not notes:
        return None
    return Tune(source=source, ident=ident, notes=notes, meter=meter, mode=mode,
                key_tonic=tonic, chords=chords)


_TOKEN = re.compile(
    r'"(?P<chord>[^"]*)"'                       # "Am" inline chord/annotation
    r'|(?P<grace>\{[^}]*\})'                     # {grace notes} — skipped
    r'|(?P<deco>![^!]*!|\+[^+]*\+)'              # !decorations!
    r'|(?P<acc>\^{1,2}|_{1,2}|=)?(?P<note>[A-Ga-g])(?P<oct>[,\']*)(?P<num>\d*)(?P<slash>/+)?(?P<den>\d*)'
    r'|(?P<rest>[zxZX])(?P<rnum>\d*)(?P<rslash>/*)(?P<rden>\d*)'
    r'|(?P<broken>[<>]+)'
)


def _parse_body(body, acc, unit):
    notes, chords = [], []
    onset = 0.0
    cur_acc = {}                                  # accidentals active to end of bar
    pending_broken = None
    for m in _TOKEN.finditer(body):
        kind = m.lastgroup
        if m.group("chord") is not None:
            c = m.group("chord")
            if c and c[0] in "ABCDEFG" and not c[0].islower():
                chords.append(c)
            continue
        if m.group("note"):
            letter = m.group("note")
            base = _LETTER_PC[letter.upper()]
            octave = 60 if letter.isupper() else 72
            octave += 12 * (m.group("oct").count("'") - m.group("oct").count(","))
            if m.group("acc"):
                a = m.group("acc")
                semi = {"^": 1, "^^": 2, "_": -1, "__": -2, "=": 0}[a]
                cur_acc[letter] = semi
                pitch = octave + base + semi
            elif letter in cur_acc:
                pitch = octave + base + cur_acc[letter]
            else:
                pitch = octave + base + acc.get(letter.upper(), 0)
            dur = _duration(m.group("num"), m.group("slash"), m.group("den"), unit)
            if pending_broken:
                dur, onset = _apply_broken(pending_broken, dur, notes, onset)
                pending_broken = None
            notes.append(Note(pitch=pitch, onset=onset, dur=dur, voice=0))
            onset += dur
        elif m.group("rest"):
            dur = _duration(m.group("rnum"), m.group("rslash"), m.group("rden"), unit)
            onset += dur
        elif m.group("broken"):
            pending_broken = m.group("broken")
    return notes, chords


def _duration(num, slash, den, unit):
    mult = int(num) if num else 1
    if slash:
        mult = mult / (int(den) if den else (2 ** len(slash)))
    return unit * mult


def _apply_broken(broken, dur, notes, onset):
    """ABC broken rhythm a>b: lengthen previous note, shorten this one (and vice versa)."""
    n = len(broken)
    factor = 1.5 if ">" in broken else 0.5
    for _ in range(n - 1):
        factor = factor * 1.5 if ">" in broken else factor * 0.5
    if notes:
        prev = notes[-1]
        delta = prev.dur * (factor - 1)
        prev.dur *= factor
        onset += delta
        dur *= (2 - factor)
    return dur, onset
