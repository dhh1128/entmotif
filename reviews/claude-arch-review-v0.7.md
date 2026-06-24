# entmotif `motif.py` v0.7 — Architecture & Maintainability Review

**Reviewer lens:** Senior software architect. Fowler *Refactoring* smells, SOLID, separation of concerns, clarity, naming. Music-theory correctness is explicitly **out of scope** — this judges software-engineering merit only.

**File under review:** `/home/daniel/code/entmotif/experiments/engine/motif.py` (~527 lines, zero-dependency prototype)

**Hard invariants any refactor MUST preserve** (from `AGENTS.md` §3 + file docstring):

1. **Zero third-party dependencies** — `hashlib`, `math`, `struct` only.
2. **Determinism** — same input string ⇒ byte-identical MIDI, on every platform. No wall-clock, locale, env, or RNG. Entropy is the *only* source of variation; everything downstream is a pure function of the SHA-512 fingerprint.
3. **Avalanche** — a one-character input change must produce an audibly different motif (demo rows #1 vs #2 are the living assertion of this).
4. It will **graduate into a `src/` package developed under TDD**, with a golden-output songbook test (`tests/test_songbook.py`) as the regression surface (`AGENTS.md` §5).

The single most important consequence of #2/#3: **the order and the exact string labels passed to `Chooser`** (`"mode"`, `"key"`, `"idea_d0"`, `"breath%d"`, `"dev%d"`, …) are part of the observable contract. Each label seeds a SHA-512 draw; rename a label or reorder/insert a draw and the bytes change. **Any refactor must treat the label strings as a frozen wire format** — preserve them verbatim even while renaming the surrounding Python identifiers. This is the central discipline that makes the whole sequence below safe.

---

## 1. Top problems, ranked

### P1 — `generate()` is a god-function mixing every concern (lines 299–392)
**Smells:** *Long Function*, *Divergent Change*, no separation of concerns.

A single ~94-line function does, in one breath: (a) **entropy decisions** — ~18 `Chooser` draws for mode/key/lead/tempo/leap/tendency/resolution/form/fat/figr/bass/template/color/sig plus the figure picks; (b) **range/tessitura math** (`ilo/ihi/icen`, `tonic`, `lo/hi`, `base`, lines 307–310); (c) **form expansion** via `build_form`; (d) **arch/dynamics planning** (`peak`, `span`, `frac`, `center`, `dyn`, lines 331–342); (e) **per-unit melody generation** with four template-specific branches inline (lines 344–385); (f) **arrangement assembly**; and (g) **metadata packaging** (lines 387–391). It is the place every future feature must edit, so it attracts every kind of change at once — the textbook *Divergent Change* smell. It is also effectively untestable below the whole-function level: there is no seam to assert "given this fingerprint, these decisions" separately from "given these decisions, these notes."

This is the #1 obstacle to the planned TDD graduation: §4 of `AGENTS.md` wants tests on "the chosen key, scale degrees, durations, instrument numbers, the bit→decision mapping" as a *structured intermediate representation* — which does not exist as a value today; it is implicit in local variables.

### P2 — `line()` has an ~18-parameter signature (lines 158–159)
**Smell:** *Long Parameter List*, low cohesion, *Data Clumps*.

```python
def line(figs, chords2, mode, key, base, lo, hi, bar0, center, tendency, leap, ch,
         tag, offset, invert, sig, chan, vel):
```

Eighteen positional parameters. Call sites (lines 348, 354, 358, 368, 382) are dense and unreadable; the contrary-motion call passes `lo - 7, hi - 9, ..., center - 9, -tendency, 0, ..., True, None, 3, 72` as bare positionals — impossible to read without counting commas against the def, and a magnet for argument-transposition bugs. The clump is real: `(mode, key)` is a tonal context, `(lo, hi, center, base)` is a tessitura, `(tendency, leap, sig, offset, invert)` is a melodic-contour policy, `(chan, vel)` is an output channel. These travel together everywhere and should be objects.

### P3 — Terse, non-metaphor names violate `AGENTS.md` §4 wholesale
**Smell:** *Mysterious Name*; direct contract violation.

`AGENTS.md` §4 mandates a musical metaphor — **Motif / Phrase / Voice / Palette / Cadence** — and explicitly says "avoid generic names." The code instead uses cryptic abbreviations almost everywhere: `cpcs` (chord pitch-classes), `snap`, `step`, `_voice`, `cadc`, `chm`, `chs`, `cad`, `dv`, `frac`, `figr`, `fat`, `sd`, `bt`, `voic`, `seqv`, `pat`, `ivs`, `pcset`, `ev`, `q`, `nU`, `ihi/ilo/icen`, `cr_answer`, `dyn_bars`. Single-letter loop bodies (`b`, `k`, `m`, `d`, `s`, `u`) compound it. **Not one** of the prescribed metaphor nouns appears as a type or function name. For a project whose first principle is "comprehension is the primary output," this is the highest-leverage clarity debt — and the cheapest to start paying down (pure renames under a golden test).

### P4 — `Chooser` label strings are a hidden, stringly-typed wire format (lines 85–106, used throughout)
**Smell:** *Primitive Obsession* / hidden coupling; a determinism landmine.

Determinism is keyed on ad-hoc string labels assembled inline: `"%s_d%d" % (tag, k)`, `"dev%d" % devslot`, `"breath%d" % u`, `"ans%d" % u`, literals `"sd"`, `"sd2"`, `"mode"`, `"sig"`, etc. These strings *are* the determinism contract (§ intro above), yet they are scattered as inline literals with no central registry, no documented "bit schedule" (which `AGENTS.md` §3 explicitly requires: "Bits are consumed by a documented schedule … exactly which fingerprint bits feed which musical decision, in order"). A future refactor that innocently renames `tag` from `"idea"` to `"phrase"`, or reorders two draws, silently breaks every committed golden file with no compile-time signal. This is *Primitive Obsession* with a determinism blast radius.

### P5 — `arrange_unit()` mixes figuration dispatch, voicing, register math, and event encoding (lines 226–260)
**Smells:** *Long Function*, *Switch Statements*, *Feature Envy*, leaky note-tuple format.

One function branches on `figr` (`block`/`stabs`/`arp`/`alberti`) **and** on `bassfig` (`pedal`/`walking`/`root5`), emitting raw 5-tuples `(channel, midi, velocity, start_tick, dur_tick)` inline with hand-computed tick arithmetic (`base + i * (DIV // 2)`, `4 * DIV - 6`). The `if/elif` chains are classic *Replace Conditional with Polymorphism* candidates. The magic `- 6` / `- 4` note-shortening (to avoid overlap) is repeated and unexplained. The bass-tone lambda `bt = lambda pc: 36 + pc` (line 249) buries the bass register constant. The note format leaks: the *meaning* of tuple slots is encoded positionally and re-decoded by index everywhere downstream (`n[0]`, `n[3]`, `n[4]` in ABC; `chn, pitch, vel, start, dur` in MIDI).

### P6 — The note 5-tuple `[chan, pitch, vel, start, dur]` is an anonymous positional record used everywhere
**Smell:** *Primitive Obsession*, *Data Clump*, fragile positional access.

Notes are `list`/`tuple` of 5 positional fields. `line()` builds `[chan, cur, vel, int(...), int(dur*DIV)]` (line 188); `arrange_unit` builds `(channel, midi, vel, start, dur)`; `cadence_bar` builds another shape entirely — `(chan, pitch, vel, start, dur)` — fine, but `_voice` (line 434) and `abc_export.pick` (line 461) re-slice by raw index (`n[0]`, `n[1]`, `n[3]`, `n[4]`), and confusingly `_voice` treats `n[0]` as *start tick* whereas elsewhere `n[0]` is *channel*. Two different positional conventions for "a note" coexist: the engine's `(chan, pitch, vel, start, dur)` and the ABC layer's projected `(start, dur, pitch)` from `pick`. This is exactly the kind of mismatch that a named record (frozen `NamedTuple`/`dataclass`) eliminates at zero runtime cost and zero determinism risk.

### P7 — Magic numbers and unexplained constants saturate the arithmetic
**Smell:** *Magic Number*, poor explanatory power.

Examples: tessitura math `tonic + 15`, `tonic - 3`, `lo + (hi-lo)//4`, `hi - 2`, `melody_lo - 4`, `top = melody_lo - 4`, `top - 13` (line 214); voicing gap `+ 3` / `cand < m + 3`; bass register base `36`; comp base `34`/`42`/`40`/`38` velocities; note-tail trims `- 6` / `- 4`; arch ratio `2.0/3.0`; drift clamp `round((center-cur)/3.0)`, `max(-2, min(2, …))`; `SEVENTH = 10` is named but `+ 2` (the added 9th in `voice_chord` fat=3, line 212) is not. `DIV = 480` is reasonably named, but `DIV // 4` (16th-note ticks) recurs un-aliased in `_dtok`/`_rest`. Each bare number is a small comprehension tax and a refactoring hazard; collect them into named constants or a config object.

### P8 — Global music-theory tables are module-level mutable structures with no model boundary (lines 35–71)
**Smell:** *Primitive Obsession* / missing domain model; *Shotgun Surgery* risk.

`MAJOR_SCALE`, `MINOR_SCALE`, `CHORDS`, `APPLIED`, `SEVENTH`, `ROMAN_TO_MINOR`, `FIGURES`, `HOOKS`, `SIG_STEPS`, `BREATHS`, `TEMPOS`/`TEMPO_W`, `MAXLEAP`, `SIGMA`, `LEADS`, `LEAD_NAMES`, `LEAD_RANGE`, `ANSWER_INSTR`, `LEAP_NAMES`, `KEY_NAMES`, `DYN_VEL`, `ABC_PC` — ~21 bare dicts/lists at module scope, mixing **theory** (scales, chords), **palette** (instrument programs, ranges, names), **rhythm vocabulary** (figures, hooks), **planning weights** (`MAXLEAP`, `SIGMA`, `TEMPO_W`), and **notation tables** (`ABC_PC`, `KEY_NAMES`). They are read from every function and from two output backends. Because `CHORDS[mode][s]` is mutable and globally reachable, there's no enforced read-only boundary, and adding a genre/palette (the explicit broad-style goal in §0) means *Shotgun Surgery* across the file. These belong behind a **Palette** and a music-theory **model** module.

### P9 — Module conflates four layers with only comment-banner separation (whole file)
**Smell:** missing module boundaries; *Single Responsibility* at the file level.

The file is sectioned only by ASCII comment banners (`# --- melody ---`, `# --- arrangement ---`, `# --- ABC ---`, `# --- MIDI ---`). Entropy/decision, theory model, generation, ABC notation, and MIDI encoding all live in one namespace and freely reach into each other's globals. The MIDI writer (`write_midi`, lines 480–501) and ABC exporter (`abc_export`/`_voice`, 456–476) are genuinely independent output backends that should not share a module with the generator, yet both depend on the positional note tuple and on `DIV`/`KEY_NAMES` globals. This is the boundary the planned `src/` package split should follow.

### P10 — Output-encoding helpers are private-by-underscore but carry real logic; duplicated tick math
**Smell:** *Duplicated Code*, misleading visibility, *Feature Envy*.

`_dtok` (417) and `_rest` (422) both compute `int(round(ticks / (DIV // 4)))` then `str(n) if n != 1 else ""` — duplicated logic, one prepending `z`. `_voice` (427) reaches across the whole note list and re-implements grouping/sorting of simultaneous events. `abc_pitch` (400) hard-codes octave math (`m // 12 - 1`, `octv >= 5`, `"'" * (octv-5)`, `"," * (4-octv)`) with no explanation of the reference octave. These are cohesive enough to form an `AbcWriter` with shared duration-token logic, removing the duplication and the leading-underscore "pseudo-private" smell (they're module functions, not class privates).

### Honorable mentions (lower severity)
- **`step()` (130–135)** silently returns `cur` on empty scale — a swallowed edge case with no signal.
- **`snap()` (123–127)** falls back to "all chromatic pitches" when no chord tone is in range — silent semantic fallback worth a named guard.
- **`line()` inline anti-repeat** (lines 182–187) is a non-obvious nested concern (avoid repeating the previous landed note) buried mid-loop; extract & name it.
- **`build_form()` (267–289)** forces the terminal cadence by *post-hoc tuple surgery* (`units[-1] = (role, ["V","I"], "authentic", dv)`, lines 287–288) — mutation-after-construction that's easy to miss.
- **`__main__` demo block (508–527)** mixes a hardcoded corpus, file I/O (writing `.mid` to cwd), and ASCII-table formatting into the library module; belongs in a CLI/script entry point, not the engine.

---

## 2. Proposed module + class/function structure

Target the `src/` graduation now, so the package boundaries are the seams the TDD tests assert against. Five modules along the four concerns (entropy/decision, theory model, generation, notation+MIDI export), realizing the §4 metaphor.

```
src/entmotif/
├─ entropy.py        # Chooser → Entropy/Oracle: the deterministic draw engine
├─ theory.py         # the music-theory MODEL (scales, chords, cadences, tessitura)
├─ palette.py        # instrument/timbre selection (the §4 "Palette")
├─ plan.py           # entropy → a structured DECISION record (the bit-schedule)
├─ generate.py       # decisions → Motif (Phrases, Voices) — pure musical assembly
├─ render/
│   ├─ abc.py        # Motif → ABC text   (one output backend)
│   └─ midi.py       # Motif → MIDI bytes (the canonical backend)
└─ cli.py            # corpus demo, file I/O, the table printer (was __main__)
```

### Core domain types (frozen / immutable — determinism-friendly)

- **`Fingerprint`** — wraps the 64 SHA-512 bytes of the canonical input. Constructed once.
- **`Oracle`** (rename of `Chooser`) — the only place that turns labels into choices. Methods `index`, `choice`, `weighted` (current `int`/`choice`/`weighted`, with `int` renamed off the builtin). **Crucially, label strings stay byte-identical** — see §3.
- **`TonalContext`** — `(mode, key)` plus derived `scale_pcs`. Replaces the `(mode, key)` clump threaded through ~10 functions. Owns `scale_pitch_classes()`, `chord_pitch_classes(symbol)` (was `cpcs`), `scale_tones(lo, hi)`, `degree(n, …)`.
- **`Tessitura`** — `(lo, hi, center, base)` register window. Replaces the `lo, hi, center, base` clump. Owns `snap(target, pcs)` (was `snap`) and `step(cur, delta)` (was `step`).
- **`ContourPolicy`** — `(tendency, leap, sigma, max_leap, sig_interval, offset, invert)` — the melodic-shape inputs to `line()`. Replaces the bulk of `line`'s parameter list. Owns `gravity_delta(...)`.
- **`Cadence`** — value object for a resolution kind (`authentic`/`deceptive`/`half`) knowing both its progression (`cadc`) and its melodic close (`cadence_bar`). Realizes the §4 **Cadence** noun.
- **`Note`** — frozen `NamedTuple(channel, pitch, velocity, start, duration)` (P6). One canonical shape; the ABC layer derives its own projection explicitly rather than re-slicing by index.
- **`Voice`** — a channel's worth of `Note`s plus its role/name (`lead`/`comp`/`bass`/`answer`). Realizes §4 **Voice**; replaces the `pick([0])` channel-filtering scattered in `abc_export`.
- **`Phrase`** — the notes for one 2-bar unit across voices (melody + arrangement + counter/antiphon). Realizes §4 **Phrase**; what the per-`u` loop body in `generate` produces.
- **`Motif`** — the whole rendered output: ordered `Phrase`s + `MotifPlan` metadata (was the `meta` dict). Realizes §4 **Motif**; the single object both renderers consume.

### Decision/plan layer (cracks open P1)

- **`MotifPlan`** — the *structured intermediate representation* `AGENTS.md` §4 asks tests to assert on. A frozen record of every discrete decision: `mode, key, lead, tempo, leap, tendency, resolution, form, fat, figuration, bass_figuration, template, color, sig_interval, hook, figures, …`. Produced by `plan_motif(fingerprint) -> MotifPlan` — a thin, linear, **auditable** function that makes ~18 `Oracle` draws *in the documented order* (the bit schedule). This is where the determinism contract becomes visible and testable.
- **`build_form(plan, oracle) -> list[Unit]`** stays close to current, but `Unit` becomes a small record `(role, chords, cadence, dev_slot)` instead of a bare 4-tuple, and the terminal-cadence force (P8 honorable mention) becomes an explicit `units[-1] = units[-1].with_authentic_close()` method call.

### Generation layer

- **`generate(plan) -> Motif`** shrinks to an orchestrator: build `TonalContext`/`Tessitura` from the plan, compute the `ArchPlan` (peak/span/center/dynamics — extract `plan_arch(units, peak)` and keep `unit_dyn`), then for each `Unit` delegate to a **`PhraseBuilder`** keyed by `template`. The four template branches (`solo_bed`/`lead_counter`/`call_resp`/`groove_first`) become a small strategy set (P5-style polymorphism) rather than inline `if template == …` tests.
- **`PhraseBuilder.melody_line(...)`** is the renamed `line()`, now taking `(figures, chord_symbols, TonalContext, Tessitura, ContourPolicy, Voice-spec)` — collapsing 18 params to ~5 cohesive objects (P2). The inline anti-repeat logic (lines 182–187) becomes a named `_avoid_repeat(...)` helper.
- **`Arranger`** owns the former `arrange_unit` + `voice_chord`, with `Figuration` strategies (`Block`/`Stabs`/`Arp`/`Alberti`) and `BassFiguration` strategies (`Pedal`/`Walking`/`RootFifth`) replacing the `if/elif` ladders (P5). Velocities/tick-trim constants become named class fields.

### Render layer (two independent backends, P9)

- **`render/abc.py`** — `AbcWriter` class: `pitch(midi)` (was `abc_pitch`), `duration_token(ticks)` and `rest_token(ticks)` sharing one `_sixteenths(ticks)` helper (kills P10 duplication), `voice_line(...)` (was `_voice`), `export(motif) -> str`. `ABC_PC` becomes a class constant.
- **`render/midi.py`** — `MidiWriter`: `write(motif, path)` and a pure `to_bytes(motif) -> bytes` (so the golden test can assert bytes without touching the filesystem). The variable-length-quantity encoder becomes a named `_vlq(delta)` helper.

This split lets the songbook test (`AGENTS.md` §5) assert at three levels — `plan_motif` decisions, `Motif` IR, and final `MidiWriter.to_bytes` — instead of only on end-to-end bytes.

---

## 3. Ordered, behavior-preserving Fowler refactor sequence

**Precondition (do this first, before any other step): establish the golden harness.** Write `tests/test_songbook.py` that, for the existing demo corpus (the six inputs in `__main__`, lines 509–512) plus a handful more, captures `generate(v)` output and `write_midi` bytes (via an in-memory buffer) and asserts byte-identity. Commit the golden `.mid` files. **Nothing below is safe without this** — it is the only thing that proves determinism/avalanche survived each step.

> Throughout: the `Oracle`/`Chooser` **label strings are frozen**. Renames touch Python identifiers only, never the literal arguments to `v`/`int`/`choice`/`weighted`. After any step that could plausibly touch a label, diff the golden bytes.

Each step is individually green-able under the harness:

1. **Pure renames, leaf-first (P3).** Rename within a function body only, no signature changes: `voic→voicing`, `seqv→sequence`, `pat→pattern`, `ivs→intervals`, `pcset→pitch_classes`, `ev→events`, `q→vlq_bytes`, `nU→unit_count`, `frac→arch_fraction`, etc. Then function renames with call-site updates: `cpcs→chord_pitch_classes`, `cadc→cadence_progression`, `_voice→voice_line`, `abc_pitch→pitch`. Zero behavior change; golden stays green by construction. Cheapest, highest-clarity win.

2. **Introduce the `Note` named record (P6).** Define `Note = NamedTuple(...)`. Replace tuple/list construction in `line`, `cadence_bar`, `arrange_unit` with `Note(...)`, and index access (`n[0]`, `n[3]`, …) with field access. Reconcile the ABC layer's `(start, dur, pitch)` projection into an explicit `Note→(start,dur,pitch)` mapping. NamedTuple is still a tuple, so sort order and byte emission are unchanged — golden stays green.

3. **Extract named constants (P7).** Replace magic numbers with module-level names *in place* (no logic change): `SIXTEENTH = DIV // 4`, `NOTE_TAIL_GAP = 6`, `BASS_PROGRAM_BASE = 36`, `VOICING_MIN_GAP = 3`, `ARCH_PEAK_RATIO = 2.0/3.0`, comp velocities, tessitura offsets. Pure substitution; golden green.

4. **Extract methods to break up `arrange_unit` (P5).** Extract `voice_chord` figuration arms into `_block/_stabs/_arp/_alberti(voicing, base)` and bass arms into `_pedal/_walking/_root_fifth(...)`, each returning `list[Note]`. Keep the `if/elif` dispatch for now — this is *Extract Method*, not yet *Replace Conditional with Polymorphism*. Golden green.

5. **Extract methods to break up `generate` (P1, first pass).** Pull out, as free functions with explicit params, the cohesive blocks currently inline: `compute_tessitura(lead) -> (lo,hi,center,base)`, `plan_arch(units, peak) -> (span, …)`, and the per-unit melody selection `build_unit_melody(...)`. `generate` becomes a sequence of named calls. Behavior identical (same draws, same order); golden green.

6. **Introduce `TonalContext` and `Tessitura` value objects (P2, Data Clumps).** Define the classes wrapping `(mode,key)` and `(lo,hi,center,base)`; move `chord_pitch_classes`/`scale_tones`/`degree`/`snap`/`step` onto them as methods that delegate to the existing free functions (or move the bodies). Update call sites to pass the objects. Because the objects are thin carriers of the same values, every computation is identical — golden green. This step alone removes most of `line`'s parameter sprawl.

7. **Introduce `ContourPolicy` and finish collapsing `line()`'s signature (P2).** Bundle `(tendency, leap, sigma, max_leap, sig_interval, offset, invert)` into `ContourPolicy`; `line` (now `melody_line`) takes `(figures, chords, TonalContext, Tessitura, ContourPolicy, channel, velocity)`. Move `gravity_delta` onto `ContourPolicy`. Extract the anti-repeat block into `_avoid_repeat`. Golden green (same math, regrouped args).

8. **Introduce the `MotifPlan` decision record + `plan_motif()` (P1, P4).** Extract the ~18 `Oracle` draws from `generate` into `plan_motif(fingerprint) -> MotifPlan`, **preserving draw order and labels exactly**. `generate(plan)` now consumes the plan. This is the determinism-critical step — run the golden diff with extra care, and add a *plan-level* assertion test (e.g. fixed input ⇒ expected `mode/key/tempo/form`). Realizes the §3 "documented bit schedule." Golden green.

9. **Replace figuration/bass conditionals with strategy objects (P5, *Replace Conditional with Polymorphism*).** Turn step-4's extracted methods into `Figuration`/`BassFiguration` strategy classes selected by the plan. Each emits the same `Note`s in the same order. Golden green.

10. **Split into modules (P9), output backends last.** Now that types and seams exist, physically move code into the `src/entmotif/` layout: `entropy.py`, `theory.py`, `palette.py`, `plan.py`, `generate.py`, `render/abc.py`, `render/midi.py`, `cli.py`. Make `MidiWriter.to_bytes` filesystem-free (P-mention). Move the `__main__` corpus/printer into `cli.py`. Imports only — no logic change; golden green. **Stop before** any musical change: this whole sequence is a pure refactor; new features (genres/palettes per §0) come *after* the package and tests are in place.

11. **Tidy the ABC/MIDI helpers (P10).** Fold `_dtok`/`_rest` onto a shared `_sixteenths(ticks)`; name the VLQ encoder `_vlq`. Promote leading-underscore module functions into the `AbcWriter`/`MidiWriter` classes. Golden green; this is the cleanup pass.

Steps 1–3 are reversible, near-zero-risk, and deliver most of the *readability* win immediately; 4–7 deliver the *cohesion* win; 8–11 deliver the *separation-of-concerns / testability* win that unblocks the TDD graduation.

---

## 4. Naming recommendations (old → new)

### Types / classes (introduce the §4 metaphor)
| old | new |
|---|---|
| `Chooser` | `Oracle` (deterministic draw engine) |
| *(none — local vars)* | `Fingerprint` |
| *(`mode, key` clump)* | `TonalContext` |
| *(`lo, hi, center, base` clump)* | `Tessitura` |
| *(`tendency, leap, sig, …` clump)* | `ContourPolicy` |
| *(`meta` dict, line 387)* | `MotifPlan` + `Motif` |
| *(channel-0/1/2/3 notes)* | `Voice` |
| *(per-`u` note batch)* | `Phrase` |
| *(`[chan,pitch,vel,start,dur]`)* | `Note` (frozen NamedTuple) |
| *(figuration if/elif)* | `Figuration` / `BassFiguration` strategies |
| *(resolution string + `cadc`)* | `Cadence` |

### Functions
| old | new |
|---|---|
| `cpcs` | `chord_pitch_classes` |
| `scale_pcs` | `scale_pitch_classes` |
| `snap` | `snap_to_chord_tone` (or `Tessitura.snap`) |
| `step` | `step_scale_degree` (or `Tessitura.step`) |
| `degree` | `scale_degree_pitch` |
| `gravity_delta` | `contour_step` / `ContourPolicy.next_delta` |
| `sym` | `roman_for_mode` |
| `line` | `melody_line` / `PhraseBuilder.melody_line` |
| `cadence_bar` | `cadence_melody` / `Cadence.melody` |
| `voice_chord` | `spread_voicing` |
| `arrange_unit` | `Arranger.arrange` |
| `cadc` | `cadence_progression` / `Cadence.progression` |
| `build_form` | `expand_form` |
| `transform_for` | `motivic_transform` |
| `unit_dyn` | `unit_dynamic` |
| `_voice` | `AbcWriter.voice_line` |
| `_dtok` | `AbcWriter.duration_token` |
| `_rest` | `AbcWriter.rest_token` |
| `abc_pitch` | `AbcWriter.pitch` |
| `chord_name` | `AbcWriter.chord_label` |
| `abc_export` | `AbcWriter.export` |
| `write_midi` | `MidiWriter.write` (+ pure `to_bytes`) |
| `slug` | `filename_slug` |

### Variables / fields
| old | new |
|---|---|
| `fp` | `fingerprint` |
| `ch` (the Chooser) | `oracle` |
| `chs` / `chm` | `chord_symbols` / `chord_symbols_for_mode` |
| `cad` | `cadence` |
| `dv` / `devslot` | `dev_slot` |
| `nU` | `unit_count` |
| `frac` | `arch_fraction` |
| `figr` | `figuration` |
| `fat` | `voicing_density` |
| `sd` / `sd2` | `secondary_dominant_pct` |
| `bt` | `bass_pitch` |
| `voic` / `seqv` / `pat` / `ivs` / `pcset` | `voicing` / `arp_sequence` / `alberti_pattern` / `intervals` / `pitch_classes` |
| `ilo/ihi/icen` | `lead_lo` / `lead_hi` / `lead_center` |
| `cr_answer` | `is_call_response_answer` |
| `dyn_bars` | `dynamics_by_bar` |
| `ev` / `q` (in `write_midi`) | `events` / `vlq_bytes` |
| `chord_pitch_classes` arg `chords2` | `chord_symbols` |

### Constants (group, don't just rename)
| old (module global) | new home |
|---|---|
| `MAJOR_SCALE`, `MINOR_SCALE`, `CHORDS`, `APPLIED`, `SEVENTH`, `ROMAN_TO_MINOR` | `theory.py` |
| `LEADS`, `LEAD_NAMES`, `LEAD_RANGE`, `ANSWER_INSTR` | `palette.py` (the §4 **Palette**) |
| `FIGURES`, `HOOKS`, `SIG_STEPS`, `BREATHS`, `TEMPOS`/`TEMPO_W`, `MAXLEAP`, `SIGMA`, `LEAP_NAMES` | `plan.py` / generation config |
| `KEY_NAMES`, `ABC_PC`, `DYN_VEL` | `render/abc.py` (+ `DYN_VEL` shared with MIDI velocity) |
| `DIV`, `DIV//4` | `SIXTEENTH`, `TICKS_PER_QUARTER` |

---

## Closing note

This is a **well-behaved prototype masquerading as production code**: the determinism discipline is real and the music logic is dense but coherent. The debt is almost entirely *organizational* — a god-function, a parameter-list explosion, missing domain types, and a wholesale departure from the project's own mandated metaphor (§4). None of the fixes require touching the entropy math; the entire sequence above is behavior-preserving under a golden test. The one trap to brief every contributor on, in bold, is that **the `Oracle` label strings are a frozen wire format** — the refactor's whole safety depends on renaming Python identifiers while leaving those literals untouched. Land the golden harness first (it doesn't exist yet, per §5), then the sequence is low-risk and unblocks the TDD `src/` graduation.
