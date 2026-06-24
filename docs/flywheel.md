# entmotif engine flywheel — autonomous improvement runbook

**Read `AGENTS.md` first (authoritative). This file is the operating manual for the
improve→grade→refactor loop. It is self-contained so no session has to be re-taught.**

## Sacred invariants (NEVER violate)
1. **Determinism** — same input → byte-identical MIDI on every platform. Integer-only
   decision math (no float in the decision path). See `this.i:h0v4k7m2` north star.
2. **Avalanche** — one-char input change → audibly different motif.
3. Both are enforced by `experiments/engine/test_motif.py`. Run it after EVERY change.

## TDD is mandatory (AGENTS.md §4)
- **Red → Green → Refactor.** Write a FAILING test in `test_motif.py` first, see it
  fail, then implement the minimal change to pass. Do NOT implement first.
- `experiments/engine/test_golden.py` pins exact ABC+MIDI for the 12-input corpus.
  After an INTENTIONAL output change: `python3 test_golden.py --update`, eyeball the
  diff, then commit. Both suites must end green.
- **Metric conservation** (`this.i:m9p3k7a2`): any rhythm transform conserves the
  bar's total duration; transformed durations stay on the 16th grid; tiled cells are
  padded/trimmed to a whole strong-beat length (1/2/4/8) so repeats land on the beat.

## The engine (clean package)
`src/entmotif/`: `model` (NoteEvent/Phrase/Palette/Motif/VoiceRole + constants) ·
`entropy` (fingerprint + Chooser; integer weighted()) · `theory` (scales/chords/
snap/step/degree) · `form` (Phrase sequence, cadence) · `melody` (germ shape,
`render_transform`, `cadence_bar`, gravity, dynamics; `_q16` grid snap) ·
`arrangement` (STYLES table = the master dimension; LEAD_POOL + capability gate
`lead_choices`; voice_chord; comp_groove/bass_groove/percussion_groove; Palette) ·
`engine` (`generate`→(notes,meta); `compose`→Motif) · `exporters/{abc,midi}` · `cli`.
`experiments/engine/motif.py` is a thin shim re-exporting the package (tests + the
teaching harness `import motif`).

## One flywheel cycle
1. **Pick** the top unblocked backlog item (below). Prefer well-specified, pattern-
   following items; be conservative on taste-heavy ones.
2. **TDD**: red test in `test_motif.py` → implement in `src/entmotif/` → green.
3. Keep determinism+avalanche green; if output changed intentionally,
   `test_golden.py --update` + eyeball.
4. **Regenerate scores**: `cd experiments/teaching && python3 make_scores.py vNEXT`.
5. **Grade (panel)** — the teacher review panel approximates the maintainer's ear
   (it is NOT a substitute for it; the maintainer re-listens at checkpoints):
   - 4 faculty subagents read `scores-vNEXT.md` + `prompts/teaching/rubric.md`:
     lyricism, memorability, creative-technique, arrangement
     (`prompts/teaching/{...}.md`). Each returns /100 + top findings.
   - A **Codex** substitute grader: `cat prompts/teaching/rubric.md scores-vNEXT.md |
     codex exec "grade on the rubric; per-lens /100; top fixes"` (Codex has caught
     cross-voice harmony bugs the Claude graders missed — keep it).
6. **Record** in `docs/engine-log.md`: round grades + convergent findings + the next
   fix list. **Commit** (`-s`) every cycle so progress is crash-safe + resumable.
7. **Every ~3 cycles**: a Martin-Fowler refactor pass (behavior-preserving, golden
   stays green): rename for clarity, extract functions, kill duplication, keep the
   musical metaphor. Commit separately.

## Memorability / earworm principles — APPLY to all melodic + form work (tick ~3yhb)
Convergent research (full synthesis + ~30 sources: `docs/memorability-research.md`
Part B; now also scored by `prompts/teaching/rubric.md`). Target these features; they
are the design spec for the melody/development work, not optional flavor:
1. **Familiar ARCH contour**, peak ~2/3 through, mostly small/stepwise intervals, with
   a FEW pointed surprises (signature leap). (We have the register arc + placed climax
   + gap-fill/post-skip reversal — keep them; the gap is the *contour journey*.)
2. **Distinctive recurring HOOK** (rhythm+interval, several pitches), reused per section.
3. **Repetition WITH development** at motif/phrase/section scales (transform on return).
4. **Medium-but-LOW surprisal** — sticky > clever (Frieler): bias the transform/contour
   choices toward the interesting-but-predictable end.
5. **Short, singable phrases** (~7–12 notes, ~a 10th range).
6. Emotion (Part C) and meter clarity reinforce memorability.
Western-conditioned caveat: mode/consonance are listener-relative; contour/interval/
phrase-length/meter are broadly human.

## Resource discipline (this machine is RAM-limited)
- ≤2 general-purpose subagents concurrent; ≤3–4 if extras are read-only. Prefix heavy
  shell with `nice -n 19 ionice -c 3`. Long renders/tests → redirect to a temp file.
- Audio: `fluidsynth -ni -F out.wav -r 44100 experiments/soundfont/sf/GeneralUser-GS.sf2 in.mid`
  (the maintainer listens; agents can't hear).

## Backlog, ranked (update as items land / new feedback arrives)
**A. Highest value, well-specified (do these first):**
1. ~~**Comp/bass INSTRUMENT variety + capability gate**~~ DONE (fw1, this.i:c2k9p0a4):
   comp/bass now mirror the LEAD two-layer model — a capability-tagged pool (ATTACK
   0..2) + per-style affinity (signature ~80%) + a role capability gate (sharp grooves
   reject sustained organ/pad bass; the march "pah" is a light reed, not a brass stab).
2. **Comp/bass RHYTHM-pattern variety** (v12 #08): the groove patterns read as
   simple strong/weak alternation. Add more idiomatic + varied comp/bass rhythms per
   style (and some intra-style variation), still metric-conserving.
3. **March comp fix** (v12 #03): the brass "collection of horns" oom-pah is ugly —
   make the "pah" a lighter/lower voice or lean on tuba(bass)+percussion.
**B. Big tracks (taste-heavy — be conservative; the maintainer re-listens):**
4. **Melodic development + MEMORABILITY** (tick `~77d7`/`~3yhb`) — **PRIORITY this
   round (maintainer): apply the earworm checklist above.** Melodies "orbit the
   center" instead of going somewhere and restatements feel samey; build real ARCH
   contour journeys, a reused multi-pitch HOOK, repetition-WITH-development, short
   singable phrases, and bias toward medium-LOW surprisal — guided by the
   "Memorability / earworm principles" section and now scored by the rubric.
5. **Emotional register master dimension** (`this.i:a7k0m3p9`): pick an emotion, then
   coherently align mode>tempo>dynamics>register>articulation>dissonance (Gabrielsson
   & Lindström order) so motifs feel sad/tense/mischievous/triumphant, not flat.
6. **Melodic triplets / swung-eighth lines** (tick `~6hld`): melody is 16th-grid only.
7. **Texture beyond lead+comp** (`this.i:p6m2v9k0`): homophony is baked in; add a
   texture dimension + N-voice model (quartet/contrapuntal/chorale/heterophony).
8. **Country twang / GS bank-select** (tick `~35rc`): reach the soundfont's Hawaiian/
   lap-steel via CC0/CC32 bank-select; add a country/honky-tonk style.
**C. Approval-gated / external:**
9. entviz-exact input normalization before hashing (tick `~4eu7`, `this.i:81pz4m0v`).

## Standing maintainer preferences (from listening rounds)
- Reject SIMPLIFICATIONS; expose music's variety; consume more of the hash with
  musically-VALID choices (`this.i:h0v4k7m2`). A consummate composer (John Williams)
  should call every choice a valid possibility.
- Genre-typical instruments common, weird-but-valid rare (signature ~80%).
- No deceptive finals (dropped). Endings should resolve (authentic/plagal); half
  cadences mid-phrase only.
- Percussion is the whole family, not a kit; bass + comp must be audible & idiomatic.
- Run `tick sync` when back online (ledger backup was pending).
