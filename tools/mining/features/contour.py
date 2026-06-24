"""Feature: melodic contour — interval-size histogram, direction, and arch-peak position.

Feeds the engine's melody/contour work (the "familiar ARCH contour, peak ~2/3 through,
mostly small/stepwise intervals with a few pointed leaps" memorability spec). Reports:
* interval-size histogram (signed semitones, clamped to ±12) — how stepwise real melodies are;
* direction split (up / down / repeat);
* arch-peak position — where the highest melody note falls as a fraction of the line
  (validates or refutes the "~2/3 through" claim against real corpora).
"""
from __future__ import annotations

from collections import Counter

from featlib import histogram, normalize, percentiles

NAME = "contour"
DESC = "interval-size histogram, direction split, and arch-peak position of the melody"
REQUIRES = ("notes",)


def run(tunes):
    intervals = []
    directions = Counter()
    peak_positions = []
    ranges = []
    lengths = []
    for t in tunes:
        mel = t.melody()
        if len(mel) < 3:
            continue
        pitches = [n.pitch for n in mel]
        lengths.append(len(pitches))
        ranges.append(max(pitches) - min(pitches))
        peak_idx = pitches.index(max(pitches))
        peak_positions.append(round(peak_idx / (len(pitches) - 1), 2))
        for a, b in zip(pitches, pitches[1:]):
            d = max(-12, min(12, b - a))
            intervals.append(d)
            directions["up" if d > 0 else "down" if d < 0 else "repeat"] += 1
    return {
        "n_melodies": len(lengths),
        "interval_semitones": histogram(intervals),
        "abs_interval": histogram([abs(i) for i in intervals]),
        "direction": normalize(directions),
        "arch_peak_position": percentiles(peak_positions),
        "arch_peak_hist": histogram([round(p, 1) for p in peak_positions]),
        "melody_range_semitones": percentiles(ranges),
        "melody_length_notes": percentiles(lengths),
    }
