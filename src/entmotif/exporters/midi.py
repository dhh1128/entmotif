"""entmotif MIDI exporter — the canonical, byte-reproducible output.

`encode_midi` is a pure function (notes -> exact file bytes); `write_midi` just
writes those bytes. Channel -> program assignment: ch0 lead, ch1 comp, ch2 bass,
ch3 answer. This is the deterministic source of truth (golden-pinned); rendered
audio is a non-reproducible convenience layer above it.
"""
import struct

from entmotif.model import DIV
from entmotif.arrangement import COMP_PROGRAM, BASS_PROGRAM


def encode_midi(notes, tempo, lead_prog, ans_prog):
    """Pure: render notes to the canonical MIDI file bytes (no file I/O)."""
    ev = [(0, 0, b"\xff\x51\x03" + struct.pack(">I", 60_000_000 // tempo)[1:]),
          (0, 1, bytes([0xC0, lead_prog])), (0, 1, bytes([0xC1, COMP_PROGRAM])),
          (0, 1, bytes([0xC2, BASS_PROGRAM])), (0, 1, bytes([0xC3, ans_prog]))]
    for chn, pitch, vel, start, dur in notes:
        ev.append((start, 2, bytes([0x90 | chn, pitch, vel])))
        ev.append((start + max(1, dur), 0, bytes([0x80 | chn, pitch, 0])))
    track, last = bytearray(), 0
    for tick, _p, data in sorted(ev):
        d = tick - last
        last = tick
        q = bytearray([d & 0x7F])
        d >>= 7
        while d:
            q.append((d & 0x7F) | 0x80)
            d >>= 7
        q.reverse()
        track += bytes(q) + data
    track += b"\x00\xff\x2f\x00"
    return (b"MThd" + struct.pack(">IHHH", 6, 0, 1, DIV) +
            b"MTrk" + struct.pack(">I", len(track)) + bytes(track))


def write_midi(notes, tempo, lead_prog, ans_prog, path):
    with open(path, "wb") as f:
        f.write(encode_midi(notes, tempo, lead_prog, ans_prog))
