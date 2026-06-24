"""entmotif engine — orchestrates a value into a Motif.

Draws every musical decision from the fingerprint (mode/key/lead/tempo/leap/form/
texture/color), builds the Phrase sequence, then renders each unit's melody,
antiphon/counter, and comp+bass into one note list with a register + dynamic arc
(placed climax ~2/3 through). :func:`compose` returns a :class:`Motif`;
:func:`generate` is the legacy ``(notes, meta)`` adapter the tests/exporters use.
"""
from entmotif.model import DIV, VoiceRole, Motif
from entmotif.entropy import Chooser, fingerprint_text
from entmotif.theory import snap, sym
from entmotif.melody import (
    FIGURES, HOOKS, SIG_STEPS, BREATHS, LEAP_NAMES, DYN_VEL,
    unit_dyn, line, cadence_bar)
from entmotif.arrangement import (
    LEADS, LEAD_NAMES, LEAD_RANGE, ANSWER_INSTR, arrange_unit)
from entmotif.form import build_form, transform_for

TEMPOS = [60, 72, 84, 96, 108, 120, 138, 160, 184]
TEMPO_W = [1, 2, 3, 4, 4, 3, 2, 2, 1]


def generate(value):
    fp = fingerprint_text(value)
    ch = Chooser(fp)
    mode = ch.choice("mode", ["major", "minor"])
    key = ch.int("key", 12)
    lead = ch.choice("lead", LEADS)
    ilo, ihi, icen = LEAD_RANGE[lead]
    tonic = snap(icen, [key], ilo, ihi - 12)
    lo, hi = max(ilo, tonic - 3), min(ihi, tonic + 15)
    base = lo + (hi - lo) // 4
    tempo = ch.weighted("tempo", TEMPOS, TEMPO_W)
    leap = ch.weighted("leap", [0, 1, 2], [3, 4, 2])
    tendency = ch.weighted("tend", [-1, 0, 1], [2, 3, 2])
    resolution = ch.weighted("res", ["authentic", "deceptive", "half"], [3, 2, 2])
    form = ch.weighted("form", ["sentence", "period", "period_tag", "aaba"], [2, 4, 2, 2])
    fat = ch.weighted("fat", [0, 1, 2, 3], [2, 3, 2, 1])
    figr = ch.weighted("figr", ["block", "stabs", "arp", "alberti"], [2, 2, 2, 1])
    bassfig = ch.weighted("bass", ["root5", "walking", "pedal"], [3, 2, 1])
    template = ch.weighted("arr", ["solo_bed", "lead_counter", "call_resp", "groove_first"],
                           [3, 2, 2, 1])
    color = ch.weighted("color", [0, 1, 2], [3, 4, 1])        # harmonic adventurousness dial
    sig = ch.choice("sig", SIG_STEPS[leap])                   # signature opening interval

    idea = [ch.choice("hook", HOOKS), ch.choice("im1", FIGURES)]
    other = [ch.choice("om0", FIGURES), ch.choice("om1", FIGURES)]
    ans_fig = ch.choice("ansfig", FIGURES)
    ans_instr = ANSWER_INSTR[lead]

    units = build_form(form, resolution, ch, color)
    nU = len(units)
    peak = max(1, ((nU - 1) * 2 + 1) // 3)                    # placed climax ~2/3 through (Huron arch), integer
    span = max(1, max(peak, nU - 1 - peak))                   # integer (no float register arc)
    dyn_bars = {}
    notes, used_v4 = [], False
    for u, (role, chs, cad, devslot) in enumerate(units):
        chm = [sym(c, mode) for c in chs]
        bar0 = u * 2
        # register arc (integer): peaks (=hi-2) at the climax unit, lower away from it
        center = base + (hi - 2 - base) * (span - abs(u - peak)) // span
        dyn = unit_dyn(u, nU, peak)
        vel = DYN_VEL[dyn]
        dyn_bars[bar0] = dyn
        offset, invert = transform_for(devslot, ch)
        cr_answer = template == "call_resp" and role == "answer"
        if template == "groove_first" and u == 0:
            mel = []
        elif role == "idea":
            mel = line(idea, chm, mode, key, base, lo, hi, bar0, center, tendency, leap, ch,
                       "idea", offset, invert, sig, VoiceRole.LEAD, vel)
        elif role == "answer":
            if cr_answer:                                     # lead RESOLVES the phrase (never tacet);
                mel = cadence_bar(cad, key, mode, lo, hi, bar0 + 1, VoiceRole.LEAD, vel)   # antiphon answers below
            else:
                mel = line([ans_fig], [chm[0]], mode, key, base, lo, hi, bar0, center, tendency,
                           leap, ch, "idea", offset, invert, sig, VoiceRole.LEAD, vel)
                mel += cadence_bar(cad, key, mode, lo, hi, bar0 + 1, VoiceRole.LEAD, vel)
        else:
            mel = line(other, chm, mode, key, base, lo, hi, bar0, center, tendency, leap, ch,
                       "other", 0, False, None, VoiceRole.LEAD, max(40, vel - 6))
        if u != nU - 1 and mel:                               # breath: trim the LAST note (phrase boundary only)
            br = ch.choice("breath%d" % u, BREATHS)
            if br and mel[-1].dur - int(br * DIV) >= int(0.5 * DIV):
                mel[-1] = mel[-1]._replace(dur=mel[-1].dur - int(br * DIV))
        notes += mel

        if cr_answer:                                         # antiphonal DEVELOPED response on V:4:
            frag = idea[0][:3] or idea[0]                     #   a hook fragment SEQUENCED up a third
            ans = line([frag], [chm[0]], mode, key, base, lo, hi, bar0, center, tendency, leap,
                       ch, "ans%d" % u, 2, False, sig, VoiceRole.ANSWER, max(40, vel - 18))
            used_v4 = used_v4 or bool(ans)
            notes += ans

        comp_on = template in ("solo_bed", "lead_counter", "call_resp")
        bass_on = True
        if template == "groove_first":
            comp_on = u >= 1
        if template == "call_resp":
            comp_on = role != "idea"
        notes += arrange_unit(chm, mode, key, lo, bar0, fat, figr, bassfig, comp_on, bass_on)
        if template == "lead_counter" and role == "idea":     # real contrary-motion counter (V:4)
            cm = line([idea[0]], [chm[0]], mode, key, base, lo - 7, hi - 9, bar0,
                      center - 9, -tendency, 0, ch, "ctr", 0, True, None, VoiceRole.ANSWER, 72)
            used_v4 = used_v4 or bool(cm)
            notes += cm

    meta = {"mode": mode, "key": key, "tonic": tonic, "tempo": tempo, "lead": LEAD_NAMES[lead],
            "lead_prog": lead, "ans_prog": ans_instr, "leap": LEAP_NAMES[leap], "res": resolution,
            "form": form, "bars": nU * 2, "fat": fat, "figr": figr, "arr": template,
            "bar_chords": [c for _, chs, _, _ in units for c in (sym(x, mode) for x in chs)],
            "color": color, "v4": used_v4, "dyn_bars": dyn_bars}
    return notes, meta


def compose(value):
    """Compose a value into a :class:`Motif` aggregate (wraps :func:`generate`)."""
    notes, meta = generate(value)
    return Motif(value, notes, meta)
