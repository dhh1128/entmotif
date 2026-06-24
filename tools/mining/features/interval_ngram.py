"""Feature: melodic interval n-grams — P(next interval | previous interval(s)).

This is the core MOTIF-SHAPE / development distribution: given the last melodic move,
what move comes next? Sampling from it (rather than from independent per-note draws)
is what makes a generated line *go somewhere* instead of orbiting the tonic. Emits a
first-order transition table over signed semitone intervals (clamped to ±12), with the
per-context sample size so thin rows carry a caveat.
"""
from __future__ import annotations

from featlib import conditional, histogram

NAME = "interval_ngram"
DESC = "first-order transition P(interval_n | interval_{n-1}) over melody intervals"
REQUIRES = ("notes",)


def run(tunes):
    unigram = []
    pairs = []
    for t in tunes:
        mel = t.melody()
        if len(mel) < 3:
            continue
        ivs = [max(-12, min(12, b.pitch - a.pitch)) for a, b in zip(mel, mel[1:])]
        unigram.extend(ivs)
        pairs.extend((ivs[i], ivs[i + 1]) for i in range(len(ivs) - 1))
    transition, support = conditional(pairs)
    return {
        "n_intervals": len(unigram),
        "unigram": histogram(unigram),
        "transition": transition,
        "transition_support": support,
    }
