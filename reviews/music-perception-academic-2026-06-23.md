# Music-Perception Academic (Literature Red-Team) — entmotif design review

- **Persona:** ACA (`prompts/review/music-perception-academic.md`)
- **Run label:** 2026-06-23 · mode=unattended · effort=deep
- **Scope (read-only):** `this.i`, `docs/bit-budget.md`, `AGENTS.md`, `README.md`
- **Method:** each empirical claim entmotif relies on, checked against the music-cognition / auditory-memory literature via web search of primary sources. No motifs were rendered (no code yet); this is a *claims-and-reasoning* review per `orchestrating-reviews.md`.

---

## Evidence Inventory (sources consulted)

Primary / load-bearing:

1. **Dowling & Fujitani (1971)**, *Contour, interval, and pitch recognition in memory for melodies*, JASA 49(2B):524. — contour vs. interval in melody memory. (brainmusic.org PDF)
2. **Dowling, Kwak & Andrews (1995)**, *The time course of recognition of novel melodies*, Perception & Psychophysics / Atten Percept Psychophys (PMID 7885812; Springer BF03206500). — seven experiments, T/SC/DC paradigm, **contour decays faster than interval over filled delays; crossover.**
3. **Dowling & Bartlett (1981)** — unfamiliar Beethoven-quartet phrases, ~75% target/lure discrimination after >5 min in untrained high-schoolers (chance 50%).
4. **Dowling (1991)**, *Tonal strength and melody recognition after long and short delays*, Atten Percept Psychophys (BF03212222). — tonality facilitates interval encoding; contour discrimination declines, interval improves, **only for tonal stimuli.**
5. **Edworthy (1985)** — contour better at short retention / shorter sequences; interval better at long; **shorter sequences recognized better than longer.**
6. **Schellenberg & Habashi (2015)**, *Remembering the melody and timbre, forgetting the key and tempo*, Memory & Cognition 43(7):1021–31 (PMID 25802029). — **no forgetting of novel-melody identity over 1 week** after only two exposures; key/tempo change hurts at 10 min & 1 day but not 1 week; **timbre change hurts at all delays.**
7. **McAdams & Siedenburg (2019)** review, *Perception of musical timbre* — exemplar/auditory-image account; timbre durable; small consolidation gain at 1 week.
8. **Müllensiefen** (in McAdams & Siedenburg) — timbre is **categorical** vs. tempo's quasi-continuous scale → timbre more memorable long-term. Directly relevant to the discrete/analog law.
9. **Hébert & Peretz (1997)**, *Recognition of music in long-term memory: Are melodic and temporal patterns equal partners?*, Memory & Cognition (BF03201127). — **melody >> rhythm as a retrieval cue; rhythm alone a poor cue; combination best.**
10. **Peretz et al. / Foxton et al.; Peretz & Hyde** — melody/rhythm dissociation (amelodia without arhythmia); separate neural systems (PET working-memory study).
11. **Schmuckler & Moranis (2023)**, *Rhythm contour drives musical memory*, Atten Percept Psychophys 85:2502–2514 (PMID 36991289). — rhythmic *contour* is a memory basis in a **short-term** same/different paradigm.
12. **Gjerdingen & Perrott (2008)**, *Scanning the dial: the rapid recognition of music genres*, J. New Music Research. — **10 genres, 250 ms clips, ~44% mean accuracy**, huge per-genre variance (classical ~70%, blues <20%); music-theory majors ≈ non-musicians.
13. **Levitin (1994)**, *Absolute memory for musical pitch*, Perception & Psychophysics 56(4):414–423; **Levitin & Cook (1996)**, *Memory for musical tempo*. — for **over-rehearsed familiar pop**, 44% of subjects produced correct pitch on ≥1 of 2 trials, 12% on both; absolute tempo similarly. **Frieler et al. (2013)** six-lab replication (N≈277): effect present but **smaller** than original; ~−1 semitone mean deviation.
14. **Miller (1956)** + **Pollack** — absolute identification of pitch: channel capacity **~2.5 bits ≈ 6 categories**; one-dimensional absolute judgments cap ~2–3 bits across senses.
15. **Peretz & Vuvan (2017)**, *Prevalence of congenital amusia*, Eur J Hum Genet (PMID 28224991; ~20,000 Canadians, objective MBEA-based) — **1.5%**, revising the classic **4%** (single 1980 test) downward. Pradilla et al. (2020) ~0.52% in Colombian students.
16. **Cross-cultural mode/affect:** PNG study (Smit et al., *PLOS ONE* 2022, PMID via PMC9242494) — major-happy/minor-sad **tracks Western-music exposure**, absent in minimal-exposure community; NW-Pakistan tribal study (minor preferred); only **dissonance aversion** is robustly cross-cultural.
17. **Major/minor discrimination by non-musicians** (Halpern/Leaver-style; "Not Only Musicians Know Major and Minor", 2019; ERP major-minor classification studies) — **non-musicians cannot reliably discriminate same-melody major/minor pairs that start on different notes, nor label them "major/minor"**; they succeed only via the **happy/sad** affective framing.
18. **Loss, Limmer & von Gernler**, *The drunken bishop* analysis, and Perrig & Song, *Hash visualization* — the randomart visual analog: **useful for differentiation, not identification**; no controlled study quantifies its perceptual bits (the "~20–24 bits" the persona cites is an informal community/derived figure, not a measured result).

---

## Claim-by-Claim Ledger

### Claim 1 — Contour primacy (durable recall feature)
**Design reliance:** `this.i:k20f9a3x`, bit-budget §4 "Antecedent contour + opening gesture" 2.5–3 bits; README Q "does the melody rise, fall, arch."

**Evidence:** Contour is a *real and automatic* memory feature for novel melodies in **untrained** listeners (Dowling & Bartlett 1981, ~75% at >5 min). **BUT the literature's central, repeated finding is that contour memory DECAYS faster than interval memory over filled delays** (Dowling et al. 1995; Edworthy 1985; DeWitt & Crowder 1986). Contour dominates *immediate/short-empty-delay* recognition; over minutes-of-interference it is **overtaken by interval** — and crucially, reliable *interval* encoding requires a strong tonal frame (Dowling 1991) and is the harder, less untrained-ear-accessible code.

**Verdict:** PARTIALLY SUPPORTED but **misframed**. The design treats contour as a *durable Model-B hook*; the literature says contour is the **short-term** hook and is exactly the dimension most prone to `decays`-over-time. For Model B "later, from memory," the durable residue is *interval-within-tonality*, which untrained ears recover less reliably. The 2.5–3 bit contour line is plausible at *immediate* test, optimistic at *delayed* test. `dedupe_key: contour-decays-over-time`.

### Claim 2 — Rhythm as a strong, separable hook
**Design reliance:** `this.i:z0m4p81q` (groove "carries identity BEFORE any melody"); bit-budget §4 "Antecedent rhythmic motif" **2.5–3 bits** + "Groove variant" 0.5–1.

**Evidence:** Rhythm and melody are **separable** systems (Peretz dissociation; PET working-memory study) — so far so good. Rhythmic *contour* is a memory basis (Schmuckler & Moranis 2023) — but **only demonstrated short-term (immediate same/different)**. The decisive long-term result cuts the other way: **Hébert & Peretz (1997) found rhythm is a POOR retrieval cue in long-term memory; melody >> rhythm; the combination is best.** Rhythm's weakness is attributed to *lower encoding distinctiveness*.

**Verdict:** OVERCLAIMED for the *melodic*-rhythm line, **supported** for the *groove/style-bed* line. Giving the antecedent rhythmic motif 2.5–3 bits — **co-equal with contour** — is not supported; in durable memory rhythm is the *weaker* partner. The style-level groove (samba/funk pattern as a gestalt) is better grounded because it rides on *timbre+pattern* identity (Claim 3), not on remembered note-durations. `dedupe_key: rhythm-overclaimed`.

### Claim 3 — Genre / timbre categorization by non-musicians (the master dimension)
**Design reliance:** `this.i:z0m4p81q` ("non-musicians are expert genre classifiers"), `b7p21m9z`, `c2k9p0a4`, `d4m1z8p0`; bit-budget §4 **Style preset 5–6 bits**, 32→64 styles.

**Evidence — two-sided and the most consequential:**
- **PRO (timbre is the design's best-grounded bit source):** Timbre is encoded **categorically** and **durably** — a timbre change impairs recognition even at 1 week (Schellenberg & Habashi 2015; McAdams & Siedenburg 2019; Müllensiefen's categorical-vs-continuous argument). This is *direct empirical support* for `b7p21m9z` (timbre distinctiveness) and for style being a sturdy Model-B hook. **This is the strongest claim in the whole design.**
- **CON (the "expert genre classifier / 5–6 bits" number is overstated):** Gjerdingen & Perrott (2008) — the canonical "fast genre recognition" study the design implicitly leans on — found only **~44% mean accuracy across 10 genres at 250 ms, with classical ~70% but blues <20%.** Recognition is **fast but unreliable and wildly uneven across categories**; trained ≈ untrained. 5–6 bits asserts ~32–64 styles told apart *reliably*. The evidence supports *far fewer reliably-distinct genre categories than 32* when the discriminating cue is genre-as-such rather than raw timbre.

**Verdict:** SUPPORTED as **timbre/instrument-family** distinctiveness; **OVERCLAIMED as "genre/style" cardinality.** The honest carrier is *pairwise-distinct timbre/texture gestalts* (which `b7p21m9z` already frames correctly), not "non-musicians reliably sort 32 named genres." The §4 5–6 style bits should be defended on *gestalt pairwise distinctiveness through the pinned font* (an A/B/X result), not on genre-classification literature, which does not support 32 reliable classes. `dedupe_key: style-overclaimed`.

### Claim 4 — Model B feasibility & decay
**Design reliance:** `this.i:m4z81p3v`, `9k3f0a72` ("recognition runs to the END"); bit-budget §1, §7.

**Evidence — largely SUPPORTIVE, the design's best news:** Schellenberg & Habashi (2015) is almost custom-built for entmotif: novel melodies, **unselected (untrained) listeners**, recognition (old/new) — **fully consolidated after two exposures, NO forgetting over a week**, even a slight 1-week consolidation gain. Dowling & Bartlett (1981) gives ~75% at >5 min after a single exposure. So Model-B recognition of a novel motif over days is **realistic** — *provided the motif gets ~2 exposures and the discriminating features are the durable ones (timbre/style; interval-in-tonality), not the decaying ones (contour; absolute key/tempo).*

**The "runs to the END" sub-claim (`9k3f0a72`) is the weak spot:** Edworthy (1985) — **shorter sequences are recognized better than longer ones.** An 8-bar period, let alone a 12–16-bar form, pushes *past* the lengths in the recognition-memory literature (which uses ~5–12 note phrases). The design's lever for more bits (longer/richer form) **fights** the length-vs-recognition gradient. There is **no evidence found** that untrained listeners reliably encode a *late bound-transformation relationship* (sequence/inversion/augmentation of the antecedent) **from memory** — that is a music-theoretic relation whose *perception* untrained listeners are known to be poor at (cf. they can't even discriminate transposed major/minor — Claim 5). So the 2–3 bits assigned to "consequent transformation" as a *Model-B-recoverable* feature is **SPECULATIVE and probably optimistic.**

**Verdict:** Model-B-over-time: **SUPPORTED.** "Recognition to the end of a long motif / late transformation carries recoverable bits": **`decays`/`unsupported`** — the length gradient and untrained-ear limits both argue against it. `dedupe_key: transformation-unsupported`, `form-decays-over-time`.

### Claim 5 — Discrete/analog reliability split
**Design reliance:** `this.i:k20f9a3x` (the central law); bit-budget §4 (key=A=0 bits, analog stack=0 bits); README Q1 "major or minor (1 bit)".

**Evidence:** The *direction* of the law is **well supported.** No absolute pitch in most adults; the Levitin effect is **(a) for over-rehearsed familiar recordings only**, **(b) ~44%/12% even there**, **(c) smaller on six-lab replication** (Frieler et al. 2013). For **novel** melodies, key and tempo are explicitly the features that *decay first* (Schellenberg & Habashi 2015: key/tempo change stops mattering by 1 week). So zeroing key/tempo bits is **correct and conservative** — good.

**BUT two discrete features the design counts are themselves on the analog/unreliable side for untrained ears:**
- **Major/minor (README Q1 "1 bit"):** Non-musicians **cannot reliably discriminate same-melody major/minor pairs that start on different notes** and cannot label them; they succeed only via *happy/sad* affect (multiple studies; "Not Only Musicians Know Major and Minor" 2019). Because Model B is **transposition-invariant by design** (no absolute pitch ⇒ the candidate may be in a different key), the discrimination is being asked in exactly the configuration where untrained listeners fail. The "1 reliable bit" from mode is **`overclaimed`** unless the affect is preserved by *correlated* cues (tempo/articulation) — in which case it's double-counting style, not an independent bit. bit-budget §4 already softens this to "Mode/tonal-color 0.5–1," which is more defensible than README's flat 1 bit.
- **Tempo "fast vs slow" (S, 0.25–0.75):** defensible as a 1-bit-ish categorical only; the budget treats it so. OK.

**Verdict:** Law direction **SUPPORTED**; the **mode bit is overclaimed** for untrained, transposition-invariant Model B. README Q1's "1 bit" should be reconciled down to the bit-budget's 0.5–1 and explicitly conditioned on affect-via-correlates. `dedupe_key: mode-overclaimed`.

### Claim 6 — The 25–50-bit aspiration
**Design reliance:** `this.i:2p8z1m40`; bit-budget §4 (~19–28), §5 (curve).

**Evidence / precedent:** There is **no precedent in the literature that measures "information recovered from melody recognition" in bits.** The closest channel-capacity anchor is **Miller/Pollack: ~2.5 bits (≈6 categories) for one-dimensional absolute identification**, and ~2–3 bits per perceptual dimension generally. The visual analog (randomart): the persona's "~20–24 perceptual bits" is **not a measured result** — Loss/Limmer/von Gernler analyze the algorithm, not human perceptual capacity, and the consensus is randomart is good for *differentiation, not identification*. So **"no evidence found"** for any direct quantification on either side.

**What the literature *does* let us bound** (see Bit Ceiling below): summing **independent** perceptual dimensions each at their *absolute-identification* capacity. The design's §3 independence audit (joint cardinality, condition-on-style) is **methodologically the right move** and is *more honest than the additive v1*. The audited **19–28** for an 8-bar period is **broadly consistent** with a from-the-literature ceiling — *if* the per-row yields survive the decay/over-time discounts above. The **upper 45–50** sits **above** what the literature comfortably supports for *untrained, delayed, novel-melody* recognition and is correctly flagged "aspirational."

**Verdict:** The **floor (~20–25 at immediate/short delay) is plausible**; the **headline range's top (50) is unsupported** for Model B over time; "25–50" should be read as "~15–25 reliable over days, ~25–33 only at immediate test or with repeated exposure." `dedupe_key: bit-budget-overclaimed`.

### Claim 7 — Population & culture (WEIRD assumptions)
**Design reliance:** bit-budget §7 ("amusia ~4%"); the whole design's reliance on Western tonal grammar (major/minor, cadence, I–IV–V).

**Evidence:**
- **Amusia:** doc says **~4%**; the current best estimate is **1.5%** (Peretz & Vuvan 2017, N≈20k, objective). 4% is the obsolete 1980 single-test figure. (Erring high is *conservative* for budgeting, but the doc should cite the right number and note that amusics lose the *pitch/contour/mode* bits specifically, not timbre/rhythm — so the budget degrades *unevenly* under amusia, not uniformly.)
- **Cross-culture:** **major-happy / minor-sad is enculturated, not universal** (PNG 2022; NW-Pakistan; only dissonance-aversion is robust). entmotif doesn't claim *affect*, only *discriminability* — so this is a smaller hit than it first appears — BUT the **mode bit's only untrained-ear handle is the affective happy/sad framing (Claim 5)**, which **fails for non-Western listeners.** So mode contributes ~0 reliable bits for a non-Western, non-musician listener. The cadence/progression vocabulary (I–IV–V resolution feel in README) is likewise a learned Western grammar; its *recognizability* by non-enculturated listeners is **unestablished** (no evidence found).

**Verdict:** `inaccessible-cross-culture` for mode/cadence/progression bits; amusia figure `missing`/stale. The budget is **WEIRD-sample-bound** wherever it leans on tonal grammar; timbre/groove/texture-interruption bits travel better cross-culturally and should be weighted as the *culture-robust core*. `dedupe_key: mode-inaccessible-cross-culture`, `amusia-missing`.

---

## Executive Summary

entmotif's design is **more right than wrong**, and its single best-grounded pillar — **timbre/style as a durable, categorical, untrained-ear hook** — is squarely supported by the recognition-memory literature (Schellenberg & Habashi 2015; McAdams & Siedenburg 2019; Müllensiefen). The headline Model-B premise also holds up well: **novel melodies are recognized by unselected listeners with NO forgetting over a week after just two exposures.** The discrete/analog law's *direction* is correct, and zeroing absolute pitch/tempo for novel material is conservative and right.

The problems are concentrated in **which discrete dimensions the budget banks, and over what timescale**:

1. **Contour is mis-sold as durable.** The literature's most repeated melody-memory result is that **contour decays faster than interval over filled delays**; contour is the *short-term* hook. The 2.5–3 contour bits are an *immediate-test* figure, not a days-later one.
2. **Melodic rhythm is overclaimed.** Hébert & Peretz: rhythm is a **poor** long-term retrieval cue (melody >> rhythm). Co-equal 2.5–3 rhythm bits aren't supported; the *groove-bed* (a timbre+pattern gestalt) is the defensible part.
3. **"32–64 reliably-distinct genres = 5–6 bits" is overstated.** Fast genre recognition (Gjerdingen & Perrott) is real but ~44% / 10 genres / hugely uneven. The honest carrier is *pairwise-distinct timbre/texture gestalts*, not genre labels.
4. **The mode bit is overclaimed and culture-bound.** Non-musicians can't reliably discriminate *transposed* major/minor pairs (and Model B is transposition-invariant); they lean on happy/sad affect, which is **enculturated** and fails cross-culturally.
5. **"Recognition runs to the end" / late bound-transformation as recoverable bits is speculative.** Edworthy: shorter is recognized better; no evidence untrained ears recover a late theoretic transformation *from memory*. The integrity mechanism is sound *engineering* against the "identical-opening" attack but is **not** a demonstrated *perceptual* bit source.
6. **Amusia cited at the stale 4%** (now 1.5%, Peretz & Vuvan 2017), and degradation under amusia is *uneven* (kills pitch/contour/mode, spares timbre/rhythm) — not the uniform erosion §7 implies.

None of these is fatal. The bit-budget's **independence audit is the right methodology**, and its own §7 already lists most of these as open questions — this review *confirms and sharpens* them with citations. The corrective is: **lean harder on the culture-robust, categorical, durable carriers (timbre, groove-bed, texture-interruption), discount the decaying/contour/rhythm/mode carriers for the over-time case, and re-anchor the headline as a *short-delay* number with an explicit *days-later* haircut.**

---

## Top Findings (≤7)

- **ACA-F1 (HIGH):** Contour banked as durable; literature says it **decays** faster than interval over filled delays — the over-time Model-B residue is interval-in-tonality, which untrained ears recover *less* reliably. (`contour-decays-over-time`)
- **ACA-F2 (HIGH):** Melodic-rhythm bits (2.5–3, co-equal with contour) **overclaimed**; Hébert & Peretz show rhythm is a poor LTM cue. (`rhythm-overclaimed`)
- **ACA-F3 (HIGH):** Mode "1 bit" **overclaimed** for untrained, transposition-invariant Model B (can't discriminate transposed major/minor; rely on enculturated happy/sad). (`mode-overclaimed`)
- **ACA-F4 (HIGH):** "Recognition runs to the END" / late bound-transformation as a **recoverable** bit source is **unsupported**; Edworthy length gradient runs against it. Sound as anti-attack engineering, not as perception. (`transformation-unsupported`)
- **ACA-F5 (MEDIUM):** Style cardinality (32–64 reliable classes ⇒ 5–6 bits) **overstated**; genre recognition is fast but ~44%/10-genre uneven. Re-ground on pairwise timbre-gestalt distinctiveness. (`style-overclaimed`)
- **ACA-F6 (MEDIUM):** Mode/cadence/progression bits are **WEIRD-bound** (major-happy enculturated; non-Western listeners lose them). (`mode-inaccessible-cross-culture`)
- **ACA-F7 (LOW):** Amusia cited at stale **4%** (now **1.5%**, Peretz & Vuvan 2017) and degradation is **uneven**, not uniform. (`amusia-missing`)

(Note in the design's favor, not a finding: the timbre-durability literature **affirms** `b7p21m9z` and the §3 independence audit is methodologically sound.)

---

## Research-Grounded Bit Ceiling for novel-melody Model-B recognition

**Approach:** bound by summing *independent* perceptual dimensions, each at its *absolute-identification* capacity (Miller/Pollack: ~2–2.5 bits/dimension is the asymptote for a single perceptual axis), then apply an **over-time decay haircut** for the dimensions the literature says fade, and discount correlated/style-gated rows (the design's own audit move).

| Dimension | Lit. anchor | Immediate-test bits | Days-later bits |
|---|---|---|---|
| Timbre / instrument-family gestalt (style bed) | Categorical, durable; no 1-wk decay (S&H 2015; McAdams) | 3–4 | **3–4** (durable) |
| Genre/style *label* beyond timbre | G&P uneven, ~44%/10 | +0.5–1 | +0.5 |
| Melodic contour (opening shape) | Strong now, **decays** filled-delay (Dowling 1995; Edworthy) | 2–3 | **1–1.5** |
| Interval-in-tonality residue | Becomes dominant late, but harder for untrained | 1–2 | 1.5–2 |
| Rhythm / groove (as gestalt, not note durations) | Poor LTM cue alone (Hébert & Peretz); groove-bed ok | 1.5–2 | **1–1.5** |
| Mode (major/minor) | Untrained can't discriminate transposed; affect-only | 0.5–1 | **0–0.5** |
| Tempo band (fast/slow categorical) | Absolute tempo fades by 1 wk (S&H) | 0.5 | 0.25 |
| Meter feel (3 vs 4 vs 6/8) | Categorical, plausibly durable | 0.5–1 | 0.5–1 |
| Texture-interruption (foreign timbre event) | = categorical timbre, durable (rides on F-3 finding) | 1–1.5 | **1–1.5** |
| Cadence / progression family | Learned grammar; recoverability unestablished | 0.5–1 | 0.25–0.5 |
| Late bound-transformation (consequent) | No evidence untrained recover from memory | 0–1 | **~0** |
| Absolute key / pitch | No AP; decays first | 0 | 0 |
| Analog stack | margin only | 0 | 0 |

**Independence-discounted totals (8-bar period):**
- **Immediate / Model-A-adjacent test:** ~**18–26 bits** — consistent with the doc's §4 "~19–28."
- **Days-later, untrained, single-culture Model B (the doc's actual contract):** ~**11–18 bits**, centered **~14**. The durable core (timbre/style ≈ 4, contour-residue+interval ≈ 2.5–3.5, groove ≈ 1–1.5, texture-interruption ≈ 1–1.5, meter ≈ 0.5–1) carries most of it; mode/cadence/transformation contribute little over time.
- **Non-Western / no-tonal-enculturation listener:** subtract mode + cadence + progression ⇒ ~**9–14 bits**.

**Comparison to `docs/bit-budget.md` §5:** The doc's **8-bar "~19–28"** is a reasonable **immediate-test** estimate and I broadly endorse it as such. But the doc presents it as the *Model-B-over-time* number, and **the literature supports a meaningful haircut (~30–40%) once you move to days-later recognition by untrained ears.** A defensible restatement: **"~19–28 at immediate/short-delay test; ~12–18 reliable days later for an untrained, enculturated listener; the 45–50 top end is not supported for Model B over time."** The **25-bit floor "reliably reachable" claim in §5 is true only at immediate test or with ≥2 exposures of the *same* motif** (the Schellenberg consolidation condition) — which is actually a realistic deployment (a user hears their own key's motif repeatedly), and the doc should state that exposure assumption explicitly, because the entire 25-bit floor rests on it.

---

## Residual Unknowns (and the smallest study to settle each)

1. **Do the §4 D-row yields survive Model-B *over days*?** → A/B/X recognition study: hear motif twice, test old/new + same-style-lure at 10 min / 1 day / 1 week (the Schellenberg & Habashi paradigm, applied to entmotif's own renders). Settles F1–F4 at once.
2. **Is the late bound-transformation perceptually recoverable?** → 2AFC: present motif; later test target vs. a lure identical for bars 1–4 but with a *different* consequent transformation. If untrained d′≈0, F4 is confirmed and `9k3f0a72` should be reclassified as integrity-only (0 perceptual bits).
3. **How many pinned-font styles are *pairwise* reliably told apart, from memory?** → confusion-matrix listening test over the 32 candidate styles → effective log₂(distinct classes); replaces the asserted 5–6.
4. **Mode bit under transposition:** → same-melody major/minor pair, candidate transposed, untrained listeners, days later. Expected d′≈0 (predict F3 confirmed).
5. **Cross-cultural transfer:** the timbre/groove/texture bits *should* survive; the mode/cadence bits *should* not — testable with a non-Western, low-Western-exposure sample on the same A/B/X corpus.
6. **Amusia degradation profile:** test the ~1.5% amusic subset — predict they keep timbre/rhythm bits, lose pitch/contour/mode (uneven, not uniform).

---

## Findings manifest

```yaml
findings:
  - id: ACA-F1
    persona: music-perception-academic
    title: Contour banked as durable; literature shows it decays faster than interval over filled delays
    severity: HIGH
    confidence: LIKELY
    location: this.i:k20f9a3x / docs/bit-budget.md §4 (contour row)
    dedupe_key: contour-decays-over-time
    recommended_disposition: recommend-fix
    rationale: Dowling 1995, Edworthy 1985 — contour is the short-term hook; over-time residue is interval-in-tonality, harder for untrained ears. The 2.5-3 contour bits are an immediate-test figure.
    revisit_condition: null
    fix_effort: medium
    settling_experiment: A/B/X recognition (2 exposures; old/new + same-contour/diff-contour lures) at 10min/1day/1week per Schellenberg & Habashi 2015 paradigm on entmotif renders.
  - id: ACA-F2
    persona: music-perception-academic
    title: Melodic-rhythm bits overclaimed; rhythm is a poor long-term retrieval cue
    severity: HIGH
    confidence: LIKELY
    location: docs/bit-budget.md §4 (rhythmic-motif row, 2.5-3) / this.i:z0m4p81q
    dedupe_key: rhythm-overclaimed
    recommended_disposition: recommend-fix
    rationale: Hebert & Peretz 1997 — melody >> rhythm in LTM; rhythm alone poor. Schmuckler & Moranis 2023 rhythm-contour effect is short-term only. Co-equal 2.5-3 bits unsupported; only the groove-bed gestalt is defensible.
    revisit_condition: null
    fix_effort: small
    settling_experiment: Recognition test with rhythm-only vs melody-only vs combined lures at >=1 day; predict rhythm-only d' << melody-only.
  - id: ACA-F3
    persona: music-perception-academic
    title: Mode (major/minor) "1 bit" overclaimed for untrained, transposition-invariant Model B
    severity: HIGH
    confidence: LIKELY
    location: README.md Q1 (major/minor 1 bit) / docs/bit-budget.md §4 (mode row) / this.i:k20f9a3x
    dedupe_key: mode-overclaimed
    recommended_disposition: recommend-fix
    rationale: Non-musicians cannot discriminate same-melody major/minor pairs starting on different notes nor label them; they use happy/sad affect. Model B is transposition-invariant, so the discrimination is asked in the failing configuration. Reconcile README's 1 bit down to bit-budget's 0.5-1 and condition on affect-via-correlates.
    revisit_condition: null
    fix_effort: small
    settling_experiment: Same-melody major/minor pair, candidate transposed, untrained listeners, days later; expect d'~0.
  - id: ACA-F4
    persona: music-perception-academic
    title: "Recognition runs to the END" / late bound-transformation as a recoverable bit source is unsupported
    severity: HIGH
    confidence: SPECULATIVE
    location: this.i:9k3f0a72 / this.i:5p0z9k41 / docs/bit-budget.md §4 (consequent-transformation 2-3 bits)
    dedupe_key: transformation-unsupported
    recommended_disposition: recommend-fix
    rationale: Edworthy 1985 — shorter sequences recognized better; no evidence untrained listeners recover a late theoretic transformation (sequence/inversion/augmentation) from memory. Sound as anti-"identical-opening" engineering, but not a demonstrated perceptual bit source. Reclassify as integrity-only or shrink to ~0-1 over-time bits.
    revisit_condition: null
    fix_effort: medium
    settling_experiment: 2AFC target vs lure identical for bars 1-4 differing only in consequent transformation, untrained, days later; if d'~0, reclassify 9k3f0a72 to 0 perceptual bits.
  - id: ACA-F5
    persona: music-perception-academic
    title: Style cardinality (32-64 reliable classes => 5-6 bits) overstated vs genre-recognition literature
    severity: MEDIUM
    confidence: LIKELY
    location: docs/bit-budget.md §4 (style preset 5-6) / this.i:z0m4p81q / this.i:d4m1z8p0
    dedupe_key: style-overclaimed
    recommended_disposition: recommend-fix
    rationale: Gjerdingen & Perrott 2008 — genre recognition fast but ~44% over 10 genres, hugely uneven (classical 70%, blues <20%). Re-ground the 5-6 bits on pairwise timbre/texture-gestalt distinctiveness (b7p21m9z, well supported by Schellenberg & Habashi 2015 timbre durability) rather than on genre-labeling.
    revisit_condition: Confusion-matrix listening test yields >=32 pairwise-distinct gestalts through the pinned font.
    fix_effort: medium
    settling_experiment: Pairwise confusion-matrix listening test over the 32 candidate styles -> effective log2(distinct classes).
  - id: ACA-F6
    persona: music-perception-academic
    title: Mode/cadence/progression bits are WEIRD-sample-bound (major=happy is enculturated)
    severity: MEDIUM
    confidence: LIKELY
    location: this.i:k20f9a3x / README.md (chord-progression resolution table) / docs/bit-budget.md §4 (mode, cadence, progression rows)
    dedupe_key: mode-inaccessible-cross-culture
    recommended_disposition: recommend-defer
    rationale: PNG 2022 & NW-Pakistan studies — major-happy/minor-sad tracks Western exposure; only dissonance-aversion is robust. Non-Western non-musicians lose mode + cadence + progression bits. Timbre/groove/texture-interruption bits travel; weight those as the culture-robust core.
    revisit_condition: Cross-cultural A/B/X with a low-Western-exposure sample, or an explicit recorded scope decision to target Western-enculturated listeners only.
    fix_effort: small
    settling_experiment: Run the A/B/X corpus on a non-Western low-exposure sample; predict timbre/groove bits survive, mode/cadence bits do not.
  - id: ACA-F7
    persona: music-perception-academic
    title: Amusia cited at stale 4% (now 1.5%) and degradation modeled as uniform, not uneven
    severity: LOW
    confidence: CONFIRMED
    location: docs/bit-budget.md §7 (population variation)
    dedupe_key: amusia-missing
    recommended_disposition: recommend-fix
    rationale: Peretz & Vuvan 2017 (N~20k, objective MBEA) puts congenital amusia at 1.5%, not the obsolete 1980 single-test 4%. Amusics lose pitch/contour/mode bits but retain timbre/rhythm, so the budget degrades unevenly, not uniformly.
    revisit_condition: null
    fix_effort: small
    settling_experiment: Test the ~1.5% amusic subset on the A/B/X corpus; predict retained timbre/rhythm, lost pitch/contour/mode.
```
