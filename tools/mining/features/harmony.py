"""Feature: chord-progression harmony — root-motion and quality bigrams.

Built from inline chord symbols (ABC ``"Am"`` tokens). Two distributions:
* root-motion bigram: P(next root interval | current), in semitones up the scale —
  captures "down a fifth / up a second" functional motion without needing a key;
* quality bigram: P(next quality | current quality) over {maj, min, dom7, dim, ...}.
Feeds the engine's HARMONY node (progression-family choice).
"""
from __future__ import annotations

import re

from featlib import conditional, histogram

NAME = "harmony"
DESC = "chord root-motion and quality transition distributions from inline chord symbols"
REQUIRES = ("chords",)

_ROOT = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
_CHORD = re.compile(r"^([A-G])([#b]?)(.*)$")


def _parse_chord(sym):
    m = _CHORD.match(sym.strip())
    if not m:
        return None
    root = _ROOT[m.group(1)]
    if m.group(2) == "#":
        root = (root + 1) % 12
    elif m.group(2) == "b":
        root = (root - 1) % 12
    tail = m.group(3).lower()
    if "dim" in tail or "°" in tail:
        qual = "dim"
    elif "aug" in tail or "+" in tail:
        qual = "aug"
    elif "maj7" in tail:
        qual = "maj7"
    elif tail.startswith("m") and not tail.startswith("maj"):
        qual = "min7" if "7" in tail else "min"
    elif "7" in tail:
        qual = "dom7"
    else:
        qual = "maj"
    return root, qual


def run(tunes):
    root_pairs = []
    qual_pairs = []
    qualities = []
    n = 0
    for t in tunes:
        parsed = [p for p in (_parse_chord(c) for c in t.chords) if p]
        if len(parsed) < 2:
            continue
        n += 1
        qualities.extend(q for _, q in parsed)
        for (r1, q1), (r2, q2) in zip(parsed, parsed[1:]):
            root_pairs.append(((r2 - r1) % 12, None))  # outcome carried in context below
            qual_pairs.append((q1, q2))
    # root motion as a flat histogram of semitone steps (mod 12)
    root_motion = histogram([ctx for ctx, _ in root_pairs])
    qual_trans, qual_support = conditional(qual_pairs)
    return {
        "n_progressions": n,
        "root_motion_semitones": root_motion,
        "quality_overall": histogram(qualities),
        "quality_transition": qual_trans,
        "quality_transition_support": qual_support,
    }
