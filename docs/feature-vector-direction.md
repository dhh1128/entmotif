# Direction proposal: corpus-mined feature vectors + conditional decision DAG

**Status: PROPOSED (maintainer, 2026-06-25), not started. A possible strategic pivot
away from purely hand-rolled generation. Captured durably so a fresh session can pick
it up.** Relationship to existing work: this is an *evolution* of `this.i:7c4m1k0p`
(conditioned probability distributions) — replacing hand-tuned priors/weights with
**data-derived conditional distributions** and a real **decision-dependency graph** —
NOT a throwaway of the engine (see "What transfers" below). Intent node:
`this.i:v8k2m1p0`; the dependency principle it rests on: `this.i:d2k9m4p1`.

## Why (the problem this solves)
After ~6 flywheel rounds the hand-rolled engine produces *coherent, recognizable*
music (≈C validity) but is stuck on two axes the maintainer named: **"extreme"
weirdness** and **"high" boringness**. Root causes that hand-tuning hasn't fixed:
1. **Compounding decisions are still modeled as FREE / independent** when they must be
   DEPENDENT. Concrete failures heard in the flywheel corpus:
   - *flute salsa (#01)*: the lead register sat below the flute's normal range — the
     register decision must be CONDITIONED on the chosen instrument's tessitura.
   - style→instrument convergence too weak: only 2/12 had genuinely style-suited
     instruments (06 piano ragtime, 08 swing guitar). Some weirdness is welcome
     (reggae clavinet, ragtime shamisen — novel but workable), but the *center* of the
     distribution isn't style-appropriate enough.
   - emotion is absent: nothing bold/dramatic/sad/lyrical — because mode/tempo/
     dynamics/articulation aren't conditioned on a single affect target.
2. **Hand-tuned weights don't capture what real music does.** We're guessing the
   priors. Real human-authored corpora encode the real conditional distributions
   (which intervals follow which, which instruments carry which genres, how dynamics
   track phrase position, how motifs are re-articulated). Popularity is a quality
   proxy: even non-masterpiece popular tunes rarely fall below our ≈C.

## The proposal
1. **Acquire a large corpus** of human-authored MIDI / lead sheets (thousands+),
   spanning genres; use popularity where available as a quality/representativeness
   signal.
2. **Mine probabilistic FEATURE VECTORS** (conditional distributions) for the
   dimensions the maintainer most wants — **motif development / re-articulation,
   emotion, dynamics, instrument choice** — plus register-per-instrument, groove/
   bass patterns, harmonic progressions, meter, phrase/contour, voicing density.
3. **Model decisions as a DEPENDENCY DAG** (`this.i:d2k9m4p1`): upstream master
   decisions condition downstream ones. Sketch of the order:
   `emotion → style/genre → meter → tempo → mode/harmonic-vocabulary →
    instrumentation → (per instrument) register/tessitura → groove/bass →
    motif shape → development/re-articulation → dynamics/articulation`.
   Each node draws from its **conditional** distribution given the already-decided
   ancestors (e.g. `P(register | instrument, style)`, `P(instrument | style, emotion)`,
   `P(transform | phrase-position, style)`, `P(dynamics | emotion, phrase-position)`).
4. **Map entropy → feature vectors** exactly as today's contract: the fingerprint
   bits pick a **point on each conditional distribution** (bell-curve / CDF inverse,
   tending toward the center = typical, full range reachable). This preserves
   determinism + avalanche + the discrete/analog bit law, and *strengthens*
   `this.i:7c4m1k0p` by making the distributions data-derived and conditional.
5. **Result:** much of the hand-rolled variability code collapses. After a
   decision-tree/DAG walk produces a fully-specified feature vector, the remaining
   code is mostly **assembly + render** (theory-legal realization → ABC/MIDI).

## What TRANSFERS from the current engine (not wasted)
- The **determinism/avalanche harness** + golden tests (the sacred invariants).
- The **entropy→decision** mechanism (`Chooser`; entropy picks the CDF point) — it
  just consumes conditional distributions instead of hand-tuned weights.
- The **exporters** (ABC/MIDI), the **model**/metaphor types, **music-theory**
  primitives, the **render/assembly** stage, and **metric conservation**.
- The **teaching/grading loop** + the canon + the memorability/earworm research
  (the rubric criteria become validation targets for the mined vectors).
- The **style/two-layer/capability** concepts (`z0m4p81q`, `c2k9p0a4`) become the
  *structure* of the DAG; the corpus fills in the *numbers*.

## Candidate datasets / prior art to investigate (verify licenses + suitability)
*(from memory — all `[verify]`; some may already ship feature vectors)*
- **EMOPIA** — pop-piano MIDI labelled by emotion quadrant (valence/arousal). Directly
  for the EMOTION feature vectors. **VGMIDI** — game MIDI with emotion labels.
- **Hooktheory / TheoryTab** — lead sheets (melody + functional harmony) WITH
  popularity, in relative/Roman terms. Excellent for harmony, hook, emotion, and the
  popularity quality-signal. (API/scrape; check ToS.)
- **Essen Folksong Collection** (~8k melodies, **Kern**, with phrase + meter +
  contour annotations) — melody/contour/meter features, incl. non-4/4.
- **Nottingham** (~1k folk tunes, ABC) and large **ABC tune** collections — directly
  parseable melody+chords.
- **Lakh MIDI** (~176k) / **MetaMIDI** (~436k, with genre metadata) — broad,
  multi-instrument; for instrumentation/arrangement/groove distributions.
- **POP909** — pop melody/lead/piano alignment (arrangement). **MAESTRO** — classical
  piano performances (expressive dynamics/timing). **GiantMIDI-Piano**, **ADL Piano**.
- Search for existing "symbolic music feature" toolkits: **jSymbolic / music21**
  feature extractors, **FANTASTIC** (melodic features), MIDI-emotion models.

## Open questions / risks
- License & ToS for each corpus (esp. scraped lead sheets).
- ML scope: start with simple **conditional histograms / n-gram + GMM** per feature
  before any heavy model — interpretable, deterministic to sample, and enough for
  bell-curve sampling. (A neural generator would break determinism/auditability — keep
  the model to *distributions we sample deterministically*, not an end-to-end NN.)
- How much of the bit-budget the data-derived distributions carry (re-audit
  `docs/bit-budget.md`).
- Meter expansion (`this.i:m4k0p2v9`) is a prerequisite for non-4/4 styles.

## Recommended path (incremental, low-regret) — to discuss
Do NOT big-bang rewrite. Two parallel, compatible moves:
- **(a) Build the dependency DAG now**, even with hand-tuned conditionals — it fixes
  the *independence* failures immediately (instrument→register, style→instrument
  convergence, emotion→cue coherence) without any corpus. This is `d2k9m4p1`.
- **(b) Mine the corpus** to *replace* the hand-tuned conditionals with data-derived
  ones, one dimension at a time (start with emotion via EMOPIA, and register-per-
  instrument, the two clearest wins), validated by the teaching loop.
The deterministic render pipeline + exporters + tests carry through both.
