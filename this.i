# Entmotif Intent File
# Component: entmotif
# Format: intent code
#
# IDs are OPAQUE and meaningless on purpose (rename stability): all semantics
# live in the node NAME, which can be renamed freely without breaking [[id]]
# cross-links. Never encode meaning into an id.

Entmotif = goal:
  id: 7q2f9a0k
  why: >
    Turn a high-entropy value (key, signature, UUID, address, hash) into a
    short, hummable musical motif so an ordinary adult can RECOGNIZE it by ear.
    The audible sibling of entviz. Inherits entviz's input-normalization and
    intent/TDD craft, but accepts different constraints (see children).

  children:

    Recognition Not Comparison = decision:
      id: m4z81p3v
      why: >
        The job is recognition from memory (Model B): a listener who heard motif
        X can later decide, from memory, whether a candidate is X. NOT lossless
        reconstruction or bit-comparison by ear. Stored-and-replayed comparison
        (Model A) is strictly easier and comes for free. This relaxes the
        cryptographic rigor entviz needed: we still hash for avalanche and
        arbitrary-length input, but the bar is "two different inputs reliably
        sound different to a human," not collision resistance. Drives [[k20f9a3x]].

    Discrete Vs Analog Bit Law = constraint:
      id: k20f9a3x
      why: >
        Reliable, human-recoverable bits come ONLY from discrete musical
        decisions an untrained ear can re-identify (major/minor, rises/falls,
        meter feel, which instrument, which style). Analog variables (exact
        pitch, exact tempo, micro-timing, dynamics) give recognition margin and
        pleasantness but carry NO countable bits — read with perceptual
        tolerance. Inherited from entviz this.i:d1scr3t3, recast for sound.
        Every output dimension must be classed D/A/S and only D/S count toward
        the 25-50 bit budget. A design that claims bits from an analog dimension
        is wrong. See [[2p8z1m40]].

    Bit Budget 25 To 50 = goal:
      id: 2p8z1m40
      why: >
        Carry ~25-50 bits RELIABLY (recoverable by recognition, not
        transcription) at the OPTIMISTIC / IMMEDIATE end for a TYPICAL listener
        (Western-enculturated, normal-hearing, >=2 exposures). docs/bit-budget.md
        is the authoritative breakdown -- do NOT restate divergent numbers here
        (this node previously said "25-33" and the doc said "19-28"; reconciled
        2026-06-23 by deferring to the doc). Per the doc: the v1 8-bar period is
        an ESTIMATED ~19-28 reliable bits at immediate test, unmeasured; ~25
        reliably wants the 3rd-phrase extension; ~50 is aspirational (longest/
        richest form). The figure is CONDITIONED and erodes over long unrehearsed
        delays, lo-fi playback, amusia (~1.5%), and non-Western listeners (see
        [[6b2k9p0a]] and docs/references.md). Consumed fingerprint bits >>
        delivered (machine-distinct MIDI vs lossy human recall). Full schedule:
        docs/bit-budget.md. Depends on [[k20f9a3x]], [[9k3f0a72]], [[z0m4p81q]];
        grounded by [[6b2k9p0a]].

    Musicality Over Distinctiveness = constraint:
      id: f7a2k930
      why: >
        Entropy MUST NEVER be mapped to arbitrary tones directly (that is noise,
        not a motif). Music theory defines the space of acceptable outputs;
        entropy chooses among the valid options. Every emitted note/chord/rhythm
        must be defensible as a deliberate musical choice. Aesthetic target:
        hummable and pleasant, not maximally distinct.

    Hash First Then Choose = decision:
      id: 81pz4m0v
      why: >
        Derive a fingerprint = SHA-512 of the canonical normalized input TEXT
        (reuse entviz's presentation/identity/annotation parsing; hash text, not
        decoded bytes). Drive every musical choice from fingerprint bits via a
        documented, ordered consumption schedule, not from the raw input. Gives
        avalanche (one-char change => clearly different motif) and handles any
        input length. entviz's `entropy` parser is the normalization oracle.

    Whole Motif Integrity = constraint:
      id: 9k3f0a72
      why: >
        No ignorable tail: later bars MUST influence the gestalt the listener
        remembers, so recognition runs to the END. Failure mode to kill: motifs
        identical for the opening, diverging only late, accepted after the
        opening. Mechanism: antecedent ends on a half cadence (question); the
        consequent is a BOUND TRANSFORMATION of the antecedent (sequence,
        inversion, augmentation, contrary-contour answer) and resolves it. The
        relationship is part of the remembered gestalt and is undetectable from
        either half alone, so the transformation choice both carries bits and
        enforces integrity. The input-side ("identical opening") attack is
        already hard cryptographically; this constraint covers the PERCEPTION
        side. Drives C2/C3 in docs/bit-budget.md. Relates to [[2p8z1m40]].

    V1 Form Eight Bar Period = decision:
      id: 5p0z9k41
      why: >
        v1 renders an 8-bar ANTECEDENT-CONSEQUENT period as the motif unit
        (~25-33 reliable bits). The antecedent ends on a half cadence
        (question); the consequent is a bound transformation of it and resolves
        (answer) — this is where [[9k3f0a72]] (whole-motif integrity) is
        enforced and where C2/C3 bits come from. A 3rd-phrase / AABA extension
        to ~12-16 bars is the documented, non-breaking lever toward 45-50 bits
        later, NOT a v1 requirement. Implements [[2p8z1m40]] and [[9k3f0a72]].

    Style Is Master Dimension = decision:
      id: z0m4p81q
      why: >
        Genre/style is the strongest, most redundant, most memorable Model-B
        hook (non-musicians are expert genre classifiers) AND a large entropy
        carrier. Modeled as a master preset (v1 ~32 => 5 bits, expandable to
        ~64 => 6 bits) that GATES instrument palette, groove, mode, harmonic
        vocabulary, tempo band, meter tendency, and idiom. Breadth is a
        first-class goal: world, pop, jazz, ragtime, electronic, film, folk,
        sacred — never classical-only. For many styles (samba, funk, ragtime,
        reggae) the groove+timbre bed carries identity BEFORE any melody, so the
        arrangement bed is co-equal with the melody, not a backing afterthought.
        Constrained by [[3k7a92f0]].

    Render Fidelity Graceful Degradation = constraint:
      id: 3k7a92f0
      why: >
        A style earns recognition bits only if distinguishable THROUGH our
        actual synth (entviz analog: stay legible in 256 colors / grayscale).
        The portable .mid file carries generic timbres and is the deterministic
        source of truth; the WEB PLAYER's soundfont is PINNED in the spec (like
        entviz pins a reference rasterizer) and delivers style-faithful timbre.
        Styles are curated by renderable distinctiveness: faithful styles claim
        full bits; approximate ones (microtonal maqam, heavy production) claim
        less; styles that cannot survive the pipeline are DEFERRED, not claimed.
        See [[q9f3a7k2]].

    Vocal Character Deferred = decision:
      id: q9f3a7k2
      why: >
        We cannot sing words — only open vowels. So open-vowel styles work
        (Gregorian chant; maybe scat / McFerrin-style), but lyric-driven vocal
        identity (Dylan, Beach Boys/Queen harmony) does not. Vocal-character
        styles are deferred to a future "needs real vocal samples" path and are
        NOT claimed in the v1 budget. Consequence of [[3k7a92f0]].
        UPDATE (2026 listening test): the SOLO-voice patch (Voice Oohs) in
        GeneralUser GS is NOT distinct from flute / other mid-leads, so the
        operatic ARIA is DROPPED, and scat would fail the same way. In v1 the
        only surviving vocal style is GREGORIAN CHANT, and it survives on its
        BED (modal + bare-fifth drone + ensemble choir), not on solo-voice
        timbre. So the rule tightens: ensemble chant only.

    MIDI Canonical Plus Web Player = decision:
      id: 4m1zp870
      why: >
        MIDI is the primary, canonical, DETERMINISTIC output (entviz's SVG
        render-model analog: exactly reproducible, byte-diffable). Rendered audio
        (WAV/FLAC via synth + pinned soundfont) is a listening convenience and is
        NOT bit-reproducible across synth/soundfont versions — treated like
        entviz treats its PNG raster (regenerable, perceptual, never the source
        of truth). Stack: Python core renderer + a JS/web player using the pinned
        soundfont for style-faithful playback. The audible regression surface is
        a "songbook": a fixed corpus of inputs rendered to MIDI, byte-checked in
        CI exactly as entviz checks its gallery. Implements part of [[3k7a92f0]].

    Pinned Soundfont GeneralUser GS = decision:
      id: 8a3k0f29
      why: >
        v1 pins GeneralUser GS (SF2-native, ~30 MB, permissive free-for-any-use
        license incl. commercial) as the canonical/web reference soundfont,
        rendered via FluidSynth everywhere (CLI offline + js-synthesizer WASM in
        the web player) for timbre parity. Chosen over MuseScore_General (MIT,
        ~38 MB) NOT on quality (near-identical; MuseScore's sitar slightly
        crisper, GeneralUser's slightly muddy) but on the SF2-vs-SF3 web
        tiebreaker: GeneralUser is SF2 and stays ~30 MB in the browser, while
        MuseScore_General is SF3 (browser WASM Vorbis support is build-dependent)
        and its SF2 form is ~200 MB+. MuseScore_General may still be used inside
        MuseScore for composing. Tentative — revisit if web/license needs shift.
        Implements [[3k7a92f0]]; listening test in experiments/soundfont/.

    Timbre Distinctiveness Not Realism = decision:
      id: b7p21m9z
      why: >
        The metric for the instrument palette is PAIRWISE DISTINCTIVENESS, not
        realism or nameability. A listener need not name a timbre or find it
        "real" — "weird"/synthetic timbres are fine and may even HELP
        recognition. What matters is that any two palette timbres are reliably
        told apart through the pinned font. Consequence: collapse near-duplicate
        timbres to one slot. Empirically confusable clusters from the v1
        listening test (each = ONE class): {accordion, bandoneon, harmonica}
        (free-reed); {pan flute, ocarina} (breathy flute); {shakuhachi -> reads
        as marimba/mallet}. Lead-instrument bit yield = log2(# pairwise-distinct
        timbre classes), gated by [[z0m4p81q]] (style); the v1 test already
        yields ~18-20 classes (~4 bits before gating). Also opens the GM
        synth/FX programs (80-103) as extra distinct classes. Sharpens F5 in
        docs/bit-budget.md. Refines [[3k7a92f0]].

    Two Layer Style Instrument Model = decision:
      id: c2k9p0a4
      why: >
        Style and lead instrument are PARTIALLY CORRELATED, not free and not
        locked. Two layers: (1) the STYLE owns the "bed" — groove, bass,
        harmonic rhythm, mode/scale, tempo band, meter — which is what makes it
        that style; (2) the LEAD INSTRUMENT is a separate choice layered on top,
        so "boogie-woogie on an oud" works (boogie bed + oud lead). The lead is
        picked by: a CAPABILITY GATE (hard — instrument capability tags like
        register/articulation/agility/projection rule out nonsense generically,
        e.g. zither cannot carry a driving boogie lead) + an AFFINITY WEIGHT
        (soft — a style's signature instruments are common, weird-but-allowed
        ones rarer) + a small OVERRIDE table (force chant->voice; ban specific
        ugly combos). Authoring stays small: ~8 capability axes per instrument +
        a requirements clause and signature list per style, NOT a full NxM
        matrix. Consequence: the lead-instrument bit yield is style-dependent
        (~log2 effective allowed-pool size). Builds on [[z0m4p81q]],
        [[b7p21m9z]]; overrides realize the strong cases noted in [[q9f3a7k2]].
        Extended (c2k9p0a4) to the RHYTHM SECTION: comp and bass are no longer one
        fixed program per style. Each draws from a capability-tagged pool (ATTACK
        0..2 = how sharply a timbre articulates an offbeat/plucked groove) with
        per-style affinity (signature ~80%, capability-passing alternates rare).
        The gate forbids a sustained organ/pad bass for a syncopated groove
        (reggae skank / funk stabs / salsa montuno need sharp attack) and bans
        brass from the oom-pah comp (the march "collection of horns" was ugly ->
        a lighter reed). Keyboard-bed styles (ragtime/boogie) keep comp==bass==
        the piano left hand. Adds independent Chooser labels "comp"/"bass" (no
        perturbation of existing draws — each label hashes independently).

    Rhythm Pattern Variety = decision:
      id: r4d8m1k6
      why: >
        The two-layer "signature common, alternates rare" model [[c2k9p0a4]],
        first applied to the rhythm section's INSTRUMENT, is now extended to its
        RHYTHM. v12 #08 complaint: the comp/bass grooves read as a single
        strong/weak alternation per style. Fix: each style's signature comp_pat /
        bass_pat names a small FAMILY of idiomatic, metric-CONSERVING variants
        (COMP_PAT_VARIANTS / BASS_PAT_VARIANTS in arrangement.py) — e.g. swing
        walking <-> walking_skip, ragtime/march stride <-> stride_octave, blues
        shuffle <-> shuffle_jab, jazz comp4 <-> charleston, reggae skank <->
        skank_double, salsa montuno <-> montuno_synco, bossa <-> bossa_partido.
        The fingerprint draws a variant per input (new independent Chooser labels
        "comp_pat"/"bass_pat", so existing draws are unperturbed); the signature
        keeps ~70% affinity (PAT_SIG_W) and each variant is reachable-but-rarer.
        Every variant fills exactly one bar on the 16th grid [[m9p3k7a2]] and
        stays inside the idiom (capability gate still keys off the BASE pattern,
        since variants share its attack demands). Result: the same style's groove
        rhythm differs across inputs instead of being one fixed cell, consuming
        more of the hash with musically-valid choices [[h0v4k7m2]]. Refines
        [[c2k9p0a4]]; conserves [[m9p3k7a2]].

    Style Inventory Size = decision:
      id: d4m1z8p0
      why: >
        v1 ships ~32 styles (5 bits), expandable toward ~64 (6 bits) as a
        non-breaking growth. Each style MUST pass three disciplines: (a)
        pairwise-distinct as a gestalt [[b7p21m9z]]; (b) renderable in the
        pinned font [[8a3k0f29]]; (c) expressible in the melody + light-harmony
        + groove form. Open-vowel solo voice (chant, aria, scat) is the allowed
        vocal subset; lyric-driven vocal is deferred [[q9f3a7k2]], and aria is
        fidelity-gated on the solo-voice patch. The inventory spans
        keyboard/jazz/blues, classical, Latin/Caribbean, world
        (Asia/Mideast/folk), Americana/country, pop/rock/electronic, film/mood,
        sacred/vocal, and solo/novelty (incl. SFX-bank timbres). Combined with
        [[c2k9p0a4]] (each style x its lead pool) and [[b7p21m9z]] (weird-OK),
        the perceptual space is far larger than the raw style count. Realizes
        [[2p8z1m40]] and [[z0m4p81q]].

    Analog Layers For Aggregate Divergence = decision:
      id: e9k2m4p1
      why: >
        Beyond the discrete, bit-bearing decisions, deliberately layer MANY
        analog choices: dynamics (velocity), articulation (staccato/legato/
        accent), micro-timing / swing depth, rubato, note-length variation,
        ornament density, register shading, brightness/filter (CC), vibrato
        depth, pan. These carry NO reliable Model-B recall bits (see
        [[k20f9a3x]]) — a listener cannot recover them from memory — but they
        (1) raise Model-A (side-by-side) distinguishability; (2) consume EXTRA
        fingerprint bits, so the rendered MIDI reflects more of the whole input
        and machine collisions fall toward ~2^-consumed (the consumed>>delivered
        margin in [[2p8z1m40]]); and (3) provide casual avalanche: any honest
        one-character input change perturbs every analog layer, so two inputs
        that happen to share most DISCRETE choices still diverge audibly in the
        aggregate. Design rule: every discrete choice sets a BASE value; a stack
        of analog layers then modulates within perceptual tolerance, each
        drawing fresh fingerprint bits. Plan for plenty of them. Refines
        [[k20f9a3x]].

    Heterogeneous Texture As Distinctiveness = decision:
      id: f3a0k9m2
      why: >
        Listening-test finding (2026): the novelty/SFX fragment was the MOST
        distinct of every style tested — not because of melody but because a
        FOREIGN timbre (a bird-tweet "whistle", GM SFX program 123) zig-zagged
        through and INTERRUPTED the main texture. Lesson: heterogeneous textural
        events — an unexpected timbre cutting across the lead/bed — are a
        powerful, robust distinctiveness lever at this fidelity, strongly
        validating [[b7p21m9z]] (weird helps). Candidate dimension: an
        entropy-chosen TEXTURAL-INTERRUPTION layer (which foreign/SFX timbre
        punctuates, where, or none) — partly DISCRETE (presence + which foreign
        timbre, both recognizable) and partly analog (placement [[e9k2m4p1]]).
        Use it both as its own "novelty/SFX" style AND as an optional
        cross-style ornament. Relates to [[c2k9p0a4]], [[d4m1z8p0]].

    Conditioned Probability Distributions = decision:
      id: 7c4m1k0p
      why: >
        Entropy selects a POINT ON A CONTEXT-CONDITIONED PROBABILITY DISTRIBUTION,
        not a uniform choice, so typical output is musically believable while the
        full range stays reachable. Examples implemented in the engine prototype:
        melodic shape uses REGISTER-GRAVITY (each interval drawn from a bell curve
        centered on a drift back toward the tessitura center plus a mild global
        tendency; a high note is likelier to fall; width set by leapiness), and
        discrete dimensions use MUSICAL PRIORS (period / moderate-leap / mid-
        register / resolving are likelier; extremes rarer). Distributions can be
        CONDITIONAL (e.g. tempo|style, leapiness|style) once styles land.
        TRADEOFF: non-uniform priors carry less than log2(n) bits per dimension,
        so this trades a little entropy for believability -- accepted, since
        musicality is the higher bar [[f7a2k930]]; account for it in [[2p8z1m40]]
        (the per-dimension yields assume the realized distribution, not uniform).
        Keeps determinism + whole-input dependence (entropy picks the CDF point).
        Relates to [[k20f9a3x]].

    Adversarial Review And Evidence Grounding = decision:
      id: 6b2k9p0a
      why: >
        A 5-persona adversarial DESIGN review (2026-06-23;
        reviews/review-panel-2026-06-23.md; lenses: bit-budget, music-perception,
        musicology, psychoacoustics, collision) challenged the 25-50 headline and
        proposed ~12-21. Its load-bearing citations were then INDEPENDENTLY
        VERIFIED (docs/references.md). Verdict: the blanket downward revision was
        a competing ESTIMATE, not evidence, and is NOT adopted; the headline range
        stays but is now explicitly CONDITIONED [[2p8z1m40]].
        UPHELD + folded in: (a) melodic-rhythm and (b) contour weaken over long
        unrehearsed delays (HebertPeretz1997; DowlingKwakAndrews1995); (c) amusia
        is ~1.5% not 4%, degrading UNEVENLY (PeretzVuvan2017); (d) mode/cadence
        AFFECT is Western-enculturated (Smit2022).
        REFUTED: the style downgrade rested on a MISREAD genre statistic
        (GjerdingenPerrott2008's 44% is 250ms-vs-3s agreement = how FAST genre is
        grasped). Style/timbre is fast, robust, and the MOST DURABLE carrier
        (SchellenbergHabashi2015: novel melodies consolidate after 2 exposures,
        no week-long forgetting; timbre durable; key/tempo fade) -- so the master
        dimension [[z0m4p81q]] stands and zeroing absolute key + weak tempo is
        confirmed.
        STILL OPEN (not yet resolved): the antecedent/consequent engine is
        unbuilt (next build task); whether the consequent transformation is a
        PERCEPTUAL bit is untested (reclassify [[9k3f0a72]] pending a study);
        surface the recognition-is-not-cryptographic anti-claim at any point of
        trust [[m4z81p3v]]; harden determinism (float->MIDI, modulo bias,
        discrete-gestalt avalanche).
        LESSON: an adversarial panel surfaces arguments to ADJUDICATE on merits +
        VERIFY, not point-estimates to adopt. Refines [[k20f9a3x]], [[z0m4p81q]],
        [[q9f3a7k2]]; the real arbiter is the A/B/X listening study.

    Full Hash Consumption Rich Variety = principle:
      id: h0v4k7m2
      why: >
        NORTH STAR (maintainer, 2026-06-24). The generator's purpose is to EXPOSE
        the variety in entropy, and entropy is maximally varied — so the engine
        must expose music's enormous variety, NOT a narrow set. The standing
        directive: BE IMPATIENT WITH SIMPLIFICATIONS. By the time the engine is
        "done" it should CONSUME EVERY BIT of the SHA-512 fingerprint, with each
        consumed bit driving a musical decision that is LOGICALLY VALID — a
        consummate composer (think John Williams) would agree it is a legitimate
        possibility, never random nonsense (a hard read of [[f7a2k930]]). This is
        an ambition about the GENERATOR, not a claim about human recall: the ear
        may reliably distinguish only ~20-30 bits (Model B, [[2p8z1m40]]), but
        full consumption is still the goal — it maximizes machine-distinctness
        (consumed >> delivered) AND casual avalanche, and forces us to keep
        finding real musical axes instead of collapsing the space. Mechanism:
        keep adding DISCRETE valid-choice dimensions (more styles/idioms, meter,
        form, harmony vocab, groove variants, instrumentation, ornaments,
        texture-interruption [[f3a0k9m2]]) AND a deep stack of ANALOG layers
        [[e9k2m4p1]], each drawing fresh fingerprint bits from a CONTEXT-
        CONDITIONED distribution [[7c4m1k0p]] so typical output stays believable
        while the FULL range stays reachable. Test of done-ness: (a) no fingerprint
        bits left unconsumed; (b) a rich, audibly broad spread across inputs; (c)
        every decision defensible as valid music. Anti-pattern to reject in review:
        any dimension hard-coded, collapsed, or left narrow "for simplicity" when a
        musically-valid richer mapping exists. Ties together [[2p8z1m40]],
        [[k20f9a3x]], [[f7a2k930]], [[z0m4p81q]], [[d4m1z8p0]], [[c2k9p0a4]],
        [[e9k2m4p1]], [[f3a0k9m2]], [[7c4m1k0p]].

    Metric Conservation In Rhythm Transforms = constraint:
      id: m9p3k7a2
      why: >
        Maintainer lesson (2026-06-24), learned from a real bug: "if you add a
        flourish in one place, you have to SUBTRACT to compensate somewhere else."
        Every rhythmic transformation (subdivision, diminution, augmentation,
        ornament, swing) MUST CONSERVE the bar's total duration: time added by
        splitting a note must be removed elsewhere so the barline never moves. Two
        sub-rules the bug violated: (1) GRID — transformed durations snap to the
        sixteenth grid (halving 0.75->0.375 drifted every later onset off the beat);
        (2) METRIC ANCHOR — a repeated/tiled cell must total a whole, strong-beat-
        aligned length (1/2/4/8 beats) so each repeat starts on a down/strong beat
        (a 4.25-beat cell flipped stressed<->unstressed on every repeat). Enforced by
        regression tests in test_motif.py (no off-grid pitched onsets; diminished
        cells bar-aligned). When melodic triplets / swung-eighth melodies are added
        later, they must obey the same conservation (a triplet group fills its beat
        exactly). Relates to [[9k3f0a72]] (whole-motif integrity), [[h0v4k7m2]].

    Texture Model Beyond Lead Plus Comp = decision:
      id: p6m2v9k0
      why: >
        OPEN / NORTH-STAR DEBT (maintainer, 2026-06-24). The v0.x engine bakes in a
        single HOMOPHONIC texture — one LEAD melody + a chordal COMP ("accompanying")
        + a BASS — and that is a SIMPLIFICATION rejected by [[h0v4k7m2]]: not all
        music is tune-plus-backing. A string quartet is four interdependent voices;
        a fugue/invention is independent imitative lines; a chorale/hymn is
        homorhythmic four-part harmony; much world/folk is HETEROPHONIC (simultaneous
        variants of one line) or MONOPHONIC + drone; gamelan/polyphony don't fit
        "lead+comp" at all. So TEXTURE itself must become a dimension (entropy-chosen,
        conditioned on style): at least {monophonic(+drone), homophonic melody+
        accompaniment, homorhythmic/chordal, polyphonic/contrapuntal, heterophonic},
        and the voice model must generalize from fixed LEAD/COMP/BASS roles to N
        Voices whose RELATIONSHIP the texture defines (equal contrapuntal voices,
        doubling/heterophony, chordal blocks, melody+drone). The metaphor already has
        the right primitive — Voice (AGENTS.md §4) — it is the ROLES that are
        over-specialized. STATUS: most current idioms (ragtime, swing, blues, bossa,
        samba, salsa, reggae, funk, gospel, march, tango) genuinely ARE homophonic,
        so the v1 model fits them; it OVERSIMPLIFIES the art-music styles
        (classical/baroque want counterpoint + true quartet) and BLOCKS whole
        families (fugue, chorale, Renaissance polyphony, heterophonic world music).
        A big v0.11+ track: add the texture dimension + a generalized N-voice model
        with per-texture voice-leading (species-counterpoint-ish for polyphony, SATB
        for chorale). Refines [[z0m4p81q]], [[h0v4k7m2]]; relates to [[c2k9p0a4]],
        [[d4m1z8p0]].

    Breath Phrases The Line Not The Form = decision:
      id: b3r8k1m7
      why: >
        Top lyricism finding (fw4, panel + maintainer): "breath is an afterthought,
        not phrasing." The engine only rested where a form-template boundary landed
        (end of bar 4/8 in a period/aaba) and otherwise packed bars wall-to-wall —
        lead runs of 24-48 sounded notes with no rest. A singable line BREATHES as a
        function of PHRASE LENGTH, not form structure: after at most ~12 sounded
        notes (target a singable ~7-12) it must take a comma-length rest so the
        antecedent breathes into the consequent even MID-section. FIX: a post-render
        `breathe` pass over the LEAD voice (melody.py) opens a comma by SHORTENING a
        note's duration — onsets are never moved, so the bar total and the 16th grid
        are conserved [[m9p3k7a2]]; the rest is the silence the trim opens before the
        next onset. It prefers a note that ends on a beat boundary (rest between
        phrase limbs) and the latest note in the run window (so the next run is
        bounded), opens a full eighth wherever a note can spare it and falls back to
        a sixteenth comma in a dense fast run. ANALOG layer (note-length variation,
        [[e9k2m4p1]]): carries no Model-B recall bits but draws fresh fingerprint
        bits and makes the line sing. Comp/bass/percussion are untouched. The single
        biggest lyricism lever before any pitch change. Refines [[e9k2m4p1]],
        [[f7a2k930]]; conserves [[m9p3k7a2]]; serves [[h0v4k7m2]].

    Lead De-Stutter (singability cap on same-pitch repeats) = decision:
      id: d5t8m2k7
      why: >
        Convergent prior finding (fw6, multiple graders): the LEAD emits "machine-gun
        repeated note" / unsingable patter — runs of 3+ identical pitches no voice
        could phrase (e.g. "=c =c =c", a jumpy octave-toggle that collapses on snap, a
        re-snapped tag). The strong-beat anti-repeat ([[snap_chord_tone]]) only guards
        beats 1 & 3; the jumpy/patter contour paths and cell-tiling still produce 3-6
        identical pitches in a row off the strong beats. FIX: a PURE post-render
        `destutter` pass over the LEAD voice (melody.py) caps consecutive same-pitch
        repeats at 2 by nudging the 3rd+ note to an ADJACENT scale tone — onset and
        duration are NEVER touched, so the 16th grid and metric conservation hold
        [[m9p3k7a2]]. It prefers the neighbour toward the register center (keeps the
        contour sane) and never re-collides with the note on either side. Runs
        alongside (before) `breathe` [[b3r8k1m7]] — pitch-only vs duration-only, the
        two passes don't interact. ANALOG layer (exact pitch, [[e9k2m4p1]]): carries
        no Model-B recall bits but makes every line singable. Determinism + avalanche
        untouched (pure function of the already-chosen notes). Refines [[b3r8k1m7]],
        [[e9k2m4p1]]; conserves [[m9p3k7a2]]; serves [[h0v4k7m2]].

    Emotional Register Master Dimension = decision:
      id: a7k0m3p9
      why: >
        OPEN / NORTH-STAR DEBT (maintainer, 2026-06-24): output is "emotionally
        flat" — nothing reads as sad / mischievous / angry / tense / triumphant.
        ROOT CAUSE: mode, tempo, register, dynamics, articulation, harmonic
        dissonance and rhythm are each drawn INDEPENDENTLY, so their affective cues
        never ALIGN — and affect is a GESTALT of aligned cues. FIX: add EMOTION as a
        master dimension (a second master alongside style [[z0m4p81q]]) that is
        entropy-chosen and then COHERENTLY conditions the affective cues in
        Gabrielsson & Lindström's strength order: mode (major/minor) > tempo > loudness/
        dynamics > register/pitch height > articulation (staccato/legato) >
        timbre/brightness > harmonic dissonance/consonance > rhythmic regularity. So
        "tense" = minor + moderate-fast + crescendo + rising register + detached +
        dissonant color + irregular accent; "sad" = minor + slow + soft + low +
        legato + consonant + simple; "mischievous" = major/modal + brisk + staccato +
        leaps + bright + playful syncopation; "angry" = minor + fast + loud + wide
        leaps + harsh; "triumphant" = major + moderate + loud + brass-ish + full.
        Style x Emotion interact (a SAD samba vs an ANGRY samba) — emotion biases the
        WITHIN-style choices, it does not override the idiom. CAVEAT: mode/cadence/
        consonance affect is Western-enculturated (Smit2022, [[6b2k9p0a]]) — these are
        cues for the typical Western listener, not universals; tempo/loudness/register
        are more cross-cultural. Bit-bearing: emotion is a DISCRETE, recognizable
        master choice (~2-3 bits) AND it makes every conditioned sub-cue coherent,
        which is what makes the motif feel like SOMETHING. A big v0.11+ track with
        [[p6m2v9k0]] (texture). Refines [[z0m4p81q]], [[7c4m1k0p]], [[h0v4k7m2]];
        the enculturation caveat ties to [[6b2k9p0a]].

    Conditional Decision Dependencies = constraint:
      id: d2k9m4p1
      why: >
        RECURRING ROOT CAUSE (maintainer, across listening rounds; sharpest 2026-06-25):
        compounding musical decisions are still drawn as FREE / INDEPENDENT when they
        must be DEPENDENT — a directed acyclic graph where downstream choices are
        CONDITIONED on the already-decided upstream ones. Failures this caused: a flute
        salsa whose lead register sat below the flute's normal tessitura (register must
        be conditioned on the chosen INSTRUMENT); style->instrument convergence too weak
        (only 2/12 style-suited); emotion absent because mode/tempo/dynamics/articulation
        weren't conditioned on one affect target. Required dependency order (sketch):
        emotion -> style/genre -> meter -> tempo -> mode/harmonic-vocab -> instrumentation
        -> (per instrument) register/tessitura -> groove/bass -> motif shape ->
        development -> dynamics/articulation. Each node samples its CONDITIONAL
        distribution P(node | decided ancestors); entropy still picks the CDF point
        (determinism + [[7c4m1k0p]] preserved). Capability gates ([[c2k9p0a4]]) are the
        hard edges of this DAG; the soft edges are conditional probabilities. Implement
        the DAG even with hand-tuned conditionals first (immediate fix), then data-derive
        the conditionals [[v8k2m1p0]]. Sharpens [[7c4m1k0p]], [[c2k9p0a4]], [[z0m4p81q]],
        [[a7k0m3p9]]; the "instrument has a normal register" rule extends [[b7p21m9z]].

    Corpus Mined Feature Vectors = decision:
      id: v8k2m1p0
      why: >
        PROPOSED PIVOT (maintainer, 2026-06-25) — full write-up:
        docs/feature-vector-direction.md. After ~6 flywheel rounds the hand-rolled
        engine is coherent (~C) but stuck on "extreme weirdness + high boringness"
        because the priors are guessed. Proposal: acquire a large corpus of
        human-authored MIDI / lead sheets (thousands+, popularity as a quality proxy),
        MINE probabilistic FEATURE VECTORS (conditional distributions) for motif
        development/re-articulation, emotion, dynamics, instrument choice (+ register-
        per-instrument, groove, harmony, meter, contour, voicing density), wire them
        into the dependency DAG [[d2k9m4p1]], and map entropy -> a point on each
        conditional distribution (same contract as today, data-derived). Then most
        hand-rolled variability code collapses to ASSEMBLY + render after a DAG walk.
        This is an EVOLUTION of [[7c4m1k0p]], not a throwaway: the determinism harness,
        Chooser, exporters, theory, render stage, teaching loop, and the style/two-layer/
        capability structure all transfer (see doc "What transfers"). CONSTRAINT: keep
        the model to distributions we sample DETERMINISTICALLY (conditional histograms /
        n-gram + GMM), NOT an end-to-end neural generator, to preserve determinism +
        auditability [[81pz4m0v]]. Candidate corpora (verify): EMOPIA / VGMIDI
        (emotion-labelled), Hooktheory TheoryTab (harmony + popularity), Essen / Nottingham
        / ABC (melody+meter+contour), Lakh / MetaMIDI (instrumentation), POP909, MAESTRO.
        Recommended: incremental — build the DAG with hand-tuned conditionals first, then
        replace dimensions with mined vectors (emotion + register-per-instrument first).
        Realizes [[h0v4k7m2]] (consume more of the hash with VALID, data-grounded choices);
        depends on [[d2k9m4p1]]; relates to [[2p8z1m40]], [[a7k0m3p9]], [[m4k0p2v9]].

    Meter Beyond Four Four = decision:
      id: m4k0p2v9
      why: >
        OPEN (maintainer, 2026-06-25): the engine is hardcoded 4/4 (BEATS_PER_BAR=4,
        M:4/4). Whole idiom families need other meters: waltz/minuet/mazurka (3/4),
        many marches/polkas (2/2 cut time), jigs/some folk (6/8), compound (9/8, 12/8),
        odd (5/4, 7/8), and 3/2. METER is an upstream master decision in the DAG
        [[d2k9m4p1]] (conditioned on style/emotion) that re-parameterizes the bar grid,
        the groove patterns, the strong-beat map (metric conservation [[m9p3k7a2]] must
        generalize off the 16th-in-4/4 grid), and the ABC M: header. A prerequisite for
        non-4/4 styles and for sitar raga / chant ([[p6m2v9k0]], tick ~55y2). Relates to
        [[z0m4p81q]], [[d2k9m4p1]].
