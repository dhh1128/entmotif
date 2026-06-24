# Entmotif Bit Budget & Consumption Schedule (DRAFT v2)

**Status:** working design document, not yet normative. Headed for `docs/spec.md`
once pressure-tested (an adversarial review is the next step). Decisions here are
recorded in `this.i`; node ids are cited inline as `[id]`.

This document answers the central question: *can entmotif carry ~25–50 bits of
entropy that an ordinary adult can reliably **recognize** by ear, in a hummable
motif — and exactly which bits come from where, after honestly removing
double-counting?*

> **v2 changes from v1:** adds the two-layer style/lead model `[c2k9p0a4]`, the
> ~32-style inventory `[d4m1z8p0]`, the analog-layer stack `[e9k2m4p1]`, the
> texture-interruption candidate `[f3a0k9m2]`; folds in the soundfont pin
> `[8a3k0f29]` and the listening-test fidelity casualties; and — most
> importantly — replaces the v1 additive totals with an **independence-audited**
> accounting that conditions correlated dimensions on style. The audited totals
> are **lower and more honest** than v1's.

---

## 1. Ground rules (the pillars)

1. **Model B — recognition from memory** `[m4z81p3v]`. Success = a listener who
   heard motif *X* can later decide *from memory* whether a candidate is *X*.
   Only the memorable gestalt counts. (Model A, side-by-side replay, is strictly
   easier and free.)
2. **The discrete/analog law** `[k20f9a3x]`. Reliable bits come **only** from
   discrete musical decisions an untrained ear can re-identify. Analog variables
   (exact pitch/tempo, micro-timing, dynamics) give recognition margin, not
   countable bits. Rows are tagged `D` / `A` / `S`.
3. **Whole-motif integrity (no ignorable tail)** `[9k3f0a72]`. Later bars must
   shape the remembered gestalt; the consequent is a *bound transformation* of
   the antecedent and resolves a tension the antecedent opened.
4. **Style is the master dimension** `[z0m4p81q]`, with a **two-layer
   style↔lead model** `[c2k9p0a4]`: the style owns the *bed* (groove, bass,
   harmonic rhythm, mode, tempo band, meter); the lead instrument is a separate
   capability-gated, affinity-weighted choice on top.
5. **Render fidelity = graceful degradation** `[3k7a92f0]`. A dimension earns
   bits only if distinguishable through the pinned soundfont (**GeneralUser GS**,
   FluidSynth everywhere `[8a3k0f29]`). Listening tests already retired several
   would-be distinctions (below).
6. **Analog layers for aggregate divergence** `[e9k2m4p1]`. Layer many analog
   modulations: zero recall bits, but they raise Model-A distinguishability and
   provide casual avalanche.

## 2. Consumed bits ≠ delivered bits

Entropy source: `SHA-512(canonical-normalized-input-text)` `[81pz4m0v]`, 512
bits, reusing entviz's normalization. **Consumed** = fingerprint bits the
schedule reads (target ~120–180 once analog layers are counted). **Delivered** =
bits a human reliably recovers under Model B (the 25–50 headline). Because we
consume far more than we deliver, two different inputs collide in the *rendered
MIDI* only at ~`2^-consumed` (machine-rare), while human-recognition collisions
sit at the *delivered* rate (~`2^-25..50`) — the intended lossy contract.

## 3. Independence-audit methodology

v1 summed per-dimension yields and over-counted, because **style gates
mode/tempo/meter/instrument/groove** — those dimensions share perceptual
variance with style. v2 estimates the **joint cardinality** instead: each
correlated dimension is scored by its *marginal* (conditional-on-style) reliable
yield, not its gross yield. Equivalently: total ≈ log₂(number of
reliably-distinct *whole motifs*), not the sum of independent-looking knobs.
These are still **pre-empirical estimates** — the adversarial review and later
A/B/X listening studies should move them.

## 4. The audited schedule (8-bar antecedent–consequent period, v1)

| Dimension | Class | Style-gated | Marginal reliable bits |
|---|---|---|---|
| **Style preset** (master) `[z0m4p81q]` | D | — | **5 – 6** |
| Lead instrument (from style's gated pool) `[c2k9p0a4]` | D | yes | 1.5 – 2.5 |
| Mode / tonal-color variant | D | yes | 0.5 – 1 |
| Tempo within style band | S | yes | 0.25 – 0.75 |
| Meter residual | D | yes | 0.25 – 0.5 |
| Antecedent **rhythmic motif** (melodic) † | D | partial | 2.5 – 3 |
| Antecedent contour + opening gesture (overlap-discounted) ‡ | D | partial | 2.5 – 3 |
| **Consequent transformation** (whole-motif, integrity) `[9k3f0a72]` | D | no | 2 – 3 |
| Cadence type (authentic/plagal/deceptive) | D | partial | 0.75 – 1.25 |
| Form / phrase count (v1 ≈ fixed period) | D | — | 0.25 – 0.75 |
| Harmonic progression (within style vocabulary) | D | yes | 1.5 – 2 |
| Groove variant (within style) | D/S | yes | 0.5 – 1 |
| Accompaniment texture (block/arp/ostinato/drone) | D | yes | 0.5 – 1 |
| Texture-interruption layer (candidate) `[f3a0k9m2]` | D | no | 1 – 2 |
| Key / absolute pitch | A | — | 0 (no absolute pitch; register/singability lever) |
| Analog stack (dynamics, articulation, swing, rubato, …) `[e9k2m4p1]` | A | — | 0 (margin + avalanche only) |
| **TOTAL — 8-bar period** | | | **~19 – 28** |

† **melodic rhythm** is an *immediate-test* figure; rhythm *alone* is a weak
long-term retrieval cue (`[HebertPeretz1997]`), so this row decays over long
unrehearsed delays. Caveat: that study tested *familiar*-tune naming, not novel-
motif discrimination, and it does **not** touch the *groove-bed* rhythm that
carries style (durable). ‡ **contour** dominates at short delays but cedes to
interval-in-tonality after long *filled* delays (`[DowlingKwakAndrews1995]`);
our tonal, "real" melodies partly mitigate. See §8.

## 5. Totals & the length↔bits curve (honest)

| Form | Bars | Reliable (delivered) bits |
|---|---|---|
| Single phrase | ~4 | ~14 – 20 |
| **8-bar period (v1 target)** | ~8 | **~19 – 28** |
| + 3rd phrase / AABA (new contour+rhythm+transformation, discounted) | ~12–16 | ~25 – 40 |
| Longest/richest form + 64-style inventory | ~16 | ~35 – 45 (50 only at the optimistic edge) |

**Honest landing (revised down from v1):** the independence audit confirms the
**25-bit floor is reachable** but tighter than v1 implied — an 8-bar period lands
~19–28, centered low-/mid-20s, and **reliably clearing 25 wants the 3rd-phrase
extension.** The **upper end (~50) is aspirational**, attainable only in the
longest, richest form at optimistic estimates. Style absorbing the
mode/tempo/meter/instrument correlations is *why* the honest number is lower than
the naive sum — and also why the bits we keep are sturdy and redundant
(Model-B-safe). This recalibration is itself a finding the review should stress.

### Conditions on these numbers (evidence-grounded — see §8)

These are **estimates at immediate test**, unmeasured, holding for a **typical
listener: Western-enculturated, normal-hearing, who has heard the motif at least
twice** — an assumption with direct support: novel melodies consolidate after two
exposures with no week-long forgetting (`[SchellenbergHabashi2015]`). The figures
**erode** under conditions they do not include, each evidence-grounded:

- **Long unrehearsed intervals:** the melodic-rhythm (†) and contour (‡) rows
  weaken; the durable residue is **timbre/style** plus interval-in-tonality
  (`[SchellenbergHabashi2015]`, `[DowlingKwakAndrews1995]`, `[HebertPeretz1997]`).
- **Lo-fi playback / hearing loss / amusia (~1.5%):** see §7 and the review's
  accessibility finding.
- **Non-Western listeners:** the mode/cadence *affect* bits are enculturated
  (`[Smit2022]`); the culture-robust core is timbre/groove/texture.

So quote the range as the **optimistic, immediate, typical-listener** estimate it
has always been — not a guarantee across every listener, device, and delay. The
A/B/X study in §7 is what converts any of these into a measurement.

## 6. Style inventory & render-fidelity casualties

Target ~32 styles in v1 (5 bits), expandable to ~64 `[d4m1z8p0]`, spanning
keyboard/jazz/blues · classical · Latin/Caribbean · world (Asia/Mideast/folk) ·
Americana/country · pop/rock/electronic · film/mood · sacred · solo/novelty.
Two listening batches validated mutual distinctiveness for ragtime, boogie,
bossa, samba, sitar, synthwave, spaghetti-western, chant, reggae, rock-ballad,
Celtic jig, polka, and novelty/SFX (most distinct of all, via texture
interruption `[f3a0k9m2]`).

**Retired by the fidelity gate** (do not claim): shakuhachi (reads as
marimba/mallet); the free-reed twins {accordion, bandoneon, harmonica} → one
slot; the breathy-flute twins {pan flute, ocarina} → one slot; **operatic aria /
solo voice** (Voice Oohs indistinct from flute) — so the only surviving vocal
style is **ensemble Gregorian chant** `[q9f3a7k2]`.

## 7. Open questions / what the review and studies must settle

- **Are the `D` marginal yields real under Model B?** Every number in §4 is an
  estimate; an A/B/X recognition study should confirm or shrink them. The whole
  budget rests on these.
- **Is the independence audit aggressive enough?** Residual correlations
  (rhythm↔meter, contour↔transformation, progression↔mode) may still inflate the
  total.
- **Memorability decay.** Model B over *time* (minutes? days?) is untested;
  recall degrades and may erase the lower-yield dimensions first.
- **Population variation.** Congenital amusia (**~1.5%**, not the obsolete 4% —
  `[PeretzVuvan2017]`; degrades *unevenly*, sparing timbre/rhythm), hearing loss,
  phone-speaker playback, and musical-culture differences (`[Smit2022]`) all erode
  the budget — still unquantified, pending the study.
- **Adversarial collision.** Cheapest channel for an attacker to grind a Model-B
  near-collision; whether style+contour+rhythm can be matched while the rest
  diverges unnoticed.
- **Soundfont pin** still tentative `[8a3k0f29]`; the SF2/web path
  (js-synthesizer WASM) is unproven in practice.
- **Bit-reader bias**: modulo vs rejection sampling for non-power-of-two option
  counts.

## 8. Verified evidence (review of 2026-06-23)

The adversarial design review (`reviews/review-panel-2026-06-23.md`) challenged
the headline; its load-bearing citations were then **independently verified**
(full annotations in `docs/references.md`). Outcome:

- **Style was NOT downgraded.** The review's claim that genre recognition is
  unreliable rested on a **misread** of `[GjerdingenPerrott2008]` — its 44% is
  the agreement between 250 ms and 3 s judgments (how *fast* genre is grasped,
  above chance at a quarter-second), not an accuracy ceiling. Genre/timbre is
  fast and robust, so the ~5-bit **style** row stands.
- **Timbre/style is the most durable carrier.** `[SchellenbergHabashi2015]`:
  novel melodies consolidate after **two exposures with no forgetting over a
  week** in unselected listeners, and **timbre memory is durable at all delays**,
  while key and tempo fade — vindicating the master dimension `[z0m4p81q]` and
  confirming key = 0 bits and weak tempo.
- **Two evidence-based, time-conditioned haircuts** (the † and ‡ notes in §4):
  melodic-rhythm-motif (`[HebertPeretz1997]`) and contour-at-long-delay
  (`[DowlingKwakAndrews1995]`).
- **Amusia** corrected 4% → ~1.5% (`[PeretzVuvan2017]`), uneven degradation.
- **Mode affect is culture-bound** (`[Smit2022]`) — a Western-enculturated bit.

**Net:** the review's *specific* concerns were partly upheld (rhythm, contour-
over-time, amusia, culture) and partly **refuted** (style); its *aggregate*
"revise the headline to ~12–21" was a competing estimate, not evidence, and is
**not adopted**. The headline range is unchanged but now explicitly conditioned
(§5). Lesson: an adversarial panel surfaces arguments to adjudicate and verify —
not point-estimates to adopt.

**Still open** (flagged by the review, not yet resolved): the antecedent/
consequent motif engine is unbuilt; whether the consequent transformation is a
*perceptual* bit is untested (reclassify pending a study); the recognition-is-
not-cryptographic anti-claim should be surfaced at any point of trust; and the
determinism hazards (float→MIDI, modulo bias, discrete-gestalt avalanche) need
hardening.
