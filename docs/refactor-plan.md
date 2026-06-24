# entmotif engine — refactor plan (architecture review, 2026-06-24)

Consolidated from two independent adversarial code reviews of `experiments/engine/motif.py`
(v0.7): **Codex / gpt-5.5** (`reviews/codex-arch-review-v0.7.md`) and a **Claude
architect** subagent (`reviews/claude-arch-review-v0.7.md`). They converged strongly;
this is the merged, ordered plan. Goal (Fowler): grow the code into the prescribed
musical metaphor (AGENTS.md §4) and separate concerns — *without changing output*.

## Why now / cadence
Milestone-gated, not every round. This is the natural moment: the engine is slated
to **graduate from `experiments/` prototype into a `src/` package with TDD** (AGENTS.md
§5), which is exactly the Fowler "cash in the accumulated mental model" point. Re-review
when the model next shifts materially (e.g. adding an emotional-register dimension).

## The two SACRED safety rules for this refactor
1. **`Chooser` label strings are a FROZEN WIRE FORMAT.** The literals (`"mode"`, `"sd"`,
   `"sd2"`, `"idea"`, `"dev%d"`, `"breath%d"`, `"ans%d"`, `"ctr"`, the `"%s_d%d"` melody
   keys, …) are hashed to drive every decision. **Rename Python identifiers freely;
   NEVER change a label literal** — doing so silently changes all output and breaks every
   golden file. Centralize them as named constants whose *values* are unchanged.
2. **Refactor only under green golden tests.** `test_golden.py` (built first, below) pins
   exact ABC text + MIDI bytes for the frozen corpus. Run it after every step.

## CRITICAL pre-existing bug to flag (needs maintainer sign-off — not in scope of a
## behavior-preserving refactor)
**Platform-sensitive determinism** (Codex severity 1): `Chooser.weighted()` uses float
accumulation and `gravity_delta()` uses `math.exp()`. `math.exp`/float rounding can
differ across platforms/libm versions → the same input could yield different MIDI on a
different machine, violating AGENTS.md §1 ("byte-identical on every platform"). Our tests
only check determinism on one machine. **Fix = integer threshold selection + a versioned
integer/fixed-point weight table; it CHANGES all output**, so do it as a deliberate
"invariant repair" with a golden re-baseline and explicit approval — last, not casually.

## Ranked problems (both reviewers)
1. (Codex) Platform-sensitive determinism — see above.
2. **God function `generate()`** — fingerprint + decisions + form + melody + dynamics +
   breath + arrangement + voice allocation + export metadata in one place.
3. **Primitive obsession / implicit schemas** — notes are positional 5-tuples, form units
   4-tuples, `meta` an untyped dict; `n[3]`, `mel[-1][4]` are undocumented APIs.
4. **`line()` 18-parameter signature** — a data clump (rhythm, harmony, range, timeline,
   contour policy, entropy, transform, voice, dynamics); positional mistakes stay type-correct.
5. **Stringly-typed, distributed decision protocol** — labels are output contract but look
   incidental; no central inventory (→ rule 1 above).
6. **Voice identity == MIDI channel number** (0/1/2/3 mean lead/comp/bass/answer in
   `generate`, `arrange_unit`, `abc_export`, `write_midi` independently).
7. **Magic numbers + mutable module globals** (beats/bar, channels, programs 48/32,
   velocities, −6 gaps, 1_000_000 scale; public mutable lists can alter output at runtime).
8. **Form/cadence as ad-hoc tuples + control flow** — incl. the round-4 "mutate the last
   unit to force resolution," which hides the terminal-resolves invariant.
9. **Exporters reach into generator internals** — ABC re-derives voices by filtering raw
   tuples; `write_midi` couples encoding with file I/O (can't get bytes without a file).
10. **Terse names** — `cpcs/snap/step/sym/cadc/figr/fat/chm/frac`; `_voice()` renders ABC,
    it doesn't model a Voice. (Full old→new table in the Codex review.)

## Target structure (both proposed ~identically) — `src/entmotif/`
`model.py` (frozen dataclasses `NoteEvent, Voice, Phrase, Palette, Motif` + enums
`Mode/VoiceRole/PhraseRole/CadenceKind/ArrangementTemplate/AccompanimentPattern/
BassPattern/Dynamic`; value objects `PitchRange, Development`) · `entropy.py`
(`fingerprint_text`, `DecisionSource`/`HashDecisionSource`, `DecisionKey` constants,
`choose_motif_decisions`) · `theory.py` (pure: scales/chords/voicing/nearest/degree) ·
`form.py` (`build` → `tuple[Phrase]`, cadence, development) · `melody.py`
(`MelodyContext`, `render_phrase`, cadence, breath — replaces `line()`) ·
`arrangement.py` (pattern strategy fns keyed by enum; `Palette` owns programs/ranges;
channel allocation once) · `engine.py` (`MotifComposer.compose(text)->Motif`, + a
temporary legacy `generate()` façade) · `exporters/{abc,midi}.py` (consume `Motif`;
`MidiEncoder.encode->bytes` separate from `write_midi(path,bytes)`) · `cli.py`.
Keep functions + frozen dataclasses; avoid GoF ceremony (strategy = dict→fn is enough).

## Ordered Fowler sequence (each step green-gated by test_golden.py)
1. **Golden characterization tests** — DONE (`test_golden.py`, this commit): exact ABC +
   MIDI sha for the frozen corpus; plus the existing `test_motif.py` invariants.
2. Extract pure `encode_midi(...)->bytes`; `write_midi` becomes `write_bytes(encode_midi())`.
3. Freeze compatibility constants (tuples/private), name the magic numbers — values UNCHANGED.
4. Rename leaf fns/locals (one cluster at a time) — NOT label literals.
5. Introduce `NoteEvent` with legacy-tuple conversion; hide indexing behind names; preserve sort keys.
6. Introduce `VoiceRole` + a single channel/program map.
7. Introduce `PitchRange`/`Development`/`MelodyContext` parameter objects (logic unchanged).
8. Rename+extract `line()`→`generate_melodic_line()`; pull out leap/next-pitch/snap/event helpers.
9. Replace form tuples with `Phrase` (same order; legacy projection kept).
10. Extract decision selection → `choose_motif_decisions()` (labels/options/weights preserved); add a decision-trace snapshot.
11. Extract form/cadence/development → `form.py`; make terminal-resolution a constructor invariant only after parity proven.
12. Extract melody + arrangement stages (move first, redesign second; preserve order).
13. Introduce the `Motif` aggregate; keep `generate()` as adapter.
14. Move theory ops → `theory.py` (table-driven tests, entropy-free).
15. Convert exporters to consume `Motif`; keep adapters until byte-identical.
16. Extract CLI (import = no side effects).
17. **(Approval-gated invariant repair)** integer/fixed-point determinism; golden re-baseline.
18. Remove compatibility adapters.
Do NOT collapse 10–17 into one commit — output drift must stay traceable.

## Execution note
This is read/edit-heavy; best run as a focused session of its own. The two safety rules
+ test_golden.py make aggressive renaming/extraction safe. Steps 1–9 are pure
behavior-preserving cleanup (high value, low risk); 10–16 are the structural payoff;
17 is the one that changes output and needs sign-off.
