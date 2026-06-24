"""entmotif form — phrase structure, cadences, and development assignment.

Builds the ordered sequence of :class:`Phrase` units for a chosen form
(sentence / period / period_tag / aaba), threading the cadence plan and the
secondary-dominant color dial, and forcing clean terminal resolution. `cadc`
maps a cadence kind to its two roman numerals; `transform_for` picks the
:class:`Development` applied to a restatement slot.
"""
from entmotif.model import Phrase, Development


def cadc(res):
    return {"authentic": ["V", "I"], "deceptive": ["V", "vi"], "half": ["IV", "V"]}[res]


def build_form(form, res, ch, color):
    P = cadc(res)
    sd = {0: 0, 1: 25, 2: 60}[color]                          # 2(d) secondary-dominant prob %, by color dial
    if P[1] == "V" and ch.int("sd", 100) < sd:
        P = ["VsV", "V"]
    pre = ["VsV", "V"] if ch.int("sd2", 100) < sd else ["IV", "V"]
    if form == "sentence":
        units = [("idea", ["I", "I"], None, 0), ("answer", P, res, 0)]
    elif form == "period":
        units = [("idea", ["I", "vi"], None, 0), ("answer", pre, "half", 0),
                 ("idea", ["I", "vi"], None, 1), ("answer", P, res, 0)]
    elif form == "period_tag":
        units = [("idea", ["I", "vi"], None, 0), ("answer", pre, "half", 0),
                 ("idea", ["I", "vi"], None, 1), ("answer", ["ii", "V"], "half", 0),
                 ("idea", ["I", "vi"], None, 2), ("answer", P, res, 0)]
    else:
        units = [("idea", ["I", "vi"], None, 0), ("answer", pre, "half", 0),
                 ("idea", ["I", "vi"], None, 1), ("answer", ["ii", "V"], "half", 0),
                 ("contrast", ["IV", "I"], None, 0), ("contrast", ["ii", "V"], None, 0),
                 ("idea", ["I", "vi"], None, 2), ("answer", P, res, 0)]
    units = [Phrase(*u) for u in units]
    role, _chs, _cad, dv = units[-1]                           # round 4: terminal cadence ALWAYS resolves
    units[-1] = Phrase(role, ["V", "I"], "authentic", dv)      # (clean closure; no half/abrupt final)
    return units


def transform_for(devslot, ch):
    if devslot == 0:
        return Development(0, False)
    return Development(*ch.weighted("dev%d" % devslot, [(2, False), (-2, False), (0, True), (1, False)],
                                    [3, 2, 2, 1]))
