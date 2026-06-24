# Entmotif Paper — Approved Plan (drafting deferred)

Status: **plan approved 2026-06-23; drafting deferred** by maintainer to prioritize
building the motif engine. Resume by handing this file (and the sources) to the
ghostwriter skill. Companion to `../entviz/docs/entviz-paper.md`.

## Parameters
- **Form / output:** academic companion paper → `docs/entmotif-paper.md`.
- **Audience / grade:** technically literate generalist; assumes neither
  music-cognition nor crypto expertise; undergraduate level.
- **Voice:** third-person academic ("we"). **Author:** Daniel Hardman.
- **Citations:** ACM-style numbered `[n]`, mapped to `docs/references.md` keys;
  bibliography as a separate artifact; every load-bearing claim traces to a source
  with a recorded verification status. Borrowed intro-framing sources (Perrig &
  Song; Turner, Shahandashti & Petrie; Whitten & Tygar) must be **verified** and
  added to `references.md` before final.
- **Length:** ~6 sections.
- **Stance:** a *design-and-reasoning* paper — candid that there is no
  implementation and no listening study yet (mirroring entviz's candor about
  untested ergonomics). Distinguish estimates from measurements throughout.

## Central metaphor (approved)
**Recognizing a familiar voice or face** — instantly known, impossible to
reproduce from memory. That gap *is* Model B (recognition without reconstruction),
the line that most separates entmotif from entviz (which compares losslessly).
(Rejected alternatives: the *leitmotif*; no metaphor.)

## Outline (approved)
1. **Introduction** — the human-verification bottleneck (shared with entviz); why
   the ear; the voice/face hook; thesis; what this paper is and isn't.
2. **From comparison to recognition** — Model A vs. B; why *lossy* is acceptable
   and what relaxed cryptographic rigor buys; contrast with entviz's losslessness.
3. **The discrete/analog law** — reliable bits from discrete categories; analog as
   recognition margin + casual avalanche; consumed-vs-delivered (honestly trimmed).
4. **Turning entropy into music without noise** — musicality-first; hash-then-
   choose; style as master dimension + two-layer style/lead model; whole-motif
   integrity (engineering whose *perceptual* payoff is untested); render fidelity +
   pinned soundfont.
5. **The bit budget, honestly** — independence-audited schedule; the conditioning
   (exposure, time, device, culture); the length↔bits curve; randomart's ~20–24
   visual-bit benchmark.
6. **Evidence and adversarial review** — the panel; what it got right (rhythm,
   contour-over-time, amusia, culture) and wrong (the style misread); the
   verification; the Schellenberg backbone; conclusion + open questions (unbuilt
   engine, the recognition≠cryptographic-proof anti-claim, determinism, the A/B/X
   study that converts estimates to measurements).

## Source-of-truth inputs
`this.i`, `docs/bit-budget.md`, `docs/references.md`, `reviews/`, `AGENTS.md`,
`README.md`, and (for structure/spirit) `../entviz/docs/entviz-paper.md`.
