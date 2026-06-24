#!/usr/bin/env python3
"""Generate a soundfont A/B test MIDI for entmotif.

Zero dependencies (writes a Standard MIDI File by hand). Exercises the
*hard* General-MIDI patches our exotic styles rely on, plus two short style
fragments (ragtime, samba), so we can judge which pinned soundfont renders
them convincingly through FluidSynth.

Run:  python3 gen_test_midi.py   ->  writes test_instruments.mid
Then: ./render_test.sh           ->  renders one WAV per soundfont in sf/
"""

import struct

DIV = 480                # ticks per quarter note
BPM = 100
QUARTER = DIV
EIGHTH = DIV // 2

events = []              # (tick, priority, raw_bytes)


def add(tick, priority, data):
    events.append((tick, priority, bytes(data)))


def tempo(bpm, tick=0):
    mpq = int(60_000_000 / bpm)                       # microseconds per quarter
    add(tick, 0, b"\xff\x51\x03" + struct.pack(">I", mpq)[1:])


def program(ch, prog, tick):
    add(tick, 1, [0xC0 | ch, prog])


def note(ch, pitch, vel, start, dur):
    # priority: note-off (0) < program (1) < note-on (2) at the same tick
    add(start, 2, [0x90 | ch, pitch, vel])
    add(start + dur, 0, [0x80 | ch, pitch, 0])


def vlq(n):
    out = bytearray([n & 0x7F])
    n >>= 7
    while n:
        out.append((n & 0x7F) | 0x80)
        n >>= 7
    out.reverse()
    return bytes(out)


# ---------------------------------------------------------------- content ----
sections = []                         # (start_tick, label) for the listening map
t = 0
tempo(BPM, 0)

# 1) Exotic / hard GM patches, each playing a major-pentatonic arc.
#    (name, GM program 0-indexed, base MIDI note)
INSTRUMENTS = [
    ("Sitar",        104, 60),
    ("Koto",         107, 72),
    ("Shakuhachi",    77, 72),
    ("Steel Drums",  114, 60),
    ("Kalimba",      108, 72),
    ("Harpsichord",    6, 60),
    ("Nylon Guitar",  24, 52),
    ("Violin",        40, 67),
    ("Oboe",          68, 72),
    ("Trumpet",       56, 60),
    ("Choir Aahs",    52, 60),
    # second batch — more distinctive timbres to audition
    ("Banjo",        105, 55),
    ("Bagpipe",      109, 62),
    ("Church Organ",  19, 55),
    ("Drawbar Organ", 16, 55),
    ("Dulcimer/Zither", 15, 67),
    ("Accordion",     21, 60),
    ("Harmonica",     22, 60),
    ("Bandoneon",     23, 55),
    ("Music Box",     10, 72),
    ("Tubular Bells", 14, 72),
    ("Pan Flute",     75, 72),
    ("Ocarina",       79, 72),
]
PENTA = [0, 2, 4, 7, 9, 7, 4, 0]      # major-pentatonic up-and-down

for name, prog, base in INSTRUMENTS:
    sections.append((t, name))
    program(0, prog, t)
    for i, off in enumerate(PENTA):
        note(0, base + off, 95, t + i * EIGHTH, EIGHTH)
    t += len(PENTA) * EIGHTH + QUARTER     # + one beat of rest

# 2) Ragtime fragment: straight stride LH under a syncopated (3+3+2) RH.
sections.append((t, "RAGTIME (piano)"))
program(0, 0, t)
BAR = 4 * QUARTER
SIX = DIV // 4                                                # sixteenth note
RAG_DURS = [3, 3, 2, 3, 3, 2]                                 # secondary-rag lilt
RAG_RH = [[76, 84, 79, 76, 72, 79],                          # bar 1 over C
          [77, 83, 79, 77, 74, 71]]                          # bar 2 over G7
for b in range(2):
    bt = t + b * BAR
    note(0, 36, 80, bt + 0 * QUARTER, EIGHTH)                 # stride bass C2
    for p in (48, 52, 55):                                    # C-E-G chord
        note(0, p, 68, bt + 1 * QUARTER, EIGHTH)
    note(0, 43, 80, bt + 2 * QUARTER, EIGHTH)                 # stride bass G2
    for p in (48, 52, 55):
        note(0, p, 68, bt + 3 * QUARTER, EIGHTH)
    off = 0                                                   # syncopated RH
    for pit, d in zip(RAG_RH[b], RAG_DURS):
        note(0, pit, 100, bt + off * SIX, d * SIX - 10)
        off += d
t += 2 * BAR + QUARTER

# 3) Samba fragment: percussion (ch 9) + nylon-guitar bossa stabs (ch 1).
sections.append((t, "SAMBA (drums + nylon guitar)"))
program(1, 24, t)
for b in range(2):
    bt = t + b * BAR
    for i in range(8):                                        # cabasa, every 8th
        note(9, 69, 55, bt + i * EIGHTH, EIGHTH // 2)
    note(9, 36, 105, bt + 1 * QUARTER, EIGHTH)               # surdo on 2
    note(9, 36, 105, bt + 3 * QUARTER, EIGHTH)               # surdo on 4
    for idx in (0, 3, 4, 6):                                  # side-stick pattern
        note(9, 37, 85, bt + idx * EIGHTH, EIGHTH // 2)
    for idx in (0, 3, 6):                                     # Am7 guitar stabs
        for p in (57, 60, 64, 67):
            note(1, p, 80, bt + idx * EIGHTH, EIGHTH)
t += 2 * BAR + QUARTER

# ----------------------------------------------------------- serialize -------
track = bytearray()
last = 0
for tick, _pri, data in sorted(events):
    track += vlq(tick - last) + data
    last = tick
track += vlq(0) + b"\xff\x2f\x00"                            # end of track

header = b"MThd" + struct.pack(">IHHH", 6, 0, 1, DIV)
chunk = b"MTrk" + struct.pack(">I", len(track)) + bytes(track)

with open("test_instruments.mid", "wb") as f:
    f.write(header + chunk)

print("Wrote test_instruments.mid\n\nListening map (at %d BPM):" % BPM)
for start, label in sections:
    secs = start / DIV * 60.0 / BPM
    print("  %5.1fs   %s" % (secs, label))
