"""Normalized intermediate representation for mined corpora.

Every dataset parser (ABC, **kern, MIDI) yields a stream of :class:`Tune` records in
this single vocabulary, so the feature extractors in ``tools/mining/features/`` are
dataset-agnostic: a feature asks for ``tune.notes`` / ``tune.meter`` / ``tune.emotion``
and does not care whether the source was a Session ABC string or an EMOPIA MIDI file.

Design notes
------------
* All fields are optional except ``source`` and ``notes`` — a corpus that lacks a
  dimension simply leaves it ``None``, and feature extractors skip tunes missing the
  inputs they need (and report the surviving sample size, per the [verify] discipline).
* Time is measured in **quarter-note beats** (a float), NOT MIDI ticks or ABC units,
  so rhythm/onset features compose across formats. Pitch is **MIDI note number**.
* Nothing here imports the entmotif engine — mining is upstream of and independent
  from ``src/entmotif/`` (touch-nothing rule). The features it emits are later mapped
  onto the engine's vocabulary by hand in the findings doc, not by code.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Note:
    """One sounded note, normalized to MIDI pitch + quarter-note beat time."""
    pitch: int                       # MIDI note number (60 = middle C)
    onset: float                     # onset in quarter-note beats from tune start
    dur: float                       # duration in quarter-note beats
    velocity: Optional[int] = None   # MIDI velocity 1..127 (None if format carries no dynamics)
    voice: int = 0                   # voice/track index (0 = first / melody by convention)
    program: Optional[int] = None    # General MIDI program 0..127 (None if not specified)


@dataclass
class Tune:
    """One piece/excerpt in the normalized vocabulary."""
    source: str                                  # dataset name, e.g. "thesession"
    ident: str = ""                              # stable id within the dataset
    notes: list[Note] = field(default_factory=list)
    meter: Optional[tuple[int, int]] = None      # (numerator, denominator), e.g. (3, 4)
    mode: Optional[str] = None                   # "major" | "minor" | modal name (e.g. "dorian")
    key_tonic: Optional[int] = None              # tonic pitch class 0..11 (C=0), if known
    tempo_bpm: Optional[float] = None            # quarter-notes per minute
    genre: Optional[str] = None                  # style/genre label (e.g. "reel", "jig", "pop")
    emotion: Optional[str] = None                # affect label (e.g. "Q1".."Q4" for Russell 4-quadrant)
    chords: list[str] = field(default_factory=list)  # chord symbols in order (e.g. "Am", "E7")
    meta: dict = field(default_factory=dict)     # any extra source-specific fields

    def melody(self) -> list[Note]:
        """Notes of the lowest-index voice, sorted by onset — the singable line."""
        if not self.notes:
            return []
        lead = min(n.voice for n in self.notes)
        return sorted((n for n in self.notes if n.voice == lead), key=lambda n: (n.onset, n.pitch))
