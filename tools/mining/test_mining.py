#!/usr/bin/env python3
"""Self-test for the mining pipeline — runs offline on tiny inline fixtures (no corpus,
no network). Guards the parsers + feature contracts so a future change can't silently
break extraction. Run: ``python3 tools/mining/test_mining.py`` (exit 0 = pass).
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from features import FEATURES
from parsers.abc import parse_abc
from parsers.midi import parse_midi

ABC = """X:1
M:6/8
L:1/8
K:D
A|"D"d2 A F2 A|"A"c2 d e3|
"""


def test_abc_pitches_and_key():
    t = parse_abc(ABC, source="t", ident="1")
    assert t.meter == (6, 8), t.meter
    assert t.mode == "major", t.mode
    p = [n.pitch for n in t.notes]
    # A=69, d=74, A=69, F#=66 (D-major signature applied), A=69 ...
    assert p[:4] == [69, 74, 69, 66], p[:4]
    assert "D" in t.chords and "A" in t.chords


def test_abc_modal_keysig():
    t = parse_abc("M:4/4\nL:1/8\nK:Edor\nE F G A|", source="t")
    assert t.mode == "dorian", t.mode
    # E dorian = D-major key sig: F and C are sharp; G natural
    pitches = {n.pitch for n in t.notes}
    assert 66 in pitches  # F#


def _tiny_midi():
    """Build a 2-note format-0 SMF in memory: program 40 (violin), tempo 120, 4/4."""
    def vlq(n):
        return bytes([n]) if n < 128 else bytes([0x81, n - 128])
    track = bytearray()
    track += b"\x00\xff\x58\x04\x04\x02\x18\x08"            # time sig 4/4
    track += b"\x00\xff\x51\x03\x07\xa1\x20"                # tempo 500000us = 120 bpm
    track += b"\x00\xc0\x28"                                # program change ch0 -> 40
    track += b"\x00\x90\x48\x64"                            # note on  C5(72) vel100
    track += vlq(96) + b"\x80\x48\x40"                      # note off after 96 ticks
    track += b"\x00\x90\x4c\x50"                            # note on  E5(76)
    track += vlq(96) + b"\x80\x4c\x40"                      # note off
    track += b"\x00\xff\x2f\x00"                            # end of track
    head = b"MThd" + (6).to_bytes(4, "big") + (0).to_bytes(2, "big") + \
        (1).to_bytes(2, "big") + (96).to_bytes(2, "big")
    trk = b"MTrk" + len(track).to_bytes(4, "big") + bytes(track)
    return head + trk


def test_midi_notes_program_tempo():
    t = parse_midi(_tiny_midi(), source="m", ident="x", emotion="Q1")
    assert t.tempo_bpm == 120.0, t.tempo_bpm
    assert t.meter == (4, 4), t.meter
    assert t.emotion == "Q1"
    assert [n.pitch for n in t.notes] == [72, 76], [n.pitch for n in t.notes]
    assert all(n.program == 40 for n in t.notes)
    assert t.notes[0].dur == 1.0  # 96 ticks / 96 tpq = 1 quarter beat


def test_features_run_on_fixtures():
    abc = parse_abc(ABC, source="t")
    midi = parse_midi(_tiny_midi(), source="m", emotion="Q2")
    tunes = [abc, midi]
    for name, mod in FEATURES.items():
        out = mod.run(tunes)
        assert isinstance(out, dict), name
    # meter sees both; emotion sees only the labelled MIDI fixture (Q2)
    assert FEATURES["meter"].run(tunes)["overall"]
    assert "Q2" in FEATURES["emotion"].run(tunes)["by_emotion"]


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print("ok", fn.__name__)
    print("PASS (%d tests)" % len(fns))
