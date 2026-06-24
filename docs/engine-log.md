# Engine Improvement Log (report card)

The saved history of the entmotif motif engine's successive improvements and what
drove them. Each round: the faculty GPA, per-lens grades, the change made, and the
teacher feedback that motivated it. Process: `prompts/teaching/orchestrating-teaching.md`.

Corpus: `experiments/teaching/corpus.txt` (frozen). Rubric:
`prompts/teaching/rubric.md` (normalized). Engine: `experiments/engine/motif.py`.

| Round | Engine | Faculty mean | Lyricism | Memorability | Creative | Arrangement | Codex(gpt-5.5) | Driving change |
|---|---|---|---|---|---|---|---|---|
| 1 | v0.4 | ~70 (C−) | C− 71 | 57* | C+ 77 | C− 72 | C 74 | develop restatements; tessitura; climax+cadence; rhythmic signature |
| 2 | v0.5 | ~73 (C) | C+ 77 | C+ 78 | C 75 | C 73 | **D 63** | **KEY-TRANSPOSITION BUG** (Codex); real rhythmic hook; placed climax; motivic development; arrangement mechanics |
| 3 | v0.6 | ~78 (C+) | C 74 | C+ 77 | B 84 | B− 81 | C− 72 | key fix✓; **bass chord-quality bug** (Codex); lead-silence in short call_resp; placed climax; rhythmic hook; V:4 develops |
| 4 | v0.7 | ~77 (C+) | C+ 78 | B− 81 | C+ 74 | C+ 75 | C 75 | bass-quality fix✓; resolved finals✓; dynamics arc✓; 2/3 climax✓; **v0.8 headline: real MOTIVIC TRANSFORMATION (stop restating)** |

\* Memorability reported "C+ / 57" — an internally inconsistent grade that exposed
a missing /100↔letter mapping; the rubric was given explicit bands after round 1
(57 ≈ F by the band, ≈ C− by the teacher's prose). Use the /100 numbers as the
canonical trend until round 2 re-grades on the banded rubric.

---

## Pre-loop changelog (by ear, before the teaching loop)

- **v0.1** — first 8-bar antecedent/consequent period; strong-beat chord tones;
  determinism + avalanche. (Built to fill the review's "no engine" CRITICAL.)
- **v0.2** — rest-bearing rhythm; thin bed; entropy-driven register (C2–C5),
  leapiness, and resolution (incl. non-resolving). *Ear: "marked improvement."*
- **v0.3** — bound rhythm-+-interval signature; entropy-driven form & length
  (sentence/period/period_tag/aaba); lyrical breaths at phrase boundaries only.
- **v0.4** — conditioned probability distributions (register-gravity melodic
  shape; musical priors); wider tempo (60–184); answer varies in rhythm/shape,
  not just cadence.

## Round entries

### Round 1 — engine v0.4 (2026-06-23)

Faculty: lyricism, memorability, creative-technique, arrangement (Claude subagents)
+ a generalist substitute teacher (Codex / gpt-5.5). Graded the 12-input frozen
corpus from ABC lead-sheets (`experiments/teaching/scores-v0.4.md`). Reports:
`grade-codex-v0.4.txt` + the subagent returns.

**Grades (/100):** lyricism 71 (C−) · memorability 57 (miscalibrated, see above) ·
creative-technique 77 (C+) · arrangement 72 (C−) · Codex overall 74 (C). **Mean ≈ 70 (C−).**

**Dean synthesis — convergent findings (all five graders agree):**
1. **Verbatim restatement.** AABA/period repeats are byte-identical; "answer-var"
   barely audible; variation lands only at the cadence. → Need real motivic
   *development* (sequence, inversion, augmentation, fragmentation) and mid-phrase
   variation on every restatement.
2. **Broken register/tessitura.** Melodies sit in extreme low (sub-bass) or high
   (top-octave) registers and stay frozen there. → Normalize into a singable
   window (~a 10th) and use register for arc, not a frozen per-hash octave.
3. **Rhythm has no signature.** Durations are locked to {2,4,6,8,12,16}; no
   distinctive recurring rhythmic motive. → A rhythm-+-interval hook (broken
   rhythm `>`, ties, anacrusis, tuplets), reused on every statement.
4. **No climax; boilerplate endings.** Nearly every piece ends on a held tonic;
   no melodic peak. → Place a peak (penultimate phrase) + a small cadential
   melodic formula instead of a held note.
5. **Monotone "melody".** Several scores repeat a single pitch as the theme. →
   Require minimum distinct scale degrees per phrase; cap consecutive repeats.
6. **(Bigger) Arrangement is one fixed template** — and the ABC export even drops
   the bass/comp voices the engine already computes. → Export multi-voice ABC
   (`V:`), then add role-combinatorics, entry/exit schedule, and voicing-density
   ("chord fatness") as new entropy axes (the arrangement teacher answered all
   three open design questions — see its report).

**Process refinements made this round:** (a) added explicit /100↔letter↔GPA bands
to the rubric (the "C+/57" fix); (b) Codex validated as a well-calibrated
substitute teacher; (c) noted the ABC export under-represents the engine (drops
ch1/ch2) — fix for arrangement grading.

**Chosen for round 2 (v0.5, melody-level, highest ROI):** (A) develop
restatements; (B) tessitura normalization; (C) climax + cadential gesture;
(D) rhythmic signature + anti-monotone. Arrangement (multi-voice + combinatorics)
is the larger v0.6 track.

### Round 2 — engine v0.5 (2026-06-23)

Same faculty + Codex. **Grades:** lyricism 77 (C+), memorability 78 (C+),
creative 75 (C), arrangement 73 (C — up from a lead-only baseline), **Codex 63
(D)**. Mean ≈ 73. Improved vs round 1: lyricism 71→77, memorability now
band-consistent at 78, arrangement now has a real 3-voice texture; tessitura,
lyrical breaths, cadence formulas, and voicing density all landed.

**CRITICAL bug — found by Codex, missed by all four Claude graders:
KEY-TRANSPOSITION.** Melody + comp use pitch classes relative to C
(`MAJOR_SCALE`/`MINOR_SCALE`/`CHORDS` are pc-relative-to-0 and never offset by
`key`); only the bass (`36+key`) and the chord *labels* are transposed. So every
non-C piece is **bitonal** (Score 1, labeled E major, has a C-major melody over
an E bass). The Claude graders treated the `K:C` melody as ground truth; Codex's
cross-voice harmonic check caught the clash — the multi-AI panel earned its keep.

**Persistent (v0.5 fixes too subtle):** rhythmic hook still even blocks; climax
not clearly placed/reserved; restatement reads as repeat/transpose, not
development; arrangement templates are labels without mechanism (`call_resp` has
no antiphony; `lead_counter` has no real counter-melody); comp/bass rhythmically
inert; voicings clustered, not voice-led.

**Process refinement:** instruct graders to check cross-voice key/harmony
consistency and to read `K:C` pitches as literal sounding notes (so a wrong-key
melody is caught, not rationalized).

**Chosen for round 3 (v0.6):** (1) **FIX key transposition** [critical];
(2) creative harmony — secondary dominants, real deceptive cadences, expressive
borrowed color + tonal validation; (3) a real recurring rhythmic hook (broken
rhythm / dotted / syncopation); (4) placed + reserved climax; (5) genuine motivic
development on restatement (audible sequence / inversion / fragmentation);
(6) arrangement mechanics — real antiphony (`call_resp`), real counter-melody
(`lead_counter`), comp/bass rhythm, voice-led spacing, entry/exit schedule.

### Round 3 — engine v0.6 (2026-06-23)

**Grades:** lyricism 74 (C), memorability 77 (C+), creative **84 (B, ↑ from 75)**,
arrangement **81 (B−, ↑ from 73)**, **Codex 72 (C−, ↑ from 63)**. Mean ≈ 78.
**Trajectory: 70 → 73 → 78.**

- **Wins:** KEY-TRANSPOSITION **fixed** (Codex confirms all leads in-key). Motivic
  transforms, the tasteful secondary-dominant **color dial**, real antiphony
  (`call_resp` → V:4) and the contrary-motion counter-melody (`lead_counter` →
  V:4) all landed — creative +9, arrangement +8.
- **New bug (Codex, missed by Claude): BASS CHORD-QUALITY.** Bass figuration uses
  hardcoded intervals (+4 major third in "walking", +7 perfect fifth) ignoring
  chord quality, so minor/dim chords get a clashing bass (A under Fm, C# under
  Adim). Fix: derive bass tones from the actual `cpcs`, not fixed intervals.
- **Regression:** the new antiphony **silences the lead** for half of short
  `call_resp`/sentence pieces (`z16 z16`) — reads as the melody dying. Fix: the
  lead carries the call and dovetails with the answer; never rest the principal
  voice for 50% of a 4-bar form.
- **Persistent laggards:** no *placed/reserved* climax; rhythm still even-grid
  (broken rhythm / anacrusis / tuplets — the most-repeated ask across all rounds);
  comp/bass samey; V:4 echoes rather than develops.

**Chosen for round 4 (v0.7):** (1) bass chord-quality fix; (2) lead-silence fix;
(3) deterministic placed climax; (4) a real rhythmic hook (broken rhythm /
anacrusis / tuplets) — the persistent #1 ask; (5) V:4 develops; (6) comp/bass
rhythmic + harmonic-rhythm variety; (7) **rests must reinforce phrasing** (logical
placement at phrase boundaries, not arbitrary); (8) **no abrupt fragments** — a
fragment must trail off *deliberately* (an intentional non-ending), never cut off
mid-thought like a severed sentence. **To discuss (maintainer, 2026-06-23):
reconsider whether non-resolution / incompleteness should remain a feature at all
— `res=half` as a *final* cadence may be the source of the "cut-off" feel; the
lead-silence regression compounds it.** **Possible next: calibrate the rubric
against a canon of ~50 great themes (render to ABC, grade them) and ground the
teachers in melodic-memorability research (in progress: `docs/memorability-research.md`).**

**Research-grounded additions (`docs/memorability-research.md`, 2026-06-23):**
(9) **Dynamics** as an analog layer — ABC *does* support `!p!`/`!mf!`/`!f!` and
crescendo/diminuendo hairpins (`!<(!…!<)!`); add an entropy-driven dynamic arc
(crescendo into the placed climax, settle at the cadence) and *emit* it so graders
see it. Dynamics is both casual-avalanche margin AND an emotion cue. (10) Place the
climax at **~2/3 through the phrase** (Huron's melodic arch), not the midpoint.
(11) Candidate new **MASTER dimension: emotional register** (happy/sad/tense/…)
that conditions mode > tempo > register > dynamics > articulation *coherently*
(Gabrielsson & Lindström cue ranking) — gives downstream coherence; flag
mode/consonance as Western-enculturated. **Notation: ABC still has large unused
vocabulary (dynamics, staccato `.`, grace notes `{}`, slurs, tuplets, broken
rhythm `>`, multi-voice) — exhaust it before augmenting. Introduce an enhanced
convention (ABC + a sidecar "expression track", or `%%MIDI` directives) only at
ABC's real ceiling: continuous/micro dynamics, micro-timing/swing depth, pitch
bends, per-note timbre.**

---

## Canon calibration — grading the greats (2026-06-23)

Full report: **`docs/canon-calibration.md`**. Per-grader records:
`experiments/teaching/grade-{lyricism,memorability,creative,codex}-canon.{md,txt}`.
Bundle: `scores-canon.md` (37 anchors + 5 controls). Tiers: `canon/tiers.md`.

**Maintainer reframed the canon mid-build (important):** the original `docs/canon.md`
was selected on *song-fame consensus*; entmotif needs **melodic memorability as
UNSUNG instrumental music**. Re-stratified into ANCHORs (instrumental: classical,
film/TV, riffs, jazz heads, folk/hymn, logos) vs. 5 CONTROLs (famous-as-sung
songs) + cohort/thin picks cut (Mario, Zelda, Tetris, FF, Seven Nation Army, and
thin-sung extras). Transcription confidence used as a corroborating diagnostic.

**Result — the rubric is well-calibrated; no rule changes.** Panel: 3 Claude lenses
(lyricism, memorability, creative-technique) + Codex (gpt-5.5) generalist.
- **Clean A−/B+ decision boundary:** by **argmax across lenses**, every ANCHOR ≥ A−
  (90); every CONTROL ≤ B+ (87). Zero overlap. Codex: anchors avg 94 (A), controls
  avg 81 (B−).
- **Ground-truth confirmed:** Pink Panther A, Take Five A, all classical A. No
  appeal triggered; **no "(c) rubric-is-wrong"** tag from any grader. Every sub-A
  anchor grade was (a) genuine narrow-lens weakness with another lens carrying it
  (Jaws: D lyricism / A memorability — correct).
- **One doc nuance (not a rule change):** the creative-technique lens correctly
  gives *simplicity-executed-perfectly* (Ode to Joy, Amazing Grace) a B/B+ — it
  rewards transformation; their A lives on lyricism+memorability. Relabel their
  ground-truth expectation accordingly.

**Convergent engine priors (all four graders agree) → sharpen the round-4 list:**
(1) compact germinal cell, then TRANSFORM (sequence / intervallic expansion /
fragment) — never verbatim repeat; (2) one signature interval leap vs. stepwise
context (the fingerprint); (3) one placed/reserved climax (final third); (4)
distinctive NON-uniform rhythm (dotted/broken `>`, triplets, syncopation, odd
meter, anacrusis, held cadence) — the biggest gap; (5) call-and-response of two
contrasting ideas; (6) chromatic color as a motivic signature; (7) clean cadential
closure; (8) (lyrical class) balanced antecedent/consequent + narrow singable
range. **Anti-patterns to KILL (the controls' failure = the engine's current
defaults):** verbatim repeat changed only at the last note; static arpeggio over a
pedal; rote I–IV–V; walls of even eighths. These empirically ground the standing
round-4 fixes (rhythmic hook, placed climax, development-not-repetition).

---

### Round 4 — engine v0.7 (revision 2026-06-23; grading pending)

First round built under **TDD** (`experiments/engine/test_motif.py`, zero-dep): the
SACRED invariants (determinism — same input → identical notes/meta/MIDI bytes;
avalanche — one-char change → different motif) plus the round-4 fixes were written
as failing assertions first (87 failures on v0.6), then driven to **green** (0
failures). test_motif.py is now the regression net for all future engine work.

Changes (v0.6 → v0.7), grounded in `docs/canon-calibration.md`:
1. **Bass chord-quality fix** [Codex bug] — bass tones derive from the actual chord
   pitch-classes (root/third/fifth of `cpcs`), not hardcoded +4/+7; minor/dim/applied
   chords now get a quality-correct bass. (Test: every bass note ∈ active chord.)
2. **Lead never tacet** — call_resp answer units: the principal voice (V:1) resolves
   the phrase (cadence) instead of resting `z16 z16`; the antiphonal response moves to
   V:4. (Test: lead present in every 2-bar unit.) Fixes the v0.6 "melody dying."
3. **V:4 develops** — the call_resp antiphon is a hook fragment **sequenced up a
   third**, not a verbatim echo.
4. **Final cadence always resolves** — terminal cadence forced authentic (V–I, lands
   on tonic); half/abrupt finals removed. (Test: last melodic note ∈ tonic triad.)
   **Decision on the maintainer's open question:** non-resolving *final* cadences are
   dropped — the canon's clearest shared trait is clean cadential closure; revertible
   if the "incompleteness" aesthetic is wanted back. (mid-form half/deceptive remain.)
5. **Placed climax ~2/3 through** (Huron arch) — register arc peaks at the 2/3 unit.
6. **Dynamics arc** — entropy/arc-driven `!mp!→!mf!→!f!→!mf!` emitted in ABC AND
   driving MIDI velocity (crescendo into climax, settle at cadence). (Test: `!` in ABC.)
7. **Signature rhythm hook** — stronger dotted/syncopated idea-bar cells, reused per
   idea statement.

**Deferred (noted):** true anacrusis/tuplets (needs ABC-export + bar-structure work;
the `(3` tuplet doesn't round-trip through the L:1/16 duration tokenizer yet); the
**emotional-register master dimension** (a larger design change — still "to discuss").

Scores regenerated: `scores-v0.7.md`.

**Grades (round 4, all 5 graders on the canon-calibrated rubric):** lyricism C+ 78,
memorability B− 81, creative-technique C+ 74, arrangement C+ 75, Codex(gpt-5.5) C 75.
**Faculty mean ≈ 77.** Codex report: `grade-codex-v0.7.txt`.

**Comparability caveat:** trajectory 70→73→78→77 looks flat, but rounds are NOT
cleanly comparable across the canon-calibration boundary. This round the graders
apply the *validated* "develop-not-restate / texture-envelope" bar (round 3's
creative B/84 and arrangement B−/81 predate it). So lyricism+memorability genuinely
ROSE (74→78, 77→81) on the floor-clearing fixes, while creative/arrangement are now
held to a stricter, masterpiece-anchored bar that exposes the real ceiling.

**Convergent verdict (all 5 graders):**
- **LANDED:** bass chord-quality (fixed), final tonic resolution (universal — the
  single biggest audible lift), placed climax ~2/3, dynamic arc, lead resolves in
  longer forms. v0.7 "cleared the floor" — nothing is broken or ugly.
- **PARTIAL/FAILED:** the 4-bar `call_resp` lead still has a full-bar `z16` (scores
  1, 12) — present per-unit (test passed) but reads as a hole; my test was too weak
  (per-unit, not per-bar). V:4 "develops" only in 1 case (score 2); elsewhere it
  echoes verbatim (scores 6, 8, 10). The dotted hook became a *tic*, not development.
- **CEILING (unanimous v0.8 headline):** the engine **restates a cell + swaps the
  cadence note**; it never *operates on* the germinal cell. This caps the whole
  batch at C/C+ regardless of the surface fixes.

**Chosen for round 5 (v0.8), ranked by impact:**
1. **Real motivic-transformation pass** [THE change] — derive every restatement by an
   explicit operation: sequence (±2/±3 steps), inversion about the head, augmentation/
   diminution, fragmentation. FORBID "verbatim + cadence-swap" as the only return.
2. **V:4 develops in ALL templates** (not just call_resp) — kill byte-identical echoes
   (scores 6/8/10); apply the transform pass to the answer/counter too.
3. **Fix the short-form lead `z16`** — in ≤8-bar call_resp the lead carries a tag/tie
   *through* the antiphony bar; never tacet a full bar. (Tighten the test to per-bar.)
4. **Onset-based rhythm** — anacrusis/pickups, true broken rhythm `>`/`<`, ties across
   beats; stop deriving rhythm from a duration inventory on the grid.
5. **Unify the climax** — registral peak + harmonic arrival + rhythmic activity + `!f!`
   must coincide, with a prepared approach and a release (not `!f!` at a fixed index).
6. **Texture envelope (entry/exit schedule)** + comp/bass **voice-leading** (minimal
   motion, goal-directed bass) — the arrangement ceiling.

**Notation affordances still untapped** (all graders): tuplets `(3`, grace notes `{}`,
slurs `( )`, ties `-`, articulations/ornaments, crescendo *hairpins* (vs terraced
dynamics), per-voice instrument programs, real `K:`/mode spelling, volta/repeat.

---

## Refactor — engine graduated to `src/entmotif/` (2026-06-24)

Behavior-preserving execution of `docs/refactor-plan.md` steps 2–16 (step 1, the
golden tests, was already done). The v0.7 single-file prototype
`experiments/engine/motif.py` is now a thin compatibility shim re-exporting a clean
package `src/entmotif/`: **model** (NoteEvent/Phrase/Palette/PitchRange/Development/
Motif + VoiceRole; timing constants) · **entropy** (fingerprint + Chooser; frozen
label rule) · **theory** (pure scales/chords/snap/step/degree/sym/chord_name) ·
**form** (Phrase sequence, cadence, development) · **melody** (rhythm vocab,
gravity, line→`generate_melodic_line`, cadence, dynamics) · **arrangement**
(Palette, voicing, comp/bass) · **engine** (`generate`/`compose`) · **exporters/**
(abc, midi) · **cli**.

- **Both SACRED rules honored:** every `Chooser` label literal is byte-unchanged
  (frozen wire format); every step ran under green `test_motif.py` + `test_golden.py`.
  Output is byte-identical end to end — golden NOT re-baselined, `make_scores.py
  v0.7` byte-identical, teaching harness intact.
- **Committed in small traceable steps** (8 commits on `refactor/engine-to-src` off
  a `main` baseline snapshot); steps 10–16 not collapsed.
- **Deliberate scope calls (documented in code):** (a) Mode is NOT an enum — it is
  `%s`-formatted into ABC and str-Enum `str()` is version-dependent (`"Mode.MAJOR"`),
  a determinism hazard. (b) `generate_melodic_line` keeps its 18-arg signature
  (MelodyContext bundling deferred — Phase 2 rewrites the rhythm model). (c)
  DecisionKey-constant centralization of labels deferred (labels left as unchanged
  literals).
- **Step 17 — cross-platform determinism repair — DONE (maintainer-approved 2026-06-24).**
  Eliminated every float hazard so MIDI is byte-identical on every platform/libm
  (AGENTS.md §1), mirroring entviz's discipline of making all reproducible decisions
  with pure integer arithmetic (entviz reserves float only for SVG geometry, where a
  0.01px tolerance absorbs rounding — MIDI has no such tolerance, so integer-only):
  (a) `Chooser.weighted()` now uses an integer threshold (`v(label) % total`) +
  integer cumulative comparison — no float accumulation, no `WEIGHT_SCALE` division;
  (b) `gravity_delta()` reads a **frozen, versioned integer Gaussian table**
  (`GAUSS`, `GRAVITY_TABLE_VERSION=1`) instead of `math.exp()`; (c) the register-arc
  `center`, `peak`, `span` are integer arithmetic; (d) tempo uses `//`. Output
  changed for all 12 corpus inputs (small per-input ABC diffs) → **golden
  re-baselined** intentionally (still v0.7 *musical behavior*, just deterministic).
  `scores-v0.7.md` is left as the historical round-4 grading record (not regenerated).

---

### Round 5 — engine v0.8 (built 2026-06-24; grading PENDING maintainer listen)

Built on the clean `src/entmotif/` package under TDD (new failing assertions in
`test_motif.py` first, then driven green; golden re-baselined intentionally since
output changes; `scores-v0.8.md` regenerated). Addresses the unanimous round-4
v0.8 list:

1. **Real motivic transformation [THE change].** The germinal cell is stated once,
   then its realized **shape** (scale-step interval deltas + rhythm) is extracted
   (`melody.motif_shape`) and **every restatement is an explicit operation** on it
   (`melody.render_transform`): sequence (±2/±3 scale steps), inversion about the
   head, augmentation/diminution, fragmentation, or (rarely) identity — chosen by
   the fingerprint (`choose_transform`, label `xform%d`). "Verbatim + cadence-swap"
   is forbidden as the only return type. Verified: across the corpus every 2-bar
   lead unit is now a *distinct* realized shape (was near-identical in v0.7).
   **Bit class:** the transform family is a DISCRETE, untrained-ear-recoverable
   decision ("it rose / mirrored / sped up / shrank to a fragment") — ~2–3 reliable
   bits across a multi-restatement period (declared per AGENTS.md §0).
2. **V:4 develops in ALL templates.** The `call_resp` antiphon is now a germ
   transform (label `ans%d`, never identity); the `lead_counter` counter is an
   explicit **inversion** of the germ (contrary motion, lower register) — no more
   byte-identical echoes. (Test: V:4 has ≥2 distinct pitches and ≠ the lead line.)
3. **Short-form `call_resp` z16 fixed.** The lead now holds a **tag** (a chord-tone
   pedal) through the antiphony bar, then cadences — never tacet for a full bar.
   The test is tightened to **per-bar** lead presence (was per-unit).
4. **Onset rhythm — partial.** Broken rhythm is pervasive (dotted/syncopated germ
   cells propagate through every transform); **ties** across the barline are now
   notated (`exporters/abc._split_at_bars`, ABC `-`), which also lets augmentation
   sustain correctly. **Deferred to v0.9:** true anacrusis/pickups (hard in the
   fixed bar-grid — needs a pre-bar-1 region) and the cosmetic `>`/`<` glyphs
   (numeric durations already encode the broken rhythm audibly + visibly).
5. **Unified climax.** At the placed peak (~2/3, Huron) the lead transform runs with
   `climax=True`: registral peak (start at the top of the window) + rhythmic
   activity (halved durations) + harmonic arrival (strong-beat chord snap) + the
   single `!f!`, with a prepared crescendo (mp→mf→f) and a release (→mf/mp).
   (Test: exactly one `!f!`, at the peak unit, with lead activity there.) *Known
   gap:* when the peak lands on an `aaba` **contrast** unit the activity-boost isn't
   applied (contrast uses the separate `line()` path) — register+dynamics still
   coincide; full coincidence on contrast units is a v0.9 item.
6. **Texture envelope + voice-leading.** Entry/exit schedule: lead states the germ
   **unaccompanied** first (solo_bed/lead_counter), comp **enters** after the intro,
   groove builds bass-first, and the texture **thins** (comp drops) at the final
   cadence of longer forms. (Test: comp present in some units, absent in others.)
   **Voice-leading deferred to v0.9:** comp still re-voices per bar and the bass is
   not yet goal-directed across units — the spread-voicing + chord-tone bass from
   v0.7 carry over; minimal-motion voicing + approach-tone bass are the next step.

Determinism + avalanche green; both suites green on the v0.8 golden baseline.

**Round-5 verdict = the maintainer's listening review (2026-06-24)** — taken as
ground truth in lieu of the faculty panel for this round (the ear is the ground
truth; the panel exists to approximate it, and the maintainer reviewed all 12).
Per-input: 01 recognizable but quiet/boring, *harmony comes and goes weirdly*;
02 answer too unlike the call (rhythm+octave variation broke recognizability),
melody feels similar to 01; 03 slightly better, rhythm varied but feels *random,
not synergistic* (cf. Beethoven 5: short=tension, long=land); 04 harmony off &
too quiet under the melody; 05 flute welcome, but comp enters *discordant/ugly*;
06 meh, rhythm unrelated to phrases; **07 best — simple**; 08 solid melody, harmony
"random accordion puffing," adds nothing; **09 strongest**, harmony wasted; 10
strong melody, harmony "dumb"; 11 sounds unresolved + boring monophonic flute; 12
too long for its development (strong first half). General: instruments boring (no
percussion/horns/world), only 2 voices, narrow bass/harmony range; tempo range too
small (want up to ~200–220); why never harmony on the *same* instrument as the lead? **(follow-up)** no legato,
no fat chords, no stylistic variation — "almost pure 2-instrument classical
arrangements, one carrying melody and the other a *faint suggestion* of harmony."

**Selection is genuinely SHA-512-driven (not text-driven) — verified, NOT a bug.**
The maintainer suspected we might be selecting from the lowercase-ASCII input text;
proof: one-char-apart inputs scatter across the palette, and lead choice is ~uniform
over 2000 inputs (≈400/415/404/376/401 across the 5 leads). The monotony is the
**tiny palette**, not the entropy path: 5 orchestral leads, comp *always* program 48
(strings), bass *always* 32. AGENTS.md §0 (style/genre as the broad master
dimension — sitar/oud/drums/horns/world) is essentially unimplemented.

**Technical diagnosis grounding the harmony complaints (from the corpus):**
- comp velocity is **flat per piece and far below the melody** (comp 34–42 vs lead
  78–110) → "too quiet," no dynamic shaping. (engine/arrangement.)
- **Clustered voicings** when fat=2/3 (added 7th/9th land a 2nd apart): #12 18/72,
  #1 9/36, #9 3/12 stacked intervals <3 semitones → "muddy/ugly accordion." The
  spread-voicing rule doesn't constrain the added extensions.
- **No voice-leading**: comp re-voices from scratch each bar (leaps); bass not
  goal-directed. (Deferred in v0.8 — now the top audible defect.)
- **Texture envelope reads as "harmony comes and goes"** (#1): dropping comp at the
  intro/final cadence is heard as the harmony flickering, not as phrasing.
- tempos cluster mid-range (only 5 distinct across the corpus, max 160 < the 184
  ceiling); ceiling itself too low.

**Round-6 (v0.9) fix list — ranked by audible impact:**
1. **HARMONY OVERHAUL (top priority).** Real voice-leading (comp picks the inversion
   nearest the previous voicing — minimal motion; goal-directed bass approaching the
   next root); kill clustered extensions (drop/space the added 7th/9th, or voice them
   open); raise + shape comp velocity to sit *with* the melody (not 30 below); make
   the comp actually decorate/reinforce/counterpoint the line. Tame the texture
   envelope so harmony doesn't flicker (smoother entrances, sustain through phrases).
2. **PALETTE / STYLE BREADTH (AGENTS.md §0 master dimension).** Expand far beyond 5
   orchestral leads: add percussion/drum-kit grooves, horns, and world timbres
   (sitar/oud, marimba/koto, etc.); vary the **comp + bass programs** (incl. an
   option to comp on the *same* instrument as the lead); pick a **genre/style family**
   from the fingerprint that conditions palette + groove + harmonic language
   coherently. (Bit-budget: style family is a discrete master-dimension carrier.)
3. **Tempo range** up to ~200–220 with flatter weighting (don't cluster mid-range).
4. **Rhythm–phrase synergy** (not random): tie rhythmic density to tension/release —
   shorter values build into the climax, longer values land cadences (Beethoven-5
   logic). A teacher/lens should analyze rhythm for synergy vs. randomness.
5. **Call/answer recognizability** (#02): the consequent must stay clearly related to
   the antecedent — constrain the transform (avoid octave displacement + heavy rhythm
   change at once) so the answer still "rhymes" with the call.
6. **Cross-input melodic variety + register** (#01≈#02): ensure different inputs yield
   audibly different *melodic characters*, not just different notes in the same mold.
   Melodic range feels stuck ~**C4–C6 for every input/instrument** — the per-lead
   register windows barely differentiate (all leads sit mid); widen and *vary* the
   tessitura per instrument/style (flute high, bass-clef timbres low, etc.) and use
   register as a stronger discriminator across inputs.
7. **Form length vs development** (#12): cap or earn length — don't emit 16 bars
   without enough transformation to justify it.
8. **Resolution** (#11 sounds unresolved): revisit — possibly the bare monophonic
   ending; "incompleteness as a feature" still open for debate.

**Grading-lens gap surfaced by the maintainer's "which teacher studies harmony?":**
harmony/counterpoint/voice-leading currently lives mostly under **arrangement**
(texture/voicing) + **creative-technique** (harmonic language/color), with **Codex**
as the de-facto cross-voice harmony auditor (it caught the v0.5 key-transposition and
v0.6 bass-quality bugs). No lens does *deep* voice-leading/counterpoint or
rhythm–phrase-synergy analysis — sharpen the arrangement lens (or add a dedicated
harmony+counterpoint lens and a rhythm-synergy lens) for round-6 grading.

---

### Round 6 — engine v0.9 (built 2026-06-24; grading PENDING maintainer listen)

Built on the round-5 verdict, under TDD (golden re-baselined intentionally;
`scores-v0.9.md` regenerated). The headline is **STYLE as the master dimension**
(this.i:z0m4p81q) plus the harmony overhaul the maintainer demanded.

**North-star context (this.i:h0v4k7m2, recorded this session):** the maintainer
set the long-range goal — *consume every SHA-512 bit via musically-valid decisions;
a rich, broad spread, no simplifications.* v0.9 is a large step toward it, not the
finish; the engine is still far from full-hash consumption.

**Landed:**
1. **Style master dimension — 14 real 4/4 idioms** (`arrangement.STYLES`): classical,
   baroque, ragtime, boogie-woogie, swing, blues, bossa nova, samba, salsa, tango,
   reggae, funk, gospel, march. Each is a genuine idiom with its own **groove**
   (idiomatic comp + bass + percussion patterns — stride, walking, boogie ostinato,
   bossa, montuno, skank, funk-16ths, habanera, oom-pah…), instrumentation, tempo
   band, register, harmonic-color bias, mode bias, and articulation. The fingerprint
   picks the style (`"style"` decision), which conditions everything downstream for
   internal cohesion. All 14 verified reachable + ~uniform over 4000 inputs. *(Fixes
   the v0.8 "boring 2-instrument classical / monochrome palette" — confirmed the
   selection was always SHA-512-driven; the palette was the problem.)*
2. **Percussion is the whole family, not a kit** (`VoiceRole.PERCUSSION`, ch 9):
   per-style grooves draw on congas/bongos/timbales/agogo/claves/cowbell/guiro/
   shaker/cabasa/tamb/woodblock/triangle/cuica/surdo as well as kit pieces (e.g.
   salsa uses 7 distinct percussion instruments).
3. **Harmony overhaul:** open, **cluster-free** voicings (every stacked tone ≥3
   semitones apart; capped at 4 voices so it stays clear, not 2 octaves wide); comp
   velocity now tracks the unit dynamic and **sits with the melody** (≈12 below, was
   ≈30 below — the "faint accordion" complaint); octave **voice-leading** (comp picks
   the inversion nearest the previous voicing); **goal-directed walking bass** (last
   beat aims at the next root); legato sustain for legato styles.
4. **Wider tempo (to 208) + per-style register** — melodies no longer stuck ~C4–C6;
   tessitura varies by style.
5. **Call/answer recognizability:** the consequent is restricted to recognizable ops
   (identity/small-sequence/fragment — no inversion or octave displacement), fixing
   the v0.8 "answer too unlike the call" (#02).

**Deferred (tracked for v0.10+, toward the north star):** sitar raga / Gregorian
chant / waltz (need a **meter dimension** + **drone/modal harmony** — not faked);
deeper rhythm–phrase synergy (Beethoven-5 tension/release shaping); ABC percussion
notation (audio has it; ABC shows it only in the header `perc=`); analog-layer stack
(this.i:e9k2m4p1) and texture-interruption (this.i:f3a0k9m2); and the long tail of
unconsumed fingerprint bits.

Determinism + avalanche green; both suites green on the v0.9 golden baseline.
`scores-v0.9.md` regenerated; corpus audio rendered to
`~/winhome/Downloads/entmotif-v0.9-listen/`. **Grades pending the maintainer's listen.**

### Round 6.5 — engine v0.10 (built 2026-06-24; from the maintainer's v0.9 listen)

The v0.9 listen produced a dense round of feedback (all addressed; two deep items
recorded as intent for v0.11+). Fixes:
- **Broad LEAD palette via the two-layer capability model** (this.i:c2k9p0a4): the
  lead is now drawn from a wide pool (`LEAD_POOL`, ~50 timbres incl. guitar/banjo/
  oboe/french-horn/harp/koto/shamisen/kalimba/pan-flute/vibes/contrabass-family) by a
  CAPABILITY gate (register reach + per-style minimum **agility**) and an AFFINITY
  weight (signature ~80% common; "weird-but-valid" ~20% rare — a koto over swing, a
  clarinet/banjo/synth ragtime over the piano stride bed; church-organ ragtime is
  correctly excluded by agility). Fixes "weird instruments common" + "not hearing
  guitar/banjo/oboe/koto…". (Confirmed selection always SHA-512-driven.)
- **Lead ≠ comp timbre** (fixes v0.9 reggae "organ comping organ huffing"); keyboard-
  bed styles (ragtime/boogie) intentionally keep the piano bed.
- **Percussion audible** (perc velocity 30-60 → 62-104, sits in the mix) and **bass
  cuts through** (bass velocity → ~80-112) — fixes "no percussion / can't hear bass /
  2-instrument feel".
- **Lower, less-shrill register** (window dropped from tonic+19 to tonic+12; per-style
  reg centers lowered) — fixes "shrill / all C4-C6 / too high".
- **Cadence variety** (this round): the final cadence is entropy-chosen authentic
  (common) / half-open / deceptive — no longer always a full close (maintainer
  request). Test relaxed: only authentic finals must land on the tonic.
- **Ragtime livelier** (tempos 104-140); blues comp moved on-grid (fixes #9 off-grid
  "stutter").

**Recorded as intent for the big v0.11+ tracks (north star [[h0v4k7m2]]):**
- **Texture model beyond lead+comp** (this.i:p6m2v9k0): the homophonic melody+
  accompaniment+bass frame is itself a simplification — a string quartet/fugue/chorale/
  heterophony don't fit it. Needs a TEXTURE dimension + a generalized N-voice model.
- **Emotional register master dimension** (this.i:a7k0m3p9): output is "emotionally
  flat" because mode/tempo/register/dynamics/articulation are chosen independently;
  add EMOTION as a master that coherently aligns those cues (sad/tense/mischievous/…).

Determinism + avalanche green; both suites green on the v0.10 golden baseline;
`scores-v0.10.md` + `~/winhome/Downloads/entmotif-v0.10-listen/` rendered.

---

## Flywheel cycle fw1 — Backlog A2: comp/bass RHYTHM-pattern variety (2026-06-24)

**Backlog item A2** (v12 #08; `this.i:r4d8m1k6`), under strict TDD. The comp/bass
grooves previously read as one fixed strong/weak cell per style; this extends the
existing two-layer "signature common, alternates rare" model (`c2k9p0a4`, used for the
rhythm section's INSTRUMENT in fw1's A1) to its RHYTHM. WHY: maintainer/backlog
complaint that grooves were a simple strong/weak alternation — this consumes more of
the hash with musically-valid, idiomatic choices while conserving the bar's duration
(`this.i:m9p3k7a2`).

**Change:**
- `src/entmotif/arrangement.py` — added `COMP_PAT_VARIANTS`/`BASS_PAT_VARIANTS` family
  tables + `comp_pat_choices()`/`bass_pat_choices()`. Each style's signature
  comp_pat/bass_pat now heads a small family of idiomatic, metric-conserving variants
  (walking↔walking_skip, stride↔stride_octave, shuffle↔shuffle_jab, comp4↔charleston,
  skank↔skank_double, montuno↔montuno_synco, bossa↔bossa_partido, boogie↔boogie_shuffle,
  continuo↔continuo_synco, oompah↔oompah_push, funk16↔funk16_synco, root5↔root5_arp,
  reggae↔reggae_drop, tumbao↔tumbao_anticipate, habanera↔habanera_dotted). Added the
  matching render branches in `comp_groove()`/`bass_groove()`, each filling exactly one
  4/4 bar on the 16th grid. `palette_for()` now accepts comp_pat/bass_pat overrides.
  Signature affinity ~70% (`PAT_SIG_W=5` vs `PAT_VAR_W=2`); variants reachable-but-rare.
  Capability gate untouched (keys off the base pattern; variants share its attack demands).
- `src/entmotif/engine.py` — draws comp_pat/bass_pat per input via two NEW Chooser
  labels (`"comp_pat"`/`"bass_pat"`) and exposes them in meta. Because the Chooser is
  label-keyed (hashes fp+label independently), existing draws (lead, harmony, form,
  tempo, …) are byte-unperturbed; only the comp/bass rhythm changes.

**TDD:** added a FAILING assertion block to `experiments/engine/test_motif.py` first
(verified `AttributeError` on the missing `COMP_PAT_VARIANTS`), then the minimal change.
The test checks every variant is on-grid, fills the bar, has a downbeat note, the
signature is in its own family, several families have ≥2 variants, and the rendered
comp/bass rhythm actually varies across ≥4 styles over 1500 probe inputs.

**Validation:** `test_motif.py` = 0 failures (determinism + avalanche green);
`test_golden.py` green after `--update`. 3 corpus inputs drew a variant (#4 swing
walking_skip, #6 ragtime stride_octave, #10 blues shuffle_jab) — eyeballed: drift
confined to comp/bass voices (chan 1/2), lead unchanged. Decision recorded in `this.i`
(node `r4d8m1k6`); item marked DONE in `docs/flywheel.md`; `scores-fw1.md` regenerated.

**Panel grades (/100):** lyricism 80 · memorability 74 · creative-technique 68 ·
arrangement 73 · Codex(gpt-5.5) 73. (Lead-side lenses unaffected as expected; the
change targets the rhythm-section groove, which the arrangement/Codex lenses cover.)

**Convergent findings (merged across graders):**
- The melody/lead still **restates a cell and orbits the tonic** rather than going on a
  real ARCH-contour journey with development on return — the persistent ceiling
  (creative-technique lowest at 68). This is the highest-leverage open item.
- **Harmony/comp is still mechanical** relative to the line: it does not yet decorate,
  reinforce, or counterpoint the melody — the rhythm-variety win is audible but the
  comp's *pitch* relationship to the lead is the next gap.
- **Emotional flatness**: mode/tempo/register/dynamics/articulation are still chosen
  independently, so motifs don't cohere around a feeling.
- The **march oom-pah comp** remains the most pointed timbral defect (the brass "pah"
  reads as a collection of horns).

**Chosen next-fix list (ranked):**
1. **March comp fix** (Backlog A3, v12 #03) — lighten/lower the "pah" (lighter reed or
   tuba+percussion); the only remaining well-specified, low-taste-risk A-item.
2. **Melodic development + MEMORABILITY** (Backlog B4, tick `~77d7`/`~3yhb`) — apply
   the earworm checklist: real ARCH contour, a reused multi-pitch HOOK, repetition-
   WITH-development, short singable phrases, medium-LOW surprisal. PRIORITY per the
   maintainer; taste-heavy, so be conservative and expect a re-listen.
3. **Emotional register master dimension** (Backlog B5, `this.i:a7k0m3p9`) — pick an
   emotion, then align mode>tempo>dynamics>register>articulation>dissonance coherently.

---

## Flywheel cycle fw2 — Backlog A3: March comp fix (lighten the oom-pah "pah") (2026-06-24)

**Backlog item A3** (v12 #03), under strict TDD. Picked the top unblocked Group A
item: the march comp fix. Group A items 1 and 2 (comp/bass instrument variety +
capability gate, and rhythm-pattern variety) were already DONE in fw1, and the
brass-exclusion half of the march fix was already in place. The remaining,
well-specified, low-taste-risk defect was the heavy "collection of horns" oom-pah:
the comp "pah" on beats 2 and 4 sounded the FULL chord voicing, doubling its lowest
voice down into the tuba's "oom" register and muddying the texture.

**Change (strict TDD):**
- First added a FAILING assertion in `experiments/engine/test_motif.py` asserting the
  oom-pah "pah" must drop the bass-register bottom voice and sound strictly fewer
  voices than the full voicing (verified it failed: 4 failures — "still doubles the
  bottom voice 60" / "4 of 4 voices").
- Then the minimal change in `src/entmotif/arrangement.py` `comp_groove()`: the
  `oompah` and `oompah_push` patterns now use `voic[1:]` (drop the lowest voice) for
  the "pah", so the band answers ABOVE the bass rather than on it — a thinner, crisper
  backbeat chord. `stride` (also ragtime's keyboard bed) and tango's marcato were
  deliberately left unchanged to avoid collateral drift.

**WHY:** directly addresses the maintainer's most pointed timbral complaint while
conserving the metric grid (`this.i:m9p3k7a2` — same onsets/durations) and the frozen
Chooser labels.

**Validation:** `test_motif.py` = 0 failures (determinism + avalanche stay green).
Output changed intentionally for exactly one corpus input (golden score #3, the
march); ran `test_golden.py --update`, eyeballed the diff (the "pah" now sounds 3
voices starting at pitch 58, above the tuba oom, instead of 4 voices reaching down to
58's octave), and confirmed both golden ABC and MIDI now green (0 failures).
Regenerated `scores-fw2.md` (12 scores). Committed with sign-off as `4ee5a38`.

**Panel grades (/100):** lyricism 74 · memorability 75 · creative-technique 72 ·
arrangement 78 · Codex(gpt-5.5) 72.

**Convergent findings (merged across graders):**
- The melody/lead still **restates a cell and orbits the tonic** rather than going on a
  real ARCH-contour journey with development on return — the persistent ceiling
  (creative-technique among the lowest). Highest-leverage open item.
- **Harmony/comp is still mechanical** relative to the line: it does not yet decorate,
  reinforce, or counterpoint the melody — the comp's *pitch* relationship to the lead is
  the next gap (the rhythm/voicing wins are audible, but the comp answers rather than
  converses).
- **Emotional flatness**: mode/tempo/register/dynamics/articulation are still chosen
  independently, so motifs don't cohere around a feeling.
- The march oom-pah "pah" lightening is **audibly landed** (arrangement highest at 78);
  the timbral defect that drove this cycle is closed.

**Chosen next-fix list (ranked):**
1. **Melodic development + MEMORABILITY** (Backlog B4, tick `~77d7`/`~3yhb`) — apply the
   earworm checklist: real ARCH contour, a reused multi-pitch HOOK, repetition-WITH-
   development, short singable phrases, medium-LOW surprisal. PRIORITY per the maintainer;
   taste-heavy, so be conservative and expect a re-listen.
2. **Harmony↔melody relationship** — make the comp decorate/reinforce/counterpoint the
   line's *pitches*, not just supply idiomatic rhythm under it.
3. **Emotional register master dimension** (Backlog B5, `this.i:a7k0m3p9`) — pick an
   emotion, then align mode>tempo>dynamics>register>articulation>dissonance coherently.

---

## Flywheel cycle fw3 — Group B #4: kill dead whole-bar lead holds (memorability) (2026-06-24)

**Group B #4 (melodic development + MEMORABILITY)**, under strict TDD. Group A items
1–3 were already DONE (fw1: comp/bass instrument variety + capability gate, rhythm-
pattern variety; fw2: march oom-pah lightening), so this cycle took the maintainer-
priority Group B #4 via the most well-specified convergent panel finding: **"static
held-note bars (`=E16` / `=B16` / `^F16`) read as filler, not hook."** Root cause: the
call/response **"tag" bar** in `engine.py` emitted ONE pitch sustained for the whole
bar while V:4 answered — the sole source of all 8 whole-bar single-pitch lead bars in
the corpus (the 3 `call_resp` inputs).

**Change (strict TDD):**
- First added a FAILING assertion to `experiments/engine/test_motif.py` forbidding the
  lead from dead-holding a whole bar anywhere except the placed climax (failed on all
  relevant bars: 7 reported, climax bar excluded).
- Then the minimal fix: a new `melody.tag_call` helper
  (`src/entmotif/melody.py`) builds a singable CALL gesture instead of a dead sustain —
  chord tone, upper scale neighbour, settle back (1+1+2 beats, metric-conserving per
  `this.i:m9p3k7a2`, consonant chord tones at the seams). Wired into the `cr_answer`
  branch of `engine.generate` (`src/entmotif/engine.py`), removing the now-unused
  `cpcs` import there.

**Result:** e.g. score 3 bars that were `^F16` / `^d16` / `^G16` are now `^F4 ^G4 ^F8`
/ `^d4 =f4 ^d8` / `^G4 ^A4 ^G8` — the line keeps moving. `test_motif.py` = 0 failures
(determinism, avalanche, metric conservation, climax, all prior invariants green);
`test_golden.py` rebaselined (`--update`) for scores 2/3/5 (exactly the `call_resp`
inputs) and re-run green. Scores regenerated to `scores-fw3.md`. Committed with
sign-off; sha `800d4db`.

**Panel grades (/100):** lyricism 76 · memorability 79 · creative-technique 73 ·
arrangement 81 · Codex(gpt-5.5) 72.

**Convergent findings (merged across graders):**
- The melody/lead still **restates a cell and orbits the tonic** rather than going on a
  real ARCH-contour journey with development on return — the persistent ceiling
  (creative-technique lowest at 73). Killing the dead holds helped memorability (→79),
  but the deeper "develop on return, don't just restate" gap remains the top item.
- **Harmony/comp is still mechanical** relative to the line: it does not yet decorate,
  reinforce, or counterpoint the melody — the comp's *pitch* relationship to the lead is
  the next gap (rhythm/voicing wins are audible, but the comp answers rather than converses).
- **Emotional flatness**: mode/tempo/register/dynamics/articulation are still chosen
  independently, so motifs don't cohere around a feeling.
- The dead whole-bar lead holds that drove this cycle are **closed** — the tag bar now
  sings a CALL gesture; the "filler, not hook" defect is gone (arrangement highest at 81).

**Chosen next-fix list (ranked):**
1. **Melodic development on return** (Group B #4, deeper half) — the line still restates
   a cell and orbits the tonic; apply the earworm checklist's real ARCH contour +
   repetition-WITH-development so restatements *transform*, not just recur. Highest leverage.
2. **Harmony↔melody relationship** — make the comp decorate/reinforce/counterpoint the
   line's *pitches*, not just supply idiomatic rhythm under it.
3. **Emotional register master dimension** (Backlog B5, `this.i:a7k0m3p9`) — pick an
   emotion, then align mode>tempo>dynamics>register>articulation>dissonance coherently.
