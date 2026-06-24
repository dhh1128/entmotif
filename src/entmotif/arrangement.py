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
BASS_C2 = 36                                                  # MIDI C2 — the bass line's octave floor

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
# reg is the lead's (lo,hi,center) — kept lower/singable (v0.10: melodies were shrill);
# lead_w is the AFFINITY weight per lead (signature instrument common, atypical rare);
# perc_vel is loud enough to sit IN the mix (v0.10: percussion was buried 30-50 below).
STYLES = {
    "classical":     dict(leads=[0, 40, 73, 68], lead_w=[3, 3, 2, 2], comp=48, bass=42,
                          comp_pat="alberti", bass_pat="root5", perc="none", perc_vel=0,
                          reg=PitchRange(52, 79, 62), tempos=[88, 100, 112, 126], tempo_w=[3, 4, 3, 2],
                          color_w=[3, 4, 1], fat_w=[1, 3, 3, 1], mode_w=[3, 2], legato=True),
    "baroque":       dict(leads=[6, 40, 73, 68], lead_w=[3, 3, 2, 2], comp=6, bass=42,
                          comp_pat="continuo", bass_pat="continuo", perc="none", perc_vel=0,
                          reg=PitchRange(52, 79, 62), tempos=[72, 84, 96, 108], tempo_w=[2, 4, 3, 2],
                          color_w=[2, 4, 2], fat_w=[1, 3, 3, 1], mode_w=[2, 2], legato=False),
    "ragtime":       dict(leads=[0], lead_w=[1], comp=0, bass=0, comp_pat="stride", bass_pat="stride",
                          perc="none", perc_vel=0, reg=PitchRange(55, 82, 65),
                          tempos=[128, 144, 160], tempo_w=[2, 3, 2],   # lively (recordings 116-182); ~4at7
                          color_w=[2, 4, 2], fat_w=[2, 3, 2, 1], mode_w=[4, 1], legato=False),
    "boogie_woogie": dict(leads=[0], lead_w=[1], comp=0, bass=0, comp_pat="none", bass_pat="boogie",
                          perc="shuffle", perc_vel=92, reg=PitchRange(55, 82, 65),
                          tempos=[120, 138, 152, 168], tempo_w=[2, 3, 3, 2],
                          color_w=[1, 2, 4], fat_w=[1, 2, 3, 2], mode_w=[4, 1], legato=False),
    "swing":         dict(leads=[66, 56, 11, 26], lead_w=[4, 4, 2, 2], comp=26, bass=32,
                          comp_pat="comp4", bass_pat="walking", perc="swing", perc_vel=92,
                          reg=PitchRange(52, 81, 64), tempos=[120, 138, 160, 184], tempo_w=[3, 4, 3, 2],
                          color_w=[0, 2, 4], fat_w=[0, 1, 3, 4], mode_w=[3, 2], legato=False),
    "blues":         dict(leads=[25, 22, 18, 29], lead_w=[3, 3, 2, 3], comp=18, bass=33,
                          comp_pat="shuffle", bass_pat="shuffle", perc="shuffle", perc_vel=96,
                          reg=PitchRange(48, 76, 60), tempos=[76, 92, 108, 120], tempo_w=[2, 4, 3, 2],
                          color_w=[1, 2, 4], fat_w=[0, 2, 3, 2], mode_w=[3, 3], legato=False),
    "bossa_nova":    dict(leads=[24, 73, 11], lead_w=[4, 3, 2], comp=24, bass=32, comp_pat="bossa",
                          bass_pat="twofeel", perc="bossa", perc_vel=82, reg=PitchRange(53, 80, 63),
                          tempos=[120, 132, 144], tempo_w=[3, 4, 3],
                          color_w=[0, 2, 4], fat_w=[0, 2, 3, 3], mode_w=[3, 2], legato=False),
    "samba":         dict(leads=[73, 56, 24, 11], lead_w=[3, 3, 3, 2], comp=24, bass=32,
                          comp_pat="bossa", bass_pat="samba", perc="samba", perc_vel=100,
                          reg=PitchRange(55, 83, 66), tempos=[132, 150, 168], tempo_w=[2, 3, 2],
                          color_w=[1, 3, 3], fat_w=[1, 2, 3, 2], mode_w=[3, 2], legato=False),
    "salsa":         dict(leads=[56, 61, 65, 73], lead_w=[4, 2, 3, 2], comp=0, bass=32,
                          comp_pat="montuno", bass_pat="tumbao", perc="salsa", perc_vel=98,
                          reg=PitchRange(54, 82, 65), tempos=[150, 168, 184], tempo_w=[2, 3, 2],
                          color_w=[1, 3, 3], fat_w=[0, 2, 3, 2], mode_w=[2, 3], legato=False),
    "tango":         dict(leads=[21, 40, 0], lead_w=[4, 3, 2], comp=21, bass=43, comp_pat="marcato",
                          bass_pat="habanera", perc="none", perc_vel=0, reg=PitchRange(50, 77, 60),
                          tempos=[100, 116, 132], tempo_w=[3, 4, 2],
                          color_w=[2, 3, 3], fat_w=[1, 3, 3, 1], mode_w=[1, 4], legato=False),
    "reggae":        dict(leads=[18, 0, 73], lead_w=[4, 2, 2], comp=27, bass=33, comp_pat="skank",
                          bass_pat="reggae", perc="one_drop", perc_vel=94, reg=PitchRange(50, 78, 61),
                          tempos=[72, 80, 92], tempo_w=[3, 4, 2],
                          color_w=[3, 3, 1], fat_w=[2, 3, 2, 1], mode_w=[3, 2], legato=False),
    "funk":          dict(leads=[80, 7, 65, 29], lead_w=[2, 3, 3, 3], comp=7, bass=36,
                          comp_pat="funk16", bass_pat="funk", perc="funk", perc_vel=104,
                          reg=PitchRange(52, 80, 63), tempos=[96, 108, 116, 124], tempo_w=[2, 3, 3, 2],
                          color_w=[1, 2, 4], fat_w=[0, 2, 3, 3], mode_w=[2, 3], legato=False),
    "gospel":        dict(leads=[0, 19, 53, 56], lead_w=[4, 3, 2, 2], comp=19, bass=33,
                          comp_pat="comp4", bass_pat="walking", perc="backbeat", perc_vel=96,
                          reg=PitchRange(52, 79, 62), tempos=[84, 100, 120, 138], tempo_w=[3, 3, 2, 2],
                          color_w=[1, 3, 4], fat_w=[0, 1, 3, 4], mode_w=[4, 1], legato=True),
    "march":         dict(leads=[56, 61, 57, 72, 71], lead_w=[4, 3, 3, 3, 2], comp=71, bass=58,
                          comp_pat="oompah", bass_pat="stride", perc="march", perc_vel=96,
                          reg=PitchRange(55, 82, 66), tempos=[108, 116, 124], tempo_w=[3, 4, 2],
                          color_w=[3, 3, 1], fat_w=[1, 3, 3, 1], mode_w=[4, 1], legato=False),
}
STYLE_NAMES = list(STYLES.keys())
STYLE_W = [3, 2, 3, 3, 3, 3, 3, 2, 2, 2, 3, 3, 2, 2]         # all reachable; classics + grooves common
KEYBOARD_BED_STYLES = {"ragtime", "boogie_woogie"}           # bed IS the keyboard (stride/ostinato): comp stays
#   piano even when the lead is also piano (solo ragtime) — but the lead may still be a
#   capable non-piano timbre (clarinet/banjo/synth) played OVER that piano bed.

GM_NAMES = {
    0: "piano", 4: "e-piano", 6: "harpsichord", 7: "clavinet", 8: "celesta", 9: "glockenspiel",
    10: "music-box", 11: "vibraphone", 12: "marimba", 13: "xylophone", 16: "drawbar-organ",
    18: "rock-organ", 19: "church-organ", 21: "accordion", 22: "harmonica", 24: "nylon-guitar",
    25: "steel-guitar", 26: "jazz-guitar", 27: "clean-guitar", 29: "od-guitar",
    32: "acoustic-bass", 33: "fingered-bass", 34: "picked-bass", 35: "fretless-bass",
    36: "slap-bass", 40: "violin", 41: "viola",
    42: "cello", 43: "contrabass", 45: "pizz-strings", 46: "harp", 53: "voice-oohs",
    56: "trumpet", 57: "trombone", 58: "tuba", 59: "muted-trumpet", 60: "french-horn",
    61: "brass", 65: "alto-sax", 66: "tenor-sax", 68: "oboe", 69: "english-horn", 70: "bassoon",
    71: "clarinet", 72: "piccolo", 73: "flute", 74: "recorder", 75: "pan-flute",
    48: "string-ensemble", 77: "shakuhachi", 78: "whistle", 79: "ocarina",
    80: "square-lead", 81: "saw-lead",
    105: "banjo", 106: "shamisen", 107: "koto", 108: "kalimba", 111: "shanai", 114: "steel-drums",
}


def gm_name(program):
    return GM_NAMES.get(program, "prog%d" % program)


# The broad LEAD palette (two-layer model, this.i:c2k9p0a4): the STYLE owns the bed;
# the lead is chosen from this wide pool of melodic timbres — strings, winds, brass,
# keys, mallets, guitars, world/folk (koto, shamisen, kalimba, banjo, shanai, pan/
# wood flute…). program -> comfortable register CENTER (MIDI). A lead is eligible for
# a style if its center is within ~an octave of the style's register, and gets a high
# AFFINITY weight if it is one of that style's signature instruments, else a low base
# weight (so "weird-but-valid" leads — koto over swing — appear rarely, not never).
# (Oud and sitar are deferred per this.i:q9f3a7k2 / maintainer, so excluded here.)
LEAD_POOL = {
    0: 60, 4: 60, 6: 64, 7: 60, 8: 74, 9: 84, 10: 80, 11: 66, 12: 64, 13: 76,
    16: 60, 18: 60, 21: 60, 22: 64, 24: 60, 25: 62, 26: 62, 27: 62, 29: 62,
    40: 67, 41: 60, 42: 52, 45: 57, 46: 62, 53: 60, 56: 66, 57: 52, 59: 64, 60: 58,
    61: 60, 65: 66, 66: 58, 68: 70, 69: 62, 70: 50, 71: 62, 72: 84, 73: 74, 74: 72,
    75: 72, 77: 70, 78: 78, 79: 76, 80: 66, 81: 66, 105: 64, 106: 64, 107: 66,
    108: 66, 111: 68, 114: 64,
}
LEAD_SIG_W, LEAD_BASE_W, LEAD_REACH = 16, 1, 8               # signature ~80% (typical common); weird ~20% (rare)

# CAPABILITY attribute (this.i:c2k9p0a4): AGILITY 0..2 = how well a timbre carries a
# fast/syncopated melodic line (0 = slow/sustained-only, 2 = nimble/clean-attack).
# Default 2; only the less-agile timbres are listed. A style then REQUIRES a minimum
# agility for its lead, so a non-piano ragtime lead is allowed ONLY if it can actually
# play ragtime (clarinet/banjo yes; church-organ/pad no) — capability, not a hard lock.
LEAD_AGILITY = {
    10: 1, 16: 1, 18: 1, 19: 0, 42: 1, 53: 0, 57: 1, 60: 1, 69: 1, 70: 1,
    75: 1, 77: 1, 78: 1, 79: 1, 108: 1, 114: 1,
}
STYLE_MIN_AGILE = {                                           # what the idiom demands of its lead
    "ragtime": 2, "boogie_woogie": 2, "funk": 2, "samba": 2, "salsa": 2,
    "swing": 1, "blues": 1, "bossa_nova": 1, "march": 1, "reggae": 1, "tango": 1,
    "classical": 0, "baroque": 0, "gospel": 0,
}


def lead_choices(style):
    """(programs, weights) for the lead. The lead is chosen by a CAPABILITY gate
    (register reach + the style's minimum agility) AND an affinity weight (signature
    timbres dominate; capable others reachable-but-rare). So ragtime can take a
    clarinet or banjo lead over its piano stride bed, but not a church organ."""
    sig = STYLES[style]["leads"]
    sigset, center = set(sig), STYLES[style]["reg"].center
    min_ag = STYLE_MIN_AGILE.get(style, 0)
    progs, wts = [], []
    for p, c in LEAD_POOL.items():
        capable = abs(c - center) <= LEAD_REACH and LEAD_AGILITY.get(p, 2) >= min_ag
        if p in sigset or capable:
            progs.append(p)
            wts.append(LEAD_SIG_W if p in sigset else LEAD_BASE_W)
    return progs, wts


# The COMP and BASS pools (two-layer model extended to the rhythm section, c2k9p0a4 /
# this.i:c2k9p0a4): the STYLE names a SIGNATURE comp/bass program (high affinity) but
# the role is now drawn from a capability-tagged pool, so the same style's bed varies
# across inputs (the v12 "abysmal, always rock-organ" complaint) instead of being one
# fixed program. ATTACK 0..2 = how sharply a timbre can articulate an offbeat/plucked
# groove (0 = sustained-only organ/pad/strings; 1 = moderate; 2 = sharp/plucked). A
# style whose groove syncopates (reggae skank, funk stabs, salsa montuno) REQUIRES a
# minimum attack, so a sustained organ is never offered for a reggae bass — capability,
# not a hard lock; on-beat grooves (continuo, walking, oompah) still admit sustained.
COMP_POOL = {                                                # chordal-accompaniment timbres
    0: 60, 4: 60, 6: 64, 7: 60, 11: 66, 12: 64, 16: 60, 18: 60, 19: 60, 21: 60,
    24: 60, 26: 62, 27: 62, 48: 60, 53: 60, 61: 60, 71: 62,
}
COMP_ATTACK = {16: 0, 18: 0, 19: 0, 48: 0, 53: 0, 61: 1, 21: 1, 11: 1, 71: 1}  # organs/pads/strings sustain; brass/accordion/vibe/reed medium
BASS_POOL = {                                                # bass-register timbres
    32: 0, 33: 0, 34: 0, 35: 0, 36: 0, 42: 0, 43: 0, 58: 0,
}                                                            # value is unused (center fixed C2); kept for symmetry
BASS_ATTACK = {32: 2, 33: 2, 34: 2, 35: 1, 36: 2, 42: 1, 43: 1, 58: 1}  # plucked sharp; bowed/tuba medium
COMP_SIG_W, COMP_BASE_W = 64, 1                              # signature ~80% (maintainer pref); alts reachable-but-rare
BASS_SIG_W, BASS_BASE_W = 28, 1                              # bass pool is small (~7 alts) -> ~80% on the signature
# What each groove DEMANDS of its rhythm-section timbre (min ATTACK); default 0 (on-beat).
COMP_PAT_MIN_ATTACK = {"skank": 2, "funk16": 2, "montuno": 1, "shuffle": 1, "bossa": 1}
BASS_PAT_MIN_ATTACK = {"reggae": 2, "funk": 2, "tumbao": 2, "samba": 1, "boogie": 1,
                       "shuffle": 1, "walking": 1}
# A few timbres are too high/thin to be a CONVINCING bass even though they sit in range;
# and the march "pah" must not be a brass stab (v12 #03 "collection of horns" is ugly) —
# so brass/trumpet are excluded from the COMP pool offered to oom-pah styles.
COMP_NO_BRASS_PATS = {"oompah", "marcato"}


def comp_choices(style):
    """(programs, weights) for the comp (chordal bed): the style's signature program
    at high affinity plus capability-passing alternates at a low base weight, so the
    bed varies across inputs but stays idiomatic. The capability gate drops sustained
    timbres for syncopated grooves and brass from oom-pah comps (c2k9p0a4, v12 #03)."""
    s = STYLES[style]
    sig, pat = s["comp"], s["comp_pat"]
    if style in KEYBOARD_BED_STYLES:                         # the stride/ostinato bed IS the piano: no substitution
        return [sig], [1]
    min_at = COMP_PAT_MIN_ATTACK.get(pat, 0)
    no_brass = pat in COMP_NO_BRASS_PATS
    progs, wts = [], []
    for p in COMP_POOL:
        if no_brass and p in (56, 57, 59, 61):
            continue
        if COMP_ATTACK.get(p, 2) < min_at:
            continue
        progs.append(p)
        wts.append(COMP_SIG_W if p == sig else COMP_BASE_W)
    if sig not in progs:                                     # the signature is always eligible (it defines the idiom)
        progs.insert(0, sig)
        wts.insert(0, COMP_SIG_W)
    return progs, wts


def bass_choices(style):
    """(programs, weights) for the bass: signature program (high affinity) + capability-
    passing alternates (low base weight). A syncopated/plucked groove requires a sharp
    attack, so a bowed contrabass or tuba is not offered for a reggae/funk bass."""
    s = STYLES[style]
    sig, pat = s["bass"], s["bass_pat"]
    if style in KEYBOARD_BED_STYLES:                         # ragtime/boogie left hand is the same piano
        return [sig], [1]
    min_at = BASS_PAT_MIN_ATTACK.get(pat, 0)
    progs, wts = [], []
    for p in BASS_POOL:
        if BASS_ATTACK.get(p, 2) < min_at:
            continue
        progs.append(p)
        wts.append(BASS_SIG_W if p == sig else BASS_BASE_W)
    if sig not in progs:
        progs.insert(0, sig)
        wts.insert(0, BASS_SIG_W)
    return progs, wts


# --- RHYTHM-pattern variety (A2, v12 #08, this.i:r4d8m1k6) ------------------------
# The two-layer model (signature common, alternates rare) extended from INSTRUMENT to
# the groove's RHYTHM: each style's signature comp/bass pattern names a small FAMILY of
# idiomatic, metric-CONSERVING variants (this.i:m9p3k7a2 — every variant fills exactly
# the bar). The fingerprint draws a variant per input, so the same style's groove rhythm
# differs across inputs (the v12 "simple strong/weak alternation" complaint) while the
# signature stays dominant (PAT_SIG_W) and every variant stays inside the idiom. A base
# pattern with no listed family is its own only member. Keys are the style-declared
# comp_pat/bass_pat; values are (variant_names, affinity_weights).
PAT_SIG_W, PAT_VAR_W = 5, 2                                  # signature ~70%; each variant reachable-but-rarer
COMP_PAT_VARIANTS = {
    "alberti":  (["alberti", "alberti_up"],          [PAT_SIG_W, PAT_VAR_W]),
    "continuo": (["continuo", "continuo_synco"],     [PAT_SIG_W, PAT_VAR_W]),
    "comp4":    (["comp4", "charleston"],            [PAT_SIG_W, PAT_VAR_W]),
    "oompah":   (["oompah", "oompah_push"],          [PAT_SIG_W, PAT_VAR_W]),
    "bossa":    (["bossa", "bossa_partido"],         [PAT_SIG_W, PAT_VAR_W]),
    "montuno":  (["montuno", "montuno_synco"],       [PAT_SIG_W, PAT_VAR_W]),
    "skank":    (["skank", "skank_double"],          [PAT_SIG_W, PAT_VAR_W]),
    "funk16":   (["funk16", "funk16_synco"],         [PAT_SIG_W, PAT_VAR_W]),
    "shuffle":  (["shuffle", "shuffle_jab"],         [PAT_SIG_W, PAT_VAR_W]),
}
BASS_PAT_VARIANTS = {
    "root5":    (["root5", "root5_arp"],             [PAT_SIG_W, PAT_VAR_W]),
    "walking":  (["walking", "walking_skip"],        [PAT_SIG_W, PAT_VAR_W]),
    "stride":   (["stride", "stride_octave"],        [PAT_SIG_W, PAT_VAR_W]),
    "boogie":   (["boogie", "boogie_shuffle"],       [PAT_SIG_W, PAT_VAR_W]),
    "shuffle":  (["shuffle", "shuffle_walk"],        [PAT_SIG_W, PAT_VAR_W]),
    "reggae":   (["reggae", "reggae_drop"],          [PAT_SIG_W, PAT_VAR_W]),
    "tumbao":   (["tumbao", "tumbao_anticipate"],    [PAT_SIG_W, PAT_VAR_W]),
    "habanera": (["habanera", "habanera_dotted"],    [PAT_SIG_W, PAT_VAR_W]),
}


def comp_pat_choices(style):
    """(variant_names, weights) for the comp rhythm: the style's signature comp_pat at
    high affinity plus its idiomatic, metric-conserving variants at a low base weight."""
    base = STYLES[style]["comp_pat"]
    return COMP_PAT_VARIANTS.get(base, ([base], [1]))


def bass_pat_choices(style):
    """(variant_names, weights) for the bass rhythm: signature bass_pat (high affinity)
    plus its idiomatic, metric-conserving variants (low base weight)."""
    base = STYLES[style]["bass_pat"]
    return BASS_PAT_VARIANTS.get(base, ([base], [1]))


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


def palette_for(style, lead, comp=None, bass=None, comp_pat=None, bass_pat=None):
    """Assemble the palette. comp/bass (instrument) and comp_pat/bass_pat (groove rhythm)
    default to the style signature (back-compat) but are normally supplied by the engine
    from comp_choices/bass_choices (c2k9p0a4) and comp_pat_choices/bass_pat_choices
    (rhythm variety, r4d8m1k6)."""
    s = STYLES[style]
    comp = s["comp"] if comp is None else comp
    bass = s["bass"] if bass is None else bass
    comp_pat = s["comp_pat"] if comp_pat is None else comp_pat
    bass_pat = s["bass_pat"] if bass_pat is None else bass_pat
    if comp == lead and style not in KEYBOARD_BED_STYLES:    # never comp on the lead's own timbre (the v0.9
        comp = 48 if lead != 0 else 0                        # "organ-on-organ huffing"); contrast piano<->strings
    #   (keyboard-bed styles keep comp==piano: the stride bed needs the piano)
    return Palette(style, lead, comp, bass, lead, s["reg"],   # antiphon answers on the lead's own voice
                   comp_pat, bass_pat, s["perc"], s["perc_vel"], s["legato"])


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
    while out and out[0] < 50:                                # NEVER comp in the bass register (D3 floor):
        out = [x + 12 for x in out]                           # sub-bass voicings were muddy "ugly off-beat thunks"
    return sorted(out)


def _bn(pcs, role):
    """A bass MIDI note (C2 register) for a chord role."""
    semis = {"root": pcs[0], "third": pcs[1], "fifth": pcs[2],
             "sixth": (pcs[0] + 9) % 12, "b7": (pcs[0] + 10) % 12}[role]
    return BASS_C2 + semis


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
    elif pat == "alberti_up":                                  # ascending Alberti variant (bot-mid-top-mid)
        seq = [bot, mid, top, mid]
        for i in range(8):
            out.append(NoteEvent(VoiceRole.COMP, seq[i % 4], vel - 8, base + i * (B // 2), B // 2 - 4))
    elif pat == "continuo":                                   # baroque chord on each beat
        for beat in range(BEATS_PER_BAR):
            chord(beat, 1)
    elif pat == "continuo_synco":                             # baroque: sustained 1, syncopated push to 2& and 4
        chord(0, 1.5); chord(1.5, 0.5); chord(2, 1); chord(3, 1)
    elif pat == "comp4":                                      # swing/gospel light 4-to-the-bar chunks
        for beat in range(BEATS_PER_BAR):
            chord(beat, 0.5, vel - 6)
    elif pat == "charleston":                                 # the classic jazz Charleston: 1 + and-of-2
        chord(0, 1, vel - 4); chord(1.5, 0.5, vel - 4); chord(2.5, 1.5, vel - 8)
    elif pat in ("stride", "marcato"):                        # chord "pah" on the backbeats (2 & 4)
        chord(1, 0.75, vel - 2)
        chord(3, 0.75, vel - 2)
    elif pat == "oompah":                                     # march "pah" — LIGHTER than a block chord (v12 #03):
        pah = voic[1:]                                        # drop the lowest voice so the "pah" doesn't double into
        chord(1, 0.75, vel - 2, tones=pah)                   # the tuba's "oom" register (the muddy "collection of
        chord(3, 0.75, vel - 2, tones=pah)                   # horns"); the band answers ABOVE the bass, not on it
    elif pat == "oompah_push":                                # oom-pah with an extra anticipating "pah" (1& 2& 3& 4)
        pah = voic[1:]                                        # same lightened "pah" (drop the bass-register voice)
        chord(1, 0.5, vel - 2, tones=pah); chord(2.5, 0.5, vel - 4, tones=pah); chord(3, 0.75, vel - 2, tones=pah)
    elif pat == "bossa":                                      # nylon-guitar syncopation
        for beat, dur in [(0, 0.5), (1.5, 0.5), (2, 0.5), (3, 0.5)]:
            chord(beat, dur, vel - 4)
    elif pat == "bossa_partido":                              # partido-alto: anticipated 1& and 3&
        for beat, dur in [(0, 0.5), (1.5, 0.5), (2.5, 0.5), (3, 0.5)]:
            chord(beat, dur, vel - 4)
    elif pat in ("montuno", "montuno_synco"):                 # salsa piano: arpeggiated offbeats
        seq = voic + voic[-2::-1]
        beats = [0.5, 1, 1.5, 2.5, 3, 3.5] if pat == "montuno" else [0, 0.5, 1.5, 2, 3, 3.5]
        for i, beat in enumerate(beats):
            out.append(NoteEvent(VoiceRole.COMP, seq[i % len(seq)], vel - 4,
                                 base + int(beat * B), B // 2 - 4))
    elif pat == "skank":                                      # reggae offbeat stabs
        for beat in [0.5, 1.5, 2.5, 3.5]:
            chord(beat, 0.4, vel - 2)
    elif pat == "skank_double":                               # double skank: a quick pair on each off-beat
        for beat in [0.5, 0.75, 1.5, 1.75, 2.5, 2.75, 3.5, 3.75]:
            chord(beat, 0.2, vel - 4)
    elif pat == "funk16":                                     # funk 16th stabs (syncopated)
        for beat in [0, 0.75, 1.5, 2.25, 3, 3.5]:
            chord(beat, 0.25, vel)
    elif pat == "funk16_synco":                               # funk: a different 16th stab placement
        for beat in [0.25, 0.75, 1.25, 2, 2.75, 3.25]:
            chord(beat, 0.25, vel)
    elif pat == "shuffle":                                    # blues: on-grid backbeat chord jabs (no off-grid stutter)
        chord(1, 0.5, vel - 4)
        chord(3, 0.5, vel - 4)
    elif pat == "shuffle_jab":                                # blues: backbeats plus a pickup jab into 3
        chord(1, 0.5, vel - 4); chord(2.5, 0.5, vel - 8); chord(3, 0.5, vel - 4)
    return out


# --------------------------------------------------------------- bass grooves -
def bass_groove(pat, pcs, next_root_pc, base, vel):
    """Render one bar of bass in the style's idiom; beat 1 is always the root (so the
    harmony is grounded) — mid-bar notes may be idiomatic 6th/b7/passing tones."""
    out = []

    def note(role_or_pc, beat, dur, v=vel):
        m = _bn(pcs, role_or_pc) if isinstance(role_or_pc, str) else BASS_C2 + role_or_pc % 12
        out.append(NoteEvent(VoiceRole.BASS, m, v, base + int(beat * B), int(dur * B) - SUSTAIN_GAP))

    aim = min(("root", "third", "fifth"),
              key=lambda r: min((_bn(pcs, r) - (36 + next_root_pc)) % 12,
                                ((36 + next_root_pc) - _bn(pcs, r)) % 12))
    if pat == "root5":
        note("root", 0, 2); note("fifth", 2, 2)
    elif pat == "root5_arp":                                  # root-fifth arpeggiated to quarters
        for i, r in enumerate(["root", "fifth", "root", "fifth"]):
            note(r, i, 1)
    elif pat == "continuo":                                   # baroque walking quarters
        for i, r in enumerate(["root", "third", "fifth", "third"]):
            note(r, i, 1)
    elif pat == "stride":                                     # "oom" on 1 & 3 (ragtime/march)
        note("root", 0, 1); note("fifth", 2, 1)
    elif pat == "stride_octave":                              # stride with an octave leap on the "oom"s
        note("root", 0, 1); note(pcs[0] + 12, 2, 1)
    elif pat == "walking":                                    # jazz walking, last beat aims at next root
        for i, r in enumerate(["root", "third", "fifth", aim]):
            note(r, i, 1)
    elif pat == "walking_skip":                               # walking with a fifth-skip on beat 3
        for i, r in enumerate(["root", "fifth", "third", aim]):
            note(r, i, 1)
    elif pat == "boogie":                                     # eighth-note ostinato
        for i, r in enumerate(["root", "third", "fifth", "sixth", "b7", "sixth", "fifth", "third"]):
            note(r, i * 0.5, 0.5)
    elif pat == "boogie_shuffle":                             # boogie outlining root-3-5-6-5-3 (rocking)
        for i, r in enumerate(["root", "third", "fifth", "sixth", "fifth", "third", "fifth", "sixth"]):
            note(r, i * 0.5, 0.5)
    elif pat == "shuffle":                                    # blues shuffle bass
        for i, r in enumerate(["root", "fifth", "sixth", "fifth"]):
            note(r, i, 1)
    elif pat == "shuffle_walk":                               # shuffle that walks up root-5-6-b7
        for i, r in enumerate(["root", "fifth", "sixth", "b7"]):
            note(r, i, 1)
    elif pat == "twofeel":                                    # bossa two-feel
        note("root", 0, 2); note("fifth", 2, 2)
    elif pat == "samba":                                      # surdo emphasis (2& and 4&)
        note("root", 0, 1.5); note("fifth", 1.5, 0.5); note("root", 2, 1.5); note("fifth", 3.5, 0.5)
    elif pat == "tumbao":                                     # salsa anticipated bass
        note("root", 0, 1); note("root", 1.5, 0.5); note("fifth", 2.5, 0.5); note(aim, 3, 1)
    elif pat == "tumbao_anticipate":                          # tumbao with the bombo accent on 2& and the &-of-4
        note("root", 0, 1.5); note("fifth", 1.5, 0.5); note("root", 2.5, 0.5); note(aim, 3, 1)
    elif pat == "habanera":                                   # tango habanera cell
        note("root", 0, 1.5); note("root", 1.5, 0.5); note("fifth", 2, 1); note("fifth", 3, 1)
    elif pat == "habanera_dotted":                            # habanera with a dotted second half
        note("root", 0, 1.5); note("root", 1.5, 0.5); note("fifth", 2, 1.5); note(aim, 3.5, 0.5)
    elif pat == "reggae":                                     # spacious, syncopated
        note("root", 0, 1); note("root", 1.5, 0.5); note("fifth", 2.5, 1)
    elif pat == "reggae_drop":                                # reggae with a one-drop emphasis on beat 3
        note("root", 0, 1); note("fifth", 2, 1); note("root", 3, 1)
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
        elif pattern == "march":                              # bass drum on 1&3, snare backbeat (clean, no buzzy ruff)
            out += [_hit(KICK, vel, base), _hit(KICK, vel - 6, base + 2 * B),
                    _hit(SNARE, vel - 4, base + B), _hit(SNARE, vel - 4, base + 3 * B),
                    _hit(SNARE, vel - 20, base + 3 * B + B // 2)]   # one pickup into the next bar
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
    comp_vel = max(56, vel_base - 10)
    bass_vel = min(98, max(76, vel_base))                    # audible but capped (v0.10 hit 112 -> low-register distortion)
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
