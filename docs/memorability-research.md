# Melodic Memorability & Emotion — Research Reference (annotated, citable)

What the research literature says about (a) what makes melodies **memorable /
recognizable / earwormy**, (b) what makes them **well-formed**, (c) **cross-cultural
universals**, and (d) which features produce which **emotional colors** — distilled
for entmotif's grading rubric (`prompts/teaching/`) and the engine's priors.

Compiled 2026-06-23 by a fan-out of read-only research agents (see
`prompts/canon/research-memorability.md`). **Verification convention** (as in
`docs/references.md`): entries are tagged `[canonical]` (well-established,
high-confidence, widely cited — safe to rely on), or `[verify]` (preprint,
under-review, or a specific number an agent reported that should be spot-checked
against the source before formal citation). Never cite a `[verify]` item as
confirmed. Sources are grouped; each has a URL for checking.

---

## Part A — Annotated bibliography

### A1. Earworms / involuntary musical imagery (INMI)
- **Jakubowski, Finkel, Stewart & Müllensiefen (2017), *Psych. of Aesthetics,
  Creativity & the Arts* 11(2)** `[canonical]` — "Dissecting an Earworm." 100 INMI
  vs 100 matched control tunes, 83 features. **Earworms = faster tempo + a *common
  global contour* (archetypal rise–fall) but *uncommon local interval patterns*
  (unusual gradients between turning points).** The "familiar shape, surprising
  details" formula. <https://www.gold.ac.uk/news/scientists-find-key-to-writing-catchy-pop-hits/>
- **Liikkanen & Jakubowski (2020), *Psychonomic Bulletin & Review* 27** `[canonical]`
  — review of 47 studies: INMI tunes have **longer note durations + smaller pitch
  intervals**; melody & lyrics are the most vivid dimensions. <https://pmc.ncbi.nlm.nih.gov/articles/PMC7704448/>
- **Williamson et al. (2012), *Psychology of Music* 40(3)** `[canonical]` — earworm
  *triggers*: recent exposure, memory associations, affect, low-attention states.
- **Killingly & Lacherez (2023), *QJEP* 76(11)** `[verify]` — repeated exposure
  (≈3–4 plays) drives earworm formation; recency effect. <https://pmc.ncbi.nlm.nih.gov/articles/PMC10585939/>
- **Arthur (2023), *Music & Science* 6** `[canonical]` — notes only *two* corpus
  feature studies exist; consistent profile = familiar contour + uncommon intervals
  + longer notes + small intervals. (Caveat: evidence base is narrow + correlational.)

### A2. Recognition memory for melodies
- **Dowling & Fujitani (1971); Dowling (1978); Dowling & Bartlett (1981); Dowling,
  Kwak & Andrews (1995)** `[canonical]` — the contour/interval timecourse:
  **contour dominates short delays; interval-in-tonality dominates after long
  filled delays**; rich, *real* (rhythmically-varied) melodies keep contour
  discriminable longer. (Also in `references.md`.) <https://link.springer.com/article/10.3758/BF03206500>
- **Schellenberg & Habashi (2015), *Memory & Cognition* 43(7)** `[canonical]` —
  novel melodies consolidate after **2 exposures, no forgetting over a week**;
  **timbre durable, key & tempo fade.** (Backbone of Model B; in `references.md`.)
- **Halpern & Müllensiefen (2008), *QJEP* 61(9)** `[canonical]` — timbre & tempo
  changes impair recognition; tempo JND ≈ 15–20%.
- **Müllensiefen & Frieler (2007) / FANTASTIC & SIMILE (Goldsmiths)** `[canonical]`
  — computational melodic-similarity toolsets (validated in plagiarism cases);
  best human-similarity model = rhythm-weighted pitch edit distance + distinct-note
  count. Useful to score a generated motif's distinctiveness vs a corpus.

### A3. Repetition & catchiness
- **Margulis (2014), *On Repeat* (Oxford UP)** `[canonical]` — repetition is
  "prosthetic memory": it drives learning, segmentation, expectation, and embodied
  engagement. Build repetition at micro (motif), meso (phrase), macro (section) scales.
- **Burgoyne, Bountouridis, van Balen & Honing (2013), ISMIR — "Hooked"**
  `[canonical]` — citizen-science recognition game; catchiness *is* measurable as
  recognition speed; the hook = the most quickly-recognized fragment. <https://webspace.science.uu.nl/~veltk101/publications/art/ismir2013-hooked.pdf>
- **Pawley & Müllensiefen (2012)** `[verify]` — sing-along field study: longer
  phrases and a chorus hook spanning **several distinct pitches** (not one note)
  with little ornament → more singalong.
- **Salimpoor et al. (2011), *Nature Neuroscience* 14(2)** `[canonical]` — dopamine
  in anticipation *and* peak; the prediction→confirmation loop is the reward engine
  (grounds "tension then resolution"). <https://www.nature.com/articles/nn.2726>
- **Kallinen & Ravaja (2006), *Perception & Psychophysics* 68(1)** `[canonical]` —
  mere-exposure: repeated hearing raises both liking and recognition.

### A4. Expectation & "well-formed melody" theory
- **Meyer (1956), *Emotion and Meaning in Music*** `[canonical]` — emotion arises
  from expectations established then delayed/violated; full predictability = boring,
  total violation = incomprehensible. Establish a pattern (2–3×), then surprise.
- **Narmour (1990/92) Implication-Realization** `[canonical]` — small interval →
  expect continuation; **large leap → expect reversal (gap-fill)**; closure at
  reversals.
- **Schellenberg (1997, 2002)** `[canonical]` — I-R simplifies to **two factors:
  pitch proximity (expect the next note close) + pitch reversal (reverse after a
  leap)**; predicts listener ratings as well as the full model (r≈0.7). <https://pubmed.ncbi.nlm.nih.gov/12500861/>
- **Huron (2006), *Sweet Anticipation* (MIT)** `[canonical]` — ITPRA; **post-skip
  reversal = regression to the mean** captures ~80% of gap-fill simply (a leap to
  a register extreme tends to return toward center).
- **Pearce — IDyOM (2005/2018)** `[canonical]` — statistical learning: expectation =
  −log₂ P(note | context); **optimal interest ≈ medium surprise (~2–4 bits)**;
  too predictable = dull, too surprising = incoherent. <https://pmc.ncbi.nlm.nih.gov/articles/PMC6849749/>
- **Temperley (2008), *Music and Probability*** `[canonical]` — melodies favor a
  narrow range (~1.5–2 octaves), small intervals (mode 1–2 semitones), and key-profile fit.

### A5. Computational / corpus memorability
- **Frieler et al. (2017), *Frontiers in Psychology* 8:621** `[verify]` — folk-song
  memorability corpus: **shorter phrases (~7–12 notes), smaller intervals, earlier
  (primacy) position, and *lower* surprisal predict memorability**; higher surprisal
  did NOT aid recall. Model explained ~22% of variance. <https://pmc.ncbi.nlm.nih.gov/articles/PMC5403935/>
- **Simonton (1980)** `[canonical]` vs **Gripchuk et al. (2022, arXiv)** `[verify]`
  — melodic originality (uncommon 2-note transitions) ↔ thematic fame: Simonton
  found a positive link across 15,618 themes; a Romantic-era replication found none
  → originality's value is era/context-dependent. **Treat "originality" as a
  low-weight, contextual feature.**
- **"Music memorability" ML dataset (2024, arXiv:2405.12847)** `[verify]` —
  modest predictors (ρ≈0.30): arousal, tempo, harmony, melody prominence, timbre.

### A6. Cross-cultural universals (what's broadly human vs Western)
- **Savage, Brown, Sakai & Currie (2015), *PNAS* 112(29)** `[canonical]` — 304
  recordings / 60 societies. Statistical universals: **discrete pitches, ≤7 scale
  degrees/octave, descending or arched contours of small intervals (<~P5),
  isochronous beats in 2s/3s, and near-universal repetition (~94%).** <https://www.pnas.org/doi/10.1073/pnas.1414495112>
- **Tierney, Russo & Patel / Tierney et al. (2021), *Frontiers*** `[verify]` —
  iterated-learning: these universals *emerge* from cognitive bias (discretization,
  ≤~5 degrees, arch contour, small intervals, motif repetition, short phrases <9s).
- **Huron (1996), "The Melodic Arch in Western Folksongs"** `[canonical]` — arch
  contour is over-represented; **peak typically ~2/3 through the phrase** (not the
  midpoint). Directly supports a *placed* climax.
- **McDermott et al. (2016), *Nature* 535** `[canonical]` — **consonance preference
  is NOT universal** (Tsimané indifferent); structure (discretization, contour,
  small intervals) is broadly shared, but consonance/dissonance *aesthetics* are
  enculturated. <https://www.nature.com/articles/nature18635>
- **Jacoby & McDermott (2017), *PNAS* 114(13)** `[canonical]` — integer-ratio
  rhythm priors are cross-cultural (favoring 2:1/3:1 metrical structure).

### A7. Emotion → musical features
- **Gabrielsson & Lindström (2001/2010), in Juslin & Sloboda (eds.)** `[canonical]`
  — the key feature→emotion review. **Cue importance: mode > tempo > register >
  dynamics > articulation > timbre** (additive, ~77–89% of rating variance linear).
  Happy = major+fast+high+loud+staccato+bright; Sad = minor+slow+low+soft+legato+dark;
  Peaceful = soft+warm+legato (dynamics/timbre dominate); Scary = minor+fast+high+irregular. <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3726864/>
- **Eerola & Vuoskoski (2011), *Music Perception* 28(4)** `[canonical]` — **3
  dimensions: valence (mode/consonance), energy-arousal (tempo/loudness/register),
  tension-arousal (dissonance/irregularity).** <https://journals.sagepub.com/doi/10.1177/0305735610362821>
- **Juslin & Laukka (2003); Juslin (2013)** `[canonical]` — 5 basic emotions
  (happy/sad/anger/fear/tenderness) with vocal-iconic acoustic profiles; **cue
  redundancy** (no single cue is necessary — sadness via slow+low+legato survives
  without minor mode). <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3764399/>
- **Balkwill & Thompson (1999); Hevner (1936)** `[canonical]` — psychophysical cues
  (tempo, loudness, register, rhythm regularity) are cross-cultural; mode &
  consonance are enculturated. Hevner's adjective circle = an early affect map.
- **Smit et al. (2022), *PLOS ONE*** `[canonical]` — major=happy is largely
  *enculturated* (PNG minimal-exposure communities don't show it). (Also in
  `references.md`.) <https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0269597>

---

## Part B — Synthesis: features of memorable melodies (ranked, actionable)

Convergent across the literature. Mapped to our **rubric** and **engine**.

1. **Familiar contour + surprising details** (Jakubowski; Frieler; Savage; Huron-arch).
   A *common, arched* global shape (peak ~2/3 through) with mostly small intervals,
   carrying a *few* uncommon local moves. → Rubric: reward arch + a placed peak +
   stepwise motion with 1–3 pointed surprises. Engine: arch register-arc with the
   climax ~2/3 through; gravity (we have it) + a small budget of pointed leaps.
2. **A distinctive, recurring rhythm-+-interval hook** (Margulis; Burgoyne;
   Jakubowski). → the engine's persistent #1 gap; a clappable signature reused.
3. **Repetition at multiple scales, with development** (Margulis; Meyer). Repeat,
   but transform on return (sequence/inversion) — pure copy is dull.
4. **Small intervals as default, with gap-fill** (Narmour; Schellenberg; Huron;
   Temperley; Savage). Leap → step back toward center. **We already do this**
   (gravity + leap-recovery = post-skip reversal).
5. **Medium surprise (~2–4 bits)** (Pearce). Not too predictable, not chaotic. But
   note Frieler: for *memorability* specifically, *lower* surprisal helped — so
   tune toward the lower end of "interesting."
6. **Short, singable phrases** (~7–12 notes, <~9s; ~a 10th range) (Frieler; Tierney;
   Temperley). Supports our tessitura work.
7. **Two-exposure learnability + durable timbre** (Schellenberg & Habashi). Re-hearing
   is realistic; lean on timbre/style (our master dimension) for durability.
8. **Clear, isochronous meter in 2s/3s** (Savage; Jacoby & McDermott).

**Cross-cultural caveat:** items 1, 4, 6, 8 and *energy/tension* are broadly human;
**mode→valence and consonance→pleasure are enculturated** (Smit; McDermott;
Balkwill & Thompson). entmotif's mode/cadence bits are Western-listener bits.

---

## Part C — Emotion → feature mapping, and "emotional register" as a master dimension

The research strongly supports making **emotional register a top-level entropy
choice that conditions downstream decisions coherently** (exactly the architecture
of `style`). Cue precedence (Gabrielsson & Lindström): **mode > tempo > register >
dynamics > articulation > timbre.**

| Register | Mode | Tempo | Register/pitch | Dynamics | Articulation | Timbre | Harmony/rhythm |
|---|---|---|---|---|---|---|---|
| **Happy** | major | fast | high | loud | staccato | bright | consonant, regular |
| **Sad** | minor | slow | low | soft | legato | dark | consonant, steady |
| **Peaceful** | maj/min | slow–mod | low–mid | soft | legato | warm | consonant, smooth |
| **Tense/Fearful** | minor | fast/variable | high | unpredictable | staccato + irregular | sharp | dissonant, irregular |
| **Triumphant** | major | mod–fast | high | loud | emphatic | brass | consonant + accents |
| **Tender** | maj/min | slow | low–mid | soft | legato | warm | consonant, flowing |

**Why it matters (Daniel's instinct, confirmed):** a single affect target makes a
*coherent* set of downstream choices — the cues reinforce instead of contradicting.
Use **cue redundancy** (Juslin): don't require mode; for cross-cultural robustness,
lean on tempo/register/dynamics/articulation/rhythm (psychophysical, universal) and
treat mode/consonance as Western-listener reinforcement.

---

## Part D — Implications for entmotif

- **Rubric:** add/ sharpen criteria for: placed arch climax (~2/3 through); a
  recurring rhythm-+-interval hook; repetition-with-development; gap-fill; ~7–12-note
  singable phrases; medium-low surprisal. Tag mode/consonance criteria as
  Western-listener-conditioned.
- **Engine priors:** we already implement gap-fill/post-skip-reversal (good — it's
  Narmour/Huron), tessitura, and a register arc. Strengthen the *placed* climax
  (peak ~2/3), the hook, and development-on-restatement. Add **emotional register**
  as a master conditioned dimension (Part C) and **dynamics** as an analog layer
  (below).
- **Validation:** the canon ("grade the greats") + the FANTASTIC/SIMILE similarity
  tools give external checks; the A/B/X listening study remains the ground truth.

## Caveats

The corpus evidence for *memorability specifically* is thin (only two feature
studies; Frieler's model explains ~22%). Originality is context-dependent. Mode and
consonance are enculturated. `[verify]` items (preprints, specific reported numbers)
must be spot-checked against the source before any formal citation (e.g. in the paper).
