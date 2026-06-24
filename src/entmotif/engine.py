"""entmotif engine — orchestrates a value into a Motif.

Draws every musical decision from the fingerprint (mode/key/lead/tempo/leap/form/
texture/color), builds the Phrase sequence, then renders each unit's melody,
antiphon/counter, and comp+bass into one note list with a register + dynamic arc
(placed climax ~2/3 through). :func:`compose` returns a :class:`Motif`;
:func:`generate` is the legacy ``(notes, meta)`` adapter the tests/exporters use.
"""
from entmotif.model import DIV, BEATS_PER_BAR, VoiceRole, NoteEvent, Motif, climax_unit
from entmotif.entropy import Chooser, fingerprint_text
from entmotif.theory import snap, sym
from entmotif.melody import (
    FIGURES, HOOKS, SIG_STEPS, BREATHS, LEAP_NAMES, DYN_VEL,
    unit_dyn, line, cadence_bar, tag_call, motif_shape, render_transform, choose_transform)
from entmotif.arrangement import (
    STYLES, STYLE_NAMES, STYLE_W, palette_for, gm_name, lead_choices,
    comp_choices, bass_choices, comp_pat_choices, bass_pat_choices,
    arrange_unit, percussion_groove)
from entmotif.form import build_form

# Answers stay RECOGNIZABLE: the consequent is a small sequence / fragment / restate of
# the antecedent, never an inversion or octave-displacing op (which broke the call->answer
# relationship in v0.8). Used for answer-role restatements only.
ANSWER_TRANSFORMS = ["identity", "seq+2", "seq-2", "fragment"]
ANSWER_TRANSFORM_W = [3, 3, 3, 2]


def generate(value):
    fp = fingerprint_text(value)
    ch = Chooser(fp)
    style = ch.weighted("style", STYLE_NAMES, STYLE_W)        # the broad master dimension (idiom/groove)
    S = STYLES[style]
    mode = ch.weighted("mode", ["major", "minor"], S["mode_w"])  # style-biased (tango minor, march major...)
    key = ch.int("key", 12)
    lead = ch.weighted("lead", *lead_choices(style))          # broad pool; signature common, weird-valid rare
    comp_prog = ch.weighted("comp", *comp_choices(style))     # rhythm-section two-layer model (c2k9p0a4): signature
    bass_prog = ch.weighted("bass", *bass_choices(style))     # common, capability-passing alternates rare
    comp_pat = ch.weighted("comp_pat", *comp_pat_choices(style))  # RHYTHM-pattern variety (A2, r4d8m1k6): signature
    bass_pat = ch.weighted("bass_pat", *bass_pat_choices(style))  # groove common, idiomatic variants rare
    pal = palette_for(style, lead, comp_prog, bass_prog, comp_pat, bass_pat)
    ilo, ihi, icen = pal.range
    tonic = snap(icen, [key], ilo, ihi - 12)
    lo, hi = max(ilo, tonic - 7), min(ihi, tonic + 12)        # ~1.5 oct, sitting LOWER (v0.9 was shrill/too high)
    base = lo + (hi - lo) // 4
    tempo = ch.weighted("tempo", S["tempos"], S["tempo_w"])   # per-style tempo range (up to 208)
    leap = ch.weighted("leap", [0, 1, 2], [3, 4, 2])
    tendency = ch.weighted("tend", [-1, 0, 1], [2, 3, 2])
    resolution = ch.weighted("res", ["authentic", "deceptive", "half"], [3, 2, 2])
    form = ch.weighted("form", ["sentence", "period", "period_tag", "aaba"], [2, 4, 2, 2])
    fat = ch.weighted("fat", [0, 1, 2, 3], S["fat_w"])        # voicing richness, style-biased
    # comp/bass GROOVE is fixed by the style (cohesion) — not a separate entropy draw.
    template = ch.weighted("arr", ["solo_bed", "lead_counter", "call_resp", "groove_first"],
                           [3, 2, 2, 1])
    color = ch.weighted("color", [0, 1, 2], S["color_w"])     # harmonic adventurousness, style-biased
    sig = ch.choice("sig", SIG_STEPS[leap])                   # signature opening interval

    idea = [ch.choice("hook", HOOKS), ch.choice("im1", FIGURES)]
    other = [ch.choice("om0", FIGURES), ch.choice("om1", FIGURES)]

    units = build_form(form, resolution, ch, color)
    nU = len(units)
    peak = climax_unit(nU)                                    # placed climax ~2/3 through (Huron arch)
    span = max(1, max(peak, nU - 1 - peak))                   # integer (no float register arc)

    def arc_center(u):                                        # register arc: peaks (=hi-2) at the climax unit
        return base + (hi - 2 - base) * (span - abs(u - peak)) // span

    # The GERMINAL CELL: the first idea, stated once. Every later statement is an
    # EXPLICIT transformation of its realized shape (v0.8 headline) — never verbatim.
    g_chm = [sym(c, mode) for c in units[0].chords]
    germ_notes = line(idea, g_chm, mode, key, base, lo, hi, 0, arc_center(0), tendency, leap, ch,
                      "idea", 0, False, sig, VoiceRole.LEAD, DYN_VEL[unit_dyn(0, nU, peak)])
    germ_shape = motif_shape(germ_notes, mode, key, lo, hi)

    def render_lead(u, role, chm, cad, bar0, center, vel, at_peak, cr_answer):
        """The lead line for one unit: state the germ, transform it on a restatement,
        call+cadence over an antiphony bar, or sound a contrasting idea."""
        if template == "groove_first" and u == 0:
            return []
        if role == "idea":
            if u == 0:                                        # state the germ
                return list(germ_notes)
            op = choose_transform(ch, "xform%d" % u)          # RESTATEMENT = explicit operation on the germ
            return render_transform(germ_shape, op, mode, key, lo, hi, bar0, chm,
                                    VoiceRole.LEAD, vel, center, climax=at_peak)
        if role == "answer":
            if cr_answer:                                     # lead CALLS through the antiphony bar (singable
                mel = tag_call(center, chm[0], mode, key, lo, hi, bar0, VoiceRole.LEAD, vel)
                #   figure, not a dead whole-bar hold — fw3, the "static held-note" fix)
                return mel + cadence_bar(cad, key, mode, lo, hi, bar0 + 1, VoiceRole.LEAD, vel)
            op = ch.weighted("xform%d" % u, ANSWER_TRANSFORMS, ANSWER_TRANSFORM_W)
            mel = render_transform(germ_shape, op, mode, key, lo, hi, bar0, [chm[0]],
                                   VoiceRole.LEAD, vel, center, climax=at_peak)
            return mel + cadence_bar(cad, key, mode, lo, hi, bar0 + 1, VoiceRole.LEAD, vel)
        return line(other, chm, mode, key, base, lo, hi, bar0, center, tendency, leap, ch,
                    "other", 0, False, None, VoiceRole.LEAD, max(40, vel - 6))

    dyn_bars = {}
    notes, used_v4, prev_voicing = [], False, None
    for u, (role, chs, cad, devslot) in enumerate(units):
        chm = [sym(c, mode) for c in chs]
        bar0 = u * 2
        center = arc_center(u)
        dyn = unit_dyn(u, nU, peak)
        vel = DYN_VEL[dyn]
        dyn_bars[bar0] = dyn
        at_peak = (u == peak)
        cr_answer = template == "call_resp" and role == "answer"

        mel = render_lead(u, role, chm, cad, bar0, center, vel, at_peak, cr_answer)

        if u != nU - 1 and mel:                               # breath: trim the LAST note (phrase boundary only)
            br = ch.choice("breath%d" % u, BREATHS)
            if br and mel[-1].dur - int(br * DIV) >= int(0.5 * DIV):
                mel[-1] = mel[-1]._replace(dur=mel[-1].dur - int(br * DIV))
        notes += mel

        if cr_answer:                                         # antiphonal DEVELOPED response on V:4 (germ transform)
            op = choose_transform(ch, "ans%d" % u)
            ans = render_transform(germ_shape, op if op != "identity" else "fragment",
                                   mode, key, lo, hi, bar0, [chm[0]],
                                   VoiceRole.ANSWER, max(40, vel - 18), center)
            used_v4 = used_v4 or bool(ans)
            notes += ans

        # ---- texture: the groove/harmony is CONSTANT (v0.10's envelope flickered the
        #      skank/comp on and off, breaking reggae/swing — "comes in at random",
        #      "scraping added partway"). Only two thinning exceptions remain:
        #      the groove_first bass-first intro, and a lead-alone opening reserved for
        #      the homophonic art styles (classical/baroque). ----
        bass_on = True
        comp_on = not (template == "groove_first" and u == 0)
        if style in ("classical", "baroque") and template in ("solo_bed", "lead_counter") and u == 0:
            comp_on = False                                   # art-style lead states the theme unaccompanied
        anotes, prev_voicing = arrange_unit(chm, mode, key, lo, bar0, fat, pal.comp_pat, pal.bass_pat,
                                            comp_on, bass_on, vel, pal.legato, prev_voicing)
        notes += anotes

        if template == "lead_counter" and role == "idea":     # DEVELOPED counter on V:4 = inversion of the germ
            cm = render_transform(germ_shape, "invert", mode, key, lo - 7, hi - 9, bar0, chm,
                                  VoiceRole.ANSWER, 72, center - 9)
            used_v4 = used_v4 or bool(cm)
            notes += cm

    # ---- percussion: the style's groove across the piece (skip the groove-build intro) ----
    perc_start = 2 if template == "groove_first" else 0
    perc = percussion_groove(pal.perc, perc_start, nU * 2 - perc_start, pal.perc_vel)
    notes += perc

    meta = {"mode": mode, "key": key, "tonic": tonic, "tempo": tempo, "style": style,
            "lead": gm_name(lead), "lead_prog": lead, "comp_prog": pal.comp_program,
            "bass_prog": pal.bass_program, "ans_prog": pal.answer_program,
            "leap": LEAP_NAMES[leap], "res": resolution, "form": form, "bars": nU * 2,
            "fat": fat, "arr": template, "percussion": pal.perc if perc else "none",
            "comp_pat": pal.comp_pat, "bass_pat": pal.bass_pat,
            "final_cad": units[-1].cad,
            "bar_chords": [c for _, chs, _, _ in units for c in (sym(x, mode) for x in chs)],
            "color": color, "v4": used_v4, "dyn_bars": dyn_bars}
    return notes, meta


def compose(value):
    """Compose a value into a :class:`Motif` aggregate (wraps :func:`generate`)."""
    notes, meta = generate(value)
    return Motif(value, notes, meta)
