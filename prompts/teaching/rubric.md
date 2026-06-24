# entmotif Teaching Rubric (NORMALIZED — keep stable)

The faculty grades the engine's compositions from ABC lead-sheets. This rubric is
the shared, **absolute** yardstick: apply it identically every round so grades
are comparable over time. Grade each score on its **intrinsic** musical quality —
NOT relative to earlier rounds and NOT on a curve against the other scores in the
batch.

## Grade scale (per criterion) — with GPA and a fixed anchor

| Letter | GPA | /100 band | Anchor (absolute meaning) |
|---|---|---|---|
| A  | 4.0 | 93–100 | At the level of a real, memorable theme a listener would hum. Nothing to add. |
| A− | 3.7 | 90–92 | Excellent; one small refinement from a real theme. |
| B+ | 3.3 | 87–89 | Strong and clearly musical; a few clear improvements remain. |
| B  | 3.0 | 83–86 | Competent and clearly musical, but unremarkable / easily forgotten. |
| B− | 2.7 | 80–82 | Solid; clearly past competent-but-forgettable in places. |
| C+ | 2.3 | 77–79 | A notch above bland; flashes of real interest. |
| C  | 2.0 | 73–76 | Musically valid but bland, generic, or mechanical. |
| C− | 1.7 | 70–72 | Valid but weak — notable dullness or small flaws. |
| D+ | 1.3 | 67–69 | Notably flawed (aimless/awkward) with a redeeming feature. |
| D  | 1.0 | 60–66 | Notably flawed in this dimension. |
| F  | 0.0 | 0–59 | Fails this dimension (not a melody; ugly; structureless). |

**The letter, /100, and GPA MUST agree per this table.** Decide the **/100 first**,
then read the letter and GPA from its band — never report a letter and a number
from different rows. (Normalization fix added after round 1, where a teacher
reported "C+ / 57".)

## You are grading a GENERATOR, not a song

The scores are samples from a generative engine driven by a hash of each input.
Your feedback must target the **engine's rules** — patterns *across the batch*
("every melody peaks on the downbeat of bar 5"; "answers never vary the rhythm";
"contour is always an arch") — not one-off edits to a single score. Generic,
single-piece notes are nearly useless here.

Always include **"creativity left on the table"**: specific techniques and **ABC
affordances** the engine does not yet use but should — grace notes (`{}`), slurs,
broken rhythm (`>` `<`), tuplets (`(3`), ornaments/decorations (`!trill!`, `.`
staccato), tied notes, multiple voices (`V:`), dynamics. The affordances of the
notation are a checklist of options we may be ignoring.

## Memorability features to assess (earworm research — inject every round)

Ground your grades AND findings in the convergent research on what makes melodies
memorable/earwormy (full synthesis + ~30 sources: `docs/memorability-research.md`
Part B). These are **features to REWARD when present and serving the music, and to
FLAG as missing across the batch** — they are NOT rules to demand on every single
score (do not penalize a musical piece merely for not arching):

- **Familiar ARCH contour**, peak ~2/3 through, mostly small/stepwise intervals,
  carrying a FEW pointed surprises (a signature leap) — not a flat orbit, not chaos.
- **A distinctive recurring HOOK** (rhythm + interval) spanning several pitches, reused.
- **Repetition WITH development** at motif/phrase/section scales (transform on return —
  sequence/inversion/fragment; never verbatim copy, never aimless variation).
- **Small intervals as default + gap-fill** (a leap is answered by a step back).
- **Medium-but-LOW surprisal** — interesting yet predictable enough to stick (for
  *memorability* specifically, lean toward the lower end of "interesting").
- **Short, singable phrases** (~7–12 notes, ~a 10th range).
- **Clear, steady meter**; a groove/timbre identity that can land before the melody.

Caveat: contour / interval-size / phrase-length / meter are broadly human, but
**mode→mood and consonance→pleasure are Western-listener-conditioned** — weight them
as such. When you flag a missing feature, say which engine rule should add it.

## Required output from every teacher

1. **Grades table:** `score# | letter | /100 | one-line reason`.
2. **Aggregate:** your overall letter + GPA + /100 for the batch, on your lens.
3. **Top 3–5 ENGINE changes**, ranked by impact, each concrete enough to implement.
4. **Untapped affordances / techniques.**

Be a demanding master teacher: a `B` is the default for "competent but
forgettable." Reserve `A` for work that genuinely rivals a real theme.
