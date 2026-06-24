"""entmotif music theory — pure, entropy-free pitch/chord operations.

Scales, diatonic + applied chords, register snapping, scale-step motion, scale
degrees, roman-numeral mode spelling, and chord naming. Everything here is a pure
function of its arguments (no Chooser, no fingerprint) and table-driven, so it can
be unit-tested in isolation. Pitch classes are 0..11; MIDI note numbers elsewhere.
"""

MAJOR_SCALE = [0, 2, 4, 5, 7, 9, 11]
MINOR_SCALE = [0, 2, 3, 5, 7, 8, 10]
CHORDS = {
    "major": {"I": [0, 4, 7], "ii": [2, 5, 9], "iii": [4, 7, 11], "IV": [5, 9, 0],
              "V": [7, 11, 2], "vi": [9, 0, 4]},
    "minor": {"i": [0, 3, 7], "iio": [2, 5, 8], "III": [3, 7, 10], "iv": [5, 8, 0],
              "V": [7, 11, 2], "VI": [8, 0, 3]},
}
APPLIED = {"VsV": [2, 6, 9]}                                   # V/V: major triad on degree 2
SEVENTH = 10                                                  # interval added for a dominant 7th color
ROMAN_TO_MINOR = {"I": "i", "ii": "iio", "iii": "III", "IV": "iv", "V": "V", "vi": "VI"}
KEY_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def scale_pcs(mode, key):                                     # KEY-TRANSPOSED scale
    return [(p + key) % 12 for p in (MAJOR_SCALE if mode == "major" else MINOR_SCALE)]


def cpcs(s, mode, key):                                       # KEY-TRANSPOSED chord tones
    base = APPLIED[s] if s in APPLIED else CHORDS[mode][s]
    return [(p + key) % 12 for p in base]


def scale_tones(mode, key, lo, hi):
    sp = scale_pcs(mode, key)
    return [m for m in range(lo, hi + 1) if m % 12 in sp]


def snap(target, pcs, lo, hi):
    c = [m for m in range(lo, hi + 1) if m % 12 in [p % 12 for p in pcs]]
    if not c:
        c = list(range(lo, hi + 1))
    return min(c, key=lambda m: abs(m - target))


def snap_chord_tone(target, cp, scale, snapped, prev_pitch):
    """Land a strong beat on a chord tone, avoiding a dead repeat of the previous
    note. ``snapped`` is the already-snapped candidate (``snap(target, cp, ...)``);
    if it equals ``prev_pitch`` we substitute the nearest OTHER chord tone drawn
    from ``scale``. Pure; shared by the melody line and the transform renderer."""
    if snapped != prev_pitch:
        return snapped
    alt = [m for m in scale if m % 12 in [p % 12 for p in cp] and m != snapped]
    if alt:
        return min(alt, key=lambda m: abs(m - target))
    return snapped


def step(cur, delta, mode, key, lo, hi):
    L = scale_tones(mode, key, lo, hi)
    if not L:
        return cur
    i = min(range(len(L)), key=lambda k: abs(L[k] - cur))
    return L[max(0, min(len(L) - 1, i + delta))]


def degree(n, key, mode, lo, hi):
    base = snap((lo + hi) // 2, [key], lo, hi)                # tonic (degree 1) = key
    return step(base, n - 1, mode, key, lo, hi)


def sym(roman, mode):
    return roman if (mode == "major" or roman in APPLIED) else ROMAN_TO_MINOR[roman]


def chord_name(s, key, mode):
    if s in APPLIED:
        return KEY_NAMES[(key + APPLIED[s][0]) % 12]          # applied dominant = major
    pcs = CHORDS[mode][s]
    third, fifth = (pcs[1] - pcs[0]) % 12, (pcs[2] - pcs[0]) % 12
    q = "" if third == 4 else ("dim" if fifth == 6 else "m")
    return KEY_NAMES[(key + pcs[0]) % 12] + q
