# Psychoacoustician / Audiologist — Adversarial Design Review

**Project:** entmotif · **Run:** 2026-06-23 · **Mode:** unattended, deep, ANALYSIS-ONLY
**Persona:** AUD (`prompts/review/psychoacoustician.md`) · **Lens:** auditory perception &
accessibility — masking, loudness/register floor, timbre-discrimination limits, tempo/rhythm
JND, population accessibility (amusia, presbycusis, hearing aids / cochlear implants),
device/codec/loudness-normalization variation, immediate-audibility vs Model-B memorability.

> **I cannot hear audio.** Every claim below is reasoned from psychoacoustics and from the
> *measured* MIDI note/register/velocity data in `experiments/soundfont/` (parsed directly,
> ground truth — see Evidence Inventory). Where a claim genuinely needs ears, it is in
> **§ For human listening** and tagged `confidence: SPECULATIVE pending listening`.

---

## Evidence Inventory

Read: `docs/bit-budget.md` (DRAFT v2), `this.i` (all nodes, esp. `k20f9a3x`, `b7p21m9z`,
`3k7a92f0`, `8a3k0f29`, `e9k2m4p1`, `f3a0k9m2`, `q9f3a7k2`, `z0m4p81q`, `c2k9p0a4`), `AGENTS.md`,
and the three generators in `experiments/soundfont/` (`gen_style_midi.py`,
`gen_style_midi2.py`, `gen_test_midi.py`) plus `render_test.sh`.

**Measured ground truth** — I parsed `test_styles.mid` and `test_styles2.mid` per tempo-section
and tabulated, per voice (channel), pitch range and velocity range. Highlights that drive the
findings below:

| Fragment | LEAD (ch0) reg / vel | Bed reg / vel | Bass reg / vel | Perc vel |
|---|---|---|---|---|
| Ragtime | 36–84 / 66–102 | (single piano voice) | — | — |
| **Boogie** | 60–75 / **78** | — | 36–51 / **96** | — |
| Bossa | 74–81 / 84 | guitar 62–77 / 70 | 26–38 / 78 | 42–70 |
| **Sitar** | 60–72 / 96 | drone 48–55 / **40** | — | 80 |
| Synthwave | 62–76 / 100 | pad 48–64 / 60 | **29–36** / 92 | 60–110 |
| Western | 76–88 / 102 | twang 62–64 / 55 | 40–45 / 70 | — |
| **Chant** | 60–72 / 88–102 | drone 50–57 / **45** | — | — |
| Aria (retired) | 66–78 / 100 | strings 50–64 / **48** | — | — |
| Reggae | 67–72 / 88 | organ 55–64 / 64 | **31–45** / 88–92 | 45–100 |
| Rock ballad | 67–76 / 104 | pad 53–67 / **46**; piano 41–64 / 60 | **29–36** / 80 | 95–100 |
| **Celtic jig** | 62–74 / 98 | drone 50–57 / **42** | — | 55–95 |
| Polka | 67–79 / 96 | accordion 48–62 / 70 | tuba 36–43 / 95 | 80–95 |
| Novelty/SFX | 71–79 / 100 | pizz 43–57 / 70 | — | bird 84/100; applause 60/110 |

Two structural facts about this evidence matter for the whole review:

1. **These fragments are hand-composed sketches, not generator output.** A human arranger kept
   the lead clear (lead velocity ≥ bed velocity in every fragment *except boogie*; lead register
   above the bed). The shipping system will instead place lead/bed/groove/analog layers by
   *entropy*, across ~32 styles × capability-gated lead pools (`c2k9p0a4`) × a deep analog stack
   (`e9k2m4p1`). **Demo audibility is not evidence of generated-output audibility.** The masking
   and floor findings below are about what the *generator* can emit, not what these 13 sketches
   happen to do.
2. **The listening tests cited as validation (`b7p21m9z`, `8a3k0f29`, `q9f3a7k2`) were run by
   the design author, on the author's hardware, presumably on a decent speaker, with a normal,
   attentive, musically-literate ear.** Every retirement (shakuhachi, free-reed twins, aria) and
   every "validated distinct" claim inherits that single listener / single device. The
   population and device axes this persona owns are *entirely unmeasured*.

---

## Audible-Bits Budget (per dimension × listening condition)

Columns: **(a)** good speaker / normal attentive hearing; **(b)** phone speaker or single
earbud in a noisy room; **(c)** moderate presbycusis (≥40 yo, rolled off above ~4–6 kHz);
**(d)** congenital amusia (~1.5% prevalence — the modern figure; `docs/bit-budget.md §7` still
cites the **obsolete 4%** and should be corrected). Values are *delivered Model-B bits I judge
survive*, against the v2 nominal. All SPECULATIVE pending a real study; this is a
psychoacoustic estimate, not a measurement.

| Dimension (nominal v2) | (a) good | (b) phone/noisy | (c) presbycusis | (d) amusia |
|---|---|---|---|---|
| Style preset 5–6 | 5–6 | **3–4** | 4–5 | **3–4** (rhythm/timbre carry it) |
| Lead instrument 1.5–2.5 | 1.5–2.5 | **0.5–1** | **0.5–1.5** | 1–2 |
| Mode (major/minor color) 0.5–1 | 0.5–1 | 0.25–0.5 | 0.5–1 | **~0** (pitch-deaf) |
| Tempo within band 0.25–0.75 (S) | 0.25–0.75 | 0.25–0.75 | 0.25–0.75 | 0.25–0.75 |
| Meter residual 0.25–0.5 | 0.25–0.5 | 0.25–0.5 | 0.25–0.5 | 0.25–0.5 (rhythm spared) |
| Antecedent rhythm 2.5–3 | 2.5–3 | **1.5–2.5** | 2.5–3 | 2.5–3 (amusia spares rhythm) |
| Antecedent contour 2.5–3 | 2–3 | 1.5–2.5 | 2–2.5 | **0–0.5** (contour is pitch) |
| Consequent transformation 2–3 | 1.5–2.5 | **1–1.5** | 1.5–2 | **0.5–1** (mostly pitch-based) |
| Cadence type 0.75–1.25 | 0.5–1 | **0.25–0.5** | 0.5–1 | **~0** (harmonic/pitch) |
| Form / phrase count 0.25–0.75 | 0.25–0.75 | 0.25–0.5 | 0.25–0.75 | 0.25–0.75 |
| Harmonic progression 1.5–2 | 1–1.5 | **0.25–0.75** | 1–1.5 | **~0** (pitch/harmony) |
| Groove variant 0.5–1 | 0.5–1 | 0.5–1 | 0.5–1 | 0.5–1 (rhythm spared) |
| Accompaniment texture 0.5–1 | 0.5–1 | **0.25–0.5** | 0.5–1 | 0.5–1 |
| Texture-interruption 1–2 | 1–2 | **0.5–1.5** | **0.25–1** (often hi-freq SFX) | 1–2 |
| **Approx total (nominal ~19–28)** | **~17–26** | **~10–16** | **~14–21** | **~9–14** |

**Headline reading:** under a good speaker and normal hearing the budget is roughly intact
(~17–26 vs ~19–28). But **on a phone speaker / single earbud in a noisy room the delivered
budget falls to ~10–16 bits, and for a congenital-amusic listener to ~9–14 bits** — in both
cases *below the 25-bit floor the design treats as its product promise* (`2p8z1m40`,
`docs/bit-budget.md §5`). The collapse is concentrated in the **pitch-derived dimensions**
(contour, mode, harmonic progression, cadence, consequent transformation), which is exactly
where roughly half the nominal budget lives. The budget is **not** a single number; it is a
distribution over listeners and devices, and the design currently quotes only the best cell of
that distribution.

---

## Executive Summary

The design is psychoacoustically thoughtful in its bones — the discrete/analog law
(`k20f9a3x`), the "style bed carries identity before melody" insight (`z0m4p81q`), the
fidelity gate (`3k7a92f0`), and the "weird-but-distinct timbre helps recognition" finding
(`b7p21m9z`, `f3a0k9m2`) are all correct and well-motivated. The headline claim — *~25–50 bits
recoverable by recognition from memory* — is **conditionally true for a normal-hearing,
attentive listener on a decent speaker, and materially false for two large, silent populations
the design does not budget for**:

1. **Phone-speaker / earbud-in-noise listeners** (a *majority* of real playback, given the web
   player `4m1zp870`): a phone speaker rolls off hard below ~400–600 Hz and is bandwidth- and
   dynamic-range-limited. **Every bass-bed and drone-bed dimension lives partly or wholly under
   that floor** (measured: bass at MIDI 29–45 = ~44–110 Hz; drones at vel 40–48). The bed is
   *co-equal with melody* by design (`z0m4p81q`) — so when the bed vanishes, a load-bearing,
   bit-claimed dimension vanishes silently. Loudness normalization (every streaming/web context)
   further flattens the velocity contrasts the analog stack relies on.

2. **Congenital amusia (~1.5%, not 4%)**: pitch-melody-deficit listeners lose contour, mode,
   harmony, cadence, and most of the consequent-transformation bits — *all* the melodic
   dimensions. That is ~9–14 surviving bits, well under the floor. ~1.5% of the population is
   millions of users for any deployed tool; the failure is total for them on the melodic half
   and completely silent (they will "recognize" by style/rhythm/timbre alone and collide on
   everything melody-distinguished).

Three more specific perceptual hazards: **masking** — the design's own deep analog stack
(`e9k2m4p1`) plus entropy-placed beds can put bit-bearing lead contour *behind* a louder/denser
bed (boogie already shows lead vel 78 under bass vel 96 in the hand-tuned demo — the generator
has no constraint preventing far worse); **timbre over-claim** — the ~18–20 "pairwise-distinct"
lead-timbre classes (`b7p21m9z`, ~4 bits) were judged in the clear, solo, mid-register, on one
device; through a phone speaker and *especially* through a cochlear implant or hearing aid,
timbre discrimination collapses toward a handful of classes (bright vs dark vs plucked vs
sustained), so the lead-instrument bits are the most over-claimed in the schedule on lo-fi/HoH
paths; and **memory decay** — the lowest-yield dimensions (meter residual, mode, cadence,
texture, form) are precisely the ones most likely audible-A/B but *not* encoded to Model-B
recall, especially over the "minutes-to-days" gap the design admits is untested
(`docs/bit-budget.md §7`).

None of these block *building* a v1; all of them mean the **claimed number must be
condition-and-population-qualified** before it goes normative, and that the smallest honest
correction (the obsolete 4% amusia figure) should be made now. The single highest-leverage
design change is to **make the bit floor a function of (device class, hearing profile)** and to
quote the *phone-speaker* number as the headline, not the studio number.

---

## Top Findings (≤7)

### AUD-F1 — Phone-speaker / earbud playback drops the budget below its own floor (bass & drone beds vanish) — **Population: PHONE-SPEAKER / ALL** — HIGH

The design's delivery surface is a **web player** (`4m1zp870`, `8a3k0f29` via js-synthesizer
WASM), i.e. most listeners are on laptop, phone, or earbud — not a studio monitor. A typical
phone/laptop speaker is ~−10 to −30 dB by 300–500 Hz and effectively silent below ~150–200 Hz;
a single earbud in a noisy room (street, café) has a noise floor that swamps soft, low content.

Measured: style **bass beds sit at MIDI 29–45 (≈44–110 Hz)** — synthwave 29–36, rock-ballad
29–36, reggae 31–45, polka tuba 36–43. **Drone beds** (sitar, Celtic, chant, aria-strings) sit
at vel **40–48**, ~40–55 velocity units below the lead. The design explicitly makes the
**groove+timbre bed co-equal with melody** and the carrier of style identity *before any melody*
(`z0m4p81q`). So the dimensions most likely to be eaten by a small speaker (bass groove, drone
mode-color, accompaniment texture) are **bit-claimed**, not flavor. When they're inaudible the
listener recognizes a *thinner* motif and the style/groove/texture/progression bits silently
erode toward the (b)-column numbers (~10–16 total). Loudness normalization compounds it by
compressing the velocity contrasts the analog stack (`e9k2m4p1`) banks on for casual avalanche.

*Disposition: recommend-fix.* Quote the **phone-speaker budget** as the product number, and add
a render-fidelity rule analogous to `3k7a92f0`: a dimension earns bits only if it survives a
**band-limited, dynamic-range-compressed playback model**, not just the full-range font.
*Settling experiment:* render 30 entropy-varied motifs, play through a measured phone-speaker
EQ + a noisy-room masker, run A/B/X recognition; compare per-dimension recovery to studio.

`dedupe_key: analog-stack-inaccessible-on-phone-speaker`

### AUD-F2 — Congenital amusia zeros the melodic half of the budget; prevalence is mis-stated (4% → ~1.5%) — **Population: AMUSIA** — HIGH

Congenital amusia (true prevalence **~1.5%** by current estimates, e.g. Peretz lab revisions
downward from the legacy 4% Kalmus/Fry-era figure that `docs/bit-budget.md §7` still cites)
is a *fine-grained pitch-direction and pitch-interval* deficit with **rhythm and timbre largely
spared.** For an amusic listener, **contour, mode (major/minor), harmonic progression, cadence
type, and most of the consequent-transformation** bits are unrecoverable — that is the entire
melodic, ~10–13-bit half of the v2 schedule. They retain style-by-rhythm/timbre, meter, groove,
tempo, texture-interruption: ~9–14 bits, below the 25 floor. The failure is **silent and
collision-prone**: two inputs that differ *only* in melodic dimensions are Model-B-identical to
this population (ties into the collision-adversary lens — `collidable-under-amusia`).

Two concrete corrections: (1) the **obsolete 4%** in `§7` should be `~1.5%` (still load-bearing
— millions of users); (2) the design should **state explicitly which dimensions survive amusia**
and lean the redundant, recognizable hooks on the *spared* channels (style-via-groove, rhythm,
timbre-family, texture-interruption) so amusic recognition degrades gracefully rather than to
near-chance on melody-distinguished pairs.

*Disposition: recommend-fix* (the number correction is `fix_effort: small` and should happen
now; the design accommodation is `medium`). *Settling experiment:* screen listeners with the
Montreal Battery (MBEA); run the recognition study split by amusic/non-amusic.

`dedupe_key: contour-inaccessible-under-amusia`

### AUD-F3 — Lead-timbre bit count (~18–20 classes ≈ 4 bits) is over-claimed on lo-fi, presbycusis, and hearing-aid/CI paths — **Population: PHONE-SPEAKER / HoH / ALL** — HIGH

`b7p21m9z` claims ~18–20 pairwise-distinct lead-timbre classes (~4 bits before style gating),
from a listening test that already (correctly) collapsed shakuhachi, the free-reed triplet, and
the breathy-flute pair. But timbre discrimination is the **least robust** dimension across
device and hearing:

- **Phone speaker / band-limit:** timbre identity lives largely in the upper formants/harmonics
  and attack transients. Roll off the top and add room noise and many GeneralUser-GS mid-leads
  collapse toward each other — the aria→flute confusion (`q9f3a7k2`) is the *clean-path* example;
  expect more pairs (oboe/violin/whistle/pan-flute-survivor, organ variants, plucked
  sitar/koto/banjo/harpsichord) to merge on lo-fi.
- **Presbycusis (≥~50 yo, very common):** high-frequency roll-off above ~4–6 kHz directly
  attacks "bright" timbres, cymbals, and the **high SFX texture-interruption** (the bird-tweet at
  MIDI 84, GM 123, is a high-frequency event — `f3a0k9m2`); the most-distinct style in the test
  may be the *least* audible to older ears.
- **Hearing aids / cochlear implants:** CIs convey **pitch and timbre very poorly** — CI users
  reliably distinguish only coarse spectral categories. ~18–20 timbre classes is implausible on
  a CI; realistically 3–5 (bright/dark/plucked/sustained/noisy). Hearing aids add compression
  and frequency-shaping that smear timbre further.

So lead-instrument bits should be **conditioned on device/hearing**, not quoted as a flat ~4.
This is the single most over-claimed row of the schedule on non-ideal paths.

*Disposition: recommend-fix* (qualify the claim; keep timbre as recognition-margin where bits
don't survive). *Settling experiment:* repeat the pairwise-distinctness test through (i) a phone
EQ, (ii) a presbycusis-simulating high-shelf cut, (iii) a CI vocoder simulation; report the
surviving class count per condition.

`dedupe_key: lead-instrument-overclaimed-on-phone-speaker`

### AUD-F4 — Entropy-placed beds + the deep analog stack can mask the bit-bearing lead (simultaneous & temporal masking) — **Population: ALL** — MEDIUM

The demos are hand-balanced, but the shipping generator places lead, bed, groove, and a *stack*
of analog modulations (velocity, articulation, register shading, brightness CC — `e9k2m4p1`) by
entropy, with **no stated masking constraint.** Risks:

- **Simultaneous (spectral) masking:** a loud, harmonically dense bed in the lead's critical
  bands masks the lead's contour. The boogie demo *already* shows lead vel 78 *under* bass vel 96
  — the only constraint keeping that from being worse is the human arranger, which the generator
  lacks. A bright pad or organ skank in the lead's register (reggae organ 55–64 vel 64 vs lead
  67–72 vel 88 is fine; entropy could invert it) can bury the bit-bearing line.
- **Temporal (forward/backward) masking:** a loud transient — the 4-on-floor kick (vel 110,
  synthwave), the crash (vel 100), the applause tag (vel 110), a hard rhythmic stab — masks soft
  lead onsets within ~20–200 ms. The **consequent transformation** (`9k3f0a72`) and the
  **texture-interruption** (`f3a0k9m2`) are exactly the bit-bearing events most exposed to being
  stepped on by a co-timed groove hit.

*Disposition: recommend-fix.* Add an explicit arrangement constraint to the spec: a minimum
lead-over-bed loudness margin in the lead's critical bands, and a guard that bit-bearing onsets
(opening gesture, consequent downbeat, texture-interruption) are not co-placed with the loudest
groove transients. *Settling experiment:* generate adversarial entropy values that place a loud
dense bed in the lead band; A/B/X whether the contour/transformation is still recoverable.

`dedupe_key: lead-instrument-collidable` (lead vs bed masking)

### AUD-F5 — Low-yield discrete dimensions are audible-A/B but decay before Model-B recall — **Population: ALL** — MEDIUM

Model B is recognition *from memory*, after a gap the design admits is untested (minutes to
days, `docs/bit-budget.md §7`). Several schedule rows yield small, fragile distinctions that an
A/B side-by-side (Model A) resolves but that **do not encode to a durable memory trace**: meter
residual (0.25–0.5), mode color (0.5–1) for a brief motif, cadence type (0.75–1.25), accompani-
ment texture (0.5–1), and form/phrase count (0.25–0.75). Non-musicians do not reliably tag
"plagal vs deceptive cadence" or "block vs arpeggio texture" *from memory* — these are
expert-listener categories. The risk is that the budget counts ~2–4 bits that are real in the
lab (Model A) but evaporate in the field (Model B over time), pulling the honest delivered
number further toward the low end of every column above.

*Disposition: recommend-defer* (re-estimate after a recall-over-delay study; mark these rows as
"Model-A-confirmed, Model-B-pending"). *Revisit condition:* the §7 memorability-decay study runs.
*Settling experiment:* recognition study with 1-minute / 1-hour / 1-day delays, per-dimension
recovery curves; the dimensions whose recovery falls to chance by 1 hour lose their bits.

`dedupe_key: cadence-decays-over-time` (representative; also mode/meter/texture/form)

### AUD-F6 — Tempo & meter are perceptually robust but the *tempo-band* bits are thin and S-class margin, not countable — **Population: ALL** — LOW

This is a *confirming/bounding* finding, not an attack on a big number. Rhythm/tempo perception
is the one channel robust across phone speakers, presbycusis, *and* amusia, so meter (3 vs 4 vs
6/8 feel) and broad fast/slow are sturdy and correctly modest in the schedule. Two cautions: (1)
the tempo-within-band row is tagged **S** and valued 0.25–0.75 — tempo JND for non-musicians is
~5% and *relative* (no absolute-tempo memory), so any "tempo class" must be separated by well
more than 5% and is at most ~1 coarse bit; keep it as margin, don't inflate it. (2) The demo
tempo set (72–150 BPM) is fine, but the design should ensure **tempo classes within a style band
differ by ≥ ~15–20%** to clear JND-plus-memory, not just ≥ JND. Meter is the strongest leg of
the budget for the impaired/lo-fi populations — lean on it.

*Disposition: recommend-accept-risk* (already conservatively budgeted; just enforce the class
separation in the spec). *Settling experiment:* a tempo-discrimination-from-memory task to fix
the minimum within-band tempo-class spacing.

`dedupe_key: tempo-overclaimed` (minor; mostly a confirm-and-bound)

### AUD-F7 — Device / soundfont / codec variation moves *heard* timbre and balance even with the .mid pinned — **Population: ALL** — MEDIUM

`3k7a92f0`/`8a3k0f29` pin the soundfont (GeneralUser GS) and render via FluidSynth "everywhere"
for parity — good. But the *heard* audio still varies along axes the pin does not control: (1)
**js-synthesizer WASM in-browser is explicitly unproven** (`docs/bit-budget.md §7`) and may not
be sample-identical to offline FluidSynth (interpolation, reverb defaults, polyphony limits, DC);
(2) **speaker/headphone EQ** reshapes timbre per device; (3) **lossy codecs** (if audio is ever
served as MP3/AAC/Opus rather than rendered client-side) smear high-frequency timbre and
transients — directly attacking the timbre and texture-interruption bits; (4) **loudness
normalization** (browser, OS, platform) flattens the velocity/dynamics contrasts of the analog
stack. The .mid being canonical/deterministic (`4m1zp870`) does **not** rescue the *perceptual*
delivery — recognition happens on the rendered audio, which is exactly where these vary. The
"timbre parity" claim should be scoped to "same soundfont + same FluidSynth build," with the
WASM path treated as a *separate* fidelity tier until measured.

*Disposition: recommend-fix* (scope the parity claim; add a WASM-vs-offline render diff to the
songbook discipline). *Settling experiment:* render the songbook offline and via the WASM player;
spectrally diff; confirm no timbre-class merges; repeat after Opus transcode at typical bitrates.

`dedupe_key: soundfont-unrenderable` (cross-path render variance / parity scope)

---

## For human listening

I cannot hear; these need real ears (each `confidence: SPECULATIVE pending listening`). The
harness exists: `experiments/soundfont/render_test.sh` + the generators. I deliberately did
**not** render-and-judge, to avoid claiming an audibility verdict I cannot make.

1. **Phone-speaker pass (AUD-F1).** Render `test_styles*.mid` via FluidSynth, then play through a
   measured phone/laptop-speaker EQ (high-pass ~300 Hz + the device response) in a noisy room.
   Confirm whether the bass/drone beds (synthwave/reggae/rock-ballad bass MIDI 29–45; sitar/
   Celtic/chant drones vel 40–45) are still audible and whether style identity holds.
2. **Boogie lead-under-bass (AUD-F4).** Listen specifically to whether the RH 7th-stab contour
   (vel 78) is intelligible under the rolling LH bass (vel 96) — the one demo where bed > lead.
3. **Timbre-merge sweep (AUD-F3).** Render `test_instruments.mid` (23 patches) through (a) clean,
   (b) phone EQ, (c) a presbycusis high-shelf cut (−12 dB above 4 kHz), (d) a CI-vocoder sim;
   count surviving pairwise-distinct classes per condition vs the claimed ~18–20.
4. **Texture-interruption audibility (AUD-F3/F1).** Confirm the bird-tweet (MIDI 84, GM 123) and
   applause tag survive a phone speaker and a presbycusis cut — they're high-frequency events.
5. **Loudness-normalization flattening (AUD-F1/F7).** Apply a loudness-normalization/limiter and
   judge whether the analog-stack velocity contrasts (the casual-avalanche margin) still read.
6. **WASM-vs-offline render diff (AUD-F7).** Render the same `.mid` offline (FluidSynth) and via
   js-synthesizer WASM; A/B for any audible timbre/balance difference.

---

## Residual Unknowns

- **No empirical recognition study exists.** Every delivered-bit number (mine and the design's)
  is a pre-empirical estimate. The whole budget rests on an A/B/X recognition study that has not
  been run — across populations and devices, not just the author's ear.
- **Memorability-decay curve is entirely unmeasured** (Model B over minutes/hours/days) — the
  decay finding (AUD-F5) is the largest unquantified risk to the *delivered* total.
- **Amusia prevalence and per-dimension impact** are cited from literature, not measured on this
  stimulus set; the ~1.5% figure is current best-estimate, the per-dimension zeroing is inferred
  from the deficit's known profile (pitch-impaired, rhythm-spared).
- **CI / hearing-aid timbre discrimination** for *this* soundfont is unmeasured; my 3–5-class
  estimate is from the CI literature, not from these renders.
- **WASM render fidelity vs offline FluidSynth** is unproven (the design itself flags this).

---

```yaml
findings:
  - id: AUD-F1
    persona: psychoacoustician
    title: Phone-speaker/earbud playback drops the budget below its own 25-bit floor; bass & drone beds vanish
    severity: HIGH
    confidence: SPECULATIVE
    location: this.i:e9k2m4p1   # analog stack / bed; also docs/bit-budget.md §5 totals
    dedupe_key: analog-stack-inaccessible-on-phone-speaker
    recommended_disposition: recommend-fix
    rationale: Bed/bass beds (MIDI 29-45, drones vel 40-48) are bit-claimed yet live under the phone-speaker low-frequency/dynamic floor; quote the phone-speaker budget as the product number.
    revisit_condition: null
    fix_effort: medium
    settling_experiment: A/B/X recognition on 30 entropy-varied motifs through a measured phone-speaker EQ + noisy-room masker vs studio; per-dimension recovery delta.
  - id: AUD-F2
    persona: psychoacoustician
    title: Congenital amusia zeros the melodic half of the budget; prevalence mis-stated (4% should be ~1.5%)
    severity: HIGH
    confidence: LIKELY
    location: docs/bit-budget.md §7   # also this.i:k20f9a3x melodic dimensions
    dedupe_key: contour-inaccessible-under-amusia
    recommended_disposition: recommend-fix
    rationale: Amusic listeners lose contour/mode/harmony/cadence/transformation (~10-13 bits), landing ~9-14 < 25 floor; §7's 4% figure is obsolete (~1.5%). Number correction is small and should happen now.
    revisit_condition: null
    fix_effort: small
    settling_experiment: MBEA-screen listeners; run the recognition study split amusic/non-amusic; report per-dimension recovery.
  - id: AUD-F3
    persona: psychoacoustician
    title: Lead-timbre bit count (~18-20 classes, ~4 bits) over-claimed on lo-fi, presbycusis, and CI/hearing-aid paths
    severity: HIGH
    confidence: SPECULATIVE
    location: this.i:b7p21m9z
    dedupe_key: lead-instrument-overclaimed-on-phone-speaker
    recommended_disposition: recommend-fix
    rationale: Timbre lives in upper harmonics/transients; band-limit, HF loss, and CI vocoding collapse ~18-20 classes toward ~3-5. Condition the claim on device/hearing; keep timbre as margin where bits don't survive.
    revisit_condition: null
    fix_effort: medium
    settling_experiment: Re-run pairwise-distinctness through phone EQ, presbycusis high-shelf cut, and CI-vocoder sim; report surviving class count per condition.
  - id: AUD-F4
    persona: psychoacoustician
    title: Entropy-placed beds plus the deep analog stack can mask the bit-bearing lead (simultaneous & temporal masking)
    severity: MEDIUM
    confidence: SPECULATIVE
    location: this.i:e9k2m4p1   # also 9k3f0a72 (consequent), f3a0k9m2 (interruption)
    dedupe_key: lead-instrument-collidable
    recommended_disposition: recommend-fix
    rationale: Demos are hand-balanced (boogie already has lead vel 78 < bass vel 96); the generator has no masking constraint, so a loud/dense bed or co-timed transient can bury contour/transformation/interruption onsets.
    revisit_condition: null
    fix_effort: medium
    settling_experiment: Generate entropy values that place a loud dense bed in the lead's critical band / co-time loud transients with bit-bearing onsets; A/B/X whether contour/transformation survive.
  - id: AUD-F5
    persona: psychoacoustician
    title: Low-yield discrete dimensions are audible side-by-side but decay before Model-B recall
    severity: MEDIUM
    confidence: SPECULATIVE
    location: docs/bit-budget.md §4   # cadence/mode/meter/texture/form rows
    dedupe_key: cadence-decays-over-time
    recommended_disposition: recommend-defer
    rationale: Meter-residual/mode/cadence/texture/form are expert-listener, low-yield categories that resolve in Model A but likely evaporate from memory over minutes-days for non-musicians; ~2-4 bits at risk.
    revisit_condition: The §7 memorability-decay (recall-over-delay) study is run.
    fix_effort: small
    settling_experiment: Recognition study at 1-min/1-hr/1-day delays; per-dimension recovery curves; rows reaching chance by 1 hour lose their bits.
  - id: AUD-F6
    persona: psychoacoustician
    title: Tempo/meter are robust across populations but tempo-band bits are thin S-class margin, not countable
    severity: LOW
    confidence: LIKELY
    location: docs/bit-budget.md §4   # tempo-within-band row (S)
    dedupe_key: tempo-overclaimed
    recommended_disposition: recommend-accept-risk
    rationale: Tempo JND ~5% and relative (no absolute-tempo memory); tempo-within-band is at most ~1 coarse bit and correctly S-tagged. Enforce >=15-20% within-band tempo-class spacing; meter is the sturdiest leg for impaired/lo-fi users.
    revisit_condition: null
    fix_effort: small
    settling_experiment: Tempo-discrimination-from-memory task to fix the minimum within-band tempo-class spacing.
  - id: AUD-F7
    persona: psychoacoustician
    title: Device/soundfont/codec/loudness-normalization variation shifts heard timbre & balance despite the pinned .mid
    severity: MEDIUM
    confidence: SPECULATIVE
    location: this.i:8a3k0f29   # also 3k7a92f0, 4m1zp870
    dedupe_key: soundfont-unrenderable
    recommended_disposition: recommend-fix
    rationale: Pin guarantees MIDI parity, not perceptual parity; WASM render is unproven, speaker EQ/lossy codecs/loudness norm reshape timbre & dynamics where recognition actually happens. Scope the parity claim and add a WASM-vs-offline render diff.
    revisit_condition: null
    fix_effort: medium
    settling_experiment: Render the songbook offline vs WASM, spectrally diff, confirm no timbre-class merges; repeat after Opus transcode at typical bitrates.
```
