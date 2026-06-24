"""entmotif arrangement — STYLE as the master dimension: idiom, groove, palette.

A *style* here is a real musical idiom, not a canon shelf: it is defined by its
**groove** (the characteristic comp + bass + percussion patterns), its instrumentation,
harmonic bias, tempo, register and articulation. ragtime *is* a stride left hand;
boogie-woogie *is* the walking-eighths bass; reggae *is* the offbeat skank; swing
*is* walking bass + ride. The fingerprint picks the style (a big discrete master
decision, AGENTS.md §0), which then conditions everything downstream so each motif
is internally cohesive. (Meter is 4/4-only for now, and harmony is functional —
modal/drone idioms like sitar raga and Gregorian chant are deferred to a future
meter + drone-harmony track.)

Also fixes the v0.8 harmony complaints: open (cluster-free) voicings, comp velocity
that sits WITH the melody, octave voice-leading (minimal motion), and legato.
Channel identity via :class:`VoiceRole` (PERCUSSION = ch 9).
"""
from typing import NamedTuple

from entmotif.model import DIV, BEATS_PER_BAR, NoteEvent, VoiceRole, PitchRange
from entmotif.theory import cpcs, SEVENTH

SUSTAIN_GAP = 6
B = DIV                                                       # one beat in ticks (4/4)

# --- GM percussion (channel 9) — the whole family, not just a kit ------------
KICK, SNARE, SIDE, HHC, HHO, RIDE, CRASH = 36, 38, 37, 42, 46, 51, 49
LTOM, MTOM, HTOM = 45, 47, 50
CONGA_L, CONGA_M, CONGA_H, BONGO_L, BONGO_H = 64, 62, 63, 61, 60
TIMB_L, TIMB_H, AGOGO_L, AGOGO_H, COWBELL = 66, 65, 68, 67, 56
CLAVE, WOOD_H, WOOD_L, GUIRO, CABASA, MARACAS, SHAKER, TAMB, TRIANGLE, CUICA, VIBRASLAP = \
    75, 76, 77, 74, 69, 70, 82, 54, 81, 78, 58

# --- the 14 idioms. comp/bass/drum name a groove (below); leads/comp/bass are GM
# programs; reg is the lead (lo,hi,center); color_w/fat_w bias harmony+voicing;
# mode_w biases major vs minor; legato sustains the comp. -----------------------
STYLES = {
    "classical":     dict(leads=[0, 40, 73, 68], comp=0, bass=42, comp_pat="alberti",
                          bass_pat="root5", perc="none", perc_vel=0, reg=PitchRange(55, 86, 68),
                          tempos=[88, 100, 112, 126], tempo_w=[3, 4, 3, 2],
                          color_w=[3, 4, 1], fat_w=[1, 3, 3, 1], mode_w=[3, 2], legato=True),
    "baroque":       dict(leads=[6, 40, 73, 68], comp=6, bass=42, comp_pat="continuo",
                          bass_pat="continuo", perc="none", perc_vel=0, reg=PitchRange(55, 84, 67),
                          tempos=[72, 84, 96, 108], tempo_w=[2, 4, 3, 2],
                          color_w=[2, 4, 2], fat_w=[1, 3, 3, 1], mode_w=[2, 2], legato=False),
    "ragtime":       dict(leads=[0], comp=0, bass=0, comp_pat="stride", bass_pat="stride",
                          perc="none", perc_vel=0, reg=PitchRange(60, 90, 74),
                          tempos=[88, 96, 104, 112], tempo_w=[2, 3, 3, 2],
                          color_w=[2, 4, 2], fat_w=[2, 3, 2, 1], mode_w=[4, 1], legato=False),
    "boogie_woogie": dict(leads=[0], comp=0, bass=0, comp_pat="none", bass_pat="boogie",
                          perc="shuffle", perc_vel=46, reg=PitchRange(60, 90, 74),
                          tempos=[120, 138, 152, 168], tempo_w=[2, 3, 3, 2],
                          color_w=[1, 2, 4], fat_w=[1, 2, 3, 2], mode_w=[4, 1], legato=False),
    "swing":         dict(leads=[66, 56, 11, 26], comp=26, bass=32, comp_pat="comp4",
                          bass_pat="walking", perc="swing", perc_vel=60, reg=PitchRange(54, 86, 69),
                          tempos=[120, 138, 160, 184], tempo_w=[3, 4, 3, 2],
                          color_w=[0, 2, 4], fat_w=[0, 1, 3, 4], mode_w=[3, 2], legato=False),
    "blues":         dict(leads=[25, 22, 18, 29], comp=18, bass=33, comp_pat="shuffle",
                          bass_pat="shuffle", perc="shuffle", perc_vel=64, reg=PitchRange(52, 82, 64),
                          tempos=[76, 92, 108, 120], tempo_w=[2, 4, 3, 2],
                          color_w=[1, 2, 4], fat_w=[0, 2, 3, 2], mode_w=[3, 3], legato=False),
    "bossa_nova":    dict(leads=[24, 73, 11], comp=24, bass=32, comp_pat="bossa",
                          bass_pat="twofeel", perc="bossa", perc_vel=46, reg=PitchRange(55, 84, 67),
                          tempos=[120, 132, 144], tempo_w=[3, 4, 3],
                          color_w=[0, 2, 4], fat_w=[0, 2, 3, 3], mode_w=[3, 2], legato=False),
    "samba":         dict(leads=[73, 56, 24, 11], comp=24, bass=32, comp_pat="bossa",
                          bass_pat="samba", perc="samba", perc_vel=62, reg=PitchRange(57, 88, 71),
                          tempos=[152, 168, 184, 200], tempo_w=[2, 3, 3, 2],
                          color_w=[1, 3, 3], fat_w=[1, 2, 3, 2], mode_w=[3, 2], legato=False),
    "salsa":         dict(leads=[56, 61, 65, 73], comp=0, bass=32, comp_pat="montuno",
                          bass_pat="tumbao", perc="salsa", perc_vel=62, reg=PitchRange(56, 88, 70),
                          tempos=[150, 168, 184], tempo_w=[2, 3, 2],
                          color_w=[1, 3, 3], fat_w=[0, 2, 3, 2], mode_w=[2, 3], legato=False),
    "tango":         dict(leads=[21, 40, 0], comp=21, bass=43, comp_pat="marcato",
                          bass_pat="habanera", perc="none", perc_vel=0, reg=PitchRange(52, 82, 64),
                          tempos=[100, 116, 132], tempo_w=[3, 4, 2],
                          color_w=[2, 3, 3], fat_w=[1, 3, 3, 1], mode_w=[1, 4], legato=False),
    "reggae":        dict(leads=[18, 27, 0], comp=18, bass=33, comp_pat="skank",
                          bass_pat="reggae", perc="one_drop", perc_vel=58, reg=PitchRange(54, 82, 66),
                          tempos=[72, 80, 92], tempo_w=[3, 4, 2],
                          color_w=[3, 3, 1], fat_w=[2, 3, 2, 1], mode_w=[3, 2], legato=False),
    "funk":          dict(leads=[80, 7, 65, 29], comp=7, bass=36, comp_pat="funk16",
                          bass_pat="funk", perc="funk", perc_vel=72, reg=PitchRange(55, 86, 69),
                          tempos=[96, 108, 116, 124], tempo_w=[2, 3, 3, 2],
                          color_w=[1, 2, 4], fat_w=[0, 2, 3, 3], mode_w=[2, 3], legato=False),
    "gospel":        dict(leads=[0, 19, 53, 56], comp=19, bass=33, comp_pat="comp4",
                          bass_pat="walking", perc="backbeat", perc_vel=66, reg=PitchRange(54, 84, 66),
                          tempos=[76, 88, 100], tempo_w=[3, 4, 3],
                          color_w=[1, 3, 4], fat_w=[0, 1, 3, 4], mode_w=[4, 1], legato=True),
    "march":         dict(leads=[56, 61, 57, 71], comp=61, bass=58, comp_pat="oompah",
                          bass_pat="stride", perc="march", perc_vel=70, reg=PitchRange(56, 86, 69),
                          tempos=[108, 116, 124], tempo_w=[3, 4, 2],
                          color_w=[3, 3, 1], fat_w=[1, 3, 3, 1], mode_w=[4, 1], legato=False),
}
STYLE_NAMES = list(STYLES.keys())
STYLE_W = [3, 2, 3, 3, 3, 3, 3, 2, 2, 2, 3, 3, 2, 2]         # all reachable; classics + grooves common

GM_NAMES = {
    0: "piano", 6: "harpsichord", 7: "clavinet", 11: "vibraphone", 18: "rock-organ",
    19: "church-organ", 21: "accordion", 22: "harmonica", 24: "nylon-guitar",
    25: "steel-guitar", 26: "jazz-guitar", 27: "clean-guitar", 29: "od-guitar",
    32: "acoustic-bass", 33: "fingered-bass", 36: "slap-bass", 40: "violin", 42: "cello",
    43: "contrabass", 53: "voice-oohs", 56: "trumpet", 57: "trombone", 58: "tuba",
    61: "brass", 65: "alto-sax", 66: "tenor-sax", 68: "oboe", 71: "clarinet", 73: "flute",
    80: "square-lead",
}


def gm_name(program):
    return GM_NAMES.get(program, "prog%d" % program)


class Palette(NamedTuple):
    style: str
    lead_program: int
    comp_program: int
    bass_program: int
    answer_program: int
    range: PitchRange
    comp_pat: str
    bass_pat: str
    perc: str
    perc_vel: int
    legato: bool


def palette_for(style, lead):
    s = STYLES[style]
    return Palette(style, lead, s["comp"], s["bass"], lead, s["reg"],
                   s["comp_pat"], s["bass_pat"], s["perc"], s["perc_vel"], s["legato"])


def programs_of(palette):
    return {int(VoiceRole.LEAD): palette.lead_program,
            int(VoiceRole.COMP): palette.comp_program,
            int(VoiceRole.BASS): palette.bass_program,
            int(VoiceRole.ANSWER): palette.answer_program}


# --------------------------------------------------------------- voicing -----
def voice_chord(pcs, fat, top, prev=None):
    """Open, cluster-FREE voicing: stack chord tones (triad/+7th/+9th by fat) each
    >= 3 semitones above the one below, then octave-shift to voice-lead from prev."""
    tones = {0: [pcs[0], pcs[2]], 1: pcs, 2: pcs + [(pcs[0] + SEVENTH) % 12],
             3: pcs + [(pcs[0] + SEVENTH) % 12, (pcs[0] + 2) % 12]}[fat]
    pcset = list(dict.fromkeys(p % 12 for p in tones))[:4]    # <=4 voices: keeps the voicing clear, not 2 octaves wide
    out, m = [], top - 12
    for pc in pcset:
        cand = m + ((pc - m) % 12)
        if cand < m + 3:
            cand += 12
        out.append(cand)
        m = cand
    while out and out[-1] > top:
        out = [x - 12 for x in out]
    if prev:
        tgt = prev[-1]
        while out[-1] - tgt > 6:
            out = [x - 12 for x in out]
        while tgt - out[-1] > 6:
            out = [x + 12 for x in out]
    return sorted(out)


def _bn(pcs, role):
    """A bass MIDI note (C2 register) for a chord role."""
    semis = {"root": pcs[0], "third": pcs[1], "fifth": pcs[2],
             "sixth": (pcs[0] + 9) % 12, "b7": (pcs[0] + 10) % 12}[role]
    return 36 + semis


# --------------------------------------------------------------- comp grooves -
def comp_groove(pat, voic, base, vel, legato):
    """Render one bar of comp (chords) in the style's idiom. base = bar start tick."""
    if pat == "none" or not voic:
        return []
    out = []
    full = BEATS_PER_BAR * B
    gap = 0 if legato else SUSTAIN_GAP
    top, bot, mid = voic[-1], voic[0], voic[len(voic) // 2]

    def chord(beat, dur, v=vel, tones=None):
        for m in (voic if tones is None else tones):
            out.append(NoteEvent(VoiceRole.COMP, m, v, base + int(beat * B), int(dur * B) - gap))

    if pat == "alberti":                                      # classical broken chord
        seq = [bot, top, mid, top]
        for i in range(8):
            out.append(NoteEvent(VoiceRole.COMP, seq[i % 4], vel - 8, base + i * (B // 2), B // 2 - 4))
    elif pat == "continuo":                                   # baroque chord on each beat
        for beat in range(BEATS_PER_BAR):
            chord(beat, 1)
    elif pat == "comp4":                                      # swing/gospel light 4-to-the-bar chunks
        for beat in range(BEATS_PER_BAR):
            chord(beat, 0.5, vel - 6)
    elif pat in ("stride", "oompah", "marcato"):              # chord "pah" on the backbeats (2 & 4)
        chord(1, 0.75, vel - 2)
        chord(3, 0.75, vel - 2)
    elif pat == "bossa":                                      # nylon-guitar syncopation
        for beat, dur in [(0, 0.5), (1.5, 0.5), (2, 0.5), (3, 0.5)]:
            chord(beat, dur, vel - 4)
    elif pat == "montuno":                                    # salsa piano: arpeggiated offbeats
        seq = voic + voic[-2::-1]
        for i, beat in enumerate([0.5, 1, 1.5, 2.5, 3, 3.5]):
            out.append(NoteEvent(VoiceRole.COMP, seq[i % len(seq)], vel - 4,
                                 base + int(beat * B), B // 2 - 4))
    elif pat == "skank":                                      # reggae offbeat stabs
        for beat in [0.5, 1.5, 2.5, 3.5]:
            chord(beat, 0.4, vel - 2)
    elif pat == "funk16":                                     # funk 16th stabs (syncopated)
        for beat in [0, 0.75, 1.5, 2.25, 3, 3.5]:
            chord(beat, 0.25, vel)
    elif pat == "shuffle":                                    # blues shuffle chord jabs
        for beat in [0, 1, 2, 3]:
            chord(beat + 0.66, 0.34, vel - 6)
    return out


# --------------------------------------------------------------- bass grooves -
def bass_groove(pat, pcs, next_root_pc, base, vel):
    """Render one bar of bass in the style's idiom; beat 1 is always the root (so the
    harmony is grounded) — mid-bar notes may be idiomatic 6th/b7/passing tones."""
    out = []

    def note(role_or_pc, beat, dur, v=vel):
        m = _bn(pcs, role_or_pc) if isinstance(role_or_pc, str) else 36 + role_or_pc % 12
        out.append(NoteEvent(VoiceRole.BASS, m, v, base + int(beat * B), int(dur * B) - SUSTAIN_GAP))

    aim = min(("root", "third", "fifth"),
              key=lambda r: min((_bn(pcs, r) - (36 + next_root_pc)) % 12,
                                ((36 + next_root_pc) - _bn(pcs, r)) % 12))
    if pat == "root5":
        note("root", 0, 2); note("fifth", 2, 2)
    elif pat == "continuo":                                   # baroque walking quarters
        for i, r in enumerate(["root", "third", "fifth", "third"]):
            note(r, i, 1)
    elif pat == "stride":                                     # "oom" on 1 & 3 (ragtime/march)
        note("root", 0, 1); note("fifth", 2, 1)
    elif pat == "walking":                                    # jazz walking, last beat aims at next root
        for i, r in enumerate(["root", "third", "fifth", aim]):
            note(r, i, 1)
    elif pat == "boogie":                                     # eighth-note ostinato
        for i, r in enumerate(["root", "third", "fifth", "sixth", "b7", "sixth", "fifth", "third"]):
            note(r, i * 0.5, 0.5)
    elif pat == "shuffle":                                    # blues shuffle bass
        for i, r in enumerate(["root", "fifth", "sixth", "fifth"]):
            note(r, i, 1)
    elif pat == "twofeel":                                    # bossa two-feel
        note("root", 0, 2); note("fifth", 2, 2)
    elif pat == "samba":                                      # surdo emphasis (2& and 4&)
        note("root", 0, 1.5); note("fifth", 1.5, 0.5); note("root", 2, 1.5); note("fifth", 3.5, 0.5)
    elif pat == "tumbao":                                     # salsa anticipated bass
        note("root", 0, 1); note("root", 1.5, 0.5); note("fifth", 2.5, 0.5); note(aim, 3, 1)
    elif pat == "habanera":                                   # tango habanera cell
        note("root", 0, 1.5); note("root", 1.5, 0.5); note("fifth", 2, 1); note("fifth", 3, 1)
    elif pat == "reggae":                                     # spacious, syncopated
        note("root", 0, 1); note("root", 1.5, 0.5); note("fifth", 2.5, 1)
    elif pat == "funk":                                       # syncopated 16ths + octave pop
        note("root", 0, 0.5); note("root", 0.75, 0.25); note(pcs[0] + 12, 1.5, 0.25)
        note("fifth", 2, 0.5); note("root", 2.75, 0.25); note(aim, 3.5, 0.5)
    else:
        note("root", 0, 4)
    return out


# ------------------------------------------------------------- percussion ----
def _hit(note, vel, start, dur=B // 4):
    return NoteEvent(VoiceRole.PERCUSSION, note, vel, start, dur)


def percussion_groove(pattern, bar0, nbars, vel):
    """One percussion groove per style, drawing on the idiomatic instruments — kits
    AND hand/Latin/orchestral percussion (congas, timbales, agogo, claves, cowbell,
    guiro, shaker, tambourine, woodblock, surdo, cuica…), not a generic drum kit."""
    if pattern == "none" or vel <= 0:
        return []
    out, half = [], B // 2
    for b in range(nbars):
        base = (bar0 + b) * BEATS_PER_BAR * B
        first = (bar0 + b) == 0
        if pattern in ("rock", "backbeat"):                   # kit; gospel adds tambourine
            for beat in range(BEATS_PER_BAR):
                out.append(_hit(HHC, vel - 24, base + beat * B))
                out.append(_hit(HHC, vel - 30, base + beat * B + half))
            out += [_hit(KICK, vel, base), _hit(KICK, vel - 8, base + 2 * B),
                    _hit(SNARE, vel - 2, base + B), _hit(SNARE, vel - 2, base + 3 * B)]
            if pattern == "backbeat":
                out += [_hit(TAMB, vel - 18, base + B), _hit(TAMB, vel - 18, base + 3 * B)]
            if first:
                out.append(_hit(CRASH, vel, base))
        elif pattern == "swing":                              # ride + hi-hat foot on 2 & 4
            for beat in range(BEATS_PER_BAR):
                out.append(_hit(RIDE, vel - 16, base + beat * B))
                if beat in (0, 2):
                    out.append(_hit(RIDE, vel - 30, base + beat * B + B * 2 // 3))
            out += [_hit(HHC, vel - 14, base + B), _hit(HHC, vel - 14, base + 3 * B),
                    _hit(KICK, vel - 18, base), _hit(SNARE, vel - 12, base + 2 * B)]
        elif pattern == "shuffle":                            # blues shuffle kit
            for beat in range(BEATS_PER_BAR):
                out.append(_hit(HHC, vel - 20, base + beat * B))
                out.append(_hit(HHC, vel - 30, base + beat * B + B * 2 // 3))
            out += [_hit(KICK, vel - 6, base), _hit(SNARE, vel - 4, base + B),
                    _hit(KICK, vel - 10, base + 2 * B), _hit(SNARE, vel - 4, base + 3 * B)]
        elif pattern == "one_drop":                           # reggae: kick+rim together on beat 3
            for beat in range(BEATS_PER_BAR):
                out.append(_hit(HHC, vel - 24, base + beat * B + half))
            out += [_hit(KICK, vel, base + 2 * B), _hit(SIDE, vel - 4, base + 2 * B)]
        elif pattern == "funk":                               # tight kit + open-hat accents
            for i in range(8):
                out.append(_hit(HHC if i % 2 else HHO, vel - 22 - (i % 2) * 6, base + i * half))
            out += [_hit(KICK, vel, base), _hit(KICK, vel - 6, base + B + half),
                    _hit(SNARE, vel - 2, base + B), _hit(SNARE, vel - 2, base + 3 * B)]
        elif pattern == "four":
            for beat in range(BEATS_PER_BAR):
                out.append(_hit(KICK, vel, base + beat * B))
                out.append(_hit(HHO, vel - 26, base + beat * B + half))
        elif pattern == "bossa":                              # soft: rim cross-stick + shaker/cabasa
            for i in range(8):
                out.append(_hit(CABASA if i % 2 else SHAKER, vel - 24 - (i % 2) * 4, base + i * half))
            out += [_hit(SIDE, vel - 8, base), _hit(SIDE, vel - 8, base + B + half),
                    _hit(SIDE, vel - 8, base + 3 * B)]
        elif pattern == "samba":                              # surdo + tamborim(woodblock) + agogo + ganza
            for i in range(8):
                out.append(_hit(SHAKER, vel - 18 - (i % 2) * 6, base + i * half))
            out += [_hit(LTOM, vel, base + B + half), _hit(LTOM, vel, base + 3 * B + half),
                    _hit(WOOD_H, vel - 12, base), _hit(WOOD_L, vel - 14, base + 2 * B),
                    _hit(AGOGO_H, vel - 12, base + half), _hit(AGOGO_L, vel - 16, base + B + half),
                    _hit(CUICA, vel - 18, base + 3 * B)]
        elif pattern == "salsa":                              # clave + congas + timbale + cowbell + guiro
            for beat in range(BEATS_PER_BAR):
                out.append(_hit(COWBELL, vel - 16, base + beat * B))
            for beat, n in [(0, CONGA_H), (1.5, CONGA_L), (2, CONGA_M), (3.5, CONGA_L)]:
                out.append(_hit(n, vel - 12, base + int(beat * B)))
            out += [_hit(CLAVE, vel - 4, base), _hit(CLAVE, vel - 4, base + B + half),
                    _hit(CLAVE, vel - 4, base + 3 * B), _hit(GUIRO, vel - 18, base + 2 * B),
                    _hit(TIMB_H, vel - 14, base + 2 * B + half)]
        elif pattern == "march":                              # bass drum + snare ruffs + crash
            out += [_hit(KICK, vel, base), _hit(KICK, vel - 6, base + 2 * B),
                    _hit(SNARE, vel - 6, base + B), _hit(SNARE, vel - 6, base + 3 * B)]
            for i in (0, 1, 2, 3):
                out.append(_hit(SNARE, vel - 22, base + 2 * B + i * (B // 4)))
            if first:
                out.append(_hit(CRASH, vel, base))
        elif pattern == "hand":                               # bongos + congas
            for beat in range(BEATS_PER_BAR):
                out.append(_hit(BONGO_H if beat % 2 else CONGA_L, vel - 10, base + beat * B))
                out.append(_hit(BONGO_L, vel - 24, base + beat * B + half))
        elif pattern == "soft":                               # brushy: kick + cross-stick + triangle
            out += [_hit(KICK, vel - 8, base), _hit(SIDE, vel - 6, base + 2 * B),
                    _hit(TRIANGLE, vel - 18, base + B)]
    return out


# --------------------------------------------------------------- arrange unit -
def arrange_unit(chords2, mode, key, melody_lo, bar0, fat, comp_pat, bass_pat,
                 comp_on, bass_on, vel_base, legato, prev_voicing):
    """Render the comp + bass for a 2-bar unit in the style's groove. comp velocity
    tracks vel_base (sits with the melody); voicings voice-lead from prev_voicing.
    Returns (notes, last_voicing)."""
    out, top, voicing = [], melody_lo - 4, prev_voicing
    comp_vel = max(52, vel_base - 12)
    bass_vel = max(54, vel_base - 4)
    roots = [cpcs(s, mode, key)[0] for s in chords2]
    for b, s in enumerate(chords2):
        pcs = cpcs(s, mode, key)
        base = (bar0 + b) * BEATS_PER_BAR * B
        if comp_on:
            voicing = voice_chord(pcs, fat, top, voicing)
            out += comp_groove(comp_pat, voicing, base, comp_vel, legato)
        if bass_on:
            out += bass_groove(bass_pat, pcs, roots[b + 1] if b + 1 < len(roots) else pcs[0],
                               base, bass_vel)
    return out, voicing
