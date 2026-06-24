"""Shared helpers for feature extractors: histograms, percentiles, distribution JSON.

A "feature" in this pipeline is a *conditional distribution* we can sample
deterministically later (the entropy fingerprint picks a CDF point). So every extractor
ultimately emits, per conditioning context, a small **normalized histogram** (or a few
percentiles for continuous quantities). Keep outputs small and human-auditable — they
are committed to ``data/features/``.
"""
from __future__ import annotations

from collections import Counter, defaultdict


def normalize(counter, ndigits=4):
    """Counter → {key: probability} sorted by descending probability."""
    total = sum(counter.values())
    if not total:
        return {}
    items = sorted(counter.items(), key=lambda kv: (-kv[1], str(kv[0])))
    return {str(k): round(v / total, ndigits) for k, v in items}


def conditional(pairs, ndigits=4):
    """[(context, outcome), ...] → {context: {outcome: prob}}, with per-context counts.

    Returns (dist, support) where support[context] is the sample size behind that row —
    callers surface it so thin conditioning contexts carry a sample-size caveat.
    """
    buckets = defaultdict(Counter)
    for ctx, outcome in pairs:
        buckets[str(ctx)][outcome] += 1
    dist = {ctx: normalize(c, ndigits) for ctx, c in buckets.items()}
    support = {ctx: sum(c.values()) for ctx, c in buckets.items()}
    return dist, support


def percentiles(values, ps=(5, 25, 50, 75, 95)):
    """Plain-Python percentiles (no numpy dependency in the hot path)."""
    if not values:
        return {}
    s = sorted(values)
    out = {}
    for p in ps:
        k = (len(s) - 1) * p / 100.0
        lo, hi = int(k), min(int(k) + 1, len(s) - 1)
        out["p%d" % p] = round(s[lo] + (s[hi] - s[lo]) * (k - lo), 2)
    return out


def histogram(values, ndigits=4):
    return normalize(Counter(values), ndigits)
