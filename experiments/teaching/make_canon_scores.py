#!/usr/bin/env python3
"""Assemble the CANON score bundle for faculty calibration grading.

Reads the curated/stratified canon ABC files (canon/abc/<id>.abc) per the manifest
below and emits scores-canon.md — the calibration surface: real, famous themes
reduced to a bare identifiable phrase, so the faculty can check whether the rubric
awards A's to genuine masterpieces (anchors) and grades famous-as-sung songs lower
(controls). Tiers from canon/tiers.md (axis: memorable as UNSUNG instrumental music).

Usage: python3 make_canon_scores.py   (writes scores-canon.md next to this file)
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ABC = os.path.join(HERE, "canon", "abc")

# (tier, [ids]) — anchors are the calibration target; controls SHOULD grade lower.
MANIFEST = [
    ("ANCHOR · classical", ["C01", "C02", "C03", "C04", "C05", "C06", "C46", "T01", "T02"]),
    ("ANCHOR · film/TV",    ["C07", "C08", "C09", "C10", "C11", "C12", "T04", "T05", "T07"]),
    ("ANCHOR · riff",       ["C17", "C18", "C19", "C27"]),
    ("ANCHOR · jazz head",  ["C29", "C30", "C31", "C32", "C33", "T29"]),
    ("ANCHOR · folk/hymn",  ["C37", "C38", "C39", "C40", "C49"]),
    ("ANCHOR · logo",       ["C50", "T56"]),
    ("ANCHOR · borderline", ["C47", "C41"]),
    ("CONTROL · famous-as-sung-song (expect lower as bare melody)",
                            ["C22", "C23", "C48", "C26", "C21"]),
]

out = ["# entmotif CANON scores — calibration bundle",
       "",
       "Real, famous themes, each reduced to its identifiable phrase in ABC.",
       "Tiers per `canon/tiers.md` (axis: *memorable as UNSUNG instrumental music*).",
       "ANCHORs are the calibration target (expect A/B); CONTROLs are famous-as-sung",
       "songs expected to grade lower as bare melody. Each ABC's `% confidence:` tag",
       "flags transcription certainty; weigh a low grade on a low-confidence file",
       "accordingly. The `C:` header gives composer/year; chords are in \"quotes\".",
       ""]

n = 0
missing = []
for tier, ids in MANIFEST:
    out.append("## %s" % tier)
    out.append("")
    for cid in ids:
        path = os.path.join(ABC, cid + ".abc")
        if not os.path.exists(path):
            missing.append(cid)
            continue
        n += 1
        abc = open(path).read().rstrip()
        out.append("### %s" % cid)
        out.append("```abc\n%s\n```\n" % abc)

path = os.path.join(HERE, "scores-canon.md")
open(path, "w").write("\n".join(out))
print("wrote %s (%d scores)" % (path, n))
if missing:
    print("MISSING (not yet transcribed): %s" % ", ".join(missing))
