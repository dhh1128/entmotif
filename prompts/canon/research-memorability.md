# Prompt — Research the science of melodic memorability (fan-out Explore agents)

*Run from a session that can spawn agents. Self-contained.*

## Context & goal

**entmotif** grades a motif-generating engine against a rubric
(`prompts/teaching/`). We want that rubric — and the engine's probabilistic priors
— grounded in the **actual research** on what makes melodies memorable,
recognizable, and earwormy, rather than on general taste. Produce a **permanent,
citable on-disk reference**, not just session knowledge.

Repo root: `/home/daniel/code/entmotif`. Read `docs/references.md` first — match
its *annotated-bibliography + verification-status* style exactly.

## Method — fan out read-only research agents

Spawn **Explore / research agents**, but respect this machine's limits: **at most
3–4 read-only Explore agents concurrently**, and prefix any heavy shell work with
`nice -n 19 ionice -c 3`. Give each agent ONE sub-topic; have it find **primary,
reputable** sources (peer-reviewed papers, books by domain experts — not blogs that
merely republish), extract **specific, actionable features** (with numbers where
the source gives them), and return citations (author, year, venue, URL) with a
**verification note** (did the agent actually read the abstract/source, or is it
second-hand?).

Suggested sub-topics (one per agent; add others if found):
1. **Earworms / INMI features** — what melodic features predict involuntary musical
   imagery (e.g. Jakubowski, Finkel, Stewart & Müllensiefen; Williamson; Beaman &
   Williams): tempo, global contour shape, interval patterns, repetition.
2. **Recognition memory for melodies** — durability, contour vs. interval over
   time, exposure effects (Dowling; Dowling, Kwak & Andrews; Schellenberg &
   Habashi; Halpern; Bartlett & Dowling). *(Some are already in `references.md` —
   extend, don't duplicate.)*
3. **Repetition & catchiness** — Margulis (*On Repeat*); the "Hooked on Music"
   project and Müllensiefen's FANTASTIC feature set; pop-hook catchiness studies.
4. **Expectation & "good melody" theory** — Huron (*Sweet Anticipation*); Narmour's
   Implication-Realization model; Meyer (*Emotion and Meaning in Music*).
5. **Computational / corpus studies** of memorable vs. forgettable melodies, and
   **cross-cultural statistical universals** of melody (e.g. Savage et al.).

## Synthesis

After the agents return, one pass (an agent or the orchestrator) consolidates the
findings into **"Features of memorable melodies (research-grounded)"** — a ranked,
concrete list, each item mapped to: (a) which **rubric criterion** it sharpens, and
(b) which **engine prior/dimension** it should inform. Distinguish well-established
findings from tentative ones; note where evidence is thin or culture/exposure-bound.

## Output — write to disk

Write `docs/memorability-research.md`:
- **Annotated bibliography** — per source: full citation, URL, *what it found* (the
  specific features/numbers), *how it bears on entmotif* (rubric/engine), and a
  **verification status** (`verified <date>` vs `secondary — cite with care`).
  Same format and discipline as `docs/references.md`.
- **Synthesis** section — the ranked, actionable "features of memorable melodies",
  mapped to rubric + engine.

## Discipline

- Primary, reputable sources only; record URLs; mark anything unverified.
- **Never invent** a study, finding, statistic, or quote. If a sub-topic yields no
  solid evidence, say so — a documented gap is a valid result.
- The file is the deliverable; it must be self-contained and citable later.
