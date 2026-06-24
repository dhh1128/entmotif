# Adversarial Design Review — Synthesis (2026-06-23)

**Panel:** BIT (bit-budget/determinism), ACA (music-perception literature), MUS
(musicologist/composer), AUD (psychoacoustician), ADV (collision adversary).
Run as subagents; MUS & AUD in analysis-only mode (no listening). Per-persona
reports in this directory. This file merges by `dedupe_key`, clusters
semantically, and adjudicates. **No `this.i` was written autonomously** — the
recommended actions below await maintainer ratification.

## Executive summary

The **architecture is sound and was independently praised** by multiple
reviewers: style-as-bed, the discrete/analog law, the two-layer style↔lead
model, hash-first derivation, the fidelity gate, and "weird-but-distinct timbre
helps." The problems are in **the numbers, the unbuilt core, and the honesty of
the boundaries** — not the foundations.

Three things every relevant persona agreed on:

1. **The 25–50-bit headline is overclaimed.** Two fully independent estimates —
   BIT's joint-cardinality re-derivation and ACA's literature-grounded ceiling —
   land at **~12–21 bits at immediate test, ~12–18 days later, ~9–14 for
   non-Western or amusic listeners or phone-speaker playback.** 25 is reachable
   only at the optimistic edge with the (still-unbuilt) 3rd-phrase form; ~50 is
   unsupported.
2. **The core motif/question-answer engine does not exist**, so the musicality
   claim and ~4–6 of the budgeted bits rest on no artifact (all 13 demo
   fragments are 4-bar single loops).
3. **The whole-motif-integrity defense is perceptually inert and the
   consequent-transformation is not a recall-bit source** — ADV constructed a
   byte-distinct pair sharing the whole antecedent; ACA found no evidence
   untrained listeners recover a late theory transformation from memory.

None is fatal. The net is a **downward recalibration + a concrete build agenda +
a set of listening studies that must run before any number is trusted.**

## Merged finding queue (ranked; most-obligated severity wins)

| # | Cluster (dedupe) | Sev | Reporters | Recommended disposition |
|---|---|---|---|---|
| 1 | **musicality-engine-unspecified** — antecedent/consequent + cadence + hook + strong-beat constraints undesigned/unbuilt | CRITICAL | MUS-F1, F2, F3 | **fix** — this is the next design/build task; the musicality promise is currently unfalsifiable |
| 2 | **bit-budget-overclaimed** — ~12–21 not 25–50; `this.i` (25–33) and doc (19–28) disagree; contour/rhythm/mode/style/tempo individually overclaimed | CRITICAL (headline) | BIT-F1,F2,F7; ACA-F1,F2,F3,F5; AUD-F6; MUS-F6 | **fix** — revise down, reconcile this.i↔doc, add (time/device/hearing/culture/exposure) qualifiers |
| 3 | **collision-grindable + boundary-unstated** — Model-B second-preimage ~2¹³ for a habituated victim; anti-claim not surfaced at point of trust | CRITICAL | ADV-F1,F4,F5,F6,F7; BIT-F6 | **accept-risk + document** (relaxed crypto is by design, `m4z81p3v`) — but ADV-F7 (explicit "a matching motif is not proof of a matching input") is a **fix** |
| 4 | **transformation-not-perceptual / integrity-inert** — late bound-transformation gives ~0 recall bits; "no ignorable tail" doesn't hold under Model B | HIGH | ACA-F4, ADV-F2, (MUS-F1) | **fix** — reclassify C2/C3 to integrity-engineering, ~0–1 perceptual bits, pending a study; reconcile `9k3f0a72` |
| 5 | **analog-stack-overclaimed** — cannot claim *0 recall bits* AND *collision-hardening / big consumed margin* from the same layers; consumed≈delivered | HIGH | BIT-F3, ADV-F3, AUD-F1 | **fix** — rewrite §2; analog = Model-A margin + casual avalanche only; drop or re-derive the `2^-consumed` machine-collision claim from real MIDI resolution |
| 6 | **accessibility-erodes-below-floor** — phone-speaker & amusia both drop below the 25 floor; timbre count collapses lo-fi; masking; cross-culture; amusia mis-stated (4%→~1.5%) | HIGH | AUD-F1,F2,F3,F4,F7; ACA-F6,F7 | **fix** numbers+qualifiers+masking constraint; **defer** cross-culture with a recorded scope decision |
| 7 | **style-bed-authenticity + mode** — bossa/reggae/samba lack defining devices (clave, one-drop, teleco-teco); modal color needs its characteristic degree foregrounded; lead/bed clash gate too coarse | MEDIUM | MUS-F4,F5,F6; ACA-F3 | **fix** when building the beds |
| 8 | **determinism hazards** — tempo/timing float-rounding into MIDI; modulo bit-reader bias; discrete-gestalt avalanche unquantified | MEDIUM/LOW | BIT-F4,F5,F6 | **fix** at implementation (cheap; record requirements now) |
| 9 | **long-form-hummability** — AABA integrity-vs-singability tension; no specified ambitus | LOW | MUS-F7 | **defer** until long form is designed |

## Recommended `this.i` / doc actions (await ratification)

- Revise `[2p8z1m40]` + `docs/bit-budget.md` to **~12–21 (immediate)** with
  explicit qualifiers; **reconcile this.i↔doc**; state the **exposure assumption**
  (the floor needs ≥2 exposures of the same motif).
- Reclassify `[9k3f0a72]` consequent-transformation as **integrity engineering**,
  0–1 perceptual bits pending a study.
- Rewrite consumed≠delivered (§2): drop/recompute the machine-collision claim;
  **analog = Model-A margin only** (update `[e9k2m4p1]`).
- Add an **anti-claim node**: *recognition is not cryptographic evidence; use byte
  comparison for trust-bearing checks* (relate to `[m4z81p3v]`); plan to surface
  it at the point of trust in any UI.
- Fix amusia prevalence **4% → ~1.5%** and note **uneven** degradation (kills
  pitch/contour/mode, spares timbre/rhythm).
- Record **determinism requirements**: whiten a full-width fingerprint expansion
  per choice (avalanche on the discrete gestalt); rejection-sample non-2^k reads;
  integer tempo/timing.
- Add **bed-device authenticity** + **masking-budget** + **register/phrase-rate
  compatibility** as design tasks for the generator.

## For human listening (needs the maintainer's ears — all currently SPECULATIVE)

1. **The most important thing to hear (does not exist yet):** hand-author and
   render a **true 8-bar antecedent/consequent** motif — antecedent ending on V
   (melody on degree 2), consequent = sequence or inversion ending V→I (melody on
   1) — and confirm hummability + an *audible* question/answer. Settles MUS-F1.
2. **ADV's constructed collision pair** at `/tmp/entmotif-adv/` (byte-distinct
   MIDI+WAV sharing the whole antecedent) — listen and judge Model-B
   confusability. Settles ADV-F2. (Move into the repo if you want to keep it.)
3. **Phone-speaker pass** on `render_test_styles*__GeneralUser-GS.wav` — do the
   bass/drone beds survive? Settles AUD-F1.
4. **Boogie** — is the RH-stab contour (vel 78) intelligible under the LH bass
   (vel 96)? Settles AUD-F4.
5. **Bed corrections** — A/B current vs clave-/one-drop-corrected bossa & reggae.
   Settles MUS-F4.

## The real settling experiment (the whole budget rests on it)

An **A/B/X recognition study** on entmotif renders at **10 min / 1 day / 1 week**
delays (Schellenberg & Habashi 2015 paradigm), with lures that match
style+opening+rhythm but diverge in the consequent, split by amusia screen
(MBEA) and ideally a low-Western-exposure sample. This fits N(t) per dimension
and converts every estimated `D`-bit in `docs/bit-budget.md` into a measured one.
