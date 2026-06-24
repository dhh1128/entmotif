"""entmotif MIDI exporter — the canonical, byte-reproducible output.

`encode_midi` is a pure function (notes + meta -> exact file bytes); `write_midi`
just writes those bytes. Program assignment comes from meta (per-style palette):
ch0 lead, ch1 comp, ch2 bass, ch3 answer; ch9 is GM percussion (no program change,
default kit). This is the deterministic source of truth (golden-pinned).
"""
import struct

from entmotif.model import DIV, VoiceRole


def _programs(meta):
    return [(int(VoiceRole.LEAD), meta["lead_prog"]), (int(VoiceRole.COMP), meta["comp_prog"]),
            (int(VoiceRole.BASS), meta["bass_prog"]), (int(VoiceRole.ANSWER), meta["ans_prog"])]


def encode_midi(notes, meta):
    """Pure: render notes to the canonical MIDI file bytes (no file I/O)."""
    tempo = meta["tempo"]
    ev = [(0, 0, b"\xff\x51\x03" + struct.pack(">I", 60_000_000 // tempo)[1:])]
    for ch, prog in _programs(meta):                          # ch9 (drums) gets no program change
        ev.append((0, 1, bytes([0xC0 | ch, prog])))
    for chn, pitch, vel, start, dur in notes:
        c = int(chn)
        ev.append((start, 2, bytes([0x90 | c, pitch, vel])))
        ev.append((start + max(1, dur), 0, bytes([0x80 | c, pitch, 0])))
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


def write_midi(notes, meta, path):
    with open(path, "wb") as f:
        f.write(encode_midi(notes, meta))
