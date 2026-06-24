# entmotif — session handoff / project orientation (2026-06-24)

A fresh session can continue from here. **Everything important is on disk** — this
file points to it; the artifacts are the source of truth (this is a date-stamped
snapshot and may go stale, so trust the files it names over this summary).

## What entmotif is

Turns a high-entropy value (key/hash/UUID/address) into a short, **recognizable**
musical motif (MIDI), so a human can recognize it by ear. Audible sibling of
**entviz** (`../entviz/`). Read `AGENTS.md` first (authoritative rules: TDD,
intent layer, tick, defects), then `this.i` (the "why" — ~19 opaque-ID decision
nodes; IDs are deliberately meaningless, semantics live in node names).

## The design, on disk

- **`this.i`** — intent/decisions: Model B (recognition-from-memory) `[m4z81p3v]`;
  discrete/analog bit law `[k20f9a3x]`; bit budget 25–50 `[2p8z1m40]`; hash-first
  `[81pz4m0v]`; whole-motif integrity `[9k3f0a72]`; style as master dimension +
  two-layer style/lead `[z0m4p81q]`,`[c2k9p0a4]`; render-fidelity / pinned
  soundfont `[3k7a92f0]`,`[8a3k0f29]`; conditioned-probability priors `[7c4m1k0p]`;
  the 2026-06-23 adversarial review + evidence grounding `[6b2k9p0a]`; etc.
- **`docs/bit-budget.md`** — the bit-consumption schedule, independence-audited,
  with a "verified evidence" section. Honest landing: ~19–28 reliable bits for an
  8-bar period, conditioned on (exposure, time, device, culture).
- **`docs/references.md`** — annotated bibliography (verification-tagged) for the
  bit-budget evidence.
- **`docs/memorability-research.md`** — the melodic-memorability + emotion research
  (6 strands, ~30 sources, `[canonical]`/`[verify]` tags). Distilled "features of
  memorable melodies" + an emotion→features master-dimension table.
- **`docs/canon.md`** — the canon: 50 curated great themes (C01–C50) + 60 long-tail
  (T01–T60), with sources, verification tags, and notation-visibility flags.
- **`docs/engine-log.md`** — the teaching-loop report card: round-by-round grades,
  the driving changes, and the **round-4 (v0.7) fix list + research-grounded
  design notes**. READ THIS for current status.
- **`docs/entmotif-paper-plan.md`** — approved paper plan; drafting deferred.

## The engine

**The engine has graduated into a clean package: `src/entmotif/`** (v0.7 behavior,
zero-dependency). Modules: `model` (NoteEvent/Phrase/Palette/PitchRange/Development/
Motif/VoiceRole + constants) · `entropy` (fingerprint + Chooser) · `theory` (pure
pitch/chord ops) · `form` · `melody` · `arrangement` · `engine` (`generate`/
`compose`) · `exporters/{abc,midi}` · `cli`. **`experiments/engine/motif.py` is now
a thin compatibility shim** re-exporting the package, so `import motif` (the test
suites + `experiments/teaching/make_scores.py`) keeps working unchanged. New code
should import from `entmotif` directly. Refactor details: `docs/engine-log.md`
"Refactor — engine graduated" entry; the ordered plan was `docs/refactor-plan.md`
steps 2–16 (done; **step 17, the determinism repair, is intentionally NOT done** —
approval-gated, changes output).

Turns value → SHA-512 → choices → 8-bar (or longer) period → MIDI + multi-voice
ABC. **Invariants that must never break:** determinism (same input → byte-identical
MIDI) and avalanche (one-char change → different motif). Now ENFORCED by tests:
`experiments/engine/test_motif.py` (invariants + behavior) and `test_golden.py`
(exact ABC+MIDI snapshot of the corpus; run `--update` only to intentionally
re-baseline). Run both after any engine edit. Note `~4eu7` (tick): the prototype
hashes raw input; the real impl must normalize + strip prefix/suffix exactly as
entviz (`this.i:81pz4m0v`).

## The teaching loop (how grading works)

Process doc: `prompts/teaching/orchestrating-teaching.md`. One round:
1. `python3 experiments/teaching/make_scores.py <version>` → `scores-<version>.md`
   (ABC lead-sheets of the **frozen corpus** `experiments/teaching/corpus.txt`).
2. Grade with the faculty (`prompts/teaching/{lyricism,memorability,creative-technique,
   arrangement}.md` as Claude subagents) **+ a Codex substitute teacher**
   (`cat rubric.md scores.md | codex exec "<grading prompt>"`). Apply the
   normalized banded rubric `prompts/teaching/rubric.md`.
3. Synthesize (you = dean): faculty mean, convergent findings, record in
   `docs/engine-log.md`.
4. Fix **all** feedback, then run the next round (maintainer's standing rule).

**Trajectory so far:** round 1 (v0.4) ≈70 → round 2 (v0.5) ≈73 → round 3 (v0.6)
≈78 (faculty mean /100). The **multi-AI panel earns its keep**: Codex (gpt-5.5,
via `codex exec`) twice caught correctness bugs all four Claude graders missed
(key-transposition in v0.5; bass chord-quality in v0.6 — the latter is on the
round-4 list).

## Status as of 2026-06-24 (done since the 06-23 snapshot)

- **Canon built, transcribed, stratified, graded** — `experiments/teaching/canon/abc/`
  (51 phrases), re-stratified by the maintainer's "memorable as UNSUNG instrumental
  music" axis into `canon/tiers.md` (37 anchors + 5 controls). Calibration verdict:
  **rubric is well-calibrated** (`docs/canon-calibration.md`) — clean A−/B+ boundary,
  anchors all ≥A−, controls ≤B+; no rubric changes needed. The convergent "what
  winners share" became engine priors.
- **Engine v0.7 shipped + graded** (round 4) — `docs/engine-log.md`: faculty mean
  ≈77; lyricism/memorability rose, creative/arrangement held to the stricter
  canon-validated bar. Built under TDD (test_motif.py red→green).
- **Architecture review done** — `docs/refactor-plan.md` (consolidated from Codex +
  a Claude architect; full reviews in `reviews/`). Golden safety net committed
  (`test_golden.py`).

## Done 2026-06-24 (this session)

- **Refactor COMPLETE** (`refactor/engine-to-src`) — engine graduated
  `experiments/engine/motif.py` → `src/entmotif/` package, behavior-preserving
  through step 16. **Step 17 (cross-platform determinism repair) DONE** too
  (maintainer-approved): integer-only decision math (integer `weighted()`, frozen
  `GAUSS` table replacing `math.exp`, integer register arc) — golden re-baselined.
- **v0.8 engine BUILT** (`feat/engine-v0.8`, branched off the refactor) — all six
  round-4 v0.8 items (real motivic transformation, V:4 develops everywhere, z16 fix,
  ties/broken rhythm, unified climax, texture envelope); see `engine-log.md` round-5
  build entry for what's full vs. deferred-to-v0.9. Golden re-baselined; both suites
  green; `scores-v0.8.md` regenerated.
- **Round-5 verdict recorded = the maintainer's listening review** (formal faculty
  panel skipped — the ear is ground truth). Full per-input notes, the proof that
  selection is genuinely SHA-512-driven (not text-driven), the harmony/voicing/
  velocity/register technical diagnosis, and the ranked **v0.9 fix list** are in
  `docs/engine-log.md` round-5 entry. Headline v0.9: **harmony overhaul**
  (voice-leading, fat/open voicings, comp velocity, legato, tame texture flicker) +
  **palette/style breadth** (AGENTS.md §0 — percussion/horns/world, varied comp/bass
  programs, a genre master-dimension) + wider tempo/register + rhythm–phrase synergy.
- **Branches not yet merged to main** — `main` holds only the baseline snapshot;
  `refactor/engine-to-src` then `feat/engine-v0.8` stack the work (small signed-off
  commits, steps not collapsed). Merge order: refactor → v0.8 (no squash).

## Immediate next steps (pick one)

1. **Round 5 (v0.8)** — the unanimous round-4 headline: **real MOTIVIC TRANSFORMATION**
   (the engine still restates a cell + swaps the cadence note; it never *operates* on
   the germinal cell — sequence/inversion/augmentation/fragmentation). Plus: V:4
   develops in ALL templates; fix the short-form `call_resp` lead `z16`; onset-based
   rhythm (anacrusis/ties/broken `>`); unify the climax; texture envelope. Full list
   in engine-log round-4 entry. (Do under test_motif.py + test_golden.py — re-baseline
   golden intentionally since output will change.)
2. **Execute the refactor** (`docs/refactor-plan.md`) — best as its own focused
   session. Steps 1–9 are pure behavior-preserving cleanup (green-gated by
   test_golden.py); the two SACRED rules: never change `Chooser` label literals;
   refactor only under green golden tests.
3. **⚠ Approval-gated:** Codex flagged a real **cross-platform determinism risk** —
   `Chooser.weighted()` float accumulation + `gravity_delta()` `math.exp()` can round
   differently across platforms, violating AGENTS.md §1's "byte-identical on every
   platform." Fixing it (integer/fixed-point) CHANGES all output → needs a golden
   re-baseline + maintainer sign-off. Refactor-plan step 17.

## Open design questions for the maintainer (Daniel)

- **Reconsider "incompleteness as a feature"** — abrupt fragments / non-resolving
  (`res=half`) finals feel like errors ("speech cut off"); maybe drop non-resolving
  *final* cadences. Rests must reinforce phrasing (commas between phrases only).
- **Emotional register as a new MASTER dimension** (happy/sad/tense/…) conditioning
  mode>tempo>register>dynamics>articulation coherently (Gabrielsson & Lindström);
  mode/consonance are Western-enculturated. (engine-log item 11.)
- **Enhanced notation** only when ABC's ceiling is hit (continuous/micro dynamics,
  micro-timing/swing, pitch bends, per-note timbre) — ABC + a sidecar expression
  track; exhaust ABC's existing vocabulary first.

## Working disciplines (from `~/.claude/CLAUDE.md` + this project)

- Determinism + avalanche are sacred; verify after every engine change.
- Store findings on disk with verification tags; never cite `[verify]`/secondary as
  confirmed (esp. in the paper).
- Fix all of a round's feedback before the next round (unless items conflict).
- Subagent limits: ≤2 general-purpose / ≤3–4 read-only Explore concurrently;
  prefix heavy shell with `nice -n 19 ionice -c 3`.
- A second AI (`codex exec`, also `gemini -p`) gives genuine perspective variety —
  use it as a substitute grader/cross-check.
- Pinned soundfont: GeneralUser GS in `experiments/soundfont/sf/`; render via
  FluidSynth (`fluidsynth -ni -F out.wav -r 44100 <sf2> <mid>`).
- Audio can't be heard by agents — the maintainer listens at checkpoints; grading
  from notation is a fast proxy, the ear is ground truth.
