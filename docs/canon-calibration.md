# Canon calibration — grading the greats (2026-06-23)

Dean synthesis of the canon grading pass. Purpose (per `prompts/teaching/canon-grading.md`):
**calibrate the rubric** by grading real masterpieces — does the rubric award A's
to genuine greats (anchors), do famous-as-sung songs grade lower (controls), and
**what do the winners share** (→ engine priors)?

Panel: 3 Claude faculty lenses (lyricism, memorability, creative-technique) + a
**Codex (gpt-5.5)** generalist substitute. Bundle: `experiments/teaching/scores-canon.md`
(37 anchors + 5 controls, each a real theme reduced to its bare identifiable phrase).
Per-grader records: `grade-{lyricism,memorability,creative,codex}-canon.{md,txt}`.

## Verdict: the rubric is well-calibrated — no changes needed

- **Clean decision boundary.** By **argmax across lenses**, every ANCHOR reaches
  **≥ A− (90)**; every CONTROL tops out at **≤ B+ (87)**. The A−/B+ line separates
  the two groups with zero overlap.
- **Maintainer ground-truth confirmed.** Pink Panther **A**, Take Five **A**, and
  the entire classical set **A**. No ground-truth A landed sub-A on its signature
  lens → no rubric-remediation appeal triggered.
- **No (c) attributions.** Across ~60 sub-A lens-grades, not one grader judged the
  rubric/lens to be rewarding the wrong thing. Every sub-A anchor grade was **(a)
  genuine weakness on a narrow lens**, with another lens carrying the piece (e.g.
  Jaws: D on lyricism, A on memorability — correct). The argmax rule holds.
- **Controls behave.** Codex: anchors avg **94 (A)**, controls avg **81 (B−)**, a
  13-point gap; the melody lenses put the controls at C/B−. The weakest control,
  Bad Romance (16 hammered identical A's), is correctly the floor (C / C+).

### Consolidated grades (letter per lens; argmax = the calibration metric)

| id | theme | tier | Lyr | Mem | Cre | Codex | **argmax** |
|---|---|---|---|---|---|---|---|
| C01 | Beethoven 5 | anchor | C+ | A | A | A | **A** |
| C02 | Ode to Joy | anchor | A | A | B | A | **A** |
| C03 | Eine kleine | anchor | A− | A | A | A | **A** |
| C04 | William Tell | anchor | C | A | B+ | A | **A** |
| C05 | Mountain King | anchor | B | A | A− | A | **A** |
| C06 | Ride of Valkyries | anchor | B | A− | B+ | A | **A** |
| C46 | La Marseillaise | anchor | B+ | A− | A− | A | **A** |
| T01 | Zarathustra | anchor | C− | A | C+ | A | **A** |
| T02 | Toccata & Fugue | anchor | C | A− | B+ | A | **A** |
| C07 | Star Wars | anchor | B | A | B+ | A | **A** |
| C08 | Jaws | anchor(narrow) | D | A | B | A | **A** |
| C09 | James Bond | anchor | C | A | A− | A | **A** |
| C10 | Good/Bad/Ugly | anchor | B | A | B+ | A | **A** |
| C11 | Pink Panther ★ | anchor | B+ | A | A | A | **A** |
| C12 | Mission: Impossible | anchor | C | A | A− | A | **A** |
| T04 | Godfather | anchor | A | A− | B+ | A | **A** |
| T05 | E.T. | anchor | A− | A | A− | A | **A** |
| T07 | Raiders March | anchor | B+ | A | A− | A | **A** |
| C17 | Smoke on the Water | anchor(narrow) | C | A | B | A | **A** |
| C18 | Satisfaction | anchor(narrow) | C | A | C+ | A | **A** |
| C19 | Whole Lotta Love | anchor | C− | A− | B | B+ | **A−** |
| C27 | Superstition | anchor | C | A− | B+ | A− | **A−** |
| C29 | Take Five ★ | anchor | A− | A | A | A | **A** |
| C30 | So What | anchor | C | B+ | A− | A | **A** |
| C31 | Take the "A" Train | anchor | B | A− | B+ | A− | **A−** |
| C32 | 'Round Midnight | anchor | B+ | B+ | A | A− | **A** |
| C33 | Autumn Leaves | anchor | A− | B+ | A | A− | **A** |
| T29 | Linus and Lucy | anchor | C+ | A | A− | A | **A** |
| C37 | Happy Birthday | anchor | B+ | A | B | A− | **A** |
| C38 | Greensleeves | anchor | A | A | A− | A | **A** |
| C39 | Amazing Grace | anchor | A | A | B+ | A | **A** |
| C40 | Auld Lang Syne | anchor | A− | A− | B+ | A | **A** |
| C49 | Sakura Sakura | anchor | B | A− | B+ | A− | **A−** |
| C50 | Intel bong | anchor(narrow) | C− | A | C+ | A | **A** |
| T56 | NBC chimes | anchor(narrow) | D+ | A− | C | A | **A** |
| C47 | Girl from Ipanema | borderline | A− | B+ | A− | A− | **A−** |
| C41 | Over the Rainbow | borderline | A | A− | A− | A | **A** |
| C22 | Bad Romance | CONTROL | D+ | C+ | C | C | **C+** |
| C23 | Can't Get You Out | CONTROL | C | B | C | B− | **B** |
| C48 | Lion Sleeps Tonight | CONTROL | C+ | B+ | C+ | B | **B+** |
| C26 | I Heard It / Grapevine | CONTROL | C | B | C+ | B− | **B** |
| C21 | Don't Stop Believin' | CONTROL | C | B+ | C+ | B− | **B+** |

Anchor argmax floor = **A− (C19 Whole Lotta Love, C27, C31, C49, C47)**. Control
ceiling = **B+ (C48, C21)** — both have a genuine bare-melody contour (the hardest
controls), yet neither reaches A−. The split is clean.

## The payoff — convergent engine priors (what the winners share)

All four graders independently converged on the same melodic recipe. These become
the engine's target priors:

1. **A compact germinal cell (2–4 notes), then TRANSFORM it — never verbatim
   repeat.** Transposed sequence (Beethoven 5 down a step, Mountain King up a
   third), **intervallic expansion** (E.T.: rising 5th reopened as an octave),
   fragmentation. *Exact looping is the controls' failure mode.*
2. **One signature INTERVAL leap against stepwise context** — the fingerprint:
   octave launch (Over the Rainbow, Happy Birthday line 3), P5/P4 fanfare (Star
   Wars, Zarathustra), semitone oscillation (Jaws), blues 3rd. Identifiable within
   3–5 events.
3. **One placed/RESERVED climax**, typically in the consequent / final third,
   reached once by leap (Huron's arch). Earlier peaks get exceeded later.
4. **Distinctive NON-UNIFORM rhythm** (the most "left on the table"): dotted/broken
   `>`, triplets `(3`, syncopation, **odd meter** (5/4 — Take Five, M:I),
   acceleration (Jaws), pickups/anacrusis, held cadence notes. The rhythm itself
   is often the hook.
5. **Call-and-response of two CONTRASTING ideas** — active call vs. sustained/
   lyrical answer (Eine kleine, Bond, So What, the GBU call+answer).
6. **Chromatic color as a motivic signature** (Pink Panther, Bond, Mountain King's
   snap-back) — branded, not noodled.
7. **Clean cadential closure** on a stable degree / held note / return to the
   opening pitch. Open-ended noodling kills recall.
8. **(Lyrical class) balanced antecedent/consequent period + narrow singable range
   (~a 10th).** Phrases in answering pairs, not isolated cells.

**Anti-patterns to KILL (the controls' shared failure, = the engine's current
defaults per the round logs):** verbatim repetition with change only at the last
note; static arpeggio/oscillation over a pedal; rote diatonic I–IV–V; walls of
uniform even eighths.

## Action items

1. **Rubric: no change.** Validated. Keep it stable (per the normalization rule).
2. **Doc nuance (not a rubric change):** in `canon-grading.md`, Ode to Joy (C02)
   and Amazing Grace (C39) were listed "expect A across lyricism/memorability/
   **creative**." The creative-technique lens correctly gives *simplicity executed
   perfectly* a B/B+ (it specifically rewards transformation, of which these have
   little). Their A lives on lyricism+memorability. Relabel their ground-truth
   expectation to those two lenses; the "simplicity = A" rubric note applies to
   lyricism/memorability, not to the development lens. (Recorded; argmax already
   handles it — both are A overall.)
3. **Round 4 engine priors:** items 1–8 above sharpen and *empirically ground* the
   standing round-4 list in `engine-log.md` (rhythmic hook, placed climax, motivic
   development-not-repetition). The canon now gives concrete targets, and the
   controls give concrete anti-patterns to test against.
