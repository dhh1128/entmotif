"""entmotif arrangement — instrument palette, voicings, and accompaniment.

Owns the timbral palette (which instrument leads, its register, the answering
instrument, the comp/bass GM programs) and renders the non-melodic voices: spread
chord voicings (`voice_chord`) and the per-unit comp + bass figuration
(`arrange_unit`). Channel identity is carried by :class:`VoiceRole`.
"""
from typing import NamedTuple

from entmotif.model import DIV, BEATS_PER_BAR, NoteEvent, VoiceRole, PitchRange
from entmotif.theory import cpcs, SEVENTH

# --- GM programs / figuration dynamics --------------------------------------
COMP_PROGRAM = 48               # GM "String Ensemble" — the comp voice (channel 1)
BASS_PROGRAM = 32               # GM "Acoustic Bass" — the bass voice (channel 2)
SUSTAIN_GAP = 6                 # ticks trimmed off held comp/bass notes (avoid overlap)
ARP_GAP = 4                     # ticks trimmed off arpeggiated/running notes
BLOCK_VEL, STAB_VEL, ARP_VEL, ALBERTI_VEL = 34, 42, 40, 38     # comp figuration velocities
PEDAL_VEL, WALK_VEL, ROOT_VEL, FIFTH_VEL = 56, 56, 60, 50      # bass figuration velocities

# --- lead palette (GM program -> name / register / answering instrument) -----
LEADS = [0, 73, 40, 56, 12]
LEAD_NAMES = {0: "piano", 73: "flute", 40: "violin", 56: "trumpet", 12: "marimba"}
LEAD_RANGE = {0: PitchRange(50, 81, 64), 73: PitchRange(62, 88, 76), 40: PitchRange(55, 86, 69),
              56: PitchRange(54, 80, 67), 12: PitchRange(53, 84, 72)}
ANSWER_INSTR = {0: 40, 73: 56, 40: 73, 56: 73, 12: 56}


class Palette(NamedTuple):
    """The chosen timbral set for a motif: the lead instrument (program, name,
    register) and the instrument that answers it."""
    lead_program: int
    lead_name: str
    range: PitchRange
    answer_program: int


def palette_for(lead):
    return Palette(lead, LEAD_NAMES[lead], LEAD_RANGE[lead], ANSWER_INSTR[lead])


def voice_chord(pcs, fat, top):
    """Spread voicing (no clusters): stack chord tones upward with >=3-semitone gaps."""
    ivs = {0: [pcs[0], pcs[1]], 1: pcs, 2: pcs + [(pcs[0] + SEVENTH) % 12],
           3: pcs + [(pcs[0] + SEVENTH) % 12, (pcs[0] + 2) % 12]}[fat]
    pcset = list(dict.fromkeys(p % 12 for p in ivs))
    out, m = [], top - 13
    for pc in pcset:
        cand = m - ((m - pc) % 12) + 12                       # lowest >= m with this pc
        while cand < m + 3:
            cand += 12
        if cand > top:
            cand -= 12
        out.append(cand)
        m = cand
    return sorted(out)


def arrange_unit(chords2, mode, key, melody_lo, bar0, fat, figr, bassfig, comp_on, bass_on):
    out, top = [], melody_lo - 4
    for b, s in enumerate(chords2):
        pcs = cpcs(s, mode, key)
        base = (bar0 + b) * BEATS_PER_BAR * DIV
        if comp_on:
            voic = voice_chord(pcs, fat, top)
            if figr == "block":
                for m in voic:
                    out.append(NoteEvent(VoiceRole.COMP, m, BLOCK_VEL, base, BEATS_PER_BAR * DIV - SUSTAIN_GAP))
            elif figr == "stabs":
                for beat in (0, 2):
                    for m in voic:
                        out.append(NoteEvent(VoiceRole.COMP, m, STAB_VEL, base + beat * DIV, DIV - SUSTAIN_GAP))
            elif figr == "arp":
                seqv = voic + voic[-2::-1]
                for i in range(8):
                    out.append(NoteEvent(VoiceRole.COMP, seqv[i % len(seqv)], ARP_VEL, base + i * (DIV // 2), DIV // 2 - ARP_GAP))
            else:                                             # alberti
                pat = [voic[0], voic[-1], voic[len(voic) // 2], voic[-1]]
                for i in range(8):
                    out.append(NoteEvent(VoiceRole.COMP, pat[i % 4], ALBERTI_VEL, base + i * (DIV // 2), DIV // 2 - ARP_GAP))
        if bass_on:
            bt = lambda pc: 36 + pc                            # bass register (C2..B2); always a chord tone
            root, third, fifth = bt(pcs[0]), bt(pcs[1]), bt(pcs[2])
            if bassfig == "pedal":
                out.append(NoteEvent(VoiceRole.BASS, root, PEDAL_VEL, base, BEATS_PER_BAR * DIV - SUSTAIN_GAP))
            elif bassfig == "walking":
                ws = [root, third, fifth, third]               # walk the actual chord tones (quality-correct)
                for i in range(4):
                    out.append(NoteEvent(VoiceRole.BASS, ws[i], WALK_VEL, base + i * DIV, DIV - SUSTAIN_GAP))
            else:                                              # root + the chord's actual fifth
                out.append(NoteEvent(VoiceRole.BASS, root, ROOT_VEL, base, 2 * DIV))
                out.append(NoteEvent(VoiceRole.BASS, fifth, FIFTH_VEL, base + 2 * DIV, 2 * DIV))
    return out
