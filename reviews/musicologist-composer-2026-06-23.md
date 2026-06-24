# Musicologist / Composer — Adversarial Design Review (entmotif)

**Run:** 2026-06-23 · mode=unattended · effort=deep · **ANALYSIS-ONLY** (I did not
listen by ear; audio judgments are marked SPECULATIVE pending a listening study).

---

## Evidence Inventory

What I read and analyzed (no new audio judged by ear):

- `this.i` — every node, with attention to `f7a2k930` (musicality), `9k3f0a72`
  (whole-motif integrity), `5p0z9k41` (8-bar period), `c2k9p0a4` (two-layer),
  `z0m4p81q`/`d4m1z8p0` (style), `b7p21m9z` (timbre).
- `docs/bit-budget.md` §1–§7 (the audited schedule and totals).
- `README.md` (the chord-progression resolution notes, §"Chord progressions").
- `AGENTS.md` §0 + bit-budget law.
- All three generators in `experiments/soundfont/` — `gen_test_midi.py`,
  `gen_style_midi.py` (7 style beds), `gen_style_midi2.py` (6 style beds). I
  hand-decoded the pitch content of every fragment to audit the theory.
- Confirmed the harness is real: `fluidsynth` present, both soundfonts
  (`GeneralUser-GS.sf2`, `MuseScore_General.sf3`) present, and prior renders
  (`render_test_styles*__*.wav`) already on disk — so the pipeline renders. I did
  **not** re-render to judge by ear (analysis-only); renderability is confirmed,
  musicality is not.

**Pitch-level audits performed (decoded from the generator source):**
- Sitar scale `[60,61,64,65,67,68,71,72]` = C Db E F G Ab B C → intervals
  1-3-1-2-1-3-1 → **Bhairav / double-harmonic**. The "Bhairav-flavored" label is
  **correct**.
- Chant "Dorian line" `[62,64,65,67,69,…,60,62]` over a D+A drone = D E F G A … C
  D. The mode-defining **6th degree (B♮ vs B♭) is never sounded**, and there is no
  C♯ leading tone either → the line is mode-**underdetermined** (could be D Dorian
  *or* D Aeolian). Labeling it "Dorian" is not supported by its own notes.
- Bossa "clave-ish" side-stick on eighth indices `(0,3,4,6)` of a 4/4 bar = a
  symmetric on-beat-ish pattern, **not** the bossa/son clave (3-2 or 2-3). See F4.
- Boogie bass `BOOG=[0,4,7,9,10,9,7,4]` = root-3rd-5th-6th-♭7 walk-up/down — a
  legitimate boogie cell. Bossa harmony Dm7↔G7 with no resolution — a ii-V loop
  that never lands (intentional vamp, but no cadence).

---

## Executive Summary

The design has the right *instincts* — style-as-bed, antecedent/consequent,
bound transformations, discrete/analog law — but the **single most important
musical mechanism it relies on does not exist in any artifact, and the existing
evidence cannot support the musicality claim it is being used to support.**

1. **The antecedent→consequent / half-cadence→authentic-cadence engine is
   undesigned and unbuilt.** `this.i:9k3f0a72` and `5p0z9k41` make the
   question/answer period the source of *both* whole-motif integrity *and*
   ~4–6 of the budget's bits (Consequent transformation 2–3 + Cadence type
   0.75–1.25, plus the contour/rhythm that the transformation operates on). Yet
   **all 13 style fragments in the generators are 4-bar single-phrase loops with
   no antecedent/consequent, no half cadence, and no resolving authentic
   cadence.** The project's entire body of evidence is silent on its
   load-bearing claim. This is the central design risk (F1).

2. **Nothing in the design constrains the melody to be a *motif* rather than an
   in-key walk.** The schedule allocates bits to "contour" and "rhythmic motif"
   but there is no specified mechanism for a memorable *hook* (a salient interval,
   a repeated rhythmic cell, a stepwise-then-leap gesture). Constrained generation
   as currently sketched will reliably produce *in-key, on-grid* lines — but
   in-key ≠ hummable. The hand-authored fragments are hummable *because a human
   composed each one*; the generative rules that would reproduce that quality are
   absent (F2).

3. **Strong-beat / harmony coordination is unspecified — the open door to ugly
   output.** There is no stated rule that strong-beat melody notes be chord tones,
   that leaps be resolved, or that the lead avoid clashing with the bed. With only
   a scale + contour + rhythm-cell schedule, entropy *will* place a 4th or a ♭7 on
   a downbeat against the wrong chord, and *will* emit an augmented-4th leap. This
   is the under-constraint failure the persona was told to hunt (F3).

4. **Two-layer "boogie-on-oud" has no register/idiom reconciliation, only a
   capability gate.** The capability gate rules out *gross* nonsense (zither can't
   drive boogie), but says nothing about the **bed's harmonic rhythm and the
   lead's idiom colliding** — a fast walking-boogie LH under a slow modal oud lead
   is "capable" yet musically incoherent. The gate's binary "can carry a lead" is
   too coarse for the clashes that actually occur (F5).

5. **Several style beds are generic or theoretically mislabeled at our fidelity.**
   Bossa lacks clave; reggae's skank is on the "and" of every beat rather than the
   characteristic 2-&/4-& upstroke emphasis with the one-drop; ragtime's
   secondary-rag syncopation is present in `RAG_DUR=[3,3,2]` (good) but the stride
   LH is rhythmically square. These read as *generic versions* of the genre (F6).

6. **The README chord-progression theory contains real errors** that, if they
   flow into the spec, will mislabel cadences and resolution. "I–V–vi–IV ends on
   the subdominant (IV)" — correct that it ends on IV, but it is called a "moderate
   openness" when IV→(loop back to I) is a **plagal** motion, and the doc never
   names a single cadence type. More seriously it conflates "ends on I" with
   "authentic cadence" (a I reached from IV is plagal, not authentic) (see Theory
   Corrections).

Net: the **musicality promise is currently unfalsifiable** — the artifacts that
would prove it (question/answer motifs with cadences, generated rather than
hand-composed) do not exist. The honest status is "promising scaffolding, core
engine unspecified," and the bit-budget rows that depend on that engine
(consequent transformation, cadence) should be treated as **not yet evidenced.**

---

## Top Findings (≤7)

### F1 — The antecedent/consequent + cadence engine is undesigned and unbuilt; ~4–6 budget bits rest on nothing testable. `[severity: CRITICAL]`

`this.i:9k3f0a72` ("the consequent is a BOUND TRANSFORMATION of the antecedent …
and resolves it"; "antecedent ends on a half cadence") and `5p0z9k41` make the
8-bar question/answer period the mechanism for **whole-motif integrity** and the
home of **C2/C3 bits**. `docs/bit-budget.md` §4 budgets *Consequent
transformation* at 2–3 bits and *Cadence type* at 0.75–1.25.

But **no generator produces an antecedent/consequent at all.** Every fragment in
`gen_style_midi.py` and `gen_style_midi2.py` is a 4-bar one-phrase loop:
- the bossa flute, sitar phrase, synthwave lead, western whistle, chant line,
  reggae/ballad/aria leads — each is a single through-composed line, not
  question-then-bound-answer;
- none ends its first half on a **half cadence** (dominant), and none ends its
  second half on a resolving **authentic cadence** (V→I with tonic in the
  melody). The bossa is an unresolved Dm7–G7 vamp; the synthwave is an Am–F–C–G
  loop (ends on G = dominant-ish, never resolves); the chant ends D→… on a drone,
  no cadence motion at all.

So the design's most important musicality mechanism — the thing that makes the
output a *motif with an arc* rather than a loop — has **zero supporting evidence**
and **no concrete specification** (the transformation set is named but no rule
says how entropy picks one, how it preserves identity, or how the cadence is
voiced). The two bit-rows it underwrites are unfounded until this exists.

*Settling experiment:* author 3–4 hand-built 8-bar periods (antecedent ending on
V, consequent = sequence / inversion / contrary-contour answer ending on V→I),
render them, and confirm by listening that (a) they're hummable and (b) the
answer relationship is audible. Until then the claim is unproven.

**dedupe_key:** form-missing-antecedent-consequent

---

### F2 — No specified mechanism yields a *hook*; constrained generation will reliably produce in-key-but-aimless lines. `[severity: HIGH]`

`f7a2k930` demands "hummable and pleasant," and the budget allocates bits to
"contour + opening gesture" and "rhythmic motif." But a hummable motif needs a
**salient, repeatable hook** — a characteristic interval (the minor-third of NBC,
the rising-4th of Wedding March), a *repeated* rhythmic cell (Beethoven 5's
short-short-short-long), a gesture that recurs. The design names "contour" and
"rhythm cell" as bit sources but specifies **no requirement that any cell
repeat**, that an interval be foregrounded, or that the phrase have an internal
parallelism. The hand-authored fragments are memorable only because a human gave
each one a shape; the *rules that would generalize that* are absent.

Concrete failure mode: with contour = "arch" + a scale + a rhythm cell + per-note
entropy pitch fill, the most likely output is a smooth in-key noodle — every note
defensible, the whole forgettable. "Legal notes" is the design's own stated
anti-goal in the persona brief, and the current schedule trends straight toward
it.

*Fix:* make repetition/parallelism a first-class generated structure — e.g. the
rhythmic cell of bar 1 MUST recur (literal or varied) in bar 2; designate one
"signature interval" per motif that the opening gesture must contain. This also
*adds* reliable bits (a recognizable hook is exactly a Model-B-recoverable
discrete feature).

**dedupe_key:** contour-unmusical

---

### F3 — No strong-beat/chord-tone or leap-resolution constraint → ugly output slips through (under-constraint). `[severity: HIGH]`

The contract (`AGENTS.md` §3 "Never emit a pitch/duration that music theory
wouldn't endorse for the chosen context") is asserted but **no rule operationalizes
it.** A scale-tone fill over a bed does NOT guarantee:
- **strong-beat consonance** — entropy can land scale-degree 4 or ♭7 on a downbeat
  against a tonic chord (a held, exposed dissonance, not a passing tone);
- **leap resolution** — nothing forbids a melodic tritone (e.g. F→B in C major) or
  a leap that isn't stepwise-recovered;
- **lead/bed non-clash** — the lead and the bed's comping voices can sound the
  same scale degree a half-step apart, or the lead can sit a M7/♭9 against a bass
  root with no preparation.

These are precisely the "wrong scale degrees on strong beats / awkward leaps /
lead-bed clash" failures the brief flags. With a per-note entropy fill and no
voice-leading guard, they are **not edge cases — they're the expected
distribution.**

*Fix:* specify (a) strong-beat notes restricted to chord tones (entropy chooses
*which* chord tone); (b) non-chord tones only on weak beats and only as
step-approached/step-left passing/neighbor tones; (c) a leap budget (max
interval, and leaps followed by step in the opposite direction); (d) a clash
check against the bed's sounding pitches. These are standard species-counterpoint
heuristics and they *narrow* the option space honestly.

**dedupe_key:** contour-unmusical-strong-beat (cluster with F2)

### F4 — Several style beds are generic or under-specified for the genre. `[severity: MEDIUM]`

At our fidelity the bed *is* the identity (`z0m4p81q`), so a generic bed costs
real style bits. Decoded specifics:
- **Bossa (`gen_style_midi.py` §3):** side-stick on eighth indices `(0,3,4,6)` is
  **not** a clave (neither 3-2 nor 2-3 son/bossa clave). Bossa is *defined* by
  clave; without it this reads as "generic Latin-ish." `[missing: clave]`
- **Reggae (`gen_style_midi2.py` §2):** skank chord on `beat + EIGHTH` for *every*
  beat (four even off-beats) is a generic backbeat-ish chop, not the
  characteristic reggae skank (emphasis on the "and" with the one-drop on 3). The
  one-drop kick+snare on beat 3 *is* correct — but the even skank dilutes it.
- **Ragtime:** `RAG_DUR=[3,3,2]` secondary-rag lilt is **correct and good**; the
  weakness is the perfectly square stride LH (no LH lilt, no walking).
- **Samba (`gen_test_midi.py` §3):** surdo on 2 and 4 is right; but the pattern
  is otherwise a generic shaker+side-stick grid, and samba's defining
  *teleco-teco*/tamborim syncopation is absent.

These won't fail outright but will **blur cross-style distinctiveness** — the
opposite of what `z0m4p81q` needs the bed to do.

*Settling experiment:* A/B the current bossa/reggae beds against
clave-/one-drop-corrected versions and confirm naive listeners label the genre
more reliably with the corrected device.

**dedupe_key:** style-indistinct-bed

### F5 — The two-layer capability gate is too coarse to prevent register/idiom/harmonic-rhythm clashes. `[severity: MEDIUM]`

`c2k9p0a4` reconciles bed×lead with a binary capability gate (register /
articulation / agility / projection) + soft affinity + override table. That stops
*gross* nonsense (zither can't drive boogie) but not the clashes a composer
actually hears:
- **Harmonic-rhythm mismatch:** a fast boogie bed (chord every bar, busy
  shuffle LH) under a slow, melismatic modal oud lead — both are "capable," the
  combination is incoherent because the lead's phrase rate fights the bed's.
- **Register collision:** a low bed (boogie LH down at C2–G2) with a low-tessitura
  lead (cello, bass clarinet) muddies; the gate's "register" axis checks the lead
  *can* play, not that lead and bed *separate*.
- **Idiom collision:** a swung-triplet bed under a straight-sixteenth lead idiom
  reads as two players in different rooms.

"Can carry a lead" is a *necessary* condition, not a *sufficient* one for musical
coherence. The design needs at least a register-separation rule and a
harmonic-rhythm/phrase-rate compatibility check, or an expanded override/ban
table — otherwise a meaningful fraction of the (style × lead) space is legal but
clashing, silently spending lead-instrument bits on unmusical combos.

**dedupe_key:** lead-instrument-unmusical-clash

### F6 — Chant mode is mislabeled / underdetermined; mode bits may not be Model-B-recoverable as claimed. `[severity: MEDIUM]`

`gen_style_midi.py` §7 labels its line "Dorian," but (decoded) the melody
`D E F G A … C D` over a D+A drone **never sounds the 6th degree** (B♮ would make
it Dorian; B♭ Aeolian) and **has no leading tone** — so the mode is
underdetermined by its own content. Two consequences:
1. The artifact does not demonstrate what it claims (a Dorian gestalt).
2. More generally, `docs/bit-budget.md` budgets *Mode / tonal-color* at 0.5–1
   bit, but **mode is only recoverable if the mode-defining degrees are actually
   foregrounded.** Dorian vs Aeolian differ by *one* note (the 6th); if the
   generated melody can avoid that note (as this hand-authored one does), the
   listener cannot recover the mode and the bit is not delivered. Major/minor (3rd
   degree, always present and salient) is safe; finer modal distinctions are
   **conditionally** recoverable and likely overclaimed unless the schedule
   *forces* the characteristic degree to sound on a strong beat.

*Fix:* if mode is to carry bits, require the mode-characteristic scale degree(s)
to appear prominently; otherwise demote modal color to analog (recognition
margin, 0 bits) per `k20f9a3x`.

**dedupe_key:** mode-overclaimed

### F7 — Hummability of the (future) long form is unaddressed; development risks un-reproducible-by-voice motifs. `[severity: LOW]`

`5p0z9k41`/`2p8z1m40` reach for 45–50 bits via a 12–16-bar AABA. The brief asks
whether an ordinary adult can still *sing* it. Two latent risks for when this is
built: (a) range — several existing leads already span wide (synthwave lead spans
~an octave-plus quickly; western whistle sits at MIDI 69–88, **above most adult
voices**, fine for whistle but a warning if the same contour rules drive a
"singable" target); (b) a "new contour + rhythm + transformation" third phrase
(per the budget's AABA row) adds *new* material — the more genuinely new material,
the less the whole is reproducible from memory. Whole-motif integrity
(`9k3f0a72`) and hummability are in *tension* at long form: integrity wants late
material to matter; hummability wants the whole to be a graspable gestalt. The
design should pick a singable ambitus (~a 10th) and bias long forms toward
*varied repetition* over new invention.

**dedupe_key:** form-unmusical-for-long-form

---

## Theory Corrections

1. **README "Chord progressions" conflates "ends on I" with authentic cadence.**
   A I chord *reached from IV* (e.g. "I–IV–vi–V–I" is fine — that's V→I authentic;
   but "ends on I" is asserted as strong resolution for progressions where the
   final motion isn't specified). The doc should name the **final two chords**:
   V→I = authentic (strong), IV→I = plagal (softer, "amen"), V→vi = deceptive,
   ending *on* V = half cadence (open). "Strong resolution to I" is only true when
   the I is preceded by V (or vii°). Recommend rewriting the list to annotate the
   *cadence type* (the actual carrier of "resolution") rather than just the last
   chord.

2. **"I–V–vi–IV ends on the subdominant (IV), leaving openness."** Correct that it
   ends on IV; but in a *looping* pop context the perceived motion is IV→I
   (plagal) when it repeats, which is a soft *resolution*, not "openness." The
   openness framing is right only for a single non-looped pass. State the context.

3. **Half cadence definition (load-bearing for `9k3f0a72`).** A half cadence ends
   on V (the *dominant*), creating the "question." `this.i` uses the term
   correctly in prose, but **no progression in the README ends on V labeled as a
   half cadence**, and no generator realizes one. The antecedent of the 8-bar
   period MUST end on V (or at minimum a non-tonic, dominant-functioning chord)
   with the **melody on a non-tonic, tension-bearing degree** (typically 2 or 7) —
   not merely "the last chord isn't I." This precision is missing.

4. **"Bound transformation … preserves identity while developing" — needs a
   correctness criterion.** Of the named set: *sequence* (transpose a figure to a
   new scale degree) and *inversion* (mirror the contour) genuinely preserve
   motivic identity; *augmentation* (lengthen durations) preserves pitch identity
   but **changes the rhythmic cell**, which is itself a claimed bit-carrier — so
   augmentation *trades* rhythmic-motif recognizability for development and may
   *reduce* Model-B recoverability of the rhythm. "Contrary-contour answer" is the
   weakest as an *identity* preserver — a contrary answer can be heard as a *new*
   phrase, not a transformation of the first. The set is plausible but the design
   must specify, per transformation, *what stays invariant* (so the listener hears
   "same idea, answered") — otherwise some transformations break integrity rather
   than enforce it.

5. **Sitar = Bhairav: correct.** (Verified: 1-3-1-2-1-3-1 semitone pattern.) Note
   that Bhairav is a *morning* raga with strong, specific ornamentation
   (andolan/oscillation on Db and Ab); the GM sitar + a literal MIDI scale will
   read as "exotic scale," not as *raga*, at our fidelity — claim "Indian-flavored
   modal," not "raga." SPECULATIVE pending listening.

---

## For human listening (SPECULATIVE — confirm by ear)

I did not listen. These are the renders/fragments a human should audition to
confirm or refute the findings above. All paths absolute.

1. **`/home/daniel/code/entmotif/experiments/soundfont/render_test_styles__GeneralUser-GS.wav`**
   — fragments 3 (Bossa, ~no clave, F4), 4 (Sitar, "raga" vs "exotic scale",
   Theory #5), 7 (Chant, "Dorian" with no 6th, F6). Listen for: does bossa read as
   bossa or generic-Latin? does the chant read as a *mode* at all?
2. **`/home/daniel/code/entmotif/experiments/soundfont/render_test_styles2__GeneralUser-GS.wav`**
   — fragment 2 (Reggae skank placement, F4), fragment 1 (Aria — already retired
   per `q9f3a7k2`; confirm Voice-Oohs really is indistinct from flute).
3. **A motif a human must compose first (does not yet exist):** a true 8-bar
   antecedent/consequent — antecedent ending on V with melody on ŝcale-degree 2,
   consequent = inversion or sequence ending V→I with melody on 1. Render and
   confirm hummability + audible question/answer. This is the F1 settling
   experiment and the single most important thing to hear.
4. **Adversarial under-constraint demo:** hand-place scale-degree 4 on the
   downbeat of a tonic bar, and a melodic tritone leap, in any style bed, render,
   and confirm the ugliness (F3) is as audible as predicted.

Because I cannot hear, **every musicality verdict above is theory/structure-based
and SPECULATIVE on the audio axis** until a human listens.

---

## Residual Unknowns

- Whether GeneralUser GS's leads (sitar, whistle, organ, choir) actually separate
  from a busy bed in a *full* arrangement (the fragments are sparse). Masking is
  the psychoacoustician's lens (`AUD`); flagged for handoff.
- Whether varied-repetition long forms stay hummable for ordinary adults — needs
  a singing-back study, not analysis.
- The actual delivered yield of "contour" and "rhythmic motif" once a *hook*
  constraint (F2) is imposed — could go *up* (a hook is recoverable) once
  specified.

---

```yaml
findings:
  - id: MUS-F1
    persona: musicologist-composer
    title: Antecedent/consequent + cadence engine is undesigned and unbuilt; ~4-6 budget bits rest on no testable artifact
    severity: CRITICAL
    confidence: LIKELY
    location: this.i:9k3f0a72
    dedupe_key: form-missing-antecedent-consequent
    recommended_disposition: recommend-fix
    rationale: The headline musicality+integrity mechanism (half-cadence antecedent -> bound-transformation consequent -> authentic cadence) has zero supporting artifacts; all 13 generator fragments are 4-bar single-phrase loops with no question/answer and no cadence, so the C2/C3 + cadence bit rows are unevidenced.
    revisit_condition: null
    fix_effort: large
    settling_experiment: Hand-author 3-4 true 8-bar periods (antecedent ending on V/melody on degree 2; consequent = sequence or inversion ending V->I/melody on 1), render, and confirm hummability + audible question/answer by ear.
  - id: MUS-F2
    persona: musicologist-composer
    title: No specified hook/repetition mechanism; constrained generation trends to in-key-but-aimless lines
    severity: HIGH
    confidence: LIKELY
    location: this.i:f7a2k930
    dedupe_key: contour-unmusical
    recommended_disposition: recommend-fix
    rationale: Budget allocates bits to contour and rhythm cell but nothing requires a salient interval or a repeated/parallel cell; in-key fill over a bed yields legal-but-forgettable noodling, the design's own anti-goal. The hand-built fragments are memorable only because a human shaped each.
    revisit_condition: null
    fix_effort: medium
    settling_experiment: Generate motifs with vs without a forced rhythmic-cell repetition + a designated signature interval; A/B/X whether listeners recall the hook-constrained ones better.
  - id: MUS-F3
    persona: musicologist-composer
    title: No strong-beat chord-tone / leap-resolution / lead-bed clash constraint -> ugly output is the expected distribution
    severity: HIGH
    confidence: LIKELY
    location: docs/bit-budget.md §4
    dedupe_key: contour-unmusical-strong-beat
    recommended_disposition: recommend-fix
    rationale: AGENTS.md asserts "never emit a pitch theory wouldn't endorse" but no rule operationalizes it; per-note entropy fill over a scale will land dissonant strong-beat degrees, melodic tritones, and lead/bed half-step clashes - the brief's under-constraint failure, and not an edge case.
    revisit_condition: null
    fix_effort: medium
    settling_experiment: Hand-inject a downbeat scale-degree-4 and a melodic tritone into a bed, render, confirm audible ugliness; then verify species-counterpoint guards (strong beat=chord tone, NCTs step-approached, leap budget) remove it.
  - id: MUS-F4
    persona: musicologist-composer
    title: Bossa/reggae/samba beds lack defining devices (clave, true skank, teleco-teco); read as generic genre
    severity: MEDIUM
    confidence: LIKELY
    location: this.i:z0m4p81q
    dedupe_key: style-indistinct-bed
    recommended_disposition: recommend-fix
    rationale: At our fidelity the bed carries identity; decoded patterns show bossa side-stick (0,3,4,6) is not son/bossa clave, reggae skank is an even off-beat chop not the characteristic and-emphasis one-drop skank, samba lacks tamborim syncopation - blurring the cross-style distinctiveness z0m4p81q depends on.
    revisit_condition: null
    fix_effort: small
    settling_experiment: A/B current vs clave-/one-drop-corrected beds; confirm naive listeners label the genre more reliably with the corrected device.
  - id: MUS-F5
    persona: musicologist-composer
    title: Two-layer capability gate too coarse - allows register/idiom/harmonic-rhythm clashes (boogie-on-oud failure modes)
    severity: MEDIUM
    confidence: SPECULATIVE
    location: this.i:c2k9p0a4
    dedupe_key: lead-instrument-unmusical-clash
    recommended_disposition: recommend-fix
    rationale: A binary "can carry a lead" gate stops gross nonsense but not fast-bed/slow-melismatic-lead phrase-rate fights, low-bed/low-lead register muddying, or swung-bed/straight-lead idiom collisions; a fraction of (style x lead) is legal-but-clashing, silently spending lead bits on unmusical combos.
    revisit_condition: null
    fix_effort: medium
    settling_experiment: Enumerate ~10 deliberately mismatched style x lead pairs (e.g. boogie bed + slow oud lead), render, and confirm by ear which "capable" combos are musically incoherent; derive register-separation + phrase-rate compatibility rules.
  - id: MUS-F6
    persona: musicologist-composer
    title: Modal color (Dorian etc.) is underdetermined/mislabeled and likely not Model-B-recoverable as budgeted
    severity: MEDIUM
    confidence: LIKELY
    location: docs/bit-budget.md §4
    dedupe_key: mode-overclaimed
    recommended_disposition: recommend-fix
    rationale: The chant fragment labeled "Dorian" never sounds its mode-defining 6th (B-nat vs B-flat) - the mode is undetermined by its own notes; modes differing by one degree are recoverable only if that degree is foregrounded, so the 0.5-1 mode bit is overclaimed unless the schedule forces the characteristic degree to sound prominently. Major/minor (3rd, always salient) is safe.
    revisit_condition: null
    fix_effort: small
    settling_experiment: Recognition study: can listeners distinguish Dorian vs Aeolian renders when the 6th is/ isn't foregrounded? If not foregrounded -> demote mode to analog (0 bits).
  - id: MUS-F7
    persona: musicologist-composer
    title: Long-form (AABA 12-16 bar) hummability vs whole-motif integrity tension is unaddressed; range/new-material risk
    severity: LOW
    confidence: SPECULATIVE
    location: this.i:5p0z9k41
    dedupe_key: form-unmusical-for-long-form
    recommended_disposition: recommend-defer
    rationale: The 45-50-bit AABA lever adds new contour+rhythm late; whole-motif integrity wants late material to matter while hummability wants a graspable gestalt - in tension. No singable ambitus is specified and existing leads already exceed adult vocal range. Defer until long form is actually designed.
    revisit_condition: When the 12-16-bar AABA form is specified or implemented.
    fix_effort: medium
    settling_experiment: Sing-back study on hand-built AABA motifs biased toward varied repetition vs new invention; pick the ambitus (~a 10th) and repetition ratio that stays reproducible.
```
