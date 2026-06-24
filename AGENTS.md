# AI Behavioral Rules & Orientation

All AI agents (including Gemini, Claude, and GitHub Copilot) working on the `entmotif` project MUST adhere to these rules. These rules are designed to ensure that code is a byproduct of comprehension, not a replacement for it.

## 0. What entmotif is (and isn't)

Entmotif turns a high-entropy value (a key, signature, UUID, blockchain address, hash, etc.) into a **short, hummable musical motif** so a human can **recognize** it by ear. The motif may inhabit *any* musical style — the breadth is the whole point, and is itself a primary carrier of entropy (see the bit-budget law). Exemplars must span far beyond Western classical: Beethoven's 5th and Grieg's A-minor concerto, yes, but equally Joplin's *The Entertainer* (ragtime), Gershwin's *Rhapsody in Blue* (jazz), Morricone's spaghetti-western themes and *Gabriel's Oboe* (film), Vangelis's *Chariots of Fire* (electronic), a Gilberto **samba**/bossa, **sitar** or **oud** riffs, Chinese/Japanese/African instrument palettes, Michael Jackson or Queen (pop/rock), Gregorian chant (sacred), Bobby McFerrin (vocal/a cappella). Do **not** lean on any single composer or genre (e.g. don't fill the list with John Williams themes), and do **not** default to producing only classical-sounding motifs — **style/genre is a first-class, deliberately broad design dimension.** It is the audible sibling of [entviz](https://dhh1128.github.io/entviz), which renders the same kind of value as a picture. Read the entviz materials (`../entviz/docs/spec.md`, `../entviz/this.i`, `../entviz/README.md`) for the disciplines this project inherits — much of the input-handling and intent-tracking craft transfers directly.

Entmotif deliberately differs from entviz in four ways. Internalize these before designing anything:

1. **Recognition, not lossless comparison.** The job is to let an ordinary adult — no perfect pitch, no perfect recall — decide "have I heard this one before?" / "does this sound like the one I was expecting?". We are NOT trying to let someone losslessly reconstruct or bit-compare the input by ear. (entviz's losslessness, read-aloud fidelity, and side-by-side comparison machinery do **not** apply here.)
2. **Lossy by design ⇒ relaxed cryptographic rigor.** Because we never claim to carry every bit audibly, we don't need entviz's conformance tiers, golden rasters, or collision-grade guarantees. We still use a cryptographic hash as the entropy source (for avalanche and arbitrary-length inputs — see §3), but the bar is "two different inputs reliably sound different to a human," not "an attacker cannot manufacture a near-collision."
3. **Musicality is the higher bar.** Entropy must NEVER be mapped to arbitrary tones directly. That produces noise, not a motif. Instead, **music theory defines the space of acceptable outputs, and entropy chooses among the valid options.** Every note, chord, and rhythm we emit must be defensible as a deliberate musical choice. The aesthetic target is *hummable and pleasant*, not *maximally distinct*.
4. **A modest, reliable bit budget.** The goal is to carry **~25–50 bits** of entropy *reliably* — i.e., recoverable by recognition, not by transcription. Spend the budget on **discrete, untrained-ear-recoverable** musical decisions (see the bit-budget law below), and let everything else be analog flavor that aids recognition without claiming bits.

### The bit-budget law (the most important design principle)

Inherited from entviz's `this.i:d1scr3t3` and re-cast for sound: **reliable bits come only from discrete musical decisions an untrained ear can re-identify; analog musical variables give recognition and pleasantness but not countable bits.**

- **Discrete / bit-bearing** (spend the budget here): major vs. minor; does the melody rise, fall, or arch; meter (3 vs. 4 vs. 6/8 feel); roughly fast vs. slow; which instrument/timbre family carries the lead; the broad contour/shape of the opening interval (a leap vs. a step); the chord-progression family; how many phrases / call-and-answer structure.
- **Analog / recognition-only** (do NOT count these toward the budget; use them to make it hummable and to add casual avalanche): exact pitches, exact tempo in BPM, micro-rhythm, dynamics, precise voicing. These are read with perceptual tolerance, so they can't be relied on for bits — but a single-bit input change SHOULD perturb them too, so any honest difference is *also* audible at a glance (entviz's "casual avalanche").

When you propose any new entropy→music mapping, you MUST state which class each output dimension is in and estimate its reliable bit yield. A design that claims bits from an analog dimension is wrong.

## 1. Core Principles

- **Comprehension is the primary output, not code.** You must genuinely understand the *why* before writing the *how* — and for this project that includes the **music theory**, not just the software.
- **Intent is a first-class artifact.** Every major decision, tradeoff, and goal must be recorded in `this.i` (see §2).
- **The "How" of interaction determines skill.** Use AI for conceptual inquiry and reasoning. Avoid blind code delegation.
- **True TDD.** Never modify code without a failing test, and never leave code in a state where tests do not pass.
- **Determinism.** Identical input MUST yield byte-identical MIDI on every invocation, on every platform — no wall-clock, locale, environment, or random source. (Entropy is the only source of "randomness"; everything downstream is a pure function of it.)

## 2. The Intent Layer (`this.i`)

We maintain a file named `this.i` in the root of the repository, tracking the project's purpose in a structured, hierarchical, YAML-like format (mirroring entviz's `this.i`).

- **Updates:** Every time you make a significant design decision or identify a new constraint/tech debt, update `this.i`.
- **IDs:** Assign every goal/decision/constraint a unique, **opaque** 8-character alphanumeric ID (e.g., `q7f3a920` — deliberately meaningless), and cross-link related ones with `[[id]]`. The ID is opaque on purpose: all semantics live in the node's **name**, which you can then rename freely without breaking any `[[id]]` link. Do **not** encode meaning into the ID — a "meaningful" ID becomes a lie the moment the concept is renamed, and tempts a rename that breaks every cross-reference.
- **Intent Checks:** Before starting any implementation task, perform an "intent check": read `this.i` and `docs/spec.md` to ensure your plan aligns with the established vision and the bit-budget law (§0).

## 3. Entropy → music: the standing design contract

These are project-level invariants, not implementation details. Changing one is a spec decision that MUST be recorded in `this.i`.

- **Hash first, then choose.** Derive a fingerprint (a cryptographic hash, e.g. SHA-512) of the canonical normalized input *text* — reuse entviz's normalization/parsing discipline (presentation vs. identity vs. annotation; hash text, not decoded bytes). Drive every musical choice from the fingerprint bits, NOT from the raw input. This gives avalanche (one-character change ⇒ a clearly different motif) and handles inputs of any length. We can borrow entviz's `entropy` parser as an oracle/spec for normalization.
- **Bits are consumed by a documented schedule.** Lay out, in the spec, exactly which fingerprint bits feed which musical decision, in order, and how many options each decision has (so the reliable-bit total is auditable against the §0 budget). Treat this like entviz's "which bits drive which channel" table.
- **Constrained choice only.** Each decision selects among musically valid options (a key, a progression from a curated set, a rhythmic cell, an instrument from a palette). Never emit a pitch/duration that music theory wouldn't endorse for the chosen context.
- **Output format.** MIDI is the primary, canonical, deterministic output (the analog of entviz's SVG render model — exactly reproducible and diffable). Rendered audio (WAV/FLAC via a synth + pinned soundfont) is a convenience for listening and is **not** bit-reproducible across synth/soundfont versions — treat it like entviz treats the PNG raster: regenerable, perceptual, never the source of truth.

## 4. Engineering Discipline

### TDD (Test Driven Development)
1. **Red:** Write a test that fails for the new feature or bug fix.
2. **Green:** Write the minimal code to make the test pass.
3. **Refactor:** Clean up the code while keeping the tests green.

Testing music needs care: assert on the **structured intermediate representation** (the chosen key, scale degrees, durations, instrument numbers, the bit→decision mapping) and on **deterministic MIDI bytes**, not on subjective audio. Reserve listening for human review of the songbook (§5).

### Naming & Metaphor
Code is a human language. Adhere to a consistent **musical** metaphor (this project's analog of entviz's Cells/Nucleus/Edge):

- **Motif** — the whole rendered output for one input.
- **Phrase** — a melodic unit; motifs are built from phrases (and call-and-answer between them).
- **Voice** — one instrument line (lead / harmony / rhythm).
- **Palette** — the chosen set of instruments/timbres.
- **Cadence** — a progression's resolution.
- Avoid generic names like `Manager` or `data`. If you introduce a new concept, give it a name that fits the musical metaphor and record it in `this.i`. The metaphor vocabulary above is provisional — refine it in the spec and `this.i`, then keep code faithful to it.

## 5. Operational Workflow

1. **Research & Strategy:** Use search/read tools to understand context; for anything touching the entropy→music mapping, confirm the relevant music theory first.
2. **Intent Update:** If the task involves a design choice, update `this.i` first.
3. **Implementation (TDD):** Write a failing test, verify failure, implement the minimal change, verify success.
4. **Validation:** Run all project tests to ensure no regressions.
5. **Regenerate the songbook:** Any time a change can alter rendered output — anything touching normalization/fingerprinting, the bit→decision schedule, melody/harmony/rhythm generation, the instrument palette, or MIDI emission, or any spec change that flows into the renderer — regenerate the **songbook** (the project's audible regression surface: a fixed corpus of input values rendered to MIDI, plus a browsable `docs/songbook.html` that plays/notates them) and commit the updated MIDI alongside the code. MIDI is deterministic and byte-comparable, so this is enforceable in CI exactly as entviz enforces its gallery: a `tests/test_songbook.py` regenerates every corpus MIDI in-process and fails if it drifts from the committed bytes or if the committed file set diverges from the generator's. (These scripts/tests don't exist yet — build them alongside the first renderer; this step states the standing discipline.) Skip only for changes that provably cannot affect output (pure docs, comments, test-only edits).

## 6. Defect Management (GitHub Issues)

This repo tracks defects as **GitHub Issues** on `dhh1128/entmotif`, managed with the `gh` CLI (no issue-tracker MCP server). Use the standard `bug` label.

**Logging a bug.** When a maintainer says "log a bug about X" (or an agent discovers a defect worth tracking), create the issue immediately — do not wait for confirmation — and report the issue number and URL. Write the script to a temp file and run it (heredocs pasted into chat break on indentation):

```
gh issue create --repo dhh1128/entmotif --label bug \
  --title "<concise summary of the defect>" \
  --body "<Summary / Steps to reproduce / Expected / Actual / Environment / Notes>"
```

Fill in every section you can; omit one only when it genuinely doesn't apply. The only triage label is `bug`.

**Fixing a bug.** When a maintainer says "let's fix bug X":

1. Resolve X to an issue: `gh issue list --repo dhh1128/entmotif --label bug --state open --search "X"`, or `gh issue view <n>`. Confirm the match before proceeding.
2. Branch `fix/<issue#>-<short-slug>` off the default branch.
3. Fix it TDD-style per §4 (failing test first, then the minimal fix, then refactor).
4. If the fix can alter rendered output, regenerate the songbook per §5 step 5 and commit it alongside the code.
5. Reference `Fixes #<n>` in the commit message and/or PR body so the issue auto-closes on merge.

**Finding bugs.** `gh issue list --repo dhh1128/entmotif --label bug --state open` lists the open backlog; `gh issue view <n>` shows one.

## 7. Navigation

- [README.md](README.md) - Project overview and developer onboarding.
- [docs/spec.md](docs/spec.md) - Algorithm specification (to be written).
- [this.i](this.i) - The "Why" behind the project (to be created).
- [CLAUDE.md](CLAUDE.md) / [GEMINI.md](GEMINI.md) / [.cursorrules](.cursorrules) - Tool-specific pointers to this file.

<!-- >>> tick stanza >>> (managed by `tick init`) -->

## Task tracking: `tick`

This repo tracks tasks, tech debt, and ideas in a local [`tick`](https://github.com/dhh1128/tick)
ledger (an orphan `tick` branch; the `tick` CLI is the interface). Reads are plain
files — do **not** use an external API for task tracking.

- **First, if a `tick` command says the repo isn't initialized**, run `tick init`
  once to connect this clone to the ledger — it adopts the existing remote ledger
  if a colleague already set one up, or creates a new one otherwise.
- **A tick mark is the sigil `~` immediately followed by a digit-first 4-char
  base32 id** (the id part looks like `4mz3`, so the full mark is that id with a
  leading `~`). It pins a tick to a code location.
- **Before editing a file**, grep it for marks and read what they reference:
  `rg '~[2-7][a-z2-7]{3}\b' <file>` then `tick show <id>`. A mark means recorded
  context exists for that spot — read it first.
- **Search** existing ticks with `tick grep <text>`; **list** with `tick ls`.
- **Capture** new work with `tick add "<title>"` and place the printed mark
  (`~` + the new id) at the relevant code spot.
- When your change **resolves** a tick, run `tick off <id>` and **delete the
  mark(s)** it reports still in the code.
- A tick that turns out to be a real design decision should **graduate** into
  `this.i` when closed (the ledger is the workshop; `this.i` is the showroom).

<!-- <<< tick stanza <<< -->
