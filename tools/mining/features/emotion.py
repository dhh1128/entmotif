"""Feature: emotion → musical cues (the priority dimension, this.i:a7k0m3p9).

For emotion-labelled corpora (EMOPIA's Russell 4-quadrant Q1..Q4), this mines the
conditional distributions that let an entropy-chosen EMOTION node coherently align the
affective cues instead of drawing them independently:
* P(tempo_bpm | emotion)      — arousal axis
* P(mode | emotion)           — valence axis (major/minor via a pitch-class profile match)
* P(velocity | emotion)       — dynamics / loudness
* P(register | emotion)       — mean melody pitch
* P(note_density | emotion)   — notes per quarter-beat (busyness / arousal)

EMOPIA quadrants (Russell): Q1 = high-valence high-arousal (happy/excited),
Q2 = low-valence high-arousal (angry/tense), Q3 = low-valence low-arousal (sad/depressed),
Q4 = high-valence low-arousal (calm/relaxed).
"""
from __future__ import annotations

from collections import defaultdict

from featlib import histogram, percentiles

NAME = "emotion"
DESC = "P(tempo|emotion), P(mode|emotion), P(velocity|emotion), P(register|emotion), P(density|emotion)"
REQUIRES = ("emotion", "notes")

# Krumhansl-Kessler major/minor key profiles (normalized correlation, mode only).
_MAJ = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
_MIN = [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]


def _estimate_mode(pitches):
    """Best major-vs-minor over all 12 rotations via profile correlation."""
    pc = [0] * 12
    for p in pitches:
        pc[p % 12] += 1
    best, best_score = "major", -1e9
    for tonic in range(12):
        for label, prof in (("major", _MAJ), ("minor", _MIN)):
            score = sum(pc[(tonic + i) % 12] * prof[i] for i in range(12))
            if score > best_score:
                best, best_score = label, score
    return best


def run(tunes):
    labelled = [t for t in tunes if t.emotion and t.notes]
    by = defaultdict(lambda: {"tempo": [], "mode": [], "vel": [], "reg": [], "dens": []})
    for t in labelled:
        e = t.emotion
        if t.tempo_bpm:
            by[e]["tempo"].append(t.tempo_bpm)
        by[e]["mode"].append(_estimate_mode([n.pitch for n in t.notes]))
        vels = [n.velocity for n in t.notes if n.velocity is not None]
        if vels:
            by[e]["vel"].append(sum(vels) / len(vels))
        mel = t.melody()
        if mel:
            by[e]["reg"].append(sum(n.pitch for n in mel) / len(mel))
        span = max((n.onset + n.dur) for n in t.notes) or 1
        by[e]["dens"].append(len(t.notes) / span)
    out = {"n": len(labelled), "by_emotion": {}}
    for e, d in sorted(by.items()):
        out["by_emotion"][e] = {
            "support": len(d["mode"]),
            "tempo_bpm": percentiles(d["tempo"]),
            "mode": histogram(d["mode"]),
            "velocity": percentiles(d["vel"]),
            "register_midi": percentiles(d["reg"]),
            "note_density_per_beat": percentiles(d["dens"]),
        }
    return out
