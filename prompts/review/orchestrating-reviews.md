# Orchestrating Adversarial **Design** Reviews — entmotif

Companion to the persona prompts in this folder (`musicologist-composer.md`,
`psychoacoustician.md`, `music-perception-academic.md`, `bit-budget-auditor.md`,
`collision-adversary.md`). Use it when running the personas as subagents (or a
workflow) at a milestone: spawn several, collect findings, dedupe, adjudicate.

> **About this vendored set.** Adapted from entviz's `prompts/review/`. The key
> difference: **entviz reviews *code* against a spec; entmotif has no code yet.**
> This panel red-teams the **design** — the intent layer `this.i` and the
> bit-budget design doc `docs/bit-budget.md`, with supporting evidence in
> `experiments/soundfont/`. So findings target **claims and reasoning**, not
> `file:line` defects; `location` is a `this.i` node id, a `docs/bit-budget.md`
> §section, or a named design dimension.
>
> entmotif makes **two headline claims**, and the roster exists to attack them:
> (1) a **reliable ~25–50-bit budget recoverable by recognition from memory
> (Model B)**; (2) **musical, hummable, recognizable output** rendered through a
> pinned soundfont. Two lenses are bespoke — **bit-budget/determinism** and
> **musicality** — because no generic lens covers entmotif's core promises.

**Read-first artifacts (every persona):** `this.i`, `docs/bit-budget.md`,
`README.md`, `AGENTS.md`, and `experiments/soundfont/` (the MIDI generators and
the listening-test findings they encode). Personas add their own sources.

---

## 1. Roster

| Prefix | File | Lens | Default effort/model |
|---|---|---|---|
| `BIT` | `bit-budget-auditor.md` | Is the independence audit honest? consumed≠delivered sound? schedule deterministic? avalanche real? no double-counting? | deep / strongest |
| `ACA` | `music-perception-academic.md` | Does the research literature support each memorability/recognition/discrete-vs-analog claim, or do we overclaim? | deep / strongest |
| `MUS` | `musicologist-composer.md` | Is it musical, hummable, theory-correct? does constrained generation yield real motifs? genre authenticity at our fidelity? | deep |
| `AUD` | `psychoacoustician.md` | Auditory perception & accessibility: masking, loudness, amusia, hearing loss, device/playback variation, render-fidelity reality. | deep |
| `ADV` | `collision-adversary.md` | Can an attacker craft two inputs whose motifs a human confuses (Model B)? cheapest grindable channel? | deep |

**Default panel:** all five. Inherited code lenses (security, devops,
testability, maintainability, architect) are **deferred until there is code**;
only `this.i`/doc hygiene is in scope now, folded into `BIT` and `MUS`.

Each persona carries a default effort. `BIT` and `ACA` run **deep on the
strongest model** (they attack the headline claim and its evidentiary basis).

---

## 2. Severity = design fix-obligation (not bug triage)

One scale, CRITICAL / HIGH / MEDIUM / LOW, measuring how mandatory a change is
before the **design** is sound enough to build on:

| Level | Obligation |
|---|---|
| **CRITICAL** | The design cannot be built as-is; a core claim is false or unachievable. |
| **HIGH** | Fix before implementation; deferring needs an explicit recorded decision. |
| **MEDIUM** | Worth fixing; acceptable to defer with a note. |
| **LOW** | Optional / polish. |

`severity` is intrinsic; `recommended_disposition` (`recommend-fix` /
`recommend-defer` / `recommend-accept-risk`) is what to do now. Many design
findings are honestly **SPECULATIVE without a listening study** — say so, and
name the smallest experiment that would settle it, rather than overclaiming.

---

## 3. `dedupe_key` convention

`<subject>-<adjective>[-<qualifier>]`, lowercase-kebab. The key names the
*concept* so two personas seeing one issue merge.

- **subjects:** `style`, `lead-instrument`, `contour`, `rhythm`,
  `transformation`, `cadence`, `progression`, `mode`, `tempo`, `meter`,
  `texture-interruption`, `analog-stack`, `fingerprint`, `bit-budget`,
  `soundfont`, `form`, `this-i`, `spec`.
- **adjectives:**

| Adjective | Means | Usual lens |
|---|---|---|
| `overclaimed` | a reliable-bit yield not supported by perception/evidence | BIT, ACA, AUD |
| `double-counted` | shares perceptual variance with another dimension | BIT |
| `collidable` | two distinct inputs → a Model-B-confusable motif | ADV, AUD |
| `grindable` | cheap channel for an attacker to match | ADV |
| `unmusical` | violates theory / sounds bad / not hummable | MUS |
| `indistinct` | below recognition threshold / not distinguishable via the font | MUS, AUD |
| `unrenderable` | cannot be delivered by the pinned soundfont | MUS, AUD |
| `nondeterministic` | output depends on non-entropy state | BIT |
| `unsupported` | contradicted by, or absent from, the research literature | ACA |
| `inaccessible` | fails for amusic / hearing-impaired / phone-speaker users | AUD |
| `decays` | survives immediate test but not memory over time | ACA, AUD |
| `missing` | absent rationale / `this.i` node / spec section | any |

- **qualifiers:** `-over-time`, `-on-phone-speaker`, `-under-amusia`,
  `-for-short-form`, `-cross-culture`.

If none fits, use the most natural adjective and flag it as a candidate
addition. A synthesis-stage semantic clustering pass catches near-duplicate keys
across personas (canonical entry = most-obligated severity, union of reporters).

---

## 4. Manifest schema (final section of each report; required when orchestrated)

Fenced-YAML, one entry per Top Finding:

```yaml
findings:
  - id: BIT-F1
    persona: bit-budget-auditor
    title: <short summary>
    severity: HIGH            # CRITICAL | HIGH | MEDIUM | LOW
    confidence: LIKELY        # CONFIRMED | LIKELY | SPECULATIVE
    location: this.i:2p8z1m40 # node id / docs/bit-budget.md §N / design dimension
    dedupe_key: bit-budget-double-counted
    recommended_disposition: recommend-fix   # fix | defer | accept-risk
    rationale: <one line; lets the orchestrator overrule without re-deriving>
    revisit_condition: null   # required when recommend-defer
    fix_effort: medium        # small | medium | large
    settling_experiment: <smallest study that would confirm/refute, if SPECULATIVE>
```

---

## 5. Collect → merge → adjudicate

1. **Collect** each persona's manifest (the `reviews/` file is durable backup).
2. **Merge** by `dedupe_key` (most-obligated severity wins; union of reporters);
   then the semantic clustering pass.
3. **Adjudicate**: unresolved CRITICAL `recommend-fix` → milestone blocked; HIGH
   → blocked unless explicitly deferred with a reason. Record decisions to pass
   as `prior_dispositions` next run, and surface design-level findings to the
   maintainer for eventual `this.i` recording. **The orchestrator does not write
   `this.i` autonomously.**

---

## 6. Running the panel

Read-only on the repo. Spawn persona subagents (**≤3 concurrent**, RAM ceiling;
prefix `nice -n 19 ionice -c 3` for any heavy shell/render work, esp. `deep`-mode
rendering with FluidSynth), or wire a workflow. Write reports to `reviews/`
(uncommitted, mirroring entviz). `deep` mode means **render motifs and listen**
(use `experiments/soundfont/` as the harness) and **cite real sources** — not
review from memory.

*Canonical conventions live here; persona prompts reference this doc rather than
restating severity/dedupe, so there is one source of truth.*
