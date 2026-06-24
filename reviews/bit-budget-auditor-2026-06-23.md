# Bit-Budget & Determinism Auditor — entmotif DESIGN review

- **Run label:** 2026-06-23
- **Persona:** bit-budget-auditor (BIT)
- **Mode:** unattended · **Effort:** deep
- **Scope:** the headline claim that entmotif delivers ~25–50 reliably-recoverable (Model B) bits.
- **Posture:** adversarial; read-only on repo; report-only.

---

## Evidence Inventory

| Artifact | What I used it for |
|---|---|
| `docs/bit-budget.md` §3 (methodology), §4 (audited table), §5 (totals/curve), §6 (casualties), §7 (open Qs) | The claim under audit: marginal-sum total ~19–28; curve to ~50. |
| `this.i` nodes `2p8z1m40`, `k20f9a3x`, `m4z81p3v`, `81pz4m0v`, `9k3f0a72`, `c2k9p0a4`, `e9k2m4p1`, `z0m4p81q`, `3k7a92f0`, `b7p21m9z`, `8a3k0f29` | Pillars, two-layer style/lead model, analog stack, integrity, hash source, fidelity casualties. |
| `AGENTS.md` §0 (bit-budget law), §3 (entropy→music contract) | The discrete/analog law and the consumption-schedule requirement. |
| `README.md` | The *un-audited* brainstorm (16-progression list, raw question list) — useful as the un-discounted upper bound. |
| `experiments/soundfont/gen_style_midi.py`, `gen_style_midi2.py` | The actual listening-test stimuli; ground truth for what was tested and what each style's "bed" really encodes. |
| `/tmp/bitmodel.py` (this run) | My independent joint-cardinality model + modulo-bias entropy computation. |

**Note on `this.i` vs `docs/bit-budget.md` disagreement (already a finding):** `this.i:2p8z1m40` claims an 8-bar period "reaches ~25–33" and a single phrase "tops out ~17–24"; `docs/bit-budget.md` §4/§5 revises the *same* 8-bar period **down** to ~19–28 (centered low-/mid-20s) and says clearing 25 *wants the 3rd phrase*. The intent layer and the design doc now state **different numbers for the same form**. The doc is newer and lower, but the showroom (`this.i`) still advertises the optimistic v1 figure. This is a load-bearing inconsistency in the headline claim itself.

---

## Independent Bit Estimate (my own table)

I did **not** sum the doc's marginal column. I built a **top-down joint-cardinality** estimate: for each dimension I estimated the *effective number of reliably-distinct, Model-B-recoverable classes conditional on style*, took log₂, summed, then applied a **residual-correlation haircut** for the cross-dimension overlaps the doc's marginal column does not fully remove. Numbers from `/tmp/bitmodel.py`.

| Dimension | Effective distinct classes (cond. on style) | bits lo | bits hi | Why I differ from §4 |
|---|---|---:|---:|---|
| Style preset | 22 – 30 | 4.46 | 4.91 | §4 says 5–6; but §6 casualties (free-reed→1, breathy-flute→1, shakuhachi gone, aria gone, scat gone) collapse the 32 toward ~24–28 *distinct gestalts*. 6 bits needs 64 *renderable-distinct* styles — unproven. |
| Lead instrument | 2 – 3.5 | 1.00 | 1.81 | §4 says 1.5–2.5; many styles effectively imply their lead (chant→choir, ragtime→piano, sitar→sitar). The free pool conditional on style is small. |
| Mode / tonal color | 1.2 – 1.7 | 0.26 | 0.77 | §4 says 0.5–1; style largely **fixes** mode (chant=Dorian, blues=blues scale). Residual is tiny. |
| Tempo (class S) | 1.1 – 1.4 | 0.14 | 0.49 | §4 says 0.25–0.75; tempo is class **S/A** and recovering distinct tempo *classes within a style band* from memory is weak. |
| Meter residual | 1.1 – 1.4 | 0.14 | 0.49 | §4 says 0.25–0.5; style strongly implies meter (jig=6/8, polka=2/4, most=4/4). |
| Antecedent rhythm | 5 – 8 | 2.32 | 3.00 | Roughly agrees with §4 (2.5–3). |
| Contour + opening gesture | 5 – 7 | 2.32 | 2.81 | Roughly agrees with §4 (2.5–3). |
| Consequent transformation | 3 – 5 | 1.58 | 2.32 | §4 says 2–3; untrained-ear recovery of *which* transformation from memory is the weakest link in the whole table. |
| Cadence type | 2 – 3 | 1.00 | 1.58 | §4 says 0.75–1.25; "resolved vs not" is reliable, the 4-way is not. |
| Form / phrase count | 1.1 – 1.3 | 0.14 | 0.38 | Roughly agrees (≈ fixed in v1). |
| Harmonic progression | 2.5 – 4 | 1.32 | 2.00 | §4 says 1.5–2; untrained ears barely track progression *identity* from memory. |
| Groove variant | 1.3 – 1.7 | 0.38 | 0.77 | §4 says 0.5–1; groove is **part of style identity** (double count). |
| Accompaniment texture | 1.5 – 2 | 0.58 | 1.00 | Roughly agrees (0.5–1). |
| Texture-interruption | 2.5 – 4 | 1.32 | 2.00 | §4 says 1–2; but for the *novelty* style this **IS** the style (double count). |
| Key / abs. pitch | — | 0 | 0 | Agree: analog. |
| Analog stack | — | 0 | 0 | Agree: analog. |
| **Sub-total (pre-haircut)** | | **16.97** | **24.31** | |
| **Residual-correlation haircut** | | **−5** | **−3** | rhythm↔meter, contour↔transform, progression↔mode, groove↔style, texture↔style — see below. |
| **AUDITOR JOINT ESTIMATE — 8-bar period** | | **≈ 12** | **≈ 21** | vs doc §4 **19–28**. |

**Headline result:** my honest top-down estimate for the v1 8-bar period is **~12–21 bits**, centered ~16–17 — roughly **5–7 bits below** the doc's 19–28 and **8–12 bits below** the `this.i:2p8z1m40` "25–33" figure. **The 25-bit floor is *not* reached by the v1 form on an independent reckoning; it requires the 3rd-phrase extension *and* the optimistic edge of every estimate.** The ~50 ceiling is aspirational to the point of being unsupported by any current evidence.

### Why my number is lower: the marginal column still sums overlapping knobs

The doc's §3 methodology is right in principle ("score each correlated dimension by its conditional-on-style marginal"). But §4 then lists **fourteen** non-zero rows and **adds them**, and several of those marginals are not actually independent of *each other* (the audit conditioned each on **style**, but not on its sibling dimensions):

1. **rhythm ↔ meter.** The "antecedent rhythmic motif" (2.5–3) and "meter residual" (0.25–0.5) are not independent: a 6/8 jig rhythm and a 6/8 meter are the *same* perceptual fact counted twice. Over-claim ~0.3–0.5 bit.
2. **contour ↔ consequent-transformation.** The transformation (inversion/contrary-contour answer) is *defined relative to the antecedent contour*. If the contour is already counted (2.5–3), the contour-derived part of the transformation (2–3) is partly the same variance. The integrity argument (`9k3f0a72`) actually *strengthens* this: a "bound transformation" is by construction correlated with what it transforms. Over-claim ~1–1.5 bits.
3. **progression ↔ mode.** Major/minor mode and the I–IV–V vs i–VI–III progression family co-vary (a minor mode constrains the progression set). Counting mode (0.5–1) **and** progression (1.5–2) double-books their shared part. Over-claim ~0.5–1 bit.
4. **groove ↔ style** and **texture-interruption ↔ style.** `this.i:z0m4p81q` explicitly says "the groove+timbre **bed** carries identity BEFORE any melody" — i.e. groove *is* how you recognize the style. Counting style (5–6) and *then* groove (0.5–1) is the textbook double-count the methodology promised to remove. Likewise `f3a0k9m2` says the texture-interruption is *itself the novelty style* — so for that style it is counted in both the style row and the interruption row. Over-claim ~0.8–1.5 bits.
5. **lead ↔ style.** `c2k9p0a4`'s own logic ("lead yield is style-dependent, ~log₂ effective allowed-pool") means the gross lead bits (b7p21m9z's "~4 bits before gating") are *mostly absorbed by style*; the 1.5–2.5 residual is plausibly nearer 1–1.8.

Summed, the residual double-counting the §4 marginal column did **not** remove is **~3–5 bits** — exactly my haircut, and exactly the gap between the doc's 19–28 and my 12–21.

### Numeric modulo-bias result

From the model: reading **exactly log₂(m) bits** for a non-power-of-two option count is meaningfully biased — e.g. 5 bits over 24 styles concentrates 25% of mass on the low half (entropy loss ~0.085 bit on that one choice, and a *systematic* skew toward low-index styles across every such decision). Reading **8 bits per choice** drops the loss below 0.002 bit. The fix is trivial (over-read or use rejection sampling) but it is **unspecified** and the schedule does not yet exist, so the current design is silent on it. The cumulative skew across ~14 modulo reads is the concern, not any single one.

---

## Executive Summary

**The 25–50-bit headline does not survive an independent top-down audit of the v1 form.** Building my own joint-cardinality estimate (log₂ of distinct *whole* motifs, not the sum of per-knob marginals) lands the 8-bar period at **~12–21 reliable Model-B bits, centered ~16–17** — about 5–7 bits below `docs/bit-budget.md` §4's 19–28 and 8–12 below `this.i:2p8z1m40`'s "25–33," because the §4 marginal column still sums dimensions that share perceptual variance with *each other* (rhythm↔meter, contour↔consequent-transformation, progression↔mode) and with *style* (groove, texture-interruption, lead), totalling ~3–5 bits of residual double-counting the audit's "condition-on-style" pass never removed. The **25-bit floor is therefore reached only by the 3rd-phrase extension at the optimistic edge of every estimate**, and **~50 is unsupported by any current evidence**; both the design doc and the intent file should be revised down and reconciled (they currently disagree). The **consumed≠delivered** logic is sound *in direction* but its collision-probability claim (`~2^-consumed`) is **overstated**: machine-collision floor is bounded by the *effective* entropy actually injected into the canonical MIDI, and the analog stack (`e9k2m4p1`) — counted on for most of the consumed bits — perturbs only analog parameters that may be **quantized away** in the deterministic MIDI, so consumed≈delivered+a-modest-margin, not 120–180. Finally, **two real determinism hazards are unaddressed** (tempo float-rounding into MIDI tempo bytes; modulo bit-reader bias toward low-index options), and **avalanche on the *discrete* gestalt is unquantified** — if discrete choices read from an early fingerprint slice, two inputs can share the entire remembered gestalt while differing only in the analog (non-recoverable) layers.

---

## Top Findings (ordered by bang-for-buck)

### F1 — §4 marginal column still double-counts ~3–5 bits across siblings, not just vs style — total over-claimed
- **Location:** `docs/bit-budget.md` §4 (whole table) / §3 methodology / `this.i:c2k9p0a4`, `z0m4p81q`
- **Severity:** HIGH · **Confidence:** LIKELY
- **Finding:** The methodology promises to remove shared variance by conditioning each dimension on **style**, but §4 then *adds* fourteen marginals that also overlap **each other**: rhythm↔meter, contour↔consequent-transformation (the "bound transformation" is *defined* relative to the contour — `9k3f0a72` guarantees the correlation), progression↔mode, and groove/texture-interruption/lead↔style. My independent joint estimate is ~12–21 vs the doc's 19–28.
- **Evidence:** `/tmp/bitmodel.py` joint sub-total 16.97–24.31 minus a 3–5-bit residual-correlation haircut → 12–21; the haircut equals the §4↔auditor gap. `z0m4p81q` itself says groove "carries identity BEFORE any melody" (= style recognition), yet groove is a separate row.
- **Recommended action:** Re-derive §4 as an explicit joint cardinality (log₂ of distinct whole motifs) with a conditional-probability model, not an additive table; or add a documented pairwise-correlation discount between sibling dimensions. Re-state the total as ~12–21 for v1.

### F2 — The 25-bit floor is not reached by the v1 8-bar form; this.i and the doc disagree — overclaimed
- **Location:** `this.i:2p8z1m40` ("8-bar … ~25–33") vs `docs/bit-budget.md` §5 ("~19–28 … clearing 25 wants the 3rd phrase") and my §-estimate (~12–21)
- **Severity:** HIGH · **Confidence:** LIKELY
- **Finding:** The headline "~25–50" is carried in two places with **different numbers for the same form**, and *both* are above my independent estimate. On my reckoning the v1 period clears 25 only with the 3rd-phrase extension *and* optimistic edges everywhere. The showroom (`this.i`) still advertises the retired v1 figure.
- **Evidence:** direct quotes above; `2p8z1m40` even says a 4-bar phrase "tops out ~17–24" while §5 says ~14–20 — the same downward revision was applied to the doc but not the intent file.
- **Recommended action:** Reconcile `this.i:2p8z1m40` to the doc's lower figures (the maintainer writes `this.i`, per orchestrating §5). Re-frame the headline as "~15–25 reliable for v1, ~25–40 with the 3rd phrase, 50 aspirational," and make clear 25 is a *stretch* v1 goal.

### F3 — consumed≈delivered, not 120–180: analog-stack bits may be quantized out of the canonical MIDI — overclaimed
- **Location:** `docs/bit-budget.md` §2 / `this.i:e9k2m4p1`, `2p8z1m40`
- **Severity:** HIGH · **Confidence:** LIKELY
- **Finding:** §2 claims ~120–180 *consumed* bits give a machine-collision floor of ~`2^-consumed`. But the collision floor is set by the **effective entropy actually distinguishing two canonical MIDIs**, which is bounded by the number of *distinct quantized MIDI parameters*, not the number of fingerprint bits *read*. If the analog stack modulates velocity/timing/CC "within perceptual tolerance" and those land on a coarse MIDI grid (velocity 0–127, tick resolution, a handful of CC values), many of the consumed bits collapse to the *same* MIDI bytes. Two inputs sharing all discrete choices could then produce **byte-identical or near-identical** MIDI despite differing fingerprints — undercutting both the avalanche promise (F5) and the `2^-consumed` claim.
- **Evidence:** `e9k2m4p1` lists the analog layers as the source of "EXTRA fingerprint bits, so the rendered MIDI reflects more of the whole input" — but a 7-bit velocity perturbed "within tolerance" injects ≤ a few bits, not the dozens implied; the MIDI is the deterministic surface, so anything not landing on a distinct MIDI value is *not consumed in effect*.
- **Recommended action:** Define "consumed" as **distinct-MIDI-determining** bits and compute the *effective* consumed count from the actual MIDI parameter resolutions (sum of log₂ distinct values each analog layer can write). Expect a number far below 120–180; revise §2's collision-floor claim accordingly, or accept it explicitly as "machine-rare relative to delivered," dropping the specific exponent.

### F4 — Tempo and timing float-rounding can leak non-entropy state into canonical MIDI — nondeterministic
- **Location:** `AGENTS.md` §1 (determinism) / `this.i:81pz4m0v`, `4m1zp870` / `docs/bit-budget.md` §4 tempo row
- **Severity:** MEDIUM · **Confidence:** LIKELY
- **Finding:** MIDI tempo is stored as integer microseconds-per-quarter (`60_000_000 / bpm`, see both generator scripts using `int(...)`). If tempo, swing depth, rubato, or micro-timing are computed in floating point and then truncated to int ticks/µs, the **rounding mode and float representation can differ across platforms/Python builds**, producing different canonical MIDI bytes for the same input. `4m1zp870` requires byte-identical MIDI everywhere; the design has not pinned integer-only arithmetic or a rounding rule.
- **Evidence:** `experiments/soundfont/gen_style_midi.py:29` `int(60_000_000 / bpm)` and `gen_style_midi2.py:24` same — float division then `int()` truncation; the analog stack (`e9k2m4p1`) explicitly modulates "micro-timing/swing depth/rubato," all prime float candidates.
- **Recommended action:** Mandate integer-domain arithmetic for every value written to MIDI (compute ticks/µs with integer math or a fixed quantization with a specified rounding rule), and add a determinism golden test (the "songbook" in `4m1zp870`) that runs on ≥2 platforms.

### F5 — Avalanche on the *discrete* gestalt is unquantified; discrete choices may read an early fingerprint slice — overclaimed
- **Location:** `this.i:81pz4m0v` (avalanche), `m4z81p3v` (Model B), `e9k2m4p1` / `docs/bit-budget.md` §7
- **Severity:** MEDIUM · **Confidence:** SPECULATIVE
- **Finding:** AGENTS §3 / `81pz4m0v` claim "one-char change ⇒ clearly different motif," but the *recoverable* difference is only the **discrete** gestalt (`k20f9a3x`). If the schedule reads discrete choices from a small early slice of the fingerprint and spends the long tail on the analog stack, two inputs whose fingerprints differ only outside that slice share **every Model-B-recoverable bit** — the motifs are *recognition-collisions* even though the MIDI differs in analog nuance. Avalanche on the analog layers is real (casual), but avalanche on the *delivered* bits is exactly the delivered-collision rate (~`2^-15..21` by F1), not `2^-consumed`.
- **Evidence:** `e9k2m4p1` design rule: "every discrete choice sets a BASE value; a stack of analog layers then modulates … each drawing fresh fingerprint bits" — i.e. discrete choices are read first/early, analog later. SHA-512 is itself avalanche-good, so the *fingerprint* differs everywhere; the question is whether the **discrete decode** of it differs.
- **Settling experiment:** Once a schedule exists, compute the discrete-gestalt over a corpus of single-character-mutated inputs and measure the rate at which the *discrete* class vector is unchanged. Target: ≪ `2^-(delivered bits)`. Until then, do not claim discrete avalanche.
- **Recommended action:** Specify that **every discrete decision draws from a whitened full-width fingerprint** (e.g. independent HKDF/counter-mode expansions, not sequential prefix slices), so each discrete choice depends on all 512 bits. Add this as a `this.i` constraint.

### F6 — Modulo over non-power-of-two option counts skews toward low-index options — overclaimed (mildly), and unspecified
- **Location:** `docs/bit-budget.md` §7 (bit-reader bias open Q) / `AGENTS.md` §3 schedule / `this.i:d4m1z8p0` (~24–32 styles, non-power-of-two)
- **Severity:** LOW · **Confidence:** CONFIRMED (arithmetic)
- **Finding:** Style (~24–32), progression (~16–17), and most option sets are non-powers-of-two. Reading exactly log₂(m) bits and taking `mod m` concentrates mass on low-index options (style "5 bits / 24" → 25% excess mass on the low half, ~0.085-bit entropy loss on that choice). Cumulative over ~14 modulo reads, this is a systematic skew that *reduces effective delivered entropy* and biases the output toward whichever styles/progressions sit early in the list.
- **Evidence:** `/tmp/bitmodel.py`: loss(5 bits/24)=0.085, loss(5 bits/17 prog)=0.025; both fall below 0.002 at 8 bits per choice.
- **Recommended action:** Specify **rejection sampling** or **over-read ≥ log₂(m)+3 bits** per modulo decision in the schedule. Cheap to mandate now; impossible to retrofit cleanly into a frozen schedule later.

### F7 — Style "5–6 bits" assumes 32/64 *renderable-distinct* styles, but §6 casualties already collapsed the inventory — overclaimed
- **Location:** `docs/bit-budget.md` §4 style row + §6 casualties / `this.i:z0m4p81q`, `b7p21m9z`, `8a3k0f29`, `q9f3a7k2`
- **Severity:** MEDIUM · **Confidence:** LIKELY
- **Finding:** The 5-bit style claim needs 32 *pairwise-distinct-through-the-pinned-font* gestalts; the 6-bit ceiling needs 64. But §6 already retired aria, scat, shakuhachi, and collapsed the free-reed trio and breathy-flute pair to one slot each — and only ~13 styles have *validated* mutual distinctiveness (the listening batches). The effective distinct-gestalt count is plausibly ~24–28, i.e. **~4.6–4.8 bits, not 5–6**, and 64 is entirely unvalidated.
- **Evidence:** §6 explicit casualty list; the two generator scripts together render exactly 13 styles (7 + 6, minus the aria which `q9f3a7k2` then drops → 12 surviving validated). `/tmp/bitmodel.py`: log₂(24)=4.585, log₂(28)=4.807.
- **Settling experiment:** A pairwise-confusion A/B/X study over the *full* proposed inventory (not just the 12 sketched) to count truly-distinct gestalts. The style row is the single largest term, so this study moves the total most.
- **Recommended action:** Cap the claimed style yield at log₂(*validated-distinct count*); treat the path from ~25 to 64 styles as unclaimed until a confusion study exists. **This is the single change that most affects the total** (per the deep-mode mandate): style is the largest single row and gates the others, so trimming it ~0.5–1.4 bits and re-baselining the gated rows on the smaller inventory propagates through the whole table.

---

## Residual Unknowns (honest)

- **All `D` marginal yields are pre-empirical** (§7 admits this). My estimate is *also* an estimate — adversarially lower, but only an A/B/X recognition study settles the absolute numbers. I have flagged the two studies that move the total most (F5 discrete-avalanche corpus; F7 style-confusion study).
- **Memory decay over time** (`§7`): every yield assumes near-immediate recognition. Decay would erase the low-yield rows (cadence, mode, tempo, meter, groove) first — i.e. it attacks exactly the rows that pad the total from ~17 to ~28. Out of my lens (ACA/AUD own it) but it makes my low end the more honest one.
- **Whether the schedule reads discrete-first** (F5) is unknowable until the schedule is written; my finding is conditional on the `e9k2m4p1` design rule, which strongly implies it.
- **Effective consumed bits** (F3) cannot be computed without the MIDI parameter-resolution table; I bounded it qualitatively.

---

```yaml
findings:
  - id: BIT-F1
    persona: bit-budget-auditor
    title: §4 marginal column still double-counts ~3-5 bits across sibling dimensions, not just vs style
    severity: HIGH
    confidence: LIKELY
    location: docs/bit-budget.md §4
    dedupe_key: bit-budget-double-counted
    recommended_disposition: recommend-fix
    rationale: Joint-cardinality re-derivation lands ~12-21 vs the additive 19-28; the gap equals un-removed sibling correlations (rhythm/meter, contour/transformation, progression/mode, groove+texture+lead/style).
    revisit_condition: null
    fix_effort: medium
    settling_experiment: A/B/X recognition study estimating conditional (joint) distinct-whole-motif counts rather than per-knob marginals.
  - id: BIT-F2
    persona: bit-budget-auditor
    title: 25-bit floor not reached by v1 8-bar form; this.i and bit-budget.md state different numbers
    severity: HIGH
    confidence: LIKELY
    location: this.i:2p8z1m40
    dedupe_key: bit-budget-overclaimed
    recommended_disposition: recommend-fix
    rationale: this.i advertises "25-33" for the 8-bar period; the doc revised the same form to "19-28, wants 3rd phrase"; my independent estimate is ~12-21. Reconcile and revise the headline down.
    revisit_condition: null
    fix_effort: small
    settling_experiment: null
  - id: BIT-F3
    persona: bit-budget-auditor
    title: consumed bits approx delivered, not 120-180 - analog-stack bits quantize out of canonical MIDI
    severity: HIGH
    confidence: LIKELY
    location: docs/bit-budget.md §2
    dedupe_key: analog-stack-overclaimed
    recommended_disposition: recommend-fix
    rationale: The 2^-consumed collision floor is bounded by distinct-MIDI-determining bits; analog modulation "within tolerance" lands on a coarse MIDI grid, so effective consumed is far below the claimed 120-180.
    revisit_condition: null
    fix_effort: medium
    settling_experiment: Compute effective consumed = sum of log2(distinct MIDI values each analog layer can write) from the actual parameter-resolution table.
  - id: BIT-F4
    persona: bit-budget-auditor
    title: Tempo/timing float-rounding can leak platform state into canonical MIDI bytes
    severity: MEDIUM
    confidence: LIKELY
    location: this.i:4m1zp870
    dedupe_key: spec-nondeterministic
    recommended_disposition: recommend-fix
    rationale: MIDI tempo is int(60e6/bpm); float division + truncation plus float swing/rubato can differ across platforms, breaking the byte-identical-MIDI invariant.
    revisit_condition: null
    fix_effort: small
    settling_experiment: null
  - id: BIT-F5
    persona: bit-budget-auditor
    title: Discrete-gestalt avalanche unquantified; discrete choices may read an early fingerprint slice
    severity: MEDIUM
    confidence: SPECULATIVE
    location: this.i:81pz4m0v
    dedupe_key: fingerprint-overclaimed
    recommended_disposition: recommend-fix
    rationale: Avalanche on the recoverable (discrete) gestalt, not just analog nuance, is the load-bearing claim; e9k2m4p1's design rule implies discrete-first reads, which would let inputs share every delivered bit.
    revisit_condition: null
    fix_effort: small
    settling_experiment: Over a corpus of single-char-mutated inputs, measure the rate at which the discrete class vector is unchanged; require each discrete choice to draw from a whitened full-width fingerprint expansion.
  - id: BIT-F6
    persona: bit-budget-auditor
    title: Modulo over non-power-of-two option counts skews toward low-index options
    severity: LOW
    confidence: CONFIRMED
    location: docs/bit-budget.md §7
    dedupe_key: spec-nondeterministic-modulo
    recommended_disposition: recommend-fix
    rationale: Reading exactly log2(m) bits mod m concentrates ~25% excess mass on low-index styles/progressions (0.085-bit loss/choice at 5 bits/24); cumulative over ~14 reads. Fix = rejection sampling or over-read.
    revisit_condition: null
    fix_effort: small
    settling_experiment: null
  - id: BIT-F7
    persona: bit-budget-auditor
    title: Style 5-6 bits assumes 32/64 renderable-distinct styles, but fidelity casualties already collapsed the inventory
    severity: MEDIUM
    confidence: LIKELY
    location: docs/bit-budget.md §6
    dedupe_key: style-overclaimed
    recommended_disposition: recommend-fix
    rationale: Only ~12 styles have validated mutual distinctiveness; casualties collapsed several; effective distinct count ~24-28 (~4.6-4.8 bits, not 5-6), and 64 is unvalidated. Largest single row, so trimming it moves the total most.
    revisit_condition: null
    fix_effort: medium
    settling_experiment: Pairwise-confusion A/B/X study over the full proposed inventory to count truly-distinct style gestalts.
```
