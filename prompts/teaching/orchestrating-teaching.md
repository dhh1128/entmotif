# The Teaching Loop — orchestrating composition review for the entmotif engine

The engine is a composition *student*; a faculty of master composers grades its
work and drives successive improvements. Unlike the design-review panel in
`prompts/review/` (which critiques the *design*), this loop critiques the engine's
actual *compositions* and runs iteratively until the grades approach an A.

## The cycle

1. **Generate** — freeze the corpus (`experiments/teaching/corpus.txt`) and emit
   ABC lead-sheets for the current engine: `python3 experiments/teaching/make_scores.py <version>`.
2. **Grade** — each faculty persona (this folder) reads `rubric.md` + the score
   bundle and returns grades + **engine-level** feedback. Run them as Claude
   subagents; **also run at least one as a different model** (Codex / Gemini) for
   genuine variety — a "substitute teacher" (see below).
3. **Synthesize (dean)** — combine grades into a faculty GPA, resolve conflicts
   (lyricism vs. complexity), and pick the **single highest-impact engine change**
   plus a short ranked list. Record everything in `docs/engine-log.md`.
4. **Revise** — apply the change to the engine.
5. **Re-grade** — repeat. Stop when the faculty GPA plateaus near A, or returns
   diminishing gains.

## Normalization (so rounds are comparable)

- **Fixed corpus** + **fixed rubric** (absolute anchored scale), unchanged between
  rounds. If either changes, note it in the log — grades before/after aren't
  comparable.
- Teachers grade on the rubric's **absolute** scale, not relative to prior rounds.
- Every grade carries a **/100 and a GPA** so the dean can compute and trend a
  faculty GPA per round.

## Substitute teacher (a different AI)

For independent perspective, run one grader via **Codex**:
`codex exec "<rubric + score bundle + grading instructions>"` (non-interactive,
read-only sandbox). Treat its output as one more faculty member; the dean folds it
in. `gemini`/`ollama` are alternatives. Rotate which lens the substitute covers.

## Ground truth vs. fast proxy

Grading from notation is an **LLM estimate** of musicality, not hearing. The text
loop runs fast and often; the **maintainer listens at checkpoints** to keep the
faculty calibrated. If the ear disagrees with the grades, fix the rubric/faculty —
the ear is ground truth.

## Gates each round (automated)

Before grading a new engine version, confirm it still: runs/parses; is
**deterministic** (same input → identical MIDI); shows **avalanche** (one-char
change → different motif). A change that breaks these is rejected regardless of grades.

## History

`docs/engine-log.md` is the report card: per round, the faculty GPA, per-lens
grades, the change that was made, and the feedback that drove it. This is the saved
record of successive improvements and their causes.
