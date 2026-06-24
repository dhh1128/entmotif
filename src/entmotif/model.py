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
BEATS_PER_BAR = 4               # 4/4 throughout
WEIGHT_SCALE = 1_000_000        # fixed-point resolution for weighted choice


class VoiceRole(IntEnum):
    """The four instrument lines. The *value* IS the MIDI channel, so a VoiceRole
    drops in anywhere the bare channel int (0..3) was used — it compares, sorts,
    hashes and bit-ORs identically — while reading as a name."""
    LEAD = 0        # principal melody
    COMP = 1        # comping / harmony
    BASS = 2        # bass line
    ANSWER = 3      # antiphonal answer / counter-melody


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
