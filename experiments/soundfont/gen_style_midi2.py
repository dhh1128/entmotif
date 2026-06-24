#!/usr/bin/env python3
"""Style-gestalt test MIDI, batch 2 (zero dependencies).

Six more full-arrangement sketches to keep stress-testing breadth:
operatic aria (open-vowel solo voice), reggae, rock ballad, Celtic jig (6/8),
polka (2/4), and a novelty/SFX fragment (whistle + pizz + bird-tweet + applause)
to hear how "weird-but-distinct" plays.

Run:  python3 gen_style_midi2.py        ->  writes test_styles2.mid
Then: ./render_test.sh test_styles2.mid ->  renders one WAV per soundfont in sf/
"""

import struct

DIV = 480
SIXTEENTH, EIGHTH, QUARTER, HALF, BAR = 120, 240, 480, 960, 1920
BAR68, BAR24 = 1440, 960            # 6/8 and 2/4 bar lengths

events, sections = [], []
t, clock = 0, 0.0


def add(tick, pri, data): events.append((tick, pri, bytes(data)))
def tempo(bpm, tick): add(tick, 0, b"\xff\x51\x03" + struct.pack(">I", int(60_000_000 / bpm))[1:])
def program(ch, prog, tick): add(tick, 1, [0xC0 | ch, prog])


def note(ch, pitch, vel, start, dur):
    add(start, 2, [0x90 | ch, pitch, vel])
    add(start + max(1, dur), 0, [0x80 | ch, pitch, 0])


def chord(ch, pitches, vel, start, dur):
    for p in pitches:
        note(ch, p, vel, start, dur)


def seq(ch, notes, vel, start, gap=12):
    tt = start
    for pit, dur in notes:
        if pit is not None:
            note(ch, pit, vel, tt, dur - gap)
        tt += dur
    return tt


def begin(name, bpm):
    global _bpm, _start
    _bpm, _start = bpm, t
    tempo(bpm, t)
    sections.append((clock, name))
    return t


def end():
    global t, clock
    used = t - _start + BAR
    clock += used * 60.0 / _bpm / DIV
    t = _start + used


# ====================================================================== 1. Aria
bt = begin("OPERATIC ARIA (solo voice, vowels only)", 74)
program(0, 53, t)                                   # Voice Oohs (solo-ish)
program(1, 48, t)                                   # strings
PROG = [[50, 54, 57], [55, 59, 62], [57, 61, 64], [50, 54, 57]]   # D G A D
for b in range(4):
    chord(1, PROG[b], 48, bt + b * BAR, BAR)
seq(0, [(66, HALF), (69, HALF),                                   # rise...
        (71, QUARTER), (73, QUARTER), (74, HALF),
        (78, HALF + QUARTER), (76, QUARTER),                      # climax, held
        (74, QUARTER), (73, QUARTER), (71, QUARTER), (69, QUARTER),
        (66, BAR)], 100, bt)                                      # resolve
t = bt + 4 * BAR
end()

# ====================================================================== 2. Reggae
bt = begin("REGGAE (one-drop, organ skank)", 76)
program(0, 22, t)                                   # melodica (harmonica)
program(1, 16, t)                                   # drawbar organ skank
program(2, 33, t)                                   # finger bass
CH = [[57, 60, 64], [55, 59, 62], [57, 60, 64], [55, 59, 62]]     # Am G vamp
ROOT = [33, 31, 33, 31]
for b in range(4):
    o = bt + b * BAR
    for beat in range(4):                            # skank on the off-beats
        chord(1, CH[b], 64, o + beat * QUARTER + EIGHTH, SIXTEENTH)
    note(2, ROOT[b], 92, o, EIGHTH)                  # reggae bass
    note(2, ROOT[b] + 7, 92, o + 2 * QUARTER + EIGHTH, EIGHTH)
    note(2, ROOT[b] + 12, 88, o + 3 * QUARTER, EIGHTH)
    note(9, 36, 100, o + 2 * QUARTER, EIGHTH)        # one-drop: kick+snare on 3
    note(9, 38, 100, o + 2 * QUARTER, EIGHTH)
    for i in range(8):                               # hats
        note(9, 42, 45, o + i * EIGHTH, SIXTEENTH)
seq(0, [(None, QUARTER), (69, EIGHTH), (72, EIGHTH), (71, QUARTER), (None, QUARTER),
        (None, QUARTER), (67, EIGHTH), (69, EIGHTH), (71, HALF),
        (None, HALF), (72, QUARTER), (71, QUARTER),
        (69, HALF), (67, HALF)], 88, bt)
t = bt + 4 * BAR
end()

# ====================================================================== 3. Rock ballad
bt = begin("ROCK BALLAD (slow backbeat, overdriven lead)", 72)
program(0, 29, t)                                   # overdriven guitar lead
program(1, 0, t)                                    # piano arpeggio
program(2, 33, t)                                   # bass
program(3, 49, t)                                   # strings pad
PROG = [[48, 52, 55], [43, 47, 50], [45, 48, 52], [41, 45, 48]]   # C G Am F
ROOT = [36, 31, 33, 29]
for b in range(4):
    o = bt + b * BAR
    chord(3, [p + 12 for p in PROG[b]], 46, o, BAR)               # lush pad
    note(2, ROOT[b], 80, o, HALF)
    note(2, ROOT[b], 80, o + HALF, HALF)
    arp = PROG[b] + [PROG[b][1] + 12]
    for i in range(8):                                            # piano arpeggio
        note(1, arp[i % len(arp)], 60, o + i * EIGHTH, EIGHTH)
    note(9, 36, 100, o, EIGHTH)                                   # kick 1 & 3
    note(9, 36, 100, o + 2 * QUARTER, EIGHTH)
    note(9, 38, 95, o + QUARTER, EIGHTH)                          # snare 2 & 4
    note(9, 38, 95, o + 3 * QUARTER, EIGHTH)
    if b == 0:
        note(9, 49, 100, o, QUARTER)                             # crash
seq(0, [(67, HALF), (72, HALF), (74, HALF), (72, HALF),          # soulful lead
        (76, HALF + QUARTER), (74, QUARTER), (72, HALF),
        (69, HALF), (67, BAR)], 104, bt)
t = bt + 4 * BAR
end()

# ====================================================================== 4. Celtic jig (6/8)
bt = begin("CELTIC JIG (6/8, fiddle + drone)", 116)
program(0, 110, t)                                  # fiddle
program(1, 48, t)                                   # drone strings
JIG = [[62, 66, 69, 71, 69, 66], [67, 69, 71, 69, 67, 66],
       [62, 66, 69, 74, 73, 71], [69, 66, 62, 64, 66, 62]]
for b in range(4):
    o = bt + b * BAR68
    chord(1, (50, 57), 42, o, BAR68)                # D + A drone
    for i, p in enumerate(JIG[b]):
        note(0, p, 98, o + i * EIGHTH, EIGHTH - 8)
    note(9, 45, 95, o, EIGHTH)                       # bodhran on the two beats
    note(9, 45, 80, o + 3 * EIGHTH, EIGHTH)
    note(9, 45, 55, o + 2 * EIGHTH, SIXTEENTH)
    note(9, 45, 55, o + 5 * EIGHTH, SIXTEENTH)
t = bt + 4 * BAR68
end()

# ====================================================================== 5. Polka (2/4)
bt = begin("POLKA (2/4 oom-pah, accordion)", 124)
program(0, 21, t)                                   # accordion melody
program(1, 21, t)                                   # accordion chords
program(2, 58, t)                                   # tuba
PCH = [[55, 59, 62], [50, 54, 57], [55, 59, 62], [48, 52, 55], [55, 59, 62], [50, 54, 57]]
PR = [43, 38, 43, 36, 43, 38]                       # G D G C G D
MEL = [[67, 71, 74, 71], [74, 71, 69, 67], [67, 71, 74, 79], [76, 74, 72, 71],
       [67, 71, 74, 71], [74, 71, 67, 67]]
for b in range(6):
    o = bt + b * BAR24
    note(2, PR[b], 95, o, EIGHTH)                    # oom (tuba, beat 1)
    note(9, 36, 95, o, EIGHTH)                       # bass drum 1
    chord(1, PCH[b], 70, o + QUARTER, EIGHTH)        # pah (chord, beat 2)
    note(9, 38, 80, o + QUARTER, EIGHTH)             # snare 2
    for i, p in enumerate(MEL[b]):
        note(0, p, 96, o + i * EIGHTH, EIGHTH - 10)
t = bt + 6 * BAR24
end()

# ====================================================================== 6. Novelty / SFX
bt = begin("NOVELTY / SFX (whistle + pizz + birds + applause)", 132)
program(0, 78, t)                                   # whistle
program(1, 45, t)                                   # pizzicato strings
program(3, 123, t)                                  # bird tweet (SFX)
program(4, 126, t)                                  # applause (SFX)
WH = [[72, 76, 79, 76], [77, 76, 74, 72], [72, 74, 76, 79], [76, 72, 71, 72]]
PZ = [[48, 52, 55], [50, 53, 57], [48, 52, 55], [43, 47, 50]]
for b in range(4):
    o = bt + b * BAR
    for i, p in enumerate(WH[b]):
        note(0, p, 100, o + i * EIGHTH * 2, EIGHTH * 2 - 12)
    for beat in range(4):                            # pizz on off-beats
        chord(1, PZ[b], 70, o + beat * QUARTER + EIGHTH, SIXTEENTH)
    for beat in range(4):                            # comedic woodblock
        note(9, 76 if beat % 2 == 0 else 77, 70, o + beat * QUARTER, SIXTEENTH)
    note(3, 84, 100, o + 3 * QUARTER + EIGHTH, EIGHTH)   # bird tweet punctuation
note(4, 60, 110, bt + 4 * BAR - QUARTER, HALF)          # applause tag
t = bt + 4 * BAR
end()

# ----------------------------------------------------------------- serialize
track, last = bytearray(), 0
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

with open("test_styles2.mid", "wb") as f:
    f.write(b"MThd" + struct.pack(">IHHH", 6, 0, 1, DIV) +
            b"MTrk" + struct.pack(">I", len(track)) + bytes(track))

print("Wrote test_styles2.mid\n\nListening map:")
for secs, label in sections:
    print("  %5.1fs   %s" % (secs, label))
