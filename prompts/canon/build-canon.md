# Handoff prompt — Build the entmotif "canon" of great, earworm-defensible themes

*Paste this into a fresh session. It is self-contained.*

## Context

**entmotif** turns high-entropy values (keys, hashes, addresses) into short,
recognizable musical motifs. We grade a motif-generating engine with a faculty of
"teacher" personas against a rubric (`prompts/teaching/`). To **calibrate** that
rubric against real greatness, we need a **canon**: a cross-genre list of themes
that are *hard to argue with* as memorable earworms. We will later transcribe each
theme's identifiable phrase to ABC notation and grade them with our faculty, to
see what "greatness" looks like on our rubric and to ground the engine's targets.

Repo root: `/home/daniel/code/entmotif`. Read `prompts/canon/README.md` and
`prompts/teaching/rubric.md` for context before starting.

## Goal

A list of **~50 themes** (start with a rock-solid core of ~25 and grow) spanning
*every* major musical tradition, where each entry is **defensible by cross-source
consensus** — it recurs across multiple independent, reputable "greatest / most
recognizable / most memorable" rankings. Consensus is the whole point: a theme
that appears on many independent lists is hard to dispute.

## Method

1. **Gather many independent, reputable rankings**, several per genre, e.g.:
   - Classical themes/melodies; Film & TV themes; Video-game themes; Rock; Pop;
     Soul/R&B; Jazz standards; Country; Folk; Musical-theatre/Broadway; World &
     national anthems/folk tunes; even famous advertising jingles.
   - Prefer critics' lists, large public polls, broadcaster/industry rankings, and
     any *academic recognition/earworm* studies (these are gold — a theme named in
     an earworm study is maximally defensible).
   - Use **multiple, independent** sources per genre — never lean on one list.
2. **Select by consensus.** Favor themes that recur across many independent
   sources. Record, for each, *which sources* support it (with URLs) so the choice
   is defensible and citable.
3. **Bias toward MELODICALLY-carried themes.** entmotif is instrumental and can
   only "sing" open vowels, so favor themes recognizable *by their tune alone*
   (instrumental themes, strong melodic hooks). You may include lyric-/production-
   famous songs, but **flag** those whose fame is not in the melody — their
   greatness may not survive notation.
4. **Ensure each has a clear, transcribable ~4–16-bar identifiable phrase** (the
   hook/incipit) — the part a person hums. Note what that phrase is.
5. **Cover breadth + the undisputed.** Make sure every major genre is represented
   *and* the universal earworms (Beethoven's 5th, the *Jaws*/*Bond*/*Star Wars*
   motifs, "Happy Birthday", a Joplin rag, etc.) are present.

## Output — write to disk (do not just report in chat)

Write `docs/canon.md`, one structured entry per theme:

```
## C01 — <Title> — <composer/artist>, <year>, <genre>
- Phrase: <the recognizable ~4–16-bar hook, described>
- Why it qualifies: <consensus — name the independent sources + URLs>
- Notation-visible greatness?: yes | partly | mostly-not (why — melody vs
  timbre/lyric/production/performance)
- Transcribe: yes/defer
```

End with a **## Sources** section listing every ranking/source used, with URLs, so
the canon is auditable. Aim for genre balance; mark the confident core vs. the
"grow-later" tail.

## Discipline

- Cite real, reputable sources; record URLs. Do **not** fabricate rankings,
  attributions, dates, or "appears on N lists" claims you didn't check.
- When unsure of a fact (composer, year, whether a list really includes it), say
  so rather than guessing.

## Phase 2 (note for later, not this session unless asked)

Accurate **ABC transcription** of each kept theme's identifiable phrase is a
separate, careful step → `experiments/teaching/canon/abc/<id>.abc`. Transcribe the
*melody* (and a chord sketch if obvious), then **verify it against the known tune**
— a wrong transcription poisons its grade. Public ABC tune databases (e.g.
abcnotation.com) may help where accuracy and licensing permit; otherwise transcribe
from score/by ear and double-check. Keep each transcription's source noted.
