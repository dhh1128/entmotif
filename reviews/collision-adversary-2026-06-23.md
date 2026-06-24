# Collision Adversary — Adversarial Design Review

- **Persona:** collision-adversary (ADV)
- **Run label:** 2026-06-23
- **Mode:** unattended, effort=deep
- **Scope:** the *promise* of entmotif — that two different inputs produce motifs an
  ordinary listener can tell apart **from memory** (Model B `[m4z81p3v]`). No code
  exists; this attacks the design's claims and reasoning.
- **Stance:** I am the attacker. I choose inputs freely, grind many candidates
  offline, compute each motif (free — the schedule is deterministic and public),
  and win if a victim who memorized the legitimate motif **accepts a
  different-input motif** as "the one I remember."

> **Audio caveat (binding).** I cannot hear audio. I rendered the constructed pair
> through the pinned soundfont (GeneralUser GS, FluidSynth) and reason from note
> data and design logic. **Every claim that a constructed pair is actually
> confusable *by ear* is marked `confidence: SPECULATIVE` and flagged for human
> listening.** I do not assert I heard anything.

---

## Evidence Inventory

| Source | What I took from it |
|---|---|
| `this.i:m4z81p3v` (Model B) | Success = recognition from memory; **no side-by-side replay**. This is the attacker's gift: the victim's reference is a decayed memory, not the bytes. |
| `this.i:k20f9a3x` (discrete/analog law) | Only discrete decisions carry recoverable bits. **The attacker only has to match discrete classes**; analog layers are free to diverge. |
| `this.i:9k3f0a72` (whole-motif integrity) | The one defense aimed squarely at me: the late bound transformation is supposed to make recognition "run to the END." I attack whether memory actually retains it. |
| `this.i:e9k2m4p1` (analog stack) | Design claims the analog stack adds avalanche + consumed bits. **It carries zero Model-B recall bits by its own admission**, so it does not raise *my* collision cost. |
| `this.i:81pz4m0v` (hash-first) | Schedule is a deterministic public function of `SHA-512(normalized text)`. I can compute every candidate's full discrete-class vector offline at hash speed. |
| `docs/bit-budget.md` §2,§4,§5,§7 | Delivered budget ~19–28 (additive); §7 explicitly lists "adversarial collision" as an open question. This is my attack-surface size. |
| `reviews/bit-budget-auditor-2026-06-23.md` (BIT-F1/F2) | **Independent re-derivation lands ~12–21 reliable bits** — lower than the doc's 19–28. I use 12–21 as the honest surface and 19–28 as the optimistic edge. |
| `reviews/bit-budget-auditor-2026-06-23.md` (BIT-F3) | Analog-stack "consumed" bits quantize out of the coarse MIDI grid → confirms the analog stack does not even raise the *machine* collision floor as claimed, let alone Model B. |
| `reviews/bit-budget-auditor-2026-06-23.md` (BIT-F6) | Modulo over non-2^k option counts concentrates ~25% excess mass on low-index options → denser grind target. |
| `reviews/music-perception-academic-2026-06-23.md` (ACA-F1,F2,F4) | Contour/rhythm decay faster than interval over filled delays; **no evidence untrained listeners recover a late theoretic transformation from memory** → the integrity defense's perceptual premise is unsupported. This is the load-bearing external citation for my ignorable-tail attack. |
| `experiments/soundfont/gen_style_midi2.py`, `render_test.sh`, `sf/` | The zero-dependency MIDI harness + FluidSynth + both fonts. I used these to build and render the constructed pair. |

---

## Threat Model (as used)

- **Attacker capability:** offline, unlimited grind. Computing a candidate motif =
  one SHA-512 + a deterministic table walk. ~10^7 candidates/minute on a laptop is
  conservative. The attacker sees the *full* discrete-class vector of every
  candidate, not a lossy memory.
- **Victim capability (two profiles):**
  - **First-time / careful victim:** attends to the whole motif, including the
    consequent. Must be fooled across the *entire delivered budget*.
  - **Habituated victim (the realistic one, per persona threat model):** recognizes
    the **opening gestalt + style** and stops scrutinizing. Must be fooled only on
    the *memorable subset*.
- **Win condition:** victim accepts a motif derived from an input the attacker
  chose (e.g. a look-alike key/address) as the legitimate one.
- **Out of scope (and why it doesn't save the design):** the input-side
  "identical-opening" attack (forcing two inputs to share fingerprint prefix) is
  cryptographically hard — `this.i:9k3f0a72` says so correctly. **I do not need
  it.** I attack the *perception* side: I grind for inputs whose *motifs* share the
  remembered gestalt, which is cheap precisely because the remembered gestalt is
  only ~12–21 bits wide.

---

## Collision-Cost Calculation

Let **N** = delivered (human-recoverable) bits. A Model-B collision is a
**second-preimage**: the attacker has a fixed target motif (the one the victim
memorized) and grinds inputs until one lands in the same recognition cell. Cost
≈ `2^N` candidates. A birthday collision (any two of the attacker's own inputs
colliding) is `2^(N/2)` — relevant if the attacker controls both sides (e.g.
seeding a memory then swapping).

Using the **BIT-audited 12–21** (honest) and the **doc's 19–28** (optimistic edge):

| N (delivered bits) | Birthday `2^(N/2)` | **Second-preimage `2^N`** | Attacker verdict |
|---|---|---|---|
| 12 | 64 | **4,096** | trivial (sub-second) |
| 15 | 181 | **32,768** | trivial |
| 17 | 362 | **131,072** | trivial |
| 19 | 724 | **524,288** | trivial |
| 21 | 1,448 | **2,097,152** | trivial (~0.2 s of grind) |
| 24 | 4,096 | **16,777,216** | trivial (seconds) |
| 28 | 16,384 | **268,435,456** | easy (minutes) |

**Headline:** at *every* point in the budget range, a Model-B second-preimage is
within trivial reach of an offline attacker. There is no operating point in the
design where the collision cost is cryptographically meaningful — nor is one
claimed (`this.i:m4z81p3v` explicitly relaxes collision resistance). The finding
is not "the math is wrong"; it is that **the design markets a ~25–50-bit
"fingerprint" whose adversarial collision cost is ~2^12–2^28, and that gap is not
surfaced anywhere a user deciding to *trust* a motif would see it.**

### The habituated-victim cost (the cheap attack)

Against a habituated victim, the attacker need only match the **memorable subset**
— style + lead timbre + opening gesture/contour + antecedent rhythm + happy/sad
affect — and let everything else diverge. Summing the optimistic §4 yields for
*only those rows*:

```
style (effective ~4.7)                 4.7
lead instrument                         2.0
opening gesture + antecedent contour    3.0
antecedent rhythm                       2.8
mode (happy/sad affect)                 0.7
------------------------------------------
MEMORABLE-SUBSET total              ~13.2 bits
   second-preimage  ~2^13.2 = ~9,400 candidates
   birthday         ~2^6.6  = ~97 candidates
```

**~9,400 offline computations to fool a habituated victim.** That is not an
attack budget — it is a rounding error. And this *over-estimates* the work,
because (a) BIT's audit says the real per-row yields are lower, and (b) modulo
clustering (below) shrinks the effective space further.

---

## Executive Summary

entmotif's core promise — "two different inputs reliably sound different to a
human" — is **true for honest accidents and false against an adversary**, and the
design does not draw that line where a trusting user can see it. The recoverable
budget the bit-budget auditor lands at (~12–21 bits) is the *entire* attack
surface, so a Model-B second-preimage costs ~2^12–2^21 offline motif computations
— trivially grindable. Against the realistic **habituated** victim, the attacker
need match only the memorable subset (~13 bits → **~9,400 tries**).

The one defense aimed at me — **whole-motif integrity** `[9k3f0a72]`, the "no
ignorable tail" rule — rests on a perceptual premise the music-perception academic
independently rejected (ACA-F4): untrained listeners do **not** recover a late,
theory-defined transformation from memory. I **constructed a pair** (rendered,
byte-distinct MIDI and WAV) that shares the entire antecedent and diverges only in
the consequent's transformation and cadence — exactly the case the integrity
constraint claims to kill. Whether it fools the *ear* is SPECULATIVE and flagged
for a listening study, but the *design logic* that it would block acceptance is
unsupported.

The **analog stack** `[e9k2m4p1]` is, by the design's own discrete/analog law,
irrelevant to my cost: it carries zero recall bits, so the attacker simply ignores
it (and BIT-F3 shows it barely raises even the *machine* floor). Finally,
**modulo/affinity clustering** concentrates outputs on low-index, high-affinity
choices, shrinking the effective space below nominal and handing me a denser target
region. Cheapest-first findings follow.

---

## Top Findings (cheapest attacks first)

### ADV-F1 — Habituated-victim second-preimage costs ~2^13 (the cheapest real attack) · CRITICAL · LIKELY
**`dedupe_key: fingerprint-grindable`**

The design's own threat-relevant victim is habituated: recognizes opening + style,
ignores the tail. The attacker grinds inputs whose motifs match *only* the
memorable subset (~13 bits, computed above) → **~9,400 offline computations** for a
second-preimage, ~97 for a birthday pair. This is the load-bearing finding: it is
the cheapest path and it directly defeats the headline promise for the most common
usage pattern (a user who has "heard this key's tune before"). Cost is anchored in
the §4 optimistic yields restricted to memorable rows; the real number is *lower*
given BIT-F1's audit. **Bang: maximal** — cheapest attack × kills the core promise.

*Settling experiment:* A/B/X recognition study where lures match style + opening +
rhythm but diverge in consequent + analog stack, tested on habituated listeners at
≥1-day delay; measure acceptance (false-alarm) rate. If FA is high, this is
CONFIRMED.

### ADV-F2 — Whole-motif integrity does not block the ignorable-tail attack under Model B · HIGH · SPECULATIVE
**`dedupe_key: transformation-collidable`** (semantic sibling of ACA's
`transformation-unsupported`)

`this.i:9k3f0a72` and §4 (consequent-transformation row, 2–3 bits) claim the late
bound transformation makes recognition run to the end, killing the
"identical-opening, late-divergence" attack on the *perception* side. **I
constructed exactly that pair** (see Constructed Pairs): identical antecedent
(bars 1–4: opening gesture, contour, rhythm, mode, lead timbre, style bed),
divergent consequent (target = contrary-contour answer + authentic cadence; lure =
sequence-up answer + deceptive cadence). The MIDI and WAV are byte-distinct, so
Model-A side-by-side divergence genuinely exists — but Model B is *not*
side-by-side. ACA-F4 (Edworthy 1985; no evidence untrained listeners recover a late
theoretic transformation from memory) is the independent perceptual basis that this
divergence is **not part of the remembered gestalt** for the target population.
Consequence: the consequent-transformation row should be reclassified from a
recoverable bit source to **integrity-only/0 perceptual bits** until a study shows
otherwise, and the design must stop counting it as an attacker cost. **Marked
SPECULATIVE on ear-confusability — flagged for human listening.**

*Settling experiment:* 2AFC, target vs lure identical for bars 1–4 differing only
in the consequent, untrained listeners, ≥1 day later. If d′≈0, the integrity
defense is perceptually inert and this becomes CONFIRMED.

### ADV-F3 — The analog stack does NOT raise Model-B collision cost; the attacker ignores it · HIGH · CONFIRMED
**`dedupe_key: analog-stack-overclaimed`** (shared with BIT-F3)

`this.i:e9k2m4p1` lists three benefits of the analog stack; **none raises my
cost.** (1) Model-A distinguishability — irrelevant; the victim has no side-by-side
reference. (2) Casual avalanche on analog layers — irrelevant; the attacker is not
relying on accidental similarity, they are *constructing* it on the discrete
dimensions and are happy to let the analog layers diverge arbitrarily. (3)
Consumed-bit margin pushing machine collisions to ~2^-consumed — BIT-F3 shows the
analog modulation quantizes onto a coarse MIDI grid, so effective consumed is far
below the claimed 120–180; but even granting it, **machine collision resistance is
not Model-B collision resistance.** By the design's own discrete/analog law
`[k20f9a3x]`, analog dimensions carry zero recall bits, so they contribute **0** to
N and **0** to my second-preimage cost. This is CONFIRMED by the design's internal
logic: the doc cannot simultaneously claim analog layers carry no recoverable bits
*and* that they harden recognition collisions. The "consumed >> delivered" margin
protects the machine diff, never the human.

*Settling experiment:* none needed for the logical claim. To quantify (3),
compute effective consumed = Σ log2(distinct MIDI values each analog layer writes)
from the parameter-resolution table (same experiment BIT-F3 requests).

### ADV-F4 — Modulo bias + affinity weighting cluster outputs, shrinking the effective space below nominal · MEDIUM · LIKELY
**`dedupe_key: progression-grindable`** (relates to BIT-F6 `spec-nondeterministic-modulo`)

Two compounding clusterings shrink my target space below the nominal budget:
(a) **Modulo over non-power-of-two option counts** (§7, confirmed in BIT-F6)
concentrates ~25% excess probability mass on low-index options for every non-2^k
read (styles=32 is fine, but progression family, cadence type, mode variant,
lead-from-pool, meter residual are not powers of two). Across ~10 such reads this
is ~0.85 bit of effective shrink, *and* it tells the attacker **which region is
densest** — grind toward low-index choices and you collide with a
disproportionate share of victims. (b) **Affinity weighting** in the two-layer
style↔lead model `[c2k9p0a4]` deliberately makes a style's *signature* instruments
common and weird ones rare — so the realistic output distribution is even more
concentrated on signature combos than the log2(pool) figure suggests. The
attacker grinds the high-affinity, low-index mode of the distribution and matches
a larger fraction of real victims per try. **The nominal 12–21 bits overstates the
effective entropy an attacker faces.**

*Settling experiment:* over a large input corpus, render the discrete-class
vector and measure the empirical entropy H(class-vector); compare to the nominal
budget. Gap = the clustering discount available to the attacker. Also confirms
whether rejection sampling (BIT-F6's fix) closes part (a).

### ADV-F5 — Style is the master dimension AND the most grindable channel · MEDIUM · LIKELY
**`dedupe_key: style-grindable`** (relates to `style-overclaimed` in BIT-F7/ACA-F5)

`this.i:z0m4p81q` makes style the strongest, most memorable Model-B hook — which
makes it the **highest-value, easiest-to-match** channel for me. It is a single
~5-bit (BIT-F7/ACA-F5 say effective ~4.6–4.8, and fewer once fidelity casualties
collapse the inventory) discrete pick that the victim weights most heavily. Match
style + lead and a habituated victim is already ~7 bits of the way to acceptance.
Because non-musicians are "expert genre classifiers," matching style buys
disproportionate acceptance per bit — the design's strength is my cheapest lever.
The remedy is not to weaken style (it is genuinely memorable) but to stop treating
the *sum* of dimensions as the attacker's cost when one dimension dominates
recognition: the effective recognition decision is closer to
`style ∧ opening-gesture` than to the full vector.

*Settling experiment:* ablation listening study — hold style+opening fixed, vary
everything else; measure how often the victim still accepts. High acceptance ⇒
effective N for recognition is far below the budgeted N.

### ADV-F6 — Recognition decays over time, shrinking N (and my cost) the longer the gap · MEDIUM · LIKELY
**`dedupe_key: fingerprint-decays-over-time`** (relates to ACA-F1/F2 decay
findings)

The collision cost `2^N` assumes a fixed N, but ACA-F1/F2 show contour and rhythm
decay faster than interval-in-tonality over filled delays, and §7 flags
memorability decay as untested. **N is not constant — it shrinks with the
memory-to-check interval.** The realistic Model-B check happens minutes-to-days
after exposure, by which point the low-yield dimensions (cadence, transformation,
mode-via-affect, fine rhythm) have eroded, leaving roughly style + gross contour
+ timbre. My cost falls accordingly: a check at +1 week may face only ~7–9
effective bits → second-preimage ~2^7–2^9 (**hundreds**). The budget should be
quoted as a *decay curve*, and the adversarial cost quoted at the **weakest
(longest-delay) point**, not the fresh-exposure peak.

*Settling experiment:* the A/B/X recognition study run at 10 min / 1 day / 1 week
(Schellenberg & Habashi 2015 paradigm); fit N(t). Quote adversarial cost at the
intended check interval.

### ADV-F7 — The design does not surface the adversarial-collision boundary to a trusting user · MEDIUM · LIKELY
**`dedupe_key: spec-missing`**

`this.i` and `docs/bit-budget.md` are honest that this is recognition-not-crypto
(`m4z81p3v`, AGENTS.md §0.2) — but that disclaimer lives in design docs, not where
a user *decides to trust a motif*. The whole point of entviz/entmotif is that a
human uses the artifact to **judge whether two values match**; if that human treats
"the tune sounds right" as evidence the key/address is genuine, the ~2^13–2^21
collision cost is a security-relevant fact they never see. The design should record
an explicit **non-goal/anti-claim** (e.g. "a matching motif is NOT evidence of a
matching input against an adversary; use Model A / byte comparison for
trust-bearing checks") and propagate it to any UI. This is the gap between "honest
in the spec" and "safe in the hand."

*Settling experiment:* none — this is a design-disclosure decision for the
maintainer to record in `this.i`.

---

## Constructed Pairs

**Seed: `ignorable-tail` near-collision (ADV-F2).** Reproduced by the generator
below (kept out-of-repo per the read-only constraint; paste into
`experiments/soundfont/` to regenerate). Renders verified on 2026-06-23:

```
pair_target.mid  md5 a8a4272fbe23210dbd7f3668500f5cad
pair_lure.mid    md5 c7b563fb157cb9799cae87c53b98d496   (distinct inputs ✓)
pair_target.wav  md5 4e4a7219792120a3f597058eaed4da54
pair_lure.wav    md5 09a8c876a261095cc1f10dd2a261ba62   (Model-A divergence exists ✓)
```

Construction (models the *threat*, not the unbuilt renderer):
- **Shared (the remembered gestalt):** rock-ballad bed (piano arp + finger bass +
  strings pad + slow backbeat), overdriven-guitar lead (GM prog 29), tempo 72,
  C–G–Am–F antecedent harmony, and a **byte-identical antecedent lead** for bars
  1–4 (opening gesture `G→C` rising, the arch contour, the rhythm, the half-cadence
  "question" ending on B).
- **Divergent (the "ignorable tail"):** bars 5–8 only.
  - *target* consequent: contrary-contour descending answer, Am–F–G–C, authentic
    resolution to C.
  - *lure* consequent: sequence-up climbing answer, Am–Dm–G–F, deceptive
    non-resolution on A/F.

This is precisely the configuration `this.i:9k3f0a72` claims to defeat. The pair is
**CONFIRMED distinct as inputs and as audio (Model A)**; whether a habituated
listener **confuses them from memory (Model B)** is **SPECULATIVE — needs human
listening** (the 2AFC study in ADV-F2). I did not and cannot assert I heard them as
confusable.

<details><summary>Regeneration script (zero-dependency, mirrors the harness)</summary>

The generator that produced the seed is `/tmp/entmotif-adv/gen_collision_pair.py`
on this machine. It uses only `struct` (same raw-SMF approach as
`gen_style_midi2.py`), writes `pair_target.mid` / `pair_lure.mid`, and is rendered
with `experiments/soundfont/render_test.sh` against
`sf/GeneralUser-GS.sf2`. To adopt as a permanent regression seed, the maintainer
should commit it under `experiments/soundfont/` (out of my write scope here).

</details>

---

## Residual Unknowns

- **Ear-confusability is unproven.** Every "fools the victim" claim is gated on the
  A/B/X / 2AFC studies named above; I rendered but could not listen. The *costs*
  are solid given N; the *acceptance rates* are the empirical unknown.
- **True effective N.** The honest surface is BIT's 12–21, but the real
  recognition decision may collapse to `style ∧ opening` (ADV-F5) — far fewer
  bits. The ablation study would settle it.
- **Real input-space dependence.** My grind cost assumes inputs are free to choose;
  for a *targeted* victim whose legitimate input is fixed, the attacker still only
  needs a second-preimage (cost `2^N`), so the conclusion is unchanged — but the
  *plausibility* of the attacker's chosen input (a believable look-alike address)
  is application-specific and unmodeled here.
- **Decay curve shape.** N(t) is assumed monotone-decreasing but its slope is
  untested; the worst-case (and thus the quoted adversarial cost) depends on it.
- **Renderer realism.** My constructed pair models the threat with a hand-built
  arrangement, not entmotif's (nonexistent) generator. A real renderer with a
  richer analog stack would diverge *more* in Model A but — per ADV-F3 — **not** in
  Model B, so the threat conclusion is expected to hold or worsen.

---

## Findings Manifest

```yaml
findings:
  - id: ADV-F1
    persona: collision-adversary
    title: Habituated-victim Model-B second-preimage costs ~2^13 (cheapest real attack)
    severity: CRITICAL
    confidence: LIKELY
    location: this.i:m4z81p3v
    dedupe_key: fingerprint-grindable
    recommended_disposition: recommend-fix
    rationale: Attacker matches only the memorable subset (style+lead+opening+rhythm ~13 bits) -> ~9,400 offline tries; the realistic habituated check is defeated for the headline promise. Anchored in §4 optimistic yields restricted to memorable rows; BIT-F1's audit makes the real number lower.
    revisit_condition: null
    fix_effort: medium
    settling_experiment: A/B/X recognition study with lures matching style+opening+rhythm but diverging in consequent+analog stack, habituated listeners, >=1-day delay; measure false-alarm/acceptance rate.
  - id: ADV-F2
    persona: collision-adversary
    title: Whole-motif integrity does not block the ignorable-tail attack under Model B
    severity: HIGH
    confidence: SPECULATIVE
    location: this.i:9k3f0a72
    dedupe_key: transformation-collidable
    recommended_disposition: recommend-fix
    rationale: Constructed a byte-distinct pair sharing the entire antecedent and diverging only in the consequent transformation+cadence -- exactly the case 9k3f0a72 claims to kill; ACA-F4 (no evidence untrained listeners recover a late theoretic transformation from memory) supplies the perceptual basis. Reclassify the consequent-transformation row to integrity-only/0 perceptual bits until a study shows otherwise. Ear-confusability flagged for human listening.
    revisit_condition: 2AFC (target vs lure identical bars 1-4, differ only in consequent), untrained, >=1 day, yields d'>0 (then integrity defense holds and severity drops).
    fix_effort: medium
    settling_experiment: 2AFC target vs lure identical for bars 1-4 differing only in the consequent, untrained listeners, >=1 day later; if d'~0, integrity defense is perceptually inert (CONFIRMED).
  - id: ADV-F3
    persona: collision-adversary
    title: Analog stack does not raise Model-B collision cost; attacker ignores it
    severity: HIGH
    confidence: CONFIRMED
    location: this.i:e9k2m4p1
    dedupe_key: analog-stack-overclaimed
    recommended_disposition: recommend-fix
    rationale: By the design's own discrete/analog law the analog stack carries 0 recall bits, so it adds 0 to N and 0 to the attacker's second-preimage cost; Model-A distinguishability and casual avalanche are irrelevant to a memory-only victim, and BIT-F3 shows the consumed-bit margin quantizes out. The doc cannot claim 0 recoverable bits and collision-hardening from the same layers.
    revisit_condition: null
    fix_effort: small
    settling_experiment: Compute effective consumed = sum of log2(distinct MIDI values each analog layer writes) from the parameter-resolution table (shared with BIT-F3).
  - id: ADV-F4
    persona: collision-adversary
    title: Modulo bias plus affinity weighting cluster outputs, shrinking effective space below nominal
    severity: MEDIUM
    confidence: LIKELY
    location: docs/bit-budget.md §7
    dedupe_key: progression-grindable
    recommended_disposition: recommend-fix
    rationale: Modulo over non-2^k reads concentrates ~25% excess mass on low-index options (~0.85 bit shrink over ~10 reads, BIT-F6) and tells the attacker the densest region; affinity weighting (c2k9p0a4) further concentrates output on signature combos. Nominal 12-21 bits overstates the entropy the attacker faces.
    revisit_condition: null
    fix_effort: small
    settling_experiment: Over a large input corpus measure empirical H(discrete-class-vector) vs nominal budget; gap = the clustering discount; confirm rejection sampling (BIT-F6 fix) closes the modulo part.
  - id: ADV-F5
    persona: collision-adversary
    title: Style is both the master memory hook and the cheapest channel to match
    severity: MEDIUM
    confidence: LIKELY
    location: this.i:z0m4p81q
    dedupe_key: style-grindable
    recommended_disposition: recommend-fix
    rationale: Style is one ~4.6-4.8-bit pick the victim weights most heavily; matching style+lead gets a habituated victim ~7 bits toward acceptance. The effective recognition decision is closer to (style AND opening-gesture) than the full vector, so summing dimensions overstates the attacker's cost.
    revisit_condition: null
    fix_effort: medium
    settling_experiment: Ablation study holding style+opening fixed and varying everything else; high acceptance => effective recognition N far below budgeted N.
  - id: ADV-F6
    persona: collision-adversary
    title: Recognition decays over time, shrinking N and the attacker's cost at the realistic check interval
    severity: MEDIUM
    confidence: LIKELY
    location: docs/bit-budget.md §7
    dedupe_key: fingerprint-decays-over-time
    recommended_disposition: recommend-fix
    rationale: 2^N assumes fixed N, but ACA-F1/F2 show contour/rhythm decay over filled delays; at +1 week the check may face only ~7-9 effective bits (second-preimage ~hundreds). Budget should be a decay curve and adversarial cost quoted at the longest-delay point.
    revisit_condition: null
    fix_effort: medium
    settling_experiment: A/B/X recognition at 10min/1day/1week (Schellenberg & Habashi 2015); fit N(t); quote adversarial cost at the intended interval.
  - id: ADV-F7
    persona: collision-adversary
    title: The adversarial-collision boundary is not surfaced where a user decides to trust a motif
    severity: MEDIUM
    confidence: LIKELY
    location: this.i:m4z81p3v
    dedupe_key: spec-missing
    recommended_disposition: recommend-fix
    rationale: The recognition-not-crypto disclaimer lives in design docs, not at the point of trust; a user treating "the tune sounds right" as evidence of a matching input is exposed to a ~2^13-2^21 collision. Record an explicit anti-claim ("a matching motif is not adversarial evidence of a matching input; use byte comparison for trust-bearing checks") and propagate to UI.
    revisit_condition: null
    fix_effort: small
    settling_experiment: null
```
