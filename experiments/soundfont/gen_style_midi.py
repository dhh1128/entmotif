#!/usr/bin/env python3
"""Generate a STYLE-gestalt test MIDI for entmotif (zero dependencies).

Seven short full-arrangement fragments (bed + lead, per-fragment tempo) so we
can judge whether whole *styles* read as distinct gestalts — the master
dimension. Each fragment is a sketch meant to evoke the style, not a polished
composition.

Run:  python3 gen_style_midi.py        ->  writes test_styles.mid
Then: ./render_test.sh test_styles.mid ->  renders one WAV per soundfont in sf/
"""

import struct

DIV = 480
SIXTEENTH, EIGHTH, QUARTER, HALF, BAR = 120, 240, 480, 960, 1920

events = []
sections = []          # (start_seconds, label)
t = 0                  # current tick
clock = 0.0            # current seconds (accounts for per-fragment tempo)


def add(tick, pri, data):
    events.append((tick, pri, bytes(data)))


def tempo(bpm, tick):
    add(tick, 0, b"\xff\x51\x03" + struct.pack(">I", int(60_000_000 / bpm))[1:])


def program(ch, prog, tick):
    add(tick, 1, [0xC0 | ch, prog])


def note(ch, pitch, vel, start, dur):
    add(start, 2, [0x90 | ch, pitch, vel])
    add(start + max(1, dur), 0, [0x80 | ch, pitch, 0])


def chord(ch, pitches, vel, start, dur):
    for p in pitches:
        note(ch, p, vel, start, dur)


def seq(ch, notes, vel, start, gap=10):
    """notes: list of (pitch_or_None, dur). Plays sequentially."""
    tt = start
    for pit, dur in notes:
        if pit is not None:
            note(ch, pit, vel, tt, dur - gap)
        tt += dur
    return tt


def begin(name, bpm):
    global _bpm, _start
    _bpm = bpm
    _start = t
    tempo(bpm, t)
    sections.append((clock, name))
    return t


def end():
    global t, clock
    used = t - _start + BAR        # trailing one-bar rest
    clock += used * 60.0 / _bpm / DIV
    t = _start + used


# ====================================================================== 1. Ragtime
bt = begin("RAGTIME (stride piano)", 105)
program(0, 0, t)
RAG = [[76, 84, 79, 76, 72, 79], [77, 83, 79, 77, 74, 71],
       [76, 84, 79, 76, 72, 79], [72, 79, 76, 72, 67, 72]]
RAG_DUR = [3, 3, 2, 3, 3, 2]
for b in range(4):
    o = bt + b * BAR
    note(0, 36 if b != 2 else 43, 80, o, EIGHTH)
    chord(0, (48, 52, 55), 66, o + QUARTER, EIGHTH)
    note(0, 43 if b != 2 else 38, 80, o + 2 * QUARTER, EIGHTH)
    chord(0, (48, 52, 55), 66, o + 3 * QUARTER, EIGHTH)
    off = 0
    for pit, d in zip(RAG[b], RAG_DUR):
        note(0, pit, 102, o + off * SIXTEENTH, d * SIXTEENTH)
        off += d
t = bt + 4 * BAR
end()

# ====================================================================== 2. Boogie
bt = begin("BOOGIE-WOOGIE (fast shuffle piano)", 150)
program(0, 0, t)
program(2, 0, t)
BOOG = [0, 4, 7, 9, 10, 9, 7, 4]                 # rolling bass, semitone offsets
roots = [36, 36, 41, 36]                         # C C F C
for b in range(4):
    o = bt + b * BAR
    for beat in range(4):
        on = o + beat * QUARTER
        note(2, roots[b] + BOOG[beat * 2], 96, on, 300)          # swung
        note(2, roots[b] + BOOG[beat * 2 + 1], 96, on + 320, 150)
    for beat in range(4):                          # RH off-beat 7th stabs
        c = [roots[b] + 24 + x for x in (0, 4, 7, 10)]
        chord(0, c, 78, o + beat * QUARTER + 320, 150)
t = bt + 4 * BAR
end()

# ====================================================================== 3. Bossa
bt = begin("BOSSA NOVA (nylon guitar + soft perc)", 124)
program(0, 73, t)                                 # flute lead
program(1, 24, t)                                 # nylon guitar comp
program(2, 32, t)                                 # acoustic bass
DM7 = [62, 65, 69, 72]
G7 = [67, 71, 74, 77]
for b in range(4):
    o = bt + b * BAR
    ch = DM7 if b % 2 == 0 else G7
    root = 38 if b % 2 == 0 else 43
    for idx in (0, 3, 6):                          # bossa guitar stabs
        chord(1, ch, 70, o + idx * EIGHTH, EIGHTH)
    note(2, root - 12, 78, o, QUARTER)             # bass: root / fifth
    note(2, root - 5, 78, o + 2 * QUARTER + EIGHTH, QUARTER)
    for i in range(8):                             # shaker
        note(9, 70, 42, o + i * EIGHTH, SIXTEENTH)
    for idx in (0, 3, 4, 6):                        # side-stick clave-ish
        note(9, 37, 70, o + idx * EIGHTH, SIXTEENTH)
seq(0, [(81, HALF), (79, QUARTER), (77, QUARTER),     # sparse flute melody
        (76, HALF), (74, HALF),
        (None, BAR),
        (74, QUARTER), (77, QUARTER), (79, HALF), (81, BAR)], 84, bt)
t = bt + 4 * BAR
end()

# ====================================================================== 4. Sitar
bt = begin("SITAR RAGA (sitar + drone + tabla)", 92)
program(0, 104, t)                                # sitar lead
program(1, 48, t)                                 # string drone (tambura proxy)
for b in range(4):                                # drone C + G, whole notes
    chord(1, (48, 55), 40, bt + b * BAR, BAR)
SCALE = [60, 61, 64, 65, 67, 68, 71, 72]          # raga-ish (Bhairav-flavored)
# ornamented sitar line with quick grace notes
phrase = [(60, EIGHTH), (61, SIXTEENTH), (64, EIGHTH + SIXTEENTH), (65, QUARTER),
          (67, EIGHTH), (68, EIGHTH), (67, QUARTER), (65, QUARTER),
          (64, EIGHTH), (65, SIXTEENTH), (64, SIXTEENTH), (61, QUARTER), (60, HALF),
          (None, QUARTER),
          (67, QUARTER), (68, EIGHTH), (71, EIGHTH), (72, HALF),
          (71, EIGHTH), (68, EIGHTH), (67, QUARTER), (65, EIGHTH), (64, EIGHTH),
          (61, QUARTER), (60, HALF)]
seq(0, phrase, 96, bt)
for b in range(4):                                # tabla-ish pattern
    o = bt + b * BAR
    for idx, pit in ((0, 64), (2, 47), (4, 64), (5, 63), (6, 47)):
        note(9, pit, 80, o + idx * EIGHTH, SIXTEENTH)
t = bt + 4 * BAR
end()

# ====================================================================== 5. Synthwave
bt = begin("SYNTHWAVE (saw lead + pad + 4-on-floor)", 116)
program(0, 81, t)                                 # saw lead
program(1, 89, t)                                 # warm pad
program(2, 38, t)                                 # synth bass
PROG = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]   # Am F C G
BASSR = [33, 29, 36, 31]
for b in range(4):
    o = bt + b * BAR
    chord(1, [p + 0 for p in PROG[b]], 60, o, BAR)               # pad
    for i in range(8):                                            # pulsing bass
        note(2, BASSR[b], 92, o + i * EIGHTH, EIGHTH - 20)
    for beat in range(4):                                         # 4-on-floor
        note(9, 36, 110, o + beat * QUARTER, EIGHTH)
        note(9, 42, 60, o + beat * QUARTER + EIGHTH, SIXTEENTH)
    note(9, 38, 95, o + QUARTER, EIGHTH)                          # snare 2 & 4
    note(9, 38, 95, o + 3 * QUARTER, EIGHTH)
seq(0, [(69, EIGHTH), (72, EIGHTH), (76, QUARTER), (74, EIGHTH), (72, EIGHTH), (69, QUARTER),
        (65, EIGHTH), (69, EIGHTH), (72, QUARTER), (71, HALF),
        (67, EIGHTH), (71, EIGHTH), (74, QUARTER), (72, EIGHTH), (71, EIGHTH), (67, QUARTER),
        (62, EIGHTH), (67, EIGHTH), (71, QUARTER), (74, HALF)], 100, bt)
t = bt + 4 * BAR
end()

# ====================================================================== 6. Western
bt = begin("SPAGHETTI WESTERN (whistle + twang guitar)", 96)
program(0, 78, t)                                 # whistle lead
program(1, 27, t)                                 # clean electric (twang)
program(2, 33, t)                                 # finger bass
for b in range(4):                                # sparse twang tremolo + bass
    o = bt + b * BAR
    note(2, 45 if b % 2 == 0 else 40, 70, o, HALF)
    for i in range(8):                            # tremolo on a chord tone
        note(1, 64 if b % 2 == 0 else 62, 55, o + i * EIGHTH, SIXTEENTH)
seq(0, [(81, HALF), (None, EIGHTH), (88, EIGHTH), (86, QUARTER),     # lonesome whistle
        (84, HALF), (81, HALF),
        (None, QUARTER), (76, QUARTER), (81, HALF),
        (84, QUARTER), (86, QUARTER), (84, HALF),
        (81, HALF), (None, HALF), (69, HALF), (72, HALF)], 102, bt)
t = bt + 4 * BAR
end()

# ====================================================================== 7. Chant
bt = begin("GREGORIAN CHANT (choir, modal, free)", 72)
program(0, 52, t)                                 # choir aahs (melody)
program(1, 52, t)                                 # choir drone
for b in range(4):                                # bare-fifth drone D + A
    chord(1, (50, 57), 45, bt + b * BAR, BAR)
seq(0, [(62, HALF), (64, QUARTER), (65, QUARTER), (64, HALF), (62, HALF),    # Dorian line
        (65, HALF), (67, HALF), (69, HALF), (67, QUARTER), (65, QUARTER),
        (64, HALF), (62, HALF), (64, QUARTER), (62, QUARTER), (60, HALF),
        (62, HALF + HALF)], 88, bt)
t = bt + 4 * BAR
end()

# ----------------------------------------------------------------- serialize
track = bytearray()
last = 0
for tick, _pri, data in sorted(events):
    delta = tick - last
    last = tick
    vlq = bytearray([delta & 0x7F])
    delta >>= 7
    while delta:
        vlq.append((delta & 0x7F) | 0x80)
        delta >>= 7
    vlq.reverse()
    track += bytes(vlq) + data
track += b"\x00\xff\x2f\x00"

header = b"MThd" + struct.pack(">IHHH", 6, 0, 1, DIV)
chunk = b"MTrk" + struct.pack(">I", len(track)) + bytes(track)
with open("test_styles.mid", "wb") as f:
    f.write(header + chunk)

print("Wrote test_styles.mid\n\nListening map:")
for secs, label in sections:
    print("  %5.1fs   %s" % (secs, label))
