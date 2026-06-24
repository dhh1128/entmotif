# Canon calibration grading (wrapper around the faculty lenses)

This is NOT the usual "grade the generator" pass. The score bundle
(`experiments/teaching/scores-canon.md`) is a set of **real, famous themes**, each
reduced to its identifiable phrase, stratified into ANCHORs (great as *unsung
instrumental music*) and a few CONTROLs (famous-as-*sung*-song, expected thin as
bare melody). Purpose: **calibrate the rubric** before we trust it on engine output.

A grader gets: `prompts/teaching/rubric.md` + one lens
(`lyricism.md` | `memorability.md` | `creative-technique.md`) + this wrapper +
`scores-canon.md`. Apply the rubric's **absolute** scale to each piece on your lens.

## What to produce (replaces the lens's "engine feedback" framing)

1. **Grades table:** `id | letter | /100 | one-line reason`, on your lens.
2. **Calibration check:** Do the ANCHORs land where a masterpiece should
   (mostly A / A− / B+ on your lens)? **List any anchor that does NOT** — and say
   whether it reads as (a) a genuine weakness of that theme *as a bare unsung
   melody* on your lens, (b) a rubric gap (the scale fails to reward something
   real), or (c) likely a thin/wrong transcription (cross-check its `% confidence:`).
3. **Control behavior:** Do the CONTROLs grade *lower* than the anchors, as
   expected? Flag any control that grades high — that means the rubric/lens is
   rewarding the wrong thing for entmotif's instrumental purpose.
4. **What the winners SHARE (the payoff):** across the high-grading anchors on your
   lens, name the concrete, recurring melodic features — these become the engine's
   target priors. Be specific (interval signatures, contour shapes, rhythmic
   devices, phrase structure, climax placement, cadence formulas).

## Discipline
- Grade each piece on its **intrinsic** quality as a bare instrumental phrase, on
  an **absolute** scale (not on a curve against the batch).
- Recognition is cohort-conditioned; grade the *melodic craft on the page*, not
  whether you personally have heard it.
- A masterpiece's bare incipit can still be simple — simplicity executed perfectly
  is an A, not a C. Reserve low grades for genuine thinness on your lens.

## The canon is the validation set; the RUBRIC is what's under test

Your ear-anchored job here is calibration. **A masterpiece need not be an A on
EVERY lens — but it must be an A on the lens that makes it great** (Jaws is an A on
memorability and a deserved D on lyricism; that low lyricism grade is correct).
So the headline metric is **argmax across lenses, not mean**. A masterpiece that is
mediocre on *all* lenses is the real alarm.

### Forced attribution on every sub-A anchor grade
For ANY anchor you grade below A− on your lens, append a tag explaining WHO is wrong:
- **(a) genuine weakness on my narrow lens** — and name which OTHER lens you expect
  carries this piece. (Legitimate; no rubric action.)
- **(b) thin/wrong transcription** — cross-check the file's `% confidence:` tag.
- **(c) the rubric/lens is wrong here** — and you MUST name the specific rubric line
  or lens rule producing the low grade (this is how we find the bug).

### Maintainer ground-truth A's (hard check)
These are pre-labeled by the maintainer's ear as A-level masterpieces. If any lands
**sub-A on its strongest lens**, flag it LOUDLY at the top of your report with the
attribution tag — it triggers a rubric-remediation appeal (the rubric changes, not
the canon):
- **Melodically rich (expect A across lyricism / memorability / creative):**
  C11 Pink Panther · C29 Take Five · C01 Beethoven 5 · C02 Ode to Joy ·
  C03 Eine kleine · C05 Mountain King · C46 Marseillaise · C38 Greensleeves ·
  C39 Amazing Grace · T04 Godfather · T05 E.T. · T07 Raiders · T29 Linus & Lucy.
- **Narrow (expect A on its signature lens only):** C08 Jaws · C50 Intel ·
  T56 NBC · C17 Smoke on the Water · C18 Satisfaction (memorability/distinctiveness).

Report, per anchor: your grade, and if sub-A, the attribution tag + (for ground-truth
items) the named rubric rule at fault.
