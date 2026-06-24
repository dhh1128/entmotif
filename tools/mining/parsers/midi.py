"""Minimal Standard-MIDI-File reader → IR (pure Python, no deps).

Just enough of SMF format 0/1 to recover what the feature extractors need: note
on/off (with velocity), program changes (→ GM instrument), set-tempo and time-signature
meta events. We do NOT render or round-trip MIDI — this is read-only mining. Timing is
converted from ticks to quarter-note beats using the file's division, so it composes
with the ABC-derived IR.

We deliberately avoid ``mido``/``pretty_midi`` to keep mining low-dep (numpy/scipy only).
"""
from __future__ import annotations

import struct

from ir import Note, Tune


def _vlq(data, i):
    """Read a variable-length quantity; return (value, next_index)."""
    value = 0
    while True:
        b = data[i]
        i += 1
        value = (value << 7) | (b & 0x7F)
        if not (b & 0x80):
            return value, i


def parse_midi(data, source="midi", ident="", emotion=None, genre=None):
    """Parse SMF bytes → a :class:`Tune` (one tune per file), or None on failure."""
    if data[:4] != b"MThd":
        return None
    _, fmt, ntrks, division = struct.unpack(">IHHh", data[4:14])
    if division <= 0:                       # SMPTE timing unsupported — skip
        return None
    tpq = division                          # ticks per quarter note
    pos = 14
    notes = []
    tempo_bpm = None
    meter = None
    track_program = {}                      # channel → current GM program
    for _trk in range(ntrks):
        if data[pos:pos + 4] != b"MTrk":
            break
        length = struct.unpack(">I", data[pos + 4:pos + 8])[0]
        pos += 8
        end = pos + length
        t = 0
        status = 0
        on = {}                             # (channel, pitch) → (onset_ticks, velocity)
        i = pos
        while i < end:
            delta, i = _vlq(data, i)
            t += delta
            b = data[i]
            if b & 0x80:
                status = b
                i += 1
            # else: running status — reuse previous status byte
            ev = status & 0xF0
            chan = status & 0x0F
            if ev == 0x90:                  # note on
                pitch, vel = data[i], data[i + 1]
                i += 2
                if vel > 0:
                    on[(chan, pitch)] = (t, vel)
                else:
                    _close(on, notes, chan, pitch, t, tpq, track_program)
            elif ev == 0x80:                # note off
                pitch = data[i]
                i += 2
                _close(on, notes, chan, pitch, t, tpq, track_program)
            elif ev == 0xC0:                # program change
                track_program[chan] = data[i]
                i += 1
            elif ev in (0xA0, 0xB0, 0xE0):  # polytouch / control / pitchbend: 2 bytes
                i += 2
            elif ev in (0xD0,):             # channel pressure: 1 byte
                i += 1
            elif status == 0xFF:            # meta
                mtype = data[i]
                i += 1
                mlen, i = _vlq(data, i)
                payload = data[i:i + mlen]
                if mtype == 0x51 and mlen == 3 and tempo_bpm is None:
                    us = (payload[0] << 16) | (payload[1] << 8) | payload[2]
                    tempo_bpm = round(60_000_000 / us, 2) if us else None
                elif mtype == 0x58 and mlen >= 2 and meter is None:
                    meter = (payload[0], 2 ** payload[1])
                i += mlen
            elif status in (0xF0, 0xF7):    # sysex
                slen, i = _vlq(data, i)
                i += slen
            else:
                i += 1
        pos = end
    if not notes:
        return None
    notes.sort(key=lambda n: (n.onset, n.pitch))
    return Tune(source=source, ident=ident, notes=notes, meter=meter,
                tempo_bpm=tempo_bpm, emotion=emotion, genre=genre)


def _close(on, notes, chan, pitch, t, tpq, track_program):
    key = (chan, pitch)
    if key in on:
        onset_ticks, vel = on.pop(key)
        notes.append(Note(
            pitch=pitch,
            onset=onset_ticks / tpq,
            dur=max(t - onset_ticks, 0) / tpq,
            velocity=vel,
            voice=chan,
            program=track_program.get(chan, 0) if chan != 9 else None,
        ))
