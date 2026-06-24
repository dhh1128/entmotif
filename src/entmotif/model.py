"""entmotif core model — units, value types, and shared timing constants.

Frozen, behavior-free definitions shared across the engine. Deliberately
import-light (depends on nothing else in the package) so every other module can
import it without risking a cycle.

The musical metaphor (AGENTS.md §4): a :class:`NoteEvent` is the atom; a
:class:`Phrase` is a melodic unit (idea / answer / contrast) with its harmony,
cadence and development; :class:`VoiceRole` names the four instrument lines.
"""
from enum import IntEnum
from typing import NamedTuple, Optional

# --- timing / fixed-point constants -----------------------------------------
DIV = 480                       # MIDI ticks per quarter note
BEATS_PER_BAR = 4               # the 4/4 DEFAULT; meter is now per-piece (this.i:m4k0p2v9),
#   threaded as `beats` (beats-per-bar, quarter-note beat) so 4/4 stays byte-identical and
#   triple-meter idioms (waltz, 3/4) render correctly. Denominator stays /4 for now (the
#   beat is a quarter); compound 6/8-as-dotted is a later track.
WEIGHT_SCALE = 1_000_000        # fixed-point resolution for weighted choice

# Per-meter metric maps. STRONG_BEATS = the accented beat positions (where the melody
# snaps to a chord tone); METRIC_TARGETS = the whole, strong-beat-aligned cell lengths a
# tiled/diminished motif is padded/trimmed to so every repeat starts on a downbeat
# (metric conservation, this.i:m9p3k7a2, generalized off the 4/4 grid). Triple meter has a
# single strong beat (the downbeat) and aligns cells to whole bars (3 or 6 beats), never a
# sub-bar length that would flip the stress on each repeat.
_STRONG_BEATS = {2: (0.0,), 3: (0.0,), 4: (0.0, 2.0), 6: (0.0, 3.0)}
_METRIC_TARGETS = {2: (1.0, 2.0, 4.0), 3: (3.0, 6.0), 4: (1.0, 2.0, 4.0, 8.0), 6: (3.0, 6.0, 12.0)}


def strong_beats(beats):
    """The accented beat positions for a bar of `beats` quarter-note beats."""
    return _STRONG_BEATS.get(beats, (0.0,))


def metric_targets(beats):
    """The strong-beat-aligned cell lengths (in beats) a tiled motif snaps to."""
    return _METRIC_TARGETS.get(beats, (float(beats), float(beats) * 2))


def climax_unit(num_units):
    """The unit index that carries the placed climax: ~2/3 of the way through, the
    Huron arch peak. Integer-only so the register/dynamic arch is platform-stable."""
    return max(1, ((num_units - 1) * 2 + 1) // 3)


class VoiceRole(IntEnum):
    """The instrument lines. The *value* IS the MIDI channel, so a VoiceRole drops
    in anywhere the bare channel int was used — it compares, sorts, hashes and
    bit-ORs identically — while reading as a name. PERCUSSION is GM channel 9, the
    whole percussion family (drums AND shakers/claves/congas/agogo/cowbell/guiro/
    timbales/woodblock/triangle… — note numbers are percussion sounds, not pitches)."""
    LEAD = 0        # principal melody
    COMP = 1        # comping / harmony
    BASS = 2        # bass line
    ANSWER = 3      # antiphonal answer / counter-melody
    PERCUSSION = 9  # GM percussion family (idiomatic per style, not just a drum kit)


class NoteEvent(NamedTuple):
    """One sounding note.

    Tuple-compatible ``(chan, pitch, vel, start, dur)`` so it drops in wherever
    the legacy positional 5-tuple was used: it indexes, unpacks, sorts and
    compares identically, but exposes named fields. ``start``/``dur`` are ticks.
    """
    chan: int
    pitch: int
    vel: int
    start: int
    dur: int


class PitchRange(NamedTuple):
    """A registral window with a gravitational center (all MIDI note numbers)."""
    lo: int
    hi: int
    center: int


class Development(NamedTuple):
    """How a restatement is transformed from the germinal idea.

    ``offset`` is a scale-step transposition of the entry pitch; ``invert``
    mirrors the melodic contour about the head. (v0.8 will widen this to real
    motivic operations — sequence/augmentation/fragmentation.)
    """
    offset: int = 0
    invert: bool = False


class Phrase(NamedTuple):
    """A melodic unit and its harmony.

    Tuple-compatible ``(role, chords, cad, dev)`` so it unpacks exactly like the
    legacy form 4-tuple. ``role`` is "idea"/"answer"/"contrast"; ``chords`` is the
    two roman-numeral symbols for its two bars; ``cad`` is the cadence kind (or
    None); ``dev`` is the development slot index.
    """
    role: str
    chords: list
    cad: Optional[str]
    dev: int


class Motif(NamedTuple):
    """The whole rendered result for one input: the source value, the flat list of
    NoteEvents across all voices, and the decision/structure metadata. The
    exporters consume this (or the legacy ``(notes, meta)`` pair it wraps)."""
    value: str
    notes: list
    meta: dict
