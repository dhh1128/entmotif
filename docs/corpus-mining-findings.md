# Corpus-mining findings — first batch

**What this is.** The first batch of data-derived conditional distributions for the
corpus pivot (`this.i:v8k2m1p0`, `docs/feature-vector-direction.md`), mined by the
re-runnable pipeline in `tools/mining/` from two corpora. It reports *what the data
says*, with sample-size and confound caveats, and recommends which mined vectors to feed
the generator first. It does **not** change `src/entmotif/` — the engine mapping is
proposed here for a later, separately-reviewed wiring step.

**Method.** Pure-Python parsers (no `music21`/`mido`) → a normalized IR (beats + MIDI
pitch) → small committed histograms/percentiles in `data/features/`. Idempotent
(byte-identical re-runs). Datasets, licenses, and the vetted starter set are in
`docs/corpus-survey.md`. The interpretations below were **cross-checked with an
independent model (Codex)**, whose confound list is folded into the caveats.

**Corpora mined (this batch).**
- **TheSession** — 54,721 Irish-trad tune settings (ABC). ODbL; fetch-only, stats committed.
- **EMOPIA** — 1,078 of 1,087 emotion-labelled solo-piano MIDI clips (9 failed to parse).
  CC BY 4.0; fetch-only, stats committed.
- **Nottingham** — 1,034 English/American country-dance tunes (ABC, chords on nearly
  every tune). GPLv3; fetch-only, stats committed. Added to harden the (thin) harmony
  dimension and exercise the multi-tune ABC loader.

---

## ⚠️ Read the caveats first (they bound every number below)

1. **EMOPIA clips are not independent.** 1,087 clips come from only **387 songs**, so
   per-clip aggregates over-weight repeated songs/performers/arrangements. Treat
   per-quadrant n (~250–310) as *effective* << nominal.
2. **EMOPIA velocity and key are machine-derived.** The MIDI is *automatically
   transcribed* from audio: velocity confounds performance + recording/mastering +
   transcription behavior (it is **not** calibrated loudness), and our `mode` is a
   Krumhansl-profile *estimate* on top of that — a heuristic on heuristic data.
3. **EMOPIA tempo metadata is uniformly 120 BPM** — a transcription artifact, *useless*
   as an arousal cue. Consequently our **`note_density_per_beat` is effectively
   notes-per-second** (beats are fake), so it partly *encodes* the real performance
   tempo rather than beat-relative busyness. Useful as an arousal proxy, but label it
   honestly.
4. **Russell quadrants are valence–arousal regions, not categorical emotions.** "Q2 =
   angry / Q3 = sad" are convenient glosses, not labels in the data.
5. **TheSession has duplicate settings/variants and contributor-entered metadata.** We
   did **not** dedup; modal/meter percentages shift with filtering (a reviewed
   ~23.6k-tune subset in the literature reports different modal totals). `meter`/`mode`
   are TheSession's own fields, not analyzed — they inherit contributor error.
6. **Interval stats are over whole tunes, not phrases.** Median TheSession melody is
   **112 notes** — full multi-section instrumental tunes, not singable phrases — and we
   did not strip ornaments/repeats or segment phrases. So "stepwise %" and "arch peak"
   are tune-global, and the singable-phrase memorability targets can't be read directly.

---

## Findings by dimension

### EMOTION → musical cues  (EMOPIA; `data/features/emopia.emotion.json`)  **[priority]**
The cleanest, most actionable result in the batch — emotion conditions the cues
*coherently*, which is exactly the gestalt `this.i:a7k0m3p9` says the engine lacks.

| Quadrant (gloss) | mode | median velocity | median density* | n |
|---|---|---|---|---|
| Q1 happy (HV/HA) | **62% major** | 77 | 4.1 | 250 |
| Q2 tense (LV/HA) | **88% minor** | 79 | 5.0 | 265 |
| Q3 sad (LV/LA) | **73% minor** | 55 | 2.2 | 253 |
| Q4 calm (HV/LA) | **53% major** | 52 | 2.1 | 310 |
\* density = notes per (fake) beat ≈ notes/sec — see caveat 3.

- **Valence → mode** is strong and monotone: the two low-valence quadrants are
  predominantly **minor** (Q2 88%, Q3 73%), the high-valence ones lean major. This is a
  real, usable conditional `P(mode | emotion)` — modulo the auto-key caveat.
- **Arousal → loudness + density** is clean: high-arousal Q1/Q2 sit ~**25 velocity
  points louder** and ~**2× denser** than low-arousal Q3/Q4. (Density and velocity are
  correlated here and both confounded by performance tempo — treat as one "energy"
  axis, not two independent bits.)
- **Tempo is NOT a usable cue from EMOPIA** (flat 120). Arousal must come from
  density/velocity/articulation, or from a different corpus.
- **Register barely moves** with emotion (medians 60–63) — do not over-condition register
  on emotion from this corpus.

### REGISTER per instrument  (EMOPIA; `data/features/emopia.register.json`)
- Only **program 0 (piano)** appears — EMOPIA is solo piano. Piano tessitura over
  285,638 notes: p5=38, p50=62, p95=83.
- **This is the batch's biggest gap, not a win.** The brief suggested *emotion +
  register-per-instrument* as the two first wins, but **register-per-instrument cannot
  be mined from the current permissive starter set**: EMOPIA is single-instrument and
  the ABC corpora carry no instrument at all. `P(register | instrument)` needs a
  multi-instrument MIDI corpus (Lakh / MetaMIDI), which is deferred on license grounds
  (survey). See "What to do next."

### CONTOUR / interval shape  (TheSession; `data/features/thesession.contour.json`, `…interval_ngram.json`)
- **Strongly stepwise** (tune-global, un-segmented — caveat 6): of melodic intervals,
  unison 10%, m2 14%, **M2 36%**, m3 16%, M3 10% → **~60% within a whole tone, ~86%
  within a minor third.** Leaps ≥ P5 are ~7%. Empirically backs the "mostly small/
  stepwise with a few pointed leaps" memorability spec.
- **Slight descending lean**: down 46.5% / up 43.4% / repeat 10.2%. Too small to call a
  strong gravity bias without per-tune controls (Codex), but *directionally consistent*
  with the engine's register-gravity prior (`this.i:7c4m1k0p`). Don't over-claim it.
- **Interval momentum is real and usable** (`interval_ngram.transition`): after a step
  *up* (+2) the next move is most often another +2 (24%) or a reversing −2 (22%) or +1
  (16%); after a step *down* (−2) it continues −2 (24%) / −3 (19%) / −1 (15%). Sampling
  from this first-order chain is what makes a line *travel* instead of orbiting the
  tonic — the single most direct fix for "melodies orbit the center."
- Tune-global arch peak: median 0.5, p75 0.62 (not the phrase-level "~2/3" target —
  caveat 6). Median melodic range ~19 semitones; median length 112 notes (whole tunes).

### MODE  (TheSession; `data/features/thesession.mode.json`)
- Overall: **major 64%, minor 15.5%, dorian 13.6%, mixolydian 6.9%.** So **~20% is
  modal** and roughly stable across dance types (reel, jig).
- **Surprise / actionable:** a binary major/minor knob (`mode_w`) cannot represent a
  fifth of this idiom. For *stylistic fidelity* in folk styles the engine wants dorian +
  mixolydian as first-class options. (Caveat: for a *coarse emotion-control* dimension,
  major/minor may still suffice — modal ≠ required everywhere; Codex.)

### METER  (TheSession; `data/features/thesession.meter.json`)
- **Only 52% is 4/4.** 6/8 25%, 3/4 8%, 2/4 8%, 9/8 3.6%, 12/8 2.1%, 3/2 0.8%.
- In this corpus **meter is essentially a function of dance type** (jig→6/8, reel→4/4,
  waltz/mazurka→3/4, polka→2/4, slip-jig→9/8, slide→12/8) — a clean hard-edge for the
  DAG (`genre → meter`), and concrete fuel for the meter-expansion track
  (`this.i:m4k0p2v9`). **Bias caveat:** TheSession is Celtic *dance* music — this is the
  meter distribution *of Irish trad*, **not** of music at large; do not read it as a
  universal `P(meter)`.

### HARMONY  (`data/features/{thesession,nottingham}.harmony.json`)
- Coverage differs sharply: only **4,827 of 54,721** TheSession tunes carry ≥2 inline
  chords (most Session ABC is melody-only), vs **1,021 of 1,034** Nottingham tunes —
  Nottingham is the better harmony source despite being smaller.
- **TheSession** root motion is fifth-dominated: up-a-4th (= down a 5th, the V→I motion)
  **29%**, up-a-5th **20%**, up-a-2nd 15%, repeat 12%; qualities maj 69% / min 23.5% /
  dom7 5.6%.
- **Nottingham** corroborates fifth-based functional motion but with **far more dominant
  7ths** (dom7 **21.5%** vs 5.6%; maj 61%, min 16%) — the explicit `"A7"/"E7"` cadential
  chords of English country dance. **Takeaway:** dom7 frequency is *style-dependent*, so
  the harmony prior should be conditioned on style, not pooled — a concrete `P(quality |
  style)` the engine can use. Both are usable as `P(next-root | root)` progression priors
  (small-sample caveat on TheSession).

### DYNAMICS arc  (EMOPIA; `data/features/emopia.dynamics.json`)
- Within-piece velocity arc is **weak/flat** (median 68→72 rising to ~0.7–0.9, dipping
  at the end) once aggregated across 1,078 pieces of differing length. The *real*
  dynamics signal is **between emotions** (Q1/Q2 ~78 vs Q3/Q4 ~52), already captured by
  the emotion feature. Don't build a within-phrase dynamics curve from this corpus.

---

## Surprises
- **TheSession is barely half 4/4** (52%) and **one-fifth modal** — both larger than the
  engine's current 4/4-only, major/minor world assumes (for this idiom).
- **EMOPIA tempo is a dead field** (uniform 120); the arousal signal hides in density +
  velocity instead. A reminder to validate every field before trusting it.
- **Valence→minor is sharp** (Q2 88% minor) — a stronger, cleaner emotion→mode signal
  than expected from machine-estimated keys.

## Gaps (what this batch can NOT tell us yet)
- **Register-per-instrument** — blocked: no multi-instrument permissive corpus mined
  (EMOPIA = piano only; ABC = no instruments). The flute-salsa fix (`this.i:d2k9m4p1`)
  needs Lakh/MetaMIDI-class data.
- **Instrumentation / groove / voicing-density** — same blocker (needs multi-track MIDI).
- **Phrase-level** contour/length/arch and **motif re-articulation/development** — needs
  phrase segmentation + ornament stripping the parser doesn't do yet; current stats are
  tune-global.
- **A non-Celtic meter/contour baseline** — everything melodic here is Irish dance music.
  Genre breadth (the whole point of entmotif) needs a broader corpus.

## Recommended order to feed the generator
1. **EMOTION first** (`emopia.emotion.json`). It is the cleanest result and targets the
   open north-star debt `this.i:a7k0m3p9`. Concrete wiring (hand-mapped, to review):
   - `P(mode | emotion)` → bias the `mode_w` major/minor knob per chosen emotion
     (Q2/Q3 → minor-heavy, Q1/Q4 → major-heavy).
   - one **arousal→energy** axis from velocity+density (they co-move) → comp/lead
     velocity bands and lead note-density / breath spacing. **Do not** wire EMOPIA tempo.
   - keep register weakly/​not conditioned on emotion (it barely moved).
2. **Interval-momentum chain** (`thesession.interval_ngram.json`) → replace independent
   per-note interval draws with first-order `P(iv_n | iv_{n-1})` sampling. Directly
   attacks "melodies orbit the center"; preserves determinism (the Chooser samples a CDF
   point of the conditional, `this.i:7c4m1k0p`).
3. **Modal + meter** (`thesession.mode.json`, `…meter.json`) → as the *structure* fills
   in the meter-expansion track (`this.i:m4k0p2v9`): add dorian/mixolydian options and a
   `genre → meter` hard edge. Use TheSession numbers only for the Celtic styles; do not
   globalize them.

**Register-per-instrument** — the brief's other suggested first win — is **deferred to a
second mining wave** with an explicit reason: no permissive multi-instrument corpus is
in hand. Next wave should evaluate fetch-only Lakh/MetaMIDI stats (survey) for
`P(pitch | GM program)` and instrumentation/groove, which this batch's `register`/`contour`
extractors already compute once such MIDI is loaded.
