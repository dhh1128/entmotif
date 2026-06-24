"""Feature registry. To ADD A FEATURE: drop a module in this package exposing
``NAME``, ``DESC``, ``REQUIRES`` (tuple of Tune fields it needs) and ``run(tunes) -> dict``,
then add it to ``_MODULES`` below. ``mine.py --feature <NAME>`` picks it up automatically.
"""
from __future__ import annotations

from . import (contour, dynamics, emotion, harmony, interval_ngram, meter,
               mode, register)

_MODULES = [meter, mode, contour, interval_ngram, harmony, emotion, register, dynamics]

FEATURES = {m.NAME: m for m in _MODULES}
