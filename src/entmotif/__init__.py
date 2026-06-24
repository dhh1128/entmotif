"""entmotif — turn a high-entropy value into a short, recognizable musical motif.

Deterministic, zero-dependency engine. The canonical entry points:
  - :func:`entmotif.engine.generate` / :func:`entmotif.engine.compose`
  - :func:`entmotif.exporters.abc.abc_export`
  - :func:`entmotif.exporters.midi.write_midi` / ``encode_midi``

Determinism (same input -> byte-identical MIDI) and avalanche (one-char change ->
different motif) are sacred invariants — see experiments/engine/test_motif.py and
test_golden.py.
"""
from entmotif.engine import generate, compose
from entmotif.exporters.abc import abc_export
from entmotif.exporters.midi import encode_midi, write_midi
from entmotif.theory import KEY_NAMES, cpcs
from entmotif.model import DIV, Motif

__all__ = ["generate", "compose", "abc_export", "encode_midi", "write_midi",
           "KEY_NAMES", "cpcs", "DIV", "Motif"]
