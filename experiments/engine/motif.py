#!/usr/bin/env python3
"""entmotif motif engine — compatibility shim.

The engine has graduated from this single prototype file into the
``src/entmotif/`` package (AGENTS.md §5; docs/refactor-plan.md). This module now
re-exports the package's public API so existing callers — the test suites
(test_motif.py, test_golden.py) and the teaching harness
(experiments/teaching/make_scores.py) — keep working via ``import motif``.

New code should import from ``entmotif`` directly. Behavior is byte-identical to
the v0.7 prototype (golden-pinned).

Run:  python3 motif.py   (or, with src/ on PYTHONPATH, python3 -m entmotif.cli)
Test: python3 test_motif.py  &&  python3 test_golden.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "src"))

# Public API (engine + exporters) -------------------------------------------------
from entmotif.engine import generate, compose, TEMPOS, TEMPO_W  # noqa: E402,F401
from entmotif.exporters.abc import (  # noqa: E402,F401
    abc_export, abc_pitch, chord_name, ABC_PC)
from entmotif.exporters.midi import encode_midi, write_midi  # noqa: E402,F401
from entmotif.cli import slug, main  # noqa: E402,F401

# Re-export the building blocks the prototype exposed at module scope, so any
# `motif.<name>` reference (tests, scripts, ad-hoc use) keeps resolving. -----------
from entmotif.model import (  # noqa: E402,F401
    DIV, BEATS_PER_BAR, WEIGHT_SCALE, NoteEvent, VoiceRole, PitchRange,
    Development, Phrase, Motif)
from entmotif.theory import *  # noqa: E402,F401,F403
from entmotif.melody import *  # noqa: E402,F401,F403
from entmotif.arrangement import *  # noqa: E402,F401,F403
from entmotif.entropy import Chooser, fingerprint_text  # noqa: E402,F401
from entmotif.form import cadc, build_form, transform_for  # noqa: E402,F401


if __name__ == "__main__":
    main()
